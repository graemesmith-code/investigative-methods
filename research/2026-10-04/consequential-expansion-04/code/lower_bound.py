"""V01 arithmetic only. All semantic gates are caller-supplied evidence assertions.
No inference of compliance from a low bound; no automatic legal judgment.
"""
from decimal import Decimal,InvalidOperation

def number(x):
 try:d=Decimal(str(x))
 except (InvalidOperation,ValueError):raise ValueError('Invalid number')
 if not d.is_finite():raise ValueError('Nonfinite value')
 return d

def concentration_lower_bound(positions,*,fund_class,date,issuer_group,currency,denominator,cap_fraction,additive_nonnegative_measure_confirmed=False,denominator_verified=False,mandate_timing_and_exceptions_resolved=False,evidence_manifest=None,denominator_upper_bound=None,measurement_uncertainty_resolved=False):
 if not all([additive_nonnegative_measure_confirmed,denominator_verified,mandate_timing_and_exceptions_resolved]):raise ValueError('Unresolved exposure/denominator/mandate gate')
 if not measurement_uncertainty_resolved or denominator_upper_bound is None:raise ValueError('Conservative measurement/rounding bounds required')
 d=number(denominator);upper=number(denominator_upper_bound);cap=number(cap_fraction)
 if upper<d or upper<=0:raise ValueError('Denominator upper bound invalid')
 if d<=0 or not 0<=cap<=1:raise ValueError('Invalid denominator or fraction')
 if not positions:raise ValueError('No verified positions')
 ids=[p['position_id'] for p in positions]
 if any(not isinstance(x,str) or not x for x in ids) or len(set(ids))!=len(ids):raise ValueError('Unique nonempty position IDs required')
 if not evidence_manifest or not evidence_manifest.get('canonical_mapping_verified') or not evidence_manifest.get('aggregate_detail_resolution_verified'):
  raise ValueError('Evidence-level canonical and aggregate/detail review required')
 vintage=evidence_manifest.get('selected_vintage')
 if not vintage:raise ValueError('One selected filing vintage required')
 records=evidence_manifest.get('records',{})
 canonical_seen=set();locator_seen=set()
 total=Decimal(0)
 for p in positions:
  locator=p.get('evidence_locator')
  if not locator or locator not in records or locator in locator_seen:raise ValueError('Missing or duplicate source-row evidence')
  locator_seen.add(locator);r=records[locator]
  if r.get('vintage')!=vintage:raise ValueError('Mixed filing vintages/revisions')
  digest=r.get('source_sha256','')
  if len(digest)!=64 or any(ch not in '0123456789abcdef' for ch in digest):raise ValueError('Source content hash required')
  if r.get('row_kind')!='individual_position':raise ValueError('Aggregate/confidential-total rows excluded from this helper')
  canonical=r.get('canonical_holding_key')
  if not canonical or canonical in canonical_seen:raise ValueError('Duplicate or unresolved canonical holding')
  canonical_seen.add(canonical)
  if number(r['measured_exposure'])!=number(p['measured_exposure']):raise ValueError('Exposure differs from reviewed source evidence')
  if any(p[k]!=v for k,v in [('fund_class',fund_class),('date',date),('issuer_group',issuer_group),('currency',currency)]):raise ValueError('Position scope mismatch')
  v=number(p['measured_exposure'])
  if v<0:raise ValueError('Nonnegative additive measure required; no netting')
  lower=number(r.get('exposure_lower_bound'))
  if lower<0 or lower>v:raise ValueError('Conservative exposure lower bound invalid')
  total+=lower
 return dict(verified_exposure_lower_bound=str(total),denominator=str(d),denominator_upper_bound=str(upper),bound_fraction=str(total/upper),cap_fraction=str(cap),lower_bound_exceeds=total>cap*upper,compliance_established=False,interpretation='Arithmetic review flag only; undisclosed exposure is unknown, not zero. Evidence manifest must come from reviewed source rows, with canonical holding identity and one selected vintage; this helper does not authenticate documents or discover disguised duplicates. Caller assertions do not independently verify mandate, identity, exceptions or legal applicability.')
