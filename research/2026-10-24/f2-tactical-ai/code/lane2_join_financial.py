import os
import json,gzip,re,sqlite3,collections
from pathlib import Path
B=Path(os.environ.get('F2_ROOT', '.')).resolve(); OUT=B/'lane2'
def norm(s): return re.sub(r'[^A-Z0-9]','',str(s or '').upper())
def en(s):
 s=re.sub(r'[^A-Z0-9 ]',' ',str(s or '').upper());return re.sub(r'\b(?:INCORPORATED|CORPORATION|COMPANY|LIMITED|INC|CORP|LLC|LTD|CO)\b','',s).replace(' ','')
piids=collections.defaultdict(list);ueis=collections.defaultdict(set);names=collections.defaultdict(set);broad=set()
for l in open(OUT/'sbir_screened_candidates.jsonl'):
 r=json.loads(l);broad.add(r['piid_norm'])
for fn in ['sbir_current.jsonl.gz','sbir.jsonl.gz']:
 for n,l in enumerate(gzip.open(B/'data/normalized'/fn,'rt'),1):
  r=json.loads(l); ids=json.loads(r.get('identifiers_json') or '{}');p=norm(r.get('award_key'))
  a={k:r.get(k) for k in ['source','document_id','title','text','entity_name','entity_key','action_date','fiscal_year','award_key','source_url','money_json']};a['ids']=ids;a['source_row']=n
  piids[p].append(a)
  u=ids.get('UEI')
  if u and u!='nan':ueis[norm(u)].add(p)
  if r.get('entity_name'):names[en(r['entity_name'])].add(p)
c=sqlite3.connect('file:'+str(B/'data/financial_actions.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
n=c.execute('select count(*) from source_rows').fetchone()[0]
if n!=712186:raise RuntimeError(f'Financial table incomplete: {n} rows, expected 712186')
exact=[];recipient=[];counts=collections.Counter();seen=set()
for x in c.execute('select row_number,transaction_key,award_key,award_id,award_type,entity_key,entity_name,action_date,action_obligation_usd,obligation_cents,source_url,description_text,source_json from source_rows'):
 r=dict(x);counts['financial_rows_scanned']+=1;p=norm(r['award_id']);matches=piids.get(p,[])
 # exact PIID coverage includes all years, record-year sums are separate
 if matches:
  r['matching_sbir_rows']=len(matches);r['sbir_entities']=sorted(set(a['entity_name'] for a in matches));r['sbir_titles']=sorted(set(a['title'] for a in matches));r['broad_sbir_hit']=p in broad;r['match_kind']='exact_piid';exact.append(r)
  counts['exact_financial_rows']+=1
  if r['action_date'] and r['action_date']>='2024-01-01': counts['exact_financial_rows_2024_on']+=1
 u=norm(r['entity_key']);name=en(r['entity_name']);ps=ueis.get(u,set())|names.get(name,set())
 if ps and r['action_date'] and r['action_date']>='2024-01-01':
  z=dict(r);z['match_kind']='recipient_uei' if u in ueis else 'normalized_recipient_name';z['recipient_sbir_piids']=sorted(ps);z['broad_sbir_piids']=sorted(ps&broad);z['exact_piid_in_sbir']=p in piids;recipient.append(z);counts['recipient_financial_rows_2024_on']+=1
  if ps&broad:counts['broad_recipient_financial_rows_2024_on']+=1
for fn,rows in [('exact_piid_join.jsonl',exact),('recipient_potential_followons.jsonl',recipient)]:
 with (OUT/fn).open('w') as f:
  for r in rows:f.write(json.dumps(r)+'\n')
counts['all_sbir_source_rows']=sum(map(len,piids.values()));counts['all_sbir_distinct_normalized_piids']=len(piids);counts['distinct_exact_matched_piids']=len(set(norm(r['award_id']) for r in exact));counts['distinct_potential_recipient_followon_piids']=len(set(norm(r['award_id']) for r in recipient if not r['exact_piid_in_sbir']));counts['distinct_broad_recipient_followon_piids']=len(set(norm(r['award_id']) for r in recipient if not r['exact_piid_in_sbir'] and r['broad_sbir_piids']));
(OUT/'join_audit.json').write_text(json.dumps(dict(counts),indent=2));print(json.dumps(dict(counts),indent=2))
# compact potential follow-on register: grouped once per award; transaction sums are not award ceilings
aw=collections.defaultdict(list)
for r in recipient:
 if r['broad_sbir_piids']:aw[r['award_key']].append(r)
with (OUT/'followon_register.tsv').open('w') as f:
 f.write('entity\taward_id\texact_sbir\t2024_on_obligation_sum\taction_count\tmin_date\tmax_date\tmatch\turl\n')
 for k,rs in sorted(aw.items(),key=lambda kv:sum(int(x['obligation_cents'] or 0) for x in kv[1]),reverse=True):
  r=rs[-1]; f.write('\t'.join(str(x) for x in [r['entity_name'],r['award_id'],r['exact_piid_in_sbir'],round(sum(int(x['obligation_cents'] or 0) for x in rs)/100,2),len(rs),min(x['action_date'] for x in rs),max(x['action_date'] for x in rs),r['match_kind'],r['source_url']])+'\n')
