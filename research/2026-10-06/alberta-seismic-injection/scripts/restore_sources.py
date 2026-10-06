from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1]
for r in json.loads((P/'sources/multipart/manifest.json').read_text()):
 p=P/r['original']
 if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']:continue
 tmp=p.with_suffix('.restore.tmp');h=hashlib.sha256()
 with tmp.open('wb') as out:
  for part in r['parts']:
   b=(P/part['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==part['sha256'];out.write(b);h.update(b)
 assert h.hexdigest()==r['sha256'];tmp.replace(p)
 print('Restored',r['original'])
