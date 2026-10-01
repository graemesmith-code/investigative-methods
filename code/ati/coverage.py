"""Execute reviewed Exa plans through the same cumulative ledger."""
import argparse,json,pathlib
from pipeline import OUT,Ledger,open_live_ledger,Client,LiveTransport,write

from make_plans import validate_plan

def run(path):
 plans=json.loads(pathlib.Path(path).read_text())
 rows=json.loads((OUT/'full-ranked.json').read_text())
 for plan in plans:validate_plan(plan,rows)
 ledger=open_live_ledger();client=Client(ledger,LiveTransport());out=[]
 try:
  for plan in plans:
   assert len(plan['queries'])<=2
   for query in plan['queries']:
    result=client.search(query);out.append({'plan':plan,'query':query,'response':result})
    write(OUT/(pathlib.Path(path).stem+'-results.json'),out)
    print(json.dumps({'lead':plan['lead'],'results':len(result['results']),'accounted_microusd':ledger.totals()}),flush=True)
 finally:ledger.export()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('plans');args=p.parse_args();run(args.plans)
