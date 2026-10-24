"""Validate the published F2 audit without source archives or network access."""
from pathlib import Path
from decimal import Decimal
import ast,csv,hashlib,json,re
P=Path(__file__).resolve().parents[1]
for f in P.rglob('*.json'): json.loads(f.read_text())
for f in (P/'code').glob('*.py'):ast.parse(f.read_text())
ledger=P/'exa/query-cost-log.csv';rows=list(csv.DictReader(ledger.open()))
assert len(rows)==104 and len({r['query_id'] for r in rows})==104
assert all(r['status']=='success' for r in rows)
assert all(Decimal(r['actual_cost_usd'])==Decimal('0.007') for r in rows)
assert sum(Decimal(r['actual_cost_usd']) for r in rows)==Decimal('0.728')
assert ledger.stat().st_size==29412
assert hashlib.sha256(ledger.read_bytes()).hexdigest()=='905af9ad514b734f298c6a12d48b145104457d597d092214528817ce5ca0c020'
assert json.loads((P/'audit/lane1-coverage_audit.json').read_text())['unique_transaction_keys']==712186
assert json.loads((P/'audit/lane1-enrichment_audit.json').read_text())['counts']['financial_transactions_unmatched']==0
assert len(json.loads((P/'audit/lane1-tactical-combination-register.json').read_text()))==384
# Inspectable registers have distinct denominators, not interchangeable subsets.
def read_csv(name):
 with (P/'audit'/name).open(newline='') as f:return list(csv.DictReader(f))
tactical=read_csv('lane1-tactical-candidates-384.csv')
emerging=read_csv('lane1-first-observed-recipients-65.csv')
phase3=read_csv('lane1-explicit-phase-iii-36.csv')
followons=read_csv('lane2-high-scoring-nonexact-followons-92.csv')
assert [len(x) for x in (tactical,emerging,phase3,followons)]==[384,65,36,92]
for rs in (tactical,emerging,phase3,followons):assert len({r['award_key'] for r in rs})==len(rs)
tk={r['award_key'] for r in tactical}
assert {r['award_key'] for r in emerging}<=tk
assert len({r['award_key'] for r in phase3}&tk)==6
qualifying=set()
for r in emerging:
 ds=json.loads(r['qualifying_first_observed_entity_dates_json'])
 assert ds and all(d>='2024-01-01' for d in ds.values())
 qualifying.update(ds)
assert len(qualifying)==60
fj=json.loads((P/'audit/lane2-high-scoring-nonexact-followons-92.json').read_text())
assert [r['award_key'] for r in followons]==[r['award_key'] for r in fj]
assert all(not r['exact_piid_in_sbir'] and r['followon_score']>=7 and r['aggregate_2024_on_obligation_cents']>0 for r in fj)
comparison=json.loads((P/'audit/lane2-reconstruction-comparison.json').read_text())
assert comparison['differing_join_counts']['distinct_broad_recipient_followon_piids']=={'original':2809,'reconstructed':2834}
assert comparison['filter_unchanged'] and comparison['flags_not_adjusted_to_force_count']
for piid,total in [('HR0011269E197','4903954.00'),('HR0011269E025','7085366.00'),('HQ08452390066','6262295.57')]:
 d=json.loads((P/'evidence/funding'/f'{piid}_parsed.json').read_text())
 assert len({r['modNumber'] for r in d['rows']})==len(d['rows'])
 assert sum(Decimal(r['obligatedAmount']) for r in d['rows'])==Decimal(total)
# Preserve, rather than accidentally repair, the Marine aggregate discrepancy.
d=json.loads((P/'evidence/funding/M678542690040_parsed.json').read_text())
assert sum(Decimal(r['obligatedAmount']) for r in d['rows'])==Decimal('17444750.05')
assert Decimal(d['rows'][-1]['totalObligatedAmount'])==Decimal('24499918.09')
if (P/'manifest.json').exists():
 for r in json.loads((P/'manifest.json').read_text())['files']:
  p=P/r['path'];assert p.stat().st_size==r['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r['path']
print('PASS: JSON/Python syntax, 104-query ledger, archive coverage, narrower register and principal action arithmetic')
