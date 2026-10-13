"""Enumerate official English publication URLs; acquire landing metadata without claiming reading.
Python stdlib only. Copyrighted bodies remain in /tmp. Sitemap lastmod is NOT publication date.
"""
import concurrent.futures, hashlib, html, json, re, urllib.request
from pathlib import Path
ROOT=Path(__file__).parent
CACHE=Path('/tmp/ngo-secrecy'); CACHE.mkdir(exist_ok=True)
def clean(x): return html.unescape(re.sub('<[^>]+>',' ',x)).strip()
def get(u):
    ident=hashlib.sha256(u.encode()).hexdigest()[:16]; cache=CACHE/(ident+'.html')
    rec=dict(org='NRGI',url=u,title=None,date=None,type='publication',acquisition_status='not_attempted',fulltext_screened=False,deeply_read=False,bytes=None,sha256=None,pages=None,screening_rationale='Landing metadata acquired; body not yet contextually read',opportunity_ids=[])
    try:
        b=cache.read_bytes() if cache.exists() else urllib.request.urlopen(u,timeout=25).read();cache.write_bytes(b)
        s=b.decode('utf-8','replace'); title=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)
        rec.update(title=clean(title[1]) if title else u.rsplit('/',1)[-1],bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),acquisition_status='landing_html_acquired',cache_file=str(cache))
        import datetime
        visible=re.search(r'c-single-header__date[^>]*>([^<]+)',s)
        rec['date']=datetime.datetime.strptime(visible[1].strip(),'%d %B %Y').date().isoformat() if visible else None
        rec['eligible']=None if not rec['date'] else '2016-10-13'<=rec['date']<='2026-10-13'
        rec['pdf_urls']=list(dict.fromkeys(('https://resourcegovernance.org'+x if x.startswith('/') else x) for x in re.findall(r'href="([^"]+\.pdf[^"]*)"',s)))
    except Exception as e: rec['acquisition_status']='failed: '+str(e)
    return rec
if __name__=='__main__':
    raw=json.load(open(ROOT/'raw_nrgi_sitemap.json')); urls=sorted(set(x['loc'] for x in raw if '/publications/' in x['loc'] and x['loc'].count('/')==4))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        with open(ROOT/'nrgi_landing_inventory.jsonl','w') as f:
            for r in ex.map(get,urls): f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush()
    print('enumerated',len(urls))
