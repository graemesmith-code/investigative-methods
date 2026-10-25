import pathlib,csv,json,gzip,hashlib,collections
from decimal import Decimal as D
R=pathlib.Path(__file__).parent
S=pathlib.Path('/workspace/shared/f4-stage1-recovery/input/FWI-20261016-normalized-research-context/normalized/financial_actions.jsonl.gz')
A=pathlib.Path('/workspace/shared/f4-editor-recovery/sources/evidence/fpds-verified-actions.csv')
keys={'CONT_AWD_FD01_9700_N0017814D7932_9700','CONT_AWD_N0016422F3007_9700_N0017819D7763_9700','CONT_AWD_N0042123F3004_9700_N0017819D7484_9700'}
local=[];scanned=0
with gzip.open(S,'rt') as f:
 for l in f:
  scanned+=1
  if any(k in l for k in keys):
   x=json.loads(l)
   if x['award_key'] in keys:local.append(x)
actions=[r for r in csv.DictReader(A.open()) if r['award_key'] in keys]
identity=lambda r:'_'.join([r['agency_id'],r['parent_agency_id'] or '-NONE-',r['piid'],r['modification'],r['parent_piid'] or '-NONE-',r['transaction'] or '0'])
out=[];errors=[];missing=[]
for k in sorted(keys):
 a={r['transaction_key']:r for r in local if r['award_key']==k and '2018-10-01'<=r['action_date']<='2026-09-30'}
 b={identity(r):r for r in actions if r['award_key']==k and '2018-10-01'<=r['signed_date'][:10]<='2026-09-30'}
 for z in a.keys()&b.keys():
  if D(a[z]['action_obligation_usd'])!=D(b[z]['obligation_usd']) or a[z]['action_date']!=b[z]['signed_date'][:10]:errors.append({'key':z,'kind':'shared_action_mismatch'})
 for z in b.keys()-a.keys():missing.append({'award_key':k,'transaction_key':z,'signed_date':b[z]['signed_date'][:10],'obligation_usd':b[z]['obligation_usd']})
 av=sum((D(r['action_obligation_usd']) for r in a.values()),D(0));bv=sum((D(r['obligation_usd']) for r in b.values()),D(0));out.append({'award_key':k,'acquired_rows':len(a),'live_export_FY_rows':len(b),'acquired_obligations_usd':str(av),'live_export_obligations_usd':str(bv),'live_minus_acquired_usd':str(bv-av),'missing_actions':len(b.keys()-a.keys()),'source_acquisition_streams':sorted({r['source'] for r in a.values()})})
result={'source_financial_gzip_sha256':hashlib.file_digest(S.open('rb'),'sha256').hexdigest(),'source_financial_records_scanned':scanned,'retained_FPDS_export_sha256':hashlib.file_digest(A.open('rb'),'sha256').hexdigest(),'acquired_selected_rows':len(local),'retained_FPDS_selected_alltime_rows':len(actions),'same_window':'2018-10-01 through 2026-09-30 inclusive','shared_action_errors':errors,'awards':out,'missing_action_rows':missing,'caveat':'Acquisition-filtered transaction history is not complete award funding. Per-action API matching cause remains unproved; missing deobligations can mean acquired sums are not lower bounds. No change to selected safeguard totals follows from these three nonselected examples.'}
(R/'new-history-reconciliation.json').write_text(json.dumps(result,indent=2));(R/'acquired-three-award-actions.json').write_text(json.dumps(local,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='missing_action_rows'},indent=2));assert not errors
