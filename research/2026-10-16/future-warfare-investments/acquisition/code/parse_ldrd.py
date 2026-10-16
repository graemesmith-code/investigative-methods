#!/usr/bin/env python3
"""Table1 annual lab finances, FY2019-25. Two scan tables manually checked against page images."""
import collections,json,re,subprocess
from decimal import Decimal
import pandas as pd
from acquire import ROOT,DATA,save_json
from normalize import digest
manifest=[json.loads(x) for x in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines()];manual=pd.read_csv(ROOT/'evidence/ldrd_scanned_table1_transcription.csv',dtype=str,keep_default_na=False);rows=[];profiles=[]
pattern=re.compile(r'^\s*(.*?)\s+\$?([\d,]+\.\d{2})\s+\$?([\d,]+\.\d{2})\s+\$?([\d,]+\.\d{2})\s+\$?([\d,]+\.\d{2})\s+([\d.]+)%\s+([\d,]+)\s*$')
for p in sorted((DATA/'raw/doe_ldrd').glob('*.pdf')):
 year=int(re.search(r'FY(\d{4})',p.name)[1]);m=next(x for x in manifest if x.get('relative_path')==str(p.relative_to(DATA)) and x['outcome']=='downloaded');records=[]
 if year in [2019,2021]:
  for r in manual[manual.fiscal_year==str(year)].to_dict('records'):r['extraction_method']='manual_transcription_checked_against_rendered_source_page';records.append(r)
 else:
  text=subprocess.run(['pdftotext','-layout',str(p),'-'],capture_output=True,text=True).stdout;pages=text.split('\f')
  for page,t in enumerate(pages,1):
   if 'DOE Costs' not in t or 'Ames' not in t:continue
   for line in t.splitlines():
    mat=pattern.match(line)
    if mat:
     lab,*vals=mat.groups();r=dict(zip(['laboratory_label_raw','doe_cost_millions','spp_cost_millions','total_cost_millions','ldrd_cost_millions','ldrd_rate_percent','projects'],[lab]+[v.replace(',','') for v in vals]));r.update(fiscal_year=str(year),physical_pdf_page=str(page),extraction_method='pdftotext_layout_regex');records.append(r)
 for r in records:
  r.update(document_id='doe_ldrd_table1:'+digest(str(year)+'|'+r['laboratory_label_raw']),source_url=m['url']+'#page='+r['physical_pdf_page'],source_snapshot_sha256=m['sha256'],retrieved_at=m['retrieved_at'],raw_file=p.name,table='Table 1',row_kind='total' if r['laboratory_label_raw'].lower().startswith('total') else 'laboratory',unit='USD_millions',financial_semantics='DOE and Strategic Partnership Projects (SPP) laboratory costs; total cost base and LDRD costs in millions. LDRD is an institutional expenditure funded through overhead, not new prime awards. Total row nests lab rows. Do not add LDRD costs to inclusive laboratory totals or federal contracts.',eligibility='institutional_context;security_mission_requires_project_evidence')
  r['cost_components_rounding_difference_millions']=str(Decimal(r['doe_cost_millions'])+Decimal(r['spp_cost_millions'])-Decimal(r['total_cost_millions']))
  rows.append(r)
 labs=[r for r in records if r['row_kind']=='laboratory'];totals=[r for r in records if r['row_kind']=='total'];profiles.append({'year':year,'rows':len(records),'laboratories':len(labs),'total_rows':len(totals),'project_sum_labs':sum(int(r['projects']) for r in labs),'project_total_reported':int(totals[0]['projects']) if totals else None,'ldrd_cost_sum_labs_millions':str(sum(Decimal(r['ldrd_cost_millions']) for r in labs)),'ldrd_cost_reported_total_millions':totals[0]['ldrd_cost_millions'] if totals else None,'max_component_rounding_difference_millions':str(max([abs(Decimal(r['cost_components_rounding_difference_millions'])) for r in records],default=Decimal(0))),'extraction_methods':list(set(r['extraction_method'] for r in records))})
df=pd.DataFrame(rows);df.to_parquet(DATA/'normalized/doe_ldrd_table1_fy2019_2025.parquet',index=False);df.to_json(DATA/'normalized/doe_ldrd_table1_fy2019_2025.jsonl.gz',orient='records',lines=True,compression='gzip');df[df.fiscal_year=='2025'].to_csv(ROOT/'samples/doe_ldrd_fy2025.csv',index=False);save_json(ROOT/'validation/doe_ldrd_finance_profile.json',{'rows':len(df),'year_profiles':profiles,'scan_method':'FY2019 and FY2021 Table1, physical PDF page8, manually transcribed and visually checked against full-resolution rendered page. Whole-document OCR is supplementary and unreliable for monetary tables.','checks':{'all_seven_fiscal_years':len(profiles)==7,'exactly_one_total_per_year':all(p['total_rows']==1 for p in profiles),'project_counts_reconcile_each_year':all(p['project_sum_labs']==p['project_total_reported'] for p in profiles)},'warning':'Source financial bases are not identical to Sandia report cost excluding PM. Historical overhead/accounting scope and rounding need review. Do not infer all DOE laboratories or expenditures are military.'});print('DOE LDRD finances',len(df),profiles)
