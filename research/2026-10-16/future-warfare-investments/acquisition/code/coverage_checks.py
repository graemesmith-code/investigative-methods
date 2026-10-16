#!/usr/bin/env python3
"""Describe count/export discrepancies and single-FY diagnostics without inferring a cause."""
import json,pathlib
import pandas as pd
from acquire import ROOT,DATA,save_json
findings=[];subaward_checks=[]
for p in sorted((ROOT/'validation').glob('usaspending_*_source_table_profiles.json')):
 source=p.name.removesuffix('_source_table_profiles.json');count_path=ROOT/'evidence'/f'{source}_count.json'
 if not count_path.exists():continue
 sp=ROOT/'evidence'/f'{source}_subaward_download_count.json'
 if sp.exists():
  expected_sub=json.loads(sp.read_text())['calculated_count'];actual_sub=sum(x['rows'] for x in json.loads(p.read_text()) if x['kind']=='subawards');subaward_checks.append({'source':source,'subaward_count_endpoint':expected_sub,'parsed_subaward_rows':actual_sub,'difference':expected_sub-actual_sub,'note':'Five-record difference for full R&D extract; source/replica/snapshot/filter cause unestablished. Export totals match generator, not represented as a subaward census.'})
 count=sum(json.loads(count_path.read_text())['results'].values());prof=json.loads(p.read_text());actual=sum(x['rows'] for x in prof if x['kind']=='transactions');dp=ROOT/'evidence'/f'{source}_download_count.json';download_count=json.loads(dp.read_text())['calculated_count'] if dp.exists() else None;findings.append({'source':source,'search_count_endpoint_prime_transactions':count,'download_count_endpoint_prime_transactions':download_count,'parsed_prime_transactions':actual,'search_count_minus_export':count-actual,'equal':count==actual,'export_matches_download_count':actual==download_count if download_count is not None else None,'interpretation':'Matched search count' if count==actual else ('Export exactly matches download-route count; search-count route differs. Counts from routes are not interchangeable; no shortfall relative to download count observed.' if actual==download_count else 'Unresolved count/export discrepancy')})
broad=DATA/'normalized/usaspending_dod_capabilities.parquet';diagnostics=[]
if broad.exists():
 b=pd.read_parquet(broad,columns=['transaction_key','fiscal_year'])
 for year in [2019,2026]:
  p=DATA/'normalized'/f'usaspending_dod_capabilities_fy{year}.parquet'
  if not p.exists():continue
  s=pd.read_parquet(p,columns=['transaction_key']);bs=set(b[b.fiscal_year==str(year)].transaction_key);ss=set(s.transaction_key);diagnostics.append({'fiscal_year':year,'broad_export_year_unique_keys':len(bs),'single_year_export_unique_keys':len(ss),'single_year_added_keys':len(ss-bs),'broad_year_absent_from_single_year':len(bs-ss),'same_key_sets':bs==ss})
save_json(ROOT/'validation/count_export_comparison.json',{'sources':findings,'subaward_count_checks':subaward_checks,'single_year_keyword_diagnostics':diagnostics,'count_after_download_confirmed':json.loads((ROOT/'evidence/usaspending_dod_capabilities_count_after_download.json').read_text()),'scope':'Observed downloaded files and corresponding public count responses only. No inference that absent records were deleted, classified or deliberately withheld. Smaller-window equality does not prove whole-source completeness.'})
print(json.dumps({'count_discrepancies':[f for f in findings if not f['equal']],'single_year_diagnostics':diagnostics}))
