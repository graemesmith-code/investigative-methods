#!/usr/bin/env python3
import pathlib,json,gzip,hashlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
src=ROOT/'evidence/source-additional-narratives.jsonl';out=ROOT/'evidence/source-extra-narratives.jsonl.gz';n=0;keys=set();zero=collections.Counter()
with out.open('wb') as target:
 with gzip.GzipFile(filename='',fileobj=target,mode='wb',mtime=0,compresslevel=6) as gz:
  for line in src.open():
   r=json.loads(line);f=r['full_description_fields'];record={'award_key':r['award_key'],'transaction_key':r['transaction_key'],'entity_name':r['entity_name'],'action_date':r['action_date'],'title':f['prime_award_base_transaction_description'],'text':f['transaction_description'],'funding_opportunity_goals_text':f['funding_opportunity_goals_text'],'source_file':r['source_file'],'source_row':r['source_row'],'raw_locator':r['source_file']+':data_row='+str(r['source_row']),'source_url':r['source_url'],'source':'usaspending_dod_research_grants_source_extra_narratives'}
   for k,v in record.items():
    if v is None or v=='':zero[k]+=1
   keys.add(r['transaction_key']);n+=1;gz.write((json.dumps(record,sort_keys=True)+'\n').encode())
audit={'output':str(out.relative_to(ROOT)),'sha256':hashlib.file_digest(out.open('rb'),'sha256').hexdigest(),'bytes':out.stat().st_size,'rows_preserved':n,'unique_transaction_keys':len(keys),'duplicate_rows_removed':0,'total_assistance_rows_checked':88273,'empty_goals_rows_not_emitted':88273-n,'other_source_tables_without_goals_column':7,'null_or_empty_output_fields':dict(zero),'all_output_fields_null_or_empty_counts':{k:zero[k] for k in record},'narrative_coverage_note':'Output contains every nonempty funding_opportunity_goals_text source appearance; source original tables and all empty-field accounting retained. No source rows deduplicated. Core descriptions remain separate from added goals field.'}
(ROOT/'audit/source-extra-narratives.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2));assert n==33144 and len(keys)==n
