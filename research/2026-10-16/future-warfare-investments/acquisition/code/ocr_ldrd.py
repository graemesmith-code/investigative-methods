#!/usr/bin/env python3
"""OCR only the two scanned DOE annual reports; temporary page renders deleted after each page."""
import concurrent.futures,json,pathlib,re,subprocess,tempfile,os
os.environ['OMP_THREAD_LIMIT']='1'
from acquire import DATA,ROOT,save_json
profiles=[]
for year in [2019,2021]:
 p=DATA/'raw/doe_ldrd'/f'DOE_FY{year}_LDRD_1.pdf';dest=DATA/'normalized'/f'{p.stem}.ocr.json'
 if dest.exists():continue
 info=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True).stdout;n=int(re.search(r'Pages:\s+(\d+)',info)[1])
 def page(i):
  with tempfile.TemporaryDirectory(prefix='ldrd-ocr-',dir='/tmp') as tmp:
   prefix=str(pathlib.Path(tmp)/'page');subprocess.run(['pdftoppm','-f',str(i),'-l',str(i),'-singlefile','-scale-to','2200','-png',str(p),prefix],check=True,capture_output=True)
   r=subprocess.run(['tesseract',prefix+'.png','stdout','--psm','6'],capture_output=True,text=True,check=True)
   print(p.name,'OCR page',i,'chars',len(r.stdout),flush=True);return i,r.stdout
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(page,range(1,n+1)))
 version=subprocess.run(['tesseract','--version'],capture_output=True,text=True).stdout.splitlines()[0];save_json(dest,{'raw_file':p.name,'engine':version,'render':'pdftoppm PNG scale-to 2200 pixels','pages':{str(i):t for i,t in results},'warning':'OCR-derived text; amounts, names and quotes require inspection against page image.'});profiles.append({'file':p.name,'pages':n,'ocr_chars':sum(len(t) for _,t in results),'engine':version})
save_json(ROOT/'validation/ldrd_ocr_profile.json',profiles)
