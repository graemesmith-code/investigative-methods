"""Enumerate RR for every major-cohort client, respecting anonymous API rate."""
import json,time,urllib.parse,concurrent.futures
from acquire import P,S,fetch
clients=json.loads((P/'client-screen.json').read_text())
clients.sort(key=lambda c:(not (c['country']!='US' or c['foreign_additions_present'] or c['fara_report_name_matches']),c['client_id']))
progress=[]
for c in clients:
 rows=[];url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'client_id':c['client_id'],'filing_type':'RR','page_size':25});page=0
 while url:
  page+=1;t=time.monotonic();b=fetch(f"lda-rr-{c['client_id']}-{page:03}.json",url)
  if not b:break
  d=json.loads(b);rows+=d['results'];url=d['next'];time.sleep(max(0,4.3-(time.monotonic()-t)))
 def original(r):return fetch('original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:originals=list(ex.map(original,rows))
 progress.append({'client_id':c['client_id'],'name':c['client_name'],'rr_count':len(rows),'server_count':d['count'] if rows else None,'complete':url is None,'originals_readable':sum(originals),'uuids':[r['filing_uuid'] for r in rows],'foreign_entities':[r['foreign_entities'] for r in rows]})
 (P/'rr-coverage.json').write_text(json.dumps(progress,indent=2));print(len(progress),c['client_name'],len(rows),sum(originals),flush=True)
