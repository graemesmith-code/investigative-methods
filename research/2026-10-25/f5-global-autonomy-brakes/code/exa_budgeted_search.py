#!/usr/bin/env python3
"""Sole serialized F5 Exa spender. Explicit opt-in; standard library only.

Prices verified https://exa.ai/pricing 2026-10-25: auto <=10 results,
without content/summary options, $0.007. Never retries uncertain paid calls.
Logs and public search metadata belong outside Git, with raw responses kept
private until public-clearance. Missing provider cost retains reservation.
"""
import argparse, csv, datetime, decimal, fcntl, hashlib, json, os
from pathlib import Path
import urllib.request
D=decimal.Decimal
FIELDS=['sequence','timestamp_utc','query','status','reserved_usd','provider_reported_usd','exposure_debit_usd','new_exposure_usd','cumulative_exposure_usd','cache_hit','response_sha256','error']
def search(query, directory):
    directory=Path(directory); directory.mkdir(parents=True,exist_ok=True)
    ledger=directory/'exa-query-cost-log.csv'
    with (directory/'exa.lock').open('a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if (directory/'EXA_STOP').exists(): raise RuntimeError('Exa stop latch')
        rows=list(csv.DictReader(ledger.open())) if ledger.exists() else []
        used=sum((D(r['exposure_debit_usd']) for r in rows),D(0))
        reserve=D('0.007'); prior=D('5.735')
        if used+reserve>D('14.265'): raise RuntimeError('Reservation would exceed $20 ceiling')
        # Exact local cache hits incur no provider call or additional exposure.
        for r in rows:
            if r['query']==query and r['status']=='response':
                return {'local_cache_hit':True,'sequence':r['sequence']}
        row=dict.fromkeys(FIELDS,''); row.update(sequence=len(rows)+1,timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),query=query,status='reserved',reserved_usd=str(reserve),exposure_debit_usd=str(reserve),new_exposure_usd=str(used+reserve),cumulative_exposure_usd=str(prior+used+reserve),cache_hit='false')
        def save():
            temp=ledger.with_suffix('.tmp')
            with temp.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows+[row]);f.flush();os.fsync(f.fileno())
            temp.replace(ledger)
        save()
        req=urllib.request.Request('https://api.exa.ai/search',data=json.dumps({'query':query,'type':'auto','numResults':10}).encode(),headers={'x-api-key':os.environ['EXA_API_KEY'],'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(req,timeout=55) as response: raw=response.read()
            obj=json.loads(raw); digest=hashlib.sha256(raw).hexdigest()
            (directory/('exa-%04d.json'%row['sequence'])).write_bytes(raw)
            cost=obj.get('costDollars'); total=cost.get('total') if isinstance(cost,dict) else cost
            row.update(status='response',response_sha256=digest)
            if total is not None:
                reported=D(str(total))
                if reported<0: raise ValueError('Negative provider cost')
                row['provider_reported_usd']=str(reported)
                # Provider estimate is recorded; retain conservative reservation
                # until final billing, even if a provider cache hit reports zero.
                debit=max(reported,reserve)
                row.update(exposure_debit_usd=str(debit),new_exposure_usd=str(used+debit),cumulative_exposure_usd=str(prior+used+debit))
                if reported>reserve:
                    row['status']='cost_exceeds_reservation_STOP'
                    (directory/'EXA_STOP').write_text('Provider cost exceeded preflight reservation\n')
            results=[{k:r.get(k) for k in ['title','url','publishedDate','author']} for r in obj.get('results',[])]
            with (directory/'exa-discovery-results.jsonl').open('a') as f:
                f.write(json.dumps({'sequence':row['sequence'],'query':query,'results':results},ensure_ascii=False)+'\n')
            save(); return {'ledger':row,'results':results}
        except Exception as e:
            if row['status']!='cost_exceeds_reservation_STOP': row['status']='uncertain_no_retry'
            row['error']=type(e).__name__+': '+str(e); save(); raise
def main():
    p=argparse.ArgumentParser();p.add_argument('queries',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    for query in a.queries.read_text().splitlines():
        if query.strip(): print(json.dumps(search(query.strip(),a.output),ensure_ascii=False),flush=True)
if __name__=='__main__': main()
