"""Local OCR quality probe, only 25 low-text pages. Originals/extracted text unchanged."""
import json,subprocess,tempfile,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows=[json.loads(x) for x in (R/'results/pages.jsonl').read_text().splitlines()]
out=[]
with tempfile.TemporaryDirectory() as d:
 for p in rows:
  if not p['ocr_needed_candidate']:continue
  image=Path(d)/'page'
  subprocess.run(['pdftoppm','-f',str(p['pdf_page']),'-l',str(p['pdf_page']),'-r','120','-png','-singlefile',str(R/'sources'/(p['document']+'.pdf')),str(image)],check=True,stderr=subprocess.DEVNULL)
  s=subprocess.check_output(['tesseract',str(image)+'.png','stdout','-l','eng'],text=True,stderr=subprocess.DEVNULL)
  out.append(dict(document=p['document'],pdf_page=p['pdf_page'],original_characters=p['characters'],ocr_characters=len(s.strip()),ocr_text=s,engine='tesseract eng 120dpi',interpretation='candidate for visual review; no automatic replacement'))
  (R/'results/ocr-lowtext.json').write_text(json.dumps(out,indent=2))
print('OCR pages',len(out),'more than 80 chars',sum(x['ocr_characters']>80 for x in out))
