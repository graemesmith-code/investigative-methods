"""Date overlap only: caller must prove the presence interval, not assume persistence.
Two photographs bracketing a date do not by themselves establish this interval.
"""
from datetime import date
def overlaps_established_presence(claim_start,claim_end,presence_start,presence_end):
 cs,ce,ps,pe=map(date.fromisoformat,[claim_start,claim_end,presence_start,presence_end])
 if ce<cs or pe<ps:raise ValueError('Reversed interval')
 return max(cs,ps)<=min(ce,pe)
