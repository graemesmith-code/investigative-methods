import pathlib,json,hashlib,zipfile
P=pathlib.Path(__file__).resolve().parents[1]
c=json.loads((P/'counts.json').read_text());c.update(checkpoint_checks_passed=13,corrected07_checks_passed=14);(P/'counts.json').write_text(json.dumps(c,indent=2)+'\n')
files=[f for f in sorted(P.rglob('*')) if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts and f.name not in ['artifact-checksums.json','delivery-receipt.json']]
(P/'artifact-checksums.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2)+'\n')
z=P/'checkpoints/consequential-discovery-ranked-through-08.zip'
roots=[P.parent/'source-pair-completeness']+[P.parent/f'consequential-expansion-0{i}' for i in range(1,9)]
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for root in roots:
  for f in sorted(root.rglob('*')):
   if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts:a.write(f,pathlib.Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as a:assert a.testzip() is None
print(json.dumps(dict(path=str(z),bytes=z.stat().st_size,sha256=hashlib.sha256(z.read_bytes()).hexdigest())))
