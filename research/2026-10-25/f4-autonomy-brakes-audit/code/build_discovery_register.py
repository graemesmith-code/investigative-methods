#!/usr/bin/env python3
"""Publish search metadata, not third-party article bodies or signed URLs."""
import csv,hashlib,json,pathlib,re,urllib.parse
P=pathlib.Path(__file__).resolve().parents[1]
def safe_url(url):
 parts=urllib.parse.urlsplit(url);pairs=urllib.parse.parse_qsl(parts.query,keep_blank_values=True)
 signed=any(k.lower().startswith('x-amz-') or k.lower() in {'sig','signature','token','access_token','api_key'} for k,v in pairs)
 if signed:return urllib.parse.urlunsplit((parts.scheme,parts.netloc,parts.path,'','')),True
 pairs=[(k,v) for k,v in pairs if not k.lower().startswith('utm_') and k.lower() not in {'fbclid','gclid'}]
 return urllib.parse.urlunsplit((parts.scheme,parts.netloc,parts.path,urllib.parse.urlencode(pairs),'')),False
if __name__=='__main__':
 reviewed=set()
 for f in P.rglob('*.md'):
  for url in re.findall(r'https?://[^\s)>]+',f.read_text()):reviewed.add(safe_url(url)[0])
 rows=[];queries=0
 for line in pathlib.Path('/workspace/scratch/f4-private/exa-results.jsonl').read_text().splitlines():
  x=json.loads(line);queries+=1
  for r in x['results']:
   original=r.get('url') or '';url,redacted=safe_url(original)
   rows.append({'query_sequence':x['sequence'],'query':x['query'],'title':r.get('title'),'url':url,'signed_query_removed':redacted,'original_url_sha256':hashlib.sha256(original.encode()).hexdigest(),'publishedDate':r.get('publishedDate'),'review_status':'cited_in_authored_review; inspect stated access depth' if url in reviewed else 'discovered_search_metadata_only'})
 (P/'audit/exa-discovery-register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 with (P/'audit/exa-query-cost-log.csv').open() as f:ledger=list(csv.DictReader(f))
 stats={'queried_responses':queries,'ledger_requests':len(ledger),'returned_result_appearances':len(rows),'unique_safe_urls':len(set(x['url'] for x in rows)),'result_appearances_cited_in_review':sum(x['review_status'].startswith('cited') for x in rows),'signed_urls_sanitized':sum(x['signed_query_removed'] for x in rows),'limit':'Metadata review/discovery is not full-body inspection. Full document access depths, failures and hashes are recorded in source receipts and evidence notes.'}
 (P/'audit/exa-discovery-accounting.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats,indent=2))
