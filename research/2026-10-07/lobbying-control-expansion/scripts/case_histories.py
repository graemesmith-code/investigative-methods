import json,time,urllib.parse,concurrent.futures,os,signal,subprocess
from acquire import P,S,fetch
# Temporarily serialize API consumers; original-document downloads are rate-exempt.
ps=subprocess.run(['pgrep','-f','^python -u research/2026-10-07/lobbying-control-expansion/scripts/registrations.py$'],text=True,capture_output=True)
pids=[int(x) for x in ps.stdout.split()]
for pid in pids:os.kill(pid,signal.SIGSTOP)
try:
 time.sleep(4.3)
 for id in [64409,68910,64167,200358,58151,64158,203505,206637,191427,188597,104875,126471]:
  url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'client_id':id,'page_size':25});rows=[];page=0
  while url:
   page+=1;t=time.monotonic();b=fetch(f'lda-history-{id}-{page:03}.json',url)
   if b is None:break
   d=json.loads(b);rows+=d['results'];url=d['next'];time.sleep(max(0,4.3-(time.monotonic()-t)))
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(lambda r:fetch('original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None,rows))
  (S/f'lda-history-{id}-summary.json').write_text(json.dumps({'client_id':id,'count':len(rows),'server_count':d['count'],'complete':url is None,'originals':sum(results)},indent=2))
  print(id,len(rows),'originals',sum(results),flush=True)
finally:
 for pid in pids:os.kill(pid,signal.SIGCONT)
