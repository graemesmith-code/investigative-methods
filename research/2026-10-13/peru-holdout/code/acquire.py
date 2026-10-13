"""Free acquisition with append-only attempts; raw documents stay outside Git."""
import urllib.request,urllib.error,json,hashlib,time,datetime,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CACHE=Path('/workspace/peru-holdout-cache');CACHE.mkdir(exist_ok=True)
def fetch(id,url,persist=False):
 start=time.perf_counter(); row={'id':id,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'investigative-methods research https://github.com/graemesmith-code/investigative-methods'})
  with urllib.request.urlopen(req,timeout=35) as r:
   b=r.read();row.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
  dest=(ROOT/'provenance' if persist else CACHE)/id;dest.write_bytes(b)
  row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),saved_as=str(dest));return b
 except urllib.error.HTTPError as e:row.update(status=e.code,error='HTTPError');return None
 except Exception as e:row.update(error=type(e).__name__);return None
 finally:
  row['elapsed_seconds']=time.perf_counter()-start
  with (ROOT/'provenance/acquisition.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
if __name__=='__main__':fetch(sys.argv[1],sys.argv[2],len(sys.argv)>3)
