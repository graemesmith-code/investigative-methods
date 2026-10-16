#!/usr/bin/env python3
"""Free public DoD historical announcement collector; no credentials or scoring.
Run with Python 3.11+, requests and beautifulsoup4. See ../README.md.
"""
import argparse, csv, datetime as dt, fcntl, gzip, hashlib, json, os, re, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
FIELDS=['announcement_date','service_or_agency_section','contractor_name','raw_paragraph_verbatim','source_url','source_page_title']
START='2018-09-12'; END='2023-09-11'
# Source-observed section names also recognize mixed-case heading variants.
SECTION_NAMES={'SPECIAL OPERATIONS COMMAND', 'DARPA', 'DEFENSE FINANCE AND ACCOUNTING SERVICE', 'DEFENSE MICROELECTRONICS ACTIVITY', 'CONTRACTS', 'DEFENSE THREAT REDUCTION AGENCY', 'DEFENSE COMMISSARY AGENCY', 'MISSLE DEFENSE AGENCY', 'DEFENSE SECURITY SERVICE', 'WASHINGTON HEADQUARTERS SERVICE', 'DEFENSE INTELLIGENCE AGENCY', 'UNIFORMED SERVICES UNIVERSITY OF THE HEALTH SCIENCES', 'WASHINGTON HEADQUARTERS AGENCY', 'DEFENSE COUNTERINTELLIGENCE AND SECURITY AGENCY', 'DEPARTMENT OF DEFENSE EDUCATION ACTIVITY', 'AIR FORCE', 'DEFENSE LOGISTICS AGENCY', 'WASHINGTON HEADQUARTERS SERVICES', 'NAVY', 'DEFENSE FINANCE AND ACCOUNTING SERVICES', 'MISSILE DEFENSE AGENCY', 'DEFENSE HUMAN RESOURCES ACTIVITY', 'DEFENSE INFORMATION SYSTEM AGENCY', 'DEFENSE HEALTH AGENCY', 'DEFENSE COUNTERINTELLIGENCE SECURITY AGENCY', 'JOINT ARTIFICIAL INTELLIGENCE CENTER', 'SPACE DEVELOPMENT AGENCY', 'DEFENSE ADVANCED RESEARCH PROJECTS AGENCY', 'U.S. SPECIAL OPERATIONS COMMAND', 'U.S. TRANSPORTATION COMMAND', 'ARMY', 'DEFENSE INFORMATION SYSTEMS AGENCY', 'DEFENSE INFORMATIONS SYSTEMS AGENCY'}
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def write_csv(p,rows,fields):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def title_date(title):
 t=re.sub(r'^.*?Contracts?\s+(?:For|for)\s+','',title).split(' >')[0].strip().replace('.','')
 for fmt in ['%b %d, %Y','%B %d, %Y']:
  try:return dt.datetime.strptime(t.replace('Sept ','Sep '),fmt).date().isoformat()
  except ValueError:pass
 return ''
def inline_text(node):
 from bs4 import Comment
 if isinstance(node,Comment):return ''
 if not getattr(node,'name',None):return str(node)
 if node.name=='br':return '\ue000'
 return ''.join(inline_text(child) for child in node.children)
def split_breaks(text):
 # A blank line made of two BR elements is an older paragraph boundary.
 # One BR is a line break within the paragraph. Never split on punctuation.
 for part in re.split(r'\ue000[\s\ue000]*\ue000',text):
  if part.strip():yield part.replace('\ue000','\n')
def block_texts(node):
 # Older AFPIMS pages use DIV blocks and bare text separated by double BRs.
 blocktags=['p','div','h2','h3','h4','li','ul','ol','table','tr','td']
 if not node.find(blocktags):
  yield from split_breaks(inline_text(node))
  return
 pending=[]
 for child in node.children:
  if getattr(child,'name',None) in blocktags or (getattr(child,'name',None) and child.find(blocktags)):
   if pending:yield from split_breaks(''.join(pending));pending=[]
   yield from block_texts(child)
  else:pending.append(inline_text(child))
 if pending:yield from split_breaks(''.join(pending))
