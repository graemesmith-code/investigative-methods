import pathlib,json,datetime,sys
P=pathlib.Path(__file__).resolve().parents[1]
def log(test,action,target,status,observation,attempts=1):
 if action in ('close','resume','annotation'):attempts=0
 r=dict(test_id=test,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),action=action,target=target,status=status,observation=observation,attempt_charge=attempts,paid_cost=0)
 with (P/'evidence/attempts.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 return r
if __name__=='__main__':log(*sys.argv[1:6])
