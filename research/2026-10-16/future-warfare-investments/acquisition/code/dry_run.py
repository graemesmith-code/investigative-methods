#!/usr/bin/env python3
"""Small deterministic interface exercise. No network, paid tools or model scoring."""
import collections,gzip,json,pathlib,re
from acquire import DATA,ROOT,save_json
inputs=['sbir_current','usaspending_darpa','usaspending_dod_research_grants','usaspending_dod_rd_contracts','usaspending_dod_capabilities','grants'];selected=[];counts=collections.Counter();edges=[];native_awards={};piids={};max_per_source=16
for source in inputs:
 p=DATA/'normalized'/f'{source}.jsonl.gz'
 if not p.exists():continue
 chosen=[];seen_tags=set()
 with gzip.open(p,'rt') as f:
  for line in f:
   r=json.loads(line);ts=json.loads(r.get('capability_tags') or '[]')
   if not ts:continue
   key=r.get('award_key')
   if key and source.startswith('usaspending_'):
    if key in native_awards and len(edges)<40:edges.append({'left_document_id':native_awards[key],'right_document_id':r['document_id'],'relation_type':'same_reported_award','basis':'exact USAspending native award key','confidence':'identifier_supported','review_status':'not_editorially_reviewed','financial_aggregation_permitted':False})
    else:native_awards[key]=r['document_id']
   if len(chosen)<max_per_source and (not set(ts).issubset(seen_tags) or len(chosen)<8):
    ids=json.loads(r.get('identifiers_json') or '{}');r['deterministic_checks']={'nonempty_text':bool(r.get('text')),'text_at_least_200_chars':len(r.get('text') or '')>=200,'source_link_present':bool(r.get('source_url')),'raw_locator_present':bool(r.get('raw_locator')),'date_present':bool(r.get('action_date')),'entity_key_present':bool(r.get('entity_key')),'capability_regex_hits':ts,'money_interpretation':'consult per-source dictionary; no aggregate computed','novelty_score':None,'newsworthiness_score':None,'editorial_inclusion':'unreviewed'}
    r['coverage_request_design']={'execute':False,'max_requests':0,'query':' '.join(x for x in ['"'+(r.get('entity_name') or '')+'"' if r.get('entity_name') else '',(r.get('title') or '')[:140],ids.get('Contract','') or ids.get('award_id_piid','')] if x),'cluster_id':None,'status':'design_only'}
    chosen.append(r);seen_tags.update(ts)
   # Bounded scan still permits some exact-key relationships; no need to process complete graph.
   if len(chosen)>=max_per_source and len(edges)>=40:break
 selected+=chosen;counts[source]=len(chosen)
(ROOT/'samples/dry_run_candidates.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in selected));save_json(ROOT/'validation/dry_run.json',{'mode':'deterministic_only','model_calls':0,'exa_calls':0,'records_by_source':dict(counts),'total_candidate_records':len(selected),'capability_regex_counts':dict(collections.Counter(t for r in selected for t in json.loads(r['capability_tags']))),'identifier_relationship_examples':edges[:20],'all_scores_null':all(r['deterministic_checks']['novelty_score'] is None and r['deterministic_checks']['newsworthiness_score'] is None for r in selected),'warning':'Features and exact-key relationships are not evidence of novelty, same capability, newsworthiness or absence of reporting.'});print('Dry run',len(selected),'candidates',len(edges[:20]),'edges')
