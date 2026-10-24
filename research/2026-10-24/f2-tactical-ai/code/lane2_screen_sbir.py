import os
import json,gzip,re,collections,hashlib
from pathlib import Path
base=Path(os.environ.get('F2_ROOT', '.')).resolve()/'lane2'; source=base.parent/'data/normalized'
patterns={
'ai':r'\b(?:artificial intelligence|machine learning|deep learning|neural|reinforcement learning|learned|self-supervised|computer vision|AI/ML|deep reinforcement|vision.language|perception)\b',
'autonomy':r'\b(?:autonom\w*|robot\w*|swarm\w*|unmanned|uncrewed|collaborative combat|attritable|multi.agent|UGV|UUV|USV|UAV|UAS|CCA)\b',
'weapon':r'\b(?:terminal guidance|seeker|munition\w*|lethal\w*|loitering|target recognition|ATR|target acquisition|targeting|weapon\w*|fires|counter.UAS|counter.drone|electronic attack|jamm\w*|breach\w*|minefield|mine countermeasure\w*|mine warfare|kill chain)\b',
'contested':r'\b(?:GPS.denied|GNSS.denied|contested|denied navigation|off.road|spectrum|radio.frequency|RF|electronic warfare|damage|terrain|navigation)\b',
'physical':r'\b(?:test\w*|demonstrat\w*|integrat\w*|platform\w*|aircraft|drone\w*|vehicle\w*|missile\w*|torpedo\w*|soldier\w*|warfighter\w*|fleet|field\w*)\b',
'follow':r'\b(?:Phase III|Phase II enhancement|sequential|TACFI|STRATFI|transition\w*|APFIT|RDER|operational|deploy\w*)\b',
}
rx={k:re.compile(v,re.I) for k,v in patterns.items()}
rows=[];counts={};seen=set();dup=0
for filename in ('sbir_current.jsonl.gz','sbir.jsonl.gz'):
 counts[filename]={'rows':0,'broad':0,'ai_autonomy_weapon':0,'phase_ii_broad':0,'all_text_chars':0}
 for l in gzip.open(source/filename,'rt'):
  r=json.loads(l); counts[filename]['rows']+=1
  ids=json.loads(r.get('identifiers_json') or '{}');r['ids']=ids
  t=' '.join(str(r.get(k) or '') for k in ('title','text','entity_name'));counts[filename]['all_text_chars']+=len(t)
  matches={k:sorted(set(m.group(0).lower() for m in p.finditer(t))) for k,p in rx.items()};r['f2_matches']=matches
  broad=bool((matches['ai'] and (matches['autonomy'] or matches['weapon'] or matches['contested'])) or (matches['autonomy'] and matches['weapon']))
  if not broad:continue
  counts[filename]['broad']+=1
  if matches['ai'] and matches['autonomy'] and matches['weapon']:counts[filename]['ai_autonomy_weapon']+=1
  if ids.get('Phase')=='Phase II':counts[filename]['phase_ii_broad']+=1
  yr=int(r.get('fiscal_year') or 0)
  score=bool(matches['ai'])*4+bool(matches['autonomy'])*3+bool(matches['weapon'])*4+bool(matches['contested'])*2+bool(matches['physical'])+bool(matches['follow'])*2+(yr>=2024)*2+(ids.get('Phase')=='Phase II')*2
  r['f2_score']=score;r['piid_norm']=re.sub('[^A-Z0-9]','',str(r.get('award_key') or '').upper());r['source_file']=filename
  key=(r['piid_norm'],r['title'],r['entity_name'])
  r['f2_duplicate_project_key']=key in seen
  if key in seen:dup+=1
  seen.add(key);rows.append(r)
rows.sort(key=lambda r:(r['f2_score'],str(r.get('fiscal_year') or '')),reverse=True)
with (base/'sbir_screened_candidates.jsonl').open('w') as f:
 for r in rows:f.write(json.dumps(r)+'\n')
with (base/'screen_audit.json').open('w') as f:json.dump({'patterns':patterns,'counts':counts,'broad_total':len(rows),'unique_project_keys':len(seen),'cross_and_within_duplicates':dup,'source_sha256':{fn:hashlib.sha256((source/fn).read_bytes()).hexdigest() for fn in counts}},f,indent=2)
with (base/'candidate_register.tsv').open('w') as f:
 f.write('score\tyear\tphase\tentity\tpiid\ttitle\tduplicate\n')
 for r in rows:f.write('\t'.join(str(x).replace('\t',' ') for x in (r['f2_score'],r.get('fiscal_year'),r['ids'].get('Phase'),r['entity_name'],r['piid_norm'],r['title'],r['f2_duplicate_project_key']))+'\n')
print(json.dumps(counts,indent=2));print('broad',len(rows),'unique',len(seen),'duplicate',dup)
for r in rows[:180]:
 if not r['f2_duplicate_project_key']:print(r['f2_score'],r['fiscal_year'],r['ids'].get('Phase'),r['entity_name'],r['piid_norm'],r['title'],sep=' | ')
