import urllib.request,urllib.error,datetime,hashlib,json,pathlib,concurrent.futures
base=pathlib.Path('spine_regulatory');base.mkdir(exist_ok=True)
def fetch(x):
 name,url=x;rec={'name':name,'url':url,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=urllib.request.urlopen(url,timeout=40);b=r.read();rec.update(status=r.status,mime=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),final_url=r.url)
  if b'<title>Just a moment' in b or b'challenge-platform' in b or b'Access Denied' in b[:2000]: rec['blocked']='security wrapper, not preserved'
  else: (base/'raw'/name).write_bytes(b);rec['path']=str((base/'raw'/name).resolve())
 except Exception as e:rec.update(error=str(e),status=getattr(e,'code',None))
 print(json.dumps(rec),flush=True);return rec
items=json.loads((base/'urls.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(fetch,items))
(base/'fetch-log.json').write_text(json.dumps(out,indent=2))
