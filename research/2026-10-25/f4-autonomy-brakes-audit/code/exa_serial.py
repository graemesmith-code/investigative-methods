#!/usr/bin/env python3
"""Serialized, pre-reserved Exa search only. No other paid endpoint is used.
Official pricing checked 2026-10-25: /search auto <=10 results $0.007.
Response costDollars is retained separately from conservative budget debit.
Timeouts and errors keep full reservations; never automatically retried.
"""
import argparse,csv,datetime,fcntl,hashlib,json,os,pathlib,urllib.request
from decimal import Decimal
P=pathlib.Path(__file__).resolve().parents[1]
PRIVATE=pathlib.Path('/workspace/scratch/f4-private'); PRIVATE.mkdir(parents=True,exist_ok=True)
LOG=P/'audit/exa-query-cost-log.csv'
STOP=PRIVATE/'EXA_STOP.json'
FIELDS=['sequence','timestamp_utc','query','endpoint','type','num_results','status','reserved_usd','response_reported_usd','budget_debit_usd','new_cumulative_usd','all_cumulative_usd','response_sha256','error']
def run(query,contents=False):
 with open(PRIVATE/'exa.lock','a+') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  if STOP.exists():raise RuntimeError('Persistent Exa stop latch exists; no new paid request authorized by this runner')
  rows=list(csv.DictReader(LOG.open())) if LOG.exists() else []
  used=sum((Decimal(x['budget_debit_usd']) for x in rows),Decimal(0))
  # Official /contents rate: one URL, text only, $0.001; no summaries,
  # subpages, generated answers or paid model endpoint.
  reserve=Decimal('.001') if contents else Decimal('.007'); prior=Decimal('4.095')
  if used+reserve>Decimal('10.905'): raise RuntimeError('Budget ceiling: reservation refused')
  endpoint='/contents' if contents else '/search'
  row=dict.fromkeys(FIELDS,''); row.update(sequence=len(rows)+1,timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),query=query,endpoint=endpoint,type='cache-only text' if contents else 'auto',num_results=1 if contents else 10,status='reserved',reserved_usd=str(reserve),budget_debit_usd=str(reserve),new_cumulative_usd=str(used+reserve),all_cumulative_usd=str(prior+used+reserve))
  def save():
   temp=LOG.with_suffix('.tmp')
   with temp.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows+[row]);f.flush();os.fsync(f.fileno())
   temp.replace(LOG)
  save() # write reservation BEFORE request
  body=json.dumps({'urls':[query],'text':True,'maxAgeHours':-1} if contents else {'query':query,'type':'auto','numResults':10}).encode()
  req=urllib.request.Request('https://api.exa.ai'+endpoint,data=body,headers={'x-api-key':os.environ['EXA_API_KEY'],'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=55) as response: raw=response.read()
   obj=json.loads(raw); (PRIVATE/('exa-%04d.json'%row['sequence'])).write_bytes(raw)
   row.update(status='response',response_sha256=hashlib.sha256(raw).hexdigest())
   cost=obj.get('costDollars',{}); reported=cost.get('total') if isinstance(cost,dict) else cost
   if reported is not None:
    row['response_reported_usd']=str(reported)
    # Do not free an allocation if account/invoice cost is uncertain.
    if Decimal(str(reported))>reserve:
     row.update(status='cost_exceeds_reservation_STOP',budget_debit_usd=str(reported),new_cumulative_usd=str(used+Decimal(str(reported))),all_cumulative_usd=str(prior+used+Decimal(str(reported))))
     STOP.write_text(json.dumps({'reason':'reported_cost_exceeded_reservation','sequence':row['sequence'],'reported_usd':str(reported)}))
   results=[{k:r.get(k) for k in ['title','url','publishedDate','author']} for r in obj.get('results',[])]
   if contents:
    outcome={'sequence':row['sequence'],'url':query,'statuses':obj.get('statuses',[]),'returned_results':len(obj.get('results',[])),'text_characters':[len(r.get('text','')) for r in obj.get('results',[])],'response_sha256':row['response_sha256'],'provider_reported_estimated_usd':row['response_reported_usd'],'scope':'cache-only; no host access-gate workaround; source body private; full-document completeness not presumed'}
    with (PRIVATE/'contents-outcomes.jsonl').open('a') as f:f.write(json.dumps(outcome)+'\n')
   index=PRIVATE/'exa-results.jsonl'
   with index.open('a') as f:f.write(json.dumps({'sequence':row['sequence'],'query':query,'results':results},ensure_ascii=False)+'\n')
   save(); print(json.dumps({'ledger':row,'results':results},ensure_ascii=False),flush=True)
   if row['status'].endswith('STOP'):raise RuntimeError('Cost exceeded reservation; stop spending')
  except Exception as e:
   if row['status']!='cost_exceeds_reservation_STOP':row['status']='uncertain_no_retry'
   row['error']=type(e).__name__+': '+str(e);save();print(json.dumps(row),flush=True)
   raise
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('queries',type=pathlib.Path);a.add_argument('--contents',action='store_true'); args=a.parse_args()
 for q in args.queries.read_text().splitlines():
  if q.strip():run(q.strip(),args.contents)
