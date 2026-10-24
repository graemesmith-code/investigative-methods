import os
import gzip,json,re,collections,pathlib,decimal
p=pathlib.Path(os.environ.get('F2_ROOT', '.')).resolve()
rx=re.compile(r'\b(scout ai|altamar|wolfrider|tiami|analatom|nexcepta|schemata)\b',re.I)
piids=['N6523623C8011','N6523623C8001','N6523623C8002','HR00112530141','HR00112530154','HR00112530203','HR00112530331','HR00112430148']
counts=collections.Counter(); rows=[]; seen=set(); dup=0
with gzip.open(p/'data/normalized/financial_actions.jsonl.gz','rt') as g:
 for line in g:
  counts['all_rows']+=1;o=json.loads(line)
  if not (rx.search(o.get('entity_name','')) or any(x in o.get('award_key','') for x in piids)):continue
  counts['matching_rows']+=1
  if o['transaction_key'] in seen:dup+=1;continue
  seen.add(o['transaction_key']);rows.append(o)
(p/'lane5/financial_matches.jsonl').write_text('\n'.join(json.dumps(x) for x in rows)+'\n')
a={}
for o in rows:
 k=o['award_key'];x=a.setdefault(k,{'award_key':k,'entity_name':o['entity_name'],'actions':0,'sum_obligations':decimal.Decimal(0),'first_date':o['action_date'],'last_date':o['action_date'],'source_url':o['source_url']})
 x['actions']+=1;x['sum_obligations']+=decimal.Decimal(o.get('action_obligation_usd') or '0');x['first_date']=min(x['first_date'],o['action_date']);x['last_date']=max(x['last_date'],o['action_date'])
for x in a.values():x['sum_obligations']=str(x['sum_obligations'])
(p/'lane5/financial_summary.json').write_text(json.dumps({'counts':counts,'duplicate_matching_keys':dup,'awards':list(a.values())},indent=2))
print(counts,'dups',dup)
for x in a.values():print(x)
