#!/usr/bin/env python3
"""Full original-vs-normalized description validation and omitted descriptive-column inventory."""
import pathlib,json,gzip,hashlib,collections
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).resolve().parents[1]
counts=collections.Counter();files=[];omitted=collections.defaultdict(lambda:{'row_appearances':0,'values':{},'max_characters':0});mismatch_path=ROOT/'evidence/source-description-differences.jsonl'
def norm(v):return '' if v is None else str(v)
with mismatch_path.open('w') as bad:
 for p in sorted((ROOT/'input').rglob('*_transactions_source.parquet')):
  pf=pq.ParquetFile(p);fields=[f for f in pf.schema_arrow.names if any(t in f.lower() for t in ['description','text','title'])]
  keyfield='contract_transaction_unique_key' if 'contract_transaction_unique_key' in pf.schema_arrow.names else 'assistance_transaction_unique_key'
  awardfield=keyfield.replace('transaction','award')
  cols=[keyfield,awardfield]+fields
  source={};stat=collections.Counter()
  for batch in pf.iter_batches(columns=cols,batch_size=16384):
   for r in batch.to_pylist():
    tx=r[keyfield];source[tx]=(r.get('prime_award_base_transaction_description'),r.get('transaction_description'));stat['source_rows']+=1
    for field in fields:
     if field in ['prime_award_base_transaction_description','transaction_description']:continue
     value=norm(r.get(field))
     if not value:continue
     q=omitted[field];q['row_appearances']+=1;q['max_characters']=max(q['max_characters'],len(value))
     v=q['values'].setdefault(value,{'row_appearances':0,'sample_award_keys':set(),'source_files':set()});v['row_appearances']+=1;v['source_files'].add(p.name)
     if len(v['sample_award_keys'])<10:v['sample_award_keys'].add(r[awardfield])
  normalized=p.with_name(p.name.replace('_transactions_source.parquet','.jsonl.gz'))
  for i,line in enumerate(gzip.open(normalized,'rt'),1):
   r=json.loads(line);tx=r.get('transaction_key');stat['normalized_rows']+=1
   if tx not in source:stat['unmatched_transaction_keys']+=1;continue
   base,desc=source[tx]
   for nf,sv in [('title',base),('text',desc)]:
    nv=norm(r.get(nf));sv=norm(sv);label=None
    if nv==sv:label='exact_equal'
    elif nv.strip()==sv.strip():label='only_outer_whitespace_differs'
    elif not sv and nv in [norm(base),norm(desc)]:label='empty_source_fallback_to_other_full_description'
    elif sv.startswith(nv) and nv:label='normalized_is_strict_prefix_of_source'
    else:label='other_difference'
    stat[nf+'_'+label]+=1
    if label not in ['exact_equal','only_outer_whitespace_differs','empty_source_fallback_to_other_full_description']:
     bad.write(json.dumps({'source_file':str(p.relative_to(ROOT)),'normalized_file':str(normalized.relative_to(ROOT)),'normalized_line':i,'transaction_key':tx,'award_key':r['award_key'],'field':nf,'difference':label,'source_full_description':sv,'normalized_full_description':nv},sort_keys=True)+'\n')
  files.append({'source_file':str(p.relative_to(ROOT)),'descriptive_columns':fields,**stat});counts.update(stat)
  print(json.dumps(files[-1]),flush=True)
extras=[]
for field,q in sorted(omitted.items()):
 vals=[]
 for value,v in sorted(q['values'].items()):
  vals.append({'value':value,'row_appearances':v['row_appearances'],'sample_award_keys':sorted(v['sample_award_keys']),'source_files':sorted(v['source_files'])})
 extras.append({'field':field,'row_appearances':q['row_appearances'],'unique_values':len(vals),'max_characters':q['max_characters'],'values':vals})
extra_path=ROOT/'evidence/source-extra-descriptive-field-values.json';extra_path.write_text(json.dumps(extras,indent=2)+'\n')
audit={'files':files,'counts':dict(counts),'omitted_descriptive_columns':[{k:v for k,v in x.items() if k!='values'} for x in extras],'differences_file':str(mismatch_path.relative_to(ROOT)),'differences_sha256':hashlib.file_digest(mismatch_path.open('rb'),'sha256').hexdigest(),'extra_fields_file':str(extra_path.relative_to(ROOT)),'extra_fields_sha256':hashlib.file_digest(extra_path.open('rb'),'sha256').hexdigest(),'method':'Read all eight original transaction-source tables and exact-key compare every normalized title/text to base and transaction description. Inventory all other schema fields containing description, title or text. Null and empty are equivalent only for comparison; source values retained in originals.'}
(ROOT/'audit/description-completeness-validation.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({'counts':dict(counts),'omitted_columns':audit['omitted_descriptive_columns']},indent=2))
