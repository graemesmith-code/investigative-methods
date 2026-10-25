#!/usr/bin/env python3
"""Scan restored canonical files and expanded gzip streams for configured secrets.
No values are logged; no source bytes, credentials or repository refs are changed.
This checks exact configured literals, not every possible unknown secret.
"""
import argparse,gzip,json,os,pathlib,re
P=pathlib.Path(__file__).resolve().parents[1]
def run(root):
 secrets={v.encode() for k,v in os.environ.items() if re.search('API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL',k,re.I) and len(v)>=12}
 width=max(map(len,secrets),default=1);count=0;files=0;bad=[]
 for f in root.rglob('*'):
  if not f.is_file():continue
  files+=1
  for opener in [open]+([gzip.open] if f.name.endswith('.gz') else []):
   tail=b''
   with opener(f,'rb') as inp:
    for b in iter(lambda:inp.read(1048576),b''):
     block=tail+b
     if any(s in block for s in secrets):bad.append(str(f.relative_to(root)));break
     tail=block[-max(1,width-1):]
   count+=1
 assert not bad,'Configured credential literal found; source must not be published'
 result={'canonical_files':files,'file_or_expanded_gzip_streams_scanned':count,'configured_credential_like_literal_count':len(secrets),'matches':0,'values_not_logged':True,'limit':'Exact configured credential-like environment literals, including gzip-expanded content; not a claim to detect every unknown secret. Source archive member bytes remain unchanged.','archive_sha256':'2fda8de2231b5bed45041a7846a89b11fce50a7c82671b6b176eeb2630d2094c'}
 (P/'audit/recovery-content-safety-scan.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--canonical',required=True,type=pathlib.Path);run(a.parse_args().canonical)
