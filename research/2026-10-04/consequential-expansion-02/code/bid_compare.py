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
  if set(b['prices'])!=ids: raise ValueError('Missing or unmatched price item; no imputation')
  original=Decimal(0);revised=Decimal(0)
  for i in items:
   rate=b['prices'][i['id']]
   if rate['currency']!=currency or rate['unit']!=i['unit']: raise ValueError('Currency or unit mismatch')
   p=amount(rate['rate']);original+=amount(i['q0'])*p;revised+=amount(i['q1'])*p
  out.append(dict(bid_id=b['id'],original=original,revised=revised))
 w=next(x for x in out if x['bid_id']==winner)
 original_min=min(x['original'] for x in out)
 reversal=w['original']==original_min and any(x['revised']<w['revised'] for x in out)
 return dict(totals=[{k:str(v) if isinstance(v,Decimal) else v for k,v in x.items()} for x in out],winner_had_original_lowest_price=w['original']==original_min,price_rank_reversal=reversal,interpretation='Counterfactual fixed-rate basket arithmetic only; not feasible rival performance, actual payment, causation or wrongdoing evidence.')
