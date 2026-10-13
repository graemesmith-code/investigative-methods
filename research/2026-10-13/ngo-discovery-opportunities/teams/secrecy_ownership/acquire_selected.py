"""Reacquire selected official reports without paid APIs, credentials or disabled TLS.
Downloads are temporary; metadata is persistent. Acquiring is not reading.
Run after census_nrgi.py. Requires pdftotext for local PDFs.
"""
import concurrent.futures, hashlib, json, re, subprocess, urllib.request
from pathlib import Path
ROOT=Path(__file__).parent
CACHE=Path('/tmp/ngo-secrecy'); CACHE.mkdir(exist_ok=True)
def acquire(r):
    r['report_files']=[]
    for u in r.get('pdf_urls',[])[:2]:
        try:
            b=urllib.request.urlopen(u,timeout=30).read(); sha=hashlib.sha256(b).hexdigest()
            f=CACHE/(sha+'.pdf');f.write_bytes(b)
            subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True,capture_output=True)
            txt=f.with_suffix('.txt').read_text()
            r['report_files'].append(dict(url=u,bytes=len(b),sha256=sha,pages=txt.count('\f'),cache_file=str(f),text_file=str(f.with_suffix('.txt'))))
        except Exception as e:r['report_files'].append(dict(url=u,error=str(e)))
    return r
if __name__=='__main__':
    records=[json.loads(l) for l in open(ROOT/'nrgi_landing_inventory.jsonl')]
    chosen=[r for r in records if r.get('eligible') and re.search('corrupt|beneficial|payment|contract|trading',r['title'],re.I)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:out=list(pool.map(acquire,chosen))
    json.dump(out,open(ROOT/'nrgi_selected_acquisition.json','w'),ensure_ascii=False,indent=2)
    print('Selected records:',len(out),'Acquired PDF responses:',sum('sha256' in f for r in out for f in r['report_files']))
