from pathlib import Path
import json,hashlib,datetime,collections
p=Path(__file__).resolve().parents[1]
def read(n):return [json.loads(x) for x in (p/n).read_text().splitlines()]
checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name)
manifest=json.loads((p/'frozen-manifest.json').read_text())
check('nine frozen file hashes unchanged',len(manifest)==9 and all(hashlib.sha256((p/n).read_bytes()).hexdigest()==h for n,h in manifest.items()))
rank=read('uniform-consequence-ranking.jsonl');frozen=read('frozen-nine.jsonl');ref=read('refinement-groups.jsonl');results=read('results.jsonl');attempts=read('evidence/attempts.jsonl')
check('55 unique primary IDs and15zero-weight refinement records',len(rank)==55 and len({r['formulation_id'] for r in rank})==55 and len(ref)==15)
ordered=sorted(rank,key=lambda r:(-r['consequence_total'],r['formulation_id']));high=[];families=set()
for r in ordered:
 if r['family'] not in families:
  high.append(r['formulation_id']);families.add(r['family'])
 if len(high)==6:break
remaining=sorted(set(r['formulation_id'] for r in rank)-set(high))
seed='graeme-cross-family-2026-10-06-v1'
random=sorted(remaining,key=lambda k:hashlib.sha256((seed+'|'+k).encode()).hexdigest())[:3]
check('six family-diverse high and three seeded49-pool random reproduce',high==[r['formulation_id'] for r in frozen if r['arm']=='high_consequence'] and random==[r['formulation_id'] for r in frozen if r['arm']!='high_consequence'] and len(remaining)==49)
check('exactly nine frozen outcomes, no substitutions',len(results)==9 and {r['formulation_id'] for r in results}=={r['formulation_id'] for r in frozen})
check('honest outcomes and49charged attempts',collections.Counter(r['outcome'] for r in results)=={'indeterminate':7,'blocked':2} and sum(r['attempts'] for r in results)==49)
check('case costs match and at most12each',all(r['attempts']==sum(a['attempt_charge'] for a in attempts if a['test_id']==r['formulation_id'])<=12 for r in results))
check('logged spans plus60second uncertainty below900',all(r['logged_span_seconds']+60<900 for r in results))
check('no paid spend or administration counted as retrieval',all(a['paid_cost']==0 and (a['action'] not in ['close','resume','annotation'] or a['attempt_charge']==0) for a in attempts))
saved=[a['observation'] for a in attempts if isinstance(a.get('observation'),dict) and a['observation'].get('saved')]
check('saved HTTP body hashes and limits',all((p/'evidence'/r['file']).stat().st_size<=1572864 and hashlib.sha256((p/'evidence'/r['file']).read_bytes()).hexdigest()==r['sha256'] for r in saved))
check('TLS validation preserved and capped bodies unsaved',all(a['observation'].get('tls_validation') is True and not(a['status']=='byte_cap' and a['observation'].get('saved')) for a in attempts if a['action']=='http'))
check('EPA false join detected', (p/'evidence/X03-reporting-api.json').read_bytes()==(p/'evidence/X03-transfer-api.json').read_bytes())
check('CIA PDF-named response is not PDF',not (p/'evidence/N06-cia.pdf').read_bytes().startswith(b'%PDF'))
report={'passed':len(checks),'checks':checks,'limits':'Consistency tests do not certify source truth, selection eligibility or substantive legal conclusions.'}
(p/'validation-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