def parse(content,source):
 s=BeautifulSoup(content,'html.parser');title=s.title.get_text().strip() if s.title else ''
 h=s.select_one('h1');date=title_date(h.get_text(' ',strip=True) if h else title)
 body=s.select_one('div.body') or s.select_one('[itemprop="articleBody"]')
 if not date or not body:raise ValueError('Missing dated title or article body')
 records=[];notes=[];section='';blocks=[]
 # Preserve complete paragraph text, including NBSP, punctuation and corrections.
 for n,text in enumerate(t for t in block_texts(body) if t.strip()):
  clean=' '.join(text.split())
  if not clean:continue
  if len(clean)<150 and (clean.upper()==clean or clean.upper() in SECTION_NAMES) and re.search('[A-Z]',clean) and '$' not in clean:
   section=clean;blocks.append({'paragraph_index':n,'kind':'section','text':text});continue
  is_footnote=clean.startswith('*') and '$' not in clean
  is_record=not is_footnote and ('$' in clean or (len(clean)>100 and section) or (len(clean)>35 and re.search(r'\bcorrection\b',clean,re.I) is not None))
  blocks.append({'paragraph_index':n,'kind':'record' if is_record else 'note','text':text})
  if not is_record:notes.append({'paragraph_index':n,'text':text});continue
  # Deliberately blank: a location/name heuristic can silently misidentify joint awards.
  records.append(dict(zip(FIELDS,[date,section,'',text,source,title]),paragraph_index=n))
 if not records and not re.search(r'no contract awards to announce|no contracts to announce',body.get_text(),re.I):raise ValueError('No announcement paragraphs')
 if not records:blocks.append({'paragraph_index':0,'kind':'official_no_awards','text':body.get_text()})
 return date,title,records,blocks
class Collector:
 def __init__(self,workers=3,interval=0.8):
  self.workers=workers;self.interval=interval;self.pace=threading.Lock();self.last=0;self.loglock=threading.Lock()
 def request(self,url):
  with self.pace:
   delay=self.interval-(time.monotonic()-self.last)
   if delay>0:time.sleep(delay)
   self.last=time.monotonic()
  began=now();r=requests.get(url,timeout=(15,40),headers={'User-Agent':'Public-records historical research collector; 3 workers; public archive replay'})
  return r,began
 def collect_one(self,c):
  aid=c['article_id'];p=ROOT/'pages'/f'{aid}.json'
  if p.exists() and json.loads(p.read_text()).get('status')=='ok':return json.loads(p.read_text())
  u=f"https://web.archive.org/web/{c['capture_timestamp']}id_/{c['original_url']}"
  info={**c,'source_label':'Internet Archive Wayback replay of official DoD page','requested_retrieval_url':u,'attempt_started_at_utc':now(),'status':'failed'}
  try:
   r,began=self.request(u);info.update(retrieved_at_utc=began,http_status=r.status_code,retrieval_url=r.url,response_headers={k:v for k,v in r.headers.items() if k.lower() in ['memento-datetime','content-type','content-location','x-archive-orig-date','x-archive-src']})
   if r.status_code!=200:raise ValueError(f'HTTP {r.status_code}')
   content=r.content;digest=sha(content)
   (ROOT/'html'/f'{aid}.html.gz').write_bytes(gzip.compress(content,mtime=0))
   info.update(response_sha256=digest,archive_memento_datetime=r.headers.get('Memento-Datetime',''),response_bytes=len(content),html_file=f'html/{aid}.html.gz')
   date,title,rows,blocks=parse(content,c['original_url'])
   info.update(status='ok',announcement_date=date,source_page_title=title,records=rows,blocks=blocks,in_requested_period=START<=date<=END,parser_sha256=sha(Path(__file__).read_bytes()),parsed_at_utc=now())
  except Exception as e:info['error']=str(e)
  dump(p,info)
  with self.loglock:
   with (ROOT/'retrieval_attempts.jsonl').open('a') as f:f.write(json.dumps({k:v for k,v in info.items() if k not in ['records','blocks']})+'\n')
  return info
 def run(self,limit=None):
  candidates=json.loads((ROOT/'discovery/candidates.json').read_text())
  if limit:candidates=candidates[:limit]
  print('Candidates',len(candidates),flush=True)
  with ThreadPoolExecutor(max_workers=self.workers) as ex:
   for n,f in enumerate(as_completed([ex.submit(self.collect_one,c) for c in candidates]),1):
    x=f.result()
    if n%20==0 or x['status']!='ok':print(now(),n,x['article_id'],x['status'],x.get('announcement_date'),x.get('error',''),flush=True)
  build()
