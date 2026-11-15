import csv,json,hashlib
from pathlib import Path
rows=list(csv.DictReader(open('uspto_multishard_metadata_queue.csv')))
selected=[x for x in rows if x['automatic_queue']=='priority_claim_read']+[x for x in rows if x['automatic_queue']=='secondary_title_signal'][:40]
notes={
'US11415383B2':('claims inspected','Claim 1: firing lock released only with validated clearance signal in permitted orientation/area. Description situates this in shooting ranges. Concrete restraint, not demonstrated battlefield/AI ethics.'),
'US11898812B2':('claims inspected','Claim 1: human vital-sign detection in aiming direction controls firing lock. Dependent 2 permits unlock when none detected. Direct human-protection proposal for portable weapons; not military adoption or effectiveness evidence.'),
'US12553679B2':('claims inspected','Claim 1: direction-based locking/unlocking against preset target direction values; dependent 3 operator authentication. Same title as US11898812B2, but distinct claim content: do not import its human-detection requirement.'),
'US20220412682A1':('selected claim inspected','Claim 1 concerns physical safety/disconnection mechanism. Mechanical safing, not a demonstrated autonomous protected-target decision. Other claims not comprehensively assessed.'),
'US20230037964A1':('claims and selected description inspected','Claims 5/7 provide AI-activated disabling; 8/11 target classifications and lethality modes; 14 non-contact mode. No universal no-shoot-unarmed requirement established. Description permits lethal mode for unarmed targets in one passage but later gives a protective example; avoid clean universal-protection paraphrase. Grant US11933559B2 not claim-equated.'),
'US20240240894A1':('selected claim inspected','Claim 1 gates firing on high-probability hit indication. This is precision/aiming gating, not express civilian/non-target exclusion. Grant version not claim-equated.'),
'US20240125919A1':('selected claims inspected','Claims 1/8 classify radar objects/noise; dependent 10 autonomous vehicle. GM Cruise metadata. No weapon firing restriction established from inspected claims; target is generic sensing term.'),
'US20240419962A1':('selected claims inspected','Claim 1 and apparatus 8 optimize allocation of object-detection processing windows. Raytheon metadata alone does not turn detection efficiency into ethical restraint; no protected-target interlock established.'),
'US11231252B2':('selected claims inspected','Independent claim 14 expressly excludes selecting human targets. Dependent 3 similarly excludes humans; 6 disables firing at an identified human set. But independent 1 lacks universal human exclusion, and dependent 5 permits firing at identified human set. Distinguish separately claimed configurations.'),
'US12631428B2':('selected claims inspected','Independent claims 1/6 and dependent 2/7 concern automated selection/aiming/firing with human or nonhuman among target types. Reviewed clauses do not establish protected-category exclusion. Remaining claims require review; do not inherit safeguards from other Bilbrey/Sitrick patents.'),
'US11326847B1':('text retrieval failed','Google Patents open failed in this pass; no substantive exclusion.'),
'US20260328926A1':('text retrieval failed','Google Patents open failed in this pass; no substantive exclusion.'),
'US12416472B1':('text retrieval failed','Google Patents open failed in this pass; no substantive exclusion.'),
'US12663229B1':('text retrieval failed','Google Patents open failed in this pass; no substantive exclusion.')}
prior='US20230056472A1 US12007188B2 US12321773B1 US20240085134A1 US20240384959A1 US20250314457A1 US11913738B2 US12066263B2 US11262165B2 US12467704B2 US20230288925A1 US20260085911A1 US11499807B2 US12253603B2 US12292263B2'.split()
out=[]
for r in selected:
 i=r['normalized_document_id']; status,note=notes.get(i,('metadata only; claims pending','No inference of actual claim content from title.'))
 if i in prior and i not in notes:status='prior claim inspection reported; not repeated';note='See existing claims addenda and source-agent report; not newly independently rechecked here.'
 if status.startswith('metadata'):
  t=r['Title'].lower()
  if any(x in t for x in ['semi-automatic','semiautomatic','production','cartridge','charging handle']):note='Metadata suggests mechanical/manufacturing lane rather than AI restraint. Remains unexcluded pending text review.'
  elif any(x in t for x in ['automatic weapon','automated human','human transported','smart-gun']):note='Related-title weapons/control record; must check this exact version. Cannot inherit protection claims from a similarly titled grant/application.'
 out.append(dict(publication=i,tier=r['automatic_queue'],title=r['Title'],native_family_id=r['Family ID'],review_status=status,assessment=note,url=r['source_link']))
fields=list(out[0]);f=open('patent_priority_secondary_review_77.csv','w');w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out);f.close()
Path('patent_priority_secondary_review_notes.json').write_text(json.dumps(notes,indent=2))
print(len(out),{s:sum(x['review_status']==s for x in out) for s in set(x['review_status'] for x in out)})
