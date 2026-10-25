#!/usr/bin/env python3
"""Expose and screen narrative fields omitted from normalized title/text.
Uses frozen current screening lexicon, keeps complete rows and all negative screens.
"""
import pathlib,json,collections,hashlib
import pyarrow.parquet as pq
from lexicon_additional_narratives_snapshot import hits,classify
ROOT=pathlib.Path(__file__).resolve().parents[1]
rows=0;nonempty=0;new_candidates=0;new_terms=collections.Counter();candidate_awards=set();extraonly_awards=set();seen_goals=set();sources=[]
out=ROOT/'evidence/source-additional-narratives.jsonl';candidates=ROOT/'evidence/source-additional-narrative-candidates.jsonl';cache={}
def hit(t):
 if t not in cache:cache[t]=hits(t)
 return cache[t]
with out.open('w') as output,candidates.open('w') as positive:
 for p in sorted((ROOT/'input').rglob('*_transactions_source.parquet')):
  pf=pq.ParquetFile(p)
  if 'funding_opportunity_goals_text' not in pf.schema_arrow.names:continue
  cols=['assistance_award_unique_key','assistance_transaction_unique_key','recipient_name','action_date','prime_award_base_transaction_description','transaction_description','funding_opportunity_goals_text']
  cols=[x for x in cols if x in pf.schema_arrow.names];i=0
  for batch in pf.iter_batches(columns=cols,batch_size=16384):
   for r in batch.to_pylist():
    i+=1;rows+=1;goal=r.get('funding_opportunity_goals_text')
    if not goal:continue
    nonempty+=1;seen_goals.add(goal);base='\n'.join(str(r.get(f) or '') for f in ['prime_award_base_transaction_description','transaction_description'])
    before=hit(base);after=hit(base+'\n'+goal);beforetags,_=classify(before);tags,reasons=classify(after);new={g:sorted(set(ts)-set(before.get(g,[]))) for g,ts in after.items() if set(ts)-set(before.get(g,[]))}
    for g,ts in new.items():
     for t in ts:new_terms[g+':'+t]+=1
    record={'source_file':str(p.relative_to(ROOT)),'source_row':i,'award_key':r['assistance_award_unique_key'],'transaction_key':r['assistance_transaction_unique_key'],'entity_name':r.get('recipient_name'),'action_date':r.get('action_date'),'source_url':'https://www.usaspending.gov/award/'+r['assistance_award_unique_key']+'/','full_description_fields':{k:r.get(k) for k in ['prime_award_base_transaction_description','transaction_description','funding_opportunity_goals_text']},'baseline_title_text_hits':before,'combined_hits':after,'additional_goal_terms':new,'preliminary_categories_with_goal':tags,'preliminary_reasons_with_goal':reasons,'new_candidate_from_goal':bool(tags and not beforetags)}
    output.write(json.dumps(record,sort_keys=True)+'\n')
    if tags:
     positive.write(json.dumps(record,sort_keys=True)+'\n');candidate_awards.add(r['assistance_award_unique_key'])
    if tags and not beforetags:new_candidates+=1;extraonly_awards.add(r['assistance_award_unique_key'])
  sources.append({'source_file':str(p.relative_to(ROOT)),'source_rows':i})
audit={'sources':sources,'source_rows_checked':rows,'nonempty_goals_rows':nonempty,'unique_goal_values':len(seen_goals),'candidate_awards_with_combined_text':len(candidate_awards),'new_candidate_row_appearances_from_goal':new_candidates,'new_candidate_award_keys_from_goal':sorted(extraonly_awards),'additional_term_row_counts':dict(new_terms),'lexicon_snapshot_sha256':hashlib.file_digest((ROOT/'code/lexicon_additional_narratives_snapshot.py').open('rb'),'sha256').hexdigest(),'output':str(out.relative_to(ROOT)),'output_sha256':hashlib.file_digest(out.open('rb'),'sha256').hexdigest(),'candidate_output':str(candidates.relative_to(ROOT)),'candidate_output_sha256':hashlib.file_digest(candidates.open('rb'),'sha256').hexdigest(),'note':'Additional assistance goals narrative is distinct from exact-preserved base/transaction descriptions; all33144 nonempty appearances retained. Existing row exclusions are not applied; tags are preliminary lexical retrieval only.'}
(ROOT/'audit/additional-source-narratives.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
