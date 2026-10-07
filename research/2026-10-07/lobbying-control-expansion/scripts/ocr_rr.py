"""Local OCR of image-only original RR PDFs; untrusted search aid, not field verdict."""
import json,fitz,subprocess,tempfile,concurrent.futures,os
from acquire import P,S
rows=json.loads((P/'rr-coverage.json').read_text());tasks=[]
for r in rows:
 for id in r['uuids']:
  f=S/('original-'+id+'.html')
  if f.exists() and f.read_bytes().startswith(b'%PDF'):tasks.append((id,r['name']))
def one(t):
 id,name=t;out=S/('rr-ocr-'+id+'.txt')
 if out.exists():return {'uuid':id,'client':name,'characters':len(out.read_text()),'cached':True}
 doc=fitz.open(stream=(S/('original-'+id+'.html')).read_bytes(),filetype='pdf');texts=[]
 with tempfile.TemporaryDirectory(prefix='lda-rr-ocr-') as td:
  for i,page in enumerate(doc):
   f=td+'/page.png';page.get_pixmap(matrix=fitz.Matrix(2,2)).save(f)
   r=subprocess.run(['tesseract',f,'stdout'],capture_output=True,text=True,env={**os.environ,'OMP_THREAD_LIMIT':'1'},timeout=45,check=True)
   texts.append('PDF page '+str(i+1)+'\n'+r.stdout)
 out.write_text('\n\f\n'.join(texts));return {'uuid':id,'client':name,'characters':out.stat().st_size,'pages':len(doc),'body_is_ocr_not_verified_transcription':True}
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
 for r in e.map(one,tasks):out.append(r)
(P/'rr-ocr-access.json').write_text(json.dumps(out,indent=2));print('OCR complete',len(out),flush=True)
