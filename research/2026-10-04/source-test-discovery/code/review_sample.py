import json,random,collections
from normalize import OUT
from build import csvwrite

def sample(path,prefix):
 rows=[json.loads(x) for x in path.read_text().splitlines()]; byid={r['test_id']:r for r in rows}; chosen={}; rng=random.Random(20261004)
 def take(candidates,bucket):
  n=0
  for r in candidates:
   if r['test_id'] in chosen:continue
   chosen[r['test_id']]=bucket;n+=1
   if n==8:break
 take(rows,'highest_ranked')
 freq=collections.Counter(r['mechanism'] for r in rows)
 take(sorted(rows,key=lambda r:(-freq[r['mechanism']],r['test_id'])),'largest_near_duplicate_clusters')
 take(sorted(rows,key=lambda r:(r['join_confidence_score'],r['test_id'])),'risky_identity_temporal_legal')
 take(sorted(rows,key=lambda r:(freq[r['mechanism']],r['test_id'])),'sparse_mechanisms')
 shuffled=rows[:];rng.shuffle(shuffled);take(shuffled,'seeded_random_remaining')
 result=[]
 for tid,bucket in chosen.items():
  r=byid[tid]
  result.append(dict(test_id=tid,stratum=bucket,source_pair=r['source_a']+' → '+r['source_b'],mechanism=r['mechanism'],join=r['join_status'],source_b_fields='; '.join(r['source_b_fields']),inference=r['interesting_outcome'],review_status='pending_model_review',notes=''))
 csvwrite(OUT/(prefix+'review-sample.csv'),result)
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':
 import sys
 early='early' in sys.argv
 sample(OUT/('checkpoints/early-tests.jsonl' if early else 'tests.jsonl'),'checkpoints/early-' if early else '')