def fetch_discovery():
 params={'url':'www.defense.gov/News/Contracts/Contract/Article/*','output':'json','filter':'statuscode:200','collapse':'urlkey','fl':'timestamp,original,digest,mimetype','limit':3000,'showResumeKey':'true'}
 stamp=now();r=requests.get('https://web.archive.org/cdx/search/cdx',params=params,timeout=60)
 # Preserve the original discovery response; refreshing writes a separate capture.
 name='cdx-refresh-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json'
 (ROOT/'discovery'/name).write_bytes(r.content)
 dump(ROOT/'discovery'/(name+'.provenance.json'),dict(requested_at_utc=stamp,request_url=r.request.url,retrieval_url=r.url,http_status=r.status_code,response_sha256=sha(r.content),source_label='Internet Archive CDX index',response_file=name))
 r.raise_for_status();print(name,flush=True)
def discover():
 # The saved CDX batch includes a resume key; article ID bounds are discovery
 # aids, not date authority. Parsed announcement titles determine inclusion.
 data=json.loads((ROOT/'discovery/cdx-contract-first3000.json').read_text())
 seen={}
 for row in data[1:]:
  if len(row)!=4:continue
  stamp,url,digest,mime=row;m=re.search(r'/Article/(\d+)(?:/|$)',url,re.I)
  if not m:continue
  aid=int(m[1])
  if not 1627000<=aid<=3523820:continue
  c=dict(article_id=str(aid),capture_timestamp=stamp,original_url=url,cdx_digest=digest,cdx_mimetype=mime,discovery_file='discovery/cdx-contract-first3000.json')
  # Prefer clean official URL over query/referral aliases.
  if aid not in seen or len(url)<len(seen[aid]['original_url']):seen[aid]=c
 dump(ROOT/'discovery/candidates.json',[seen[k] for k in sorted(seen)])
 print('Discovered',len(seen),flush=True)
def reparse():
 for p in sorted((ROOT/'pages').glob('*.json')):
  x=json.loads(p.read_text())
  if not x.get('html_file'):continue
  try:
   content=gzip.decompress((ROOT/x['html_file']).read_bytes())
   date,title,rows,blocks=parse(content,x['original_url'])
   x['archive_memento_datetime']=x.get('response_headers',{}).get('memento-datetime','')
   x.update(status='ok',announcement_date=date,source_page_title=title,records=rows,blocks=blocks,in_requested_period=START<=date<=END,parser_sha256=sha(Path(__file__).read_bytes()),parsed_at_utc=now())
   x.pop('error',None)
  except Exception as e:x.update(status='failed',error=str(e))
  dump(p,x)
 build()
