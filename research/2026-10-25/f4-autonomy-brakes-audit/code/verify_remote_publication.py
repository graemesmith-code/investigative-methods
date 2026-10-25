#!/usr/bin/env python3
"""Verify remote branch identity, every scoped file's SHA256, and change scope.

Run after a successful push. Output is a post-publication delivery receipt, kept
outside the self-inventoried package to avoid recursive commit/hash dependencies.
Uses the existing git credential helper; does not configure persistent access.
"""
import argparse,hashlib,json,pathlib,subprocess,datetime
PREFIX='research/2026-10-25/f4-autonomy-brakes-audit/'
ROOT=pathlib.Path(__file__).resolve().parents[4]
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha_file(path):
 h=hashlib.sha256()
 with path.open('rb') as inp:
  for chunk in iter(lambda:inp.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def run(commit,branch,base):
 remote=git('ls-remote','origin','refs/heads/'+branch).decode().split()
 assert remote and remote[0]==commit,'Remote branch does not identify expected commit'
 git('-c',"credential.helper=!gh auth git-credential",'fetch','origin',branch)
 assert git('rev-parse','FETCH_HEAD').decode().strip()==commit
 changed=git('diff','--name-only',base,commit).decode().splitlines()
 assert changed and all(x.startswith(PREFIX) for x in changed),'Unrelated path changed'
 entries=git('ls-tree','-r','-z',commit,'--',PREFIX).split(b'\0');verified=[]
 for entry in entries:
  if not entry:continue
  meta,path=entry.split(b'\t',1);mode,kind,oid=meta.split();name=path.decode()
  assert kind==b'blob' and mode in (b'100644',b'100755')
  h=hashlib.sha256();count=0
  proc=subprocess.Popen(['git','cat-file','blob',oid.decode()],cwd=ROOT,stdout=subprocess.PIPE)
  for chunk in iter(lambda:proc.stdout.read(1024*1024),b''):h.update(chunk);count+=len(chunk)
  assert proc.wait()==0
  local=ROOT/name;actual=h.hexdigest()
  assert local.is_file() and local.stat().st_size==count and sha_file(local)==actual,name
  verified.append({'path':name,'bytes':count,'git_blob':oid.decode(),'sha256':actual})
 return {'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote':'https://github.com/graemesmith-code/investigative-methods','branch':branch,'remote_commit':commit,'baseline':base,'publication_status':'remote commit and every scoped file hash verified','unrelated_changed_paths':[],'verified_files':len(verified),'files':verified,'method':'Remote ref checked, fetched commit objects read and SHA256 compared with local final bytes; scope diff checked against baseline. This is not merely a local-commit assertion.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--commit',required=True);a.add_argument('--branch',default='main');a.add_argument('--base',default='6b89a82154d28fdc94ff7848407e335ecb24ec35');a.add_argument('--output',required=True);args=a.parse_args()
 result=run(args.commit,args.branch,args.base);pathlib.Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
