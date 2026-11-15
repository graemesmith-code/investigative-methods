import csv,json,hashlib,collections
from pathlib import Path
source='patent_priority_secondary_review_77.csv'
r=list(csv.DictReader(open(source)));notes=json.load(open('patent_review_continuation_notes.json'))
assert len(notes)==48
for x in r:
 if x['publication'] in notes:
  assert x['review_status'].startswith('metadata')
  n=notes[x['publication']]
  x['review_status']='text retrieval failed; retry failed' if n.startswith('BLOCKED') else 'selected claims inspected in continuation'
  x['assessment']=n
  if x['publication']=='US11703307B2':x['url']='https://patents.google.com/patent/US11703307B2'
with open('patent_priority_secondary_review_77_v2.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(r[0]));w.writeheader();w.writerows(r)
counts=dict(collections.Counter(x['review_status'] for x in r))
manifest={'date':'2026-11-15','scope':'all 48 metadata-only entries in prior 77-row checkpoint attempted','new_selected_claim_inspections':42,'new_unresolved_text_failures':6,'prior_direct_selected_claim_inspections':10,'prior_reported_not_repeated':15,'prior_unresolved_failures':4,'overall_direct_or_prior_reported':67,'overall_unresolved_fetches':10,'not_claimed':'Full prosecution review, complete full-claim reading for every document, family counts, field deployment, performance, ASIMOV linkage','status_counts':counts,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in map(Path,['patent_priority_secondary_review_77_v2.csv','patent_review_continuation_notes.json','patent_review_continuation_source_returns.json','patent_review_continuation_retry_returns.json'])}}
Path('patent_review_continuation_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
