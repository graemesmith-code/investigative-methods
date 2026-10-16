#!/usr/bin/env python3
"""Typed, unique-action financial view. No dollar totals or mixed-measure aggregation."""
import collections,csv,datetime,gzip,json
from decimal import Decimal
import pandas as pd,pyarrow as pa,pyarrow.parquet as pq
from acquire import ROOT,DATA,save_json
index=pd.read_parquet(DATA/'normalized/usaspending_unique_transaction_index.parquet');schema=pa.schema([(k,pa.string()) for k in ['document_id','transaction_key','award_key','entity_key','entity_name','source','source_url','raw_locator','source_snapshot_sha256','retrieved_at','eligibility','capability_tags']]+[('action_date',pa.date32()),('fiscal_year',pa.int16()),('action_obligation_usd',pa.decimal128(23,2))]);writer=pq.ParquetWriter(DATA/'normalized/financial_actions.parquet',schema,compression='zstd');out=gzip.open(DATA/'normalized/financial_actions.jsonl.gz','wt');counts=collections.Counter();dates=[];samples=[];buf=[]
def flush():
 global buf
 if buf:writer.write_table(pa.Table.from_pylist(buf,schema=schema));buf=[]
for source,group in index.groupby('preferred_source',sort=True):
 wanted=set(group.preferred_document_id);df=pd.read_parquet(DATA/'normalized'/f'{source}.parquet');df=df[df.document_id.isin(wanted)]
 for r in df.to_dict('records'):
  value=json.loads(r['money_json']).get('federal_action_obligation');amount=Decimal(value) if value is not None else None;dt=datetime.date.fromisoformat(r['action_date']) if r['action_date'] else None;new={k:r.get(k) for k in schema.names if k not in ['action_date','fiscal_year','action_obligation_usd']};new.update(action_date=dt,fiscal_year=int(r['fiscal_year']) if r['fiscal_year'] else None,action_obligation_usd=amount);buf.append(new);counts['rows']+=1;counts['missing' if amount is None else ('negative' if amount<0 else ('zero' if amount==0 else 'positive'))]+=1
  if dt:dates.append(str(dt))
  serial=dict(new,action_date=str(dt) if dt else None,action_obligation_usd=str(amount) if amount is not None else None);out.write(json.dumps(serial,ensure_ascii=False)+'\n')
  if len(samples)<6 or (amount is not None and amount<0 and sum(Decimal(s['action_obligation_usd'])<0 for s in samples if s['action_obligation_usd'] is not None)<3):samples.append(serial)
  if len(buf)>=5000:flush()
flush();writer.close();out.close()
with (ROOT/'samples/financial_actions.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(samples[0]));w.writeheader();w.writerows(samples[:12])
save_json(ROOT/'validation/financial_action_profile.json',{'counts':dict(counts),'expected_unique_transaction_index_rows':len(index),'date_min':min(dates),'date_max':max(dates),'schema':str(schema),'measure':'signed federal_action_obligation, USD, typed decimal128(23,2)','grain':'one preferred representation per unique native USAspending transaction key','eligibility':'Source selection/candidate flags retained; not all rows establish novel capability or international mission.','aggregation_rule':'This is a duplicate representation of the same source actions. Use this view OR the corresponding source rows, never add both. Sum only within a deliberately reviewed universe after retaining negative deobligations; do not add cumulative award values, options, requests, outlays, subawards or SBIR representations. No dollar total computed in this pass.'})
if counts['rows']!=len(index):raise SystemExit('Typed financial-view count differs from unique index')
print('Typed financial actions',dict(counts))
