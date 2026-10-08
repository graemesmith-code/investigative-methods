#!/usr/bin/env python3
"""Bounded public-publication pilot. Stdlib + Poppler; no model/API credentials."""
import argparse, hashlib, html, json, re, subprocess, time, urllib.request, urllib.parse, urllib.robotparser
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':
   d=dict(attrs)
   if 'href' in d:self.links.append(d['href'])
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--download',action='store_true');args=ap.parse_args()
 logpath=ROOT/'results/download-log.json';log=json.loads(logpath.read_text()) if logpath.exists() else [];count=0;total=0;robots={}
 def fetch(url,name):
  nonlocal count,total
  p=ROOT/'sources'/name
  if p.exists():return p.read_bytes()
  if not args.download:raise RuntimeError('Cache missing; explicit --download required')
  if count>=20:raise RuntimeError('20-request checkpoint reached')
  if total>=60*1024**2:raise RuntimeError('60 MiB checkpoint reached')
  host=urllib.parse.urlsplit(url).netloc
  if host!='publications.gc.ca':raise RuntimeError('Host outside allowlist')
  if host not in robots:
   rp=urllib.robotparser.RobotFileParser();rp.parse((ROOT/'sources/pub-robots.html').read_text().splitlines());robots[host]=rp
  if not robots[host].can_fetch('*',url):raise RuntimeError('robots disallow')
  time.sleep(1.2);count+=1
  row={'url':url,'retrieved_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'path':str(p.relative_to(ROOT))}
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AfghanistanArchivesResearchPilot/1.0 (bounded public research)', 'Referer':'https://publications.gc.ca/site/archivee-archived.html?url='+urllib.parse.quote(url,safe='')}),timeout=40) as r:
    b=r.read(12*1024**2+1);row.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
   if len(b)>12*1024**2:raise RuntimeError('12 MiB per-file limit')
   if total+len(b)>60*1024**2:raise RuntimeError('Total byte limit')
   total+=len(b);p.write_bytes(b);row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  except Exception as e:
   row['error']=str(e);raise
  finally:log.append(row);write('results/download-log.json',log)
  return b
 index='https://publications.gc.ca/site/eng/9.505603/publication.html'
 b=fetch(index,'quarterly-index.html');p=Links();p.feed(b.decode())
 urls=sorted(set(urllib.parse.urljoin(index,x) for x in p.links if re.search(r'(CP12-2-|CP22-87-).*\.pdf$',x,re.I)))
 evindex='https://publications.gc.ca/site/eng/9.809780/publication.html'
 p=Links();p.feed(fetch(evindex,'evaluation-index.html').decode())
 ev=sorted(set(urllib.parse.urljoin(evindex,x) for x in p.links if 'FR5-95-2015-eng.pdf' in x))
 assert len(urls)==14,(len(urls),urls)
 assert len(ev)==1,ev
 selection=[{'url':u,'discovered_on':index,'family':'parliamentary-report'} for u in urls]+[{'url':ev[0],'discovered_on':evindex,'family':'retrospective-evaluation'}]
 write('results/selection.json',selection)
 manifest=[];pages=[];seen={}
 for item in selection:
  u=item['url'];name=u.rsplit('/',1)[-1];b=fetch(u,name)
  assert b.startswith(b'%PDF'),name
  sha=hashlib.sha256(b).hexdigest();f=ROOT/'sources'/name
  info=subprocess.check_output(['pdfinfo',str(f)],text=True)
  n=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
  txt=subprocess.check_output(['pdftotext','-layout',str(f),'-'],text=True)
  split=txt.split('\f');split=split[:-1] if split[-1].strip()=='' else split
  assert len(split)==n,(name,n,len(split))
  row=dict(item,id=name[:-4],sha256=sha,bytes=len(b),pages=n,duplicate_of=seen.get(sha),creation_date=None,publication_date='2015-03' if item['family']=='retrospective-evaluation' else None,release_date=None,declassification_date=None,first_online_date=None)
  seen.setdefault(sha,name);manifest.append(row)
  for i,t in enumerate(split,1):
   pages.append({'document':name[:-4],'pdf_page':i,'citation':u+'#page='+str(i),'characters':len(t.strip()),'ocr_needed_candidate':len(t.strip())<80,'ocr_performed':False,'extraction':'pdftotext -layout','text':t})
 write('results/manifest.json',manifest)
 with (ROOT/'results/pages.jsonl').open('w') as f:
  for x in pages:f.write(json.dumps(x,ensure_ascii=False)+'\n')
 terms=['Dahla','school','sustainab','benchmark','hectare','monitor','baseline','polio']
 hits=[{'term':term,**{k:p[k] for k in ['document','pdf_page','citation']}} for p in pages for term in terms if term.lower() in p['text'].lower()]
 write('results/term-index.json',hits)
 summary={'documents':len(manifest),'pages':len(pages),'bytes':sum(x['bytes'] for x in manifest),'duplicate_files':sum(x['duplicate_of'] is not None for x in manifest),'low_text_pages':[{k:p[k] for k in ['document','pdf_page','characters']} for p in pages if p['ocr_needed_candidate']],'characters':sum(len(x['text']) for x in pages),'model_calls':0,'paid_api_cost_usd':0,'network_requests_this_run':count}
 write('results/coverage.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
