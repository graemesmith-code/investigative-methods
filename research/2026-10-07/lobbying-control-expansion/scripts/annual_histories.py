"""Retrieve all 2025 reports for each screened client, including downward amendments."""
import json,time,urllib.parse,os,signal,subprocess
from acquire import P,S,fetch
ps=subprocess.run(['pgrep','-f','^python -u research/2026-10-07/lobbying-control-expansion/scripts/registrations.py$'],text=True,capture_output=True)
pids=[int(x) for x in ps.stdout.split()]
for pid in pids:os.kill(pid,signal.SIGSTOP)
progress=[]
try:
 time.sleep(4.3)
 for c in json.loads((P/'client-screen.json').read_text()):
  cid=c['client_id'];rows=[];page=0;d={}
  url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'client_id':cid,'filing_year':2025,'page_size':25})
  while url:
   page+=1;t=time.monotonic();b=fetch(f'lda-annual-{cid}-{page:03}.json',url)
   if b is None:break
   d=json.loads(b);rows+=d['results'];url=d['next'];time.sleep(max(0,4.3-(time.monotonic()-t)))
  progress.append({'client_id':cid,'name':c['client_name'],'count':len(rows),'server_count':d.get('count'),'complete':url is None})
  (P/'annual-coverage.json').write_text(json.dumps(progress,indent=2))
  print(len(progress),cid,len(rows),flush=True)
finally:
 for pid in pids:
  try:os.kill(pid,signal.SIGCONT)
  except ProcessLookupError:pass
