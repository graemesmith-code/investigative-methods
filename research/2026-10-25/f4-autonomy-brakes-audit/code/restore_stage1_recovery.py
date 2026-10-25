#!/usr/bin/env python3
"""Restore all141 canonical recovery files from exact public archive parts.
No network. Verifies part/archive/member hashes; refuses unsafe archive paths
and existing different files. Public fast-access core files are duplicates.
"""
import argparse,gzip,hashlib,json,pathlib,shutil,tarfile,tempfile,os
P=pathlib.Path(__file__).resolve().parents[1]
S=P/'evidence/independent-stage1-recovery-v1'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def restore(destination):
 m=json.loads((S/'storage-map.json').read_text());dest=pathlib.Path(destination).resolve();dest.mkdir(parents=True,exist_ok=True)
 expected={r['path']:r for r in m['canonical_members']};seen=set();total=0
 with tempfile.TemporaryDirectory(dir=dest.parent,prefix='f4-stage1-archive-') as work:
  archive=pathlib.Path(work)/'package.tar.gz'
  with archive.open('wb') as out:
   for r in m['archive']['ordered_parts']:
    f=S/r['path'];assert f.resolve().is_relative_to(S.resolve())
    assert f.stat().st_size==r['bytes'] and sha(f)==r['sha256']
    with f.open('rb') as inp:shutil.copyfileobj(inp,out,1048576)
  assert archive.stat().st_size==m['archive']['bytes'] and sha(archive)==m['archive']['sha256']
  with tarfile.open(archive,'r:gz') as t:
   for member in t:
    name=member.name;assert member.isfile() and not name.startswith('/') and '..' not in pathlib.PurePosixPath(name).parts and name not in seen and name in expected
    target=dest/name;assert target.resolve().is_relative_to(dest);target.parent.mkdir(parents=True,exist_ok=True)
    row=expected[name];assert member.size==row['bytes'];temporary=pathlib.Path(work)/'member.tmp'
    with t.extractfile(member) as inp,temporary.open('wb') as out:shutil.copyfileobj(inp,out,1048576)
    assert temporary.stat().st_size==row['bytes'] and sha(temporary)==row['sha256']
    if target.exists():assert sha(target)==row['sha256'],'Existing different member not overwritten'
    else:os.replace(temporary,target)
    seen.add(name);total+=member.size
  assert seen==set(expected) and total==m['canonical_bytes']
 print(json.dumps({'canonical_files_verified':len(seen),'canonical_bytes':total,'archive_sha256':m['archive']['sha256'],'destination':str(dest),'all_original_bytes_restored':True},indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--destination',required=True);restore(a.parse_args().destination)
