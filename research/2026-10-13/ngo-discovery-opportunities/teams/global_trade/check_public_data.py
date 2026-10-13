#!/usr/bin/env python3
"""Bounded access checks; no credentials, paid APIs, retries or TLS bypass.
Checks demonstrate access only. They do not establish a contradiction or wrongdoing.
"""
import urllib.request,urllib.parse,json,hashlib,zipfile,io,pathlib
from lxml import html
ROOT=pathlib.Path(__file__).parent;cache=pathlib.Path('/tmp/ngo-global-trade');cache.mkdir(exist_ok=True)
checks=[]
def get(url,limit=10_000_000):
 try:
  with urllib.request.urlopen(url,timeout=45) as r:
   b=r.read(limit+1)
   if len(b)>limit: raise ValueError('Bounded download cap exceeded')
   record={'url':url,'status':r.status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'content_type':r.headers.get('Content-Type'),'purpose':'Access-only bounded sample; no investigation finding'}
   checks.append(record);(cache/(hashlib.sha256(url.encode()).hexdigest()[:16]+'.data')).write_bytes(b);return b,record
 except Exception as e:checks.append({'url':url,'status':'failed','error':str(e)});return None,None
u='https://download.companieshouse.gov.uk/en_pscdata.html';b,_=get(u)
if b:
 links=html.fromstring(b).xpath('//a[contains(@href,".zip")]/@href')
 if links:
  url=urllib.parse.urljoin(u,links[-1]);zipped,r=get(url)
  if zipped:
   z=zipfile.ZipFile(io.BytesIO(zipped));f=z.namelist()[0];record=json.loads(z.open(f).readline());r.update(zip_member=f,sample_parsed=True,sample_top_keys=list(record))
url='https://comtradeapi.un.org/public/v1/preview/C/A/HS?period=2022&reporterCode=604&cmdCode=260300&flowCode=X&partnerCode=156&partner2Code=0&customsCode=C00&motCode=0&maxRecords=5'
b,r=get(url)
if b:r['json_count']=json.loads(b).get('count')
# A previously denied Swiss endpoint is intentionally not retried.
(ROOT/'data-checks-rerun.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
