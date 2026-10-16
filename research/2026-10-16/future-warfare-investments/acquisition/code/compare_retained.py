#!/usr/bin/env python3
"""Before repackaging, compare corrected tables with the retained first-pass archives."""
import hashlib,json,tarfile
import pyarrow as pa,pyarrow.parquet as pq
from acquire import DATA,ROOT,save_json
checks=[];baseline_hashes={}
for archive in sorted((DATA.parent/'fwi-bundles').glob('*normalized*.tar.gz')):
 baseline_hashes[archive.name]=hashlib.sha256(archive.read_bytes()).hexdigest()
 with tarfile.open(archive,'r:gz') as t:
  for member in t:
   if not member.name.endswith('.parquet'):continue
   p=DATA/member.name
   old=pq.ParquetFile(pa.BufferReader(t.extractfile(member).read()));new=pq.ParquetFile(p)
   if 'document_id' not in old.schema_arrow.names:continue
   cols=[k for k in old.schema_arrow.names if k!='capability_tags']
   before=old.read(columns=cols);after=new.read(columns=cols)
   # Arrow equals compares exact scalar values, order, nulls and types.
   checks.append({'file':member.name,'rows':before.num_rows,'all_preexisting_non_tag_fields_identical':before.equals(after)})
result={'basis':'Comparison against the baseline archives identified by exact hashes; run before overwriting those baseline archives','baseline_archive_sha256':baseline_hashes,'checks':checks,'passed':sum(c['all_preexisting_non_tag_fields_identical'] for c in checks),'failed':sum(not c['all_preexisting_non_tag_fields_identical'] for c in checks)}
save_json(ROOT/'validation/qa_cohort_comparison.json',result);print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
if result['failed']:raise SystemExit(1)
