"""Frozen comparison workflow, conservative cumulative reservations, no automatic retries.
Default replay is offline; --live makes authorized provider calls, never overwrites attempts.
"""
import json,os,sys,time,datetime,hashlib,urllib.request,urllib.error,math
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
QUESTIONS=json.loads((ROOT/'questions.json').read_text()); CRITERIA=set(['supported','conflict','unknown'])
def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def arithmetic(p,gates):
 a,b=p['evidence']['english'],p['evidence']['spanish']
 if 'conflict' in gates.values():return {'classification':'invalid_comparison'}
 if 'unknown' in gates.values() or a.get('value') is None or b.get('value') is None:return {'classification':'insufficient_evidence'}
 factors={'t':Decimal(1),'kt':Decimal(1000),'oz':Decimal(1),'koz':Decimal(1000),'MMoz':Decimal(1000000)}
 dimensions={'t':'mass','kt':'mass','oz':'troy','koz':'troy','MMoz':'troy'}
 if a['unit'] not in factors or b['unit'] not in factors or dimensions[a['unit']]!=dimensions[b['unit']]:return {'classification':'invalid_comparison'}
 av=Decimal(a['value'])*factors[a['unit']];bv=Decimal(b['value'])*factors[b['unit']];tol=Decimal(a['display_step'])*factors[a['unit']]+Decimal(b['display_step'])*factors[b['unit']]
 return {'classification':'comparable_agreement' if abs(bv-av)<=tol else 'comparable_numerical_difference','english_normalized':str(av),'spanish_normalized':str(bv),'difference_spanish_minus_english':str(bv-av),'tolerance':str(tol),'common_unit':a['unit']}
def python_gates(p):
 # Contract accepts reviewed layout fields, checked against supplied excerpts; no end-to-end claim.
 a,b=p['evidence']['english'],p['evidence']['spanish'];target=p['target'];g={k:'unknown' for k in QUESTIONS}
 at=json.dumps(a,ensure_ascii=False);bt=json.dumps(b,ensure_ascii=False)
 if 'Cerro Lindo' in at and 'Cerro Lindo' in bt:g['entity_operation']='supported'
 if a['year']!=target['year'] or b['year']!=target['year'] or 'después de adquisición' in b.get('report_scope','') or 'no producción100%' in b.get('report_scope',''):g['period_ownership']='conflict'
 elif 'wholly owned by Nexa Peru' in a['ownership_context'] and '1 de enero al 31 de' in b['report_scope'] and 'diciembre de 2025' in b['report_scope']:g['period_ownership']='supported'
 if 'm3'==b['unit']:g['measurement_product']='conflict'
 elif 'Metal contained in concentrates' in a['table_title'] and 'concentrados' in b['mine_context'] and ('finos' in b['table_text'] or 'Contenidos' in b['table_text']):g['measurement_product']='supported'
 valid={'t','kt','oz','koz','MMoz'}
 if a['unit'] in valid and b['unit'] in valid:g['units']='supported'
 elif a['unit'] and b['unit']:g['units']='conflict'
 if p['sources']['english'].get('filing_date') and p['sources']['spanish'].get('document_date') and 'PRELIMINAR' in b['version_context']:g['versions']='supported'
 return g
ENDPOINTS={'openai':'https://api.openai.com/v1/decisions','jev':'https://api.typesafe.ai/v1/systemone'}
MODELS={'openai':'gpt-6-luna','jev':'jev-1.13.0'}
RATE={'openai':Decimal('0.10'),'jev':Decimal('0.042')}
RESERVATION={'openai':250000,'jev':10000} # microusd; $5 per provider
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None

