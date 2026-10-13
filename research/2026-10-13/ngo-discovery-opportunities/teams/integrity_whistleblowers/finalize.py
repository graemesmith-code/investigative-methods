#!/usr/bin/env python3
"""Apply human reading ledger (not inferred from a download or keyword match)."""
import pathlib,json,collections
P=pathlib.Path(__file__).parent
rows=[json.loads(s) for s in (P/'inventory.jsonl').read_text().splitlines() if json.loads(s)['org']=='Transparency International' and 'www.transparency.org/en/publications/' in json.loads(s)['url']]
screen={7,16,17,20,23,28,32,53,63,81,96,104,112,130,181,198,213};deep={7,16,28}
for i,r in enumerate(rows):
 if i in screen:r.update(fulltext_screened=True,deeply_read=i in deep,screening_rationale='Human contextual screen of relevant report passages with surrounding paragraphs; no finalist: access, evidence, identity or novelty gap. Deep reading means relevant methodology/limitations and claim context examined, not every page read.')
 r['date_provenance']='Official publication catalogue time datetime';r['coverage_scope']='TI global-secretariat English catalogue; no exhaustive national-chapter coverage'
pp=[json.loads(s) for s in (P/'pplaaf-inventory.jsonl').read_text().splitlines()];keep=[]
for i,r in enumerate(pp):
 if i in {14,22}:continue # Congo Hold-up stub is not substantial; duplicate Banana Port page.
 if i in {0,1,2,3,5,6,10,12,16,17,18,19,20,21}:r.update(fulltext_screened=True,deeply_read=i==20,screening_rationale='Contextually screened original case passages. Excluded: decisive bank/ownership documents leaked/private; previously published case, weak identity or missing lawful-conduct baseline. No finalist.')
 r['date_provenance']='CMS original date, with legacy migration caveat; case text may describe earlier investigation and later update';keep.append(r)
rows+=keep
ant=[
('2026-05-25','Cabinet of Ministers Allows Construction Material Prices to Be Concealed in Procurement for the Reconstruction of War-Affected Regions','cabinet-of-ministers-allows-construction-material-prices-to-be-concealed-in-procurement-for-the-reconstruction-of-war-affected-regions/',True),
('2024-09-19','Parliament adopted the law on opening cost estimates in construction procurement','parliament-adopted-the-law-on-opening-cost-estimates-in-construction-procurement/',True),
('2024-03-04','Do the authorities “get profit” at construction sites during the war: the draft law No. 11057 may reveal prices hidden by officials','do-the-authorities-get-profit-at-construction-sites-during-the-war-the-draft-law-no-11057-may-reveal-prices-hidden-by-officials/',True),
('2024-09-10','The Cabinet of Ministers is proposing a new version of the law on public procurement: what are the risks?','the-cabinet-of-ministers-is-proposing-a-new-version-of-the-law-on-public-procurement-what-are-the-risks/',False),
('2025-06-30','We only buy from “our guys”: how Umerov created a “closed club” of weapons suppliers','we-only-buy-from-our-guys-how-umerov-created-a-closed-club-of-weapons-suppliers/',False),
('2018-02-01','Top Corrupt Officials: Verdicts in 2015-2017','top-corrupt-officials-verdicts-in-2015-2017/',True),
('2023-01-02','Anti-corruption frontline. Main events of 2022','anti-corruption-frontline-main-events-of-2022/',False)]
for date,title,slug,d in ant:
 rows.append(dict(org='AntAC',title=title,date=date,url='https://antac.org.ua/en/news/'+slug,type='substantial_case_analysis',source_type='substantial_case_analysis',acquisition_status='browser_fulltext_acquired',fulltext_screened=True,deeply_read=d,bytes=None,sha256=None,pages=None,screening_rationale='Official source browser text read contextually; local acquisition forbidden HTTP403. Procurement inconsistency test is design candidate only, no misconduct finding.',opportunity_ids=['IW-01'] if date=='2026-05-25' else [],date_provenance='Displayed official publication date;2026 article inferred year from explicitly stated June2026 commencement',coverage_scope='Purposive official-source sample; no decade-wide census because catalogue/direct HTTP access blocked'))
rows.append(dict(org='AntAC',title='9 облдержадміністрацій приховують ціни на будівництво фортифікацій на 12,7 млрд грн – «Наші гроші»',date='2024-05-30',url='https://antac.org.ua/news/9-oblderzhadministratsiy-prykhovuiut-tsiny-na-budivnytstvo-fortyfikatsiy-na-12-7-mlrd-hrn-nashi-hroshi/',type='substantial_case_analysis',source_type='substantial_case_analysis',acquisition_status='browser_fulltext_acquired',fulltext_screened=True,deeply_read=False,bytes=None,sha256=None,pages=None,screening_rationale='Ukrainian original context screen; procurement prices rely on materials definitions and access; no AI-created evidence.',opportunity_ids=[],date_provenance='Displayed official date',coverage_scope='Purposive official-source sample;not exhaustive'))
if (P/'prior_coverage.json').exists():
 for x in json.loads((P/'prior_coverage.json').read_text())[:3]:
  rows.append(dict(org='Transparency International',title=x['title'],date=x['date'],url=x['url'],source_type=x['source_type'],type=x['source_type'],acquisition_status='search_index_text_acquired' if x['date']=='2018-11-02' else 'browser_fulltext_acquired',fulltext_screened=x['date']!='2018-11-02',deeply_read=False,bytes=None,sha256=None,pages=None,screening_rationale=x['finding'],opportunity_ids=['IW-01'],coverage_scope='Purposive TIUkraine chapter sample,not exhaustive',date_provenance='Displayed official publication date'))
(P/'inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
stats=[]
for org in ['Transparency International','PPLAAF','AntAC']:
 a=[r for r in rows if r['org']==org];stats.append(dict(org=org,enumerated=len(a),acquired=sum(r['acquisition_status'] in ['fulltext_acquired','browser_fulltext_acquired','landing_only','search_index_text_acquired'] for r in a),fulltext_acquired=sum(r['acquisition_status'] in ['fulltext_acquired','browser_fulltext_acquired'] for r in a),fulltext_screened=sum(r['fulltext_screened'] for r in a),deeply_read=sum(r['deeply_read'] for r in a),retained_finalists=0,design_candidates=1 if org=='AntAC' else 0))
(P/'coverage.json').write_text(json.dumps(stats,indent=2));print(stats)
