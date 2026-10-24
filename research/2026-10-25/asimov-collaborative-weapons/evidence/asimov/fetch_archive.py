import urllib.request,pathlib,concurrent.futures,json,datetime,hashlib
p=pathlib.Path(__file__).resolve().parent / 'raw'
p.mkdir(exist_ok=True)
timestamps=['20250906112754','20260216091212','20260617072907','20260706161318']
def f(ts):
 u='https://web.archive.org/web/'+ts+'id_/https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values'
 try:
  with urllib.request.urlopen(u,timeout=90) as r:d=r.read();final=r.url;headers=dict(r.headers)
  (p/('wayback-'+ts+'.html')).write_bytes(d)
  info={'timestamp_requested':ts,'url':u,'final_url':final,'complete_banner':b'This program is now complete' in d,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'headers':headers,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};print(ts,info['complete_banner'],len(d),final,flush=True);return info
 except Exception as e:print(ts,e,flush=True);return {'timestamp_requested':ts,'url':u,'error':repr(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(f,timestamps))
(p/'wayback-snapshot-index.json').write_text(json.dumps(r,indent=2))
