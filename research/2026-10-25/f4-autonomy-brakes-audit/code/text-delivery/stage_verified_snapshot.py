#!/usr/bin/env python3
"""Stage exact known-public Git blobs from reusable local mappings, without network."""
import argparse,hashlib,json,pathlib,shutil
MAPS={'evidence/independent-stage1/':'/workspace/shared/f4-stage1/package','evidence/independent-stage1/_connector-transport/':'/workspace/shared/f4-publisher/stage1-transport/_connector-transport','evidence/independent-stage1-addendum/':'/workspace/shared/f4-stage1-addendum','evidence/independent-editor/':'/workspace/shared/f4-editor-public-safe','evidence/independent-editor-round2-review/':'/workspace/shared/f4-editor-round2-review','evidence/independent-editor-round3-review/':'/workspace/shared/f4-editor-round3-review','evidence/independent-editor-boundary-cases/':'/workspace/shared/f4-publisher/boundary-snapshot','evidence/independent-policy/':'/workspace/shared/f4-policy-audit'}
def sha(p):
 h=hashlib.sha1();h.update(b'blob '+str(p.stat().st_size).encode()+b'\0')
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('inventory');ap.add_argument('output');ap.add_argument('--reuse',action='append',default=[]);ap.add_argument('--map',action='append',default=[]);ap.add_argument('--hash-root',action='append',default=[]);a=ap.parse_args();inv=json.loads(pathlib.Path(a.inventory).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);maps=dict(MAPS)
 for s in a.map:k,v=s.split('=',1);maps[k]=v
 missing=[];verified=[];conflicts=[];hash_index={}
 for root in a.hash_root:
  for p in pathlib.Path(root).rglob('*'):
   if p.is_file():hash_index.setdefault((p.stat().st_size,sha(p)),p)
 for r in inv['files']:
  assert r['path'].startswith(inv['root']);rel=r['path'][len(inv['root']):];assert '..' not in pathlib.PurePosixPath(rel).parts;dst=out/rel
  cand=[dst]+[pathlib.Path(x)/rel for x in a.reuse]+[pathlib.Path(v)/rel[len(k):] for k,v in maps.items() if rel.startswith(k)]
  match=next((p for p in cand if p.is_file() and p.stat().st_size==r['size'] and sha(p)==r['sha']),None)
  if match is None:match=hash_index.get((r['size'],r['sha']))
  if match is None:missing.append(r);continue
  if match!=dst:
   if dst.exists():conflicts.append(rel);continue
   dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(match,dst)
  verified.append(rel)
 result={'commit':inv['commit'],'root':inv['root'],'inventory_count':len(inv['files']),'verified_count':len(verified),'missing':missing,'conflicts':conflicts,'verified':verified};(out.parent/(out.name+'-staging.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='verified'},indent=2))
 if conflicts:raise SystemExit(2)
if __name__=='__main__':main()
