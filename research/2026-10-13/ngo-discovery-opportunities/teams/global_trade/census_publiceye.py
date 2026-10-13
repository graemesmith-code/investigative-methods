#!/usr/bin/env python3
"""Official Public Eye catalog census. No challenge bypass; TLS verification on.
Full texts live in /tmp/ngo-global-trade; inventory preserves hashes, not copyrighted text.
Uses lxml (preinstalled); bounded 4-worker acquisition.
"""
import urllib.request,urllib.parse,json,hashlib,concurrent.futures,pathlib,re,subprocess,threading
from lxml import html
OUT=pathlib.Path(__file__).parent; CACHE=pathlib.Path('/tmp/ngo-global-trade');CACHE.mkdir(exist_ok=True)
logs=[]; records={}; rate_limited=threading.Event()
def get(u):
 if rate_limited.is_set():
  logs.append({'url':u,'status':'not_attempted','error':'Circuit breaker after HTTP 429; rerun only when permitted.'});return None
 try:
  r=urllib.request.urlopen(u,timeout=30);b=r.read();logs.append({'url':u,'status':r.status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});return b
 except Exception as e:
  if getattr(e,'code',None)==429:rate_limited.set()
  logs.append({'url':u,'status':'failed','error':str(e)});return None
months={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'november':11,'december':12,'janvier':1,'février':2,'mars':3,'avril':4,'mai':5,'juin':6,'juillet':7,'août':8,'septembre':9,'octobre':10,'novembre':11,'décembre':12,'januar':1,'februar':2,'märz':3,'mai':5,'juni':6,'juli':7,'oktober':10,'dezember':12}
for lang,pub in [('en','publications'),('fr','publications'),('de','publikationen')]:
 for category in ['report','magazine','factsheet']:
  u=f'https://www.publiceye.ch/{lang}/{pub}/publication-category-{category}';b=get(u)
  if not b:continue
  d=html.fromstring(b)
  for a in d.xpath('//a[contains(@class,"PublicationTeaser")]'):
   parts=[' '.join(x.split()) for x in a.xpath('.//text()') if x.strip()]
   if len(parts)<3:continue
   typ,title,date=parts[-3:];m=re.search(r'(\S+) (20\d\d)',date)
   if not m:continue
   month=months.get(m[1].lower());year=int(m[2]);dt=f'{year:04}-{month:02}' if month else str(year)
   if dt<'2016-10' or dt>'2026-10':continue
   url=urllib.parse.urljoin(u,a.get('href')); key=a.get('href').split('/detail/')[-1]
   if key in records:records[key]['alternate_urls'].append(url);continue
   records[key]={'org':'Public Eye','title':title,'date':dt,'date_precision':'month','url':url,'type':category,'catalog_url':u,'alternate_urls':[], 'acquisition_status':'enumerated','fulltext_screened':False,'deeply_read':False,'bytes':None,'sha256':None,'pages':None,'screening_rationale':'Catalog enumeration; not yet substantive reading.','opportunity_ids':[]}
def acquire(r):
 b=get(r['url'])
 if not b:r['acquisition_status']='landing_failed';return r
 d=html.fromstring(b); links=d.xpath('//a[contains(@href,".pdf")]/@href');pdfs=list(dict.fromkeys(urllib.parse.urljoin(r['url'],x) for x in links))
 r['pdf_urls']=pdfs;r['landing_bytes']=len(b);r['landing_sha256']=hashlib.sha256(b).hexdigest()
 main=d.xpath('//main') or [d];text='\n'.join(' '.join(x.split()) for x in main[0].xpath('.//text()') if x.strip());ident=hashlib.sha256(r['url'].encode()).hexdigest()[:16];(CACHE/(ident+'.html.txt')).write_text(text)
 r['cache_key']=ident;r['acquisition_status']='landing_only';r['fulltext_available']=False
 if pdfs:
  p=get(pdfs[0])
  if p and p[:4]==b'%PDF':
   f=CACHE/(ident+'.pdf');f.write_bytes(p);subprocess.run(['pdftotext','-layout',str(f),str(CACHE/(ident+'.txt'))],capture_output=True)
   t=(CACHE/(ident+'.txt')).read_text(errors='replace') if (CACHE/(ident+'.txt')).exists() else ''
   r.update(acquisition_status='pdf_acquired',bytes=len(p),sha256=hashlib.sha256(p).hexdigest(),pages=t.count('\f'),fulltext_available=bool(t.strip()))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rr=list(ex.map(acquire,records.values()))
# Byte-identical PDFs / mirrored language pages remain represented as alternates.
seen={};dedup=[]
for r in rr:
 h=r.get('sha256')
 if h and h in seen:seen[h]['alternate_urls'] += [r['url']]+r['alternate_urls'];continue
 dedup.append(r)
 if h:seen[h]=r
with (OUT/'inventory-publiceye.jsonl').open('w') as f:
 for r in dedup:f.write(json.dumps(r,ensure_ascii=False)+'\n')
with (OUT/'acquisition-publiceye.jsonl').open('w') as f:
 for r in logs:f.write(json.dumps(r,ensure_ascii=False)+'\n')
print('deduplicated',len(dedup),'pdf acquired',sum(r['acquisition_status']=='pdf_acquired' for r in dedup))
