#!/usr/bin/env python3
# PPLAAF custom post types, not news releases. Keep translations separate for discovery then canonicalize via English preferred.
import urllib.request,json,pathlib,hashlib,re,html
BASE=pathlib.Path(__file__).parent;CACHE=pathlib.Path('/tmp/ngo-integrity-cache'); LOG=[];rows=[]
def get(u):
 b=urllib.request.urlopen(u,timeout=35).read();h=hashlib.sha256(b).hexdigest();(CACHE/h).write_bytes(b);LOG.append(dict(url=u,status='acquired',bytes=len(b),sha256=h));return b
for typ in ['cases','country']:
 for page in range(1,5):
  u=f'https://www.pplaaf.org/wp-json/wp/v2/{typ}?per_page=100&page={page}'
  try:posts=json.loads(get(u))
  except Exception as e:LOG.append(dict(url=u,status='failed',error=str(e)));break
  for post in posts:
   b=post['content']['rendered'].encode(); title=html.unescape(re.sub('<[^>]+>',' ',post['title']['rendered'])).strip();r=dict(org='PPLAAF',title=title,date=post['date'][:10],url=post['link'],source_type='investigation' if typ=='cases' else 'country_legal_report',type='investigation' if typ=='cases' else 'country_legal_report',acquisition_status='fulltext_acquired',fulltext_screened=False,deeply_read=False,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pages=None,screening_rationale='Original case/country text acquired via official free REST; human contextual reading pending.',opportunity_ids=[],wordpress_id=post['id'])
   (CACHE/r['sha256']).write_bytes(b);r['original_published_date_confidence']='CMS date; legacy site migration may have changed original dates.';rows.append(r)
  if len(posts)<100:break
(BASE/'pplaaf-raw.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
# English and English-only cases/country pages. French originals retained if no English counterpart matching WP hreflang.
keep=[r for r in rows if '/fr/' not in r['url'] and '2017-01-01'<=r['date']<='2026-10-13']
(BASE/'pplaaf-inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in keep))
(BASE/'pplaaf-acquisition.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in LOG))
print('raw',len(rows),'eligible English',len(keep));print('\n'.join(r['title']+' '+r['url'] for r in keep))
