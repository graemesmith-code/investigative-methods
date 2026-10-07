"""Public retrieval with TLS verification, immutable response cache and provenance."""
import pathlib,urllib.request,urllib.parse,json,datetime,hashlib
P=pathlib.Path(__file__).resolve().parents[1]; S=P/'sources';S.mkdir(exist_ok=True)
def fetch(name,url):
 p=S/name
 if p.exists():return p.read_bytes()
 record={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tls_verified':True}
 try:
  with urllib.request.urlopen(url,timeout=35) as r:
   b=r.read(20000001);record.update(status=r.status,final_url=r.url)
  if len(b)>20000000:raise ValueError('20MB retrieval limit')
  p.write_bytes(b);record.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest());return b
 except Exception as e:record['error']=str(e);return None
 finally:
  with (S/'manifest.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
def lda(name,params,max_pages=40):
 u='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'page_size':100,**params});out=[];pages=0
 while u and pages<max_pages:
  pages+=1;b=fetch(f'lda-{name}-{pages:03}.json',u)
  if b is None:break
  x=json.loads(b);out+=x['results'];u=x['next']
 summary={'name':name,'params':params,'pages':pages,'count':len(out),'server_count':x['count'] if pages and b else None,'remaining_next':u,'complete_query':u is None}
 (S/f'lda-{name}-summary.json').write_text(json.dumps(summary,indent=2));return out
if __name__=='__main__':
 import sys
 for name in sys.argv[1:]:
  rows=lda(name.replace(' ','_'),{'client_name':name,'filing_year':2025});print(name,len(rows),[(r['client']['name'],r['registrant']['name']) for r in rows[:4]],flush=True)
