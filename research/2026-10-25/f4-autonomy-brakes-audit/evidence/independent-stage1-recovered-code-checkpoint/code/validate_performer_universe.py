#!/usr/bin/env python3
"""Independent complete recipient-period coverage and monetary QA."""
import pathlib,json,gzip,csv,sys,re,decimal,collections,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'audit/asimov-performer-continuation-local-accounting.json').read_text());rx=[re.compile(p,re.I) for p in a['alias_regexes'].values()]
records=json.loads((ROOT/'evidence/asimov-performer-continuation-local-2025-2026.json').read_text());bykey={r['register_key']:r for r in records};assert len(bykey)==len(records)
prime={r['award_key']:r for r in records if r['record_role']=='prime_or_assistance_financial_award'};sub={r['register_key']:r for r in records if r['record_role']=='reported_first_tier_subrecipient'}
expectedprime=set();expectedsub=set();sums=collections.defaultdict(lambda:collections.defaultdict(decimal.Decimal));seen=set();negative=collections.Counter()
def match(n):return any(p.search(n or '') for p in rx)
def eligible(r):
 fy=int(r.get('fiscal_year') or 0);d=r.get('action_date') or ''
 return 2025<=fy<=2026 or '2025-01-01'<=d<='2026-12-31'
financial=next((ROOT/'input').rglob('financial_actions.jsonl.gz'))
for line in gzip.open(financial,'rt'):
 r=json.loads(line);tx=r['transaction_key'];assert tx not in seen;seen.add(tx);key=r['award_key'];fy=int(r['fiscal_year']);d=r['action_date'];v=decimal.Decimal(r['action_obligation_usd'])
 if match(r.get('entity_name')) and eligible(r):expectedprime.add(key)
 if 2019<=fy<=2026:sums[key]['fy2019_2026']+=v
 if 2024<=fy<=2026:sums[key]['fy2024_2026']+=v
 if 2025<=fy<=2026:sums[key]['fy2025_2026']+=v
 if '2025-01-01'<=d<='2026-12-31':sums[key]['cy2025_2026']+=v
 if v<0:negative[key]+=1
for p in (ROOT/'input').rglob('*_subawards.jsonl.gz'):
 for line in gzip.open(p,'rt'):
  r=json.loads(line)
  if match(r.get('entity_name')) and eligible(r):expectedsub.add('SUBRECIPIENT::'+(r.get('award_key') or '')+'::'+(r.get('entity_key') or r.get('entity_name') or ''))
expected_sbir=set()
for name in ['sbir.jsonl.gz','sbir_current.jsonl.gz']:
 p=next((ROOT/'input').rglob(name))
 for line in gzip.open(p,'rt'):
  r=json.loads(line)
  if match(r.get('entity_name')) and eligible(r):expected_sbir.add((r.get('source_record_id'),r.get('source_snapshot_sha256'),r.get('record_sha256')))
observed_sbir={(s['source_record_id'],s.get('source_snapshot_sha256'),s.get('record_sha256')) for r in records for s in r['sbir_reported_records']}
errors=[];checks=0
for r in records:
 key=r['award_key']
 if key not in sums:continue
 for period in ['fy2019_2026','fy2024_2026','fy2025_2026','cy2025_2026']:
  field='obligations_'+period+'_usd'
  if r['record_role']!='prime_or_assistance_financial_award':
   if r[field] is not None:errors.append({'key':r['register_key'],'error':'Subrecipient has attributed prime obligation','field':field})
   if period not in ['fy2025_2026','cy2025_2026']:continue
   field='parent_award_'+field
  checks+=1
  if decimal.Decimal(r[field])!=sums[key][period]:errors.append({'key':r['register_key'],'field':field,'actual':r[field],'expected':str(sums[key][period])})
 if r['negative_financial_transaction_count']!=negative[key]:errors.append({'key':r['register_key'],'error':'Negative action count mismatch'})
csv.field_size_limit(sys.maxsize)
with (ROOT/'evidence/asimov-performer-continuation-local-2025-2026.csv').open() as f:csvrows=list(csv.DictReader(f))
csvkeys={r['register_key'] for r in csvrows};assert len(csvrows)==len(records)
for r in csvrows:
 j=bykey[r['register_key']]
 for k,v in j.items():
  actual=json.loads(r[k]) if isinstance(v,(list,dict)) else r[k]
  expected=v if isinstance(v,(list,dict)) else '' if v is None else str(v)
  if actual!=expected:errors.append({'key':r['register_key'],'error':'CSV JSON mismatch','field':k})
result={'output_rows':len(records),'csv_rows':len(csvrows),'unique_register_keys':len(bykey),'exact_financial_sum_fields_rechecked':checks,'financial_transaction_keys_rechecked':len(seen),'expected_prime_awards':len(expectedprime),'observed_prime_awards':len(prime),'prime_awards_missing':sorted(expectedprime-set(prime)),'prime_awards_unexpected':sorted(set(prime)-expectedprime),'expected_subrecipient_keys':len(expectedsub),'observed_subrecipient_keys':len(sub),'subrecipient_keys_missing':sorted(expectedsub-set(sub)),'subrecipient_keys_unexpected':sorted(set(sub)-expectedsub),'expected_sbir_snapshot_records':len(expected_sbir),'observed_sbir_snapshot_records':len(observed_sbir),'sbir_records_missing':sorted(expected_sbir-observed_sbir),'sbir_records_unexpected':sorted(observed_sbir-expected_sbir),'csv_missing_keys':sorted(set(bykey)-csvkeys),'errors':errors,'status':'PASS' if not(errors or expectedprime!=set(prime) or expectedsub!=set(sub) or expected_sbir!=observed_sbir or csvkeys!=set(bykey)) else 'FAIL','note':'Validation confirms coverage under documented name regexes and archive period, not identity or real-world completeness.'}
(ROOT/'audit/asimov-performer-continuation-local-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['status']=='PASS'
