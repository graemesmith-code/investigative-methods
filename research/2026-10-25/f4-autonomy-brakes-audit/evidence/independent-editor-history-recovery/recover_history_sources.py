import pathlib,csv,json,urllib.request,hashlib,datetime,concurrent.futures
R=pathlib.Path(__file__).parent
A=pathlib.Path('/workspace/shared/f4-editor-recovery/sources/evidence/fpds-verified-actions.csv')
a=[r for r in csv.DictReader(A.open()) if r['piid'] in ['FD01','N0016422F3007','N0042123F3004']]
refs={r['source_url']:r['response_sha256'] for r in a};assert len(a)==177 and len(refs)==19
with (R/'retained-177-actions.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(a[0]));w.writeheader();w.writerows(a)
def get(pair):
 u,old=pair;d={'source_url':u,'historical_expected_sha256':old,'retrieval_started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=90) as h:b=h.read();d['http_status']=h.status
  sh=hashlib.sha256(b).hexdigest();p=R/'responses'/(sh+'.xml');p.parent.mkdir(exist_ok=True);p.write_bytes(b);d.update(sha256=sh,bytes=len(b),path=str(p.relative_to(R)),matches_historical_response_sha256=sh==old)
 except Exception as e:d.update(error_type=type(e).__name__,error=str(e))
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:out=list(ex.map(get,refs.items()))
(R/'primary-response-recovery.json').write_text(json.dumps(out,indent=2))
base='https://raw.githubusercontent.com/graemesmith-code/investigative-methods/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/'
for p in ['audit/acquisition-history-coverage.json','evidence/acquisition-history-missing-actions.csv']:
 b=urllib.request.urlopen(base+p,timeout=90).read();(R/pathlib.Path(p).name).write_bytes(b)
print({'pages':len(out),'success':sum(x.get('http_status')==200 for x in out),'historical_hash_exact_matches':sum(x.get('matches_historical_response_sha256',False) for x in out),'errors':[x for x in out if 'error' in x]})
