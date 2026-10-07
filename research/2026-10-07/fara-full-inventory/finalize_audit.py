"""Offline final cohort dispositions and historical amendment-aware amount checks."""
import json,pathlib,datetime
from decimal import Decimal
from reconcile_major import amount
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[2]
def read(n):return json.loads((P/n).read_text())
edges=read('full-inventory-edges.json')+read('full-role-edges.json');annual={x['house_relationship_id']:x for x in read('house-annual-provisional.json')}
out=[]
for hid in sorted({x['house_relationship_id'] for x in edges}):
 a=annual[hid];out.append({'house_relationship_id':hid,'clients':a['client_names'],'registrants':a['registrant_names'],'major':a['provisional_major'],'disposition':'reviewed major discovery relationship; see original reconciliation and role review' if a['provisional_major'] else 'did not qualify on acquired numeric annual data; not a compliance clearance','discovery_roles':sorted({x.get('role','client') for x in edges if x['house_relationship_id']==hid}),'income_lower_bound':a['provisional_income_sum'],'expense_lower_bound':a['provisional_expense_sum']})
assert len(out)==343 and sum(x['major'] for x in out)==25
(P/'cohort-triage.json').write_text(json.dumps(out,indent=2))
rows={}
for stage in ['lobbying-control-pilot','lobbying-control-expansion','fara-full-inventory']:
 for f in (P.parent/stage/'sources').glob('*.json'):
  try:d=json.loads(f.read_text())
  except (ValueError,UnicodeError):continue
  if isinstance(d,dict):
   for r in d.get('results',[]):
    if isinstance(r,dict) and r.get('filing_uuid'):rows[r['filing_uuid']]=r
checks=[]
for cid,year in [(194108,2010),(194108,2011),(125608,2012)]:
 latest={}
 for r in sorted([r for r in rows.values() if r.get('client',{}).get('id')==cid and r.get('filing_year')==year and r.get('filing_type') not in ['RR','RA']],key=lambda r:datetime.datetime.fromisoformat(r['dt_posted'])):
  u=r['filing_uuid'];files=list(P.parent.glob('*/sources/*'+u+'*.html'));assert files,u
  values,boxes=amount(files[0].read_bytes());assert all((values[k] is None and r[k] is None) or (values[k] is not None and r[k] is not None and Decimal(values[k])==Decimal(r[k])) for k in values)
  period=r['filing_period'];latest[period]={'uuid':u,'source':r['filing_document_url'],'original':str(files[0].relative_to(ROOT)),'posted':r['dt_posted'],'period':period,'amounts':values,'matches_api':True}
 checks.append({'client_id':cid,'year':year,'selected_originals':list(latest.values()),'expense_numeric_sum':str(sum(Decimal(x['amounts']['expenses'] or 0) for x in latest.values())),'unknown_expense_cells':sum(x['amounts']['expenses'] is None for x in latest.values())})
(P/'historical-amount-verification.json').write_text(json.dumps(checks,indent=2));print([(x['client_id'],x['year'],x['expense_numeric_sum']) for x in checks])