def build():
 extra=['record_id','paragraph_index','source_label','retrieved_at_utc','retrieval_url','capture_timestamp','response_sha256','html_file','parser_sha256','parsed_at_utc','archive_memento_datetime']
 rows=[];pages=[];issues=[]
 for p in sorted((ROOT/'pages').glob('*.json')):
  x=json.loads(p.read_text());pages.append({k:v for k,v in x.items() if k not in ['records','blocks']})
  if x['status']!='ok' or not x.get('in_requested_period'):continue
  for r in x['records']:
   rid=sha((x['article_id']+'|'+str(r['paragraph_index'])+'|'+r['raw_paragraph_verbatim']).encode())
   rows.append({**r,'record_id':rid,**{k:x.get(k,'') for k in extra if k not in ['record_id','paragraph_index']}})
 rows.sort(key=lambda r:(r['announcement_date'],r['source_url'],r['paragraph_index']))
 write_csv(ROOT/'pentagon_contract_paragraphs_history.csv',rows,FIELDS+extra)
 dump(ROOT/'page_manifest.json',pages)
 candidates=json.loads((ROOT/'discovery/candidates.json').read_text());byid={p['article_id']:p for p in pages}
 write_csv(ROOT/'candidate_coverage.csv',[dict(article_id=c['article_id'],status=byid.get(c['article_id'],{}).get('status','not_attempted'),announcement_date=byid.get(c['article_id'],{}).get('announcement_date',''),error=byid.get(c['article_id'],{}).get('error',''),original_url=c['original_url']) for c in candidates],['article_id','status','announcement_date','error','original_url'])
 dates={x['announcement_date'] for x in pages if x['status']=='ok' and x.get('in_requested_period')};empty_dates=dates-{r['announcement_date'] for r in rows};day=dt.date.fromisoformat(START);end=dt.date.fromisoformat(END);coverage=[]
 while day<=end:
  d=day.isoformat();coverage.append(dict(date=d,weekday=day.strftime('%A'),status=('official_no_awards' if d in empty_dates else 'recovered') if d in dates else 'unresolved_no_recovered_page',pages=sum(p['status']=='ok' and p.get('announcement_date')==d for p in pages),paragraphs=sum(r['announcement_date']==d for r in rows)));day+=dt.timedelta(days=1)
 write_csv(ROOT/'daily_coverage.csv',coverage,['date','weekday','status','pages','paragraphs'])
 # Original corpus stays unchanged. Deduplicate the index, retaining all pointers.
 original=ROOT.parent/'raw/pentagon_contract_paragraphs_10000.csv';index={}
 for rel,data in [('../raw/pentagon_contract_paragraphs_10000.csv',list(csv.DictReader(original.open(newline='')))),('pentagon_contract_paragraphs_history.csv',rows)]:
  for n,r in enumerate(data,1):
   key=sha(json.dumps([r['announcement_date'],' '.join(r['service_or_agency_section'].split()),' '.join(r['raw_paragraph_verbatim'].split())],ensure_ascii=False).encode())
   entry=index.setdefault(key,dict(dedup_key=key,announcement_date=r['announcement_date'],service_or_agency_section=r['service_or_agency_section'],paragraph_sha256=sha(r['raw_paragraph_verbatim'].encode()),pointers=[]))
   entry['pointers'].append(dict(file=rel,data_row=n,source_url=r['source_url'],paragraph_sha256=sha(r['raw_paragraph_verbatim'].encode())))
 write_csv(ROOT/'combined_deduplicated_index.csv',[{**e,'pointers':json.dumps(e['pointers'],ensure_ascii=False)} for e in sorted(index.values(),key=lambda e:(e['announcement_date'],e['dedup_key']))],['dedup_key','announcement_date','service_or_agency_section','paragraph_sha256','pointers'])
 summary=dict(built_at_utc=now(),period=[START,END],candidate_pages=len(candidates),attempted_pages=len(pages),successful_pages=sum(x['status']=='ok' for x in pages),in_period_pages=sum(x['status']=='ok' and x.get('in_requested_period',False) for x in pages),paragraphs=len(rows),recovered_dates=len(dates),unresolved_weekdays=sum(c['status']=='unresolved_no_recovered_page' and c['weekday'] not in ['Saturday','Sunday'] for c in coverage),original_sha256=sha(original.read_bytes()),index_unique_records=len(index),status='partial; archive discovery and missing dates do not establish publication completeness')
 dump(ROOT/'summary.json',summary);print(json.dumps(summary),flush=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['fetch-discovery','discover','collect','reparse','build']);ap.add_argument('--limit',type=int);a=ap.parse_args()
 ROOT.mkdir(exist_ok=True)
 for d in ['pages','html','discovery']:(ROOT/d).mkdir(exist_ok=True)
 lock=(ROOT/'.collector.lock').open('a+')
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:raise SystemExit('Another historical collector owns this environment lock')
 lock.seek(0);lock.truncate();lock.write(f'{os.getpid()} {now()}\n');lock.flush()
 if a.action=='fetch-discovery':fetch_discovery()
 elif a.action=='discover':discover()
 elif a.action=='collect':Collector().run(a.limit)
 elif a.action=='reparse':reparse()
 else:build()
if __name__=='__main__':main()
