#!/usr/bin/env python3
"""Independent date-selection and exact financial/source-key QA; no source mutation."""
import pathlib,json,gzip,hashlib,datetime as dt,collections,csv
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE_FILES=sorted((ROOT/'input').rglob('*_transactions_source.parquet'))
# Exact key equality, not count-only comparison.
source_transactions=set();source_awards=set();map_tx_awards={};source_rows=0
for p in SOURCE_FILES:
 pf=pq.ParquetFile(p);cols=[x for x in ['contract_transaction_unique_key','assistance_transaction_unique_key','contract_award_unique_key','assistance_award_unique_key'] if x in pf.schema_arrow.names]
 for batch in pf.iter_batches(columns=cols,batch_size=32768):
  for row in batch.to_pylist():
   tx=row.get('contract_transaction_unique_key') or row.get('assistance_transaction_unique_key');award=row.get('contract_award_unique_key') or row.get('assistance_award_unique_key')
   source_transactions.add(tx);source_awards.add(award);map_tx_awards.setdefault(tx,set()).add(award);source_rows+=1
financial=next((ROOT/'input').rglob('financial_actions.jsonl.gz'))
financial_transactions=set();financial_awards=set();financial_rows=0;financial_map_conflicts=[]
with gzip.open(financial,'rt') as f:
 for line in f:
  r=json.loads(line);tx=r['transaction_key'];a=r['award_key'];financial_transactions.add(tx);financial_awards.add(a);financial_rows+=1
  if map_tx_awards.get(tx)!={a}:financial_map_conflicts.append({'transaction_key':tx,'financial_award_key':a,'source_award_keys':sorted(map_tx_awards.get(tx,set()))})
control={'source_rows':source_rows,'source_unique_transaction_keys':len(source_transactions),'financial_rows':financial_rows,'financial_unique_transaction_keys':len(financial_transactions),'source_unique_award_keys':len(source_awards),'financial_unique_award_keys':len(financial_awards),'financial_keys_missing_in_sources':sorted(financial_transactions-source_transactions),'source_keys_missing_in_financial':sorted(source_transactions-financial_transactions),'financial_awards_missing_in_sources':sorted(financial_awards-source_awards),'source_awards_missing_in_financial':sorted(source_awards-financial_awards),'transaction_to_award_mismatches':financial_map_conflicts}
(ROOT/'audit/financial-source-key-reconciliation.json').write_text(json.dumps(control,indent=2)+'\n')
# Reconstruct selected fields independently for deterministic sample + ASIMOV and tie cases.
sample={k for k in source_awards if int(hashlib.sha256(k.encode()).hexdigest()[:8],16)%2000==0}
sample.update(k for k in source_awards if 'FA865125CB00' in k)
expected={};tiekeys=[]
with (ROOT/'evidence/award-date-fields.jsonl').open() as f:
 for line in f:
  r=json.loads(line)
  if r['date_or_money_selection_conflicts'] and len(tiekeys)<20:sample.add(r['award_key']);tiekeys.append(r['award_key'])
  if r['award_key'] in sample:expected[r['award_key']]=r
fields=['period_of_performance_start_date','period_of_performance_current_end_date','period_of_performance_potential_end_date','ordering_period_end_date']
groups=collections.defaultdict(list)
for p in SOURCE_FILES:
 pf=pq.ParquetFile(p);cols=[x for x in ['contract_award_unique_key','assistance_award_unique_key','action_date','last_modified_date']+fields if x in pf.schema_arrow.names]
 for batch in pf.iter_batches(columns=cols,batch_size=32768):
  for row in batch.to_pylist():
   key=row.get('contract_award_unique_key') or row.get('assistance_award_unique_key')
   if key in sample:groups[key].append(row)
mismatches=[];checked=0
for key,rows in groups.items():
 def rank(r):return (dt.date.fromisoformat(r['action_date']) if r.get('action_date') else dt.date.min,dt.datetime.fromisoformat(r['last_modified_date'].replace('Z','+00:00')) if r.get('last_modified_date') else dt.datetime.min.replace(tzinfo=dt.timezone.utc))
 maximum=max(map(rank,rows));latest=[r for r in rows if rank(r)==maximum]
 for field in fields:
  vs={dt.date.fromisoformat(r[field][:10]).isoformat() if r.get(field) else None for r in latest};wanted=next(iter(vs)) if len(vs)==1 else None
  observed=expected[key][field];checked+=1
  if observed!=wanted:mismatches.append({'award_key':key,'field':field,'observed':observed,'expected':wanted})
check={'sample_awards':len(expected),'independently_checked_date_fields':checked,'tied_latest_sample_awards':tiekeys,'mismatches':mismatches,'method':'SHA256 first-8hex modulo2000 plus all FA865125CB00* and first20 latest-tie awards; re-read original parquet, rank by native Python date/datetime, compare exact date/null.'}
(ROOT/'audit/date-enrichment-independent-validation.json').write_text(json.dumps(check,indent=2)+'\n')
print(json.dumps({'financial_control':{k:v for k,v in control.items() if not isinstance(v,list)},'financial_control_exception_counts':{k:len(v) for k,v in control.items() if isinstance(v,list)},'date_validation':check},indent=2))
assert not financial_map_conflicts and source_transactions==financial_transactions and source_awards==financial_awards
assert not mismatches
