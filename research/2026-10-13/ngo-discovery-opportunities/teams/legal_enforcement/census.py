"""Public catalogs only; copyright content remains in /tmp. No TLS overrides."""
import urllib.request,urllib.parse,lxml.html,lxml.etree as E,json,hashlib,concurrent.futures,pathlib,re,datetime
OUT=pathlib.Path(__file__).parent;CACHE=pathlib.Path('/tmp/legal-enforcement');CACHE.mkdir(exist_ok=True)
def get(u):
 b=urllib.request.urlopen(u,timeout=35).read();CACHE.joinpath(hashlib.sha256(u.encode()).hexdigest()+'.bin').write_bytes(b);return b
def base(org,title,date,url,typ):
 return dict(org=org,title=title,date=date,url=url,type=typ,acquisition_status='catalog_only',fulltext_screened=False,deeply_read=False,bytes=None,sha256=None,pages=None,screening_rationale='Catalog metadata only; not counted as contextual reading.',opportunity_ids=[])
def fetchbasel(u):
 try:
  b=get(u);d=lxml.html.fromstring(b);title=' '.join(d.xpath('//h1//text()'));t=' '.join(d.xpath('//main//text()'));date=re.search(r'\d{1,2} [A-Z][a-z]{2} 20\d\d',t)
  ds=date.group() if date else None
  if ds and datetime.datetime.strptime(ds,'%d %b %Y').date()<datetime.date(2016,10,13): return None
  r=base('Basel Institute on Governance',title,ds,u,'publication');r.update(acquisition_status='html_acquired',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),download_urls=[urllib.parse.urljoin(u,a) for a in d.xpath('//a/@href') if '/assets/' in a or '.pdf' in a],date_verified=bool(ds));return r
 except Exception as e: return base('Basel Institute on Governance',u.rsplit('/',1)[-1],None,u,'publication')|dict(acquisition_status=str(e))
def main():
 us=E.fromstring(get('https://baselgovernance.org/sitemap.xml')).xpath('//*[local-name()="loc"]/text()');raw=sorted(set(u for u in us if '/publications/' in u));OUT.joinpath('basel-sitemap-discovery.json').write_text(json.dumps(raw,indent=2))
 # Current canonical path, legacy mirrored path deduplicated by slug.
 urls=sorted(set('https://baselgovernance.org/resources/publications/'+u.rstrip('/').rsplit('/',1)[-1] for u in raw))
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
  for r in ex.map(fetchbasel,urls):
   if r: rows.append(r)
 print('basel',len(raw),len(urls),len(rows),flush=True)
 for cat in [901,2810]:
  u=f'https://www.asso-sherpa.org/wp-json/wp/v2/posts?categories={cat}&per_page=100&after=2016-10-13T00:00:00&before=2026-10-14T00:00:00'
  try:
   b=get(u);ps=json.loads(b);OUT.joinpath(f'sherpa-discovery-{cat}.json').write_text(json.dumps([dict(id=p['id'],url=p['link'],date=p['date'],title=p['title']['rendered'],categories=p['categories']) for p in ps],ensure_ascii=False,indent=2))
   for p in ps:
    content=p['content']['rendered'];r=base('Sherpa',lxml.html.fromstring(p['title']['rendered']).text_content(),p['date'][:10],p['link'],'research/publication');r.update(acquisition_status='full_html_acquired',bytes=len(content.encode()),sha256=hashlib.sha256(content.encode()).hexdigest(),download_urls=re.findall(r'href=[\"\']([^\"\']+)',content));rows.append(r);CACHE.joinpath(hashlib.sha256(p['link'].encode()).hexdigest()+'.html').write_text(content)
  except Exception as e: print(u,e,flush=True)
 seen=set();rows=[r for r in rows if not(r['url'] in seen or seen.add(r['url']))];OUT.joinpath('inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));print('rows',len(rows),flush=True)
if __name__=='__main__':main()
