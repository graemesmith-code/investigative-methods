#!/usr/bin/env python3
"""Validate complete OMB workbooks; normalize security-account FY2019-26 cells with vintage."""
import collections,csv,io,json,pathlib,re,subprocess,zipfile
from decimal import Decimal
import pandas as pd
from acquire import ROOT,DATA,save_json
from normalize import digest

def omb():
 manifest=[json.loads(x) for x in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines()];records=[];profiles=[]
 for p in sorted((DATA/'raw/omb_budget').glob('*.xlsx')):
  vintage=int(re.search(r'PB(\d{4})',p.name)[1]);measure='budget_authority_net' if 'authority' in p.name else 'outlays_net';df=pd.read_excel(p,dtype=str,keep_default_na=False);df.columns=[str(c) for c in df.columns];meta=next(x for x in manifest if x.get('relative_path')==str(p.relative_to(DATA)))
  yearcols=[k for k in df.columns if re.fullmatch(r'\d{4}',k)];keys=[k for k in df.columns if k not in yearcols and k!='TQ'];bound=[str(y) for y in range(2019,2027) if str(y) in df.columns]
  sec=df[df['Agency Name'].str.contains('Defense|War|Energy|Homeland Security|State|International Assistance',case=False,regex=True)]
  missing={k:int((df[k]=='').sum()) for k in keys};duplicates=int(df.duplicated(keys).sum());retained=0;non_numeric=[]
  for i,r in sec.iterrows():
   identity={k:r[k] for k in keys};key=json.dumps(identity,sort_keys=True)
   for year in bound:
    v=r[year];num=pd.to_numeric(v,errors='coerce')
    if v and pd.isna(num):non_numeric.append({'excel_row':int(i)+2,'year':year,'value':v})
    rec={'document_id':'omb:'+digest(p.name+'|'+key+'|'+year),'source':'omb_budget','source_url':meta['url'],'source_snapshot_sha256':meta['sha256'],'retrieved_at':meta['retrieved_at'],'raw_file':p.name,'raw_locator':str(p.relative_to(DATA))+f'#sheet=Sheet1&row={int(i)+2}','excel_sheet':'Sheet1','excel_row':int(i)+2,'budget_vintage':vintage,'fiscal_year':int(year),'measure':measure,'value_in_source_units':v,'unit':'USD_thousands','amount_usd':str(Decimal(v)*1000) if pd.notna(num) else None,'status':'actual_as_revised_in_vintage' if int(year)<=vintage-2 else ('current_year_estimate' if int(year)==vintage-1 else 'budget_year_or_future_estimate'),'account_key':r['Agency Code']+'|'+r['Bureau Code']+'|'+r['Account Code'],'dimensions_json':key,'eligibility':'security_institution_context;capability_and_mission_review_required'}
    records.append(rec);retained+=1
  profiles.append({'file':p.name,'rows':len(df),'columns':len(df.columns),'min_year_column':min(yearcols),'max_year_column':max(yearcols),'security_rows':len(sec),'retained_long_rows':retained,'retained_years':bound,'missing_key_fields':missing,'duplicate_full_dimension_rows':duplicates,'nonnumeric_retained_cells':non_numeric[:50],'note':'Full raw workbooks parsed. All agency/account subsets retained as context, not all eligible capability spending. Amounts are net of offsetting collections; negative receipts must remain signed. Vintage-specific estimates cannot be added to actuals from another vintage.'})
  # Retain lossless structured full table and full source keys for future alternate slicing.
  df.to_parquet(DATA/'normalized'/(p.stem+'_source.parquet'),index=False)
 d=pd.DataFrame(records);d.to_parquet(DATA/'normalized/omb_security_fy2019_2026.parquet',index=False);d.to_json(DATA/'normalized/omb_security_fy2019_2026.jsonl.gz',orient='records',lines=True,compression='gzip');d.head(10).to_csv(ROOT/'samples/omb_budget.csv',index=False);save_json(ROOT/'validation/omb_budget_profiles.json',profiles);print('OMB',len(records),'cells',flush=True)
def darpa():
 p=DATA/'raw/darpa_budget/DARPA_PB2025.pdf';r=subprocess.run(['pdftotext','-layout',str(p),'-'],capture_output=True,text=True);pages=r.stdout.split('\f');records=[];unparsed=[]
 m=next(json.loads(x) for x in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines() if json.loads(x).get('relative_path')==str(p.relative_to(DATA)))
 for page,text in enumerate(pages,1):
  if 'Accomplishments/Planned Programs ($ in Millions)' not in text:continue
  pe=re.findall(r'\bPE\s+(\d{7}[A-Z][A-Z0-9]{0,3})\b',text);prj=re.search(r'\b([A-Z]{2,5}-\d{2})\s*/',text)
  lines=text.splitlines()
  for k,line in enumerate(lines):
   if not line.startswith('Title:'):continue
   chunks=re.split(r'\s{2,}',line.strip());title=chunks[0][6:].strip();values=chunks[1:]
   if len(values)!=3 or not all(re.fullmatch(r'-|\d[\d,]*\.\d{3}',v) for v in values):unparsed.append({'page':page,'line':line});continue
   end=next((j for j in range(k+1,len(lines)) if lines[j].startswith('Title:') or lines[j].startswith('PE ')),len(lines));body='\n'.join(lines[k:end]);key=(pe[0] if pe else '')+'|'+(prj[1] if prj else '')+'|'+title
   records.append({'document_id':'darpa_program:'+digest(m['sha256']+'|'+key+'|'+str(page)),'source_url':m['url']+f'#page={page}','source':'darpa_budget','source_snapshot_sha256':m['sha256'],'retrieved_at':m['retrieved_at'],'raw_locator':str(p.relative_to(DATA))+f'#page={page}','raw_page':page,'program_element':pe[0] if pe else None,'project':prj[1] if prj else None,'title':title,'text_page_excerpt':body,'budget_vintage':2025,'FY2023_reported_program_amount_millions':values[0],'FY2024_reported_program_amount_millions':values[1],'FY2025_requested_program_amount_millions':values[2],'money_semantics':'R-2/R-2A accomplishments/planned-program funding columns; USD millions. Prior/current-year exhibit amounts are not asserted to be award obligations or outlays; dash is not coerced to zero. FY2025 is proposed request. Do not add program/project/PE totals or cross-PE references.'})
 d=pd.DataFrame(records);d.to_parquet(DATA/'normalized/darpa_pb2025_programs.parquet',index=False);d.to_json(DATA/'normalized/darpa_pb2025_programs.jsonl.gz',orient='records',lines=True,compression='gzip');d.head(5).to_json(ROOT/'samples/darpa_programs.jsonl',orient='records',lines=True)
 save_json(ROOT/'validation/darpa_program_profile.json',{'parsed_title_rows':len(d),'unparsed_title_rows':unparsed,'missing_program_element':int(d.program_element.isna().sum()),'missing_project':int(d.project.isna().sum()),'duplicate_pe_project_title':int(d.duplicated(['program_element','project','title']).sum()),'warning':'Automated title-row extraction, not a complete financial table. Full page corpus remains authoritative; wrapped titles and continuation descriptions need review.'});print('DARPA program rows',len(d),'unparsed',len(unparsed),flush=True)
if __name__=='__main__':omb();darpa()
