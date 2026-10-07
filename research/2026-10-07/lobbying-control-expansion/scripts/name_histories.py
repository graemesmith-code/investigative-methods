"""Check exact-client aliases across registrants after the annual loop finishes."""
import json,time,urllib.parse,concurrent.futures,os,signal,subprocess
from acquire import P,S,fetch
ps=subprocess.run(['pgrep','-f','^python -u research/2026-10-07/lobbying-control-expansion/scripts/registrations.py$'],text=True,capture_output=True)
pids=[int(x) for x in ps.stdout.split()]
for pid in pids:os.kill(pid,signal.SIGSTOP)
try:
 time.sleep(4.3)
 for name in ['ARM LIMITED','PRVO','KUCOIN']:
  url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'client_name':name,'page_size':25});rows=[];page=0;d={}
  while url:
   page+=1;t=time.monotonic();b=fetch('lda-name-'+name.replace(' ','_')+f'-{page:03}.json',url)
   if b is None:break
   d=json.loads(b);rows+=d['results'];url=d['next'];time.sleep(max(0,4.3-(time.monotonic()-t)))
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(lambda r:fetch('original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None,rows))
  (P/('name-'+name.replace(' ','_')+'-coverage.json')).write_text(json.dumps({'query':name,'count':len(rows),'server_count':d.get('count'),'complete':url is None,'originals':sum(results),'pairs':sorted(set((r['client']['id'],r['client']['name'],r['registrant']['name']) for r in rows))},indent=2))
  print(name,len(rows),flush=True)
finally:
 for pid in pids:
  try:os.kill(pid,signal.SIGCONT)
  except ProcessLookupError:pass
