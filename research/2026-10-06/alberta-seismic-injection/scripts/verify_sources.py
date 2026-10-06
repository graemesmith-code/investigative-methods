"""Verify every successful acquisition record against current or preserved source bytes."""
import pathlib,json,hashlib,gzip
P=pathlib.Path(__file__).resolve().parents[1];out=[];cache={}
def digest(p):
 if p not in cache:
  h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  cache[p]=h.hexdigest()
 return cache[p]
for line in (P/'sources/manifest.jsonl').read_text().splitlines():
 r=json.loads(line)
 if 'sha256' not in r:continue
 candidates=[P/'sources'/r['name'],P/'sources/pre-audit'/r['name']]
 found=next((p for p in candidates if p.exists() and digest(p)==r['sha256']),None)
 if found:out.append({'name':r['name'],'sha256':r['sha256'],'verified_path':str(found.relative_to(P)),'ok':True});continue
 if r['name']=='SummaryChemical-WaterUse.csv':
  h=hashlib.sha256()
  with gzip.open(P/'sources/SummaryChemical-WaterUse.csv.gz','rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  if h.hexdigest()==r['sha256']:out.append({'name':r['name'],'sha256':r['sha256'],'verified_path':'sources/SummaryChemical-WaterUse.csv.gz (decompressed)','ok':True});continue
 out.append({'name':r['name'],'sha256':r['sha256'],'ok':False})
(P/'results/source-verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('Successful acquisition records verified:',sum(r['ok'] for r in out),'of',len(out))
assert all(r['ok'] for r in out),[r for r in out if not r['ok']]
