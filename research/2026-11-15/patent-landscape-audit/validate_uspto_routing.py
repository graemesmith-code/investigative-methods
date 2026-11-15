import csv,random,json,collections,pathlib
rows=list(csv.DictReader(open('uspto_multishard_metadata_queue.csv')));rng=random.Random(20261115);sample=[]
for group in ['weak_title_signal_unreviewed','secondary_title_signal']:
 sample+=rng.sample(sorted([r for r in rows if r['automatic_queue']==group],key=lambda r:r['normalized_document_id']),30)
sample += [r for r in rows if r['automatic_queue']=='priority_claim_read']
weak=[
'General software-testing recommendations; possible assurance analogue, no weapon-specific title',
'Gunshot detection, not firing constraint',
'Physical ammunition component',
'Biometric performance assessment; possible human-state analogue, scope unknown',
'Responsible-AI/LLM governance; general assurance rather than established weapon safeguard',
'Promote adjacent assurance: adversarial robustness, claim1 inspected; not a firing interlock',
'Physical bolt assembly',
'Promote adjacent assurance: communications-denied coordination; claim1 inspected, no engagement veto established',
'Predictive weapon maintenance; not target restraint',
'Lighted projectile hardware',
'Breaching/tamping material',
'Visual-search retrieval unrelated on available metadata',
'Drone position regulation; retain possible containment analogue',
'Software-performance evaluation; retain assurance lead',
'Fuze initiator; mechanical safing relevance uncertain',
'Failure detection; retain assurance analogue',
'Formal drone verification; promote assurance lead for later text reading',
'Armor fasteners',
'Projectile construction',
'Training device rather than operational constraint',
'Perforating-gun detonator; industrial rather than combat use indicated',
'Entry management ambiguous; retain unknown',
'Pyrotechnic initiation; physical safing relevance uncertain',
'Optical drone guidance; retain for safeguard-in-description check',
'Armor manufacture',
'Desk/physical shielding',
'Cartridge ejector',
'Industrial perforating gun subassembly',
'Magazine security accessory; access-control adjacent',
'Machine-gun clutch hardware']
secondary=[
'UAV recognition/threat management; inspect restraint versus detection',
'Motor ignition safety; physical safing adjacent',
'Bilbrey linked automation cluster; inspect exact claims, not merged solely by title',
'Site threat detection; surveillance not established restraint',
'Electronic threat assessment ambiguous; retain',
'Access/reunification unrelated on metadata',
'Generic sensing control: insufficient title, retain unknown',
'Ballistic vest physical protection',
'Avalanche explosives payload safety; adjacent non-combat analogy',
'Access/reunification unrelated on metadata',
'Promote protected-area constraint: actual dependent13/14 read; hospital example is description',
'Air-drop package hardware',
'Optical-fiber safety signal ambiguous; retain',
'Counter-UAV neutralization; inspect constraints versus attack capability',
'Geofence/intrusion neutralization; inspect what prevents harm rather than assume safeguard',
'Camera/electrical weapon; less-lethal targeting analogue',
'Marker detection, potential friend-ID input not restraint by itself',
'Riot-shield physical linkage',
'Pest control rather than military targeting',
'Bilbrey aim/munition-selection cluster; claim-specific limits unknown',
'Ballistic vest physical protection',
'Actual claims1–7 inspected: guidance/assessment; no direct protective constraint found in these claims',
'Threat assessment ambiguous; retain',
'Smart firearm safety: access/handling analogue pending text',
'Trigger mechanics; no AI restriction established',
'Generic firearm safety mechanism; retain uncertain',
'Environmental-control module, not engagement control on title',
'Human mental-state processing; potential human-performance assurance analogue',
'Recoil inhibition, not firing inhibition; lexical false positive',
'Coordinated target tracking; target restraint unverified']
assert len(weak)==len(secondary)==30
claim_ids=set('US11972335B2 US12055951B2 US20230392899A1 US11499807B2 US20230288925A1 US20240085134A1'.split())
priority_notes={
'US20230288925A1':'Actual claim1 is user/license-based UAV software authorization; downgrade adjacent access licensing, not engagement permission',
'US20240085134A1':'Actual claim1 is thermal insignia recognition and warning display; no mandatory firing inhibition',
'US20240125919A1':'Radar target-classification title with GM Cruise applicant: possible vehicle perception, not established weapon safeguard',
'US20240419962A1':'Detection-configuration optimization: possible performance rather than restraint; inspect text',
'US12321773B1':'Earlier claim inspection: software isolation/reliability, not engagement governor',
'US11913738B2':'Earlier claim inspection: authorized-user access control, not target approval',
'US12066263B2':'Earlier claim inspection: dependent2 human-firing prohibition; independent1 broader',
'US11262165B2':'Earlier claim inspection: dependent human-set restrictions; other alternatives allow human targeting',
'US12467704B2':'Earlier claim inspection: AI safety disabling in claim1, independent5 broader conversation claim',
'US20230056472A1':'Earlier claim inspection: ML non-target maps; dependent5/12/19 launch inhibition',
'US12007188B2':'Earlier claim inspection: automatic firing and optional less-lethal settings, not demonstrated ethics',
'US20240384959A1':'Earlier claim inspection: proposed AI locking, unvalidated individual application',
'US20250314457A1':'Earlier claim inspection: no-fire computation/display, actual interlock not demonstrated',
'US20260085911A1':'Earlier claim inspection: user target designation/authorization, deconfliction not explicit inhibition',
'US20260328926A1':'Direct laser deconfliction title; native-agent inspection separate; retain high priority'}
for i,r in enumerate(sample):
 note=weak[i] if i<30 else secondary[i-30] if i<60 else priority_notes.get(r['normalized_document_id'],'Metadata reviewed: automatic-weapon/AI-gun candidate, often related Bilbrey/Sitrick or Hafen versions; exact version claims still needed. Do not treat shared title or protection in another grant as proof for this version.')
 r['validation_row']=i+1;r['manual_metadata_assessment']=note;r['new_claim_text_checked_in_validation']='yes_selective_passages' if r['normalized_document_id'] in claim_ids else 'no';r['sampling_seed']=20261115;r['validation_scope']='Metadata review only unless explicitly marked selective claim passages; not full legal/prosecution review'
with open('uspto_routing_validation.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(sample[0]));w.writeheader();w.writerows(sample)
pathlib.Path('uspto_routing_validation_sample.json').write_text(json.dumps(sample,indent=2))
print('reviewed metadata',len(sample),'new selective claim reads',sum(r['new_claim_text_checked_in_validation'].startswith('yes') for r in sample))
