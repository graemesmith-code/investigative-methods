#!/usr/bin/env python3
"""Offline integrity checks; never invokes external services."""
import argparse,ast,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote,urlsplit
P=Path(__file__).resolve().parents[1]
EXCLUDE={'file-manifest.json','validation.json','delivery-manifest.json'}
def files():
 return [f for f in sorted(P.rglob('*')) if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc' and f.name not in EXCLUDE]
def hashes():return [{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files()]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write-manifest',action='store_true');a=ap.parse_args();errors=[];checks=Counter()
 for f in files():
  try:
   if f.suffix=='.json':json.loads(f.read_text());checks['json_files']+=1
   elif f.suffix=='.jsonl':
    for l in f.read_text().splitlines():
     if l.strip():json.loads(l);checks['jsonl_records']+=1
    checks['jsonl_files']+=1
   elif f.suffix=='.py':ast.parse(f.read_text());checks['python_ast_files']+=1
  except Exception as e:errors.append(f'{f.relative_to(P)}: {e}')
 rows=[json.loads(l) for l in (P/'source-inventory.jsonl').open()];ids={r['source_id'] for r in rows}
 if len(ids)!=len(rows):errors.append('duplicate root source IDs')
 for r in rows:
  for k in ['org','title','url','source_type','date_scope','acquisition_status','screening_rationale','original_inventory','original_line']:
   if k not in r:errors.append(f"{r.get('source_id')}: missing {k}")
  if not r['url'].startswith('https://'):errors.append(f"{r['source_id']}: nonHTTPS source")
  if r['deeply_read'] and not r['context_screened']:errors.append(f"{r['source_id']}: deep without context")
  origin=P/r['original_inventory'];original=json.loads(origin.read_text().splitlines()[r['original_line']-1])
  if original['url']!=r['url']:errors.append(f"{r['source_id']}: original pointer mismatch")
  for x in [r]+r.get('source_versions',[]):
   for k in ['sha256','report_sha256','landing_sha256']:
    h=x.get(k)
    if h is not None and not re.fullmatch('[0-9a-f]{64}',h):errors.append(f"{r['source_id']}: invalid {k}")
 checks['canonical_source_records']=len(rows)
 counts=json.loads((P/'coverage-counts.json').read_text());totals=json.loads((P/'totals.json').read_text())
 for key in counts[0]:
  if key=='org':continue
  if sum(r[key] for r in counts)!=totals[key]:errors.append(f'total mismatch {key}')
 if len(counts)!=15:errors.append('not all15organizations covered')
 if totals['enumerated']!=len(rows):errors.append('enumerated mismatch')
 for field,totalkey in [('cross_org_work_id','unique_works')]:
  if len(set(r[field] for r in rows))!=totals[totalkey]:errors.append(f'unique-work mismatch {totalkey}')
 machine=[json.loads(l) for l in (P/'machine-screen-inventory.jsonl').open()]
 for m in machine:
  if m['source_id'] not in ids:errors.append('machine index unmatched source')
  for k in ['report_sha256','acquired_sha256','text_sha256','cache_text_sha256']:
   if m.get(k) and not re.fullmatch('[0-9a-f]{64}',m[k]):errors.append('invalid machine hash')
 if len(machine)!=totals['machine_text_files']:errors.append('machine-file count mismatch')
 if len(set(m['source_id'] for m in machine))!=totals['machine_screened']:errors.append('machine-work count mismatch')
 checks['machine_index_records']=len(machine)
 opp=json.loads((P/'opportunity-manifest.json').read_text())
 if opp['completed_investigative_findings']:errors.append('unexpected completed investigative finding')
 if len(opp['pilot_ready'])!=totals['pilot_ready_opportunities']:errors.append('pilot-ready count mismatch')
 for o in opp['pilot_ready']:
  if len(o['gates'])!=9:errors.append('incomplete nine-gate manifest')
  for s in o['source_ids']:
   if s not in ids:errors.append(f'unknown candidate sourceID {s}')
  for e in o['evidence_files']:
   if not (P/e).is_file():errors.append(f'missing candidate evidence {e}')
 for o in opp['conditional_opportunities']:
  if not o['specific_blocker']:errors.append('conditional design lacks specific blocker')
  for e in o['evidence_files']:
   if not (P/e).is_file():errors.append(f'missing conditional evidence {e}')
 expected_retained=set(s for o in opp['pilot_ready'] for s in o['source_ids'])
 if set(r['source_id'] for r in rows if r['retained_pilot_source'])!=expected_retained:errors.append('retained source set mismatch')
 for f in P.rglob('*.md'):
  for target in re.findall(r'\]\(([^\s)]+)\)',f.read_text()):
   if target.startswith(('http://','https://','mailto:','#')):checks['external_or_anchor_links_recorded']+=1;continue
   target=unquote(target.split('#')[0]);target=re.sub(r':\d+$','',target)
   if not (f.parent/target).exists():errors.append(f'missing local link {f.relative_to(P)} -> {target}')
   else:checks['local_links_checked']+=1
 if a.write_manifest:(P/'file-manifest.json').write_text(json.dumps({'algorithm':'sha256','files':hashes()},indent=2)+'\n')
 elif (P/'file-manifest.json').exists():
  recorded=json.loads((P/'file-manifest.json').read_text())['files']
  if recorded!=hashes():errors.append('file-manifest differs from current research files')
 else:errors.append('file-manifest missing; first run --write-manifest')
 result={'status':'PASS' if not errors else 'FAIL','checks':dict(checks),'errors':errors,'network_calls':0,'paid_calls':0,'completed_findings':0,'pilot_ready_opportunities':len(opp['pilot_ready']),'conditional_opportunities':len(opp['conditional_opportunities']),'note':'External URLs are not silently called available: recorded acquisition/failure manifests supply access evidence.'}
 (P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return bool(errors)
if __name__=='__main__':sys.exit(main())
