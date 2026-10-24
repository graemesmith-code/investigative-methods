import json,collections,csv
from pathlib import Path
B=Path(__import__('os').environ.get('F2_ROOT', str(Path(__file__).resolve().parents[1])));O=B/'lane1';c=collections.Counter();recent=collections.Counter();rows=[]
for line in (O/'candidate_register.jsonl').open():
 r=json.loads(line);ms=r['keyword_matches'].get('transition',[])
 for m in ms:c[m]+=1;recent[m]+=int(r['net_obligation_2024_2026_cents']>0)
 if set(ms)&{'apfit','rder','diu','phase iii','phase 3','afwerx','sofwerx','navalx'}:rows.append({'selection_id':r['selection_id'],'award_id':r['award_id'],'award_key':r['award_key'],'names':' | '.join(r['entity_names']),'markers':','.join(ms),'recent_cents':r['net_obligation_2024_2026_cents'],'score':r['screen_score']})
(O/'transition_marker_counts.json').write_text(json.dumps({'all_awards':dict(c),'awards_positive_2024_2026_obligations':dict(recent)},indent=2))
with (O/'transition_markers.tsv').open('w') as f:
 w=csv.DictWriter(f,rows[0].keys(),delimiter='\t');w.writeheader();w.writerows(rows)
