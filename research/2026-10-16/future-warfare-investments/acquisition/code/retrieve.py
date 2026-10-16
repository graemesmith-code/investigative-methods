#!/usr/bin/env python3
"""Retrieve manifest payloads or regenerate a bounded USAspending export. Never prints credentials."""
import argparse,hashlib,json,pathlib,time
import requests
from acquire import ROOT,DATA,fetch,save_json,now
p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--regenerate',action='store_true');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
entries=[json.loads(x) for x in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines()];entries=[x for x in entries if x['outcome']=='downloaded' and (not a.source or x['source']==a.source)]
if a.regenerate:
 if not a.source or not a.source.startswith('usaspending_'):raise SystemExit('--regenerate requires a USAspending source name')
 payload=json.loads((ROOT/'evidence'/f'{a.source}_request.json').read_text());r=requests.post('https://api.usaspending.gov/api/v2/download/transactions/',json=payload,timeout=180);r.raise_for_status();j=r.json();save_json(DATA/'logs'/f'{a.source}_regenerated_response.json',{'retrieved_at':now(),'response':j,'payload':payload})
 for _ in range(120):
  s=requests.get(j['status_url'].replace('http://','https://'),timeout=90);s.raise_for_status();status=s.json()
  if status['status']=='finished':
   fetch(a.source,status.get('file_url') or j['file_url'],j['file_name'],2_000_000_000);break
  if status['status']=='failed':raise SystemExit(status)
  time.sleep(15)
 else:raise SystemExit('Export still pending after 30 minutes; use saved status URL later')
 print('Regenerated data is a new snapshot; compare its checksum and row counts before use.')
else:
 for e in entries:
  path=DATA/e['relative_path']
  if not a.verify_only and not path.exists():fetch(e['source'],e['url'],path.name,max(e['bytes']*2,5_000_000))
  if path.exists():
   h=hashlib.sha256()
   with path.open('rb') as f:
    for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
   good=h.hexdigest()==e['sha256']
   print(json.dumps({'source':e['source'],'path':str(path),'bytes':path.stat().st_size,'expected_sha256':e['sha256'],'actual_sha256':h.hexdigest(),'match':good}))
   if not good:raise SystemExit('Snapshot checksum differs; retain as a new vintage, not the original acquisition.')
  else:print(json.dumps({'source':e['source'],'missing':str(path)}))
