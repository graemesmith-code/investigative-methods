#!/usr/bin/env python3
"""Local raster OCR for private working snapshots; public audit emits no text.

Optional dependencies: PyMuPDF, tesseract with the selected language installed.
No network, account, paid model or automatic retry. OCR is not accuracy proof.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,os,subprocess,time
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf',type=Path);p.add_argument('private_output',type=Path)
    p.add_argument('audit_jsonl',type=Path);p.add_argument('--expected-sha256',required=True)
    p.add_argument('--workers',type=int,default=4);p.add_argument('--max-pages',type=int,default=1000)
    p.add_argument('--language',default='eng');a=p.parse_args()
    if not 1<=a.workers<=8:raise ValueError('workers must be1–8')
    if hashlib.sha256(a.pdf.read_bytes()).hexdigest()!=a.expected_sha256:
        raise ValueError('Source hash mismatch')
    import fitz
    with fitz.open(a.pdf) as doc:count=len(doc)
    if count>a.max_pages:raise ValueError('PDF exceeds declared page bound')
    a.private_output.mkdir(parents=True,exist_ok=True)
    a.audit_jsonl.parent.mkdir(parents=True,exist_ok=True)
    if any(a.private_output.glob('page-*.txt')):
        raise FileExistsError('Existing OCR text: preserve it and choose a new variant directory')
    engine=subprocess.check_output(['tesseract','--version'],text=True,stderr=subprocess.STDOUT).splitlines()[0]
    def one(page):
        started=time.monotonic();image=a.private_output/f'page-{page:03}.png'
        text=a.private_output/f'page-{page:03}.txt'
        try:
            with fitz.open(a.pdf) as doc:
                doc[page-1].get_pixmap(matrix=fitz.Matrix(1.7,1.7),colorspace=fitz.csGRAY).save(image)
            env=os.environ.copy();env['OMP_THREAD_LIMIT']='1'
            result=subprocess.run(['tesseract',str(image),str(text.with_suffix('')),
                                   '--psm','3','-l',a.language],env=env,capture_output=True,timeout=45)
            if result.returncode:raise RuntimeError('tesseract exit '+str(result.returncode))
            body=text.read_bytes();image.unlink()
            return {'page':page,'status':'ocr_complete_unvalidated','bytes':len(body),
              'text_sha256':hashlib.sha256(body).hexdigest(),'engine':engine,
              'language':a.language,'raster_scale':1.7,'colourspace':'grayscale','psm':3,
              'seconds':round(time.monotonic()-started,2),'image_visual_review':'not_complete'}
        except Exception as e:
            return {'page':page,'status':'ocr_failure','error_type':type(e).__name__,
                    'seconds':round(time.monotonic()-started,2)}
    with a.audit_jsonl.open('x') as f,ThreadPoolExecutor(max_workers=a.workers) as pool:
        for row in pool.map(one,range(1,count+1)):
            f.write(json.dumps(row)+'\n');f.flush()
    print(json.dumps({'pages_attempted':count,'audit':str(a.audit_jsonl),
                      'status':'OCR attempted; inspect per-page outcomes and compare to originals'}))

if __name__=='__main__':main()
