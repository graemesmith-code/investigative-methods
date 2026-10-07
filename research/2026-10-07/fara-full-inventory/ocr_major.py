"""Reproduce OCR search aids from original PDFs; never infer checkboxes from OCR.

Uses the five PDF event originals in major-original-reconciliation.json. Outputs
physical-page text; original-image review remains separately documented.
"""
import pathlib,json,fitz,subprocess,tempfile,os
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[2]
def run():
 for case in json.loads((P/'major-original-reconciliation.json').read_text()):
  for e in case['events']:
   if e.get('format')!='pdf':continue
   doc=fitz.open(ROOT/e['original_file'])
   for i,page in enumerate(doc):
    out=P/'sources'/f"major-{e['uuid']}-{i+1}.ocr.txt"
    if out.exists():continue
    with tempfile.TemporaryDirectory(prefix='lobbying-ocr-') as tmp:
     img=pathlib.Path(tmp)/'page.png';page.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(img)
     result=subprocess.run(['tesseract',str(img),'stdout'],capture_output=True,text=True,timeout=180,env={**os.environ,'OMP_THREAD_LIMIT':'1'},check=True)
     out.write_text(result.stdout)
if __name__=='__main__':run()
