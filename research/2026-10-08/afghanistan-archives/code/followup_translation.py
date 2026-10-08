"""Bounded French counterpart discovery/download; no inference API."""
import urllib.request,urllib.parse,hashlib,json,time,subprocess,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));from pilot import Links
R=Path(__file__).resolve().parents[1]/'followup'
log=json.loads((R/'results/access.json').read_text())
def fetch(u,n):
 time.sleep(1.2)
 row={'url':u,'retrieved_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'Referer':'https://publications.gc.ca/site/archivee-archived.html?url='+urllib.parse.quote(u,safe='')}),timeout=30) as r:
   b=r.read(12*1024**2+1);assert len(b)<=12*1024**2;row.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  (R/'sources'/n).write_bytes(b);return b
 except Exception as e:row['error']=str(e);raise
 finally:log.append(row);(R/'results/access.json').write_text(json.dumps(log,indent=2))
u='https://publications.gc.ca/site/eng/9.502002/publication.html'
p=Links();p.feed(fetch(u,'french-catalogue.html').decode())
urls=sorted(set(urllib.parse.urljoin(u,x) for x in p.links if re.search('CP12-2-14-2012.*pdf$',x)))
assert len(urls)==1,urls
b=fetch(urls[0],'CP12-2-14-2012-fra.pdf');assert b.startswith(b'%PDF')
pages=subprocess.check_output(['pdftotext','-layout',str(R/'sources/CP12-2-14-2012-fra.pdf'),'-'],text=True).split('\f')
if not pages[-1].strip():pages.pop()
with (R/'results/french-pages.jsonl').open('w') as f:
 for i,t in enumerate(pages,1):f.write(json.dumps(dict(pdf_page=i,citation=urls[0]+'#page='+str(i),text=t),ensure_ascii=False)+'\n')
print('French pages',len(pages))
for i,t in enumerate(pages,1):
 if re.search(r'30\s?000|17\s?200|20\s?000',t):
  print('PAGE',i)
  for m in re.finditer(r'30\s?000|17\s?200|20\s?000',t):print(repr(t[max(0,m.start()-100):m.end()+250]))
