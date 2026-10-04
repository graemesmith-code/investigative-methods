import urllib.request,json,pathlib,hashlib,datetime,sys,re
P=pathlib.Path(__file__).resolve().parents[1]
def get(url,label,cap=1500000,save=False):
 d=dict(label=label,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),tls_validation=True)
 try:
  with urllib.request.urlopen(url,timeout=20) as r:raw=r.read(cap+1);d.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes_read=len(raw),truncated=len(raw)>cap,sha256=hashlib.sha256(raw).hexdigest())
  if len(raw)>cap:d['observation']='Read stopped at byte cap; not complete document'
  elif save:
   f=P/'evidence'/label;f.write_bytes(raw);d['saved_file']=str(f.relative_to(P))
  if 'json' in d.get('content_type',''):d['json']=json.loads(raw)
 except Exception as e:d['error']=str(e);raw=b''
 with (P/'evidence/validated-http.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
 print(json.dumps(d));return raw
if __name__=='__main__':get(sys.argv[1],sys.argv[2],save=len(sys.argv)>3)
