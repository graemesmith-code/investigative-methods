#!/usr/bin/env python3
"""Independent raw-row conservation and publication-boundary checks."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path

def read(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def validate(native,integrated,gitdir):
 errors=[];cache={};checked=0
 for name in ['sources','occurrences','claims','company_lane_coverage']:
  rows=read(integrated/(name+'.jsonl'))
  for row in rows:
   if row['domain']=='coordinator':continue
   path=row['original_file']
   if path not in cache:cache[path]=json.loads((native/path).read_text())
   original=cache[path][row['original_row_index']]
   if original!=row['original_record']:errors.append('Original row changed')
   h=hashlib.sha256(canonical(original).encode()).hexdigest()
   if h!=row['original_row_sha256']:errors.append('Original row hash differs')
   checked+=1
 sources=read(integrated/'sources.jsonl');occs=read(integrated/'occurrences.jsonl');claims=read(integrated/'claims.jsonl');panel=read(integrated/'company_lane_coverage.jsonl')
 sourceids={x['source_observation_id'] for x in sources}
 if len(sourceids)!=len(sources):errors.append('Duplicate source observation IDs')
 if any(x['source_observation_id'] not in sourceids for x in occs):errors.append('Orphan occurrence')
 if len({x['integrated_occurrence_id'] for x in occs})!=len(occs):errors.append('Duplicate occurrences')
 if any(not set(x['source_observation_ids'])<=sourceids for x in claims):errors.append('Orphan claim')
 summary=json.loads((integrated/'INTEGRATION_SUMMARY.json').read_text())
 native_occs=[x for x in occs if x['domain']!='coordinator']
 observed={'native_rows':len(native_occs),'reviewed':sum(x['reference_context_reviewed'] for x in native_occs),'machine_only':sum(not x['reference_context_reviewed'] for x in native_occs),'lexical':sum(x['lexical_detection'] for x in native_occs),'semantic':sum(not x['lexical_detection'] for x in native_occs)}
 if observed!={'native_rows':9650,'reviewed':1982,'machine_only':7668,'lexical':9640,'semantic':10}:errors.append('Native defined-unit totals differ')
 if len(panel)!=360 or len({x['company_panel_label'] for x in panel})!=30 or len({(x['company_panel_label'],x['lane']) for x in panel})!=360:errors.append('Company/lane cells incomplete')
 manifest=json.loads((native/'TRANSFER_MANIFEST.json').read_text())
 eligible={x['destinations']['github']['relative_path']:x for x in manifest['files'] if 'github' in x['destinations']}
 repo=next(p for p in gitdir.parents if (p/'.git').exists())
 for path,item in eligible.items():
  b=(repo/path).read_bytes()
  if hashlib.sha256(b).hexdigest()!=item['sha256']:errors.append('Eligible Git copy changed')
 files=[p for p in gitdir.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
 for p in files:
  if p.stat().st_size>=100000:errors.append('Git file >=100000bytes: '+str(p))
  if p.suffix in ['.csv','.jsonl','.pdf','.zip','.xml']:errors.append('Drive-only/source payload in Git: '+str(p))
 return {'errors':errors,'raw_native_rows_checked':checked,'source_observations':len(sources),'occurrence_observations':len(occs),'native_defined_units':observed,'coordinator_nonadditive_overlays':len(occs)-len(native_occs),'bounded_claim_records':len(claims),'panel_cells':len(panel),'exact_native_git_copies_checked':len(eligible),'git_files':len(files),'scope':'Mechanical raw-row and publication checks; independent release acceptance remains separate.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('integrated',type=Path);p.add_argument('gitdir',type=Path);a=p.parse_args();r=validate(a.native,a.integrated,a.gitdir.resolve());print(json.dumps(r,indent=2));raise SystemExit(bool(r['errors']))
