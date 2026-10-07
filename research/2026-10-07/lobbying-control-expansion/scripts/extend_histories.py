"""Acquire missing histories for frozen source-driven US disclosure selection."""
import json,time,urllib.parse,concurrent.futures
from acquire import P,S,fetch
selected=json.loads((P/'history-expansion-selection.json').read_text())['selected'];coverage=[]
for c in selected:
 id=c['client_id'];summary=S/f'lda-history-{id}-summary.json'
 if summary.exists() and json.loads(summary.read_text())['complete']:
  coverage.append({**json.loads(summary.read_text()),'reused':True});continue
 url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'client_id':id,'page_size':25});rows=[];page=0;d={}
 while url:
  page+=1;t=time.monotonic();b=fetch(f'lda-history-{id}-{page:03}.json',url)
  if b is None:break
  d=json.loads(b);rows+=d['results'];url=d['next'];time.sleep(max(0,4.3-(time.monotonic()-t)))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:access=list(e.map(lambda r:fetch('original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None,rows))
 s={'client_id':id,'count':len(rows),'server_count':d.get('count'),'complete':url is None,'originals':sum(access)};summary.write_text(json.dumps(s,indent=2));coverage.append({**s,'reused':False})
 (P/'history-expansion-coverage.json').write_text(json.dumps(coverage,indent=2));print(id,c['client'],len(rows),'originals',sum(access),flush=True)
(P/'history-expansion-coverage.json').write_text(json.dumps(coverage,indent=2))
