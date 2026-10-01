"""OCR image-only publicly linked release; preserves page boundaries and raw hash."""
import json,pathlib,subprocess,concurrent.futures,os
from pipeline import OUT,write
p=OUT/'public-sources'
f=next(f for f in p.glob('*.json') if json.loads(f.read_text())['url'].endswith('.pdf'))
r=json.loads(f.read_text());folder=OUT/'release-ocr';folder.mkdir(exist_ok=True)
if len(list(folder.glob('page-*.png')))!=7: subprocess.run(['pdftoppm','-r','140','-png',str(p/r['raw_file']),str(folder/'page')],check=True,capture_output=True)
def ocr(path):
 result=subprocess.run(['tesseract',str(path),'stdout','-l','eng'],check=True,capture_output=True,text=True,timeout=45,env={**os.environ,'OMP_THREAD_LIMIT':'1'})
 return {'page':int(path.stem.split('-')[-1]),'image':path.name,'text':result.stdout}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: pages=list(pool.map(ocr,sorted(folder.glob('page-*.png'))))
write(folder/'pages.json',{'source_url':r['url'],'source_sha256':r['sha256'],'method':'pdftoppm 140dpi + tesseract eng; OCR requires visual checks','pages':pages})
print('\n'.join('PAGE '+str(x['page'])+'\n'+x['text'] for x in pages))
