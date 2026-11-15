import csv,re,collections,json,pathlib
D=pathlib.Path('/tmp/patent-coverage/ep-screen');rows=list(csv.DictReader(open('/tmp/patent-coverage/expanded/ep-native-union.csv')))
priority=re.compile(r'FRIEND/FOE|FIRING CUTOUT|HUMAN DETECTION|AUTHORISING AND EXECUTING|WEAPON CONTROL|WEAPON SYSTEM AND METHOD FOR OPERATING|LESS LETHAL SHOOTING|WEAPON MANAGEMENT|WEAPON SYSTEM CONTROL|AUTONOMOUS WEAPON|WEAPON SAFETY SYSTEM|SAFETY ASSEMBLY|WEAPON EMERGENCY STOP|WEAPON AUTHORISATION|PREVENTING FIRING|OPTIONALLY AUTHORISING FIRING|DEAD MAN|CORRUPTION OF NEURAL|HUMAN SUPERVISION|NEURAL NETWORK SUITABLE')
secondary=re.compile(r'AUTONOM|ROBOT|UNMANNED|MILITARY|WEAPON|FIRING|FIRE CONTROL|TARGET IDENTIF|SAFETY CONTROL|SAFE PATH|RESTRICT|FAILSAFE|FAIL-SAFE|COLLATERAL|SAFE OPERATION|SAFE TRAJECTORY')
for r in rows:
 t=r['title'].upper();r['screen_category']='priority-title-candidate' if priority.search(t) else 'secondary-title-candidate' if secondary.search(t) else 'lower-priority-unreviewed';r['review_basis']='deterministic title pattern only; not relevance conclusion';r['publication_id']=r['publication'].split('/publication/')[1].replace('/-','').replace('/','')
with open(D/'803-title-triage.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
c=collections.Counter(r['screen_category'] for r in rows);(D/'screen-counts.json').write_text(json.dumps(c,indent=2));print(c)
for r in rows:
 if r['screen_category']=='priority-title-candidate': print(r['publication_id'],r['title'])
