#!/usr/bin/env python3
"""Describe count/export discrepancies and single-FY diagnostics without inferring a cause."""
import json,pathlib
import pandas as pd
from acquire import ROOT,DATA,save_json
findings=[]
for p in sorted((ROOT/'validation').glob('usaspending_*_source_table_profiles.json')):
 source=p.name.removesuffix('_source_table_profiles.json');count_path=ROOT/'evidence'/f'{source}_count.json'
 if not count_path.exists():continue
 count=sum(json.loads(count_path.read_text())['results'].values());prof=json.loads(p.read_text());actual=sum(x['rows'] for x in prof if x['kind']=='transactions');findings.append({'source':source,'count_endpoint_prime_transactions':count,'parsed_prime_transactions':actual,'difference_count_minus_export':count-actual,'equal':count==actual,'interpretation':'Matched independent count' if count==actual else 'Coverage discrepancy; cause unestablished; do not claim full count-endpoint universe acquired'})
broad=DATA/'normalized/usaspending_dod_capabilities.parquet';diagnostics=[]
if broad.exists():
 b=pd.read_parquet(broad,columns=['transaction_key','fiscal_year'])
 for year in [2019,2026]:
  p=DATA/'normalized'/f'usaspending_dod_capabilities_fy{year}.parquet'
  if not p.exists():continue
  s=pd.read_parquet(p,columns=['transaction_key']);bs=set(b[b.fiscal_year==str(year)].transaction_key);ss=set(s.transaction_key);diagnostics.append({'fiscal_year':year,'broad_export_year_unique_keys':len(bs),'single_year_export_unique_keys':len(ss),'single_year_added_keys':len(ss-bs),'broad_year_absent_from_single_year':len(bs-ss),'same_key_sets':bs==ss})
save_json(ROOT/'validation/count_export_comparison.json',{'sources':findings,'single_year_keyword_diagnostics':diagnostics,'count_after_download_confirmed':json.loads((ROOT/'evidence/usaspending_dod_capabilities_count_after_download.json').read_text()),'scope':'Observed downloaded files and corresponding public count responses only. No inference that absent records were deleted, classified or deliberately withheld. Smaller-window equality does not prove whole-source completeness.'})
print(json.dumps({'count_discrepancies':[f for f in findings if not f['equal']],'single_year_diagnostics':diagnostics}))
