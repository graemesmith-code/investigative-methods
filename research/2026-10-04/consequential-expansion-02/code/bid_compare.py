"""Arithmetic aid for Z01. Caller must independently establish evidence gates.
No data acquisition, legal conclusions, estimated missing prices or fraud scores.
"""
from decimal import Decimal, InvalidOperation

def amount(v):
 try: n=Decimal(str(v))
 except (InvalidOperation,ValueError): raise ValueError('Invalid numeric value')
 if not n.is_finite() or n<0: raise ValueError('Nonnegative finite values required')
 return n

def compare(items,bids,winner,currency):
 if not items or len({i['id'] for i in items})!=len(items): raise ValueError('Unique complete item schedule required')
 ids={i['id'] for i in items}
 eligible=[b for b in bids if b['eligible']]
 if len({b['id'] for b in bids})!=len(bids): raise ValueError('Duplicate bid identifier')
 if len(eligible)<2 or winner not in {b['id'] for b in eligible}: raise ValueError('Winner and at least one compliant comparator required')
 out=[]
 for b in eligible:
  if not b.get('revised_basket_equivalence_confirmed'): raise ValueError('Revised-basket comparability not established')
  for gate in ['quantity_pricing_confirmed','fixed_charges_accounted','specifications_equivalent','performance_comparable','rate_adjustments_accounted']:
   if not b.get(gate): raise ValueError('Unresolved pricing/performance gate: '+gate)
  if set(b['prices'])!=ids: raise ValueError('Missing or unmatched price item; no imputation')
  original=Decimal(0);revised=Decimal(0)
  for i in items:
   rate=b['prices'][i['id']]
   if rate['currency']!=currency or rate['unit']!=i['unit']: raise ValueError('Currency or unit mismatch')
   p=amount(rate['rate']);original+=amount(i['q0'])*p;revised+=amount(i['q1'])*p
  out.append(dict(bid_id=b['id'],original=original,revised=revised))
 w=next(x for x in out if x['bid_id']==winner)
 original_min=min(x['original'] for x in out)
 reversal=w['original']==original_min and any(w['original']<x['original'] and x['revised']<w['revised'] for x in out)
 tie_to_loss=any(x['bid_id']!=winner and w['original']==x['original'] and x['revised']<w['revised'] for x in out)
 comparisons=[]
 wb=next(b for b in eligible if b['id']==winner)
 for b in eligible:
  if b['id']==winner:continue
  x=next(x for x in out if x['bid_id']==b['id'])
  contributions=[]
  for i in items:
   difference=amount(b['prices'][i['id']]['rate'])-amount(wb['prices'][i['id']]['rate'])
   contributions.append(dict(item_id=i['id'],original_margin=str(amount(i['q0'])*difference),revised_margin=str(amount(i['q1'])*difference),quantity_change_effect=str((amount(i['q1'])-amount(i['q0']))*difference)))
  comparisons.append(dict(rival=b['id'],original_rival_minus_winner=str(x['original']-w['original']),revised_rival_minus_winner=str(x['revised']-w['revised']),item_contributions=contributions))
 return dict(comparisons=comparisons,totals=[{k:str(v) if isinstance(v,Decimal) else v for k,v in x.items()} for x in out],winner_had_original_lowest_price=w['original']==original_min,price_rank_reversal=reversal,initial_tie_to_loss=tie_to_loss,interpretation='Counterfactual fixed-rate basket arithmetic only; not feasible rival performance, actual payment, causation or wrongdoing evidence.')
