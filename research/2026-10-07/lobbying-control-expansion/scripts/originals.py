"""Acquire original forms for cohort and acquired annual histories; API-rate exempt."""
import json,concurrent.futures
from acquire import P,S,fetch
rows={r['filing_uuid']:r for r in json.loads((P/'major-cohort.json').read_text())}
for f in S.glob('lda-annual-*.json'):
 for r in json.loads(f.read_text())['results']:rows[r['filing_uuid']]=r
def one(r):
 b=fetch('original-'+r['filing_uuid']+'.html',r['filing_document_url'])
 return {'uuid':r['filing_uuid'],'url':r['filing_document_url'],'readable_html':bool(b and (b'LD-1 Disclosure Form' in b or b'LD-2 Disclosure Form' in b)),'bytes':len(b) if b else None}
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(one,rows.values()):
  out.append(r)
  if len(out)%50==0:(P/'original-access.json').write_text(json.dumps(out,indent=2));print(len(out),len(rows),flush=True)
(P/'original-access.json').write_text(json.dumps(out,indent=2))
print('Originals',len(out),'readable',sum(r['readable_html'] for r in out),flush=True)
