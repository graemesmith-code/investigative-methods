#!/usr/bin/env python3
"""Bounded access-only check, no accusations, no paid calls. First 100 recent modifications."""
import urllib.request,json,pathlib,hashlib,concurrent.futures
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-integrity-cache');out=[]
def get(u):
 try:
  b=urllib.request.urlopen(u,timeout=30).read();h=hashlib.sha256(b).hexdigest();(C/h).write_bytes(b);out.append(dict(url=u,status='acquired',bytes=len(b),sha256=h));return b
 except Exception as e:out.append(dict(url=u,status='failed',error=str(e)));return b''
u='https://public.api.openprocurement.org/api/2.5/tenders?limit=100&descending=1';rs=json.loads(get(u))['data']
def one(r):
 b=get('https://public.api.openprocurement.org/api/2.5/tenders/'+r['id']);return json.loads(b)['data'] if b else None
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:ts=list(ex.map(one,rs))
cs=[t for t in ts if t and any(str(i.get('classification',{}).get('id','')).startswith('45') for i in t.get('items',[]))]
summary=[]
for t in cs:
 summary.append(dict(id=t['id'],tenderID=t.get('tenderID'),title=t.get('title'),procurementMethodType=t.get('procurementMethodType'),status=t.get('status'),documents=[dict(id=d.get('id'),title=d.get('title'),url=d.get('url')) for d in t.get('documents',[])],awards=len(t.get('awards',[])),bids=len(t.get('bids',[]))))
# only one construction tender's first qualification/contract document; do not claim representative.
if cs:
 for d in cs[0].get('documents',[])[:2]:
  if d.get('url'):get(d['url'])
(P/'prozorro-pilot.json').write_text(json.dumps(dict(bounded_population=len(rs),construction_tenders=len(cs),sample=summary,access_checks=out),ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))

import subprocess
subprocess.run(["python", str(P/"scrub_urls.py")], check=True)
