"""Acquire originals from current reverse-query results; no API queries or paid calls."""
import json,concurrent.futures
from reverse_cohort import P,S,fetch
rows={}
for f in S.glob('lda-reverse-*.json'):
    for r in json.loads(f.read_text())['results']:rows[r['filing_uuid']]=r
def one(r):
    name='lda-original-'+r['filing_uuid']+'.html';body=fetch(name,r['filing_document_url'])
    return {'uuid':r['filing_uuid'],'client_id':r['client']['id'],'client':r['client']['name'],'registrant':r['registrant']['name'],'url':r['filing_document_url'],'acquired':body is not None,'format':'pdf' if body and body.startswith(b'%PDF') else 'html' if body else None,'local_file':'sources/'+name if body else None}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:out=list(executor.map(one,rows.values()))
(P/'reverse-original-coverage.json').write_text(json.dumps(out,indent=2));print('originals',len(out),'acquired',sum(x['acquired'] for x in out))
