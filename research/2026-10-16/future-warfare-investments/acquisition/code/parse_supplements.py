#!/usr/bin/env python3
"""Parse downloaded XML, PDF, HTML and institutional tables without paid classifiers."""
import collections,csv,gzip,hashlib,io,json,pathlib,re,subprocess,sys,xml.etree.ElementTree as ET,zipfile
from bs4 import BeautifulSoup
import pandas as pd
from acquire import ROOT,DATA,save_json
from normalize import Writer,record,iso,tags,digest,money
MANIFEST=[json.loads(x) for x in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines()]
def meta(p):return next((x for x in reversed(MANIFEST) if x.get('relative_path')==str(p.relative_to(DATA)) and x['outcome']=='downloaded'),{})
def grants():
 p=next((DATA/'raw/grants').glob('*.zip'));z=zipfile.ZipFile(p);w=Writer('grants');years=collections.Counter();sel_years=collections.Counter();agencies=collections.Counter();counts=collections.Counter();missing=collections.Counter();dates=[];selected_dates=[];seen=set();dup=0;samples=[];mm=meta(p)
 moneyfields=['AwardCeiling','AwardFloor','EstimatedTotalProgramFunding'];field_counts=collections.Counter();selected_source=[];source_f=gzip.open(DATA/'normalized/grants_selected_source.jsonl.gz','wt')
 for event,el in ET.iterparse(z.open(z.namelist()[0]),events=['end']):
  if el.tag.rsplit('}',1)[-1] not in ['OpportunitySynopsisDetail_1_0','OpportunityForecastDetail_1_0']:continue
  r={};original_fields=collections.defaultdict(list);kind=el.tag.rsplit('}',1)[-1]
  for c in el:
   k=c.tag.rsplit('}',1)[-1];original_fields[k].append(c.text or '')
   if k in r:r[k]+=';'+(c.text or '')
   else:r[k]=c.text or ''
  field_counts.update(r.keys());counts[kind]+=1;dt=iso(r.get('PostDate',''));yr=str(int(dt[:4])+(int(dt[5:7])>=10)) if dt else '';years[yr]+=1;ag=r.get('AgencyCode','');agencies[ag]+=1
  for k in ['OpportunityID','OpportunityNumber','PostDate']+moneyfields:
   if not r.get(k):missing[k]+=1
  if dt:dates.append(dt)
  title=r.get('OpportunityTitle','');text=BeautifulSoup(r.get('Description',''),'html.parser').get_text(' ',strip=True);ts=tags(title+' '+text)
  keep=bool(dt and '2018-10-01'<=dt<='2026-09-30' and (ag.startswith(('DOD','DOW')) or (ag.startswith(('DOE','DHS','DOS')) and ts)))
  if keep:
   source_f.write(json.dumps({'record_kind':kind,'fields':dict(original_fields),'source_snapshot_sha256':mm['sha256']},ensure_ascii=False)+'\n');selected_source.append(dict(r,_record_kind=kind))
   sel_years[yr]+=1;selected_dates.append(dt);sid=r.get('OpportunityID')+'|'+r.get('Version','')+'|'+kind
   if sid in seen:dup+=1
   seen.add(sid)
   out=record(document_id='grants:'+digest(sid),source='grants',source_record_id=sid,source_url='https://www.grants.gov/search-results-detail/'+r.get('OpportunityID',''),raw_locator=p.name+':'+z.namelist()[0]+':OpportunityID='+r.get('OpportunityID',''),award_key=r.get('OpportunityNumber'),title=title,text=text,action_date=dt,fiscal_year=yr,capability_tags=json.dumps(ts),eligibility='funding_intent_only;'+('security_agency_candidate' if ag.startswith(('DOD','DOW')) else 'mission_review_required'),money_json=json.dumps({k:money(r.get(k,'')) for k in moneyfields}),evidence_excerpt=text[:650],retrieved_at=mm.get('retrieved_at'),source_snapshot_sha256=mm['sha256'],record_sha256=digest(json.dumps(r,sort_keys=True)),identifiers_json=json.dumps({k:r.get(k) for k in ['OpportunityID','OpportunityNumber','Version','AgencyCode','CFDANumbers']}))
   w.write(out)
   if len(samples)<8 and ts:samples.append(out)
  el.clear()
 w.close();source_f.close();pd.DataFrame(selected_source).fillna('').to_parquet(DATA/'normalized/grants_selected_source.parquet',index=False);save_json(ROOT/'validation/grants_profile.json',{'record_kinds':dict(counts),'field_presence_counts_raw':dict(field_counts),'raw_rows':sum(counts.values()),'retained_rows':sum(sel_years.values()),'raw_year_counts':dict(sorted(years.items())),'retained_year_counts':dict(sorted(sel_years.items())),'agency_counts':dict(agencies),'missing_raw':dict(missing),'duplicate_retained_ids':dup,'raw_post_date_range':[min(dates),max(dates)],'retained_post_date_range':[min(selected_dates),max(selected_dates)],'date_semantics':'PostDate; fiscal year derived; not award/action date','money_fields':moneyfields,'uncompressed_bytes':sum(x.file_size for x in z.infolist())})
 (ROOT/'samples/grants.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in samples));print('grants',dict(counts),'selected',sum(sel_years.values()),flush=True)
def pdfs():
 profiles=[]
 for source in ['darpa_budget','govinfo_budget','navy_budget','army_budget','commons','apfit','doe_ldrd','sandia_ldrd']:
  w=Writer(source+'_pages');samples=[]
  for p in sorted((DATA/'raw'/source).glob('*.pdf')):
   m=meta(p)
   if p.read_bytes()[:4]!=b'%PDF':profiles.append({'file':str(p),'error':'not PDF signature'});continue
   r=subprocess.run(['pdftotext','-layout',str(p),'-'],capture_output=True,text=True);pages=r.stdout.split('\f')
   if pages[-1]=='':pages.pop()
   raw_text_chars=sum(map(len,pages));ocr_path=DATA/'normalized'/f'{p.stem}.ocr.json';used_ocr=False
   if ocr_path.exists():
    ocr=json.loads(ocr_path.read_text());pages=[ocr['pages'].get(str(i+1),t) if not t.strip() else t for i,t in enumerate(pages)];used_ocr=True
   count=0;pes=set();amounts=[]
   for num,text in enumerate(pages,1):
    ids=sorted(set(re.findall(r'\b(?:0[2368]|1[02])\d{5}[A-Z][A-Z0-9]{0,3}\b',text)));pes.update(ids);amts=re.findall(r'\$\s*[\d,]+(?:\.\d+)?\s*(?:[MBmb]|million|billion)?',text);amounts+=amts
    sid=m['sha256']+f'#page={num}';out=record(document_id=source+':'+sid,source=source,source_record_id=sid,source_url=m['url']+f'#page={num}',raw_locator=str(p.relative_to(DATA))+f'#page={num}',award_key=';'.join(ids) or None,title=p.name+f' page {num}',text=text,capability_tags=json.dumps(tags(text)),eligibility='context_document;manual_money_table_review_required'+(';ocr_text_review_required' if used_ocr else ''),money_json=json.dumps({'uninterpreted_currency_mentions':amts}),evidence_excerpt=text[:650],retrieved_at=m['retrieved_at'],source_snapshot_sha256=m['sha256'],record_sha256=digest(text),identifiers_json=json.dumps({'program_element_references':ids,'extraction_method':'tesseract_ocr' if used_ocr else 'pdftotext_layout'}));w.write(out);count+=1
    if len(samples)<3 and tags(text):samples.append(out)
   profiles.append({'source':source,'file':p.name,'sha256':m['sha256'],'pages':count,'nonempty_pages':sum(bool(t.strip()) for t in pages),'text_chars':sum(map(len,pages)),'raw_pdftotext_chars':raw_text_chars,'used_ocr':used_ocr,'program_element_identifiers':sorted(pes),'currency_mentions':len(amounts),'pdftotext_stderr':r.stderr[:1500],'warning':'Page records are evidence units, not projects or financial rows. Currency mentions deliberately not coerced to amounts.'})
  w.close()
  if samples:(ROOT/'samples'/f'{source}_pages.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in samples))
 save_json(ROOT/'validation/pdf_profiles.json',profiles);print('pdf pages',sum(x.get('pages',0) for x in profiles),flush=True)
def ffrdc():
 p=next((DATA/'raw/ffrdc').glob('*.zip'));z=zipfile.ZipFile(p);n=next(n for n in z.namelist() if n.endswith('.csv'));df=pd.read_csv(z.open(n),dtype=str,keep_default_na=False)
 # Full finite FY2025 survey, not a contract/award universe.
 df.to_parquet(DATA/'normalized/ffrdc_source.parquet',index=False);df.to_json(DATA/'normalized/ffrdc_source.jsonl.gz',orient='records',lines=True,compression='gzip')
 save_json(ROOT/'validation/ffrdc_profile.json',{'rows':len(df),'columns':list(df.columns),'year_counts':df.year.value_counts().to_dict(),'institutions':df.inst_id.nunique(),'missing':(df=='').sum().to_dict(),'duplicate_row_count':int(df.duplicated().sum()),'duplicate_composite_key':int(df.duplicated(['inst_id','year','questionnaire_no','row','column']).sum()),'question_counts':df.question.value_counts().to_dict(),'data_semantics':'Survey separately accounted R&D expenditure, thousands of dollars, verified questionnaire sections 1-3. Organization fiscal year 2025 may differ from federal FY. No sum across source/agency/type/field breakdowns.'})
 df.head(8).to_csv(ROOT/'samples/ffrdc.csv',index=False)
 out=df.copy();out['document_id']=['ffrdc:'+str(i)+'|'+y+'|'+q+'|'+r+'|'+c for i,y,q,r,c in zip(out.inst_id,out.year,out.questionnaire_no,out.row,out.column)];out['unit']='USD_thousands';out['fiscal_year_semantics']='organization FY2025; not necessarily federal FY';out['source_url']=meta(p)['url'];out['source_snapshot_sha256']=meta(p)['sha256'];out['retrieved_at']=meta(p)['retrieved_at'];out['measure']='institutional_R&D_expenditures';out.to_parquet(DATA/'normalized/ffrdc_expenditures.parquet',index=False)
 print('ffrdc',len(df),flush=True)
def html():
 p=DATA/'raw/apfit/index.html';s=BeautifulSoup(p.read_text(),'html.parser');main=s.find('main') or s;tables=[]
 for i,t in enumerate(main.find_all('table')):
  rows=[[c.get_text(' ',strip=True) for c in tr.find_all(['th','td'])] for tr in t.find_all('tr')];tables.append({'table':i,'rows':rows})
 save_json(DATA/'normalized/apfit_tables.json',tables)
 (DATA/'normalized/apfit_index.txt').write_text(main.get_text('\n',strip=True))
 save_json(ROOT/'validation/apfit_html_profile.json',{'tables':len(tables),'table_row_counts':[len(t['rows']) for t in tables],'page_text_chars':len(main.get_text()),'note':'HTML tables are preserved verbatim; fiscal cohorts/selection dollars not transaction obligations.'})
if __name__=='__main__':
 for task in sys.argv[1:] or ['grants','pdfs','ffrdc','html']:globals()[task]()
