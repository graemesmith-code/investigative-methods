#!/usr/bin/env python3
"""Zero-network conservative baseline for the proposed scope interpretation pilot.
Fixtures are human-transcribed numeric facts from original public documents.
It tests abstention rules, NOT document extraction, AI performance or misconduct.
Pass JSONL claim pairs as an argument to classify new human/model-extracted pairs.
"""
import json,sys,pathlib

def classify(p):
    if p['unit_a']!=p['unit_b']:
        return 'unresolved_scope'
    if p['date_a']!=p['date_b']:
        return 'unresolved_date'
    if not p['bridge_verified']:
        return 'unresolved_membership'
    return 'agree' if abs(p['pct_a']-p['pct_b'])<0.001 else 'documentary_discrepancy_for_review'

root=pathlib.Path(__file__).resolve().parent
pairs=[json.loads(x) for x in (pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else root/'controls.jsonl').read_text().splitlines()]
results=[]
for p in pairs:
    result=classify(p)
    if 'expected' in p: assert result==p['expected'],(p['id'],result,p['expected'])
    results.append({'id':p['id'],'classification':result,'model_run':False,'allegation':False})
print(json.dumps({'classification_results':results,'cash_usd':0,'paid_calls':0,'limitations':'Human-transcribed controls; no OCR/model/timing benchmark run.'},indent=2))
