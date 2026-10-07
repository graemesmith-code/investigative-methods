"""Small shareable review pack; complete source corpus remains on private branch."""
from pathlib import Path
import zipfile
P=Path(__file__).resolve().parents[1]
out=P/'lobbying-control-expansion-review.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(P.iterdir()):
  if f.is_file() and f.suffix in ('.md','.pdf','.csv','.json') and f.name not in ('major-cohort.json','fara-report-principals.json','annual-reconciled.json','delivery.json'):
   z.write(f,'expansion/'+f.name)
 for directory in ['scripts','jev']:
  for f in sorted((P/directory).rglob('*')):
   if f.is_file() and '__pycache__' not in str(f):z.write(f,'expansion/'+str(f.relative_to(P)))
 for name in ['manifest.jsonl','ppd-2024.pdf','ppd-2025.pdf','arm-2023-psc02.pdf','arm-2023-psc05.pdf','arm-2025-note33-ocr.txt','browser-major-originals.json','browser-major-details.json']:
  f=P/'sources'/name
  if f.exists():z.write(f,'expansion/sources/'+name)
 root=P.parents[2]
 z.write(root/'code/ati/pipeline.py','code/ati/pipeline.py')
 prior=P.parent/'lobbying-control-pilot'
 for name in ['README.md','TECHNICAL-ANNEX.md','spending-summary.json','lobbying-control-report.pdf','scripts/guard.py']:
  z.write(prior/name,'first-checkpoint/'+name)
 z.writestr('START-HERE.txt','Open expansion/lobbying-control-expansion-report.pdf. This compact review pack is not the complete offline source corpus and is not arranged as a runnable repository checkout. Full sources and runnable paths are in private repository graemesmith-code/investigative-methods, branch research/lobbying-control-pilot-20261007, directory research/2026-10-07/lobbying-control-expansion. The complete offline ZIP also exists in the executor workspace. Library upload was blocked by authentication before any transfer. Paid calls are closed; never reset ledgers.\n')
print(out,out.stat().st_size)
