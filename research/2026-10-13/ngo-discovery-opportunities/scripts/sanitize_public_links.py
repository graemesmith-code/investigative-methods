#!/usr/bin/env python3
"""Strip transient signing query values from public-link metadata, not original bytes."""
import json
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
P=Path(__file__).resolve().parents[1]
def clean(x):
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 if isinstance(x,str) and x.startswith(('https://','http://')):
  s=urlsplit(x);q=parse_qsl(s.query,keep_blank_values=True)
  safe=[(k,v) for k,v in q if k.lower() not in {'signature','keyid','sig','access_token','token'} and not k.lower().startswith('x-amz-')]
  if len(safe)!=len(q):return urlunsplit((s.scheme,s.netloc,s.path,urlencode(safe),s.fragment))
 return x
n=0
for f in P.rglob('*'):
 if f.suffix not in {'.json','.jsonl'}:continue
 text=f.read_text()
 if f.suffix=='.json':
  r=json.loads(text);c=clean(r)
  if c!=r:f.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');n+=1
 else:
  rr=[json.loads(l) for l in text.splitlines() if l.strip()];cc=clean(rr)
  if cc!=rr:f.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in cc));n+=1
print(json.dumps({'files_with_public_signature_queries_removed':n,'note':'Fresh signed URLs must be fetched through stable source IDs/APIs; manifests retain canonical paths.'}))
