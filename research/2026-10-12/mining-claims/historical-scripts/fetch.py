import urllib.request, urllib.error, json, time, hashlib, pathlib, concurrent.futures, sys, re
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parent
(ROOT/'raw').mkdir(exist_ok=True)
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.items=[]
 def handle_starttag(self, tag, attrs):
  d=dict(attrs)
  if tag in ('a','iframe','script'):
   u=d.get('href') or d.get('src')
   if u:self.items.append(u)
def fetch(item):
 name,url=item
 out={'id':name,'url':url,'tested_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Public-record research access check; single document retrieval'})
  with urllib.request.urlopen(req,timeout=40) as r:
   b=r.read(); out.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  p=ROOT/'raw'/name;p.write_bytes(b);out['local_path']=str(p)
  if 'html' in (out['content_type'] or ''):
   p=Links();p.feed(b.decode('utf-8',errors='replace'));out['links']=p.items
  if b[:4]==b'%PDF':out['magic']='PDF'
  elif b[:2]==b'PK':out['magic']='ZIP/XLSX'
  else:out['prefix']=b[:140].decode('utf-8',errors='replace')
 except Exception as e:out['error']=str(e)
 return out
if __name__=='__main__':
 items=json.load(sys.stdin)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
  results=list(ex.map(fetch,items))
 with open(ROOT/'access-log.jsonl','a') as f:
  for r in results:f.write(json.dumps(r,ensure_ascii=False)+'\n')
 print(json.dumps(results,ensure_ascii=False))
