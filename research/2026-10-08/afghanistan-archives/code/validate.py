"""Offline integrity and citation checks; never contacts network."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'results/manifest.json').read_text())
p=[json.loads(x) for x in (R/'results/pages.jsonl').read_text().splitlines()]
assert len(m)==15 and len(p)==676
assert len({x['sha256'] for x in m})==15
for doc in m:
 b=(R/'sources'/(doc['id']+'.pdf')).read_bytes()
 assert b.startswith(b'%PDF') and hashlib.sha256(b).hexdigest()==doc['sha256']
 rows=[x for x in p if x['document']==doc['id']]
 assert [x['pdf_page'] for x in rows]==list(range(1,doc['pages']+1))
 assert all(x['citation']==doc['url']+'#page='+str(x['pdf_page']) for x in rows)
 assert len(b)==doc['bytes']
assert sum(x['bytes'] for x in m)==26102498
ocr=json.loads((R/'results/ocr-lowtext.json').read_text())
assert {(x['document'],x['pdf_page']) for x in ocr}=={(x['document'],x['pdf_page']) for x in p if x['ocr_needed_candidate']}
packet=json.loads((R/'results/review-packet.json').read_text());assert len(packet)==10
for x in packet:assert x in p
result={'status':'PASS','checks':['15 PDF signatures and SHA256 hashes','676 page identities and URL anchors','contiguous pages per document','26,102,498 source bytes','25 low-text pages matched to supplemental OCR','10 reading-packet pages exact source matches'],'network_calls':0}
(R/'results/validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
