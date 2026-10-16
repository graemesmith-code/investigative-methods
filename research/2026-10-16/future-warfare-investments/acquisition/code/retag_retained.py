#!/usr/bin/env python3
"""Retag existing cohorts only. IDs, amounts, eligibility and raw records stay unchanged."""
import gzip,json,os
import pyarrow as pa,pyarrow.parquet as pq
from acquire import DATA,ROOT,save_json
from normalize import tags
results=[]
for p in sorted((DATA/'normalized').glob('*.parquet')):
 schema=pq.read_schema(p)
 if not {'capability_tags','text','title'} <= set(schema.names):continue
 tmp=p.with_suffix('.retag');writer=pq.ParquetWriter(tmp,schema,compression='zstd');counts={'file':p.name,'rows':0,'hypersonic':0,'untagged':0}
 jp=p.with_suffix('.jsonl.gz');jt=jp.with_suffix('.retag');gz=gzip.open(jt,'wt') if jp.exists() else None
 for batch in pq.ParquetFile(p).iter_batches(batch_size=5000):
  rows=batch.to_pylist()
  for row in rows:
   ts=tags((row.get('title') or '')+' '+(row.get('text') or ''));row['capability_tags']=json.dumps(ts);counts['rows']+=1;counts['hypersonic']+=('hypersonic' in ts);counts['untagged']+=not ts
   if gz:gz.write(json.dumps(row,ensure_ascii=False)+'\n')
  writer.write_table(pa.Table.from_pylist(rows,schema=schema))
 writer.close();os.replace(tmp,p)
 if gz:gz.close();os.replace(jt,jp)
 results.append(counts);print(counts,flush=True)
for p in (ROOT/'samples').glob('*.jsonl'):
 rows=[json.loads(x) for x in p.read_text().splitlines()]
 for row in rows:
  if 'capability_tags' in row:row['capability_tags']=json.dumps(tags((row.get('title') or '')+' '+(row.get('text') or '')))
 p.write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows))
save_json(ROOT/'validation/retag_retained.json',{'cohort':'unchanged retained records; no re-selection or acquisition','taxonomy_role':'retrieval features, not novelty or eligibility judgments','tables':results})
