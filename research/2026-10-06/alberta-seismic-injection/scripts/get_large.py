from acquire import ROOT
import urllib.request,gzip,hashlib,json,datetime
url='https://www.aer.ca/documents/by-topic/hydraulic-fracturing/SummaryChemical-WaterUse.csv'
p=ROOT/'sources/SummaryChemical-WaterUse.csv.gz'
r={'name':p.name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limit_bytes':1_000_000_000,'reason':'Official whole-province ingredient-level table; streaming gzip avoids memory and repository overhead','tls_verification':True}
n=0;h=hashlib.sha256()
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Public-record-research/1.0'}),timeout=120) as resp,gzip.open(p,'wb') as out:
  r.update(status=resp.status,final_url=resp.url,content_length=resp.headers.get('Content-Length'))
  while b:=resp.read(1024*1024):
   n+=len(b)
   if n>r['limit_bytes']:raise ValueError('1GB scoped limit')
   h.update(b);out.write(b)
 r.update(uncompressed_bytes=n,uncompressed_sha256=h.hexdigest(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
except Exception as e:r.update(error_type=type(e).__name__,error=str(e));p.unlink(missing_ok=True)
with (ROOT/'sources/manifest.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
print(json.dumps(r))
