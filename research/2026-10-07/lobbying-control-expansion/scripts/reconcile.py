"""Amendment-aware reported-amount screen. Null is unknown, never zero evidence."""
import json,collections,csv
from decimal import Decimal
from acquire import P,S
def reconcile():
 rows={r['filing_uuid']:r for f in S.glob('lda-annual-*.json') for r in json.loads(f.read_text())['results']}
 latest={};ties=[]
 for r in rows.values():
  if r['filing_type'] in ('RR','RA'):continue
  k=(r['client']['id'],r['registrant']['id'],r['filing_year'],r['filing_period'])
  old=latest.get(k)
  if old and old['dt_posted']==r['dt_posted']:ties.append([old['filing_uuid'],r['filing_uuid']])
  if old is None or (r['dt_posted'],r['filing_uuid'])>(old['dt_posted'],old['filing_uuid']):latest[k]=r
 annual={}
 for k,r in latest.items():
  a=annual.setdefault((k[0],k[1]),{'client_id':k[0],'client':r['client']['name'],'registrant_id':k[1],'registrant':r['registrant']['name'],'income_known':Decimal(0),'expenses_known':Decimal(0),'null_income_quarters':[],'null_expenses_quarters':[],'filings':[]})
  for field in ('income','expenses'):
   if r[field] is None:a['null_'+field+'_quarters'].append(r['filing_period'])
   else:a[field+'_known']+=Decimal(r[field])
  a['filings'].append({'uuid':r['filing_uuid'],'period':r['filing_period'],'posted':r['dt_posted'],'income':r['income'],'expenses':r['expenses'],'original':r['filing_document_url']})
 results=[]
 for a in annual.values():
  a['major_reported_lower_bound']=max(a['income_known'],a['expenses_known'])>=1000000
  a['income_known']=str(a['income_known']);a['expenses_known']=str(a['expenses_known']);results.append(a)
 corrections=[]
 for r in json.loads((P/'major-cohort.json').read_text()):
  k=(r['client']['id'],r['registrant']['id'],r['filing_year'],r['filing_period']);new=latest.get(k)
  if new and new['filing_uuid']!=r['filing_uuid']:
   corrections.append({'client_id':k[0],'client':r['client']['name'],'period':k[3],'old_uuid':r['filing_uuid'],'latest_uuid':new['filing_uuid'],'old_income':r['income'],'old_expenses':r['expenses'],'latest_income':new['income'],'latest_expenses':new['expenses'],'latest_has_numeric_million':any(new[x] is not None and Decimal(new[x])>=1000000 for x in ('income','expenses'))})
 (P/'annual-reconciled.json').write_text(json.dumps(results,indent=2));(P/'superseded-high-filings.json').write_text(json.dumps(corrections,indent=2))
 coverage=json.loads((P/'annual-coverage.json').read_text())
 summary={'clients_completed':sum(x['complete'] for x in coverage),'clients_target':259,'acquired_unique_2025_rows':len(rows),'latest_relationship_quarters':len(latest),'relationships':len(results),'clients_with_reported_numeric_million_lower_bound':len({a['client_id'] for a in results if a['major_reported_lower_bound']}),'superseded_high_filings':len(corrections),'superseded_below_million_or_null':sum(not x['latest_has_numeric_million'] for x in corrections),'same_timestamp_ties':ties,'caveat':'Reported amounts, not audited expenditures or foreign funding. Client-ID coverage is not all legal-group spending. Income and expenses never summed together. Nulls retained; originals must establish no activity or bounded amounts.'}
 (P/'reconciliation-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
if __name__=='__main__':reconcile()
