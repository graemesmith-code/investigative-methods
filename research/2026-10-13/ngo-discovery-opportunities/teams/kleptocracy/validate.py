#!/usr/bin/env python3
import pathlib,json,collections
p=pathlib.Path(__file__).resolve().parent
rows=[json.loads(x) for x in (p/'inventory.jsonl').read_text().splitlines()]
assert len({r['url'] for r in rows})==len(rows)
required={'org','title','date','url','type','acquisition_status','fulltext_screened','deeply_read','bytes','sha256','pages','screening_rationale','opportunity_ids'}
for r in rows:
 assert required<=r.keys()
 assert r['url'].startswith('https://')
 assert r['fulltext_acquired'] is False
 if r['sha256']:assert r['bytes']>0 and len(r['sha256'])==64 and r['hash_scope'] in ['browser_rendered_excerpt','browser_batch_segment_unverified']
 if r.get('duplicate_of'):assert r['duplicate_of'] in {x['url'] for x in rows}
counts=json.loads((p/'counts.json').read_text())
for org,c in counts.items():
 rr=[r for r in rows if r['org']==org]
 assert c['unique_source_records']==len(rr)
 assert c['canonical_works_discovered']==sum(r['type']!='report_pdf' and not r.get('duplicate_of') for r in rr)
 assert c['retained_finalists']==0
 assert c['fulltext_passage_screened']==sum(r['fulltext_screened'] for r in rr)
assert json.loads((p/'checks.json').read_text())['cash_spend_usd']==0
print(f'PASS: {len(rows)} version records; {sum(c["canonical_works_discovered"] for c in counts.values())} canonical discoveries; zero finalists/spend')
