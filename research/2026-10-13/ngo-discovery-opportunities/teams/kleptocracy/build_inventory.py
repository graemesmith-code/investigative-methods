#!/usr/bin/env python3
"""Parse official browser-rendered snapshots stored ONLY in /tmp.
These hashes/bytes describe rendered responses, not original PDF/HTML bytes.
Reacquisition: use catalog-discovery.json references or official source URLs with
an authorized browser; shell denials are never bypassed. No copyrighted cache
is copied into the repository. This script does not label machine retrieval reading.
"""
import re,json,pathlib,hashlib,datetime,collections
ROOT=pathlib.Path(__file__).resolve().parent
sources=[]
for org,name in [('The Sentry','sentry'),('OCCRP','occrp'),('C4ADS','c4')]:
 text=pathlib.Path('/tmp/kleptocracy-'+name+'-browser.txt').read_text()
 for part in text.split('--------------------------------------------------------------------------------'):
  h=re.search(r'^([^\n]*)\((https?://[^)]+)\)\n',part,re.M)
  if not h:continue
  title,url=h.groups(); title=re.sub(r'\s*(?: - (?:C4ADS|The Sentry)| \| OCCRP)$','',title.strip()).strip()
  if not title:continue
  d=re.search(r'L\d+: ([A-Z][a-z]+ \d{1,2}, \d{4})',part)
  date=None
  if d:
   for fmt in ['%B %d, %Y','%b %d, %Y']:
    try: date=datetime.datetime.strptime(d[1],fmt).date().isoformat();break
    except ValueError:pass
  body=bool(re.search(r'L\d+(?:@P[^:]+)?:',part))
  sources.append(dict(org=org,title=title,date=date,url=url,type='investigation' if org=='OCCRP' else 'report_landing_page',acquisition_status='browser_batch_excerpt_attribution_unverified' if body else 'browser_metadata_only',fulltext_screened=False,deeply_read=False,bytes=len(part.encode()) if body else None,sha256=hashlib.sha256(part.encode()).hexdigest() if body else None,pages=None,hash_scope='browser_batch_segment_unverified' if body else None,original_bytes=None,fulltext_acquired=False,screening_rationale='Catalog/sample discovery only; not counted as contextual reading.',opportunity_ids=[],eligibility='date_verified_in_window' if date and '2016-10-13'<=date<='2026-10-13' else 'publication_date_unverified',acquisition_date='2026-10-13'))
# Recover report publication dates from sampled official OCCRP catalogs.
catalog=json.loads(ROOT.joinpath('occrp-catalog-discovery.json').read_text())
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
for r in sources:
 if r['org']!='OCCRP':continue
 matches=[c for c in catalog if norm(c['title'])==norm(r['title'])]
 if matches and matches[0]['date']:
  r['date']=datetime.datetime.strptime(matches[0]['date'],'%b %d, %Y').date().isoformat()
  r['date_source']='official sampled catalog'
  r['eligibility']='date_verified_in_window' if '2016-10-13'<=r['date']<='2026-10-13' else 'outside_window'
# Stable URL deduplication; choose richest rendering, not duplicate mirrors.
by={}
for r in sources:
 if r['url'] not in by or (r['bytes'] or 0)>(by[r['url']]['bytes'] or 0):by[r['url']]=r
rows=list(by.values())
# Eight report translations map to their original and are not independent works.
translation_pairs={'architectes-de-terreur':'architects-of-terror','trafic-dinfluence':'backchannel','detournement-du-systeme':'gaming-the-system','un-empire-detourne':'embezzled-empire','culture-de-la-violence':'cultivating-atrocities','dans-le-flou-en-rdc':'fingerprints-and-money-trails','lart-et-lartifice':'artful-dodgers','etat-de-predation':'state-of-prey','le-regne-de-la-terreur-un-business-florissant-en-republique-centrafricaine':'fear-inc'}
for r in rows:
 slug=r['url'].rstrip('/').split('/')[-1]
 if r['org']=='The Sentry' and slug in translation_pairs:
  r['duplicate_of']='https://thesentry.org/reports/'+translation_pairs[slug]+'/'
  r['screening_rationale']='Translation mirror; metadata retained, excluded from independent-work count.'
