#!/usr/bin/env python3
"""Bounded public acquisition; immutable payloads + append-only HTTP manifest. No secrets."""
import argparse,datetime,hashlib,json,pathlib,shutil,sys,time
import requests
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=pathlib.Path('/workspace/task-data/future-warfare-investments')
MAX_TOTAL=15_000_000_000
MIN_FREE=6_000_000_000

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save_json(p,obj):
 p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def fetch(source,url,filename,cap=1_000_000_000):
 out=DATA/'raw'/source/filename;out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():return out
 event={'source':source,'url':url,'retrieved_at':now(),'relative_path':str(out.relative_to(DATA))}
 try:
  if sum(x.stat().st_size for x in (DATA/'raw').rglob('*') if x.is_file())>=MAX_TOTAL:raise RuntimeError('15GB download budget reached')
  r=requests.get(url,stream=True,timeout=(20,120));event.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),etag=r.headers.get('ETag'),last_modified=r.headers.get('Last-Modified'));r.raise_for_status()
  size=0;h=hashlib.sha256();temp=out.with_suffix(out.suffix+'.part')
  with temp.open('wb') as f:
   for b in r.iter_content(1024*1024):
    size+=len(b)
    if size>cap or shutil.disk_usage(DATA).free<MIN_FREE:raise RuntimeError('source byte cap or disk headroom reached')
    f.write(b);h.update(b)
  temp.rename(out);event.update(bytes=size,sha256=h.hexdigest(),outcome='downloaded')
 except Exception as e:
  event.update(outcome='failed',error=str(e));out.with_suffix(out.suffix+'.part').unlink(missing_ok=True)
 finally:
  with (ROOT/'validation/http_manifest.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
  print(json.dumps(event),flush=True)
 return out if out.exists() else None

def usaspending(name,filters):
 payload={'filters':filters,'limit':500000,'file_format':'csv'}
 request_path=ROOT/'evidence'/f'{name}_request.json';save_json(request_path,payload)
 resp_path=ROOT/'evidence'/f'{name}_response.json'
 if resp_path.exists():j=json.loads(resp_path.read_text())
 else:
  r=requests.post('https://api.usaspending.gov/api/v2/download/transactions/',json=payload,timeout=180);r.raise_for_status();j=r.json();save_json(resp_path,j)
 url=j['status_url'].replace('http://','https://')
 for _ in range(120):
  r=requests.get(url,timeout=90);r.raise_for_status();status=r.json();save_json(ROOT/'evidence'/f'{name}_status.json',status)
  print(name,status,flush=True)
  if status.get('status')=='finished':return fetch(name,j['file_url'] if j['file_url'].startswith('http') else 'https://api.usaspending.gov'+j['file_url'],j['file_name'],2_000_000_000)
  if status.get('status')=='failed':raise RuntimeError(status)
  time.sleep(15)
 raise RuntimeError('generation did not finish in 30 minutes; retry existing status URL')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode');a=p.parse_args()
 if a.mode=='sbir':fetch('sbir','https://data.www.sbir.gov/awarddatapublic/award_data.csv','award_data.csv',600_000_000)
 elif a.mode=='grants':fetch('grants','https://prod-grants-gov-chatbot.s3.amazonaws.com/extracts/GrantsDBExtract20261016v2.zip','GrantsDBExtract20261016v2.zip',150_000_000)
 elif a.mode=='darpa':usaspending('usaspending_darpa',{'time_period':[{'start_date':'2018-10-01','end_date':'2026-09-30'}],'award_type_codes':['A','B','C','D'],'agencies':[{'type':'awarding','tier':'subtier','name':'Defense Advanced Research Projects Agency'}]})
