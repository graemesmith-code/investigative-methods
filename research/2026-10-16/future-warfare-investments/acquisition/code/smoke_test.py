#!/usr/bin/env python3
"""Offline mixed-source interface check against retained files and the portable sample."""
import collections,json
import pandas as pd
from acquire import DATA,ROOT,save_json
from lineage import issues
rows=[json.loads(x) for x in (ROOT/'samples/dry_run_candidates.jsonl').read_text().splitlines()];ids={r['document_id'] for r in rows};dry=json.loads((ROOT/'validation/dry_run.json').read_text());checks={}
checks['sample_lineage']=not issues(pd.DataFrame(rows))
checks['multiple_sources']=len({r['source'] for r in rows})>=4
checks['untagged_retained']=any(not json.loads(r['capability_tags']) for r in rows)
checks['all_scores_null']=dry['all_scores_null']
checks['relationship_endpoints_in_sample']=all(e[k] in ids for e in dry['identifier_relationship_examples'] for k in ['left_document_id','right_document_id'])
projects={}
for name in ['commons_projects','apfit_fy2022_projects','darpa_pb2025_programs']:
 frame=pd.read_parquet(DATA/'normalized'/f'{name}.parquet');checks[name+'_lineage']=not issues(frame);projects[name]=len(frame)
checks['hypersonic_project_evidence']=any('hypersonic' in json.loads(x) for x in pd.read_parquet(DATA/'normalized/commons_projects.parquet').capability_tags)
spending=[r for r in rows if r['source'].startswith('usaspending_')]
result={'mode':'offline_deterministic_no_paid_calls','checks':checks,'passed':sum(checks.values()),'failed':sum(not x for x in checks.values()),'sample_rows':len(rows),'source_counts':dict(collections.Counter(r['source'] for r in rows)),'project_rows_checked':projects,'relationship_edges':len(dry['identifier_relationship_examples']),'spending_sample_rows':len(spending),'spending_text_under_200_chars':sum(len(r.get('text') or '')<200 for r in spending),'warning':'Short spending descriptions are expected source limitations; SBIR abstracts, program/project narratives and linked evidence are essential before novelty review. Regex absence does not imply irrelevance.'}
save_json(ROOT/'validation/qa_smoke_test.json',result);print(json.dumps(result))
if not all(checks.values()):raise SystemExit(1)
