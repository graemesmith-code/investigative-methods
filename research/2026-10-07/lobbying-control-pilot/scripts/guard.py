"""Jev-only adaptation of existing transactional reservation and cost controls."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location('sanctions_budget_base', ROOT / 'code/ati/pipeline.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.ENDPOINTS = {'jev': 'https://api.typesafe.ai/v1/systemone'}
base.CAP = 14_000_000
base.VERSION = 'lobbying-control-pilot-2026-10-07'
_validate = base.validate

def validate(provider, body, response):
    if provider != 'jev': raise base.GuardError('Only Jev authorized')
    choices = {k: q for k, q in body['questions'].items() if q['type'] == 'choice'}
    # Validate model, usage, answer keys and legacy types using existing logic.
    legacy_body = {**body, 'questions': {k:q for k,q in body['questions'].items() if k not in choices}}
    answers = response.get('answers', {})
    if set(answers) != set(body['questions']): raise base.GuardError('Answer keys differ')
    result = _validate(provider, legacy_body, {**response, 'answers': {k:a for k,a in answers.items() if k not in choices}})
    for k,q in choices.items():
        a=answers[k]; probs=a.get('probabilities', {})
        if a.get('type') != 'choice' or a.get('choice') not in q['criteria']: raise base.GuardError('Invalid choice')
        if set(probs) != set(q['criteria']) or any(not base.finite(v) or not 0<=v<=1 for v in probs.values()) or abs(sum(probs.values())-1)>.01: raise base.GuardError('Invalid distribution')
        if not base.finite(a.get('confidence')) or not 0<=a['confidence']<=1: raise base.GuardError('Invalid confidence')
    return result

base.validate = validate

def ledger(path):
    return base.Ledger(path, mode=base.VERSION, prior={'jev': 0})

class Client(base.Client):
    def call(self, provider, body):
        if provider != 'jev':
            raise base.GuardError('Only Jev is authorized')
        return super().call(provider, body)

def live_client():
    import os, json, urllib.request, datetime
    p=Path(__file__).resolve().parents[1]; out=p/'jev'; out.mkdir(exist_ok=True)
    if (out/'COMPLETE').exists(): raise base.GuardError('Completed pilot; live replay disabled, preserve ledger')
    price=json.loads((out/'price-verification.json').read_text())
    if price['date'] != datetime.datetime.now(datetime.timezone.utc).date().isoformat() or price['model'] != base.MODEL or price['usd_per_million_input'] != .042 or price['max_tokens'] != 64000:
        raise base.GuardError('Reverify pricing')
    key=os.environ.get('JEV_API_KEY') or os.environ.get('TYPESAFE_API_KEY')
    if not key: raise base.GuardError('Supported credential absent')
    base.OUT=out
    l=ledger(out/'ledger.sqlite')
    opener=urllib.request.build_opener(base.NoRedirect)
    def transport(provider, body):
        if provider != 'jev': raise base.GuardError('Only Jev authorized')
        req=urllib.request.Request(base.ENDPOINTS['jev'],data=base.packed(body).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
        with opener.open(req,timeout=60) as r:
            raw=r.read(2_000_001)
            if len(raw)>2_000_000: raise base.GuardError('Oversized response')
            result=json.loads(raw);result['_raw_response_utf8']=raw.decode();return result
    return Client(l,transport)

def validated_passage(source, passage):
    """Exact-text check only; never establishes a corporate relationship."""
    return bool(passage) and passage in source

