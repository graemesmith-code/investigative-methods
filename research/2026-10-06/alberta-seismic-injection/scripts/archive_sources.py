"""Lossless multipart storage for official source archives above GitHub's per-file limit."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1];S=P/'sources';A=S/'multipart';A.mkdir(exist_ok=True)
manifest=[]
for name in ['ST37-excel.zip','order-shapes.zip']:
 p=S/name;parts=[]
 with p.open('rb') as f:
  i=0
  while b:=f.read(40*1024*1024):
   out=A/f'{name}.part{i:03d}';out.write_bytes(b);parts.append({'path':str(out.relative_to(P)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});i+=1
 manifest.append({'original':'sources/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'parts':parts})
(A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Lossless source archives:',len(manifest),'parts',sum(len(x['parts']) for x in manifest))
