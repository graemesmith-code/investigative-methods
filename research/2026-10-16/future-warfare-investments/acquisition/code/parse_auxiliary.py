#!/usr/bin/env python3
"""Preserve full transaction/source schemas; parse subawards, finite survey tables, PSC lookup."""
import collections,csv,io,json,pathlib,re,sys,zipfile,warnings
import pandas as pd,pyarrow as pa,pyarrow.parquet as pq
from acquire import ROOT,DATA,save_json
from normalize import Writer,record,tags,iso,money,digest
warnings.filterwarnings('ignore',message='Workbook contains no default style')
def transactions(source):
 p=next((DATA/'raw'/source).glob('*.zip'));z=zipfile.ZipFile(p);mm=next(json.loads(x) for x in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines() if json.loads(x).get('relative_path')==str(p.relative_to(DATA)));profiles=[];schemas={}
 for name in z.namelist():
  if not name.endswith('.csv'):continue
  suffix='subawards' if 'Subawards' in name else 'transactions';outfile=DATA/'normalized'/f'{source}_{suffix}_source.parquet';pw=None;rows=0;missing=collections.Counter();ids=set();duplicates=0;datevalues=[];years=collections.Counter();moneyprofiles={};examples=[];subw=Writer(source+'_subawards') if suffix=='subawards' else None
  for chunk in pd.read_csv(z.open(name),dtype=str,keep_default_na=False,chunksize=10000):
   schemas[name]=list(chunk.columns);rows+=len(chunk);missing.update((chunk=='').sum().to_dict());t=pa.Table.from_pandas(chunk,preserve_index=False)
   if pw is None:pw=pq.ParquetWriter(outfile,t.schema,compression='zstd')
   pw.write_table(t)
   amountfields=[k for k in chunk.columns if any(s in k for s in ['obligation','obligated','outlay','_value','_amount','loan_subsidy_cost']) and not k.endswith(('code','description','name'))]
   for k in amountfields:
    s=pd.to_numeric(chunk[k],errors='coerce');v=moneyprofiles.setdefault(k,{'nonempty':0,'invalid_nonempty':0,'negative':0,'zero':0,'positive':0});v['nonempty']+=int((chunk[k]!='').sum());v['invalid_nonempty']+=int(((chunk[k]!='')&s.isna()).sum());v['negative']+=int((s<0).sum());v['zero']+=int((s==0).sum());v['positive']+=int((s>0).sum())
   datekey='subaward_action_date' if suffix=='subawards' else 'action_date';yk=datekey+'_fiscal_year'
   if datekey in chunk:
    datevalues.extend(x for x in chunk[datekey] if x);years.update(chunk[yk] if yk in chunk else [])
   if suffix!='subawards':continue
   for r in chunk.to_dict('records'):
    key='|'.join(r.get(k,'') for k in ['prime_award_unique_key','subaward_sam_report_id','subaward_number','subaward_action_date'])
    if key in ids:duplicates+=1
    ids.add(key);h=digest(json.dumps(r,sort_keys=True));text=r.get('subaward_description','');out=record(document_id=source+'_subaward:'+digest(key+'|'+h),source=source+'_subawards',source_record_id=key,source_url=r.get('usaspending_permalink'),raw_locator=p.name+':'+name+':key='+key,award_key=r.get('prime_award_unique_key'),entity_key=r.get('subawardee_uei') or r.get('subawardee_duns'),entity_name=r.get('subawardee_name'),title=r.get('subaward_number'),text=text,action_date=iso(r.get(datekey,'')),fiscal_year=r.get(yk),capability_tags=json.dumps(tags(text)),eligibility='reported_first_tier_subaward;do_not_add_to_prime_spending',money_json=json.dumps({k:money(r.get(k,'')) for k in amountfields}),evidence_excerpt=text[:650],retrieved_at=mm['retrieved_at'],record_sha256=h,source_snapshot_sha256=mm['sha256'],identifiers_json=json.dumps({k:r.get(k) for k in ['prime_award_unique_key','prime_award_piid','subaward_sam_report_id','subaward_number','subawardee_uei','subawardee_duns']}));subw.write(out)
    if len(examples)<5 and tags(text):examples.append(out)
  if pw:pw.close()
  if subw:
   subw.close();(ROOT/'samples'/f'{source}_subawards.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in examples))
  profiles.append({'csv':name,'kind':suffix,'rows':rows,'columns':len(schemas[name]),'missing_fields':dict(missing),'money_value_checks':moneyprofiles,'action_date_min':min(datevalues) if datevalues else None,'action_date_max':max(datevalues) if datevalues else None,'year_counts':dict(sorted(years.items())),'duplicate_subaward_composite_keys':duplicates if suffix=='subawards' else None})
 save_json(ROOT/'validation'/f'{source}_source_table_profiles.json',profiles);save_json(ROOT/'validation'/f'{source}_schemas.json',schemas);print(source,[(r['kind'],r['rows']) for r in profiles],flush=True)
def federal_funds():
 p=next((DATA/'raw/federal_funds').glob('*.zip'));z=zipfile.ZipFile(p);catalog=[];records=[]
 for name in z.namelist():
  if not name.endswith('.xlsx'):continue
  x=pd.ExcelFile(z.open(name))
  for sheet in x.sheet_names:
   df=pd.read_excel(x,sheet_name=sheet,header=None,dtype=str,keep_default_na=False);first=' '.join(str(v) for v in df.head(6).to_numpy().flatten() if v);units=next((str(v) for v in df.head(6).to_numpy().flatten() if 'Dollars in' in str(v) or 'Percent' in str(v)),None)
   catalog.append({'file':name,'sheet':sheet,'rows':len(df),'columns':len(df.columns),'header_excerpt':first[:1500],'units_header':units,'numeric_cells':sum(pd.to_numeric(df[c],errors='coerce').notna().sum().item() for c in df.columns)})
   for i,r in df.iterrows():records.append({'source_file':name,'source_sheet':sheet,'excel_row':int(i)+1,'units_header':units,'cells_json':json.dumps(list(r))})
 df=pd.DataFrame(records);df.to_parquet(DATA/'normalized/federal_funds_source_rows.parquet',index=False);df.to_json(DATA/'normalized/federal_funds_source_rows.jsonl.gz',orient='records',lines=True,compression='gzip');save_json(ROOT/'validation/federal_funds_table_catalog.json',catalog);save_json(ROOT/'validation/federal_funds_profile.json',{'zip_members':len(z.namelist()),'workbooks':len(set(r['file'] for r in catalog)),'sheets':len(catalog),'parsed_rows_including_headers_footnotes':len(df),'numeric_cells':sum(r['numeric_cells'] for r in catalog),'unit_headers':dict(collections.Counter(r['units_header'] for r in catalog)),'warning':'Lossless positional table rows, not independent observations. Units vary by table; FY2025 preliminary. Retain footnotes, suppression markers and revised historical values. These are reported federal obligations/outlays, not FFRDC expenditure.'});pd.DataFrame(catalog).head(8).to_csv(ROOT/'samples/federal_funds_tables.csv',index=False);print('federal funds',len(catalog),'sheets',len(df),'rows',flush=True)
def psc():
 p=DATA/'raw/psc/PSC_April_2025.xlsx';x=pd.ExcelFile(p);profiles=[]
 for sheet in x.sheet_names:
  df=pd.read_excel(x,sheet_name=sheet,header=None,dtype=str,keep_default_na=False);profiles.append({'sheet':sheet,'rows':len(df),'columns':len(df.columns),'first_rows':df.head(4).values.tolist()});df.columns=[str(c) for c in df.columns];safe=re.sub(r'[^A-Za-z0-9]+','_',sheet);df.to_parquet(DATA/'normalized'/f'psc_{safe}.parquet',index=False)
 save_json(ROOT/'validation/psc_profile.json',profiles);print('PSC',[(x['sheet'],x['rows']) for x in profiles],flush=True)
if __name__=='__main__':
 for arg in sys.argv[1:]:
  if arg.startswith('usaspending_'):transactions(arg)
  else:globals()[arg]()
