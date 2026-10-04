"""Synthetic arithmetic illustrations, not automatic evidence verification or legal conclusions."""
from decimal import Decimal,InvalidOperation

def num(x):
 try:y=Decimal(str(x))
 except (InvalidOperation,ValueError):raise ValueError('Invalid quantity')
 if not y.is_finite():raise ValueError('Nonfinite quantity')
 return y

def energy_check(*,output_lower_mwh,input_upper_mmbtu,boundary_complete=False,imports_storage_resolved=False,measurement_bounds_verified=False):
 if not all([boundary_complete,imports_storage_resolved,measurement_bounds_verified]):raise ValueError('Unresolved physical evidence gate')
 out=num(output_lower_mwh);inp=num(input_upper_mmbtu)
 if out<0 or inp<=0:raise ValueError('Require nonnegative output and positive total input bound')
 lower=out*Decimal('3.411')
 return dict(electrical_energy_lower_mmbtu=str(lower),all_input_upper_mmbtu=str(inp),unresolved_balance_flag=lower>inp,wrongdoing_established=False)

def recovery_check(payments,*,cost_upper,currency,same_cost_verified=False,cost_cap_verified=False,flow_independence_verified=False,measurement_bounds_verified=False):
 if not all([same_cost_verified,cost_cap_verified,flow_independence_verified,measurement_bounds_verified]):raise ValueError('Unresolved cost/flow/terms/bounds evidence gate')
 cost=num(cost_upper)
 if cost<0 or not payments:raise ValueError('Missing eligible cost or payments')
 seen=set();total=Decimal(0)
 for p in payments:
  key=p.get('canonical_settlement')
  if not key or key in seen:raise ValueError('Duplicate or unresolved underlying settlement')
  seen.add(key)
  if p.get('kind')!='completed_net_cost_recovery' or p.get('currency')!=currency:raise ValueError('Not a compatible completed net recovery')
  value=num(p['net_recovery_lower'])
  if value<0:raise ValueError('Reconcile refunds before supplying a nonnegative net lower bound')
  total+=value
 return dict(net_recoveries_lower=str(total),permitted_cost_upper=str(cost),unresolved_excess_flag=total>cost,wrongdoing_established=False)
