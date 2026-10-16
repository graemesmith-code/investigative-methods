#!/usr/bin/env python3
"""Small deterministic interface exercise. No network, paid tools or model scoring."""
import collections,gzip,json,pathlib,re
from acquire import DATA,ROOT,save_json
inputs=['sbir_current','usaspending_darpa','usaspending_dod_research_grants','usaspending_dod_rd_contracts','usaspending_dod_capabilities','grants'];selected=[];counts=collections.Counter();edges=[];native_awards={};piids={};max_per_source=16
inputs+=sorted(p.stem for p in (DATA/'normalized').glob('usaspending_dod_rd_fy*.parquet') if re.fullmatch(r'usaspending_dod_rd_fy\d{4}',p.stem))
for source in inputs:
 p=DATA/'normalized'/f'{source}.jsonl.gz'
 if not p.exists():continue
 chosen=[];seen_tags=set()
 with gzip.open(p,'rt') as f:
  for line in f:
   r=json.loads(line);ts=json.loads(r.get('capability_tags') or '[]')
   # Reserve two slots for untagged evidence; absence of regex hits is not ineligibility.
   untagged=sum(not json.loads(x.get('capability_tags') or '[]') for x in chosen)
   if (not ts and untagged<2) or (ts and len(chosen)-untagged<14):
    ids=json.loads(r.get('identifiers_json') or '{}');r['deterministic_checks']={'nonempty_text':bool(r.get('text')),'text_at_least_200_chars':len(r.get('text') or '')>=200,'source_link_present':bool(r.get('source_url')),'raw_locator_present':bool(r.get('raw_locator')),'date_present':bool(r.get('action_date')),'entity_key_present':bool(r.get('entity_key')),'capability_regex_hits':ts,'review_queue':'tagged_candidate' if ts else 'untagged_requires_model_review','money_interpretation':'consult per-source dictionary; no aggregate computed','novelty_score':None,'newsworthiness_score':None,'editorial_inclusion':'unreviewed','international_mission_terms_present':bool(re.search(r'overseas|allied|combat|warfight|foreign|expeditionary|deterrence',r.get('text') or '',re.I)),'administrative_terms_present':bool(re.search(r'payroll|human resources|office supplies|administrative support',r.get('text') or '',re.I)),'domestic_policing_terms_present':bool(re.search(r'police department|domestic law enforcement|local law enforcement',r.get('text') or '',re.I))}
    r['coverage_request_design']={'execute':False,'max_requests':0,'query':' '.join(x for x in ['"'+(r.get('entity_name') or '')+'"' if r.get('entity_name') else '',(r.get('title') or '')[:140],ids.get('Contract','') or ids.get('award_id_piid','')] if x),'cluster_id':None,'status':'design_only'}
    chosen.append(r);seen_tags.update(ts)
   # Bounded scan still permits some exact-key relationships; no need to process complete graph.
   if len(chosen)>=max_per_source:break
 selected+=chosen;counts[source]=len(chosen)
# Relationships only between envelopes included in this self-contained sample.
for r in selected:
 key=r.get('award_key')
 if key and r['source'].startswith('usaspending_'):
  if key in native_awards and len(edges)<20:
   edges.append({'left_document_id':native_awards[key],'right_document_id':r['document_id'],'relation_type':'same_reported_award','basis':'exact USAspending native award key','confidence':'identifier_supported','review_status':'not_editorially_reviewed','financial_aggregation_permitted':False})
  else:native_awards[key]=r['document_id']
ids={r['document_id'] for r in selected}
assert all(e['left_document_id'] in ids and e['right_document_id'] in ids for e in edges)
(ROOT/'samples/dry_run_candidates.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in selected));save_json(ROOT/'validation/dry_run.json',{'mode':'deterministic_only','model_calls':0,'exa_calls':0,'records_by_source':dict(counts),'total_candidate_records':len(selected),'capability_regex_counts':dict(collections.Counter(t for r in selected for t in json.loads(r['capability_tags']))),'identifier_relationship_examples':edges[:20],'relationship_endpoints_self_contained':True,'untagged_review_records':sum(not json.loads(r['capability_tags']) for r in selected),'all_scores_null':all(r['deterministic_checks']['novelty_score'] is None and r['deterministic_checks']['newsworthiness_score'] is None for r in selected),'warning':'Features and exact-key relationships are not evidence of novelty, same capability, newsworthiness or absence of reporting.'});print('Dry run',len(selected),'candidates',len(edges[:20]),'edges')
