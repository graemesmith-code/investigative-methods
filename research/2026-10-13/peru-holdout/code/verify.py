"""Offline evidence integrity, denominator, arithmetic, budget and secret checks."""
import json,hashlib,os,sys,tempfile,shutil,urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent));import run
ROOT=run.ROOT
freeze=json.loads((ROOT/'provenance/freeze.json').read_text());pf=json.loads((ROOT/'provenance/packet-freeze.json').read_text());rf=json.loads((ROOT/'provenance/runner-freeze.json').read_text())
for filename,digest in freeze['sha256'].items():assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest
for filename,digest in pf['packet_sha256'].items():assert hashlib.sha256((ROOT/'packets'/filename).read_bytes()).hexdigest()==digest
assert hashlib.sha256((ROOT/'reference-review.json').read_bytes()).hexdigest()==pf['reference_sha256']
for filename,digest in rf['code_sha256'].items():assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest
packets={f.stem:json.loads(f.read_text()) for f in (ROOT/'packets').glob('*.json')};results=json.loads((ROOT/'results/arm-results.json').read_text());assert len(packets)==10 and len(results)==30
assert sum(p['kind']=='natural_holdout' for p in packets.values())==5
for provider in ['python','openai','jev']:assert {r['id'] for r in results if r['provider']==provider}==set(packets)
ledger=[json.loads(l) for l in (ROOT/'results/budget-ledger.jsonl').read_text().splitlines()];assert len(ledger)==20
for provider in ['openai','jev']:
 assert sum(r['accounted_microusd'] for r in ledger if r['provider']==provider)<=5_000_000
 for p in packets.values():
  request=json.loads((ROOT/'raw'/f'{provider}-{p["id"]}.request.json').read_text());evidence=request['state'] if provider=='jev' else json.loads(request['input']);assert evidence==p
  response=json.loads((ROOT/'raw'/f'{provider}-{p["id"]}.response.json').read_text());assert response['model']==run.MODELS[provider]
  row=next(r for r in results if r['provider']==provider and r['id']==p['id']);assert row['classification']==run.arithmetic(p,run.parse(provider,response))['classification']
# Test hard budget denial before network, and durable auth-failure accounting using fake transport.
with tempfile.TemporaryDirectory(prefix='peru-budget-test-') as td:
 root=Path(td);(root/'results').mkdir();(root/'raw').mkdir();(root/'provenance').mkdir()
 for filename in ['questions.json','protocol.json']:shutil.copy(ROOT/filename,root/filename)
 for filename in ['freeze.json','openai-decisions.md']:shutil.copy(ROOT/'provenance'/filename,root/'provenance'/filename)
 with patch.object(run,'ROOT',root):
  (root/'results/budget-ledger.jsonl').write_text(json.dumps({'provider':'openai','id':'other','status':'completed','accounted_microusd':4_900_000})+'\n')
  try:run.live('openai',packets['CL-2025-Zn']);raise AssertionError('Cap failed')
  except RuntimeError as e:assert 'cap' in str(e)
  (root/'results/budget-ledger.jsonl').unlink()
  class Denied:
   def open(self,*a,**kw):raise urllib.error.HTTPError('https://api.openai.com/v1/decisions',401,'Unauthorized',{},None)
  with patch.dict(os.environ,{'OPENAI_API_KEY':'fictional-offline-test-key'}),patch.object(run.urllib.request,'build_opener',return_value=Denied()):
   try:run.live('openai',packets['CL-2025-Zn']);raise AssertionError('401 failed to stop')
   except RuntimeError as e:assert '401' in str(e)
   log=[json.loads(l) for l in (root/'results/budget-ledger.jsonl').read_text().splitlines()];assert log[0]['accounted_microusd']==250000 and log[0]['status']=='blocked_http'
   try:run.live('openai',packets['CL-2025-Au']);raise AssertionError('Blocked provider resumed')
   except RuntimeError as e:assert 'blocker' in str(e)
# Never print candidate credential values, even on failed scan.
for file in ROOT.rglob('*'):
 if file.is_file():
  content=file.read_bytes()
  for name in ['OPENAI_API_KEY','JEV_API_KEY','EXA_API_KEY']:
   key=os.environ.get(name,'')
   assert not key or key.encode() not in content,'Existing credential detected in candidate file; stop publication'
print('PASS: immutable protocol/packets/reference/runner;30rows/10targets;20saved paid calls;identical provider evidence;reproduced classifications;provider caps;offline401retains reservation and halts;no credential values.')
