import os
import gzip,json,re,collections,hashlib,pathlib
ROOT=pathlib.Path(os.environ.get('F2_ROOT', '.')).resolve(); OUT=ROOT/'lane3'; DATA=ROOT/'data/normalized'
patterns={
'flagship':r'\b(RACER|ANSR|LINC|TIAMAT|MANTA RAY|DCIST|NOMARS|SEA TRAIN|REMA|ALPHAICE|VENOM)\b|air combat evolution|artificial intelligence.{0,6}reinforcements|control of revolutionary aircraft|robotic autonomy in complex|assured neuro.?symbolic|learning introspective control|transfer from imprecise|collaborative operations in denied|offensive swarm|aircrew labor in.cockpit automation|OFFSET.{0,10}swarm',
'ai':r'\bAI\b|artificial intelligence|machine learning|deep learning|reinforcement learning|neural|learned|learning|autonom|robot|unmanned|uncrewed|swarm',
'physical':r'vehicle|aircraft|drone|ground|maritime|underwater|undersea|weapon|munition|seeker|missile|target recognition|breach|minefield|fire control|combat|tactical|electronic warfare|counter.?uas|counter.?uav|flight|maneuver|manoeuv',
'transition':r'transition|prototype|demonstrat|experiment|field.test|flight.test|testbed|integrat|phase iii|phase 3|manufactur|deploy|production|operational',
'vendor':r'overland|episy?sci|episys|physicsai|heron systems|shield ai|scientific systems|aurora flight|raytheon|lockheed|northrop|anduril|forterra|dual.?ity|applied intuition|textron|leidos|general atomics|calspan|saronic|peraton|soartech|soar technology'
}
rx={k:re.compile(v,re.I) for k,v in patterns.items()}
summary={'method':'All rows parsed; regex across all available title, text, text_page_excerpt and entity_name fields. Triage score is a discovery aid, not an inclusion decision. Assistance descriptions are often title-only, not full technical abstracts. Opportunity rows are funding intent, not award proof. Budget values never treated as obligations.','patterns':patterns,'files':{}}
for name in ['darpa_pb2025_programs.jsonl.gz','grants.jsonl.gz','usaspending_dod_research_grants.jsonl.gz']:
 stats=collections.Counter(); candidates=[]; counts=collections.Counter(); seen=set();
 with gzip.open(DATA/name,'rt') as f:
  for n,line in enumerate(f,1):
   r=json.loads(line); stats['rows']+=1
   text=' '.join(str(r.get(k) or '') for k in ['title','text','text_page_excerpt','entity_name'])
   flags={k:bool(x.search(text)) for k,x in rx.items()}
   for k,v in flags.items(): stats[k+'_matches']+=v
   broad=flags['flagship'] or (flags['ai'] and flags['physical'])
   prioritized=flags['flagship'] or (flags['ai'] and flags['physical'] and (flags['transition'] or flags['vendor']))
   stats['broad_matches']+=broad; stats['prioritized_matches']+=prioritized
   if broad:
    score=6*flags['flagship']+2*flags['ai']+2*flags['physical']+2*flags['transition']+2*flags['vendor']
    candidates.append({'source_file':name,'line':n,'flags':flags,'score':score,'row':r})
   seen.add(r.get('award_key') or r.get('document_id'))
 stats['unique_award_or_document_keys']=len(seen)
 candidates.sort(key=lambda x:(-x['score'],x['line']))
 dest=OUT/(name.replace('.jsonl.gz','')+'_matches.jsonl')
 with open(dest,'w') as f:
  for r in candidates:f.write(json.dumps(r)+'\n')
 with open(OUT/(name.replace('.jsonl.gz','')+'_triage.tsv'),'w') as f:
  f.write('score\tline\tflags\tdate\taward_key\tentity\ttitle\n')
  for c in candidates:
   r=c['row'];f.write('\t'.join(str(x).replace('\t',' ').replace('\n',' ') for x in [c['score'],c['line'],','.join(k for k,v in c['flags'].items() if v),r.get('action_date',''),r.get('award_key',''),r.get('entity_name',''),r.get('title','')])+'\n')
 summary['files'][name]={'counts':dict(stats),'compressed_sha256':hashlib.sha256((DATA/name).read_bytes()).hexdigest(),'matches_file':str(dest)}
with open(OUT/'screen_summary.json','w') as f:json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
