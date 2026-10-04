"""V01 arithmetic only. All semantic gates are caller-supplied evidence assertions.
No inference of compliance from a low bound; no automatic legal judgment.
"""
from decimal import Decimal,InvalidOperation

def number(x):
 try:d=Decimal(str(x))
 except (InvalidOperation,ValueError):raise ValueError('Invalid number')
 if not d.is_finite():raise ValueError('Nonfinite value')
 return d

def concentration_lower_bound(positions,*,fund_class,date,issuer_group,currency,denominator,cap_fraction,additive_nonnegative_measure_confirmed=False,denominator_verified=False,mandate_timing_and_exceptions_resolved=False):
 if not all([additive_nonnegative_measure_confirmed,denominator_verified,mandate_timing_and_exceptions_resolved]):raise ValueError('Unresolved exposure/denominator/mandate gate')
 d=number(denominator);cap=number(cap_fraction)
 if d<=0 or not 0<=cap<=1:raise ValueError('Invalid denominator or fraction')
 if not positions:raise ValueError('No verified positions')
 ids=[p['position_id'] for p in positions]
 if any(not isinstance(x,str) or not x for x in ids) or len(set(ids))!=len(ids):raise ValueError('Unique nonempty position IDs required')
 total=Decimal(0)
 for p in positions:
  if any(p[k]!=v for k,v in [('fund_class',fund_class),('date',date),('issuer_group',issuer_group),('currency',currency)]):raise ValueError('Position scope mismatch')
  v=number(p['measured_exposure'])
  if v<0:raise ValueError('Nonnegative additive measure required; no netting')
  total+=v
 return dict(verified_exposure_lower_bound=str(total),denominator=str(d),bound_fraction=str(total/d),cap_fraction=str(cap),lower_bound_exceeds=total>cap*d,compliance_established=False,interpretation='Arithmetic review flag only; undisclosed exposure is unknown, not zero. Caller assertions do not independently verify mandate, identity, exceptions or legal applicability.')