def live(provider,p):
 ledger=ROOT/'results/budget-ledger.jsonl';attempts=[json.loads(x) for x in ledger.read_text().splitlines()] if ledger.exists() else []
 if any(x['provider']==provider and (x['id']==p['id'] or x.get('status')!='completed') for x in attempts):raise RuntimeError('Prior attempt or provider blocker: live replay disallowed')
 used=sum(x['accounted_microusd'] for x in attempts if x['provider']==provider);reserve=RESERVATION[provider]
 if used+reserve>5_000_000:raise RuntimeError('Cumulative provider cap would be exceeded')
 env='OPENAI_API_KEY' if provider=='openai' else 'JEV_API_KEY'
 if not os.environ.get(env):raise RuntimeError('Existing credential unavailable; route stopped')
 body={'model':MODELS[provider],'state':p,'questions':QUESTIONS} if provider=='jev' else {'model':MODELS[provider],'input':json.dumps(p,ensure_ascii=False),'questions':[{'type':'choice','name':k,'instructions':q['instructions'],'choices':[{'value':v,'description':d} for v,d in q['criteria'].items()]} for k,q in QUESTIONS.items()]}
 encoded=json.dumps(body,ensure_ascii=False).encode();assert len(encoded)<30000
 # Deliberately allow five copies of the full UTF8 request, 4096 extra tokens/question.
 # One token/UTF8 byte overbound, safety overhead, max long-context+regional premium0.22/M.
 byte_token_bound=len(encoded)*5+4096*5;estimated_bound=Decimal(byte_token_bound)*Decimal('0.22' if provider=='openai' else '0.042')
 assert estimated_bound<=reserve
 # Validate today's archived primary documentation before sending and preserve both schemas.
 docs=(ROOT/'provenance/openai-decisions.md').read_text() if provider=='openai' else (ROOT/'provenance/jev-models.md').read_text()
 assert MODELS[provider] in docs and ('$0.10' in docs if provider=='openai' else '$0.042' in docs)
 frozen=json.loads((ROOT/'provenance/freeze.json').read_text())
 for filename,digest in frozen['sha256'].items():assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest
 write(ROOT/'raw'/f'{provider}-{p["id"]}.request.json',body)
 row={'provider':provider,'id':p['id'],'attempt':1,'auto_retries':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'endpoint':ENDPOINTS[provider],'requested_model':MODELS[provider],'request_sha256':hashlib.sha256(encoded).hexdigest(),'request_bytes':len(encoded),'input_token_upper_bound':byte_token_bound,'reservation_microusd':reserve,'accounted_microusd':reserve,'status':'reserved','billing_note':'Usage-derived list-price cost, not invoice. Failed/uncertain call retains full reservation.'}
 # Append reservation before network. Crash leaves full reserved entry and stops future calls.
 with ledger.open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
 start=time.perf_counter();resp=None
 try:
  req=urllib.request.Request(ENDPOINTS[provider],encoded,headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ[env]},method='POST')
  with urllib.request.build_opener(NoRedirect).open(req,timeout=55) as r:
   raw=r.read(2_000_001);row['http_status']=r.status;row['request_id']=r.headers.get('x-request-id')
  assert len(raw)<=2_000_000
  # Save exact response without key/authorization headers.
  (ROOT/'raw'/f'{provider}-{p["id"]}.response.json').write_bytes(raw);resp=json.loads(raw)
  assert resp.get('model')==MODELS[provider], 'Returned model differs; stop provider'
  usage=resp['usage'];n=usage['input_tokens'];out=usage.get('output_tokens');assert type(n)==int and 0<=n<=byte_token_bound
  cost=math.ceil(Decimal(n)*RATE[provider]);assert cost<=reserve
  row.update(status='completed',returned_model=resp['model'],usage=usage,usage_list_cost_usd=str(Decimal(n)*RATE[provider]/Decimal(1000000)),accounted_microusd=cost)
 except urllib.error.HTTPError as e:
  row.update(status='blocked_http',http_status=e.code,error_type='HTTPError')
  # Do not print response bodies/errors which could reflect authorization values.
 except Exception as e:row.update(status='failed_or_uncertain',error_type=type(e).__name__)
 finally:
  row['elapsed_seconds']=time.perf_counter()-start
  # Atomic replace preserves initial reservation plus completion via separate event log.
  with (ROOT/'results/attempt-events.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  final=attempts+[row];tmp=ledger.with_suffix('.tmp');tmp.write_text(''.join(json.dumps(x)+'\n' for x in final));tmp.replace(ledger)
 if row['status']!='completed':raise RuntimeError(f'Provider stopped: {row["status"]}, HTTP {row.get("http_status","unknown")}')
 return resp

def parse(provider,r):
 answers=r['answers'];by=answers if provider=='jev' else {a['name']:a for a in answers}
 g={k:by[k]['choice'] for k in QUESTIONS};assert all(v in CRITERIA for v in g.values());return g

def main():
 packets=[json.loads(x.read_text()) for x in sorted((ROOT/'packets').glob('*.json'))];result=[]
 for provider in ['python','openai','jev']:
  blocked=False
  for p in packets:
   start=time.perf_counter();row={'provider':provider,'id':p['id'],'kind':p['kind']}
   try:
    if provider=='python':g=python_gates(p)
    else:
     path=ROOT/'raw'/f'{provider}-{p["id"]}.response.json'
     if path.exists():r=json.loads(path.read_text())
     elif '--live' in sys.argv and not blocked:r=live(provider,p)
     else:raise RuntimeError('Provider output unavailable')
     g=parse(provider,r)
    row.update(gates=g,**arithmetic(p,g))
   except Exception as e:
    row.update(classification='insufficient_evidence',blocker=str(e));blocked=True
   row['elapsed_seconds']=time.perf_counter()-start;result.append(row)
   print(provider,p['id'],row['classification'],row.get('blocker',''),flush=True)
 write(ROOT/'results/arm-results.json',result)
if __name__=='__main__':main()
