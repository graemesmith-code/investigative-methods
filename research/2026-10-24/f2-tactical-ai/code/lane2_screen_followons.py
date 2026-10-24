import os
import json,sqlite3,re,collections
from pathlib import Path
B=Path(os.environ.get('F2_ROOT', '.')).resolve();O=B/'lane2'
rmap={}
for l in open(O/'recipient_potential_followons.jsonl'):
 r=json.loads(l)
 if r['broad_sbir_piids']:rmap[r['row_number']]=r
patterns={
 'ai':r'\b(?:AI|ML|neural|reinforcement|learning|intelligent|artificial intelligence|perception|computer vision)\b',
 'tactical':r'\b(?:autonom\w*|robot\w*|swarm\w*|munition\w*|unmanned|uncrewed|electronic warfare|electronic attack|target\w*|seeker\w*|guidance|navigat\w*|combat\w*|loitering|breach\w*|jam\w*)\b',
 'transition':r'\b(?:PHASE III|PHASE 3|STRATFI|TACFI|APFIT|RDER|OPERAT\w*|FIELD\w*|PROTOTYPE\w*|INTEGRAT\w*|PRODUCTION|DEMONSTRAT\w*)\b'}
rx={k:re.compile(p,re.I) for k,p in patterns.items()}
c=sqlite3.connect('file:'+str(B/'data/financial_actions.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
aws=collections.defaultdict(list);n=0;chars=0
for x in c.execute("select row_number,description_text,psc_text,naics_text,agency_text from source_rows where action_date>='2024-01-01'"):
 if x['row_number'] not in rmap:continue
 n+=1;r=rmap[x['row_number']];r.update(dict(x));t=r['description_text'] or '';chars+=len(t);r['followon_hits']={k:sorted(set(m.group(0) for m in p.finditer(t))) for k,p in rx.items()};h=r['followon_hits'];r['followon_score']=bool(h['ai'])*3+bool(h['tactical'])*4+bool(h['transition'])*3
 aws[r['award_key']].append(r)
with (O/'followon_description_screen.jsonl').open('w') as f:
 for k,rs in aws.items():
  r=max(rs,key=lambda x:x['followon_score']);r=dict(r);r['action_count_2024_on']=len(rs);r['obligation_sum_2024_on']=sum(int(x['obligation_cents'] or 0) for x in rs)/100;r['all_descriptions']=sorted(set(x['description_text'] for x in rs));f.write(json.dumps(r)+'\n')
print('Rows screened',n,'chars',chars,'awards',len(aws))
rank=[]
for rs in aws.values():
 r=max(rs,key=lambda x:x['followon_score']);r=dict(r);r['sum']=sum(int(x['obligation_cents'] or 0) for x in rs)/100
 if not r['exact_piid_in_sbir'] and r['followon_score']>=7 and r['sum']>0:rank.append(r)
rank.sort(key=lambda x:(x['followon_score'],x['sum']),reverse=True)
for r in rank[:140]:print(r['followon_score'],r['entity_name'],r['award_id'],r['sum'],r['description_text'][:1000],sep=' | ')
(O/'followon_description_audit.json').write_text(json.dumps({'row_count':n,'chars':chars,'awards':len(aws),'high_scoring_nonexact_awards':len(rank),'patterns':patterns},indent=2))
