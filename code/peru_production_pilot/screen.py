"""Reproduce the frozen Peru pilot from reviewed observations. Python standard library only.

This is an arithmetic and evidence-gate runner, not an autonomous filing extractor.
Never infer illegality or a company contradiction from a numerical difference alone.
"""
from __future__ import annotations
import argparse, collections, copy, json, time
from decimal import Decimal as D
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / 'research/2026-10-12/peru-production-pilot'
FACTORS = {'t': D(1), 'kt': D(1000), 'thousand_lb': D('0.45359237'), 'million_lb': D('453.59237')}
def conversion(unit, metal):
    if unit in FACTORS:
        if metal in ('Au','Ag'): raise ValueError('Mass basis is not configured for this precious-metal observation')
        return FACTORS[unit]
    if unit in ('oz','koz') and metal in ('Au','Ag'):
        return D('31.1034768') * (1000 if unit=='koz' else 1) / (1000 if metal=='Ag' else 1)
    raise ValueError(f'Unsupported or ambiguous unit/metal: {unit}/{metal}')
def compare(record):
    r=copy.deepcopy(record); w=r.get('western_claim')
    r.update(numeric_flag=None, western_normalized=None, difference_host_minus_west=None, rounding_allowance=None, difference_pct_of_west=None)
    r['confirmed_company_contradiction']=False
    if w is None or r.get('host_original_value') is None:
        r['result']='missing_observation'; return r
    if any(w.get(k)!=r.get(k) for k in ('entity_id','metal','year')):
        r['result']='blocked_metadata_mismatch'; return r
    if any(x is None for x in w['components']):
        r['result']='missing_numeric_component'; return r
    factor=conversion(w['unit'],r['metal'])
    west=sum(D(x) for x in w['components'])*factor
    allowance=D(w['rounding_step'])*len(w['components'])*factor
    host=D(r['host_original_value']); difference=host-west
    flag=abs(difference)>allowance
    r.update(western_normalized=str(west),difference_host_minus_west=str(difference),rounding_allowance=str(allowance),numeric_flag=flag,
             difference_pct_of_west=str(difference/abs(west)*100) if west else None)
    # Eligibility is a reviewed input, not inferred from numerical agreement.
    if r.get('blocker') or not r.get('screen_eligible'):
        r['result']='blocked_comparability'
    else:
        r['result']='unresolved_numeric_difference' if flag else 'consistent_with_display_precision'
    # No automatic proof promotion. A separate evidence review must establish
    # assertion identity, original submissions, and correction/supersession history.
    return r

def summarize(results):
    return {'frozen_records':len(results),'gold_records':sum(r['metal']=='Au' for r in results),
            'numeric_pairs':sum(r['numeric_flag'] is not None for r in results),
            'raw_numeric_flags_including_blocked':sum(r['numeric_flag'] is True for r in results),
            'raw_within_precision_including_blocked':sum(r['numeric_flag'] is False for r in results),
            'narrow_screen_eligible':sum(r['screen_eligible'] for r in results),
            'outcomes':dict(collections.Counter(r['result'] for r in results)),
            'confirmed_company_contradictions':0,
            'phase_outcomes':{phase:dict(collections.Counter(r['result'] for r in results if r['phase']==phase)) for phase in ['development','transfer_test']},
            'gold_outcomes':dict(collections.Counter(r['result'] for r in results if r['metal']=='Au'))}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data-dir',type=Path,default=DEFAULT);args=ap.parse_args()
    records=json.loads((args.data_dir/'comparison-input.json').read_text())
    start=time.perf_counter();results=[compare(r) for r in records];elapsed=time.perf_counter()-start
    summary=summarize(results);summary['cached_comparison_seconds']=elapsed
    for name,content in [('results.json',results),('summary.json',summary)]:
        (args.data_dir/name).write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
