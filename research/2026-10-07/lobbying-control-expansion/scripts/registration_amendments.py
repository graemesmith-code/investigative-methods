"""Recover all RA records for the entire missing-RR group, serial public API."""
import json,time,urllib.parse,concurrent.futures
from acquire import P,S,fetch
screen={x['client_id']:x for x in json.loads((P/'client-screen.json').read_text())}
selection=[x for x in json.loads((P/'rr-coverage.json').read_text()) if x['rr_count']==0 and screen[x['client_id']]['country']=='US']
(P/'missing-rr-selection.json').write_text(json.dumps({'rule':'Every screened US-domiciled client ID with zero RR records returned; no company-name exceptions. All RA records are sought. Missing RR is an access/history gap, never a clean result.','selected_client_ids':[x['client_id'] for x in selection]},indent=2))
out=[]
for c in selection:
 id=c['client_id'];history=S/f'lda-history-{id}-summary.json';rows=[];reused=False;complete=False;count=None
 if history.exists() and json.loads(history.read_text())['complete']:
  rows=[r for f in S.glob(f'lda-history-{id}-[0-9]*.json') for r in json.loads(f.read_text())['results'] if r['filing_type']=='RA'];reused=True;complete=True;count=len(rows)
 else:
  url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'client_id':id,'filing_type':'RA','page_size':25});page=0
  while url:
   page+=1;t=time.monotonic();b=fetch(f'lda-ra-gap-{id}-{page:03}.json',url)
   if b is None:break
   d=json.loads(b);rows+=d['results'];url=d['next'];count=d['count'];time.sleep(max(0,4.3-(time.monotonic()-t)))
  complete=url is None
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:access=list(ex.map(lambda r:fetch('original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None,rows))
 out.append({'client_id':id,'client':c['name'],'ra_count':len(rows),'server_count':count,'complete':complete,'reused_complete_history':reused,'originals':sum(access),'uuids':[r['filing_uuid'] for r in rows]})
 (P/'missing-rr-ra-coverage.json').write_text(json.dumps(out,indent=2));print(len(out),len(selection),id,'RA',len(rows),flush=True)
