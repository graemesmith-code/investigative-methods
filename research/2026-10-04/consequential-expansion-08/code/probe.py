import urllib.request,urllib.error,json,pathlib,hashlib,datetime,sys,re,html
P=pathlib.Path(__file__).resolve().parents[1]
def probe(url,label,cap=600000):
 d=dict(label=label,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 bounded research access check'}),timeout=20) as r:
   raw=r.read(cap+1);d.update(final_url=r.url,status=r.status,content_type=r.headers.get('Content-Type'),read_bytes=len(raw),truncated=len(raw)>cap,sha256_of_read_bytes=hashlib.sha256(raw).hexdigest())
  txt=raw.decode('utf-8','replace');d['links']=[html.unescape(x) for x in re.findall(r'(?:href|src)=[\"\x27]([^\"\x27]+)',txt) if any(t in x.lower() for t in ['tableau','fract','archive','source','png','jpg','video','pdf'])];d['title']=re.findall(r'<title>(.*?)</title>',txt,re.S)[:1]
 except Exception as e:d['error']=str(e);raw=b''
 with (P/'evidence/http-probes.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
 print(json.dumps(d));return raw
if __name__=='__main__':probe(sys.argv[1],sys.argv[2])
