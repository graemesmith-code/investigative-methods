"""Offline coverage, chronology, deduplication, annual amounts and model audit."""
import json,pathlib,csv,collections,hashlib,re
P=pathlib.Path(__file__).resolve().parents[1];S=P/'sources'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
rows={r['filing_uuid']:r for f in sorted(S.glob('lda-*-[0-9]*.json')) for r in json.loads(f.read_text())['results']}
queries=[json.loads(f.read_text()) for f in sorted(S.glob('lda-*-summary.json'))]
coverage={'frozen_fara_documents':19,'original_fara_cohort_readable_in_browser':15,'original_fara_cohort_inaccessible':4,'additional_fara_amendments_read':2,'lda_queries':len(queries),'lda_unique_query_rows':len(rows),'lda_history_originals':137,'lda_original_files':len(list(S.glob('original-*.html'))),'all_queries_paginated_to_end':all(q['complete_query'] for q in queries),'unfiltered_access_probe_excluded':True}
save(P/'coverage.json',coverage)
with (P/'filing-index.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['uuid','posted','year','period','type','registrant_id','registrant','client_id','client','income','expenses','foreign_entities','original_url','local_original'])
 for uid,r in sorted(rows.items(),key=lambda x:x[1]['dt_posted']):w.writerow([uid,r['dt_posted'],r['filing_year'],r['filing_period'],r['filing_type'],r['registrant']['id'],r['registrant']['name'],r['client']['id'],r['client']['name'],r['income'],r['expenses'],json.dumps(r['foreign_entities']),r['filing_document_url'],str((S/f'original-{uid}.html').relative_to(P)) if (S/f'original-{uid}.html').exists() else 'not_acquired'])
# Latest report per registrant/client/quarter, never sum amendments or registrations.
latest={}
for r in rows.values():
 if r['filing_year']!=2025 or r['filing_type'] in ('RR','RA'):continue
 if r['client']['id'] not in [61125,69451,65440,118975,61553]:continue
 k=(r['registrant']['id'],r['client']['id'],r['filing_year'],r['filing_period'])
 if k not in latest or r['dt_posted']>latest[k]['dt_posted']:latest[k]=r
amounts={}
for r in latest.values():
 k=str(r['client']['id']);a=amounts.setdefault(k,{'client':r['client']['name'],'known_income':0,'null_income_reports':[],'included_uuids':[]});a['included_uuids'].append(r['filing_uuid'])
 if r['income'] is None:a['null_income_reports'].append(r['filing_uuid'])
 else:a['known_income']+=float(r['income'])
save(P/'annual-amounts.json',amounts)
base={(x['stage'],x['id']):x['priority'] for x in json.loads((P/'dossiers/code-baseline.json').read_text())};audit=[]
for stage in ['stage1','stage2','stage3']:
 for f in sorted((P/'jev'/stage).glob('*.response.json')):
  a=json.loads(f.read_text())['answers'];id=f.name.split('.')[0];audit.append({'stage':stage,'id':id,'answers':{k:v['choice'] for k,v in a.items()},'baseline':base.get((stage,id)),'internally_cautionary':a['disclosure']['choice']=='documentary_mismatch' and (a['control']['choice']!='supported' or a['identity']['choice']!='strong')})
save(P/'jev/audit.json',audit)
ledger=json.loads((P/'jev/ledger.json').read_text());save(P/'spending-summary.json',{'authorized_usd':15,'internal_cap_usd':14,'attempts':len(ledger['attempts']),'successes':sum(r['status']=='success' for r in ledger['attempts']),'accounted_usd':ledger['accounted_microusd']['jev']/1000000,'all_attempts_worst_case_reservation_usd':len(ledger['attempts'])*.003,'accounting':'Conservative per-call rounded estimate from returned usage and checked price, not provider invoice; previous pilot excluded. No other paid providers.'})
# Content hashes include derived text; separate HTTP manifest describes origin/access.
save(P/'source-hashes.json',{str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(S.iterdir()) if f.is_file()})
print(json.dumps(coverage));print(json.dumps(amounts));print((P/'spending-summary.json').read_text())
