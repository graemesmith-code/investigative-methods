#!/usr/bin/env python3
"""Create exact public storage parts/indexes for the hash-pinned recovery-v1 package. No network or paid services. Verify with restore_stage1_recovery.py."""
from pathlib import Path
import hashlib,json,gzip,shutil,tarfile,argparse
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--canonical',required=True,type=Path);parser.add_argument('--archive',required=True,type=Path);args=parser.parse_args()
P=Path(__file__).resolve().parents[1];src=args.canonical;archive=args.archive;dest=P/'evidence/independent-stage1-recovery-v1';dest.mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
assert sha(archive)=='2fda8de2231b5bed45041a7846a89b11fce50a7c82671b6b176eeb2630d2094c'
parts=[]
with archive.open('rb') as inp:
 i=0
 while True:
  b=inp.read(90*1024*1024)
  if not b:break
  f=dest/f'package.tar.gz.part-{i:04d}';f.write_bytes(b);parts.append({'path':f.name,'bytes':len(b),'sha256':sha(f)});i+=1
members=[]
for f in sorted(src.rglob('*')):
 if f.is_file():members.append({'path':f.relative_to(src).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
assert len(members)==141 and sum(x['bytes'] for x in members)==375285567
fast=[]
for rel in ['evidence/brakes-candidate-register.json.gz','evidence/ab-high-priority-review.csv','manifest.json','audit/publication-representation-map.json','README-RECOVERY.md','METHODS-RECOVERY.md','FINANCIAL-SCOPE-ADDENDUM.md']:
 f=src/rel;name={'manifest.json':'canonical-manifest.json','README-RECOVERY.md':'canonical-README.md'}.get(rel,f.name);out=dest/name;shutil.copyfile(f,out);fast.append({'path':name,'bytes':out.stat().st_size,'sha256':sha(out),'canonical_member':rel,'role':'Exact duplicate fast-access representation; no additional observations'})
orig=src/'evidence/brakes-candidate-register.csv';out=dest/'brakes-candidate-register.csv.gz'
with orig.open('rb') as inp,out.open('wb') as f:
 with gzip.GzipFile(filename='',fileobj=f,mode='wb',compresslevel=9,mtime=0) as gz:shutil.copyfileobj(inp,gz,1048576)
h=hashlib.sha256();n=0
with gzip.open(out,'rb') as inp:
 for b in iter(lambda:inp.read(1048576),b''):h.update(b);n+=len(b)
assert n==orig.stat().st_size and h.hexdigest()==sha(orig)
fast.append({'path':out.name,'bytes':out.stat().st_size,'sha256':sha(out),'canonical_member':'evidence/brakes-candidate-register.csv','expanded_bytes':n,'expanded_sha256':h.hexdigest(),'role':'Deterministic gzip of complete canonical CSV; no truncation or new records'})
representation=json.loads((src/'audit/publication-representation-map.json').read_text())
m={'package_version':'f4-stage1-recovery-v1','scope':'New independently rerun package; not claimed identical to the lost original. Every141 canonical file is preserved in full; public parts/fast-access copies are storage representations, not additional records or dollars.','archive':{'filename':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive),'ordered_parts':parts},'canonical_file_count':len(members),'canonical_bytes':sum(x['bytes'] for x in members),'canonical_manifest_sha256':sha(src/'manifest.json'),'canonical_members':members,'fast_access':fast,'logical_compression_representations':representation,'restoration':'python3 code/restore_stage1_recovery.py --destination /absolute/private/stage1-recovery-v1','counts':json.loads((src/'manifest.json').read_text())['summary'],'publication_rule':'Do not add duplicate fast-access data or archive parts as observations. Do not attribute subaward parent money. Original supplied archives and private/runtime caches are not included in this authored-results archive.'}
(dest/'storage-map.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'archive_parts':parts,'canonical_files':len(members),'fast_access_files':len(fast),'storage_bytes':sum(f.stat().st_size for f in dest.iterdir() if f.is_file())},indent=2))
