import csv,re,glob,collections,json,pathlib,hashlib
files=sorted(glob.glob('uspto_broad_20??.csv'))+['uspto_F41A1708_20211115_20261115.csv','uspto_control_complement.csv','uspto_protection_language.csv','uspto_software_2021_2023.csv','uspto_software_2024_2026.csv']
rules={
 'explicit_restraint':r'deconflict|cutout|cut out|no.fire|safety.critical|safe.*engagement|engagement.*safe|rules of engagement|ethical|friend.*fire|human.*control|authorization|authorizing|disengag|stand.off.*limit',
 'autonomous_weapon':r'(autonom|automat|artificial intelligence|\bAI\b|neural|machine learning).*(weapon|gun|firearm|munition|target)|(weapon|gun|firearm|munition|target).*(autonom|automat|artificial intelligence|\bAI\b|neural|machine learning)',
 'control_safety':r'safety|safe system|interlock|inhibit|override|abort|safeguard|geofenc|containment|supervis|assurance|human|control|threat|target|arming|disarming',
 'weapon_title':r'weapon|missile|munition|firearm|\bgun\b|firing|combat|military|ordnance',
 'common_hardware':r'suppressor|silencer|barrel|magazine|bolt |breech|cartridge|primer|holster|sling|grip|mount|stock|recoil|chamber|clean|battery|illumination',
 'training':r'training|simulat|sport|hunting|toy|game|entertainment'}
docs={};inputs=[]
for f in files:
 rs=list(csv.DictReader(open(f,encoding='utf-8-sig')));inputs.append({'file':f,'rows':len(rs),'family_ids':len({r['Family ID'] for r in rs}),'sha256':hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()})
 for r in rs:
  k=re.sub(r'\s+','',r['Document ID'])
  if k not in docs:docs[k]={'row':r,'files':[]}
  docs[k]['files'].append(f)
out=[]
for k,v in docs.items():
 r=v['row'];t=r['Title'];flags=[n for n,p in rules.items() if re.search(p,t,re.I)]
 score=12*('explicit_restraint'in flags)+7*('autonomous_weapon'in flags)+3*('control_safety'in flags)+2*('weapon_title'in flags)-2*('common_hardware'in flags)-2*('training'in flags)
 cp=r['CPCI']+';'+r['CPCA']
 if 'F41A17/08' in cp:score+=3;flags+=['directional_safety_CPC']
 if 'F41H7/005' in cp:score+=2;flags+=['autonomous_armed_platform_CPC']
 q='priority_claim_read' if score>=10 else 'secondary_title_signal' if score>=3 else 'weak_title_signal_unreviewed'
 o={**r,'normalized_document_id':k,'source_exports':';'.join(v['files']),'rule_score':score,'rule_flags':';'.join(flags),'automatic_queue':q,'assessment_basis':'Deterministic title/CPC routing only; not human full-record relevance screening','abstract_read':'no','claims_read_in_this_export_pass':'no','source_link':'https://patents.google.com/patent/'+k+'/en'};out.append(o)
inspected=set('US20230056472A1 US11385007B2 US20250314457A1 US12007188B2 US20240384959A1 US12253603B2 US12066263B2 US11262165B2 US12467704B2 US20260085911A1 US20240377833A1 US20240345586A1 US11913738B2 US11420655B2 US12321773B1'.split())
for r in out:
 if r['normalized_document_id'] in inspected:
  r['claims_read_in_this_export_pass']='selective clause inspection; see addenda, not full prosecution review'
out.sort(key=lambda r:(-r['rule_score'],r['normalized_document_id']))
with open('uspto_multishard_metadata_queue.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
fams=collections.defaultdict(list)
for r in out:fams[r['Family ID']].append(r['normalized_document_id'])
pathlib.Path('uspto_multishard_family_groups.json').write_text(json.dumps(fams,indent=2))
s={'inputs':inputs,'raw_rows':sum(x['rows'] for x in inputs),'unique_document_ids':len(docs),'unique_uspto_export_family_ids':len(fams),'duplicate_document_rows':sum(x['rows'] for x in inputs)-len(docs),'queue_counts':dict(collections.Counter(r['automatic_queue'] for r in out)),'rules':rules,'limitations':['Annual files are family-filtered within each year, not all underlying publications.','Family IDs only compared within USPTO exports; no cross-database equality assumed.','Regex routing of all rows is not completed abstract/claim screening; weak signal is NOT excluded.','Some representative versions recur across exports; exact document dedup only. No title-based merging.','Query full-text hits may involve incidental words. Ranking does not validate safeguards.']}
pathlib.Path('uspto_multishard_screen_manifest.json').write_text(json.dumps(s,indent=2))
print(json.dumps({k:v for k,v in s.items() if k not in ('inputs','rules')},indent=2))
for r in out[:75]:print(r['rule_score'],r['Document ID'],r['Title'])
