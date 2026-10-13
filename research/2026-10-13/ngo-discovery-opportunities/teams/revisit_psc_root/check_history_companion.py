#!/usr/bin/env python3
"""Extend already-registry-nominated controls. Never substitutes names for IDs."""
import datetime,hashlib,json,pathlib,subprocess,urllib.parse,urllib.request
from lxml import html
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-revisit-psc');m=json.loads((P/'cohort-check.json').read_text());out=[];req=[]
for control in m['controls']:
 n=control['company_number'];h=html.fromstring((C/(n+'.html')).read_bytes());documents=[]
 for tr in h.xpath('//table//tr'):
  cells=[' '.join(c.itertext()).strip() for c in tr.xpath('./td')]
  if len(cells)<3 or cells[1] not in ['NEWINC','CS01']:continue
  links=[u for u in tr.xpath('.//a/@href') if 'format=pdf' in u]
  if not links:continue
  url=urllib.parse.urljoin('https://find-and-update.company-information.service.gov.uk',links[0]);r={'url':url,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'company_number':n,'form_type':cells[1],'filing_date':cells[0]}
  try:
   with urllib.request.urlopen(url,timeout=30) as response:b=response.read(15000001);r['status']=response.status
   if len(b)>15000000 or not b.startswith(b'%PDF'):raise ValueError('PDF/cap check failed')
   sha=hashlib.sha256(b).hexdigest();f=C/(sha+'.pdf');f.write_bytes(b);txt=f.with_suffix('.txt');subprocess.run(['pdftotext','-layout',str(f),str(txt)],check=True)
   text=txt.read_text();r.update(bytes=len(b),sha256=sha,pages=text.count('\f'),nonwhitespace_chars=len(''.join(text.split())),text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest())
   if r['nonwhitespace_chars']<30:
    img=C/(sha+'-page');subprocess.run(['pdftoppm','-r','130','-png',str(f),str(img)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    chunks=[]
    for page in sorted(C.glob(sha+'-page-*.png')):
     t=subprocess.run(['tesseract',str(page),'stdout','-l','eng','--psm','3'],capture_output=True,text=True,check=True);chunks.append(t.stdout)
    ocr='\f'.join(chunks);(C/(sha+'.ocr.txt')).write_text(ocr);r.update(local_ocr='tesseract',ocr_nonwhitespace_chars=len(''.join(ocr.split())),ocr_text_sha256=hashlib.sha256(ocr.encode()).hexdigest())
   documents.append(r)
  except Exception as e:r['error']=str(e)
  req.append(r)
 out.append({'company_number':n,'source_selection':'previous frozen data-nominated cohort, not chosen on document content','documents':documents,'historical_effective_dates_need_human_review':True})
(P/'history-companion.json').write_text(json.dumps({'controls':out,'paid_calls':0,'allegations':False,'method':'Read exact HTML filing-table type/date, then actual NEWINC+CS01 PDF bytes, free local OCR only where needed. OCR is a baseline, not a model benefit.'},indent=2)+'\n')
(P/'history-request-manifest.json').write_text(json.dumps(req,indent=2)+'\n')
print(json.dumps({'actual_pdfs':sum(len(o['documents']) for o in out),'pages':sum(d['pages'] for o in out for d in o['documents']),'ocr_documents':sum('local_ocr' in d for o in out for d in o['documents']),'errors':[d.get('error') for d in req if d.get('error')]},indent=2))
