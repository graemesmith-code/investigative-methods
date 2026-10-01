"""Bounded, unauthenticated public-source capture. Redirects refused."""
import hashlib,html,json,pathlib,re,subprocess,shutil,urllib.parse,urllib.request
from html.parser import HTMLParser
from pipeline import OUT,NoRedirect,GuardError,now,write
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  elif t in ['p','div','br','h1','h2','h3','li','tr']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def fetch(url):
 u=urllib.parse.urlsplit(url)
 if u.scheme!='https' or u.username or u.password or u.port not in [None,443] or not (u.hostname.endswith('.canada.ca') or u.hostname in ['canada.ca','sencanada.ca','www.ourcommons.ca','www.noscommunes.ca','www.international.gc.ca','international.gc.ca','www.pm.gc.ca','www.priv.gc.ca','nsicop-cpsnr.ca','nsira-ossnr.gc.ca','www.thecanadareport.ca','thecanadareport.ca','storage.ghost.io']):raise GuardError('Unapproved public host')
 folder=OUT/'public-sources';folder.mkdir(exist_ok=True);key=hashlib.sha256(url.encode()).hexdigest();meta=folder/(key+'.json')
 if meta.exists():return json.loads(meta.read_text())
 with urllib.request.build_opener(NoRedirect).open(urllib.request.Request(url,headers={'User-Agent':'ATI-public-record-research/1.0'}),timeout=30) as response:
  raw=response.read(8_000_001);media=response.headers.get_content_type()
  if len(raw)>8_000_000:raise GuardError('Public source too large')
 rawpath=folder/(key+'.raw');rawpath.write_bytes(raw)
 if media=='application/pdf' or raw.startswith(b'%PDF'):
  if not shutil.which('pdftotext'):raise GuardError('PDF text tool unavailable; raw saved')
  r=subprocess.run(['pdftotext','-layout',str(rawpath),'-'],capture_output=True,timeout=30,check=True);text=r.stdout.decode('utf-8','replace')
 elif 'html' in media:
  parser=Text();parser.feed(raw.decode('utf-8','replace'));text='\n'.join(x.strip() for x in ''.join(parser.parts).splitlines() if x.strip())
 else:text=raw.decode('utf-8','replace')
 record={'url':url,'retrieved_utc':now(),'sha256':hashlib.sha256(raw).hexdigest(),'media_type':media,'raw_file':rawpath.name,'text':text};write(meta,record);return record
if __name__=='__main__':
 import sys
 for url in sys.argv[1:]:
  try:r=fetch(url);print(json.dumps({'url':url,'characters':len(r['text']),'sha256':r['sha256']}))
  except Exception as e:print(json.dumps({'url':url,'error':type(e).__name__}))
