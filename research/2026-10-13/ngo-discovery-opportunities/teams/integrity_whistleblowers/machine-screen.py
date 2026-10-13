#!/usr/bin/env python3
"""Ordinary-code bottleneck index; no AI and no claims of human reading. Cache stays /tmp."""
import pathlib,json,re,hashlib,html,collections
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-integrity-cache')
terms=re.compile(r'(?i)\b(manual(?:ly)?|inaccessible|unavailable|fragment(?:ed|ation)|unstructured|machine.readable|(?:not|no longer) public(?:ly)?|data quality|data access|access barrier|missing data|lack of data|impossible|confidential|beneficial ownership|public procurement|qualification|rejection)\b')
rows=[]
for r in map(json.loads,(P/'inventory.jsonl').read_text().splitlines()):
 if r['acquisition_status']!='fulltext_acquired' or not r.get('sha256'):continue
 if r['org']=='Transparency International':
  f=C/(r['sha256']+'.txt')
  if not f.exists():continue
  t=f.read_text(errors='replace');kind='pdftotext-layout';url=r.get('fulltext_url',r['url'])
 elif r['org']=='PPLAAF':
  f=C/r['sha256']
  if not f.exists():continue
  t=f.read_text(errors='replace');t=re.sub(r'<(script|style)\b.*?</\1>','',t,flags=re.I|re.S);t=html.unescape(re.sub('<[^>]+>',' ',t));t=re.sub(r'\s+',' ',t);kind='html-tag-removal-whitespace-normalization';url=r['url']
 else:continue
 hits=[dict(keyword=m.group(0).lower(),character_offset=m.start(),pdf_page=t[:m.start()].count('\f')+1 if kind=='pdftotext-layout' else None) for m in terms.finditer(t)]
 rows.append(dict(org=r['org'],canonical_source_url=r['url'],acquired_fulltext_url=url,acquired_sha256=r['sha256'],text_sha256=hashlib.sha256(t.encode()).hexdigest(),character_count=len(t),extraction=kind,keyword_counts=dict(collections.Counter(x['keyword'] for x in hits)),keyword_hits=hits,machine_screened=True,human_contextual_screened=r['fulltext_screened'],deep_relevant_section_read=r['deeply_read'],interpretation='Keyword index locates passages only; no human reading or candidate judgment inferred.'))
(P/'machine-screen.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));print('machine_screened',len(rows),'by_org',dict(collections.Counter(r['org'] for r in rows)))
