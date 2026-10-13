#!/usr/bin/env python3
"""Official catalogue census. Downloads cached outside repository; no disabled TLS checks."""
import urllib.request,urllib.parse,re,json,hashlib,pathlib,concurrent.futures,html,subprocess
BASE=pathlib.Path(__file__).parent; CACHE=pathlib.Path('/tmp/ngo-integrity-cache');CACHE.mkdir(exist_ok=True)
LOG=[]
def get(u):
 p=CACHE/hashlib.sha256(u.encode()).hexdigest()
 if p.exists():return p.read_bytes()
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Research source census (public pages)'}),timeout=35) as r:b=r.read()
  p.write_bytes(b);LOG.append({'url':u,'status':'acquired','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});return b
 except Exception as e:LOG.append({'url':u,'status':'failed','error':str(e)});return b''
def text(b):
 s=b.decode(errors='replace');s=re.sub(r'<(script|style)\b.*?</\1>','',s,flags=re.S|re.I);return html.unescape(re.sub('<[^>]+>',' ',s))
def record(org,title,date,url,typ='report',status='enumerated',b=None):
 return dict(org=org,title=html.unescape(title.strip()),date=date,url=url,source_type=typ,type=typ,acquisition_status=status,fulltext_screened=False,deeply_read=False,bytes=len(b) if b else None,sha256=hashlib.sha256(b).hexdigest() if b else None,pages=None,screening_rationale='Enumerated from official catalogue; not yet substantively read.',opportunity_ids=[])
if __name__ == "__main__":
    records={};raw=[]
    # All English global-secretariat publication catalogue pages. Spotlight duplicates canonicalized.
    def ti_catalog(n):
     u='https://www.transparency.org/en/publications'+('/p'+str(n) if n>1 else '')
     b=get(u).decode(errors='replace');out=[]
     for a in re.findall(r'<article\b.*?</article>',b,re.S):
      urls=re.findall(r'href="(https://www.transparency.org/en/publications/[^"?#]+)"',a)
      d=re.search(r'<time datetime="([^" ]+)',a);t=re.search(r'aria-label="([^"]+)"',a)
      if urls and d and t:out.append(record('Transparency International',t[1],d[1],urls[0]))
     return out
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
     for rows in ex.map(ti_catalog,range(1,20)):
      for r in rows:
       raw.append(r)
       if '2016-10-13'<=r['date']<='2026-10-13':records[r['url']]=r
    # PPLAAF WordPress REST preserves original publication dates and categories. Posts include news,
    # which remains discovery-only unless classified as substantial investigation.
    u='https://www.pplaaf.org/wp-json/wp/v2/categories?per_page=100';cats=json.loads(get(u) or b'[]');(BASE/'pplaaf-categories.json').write_text(json.dumps(cats,indent=2))
    catmap={r['id']:r['name'] for r in cats}
    for pg in range(1,8):
     b=get(f'https://www.pplaaf.org/wp-json/wp/v2/posts?per_page=100&page={pg}')
     try:rows=json.loads(b)
     except Exception:break
     if not isinstance(rows,list):break
     for row in rows:
      r=record('PPLAAF',text(row['title']['rendered'].encode()),row['date'][:10],row['link'],'investigation',b=row['content']['rendered'].encode(),status='fulltext_acquired')
      r['categories']=[catmap.get(x,str(x)) for x in row.get('categories',[])];raw.append(r)
      # Category Cases/Investigations is explicit; country legislation reports added separately.
      if any(re.search('investig|case|révél|enqu',c,re.I) for c in r['categories']) and '/fr/' not in r['url'] and '2017-01-01'<=r['date']<='2026-10-13':records[r['url']]=r
     if len(rows)<100:break
    (BASE/'inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records.values()))
    (BASE/'raw-discovery.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in raw))
    (BASE/'acquisition-log.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in LOG))
    print('records',len(records),'raw',len(raw),'orgs', {o:sum(r['org']==o for r in records.values()) for o in set(r['org'] for r in records.values())})
