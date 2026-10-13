"""Bounded public filing access/OCR pilot; no model calls or allegation inference.
Sequential company IDs are preselected transport/interpretation controls, not suspects.
Default output stays in /tmp; copyrighted documents are not committed.
"""
import hashlib,html,json,re,subprocess,urllib.request
from pathlib import Path
CACHE=Path('/tmp/revisit-ownership');CACHE.mkdir(exist_ok=True)
BASE='https://find-and-update.company-information.service.gov.uk'
def acquire(url):
    r=urllib.request.urlopen(url,timeout=30);b=r.read();sha=hashlib.sha256(b).hexdigest()
    return b,dict(url=url,status=r.status,bytes=len(b),sha256=sha)
if __name__=='__main__':
    records=[]
    for company in ['11800000','11800001']:
        for endpoint in ['filing-history','persons-with-significant-control']:
            u=f'{BASE}/company/{company}/{endpoint}'
            try:
                b,d=acquire(u);d.update(company_id=company,type=endpoint);records.append(d)
                if endpoint!='filing-history':continue
                for row in re.findall(r'<tr[^>]*>(.*?)</tr>',b.decode(),re.S):
                    desc=' '.join(html.unescape(re.sub('<[^>]*>',' ',row)).split())
                    links=re.findall(r'href="([^"]+document\?format=pdf[^\"]*)"',row)
                    selected=(company=='11800000' and ('NEWINC' in desc or ('CS01' in desc and 'with updates' in desc) or 'PSC01' in desc)) or (company=='11800001' and 'CS01' in desc)
                    if not links or not selected:continue
                    pdf,d=acquire(BASE+html.unescape(links[0]));d.update(company_id=company,type=desc.split()[3] if len(desc.split())>3 else 'filing')
                    f=CACHE/(d['sha256']+'.pdf');f.write_bytes(pdf)
                    subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True,capture_output=True)
                    t=f.with_suffix('.txt').read_text();d['pages']=t.count('\f');d['text_chars']=len(t)
                    if not t.strip():
                        stem=str(CACHE/('ocr-'+d['sha256']))
                        subprocess.run(['pdftoppm','-r','130','-png',str(f),stem],check=True,capture_output=True)
                        texts=[]
                        for img in sorted(CACHE.glob('ocr-'+d['sha256']+'-*.png')):
                            texts.append(subprocess.run(['tesseract',str(img),'stdout'],check=True,capture_output=True,text=True).stdout)
                        t='\f'.join(texts);f.with_suffix('.ocr.txt').write_text(t);d['ocr_chars']=len(t)
                    # Mechanical passage candidates, not semantic/legal findings.
                    d['baseline_hits']={x:len(re.findall(re.escape(x),t,re.I)) for x in ['prescribed particulars','voting','ordinary','transferred','no updates','nature of control']}
                    records.append(d)
                    if company=='11800001':break
            except Exception as e:records.append(dict(url=u,error=str(e)))
    json.dump(records,open(CACHE/'manifest.json','w'),indent=2)
    print('Manifest:',CACHE/'manifest.json','records:',len(records))