# Contextual reading declarations only for passages actually examined by researcher.
notes={
 'https://c4ads.org/reports/covert-compute/':('K-01','Methodology/limitations and appendix context examined via 36-page PDF; underlying procurement original endpoints failed; park.'),
 'https://c4ads.org/reports/side-effects/':('K-02','Executive summary plus correction read; supply-chain registration is not proof of actual sourcing or forced labor on a batch.'),
 'https://c4ads.org/reports/keeping-the-lights-on/':('K-03','Executive summary context read; AIS encounter and insurance listing do not prove sanction-prohibited payment or landing.'),
 'https://thesentry.org/reports/fronts-fakes-and-facades/':('K-04','Summary, public source documents, annex and endnote context read; original invoice comparison depends on leaked documents and firm-level customs.'),
 'https://thesentry.org/reports/enablers-violent-kleptocracies/':('K-05','Briefing and bank case context read; onward financial flows require unavailable bank records.'),
 'https://thesentry.org/reports/safe-harbor-no-more/':('K-06','Briefing overview context read; no stable free property transaction provenance tested.'),
}
# Add contextual rendered snapshots when batch response omitted the URL.
for url,(oid,note) in notes.items():
 if not any(r['url']==url for r in rows):
  text=pathlib.Path('/tmp/kleptocracy-deep-browser.txt').read_text()
  part=next((p for p in text.split('--------------------------------------------------------------------------------') if '('+url+')' in p),'')
  h=re.search(r'^([^\n]*)\((https?://[^)]+)\)\n',part,re.M)
  rows.append(dict(org='The Sentry',title=h[1].strip() if h else url,date='2023-07' if oid=='K-04' else None,url=url,type='report_landing_page',acquisition_status='browser_rendered_excerpt',fulltext_screened=False,deeply_read=False,bytes=len(part.encode()),sha256=hashlib.sha256(part.encode()).hexdigest(),pages=None,hash_scope='browser_rendered_excerpt',original_bytes=None,fulltext_acquired=False,eligibility='date_verified_in_window' if oid=='K-04' else 'publication_date_unverified',opportunity_ids=[],screening_rationale=note,acquisition_date='2026-10-13'))
 for r in rows:
  if r['url']==url:
   text=pathlib.Path('/tmp/kleptocracy-deep-browser.txt').read_text()
   parts=[p for p in text.split('--------------------------------------------------------------------------------') if '('+url+')' in p and re.search(r'L\d+:',p)]
   part=max(parts,key=len) if parts else ''
   r.update(screening_rationale=note,opportunity_ids=[oid],abstract_context_read=True,acquisition_status='browser_context_verified_excerpt',bytes=len(part.encode()) if part else None,sha256=hashlib.sha256(part.encode()).hexdigest() if part else None,hash_scope='browser_rendered_excerpt')
# Independently opened/context-read OCCRP methodological project page.
ctx=pathlib.Path('/tmp/kleptocracy-occrp-context.txt').read_text()
rows.append(dict(org='OCCRP',title='Beneficial Ownership Data is Critical in the Fight Against Corruption',date='2022-11-30',url='https://www.occrp.org/en/project/beneficial-ownership-data-is-critical-in-the-fight-against-corruption',type='methodological_project',acquisition_status='browser_context_verified_excerpt',fulltext_screened=True,deeply_read=True,bytes=len(ctx.encode()),sha256=hashlib.sha256(ctx.encode()).hexdigest(),pages=None,hash_scope='browser_rendered_excerpt',original_bytes=None,fulltext_acquired=False,screening_rationale='Introduction and linked-case context read: access withdrawals are not an AI-solvable processing bottleneck. No presently accessible registry comparison sample checked.',opportunity_ids=['K-08'],eligibility='date_verified_in_window',acquisition_date='2026-10-13'))
# Original PDF contextual reading is counted separately from full-document acquisition.
pdfs=[('C4ADS','Covert Compute','2026-09-09','https://c4ads.org/wp-content/uploads/2026/09/Covert-Compute-C4ADS.pdf',36,'K-01','Methodology pp.7-8; acquisition pp.11-14; appendices pp.25-31 and endnotes pp.32-35 context read.'),('The Sentry','Fronts, Fakes, and Façades','2023-07','https://thesentry.org/wp-content/uploads/2023/07/FrontsFakesFacades_TheSentry_OpenSecrets_July2023.pdf',73,'K-04','Selected annex pp.61-63 and endnotes pp.63-65 context read; incomplete full report.'),('The Sentry','Constructing Corruption','2022-09','https://thesentry.org/wp-content/uploads/2022/09/ConstructingCorruption_TheSentry_Sept2022.pdf',17,'K-05','Bank profile and cases pp.2-5 contextual read; incomplete full report.')]
for org,title,date,url,pages,oid,note in pdfs:
 rows.append(dict(org=org,title=title,date=date,date_precision='day' if len(date)==10 else 'month',url=url,type='report_pdf',acquisition_status='browser_partial_fulltext',fulltext_screened=True,deeply_read=True,bytes=None,sha256=None,pages=pages,hash_scope=None,original_bytes=None,fulltext_acquired=False,screening_rationale=note,opportunity_ids=[oid],eligibility='date_verified_in_window',canonical_report_url=next((k for k,v in notes.items() if v[0]==oid),None),acquisition_date='2026-10-13'))
# PDFs share canonical reports and are acquisition versions, not extra corpus works.
ROOT.joinpath('inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
counts={}
for org in ['OCCRP','The Sentry','C4ADS']:
 rr=[r for r in rows if r['org']==org]
 counts[org]={'unique_source_records':len(rr),'canonical_works_discovered':sum(r['type']!='report_pdf' and not r.get('duplicate_of') for r in rr),'translation_mirrors':sum(bool(r.get('duplicate_of')) for r in rr),'unique_report_landing_pages':sum(r['type']!='report_pdf' for r in rr),'date_verified_in_window':sum(r['eligibility']=='date_verified_in_window' for r in rr),'rendered_excerpt_acquired':sum(r['acquisition_status'] in ['browser_context_verified_excerpt','browser_partial_fulltext'] for r in rr),'original_fulltext_acquired':0,'fulltext_passage_screened':sum(r['fulltext_screened'] for r in rr),'deeply_read_selected_sections':sum(r['deeply_read'] for r in rr),'retained_finalists':0}
ROOT.joinpath('counts.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
