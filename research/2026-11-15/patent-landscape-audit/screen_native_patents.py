import csv,json,collections,hashlib
from pathlib import Path
p=Path('uspto_F41A1708_20211115_20261115.csv')
rows=list(csv.DictReader(p.open(encoding='utf-8-sig')))
# Human-authored metadata judgments. The script validates and joins these judgments;
# it does not pretend to algorithmically determine technical relevance.
notes={
1:('candidate','high','Laser-weapon air/space deconfliction explicitly named; examine protected objects and actual inhibit conditions.'),
2:('adjacent','medium','Hunting assistance, not demonstrated autonomous military safeguard; check warning versus enforcement.'),
3:('adjacent','medium','Shooter safety warning; no autonomous or military use established.'),
4:('candidate','high','Battlefield command/control plus mine and safing classes; determine human permission and loss-of-link rules.'),
5:('adjacent','low','IR marker detection; possible identification input, not itself established weapon restraint.'),
6:('candidate','high','Human-detection sighting control; determine whether it merely hides aiming graphics or inhibits firing.'),
7:('adjacent','low','Safety/training aid; operational safeguards not established.'),
8:('candidate','high','Navy geodetic deconfliction plus directed-energy class; inspect protected-volume and engagement inhibition claims.'),
9:('candidate','high','Computer-vision human detection/warning; distinguish warning from enforceable inhibition and hunting from military use.'),
10:('candidate','high','Explicit restriction to less-lethal shooting; test claimed limits and platform scope rather than assuming battlefield deployment.'),
11:('exclude_provisional','low','Training apparatus by title/classification; retain for audit, not current operational-safeguard priority.'),
12:('adjacent','medium','Aiming with built-in training; safety logic may be training-only.'),
13:('candidate','high','Explicit AI/human gun integration with safety classification; inspect division of authority and enforced refusal.'),
14:('uncertain','medium','Selective disabling with fuze/explosive classes; insufficient metadata to tell remote restriction from component safety.'),
15:('adjacent','low','Location warnings with personal-alarm classes; no enforced weapon control established.'),
16:('exclude_provisional','low','Magazine locking; no AI or autonomous-targeting indication in exported metadata.'),
17:('adjacent','medium','Trigger control by Smart Shooter; determine whether safety or aiming performance, and whether independent inhibition exists.'),
18:('adjacent','low','Personal-defense tracking; no autonomous military safeguard established.'),
19:('candidate','high','Automatic acquisition/shooting with ML and vision classes; inspect protected-target exclusions rather than infer ethics.'),
20:('candidate','high','AI smart gun with safety classification; investigate actual logic, not AI branding alone.'),
21:('candidate','high','Explicit friendly-fire prevention; identify whether warning or enforced inhibition and whether identification depends on markers.'),
22:('adjacent','medium','Camera/conducted-electrical-weapon cooperation; likely less-lethal domain, actual restraint versus aiming needs inspection.'),
23:('adjacent','medium','Radio direction finder/identifier may support friend identification; no independent firing restraint established.'),
24:('candidate','high','Artillery guidance plus safety class; inspect no-fire sectors and protected-area calculations.'),
25:('exclude_provisional','low','Combat training system; not presently evidence of operational safeguards.'),
26:('adjacent','low','Synchronized marker flashes; potential identification input, not established restraint.'),
27:('adjacent','low','RFID article detection in security zone; autonomous targeting safeguard not demonstrated.'),
28:('adjacent','low','Training and firearm-use safety; title insufficient to distinguish real-time restraint.'),
29:('adjacent','medium','Directed-energy safety assembly with training classes; do not equate training safety with combat guardrails.'),
30:('uncertain','medium','Selective disabling/explosives; unclear if relevant to autonomous decision restraint.'),
31:('candidate','high','Explicit ML-aided firing cutout; inspect whether protects own platform, bystanders or both, and whether runtime enforced.'),
32:('adjacent','medium','Weapon-event detection; monitoring need not mean prevention.'),
33:('uncertain','medium','Generic firearm safety control, no AI/military indication; inspect before inclusion or exclusion.'),
34:('candidate','high','Projectile-launcher operation monitoring with neural-network classes; test whether monitoring constrains launch.'),
35:('adjacent','low','Weapon safety drive mechanism; no AI/autonomous function indicated.'),
36:('adjacent','medium','Mass-shooting prevention/smart gun; civilian analogue, not military autonomous-safeguard proof.'),
37:('uncertain','medium','Smart ammunition and safing classes; metadata does not establish decision or protected-target criteria.'),
38:('uncertain','medium','Smart trigger too generic to classify as AI safeguard without text.'),
39:('adjacent','medium','Gun-violence reduction system; civilian safety analogue, mechanism unverified.'),
40:('adjacent','medium','Event detection/monitoring not necessarily enforced restraint; related title to row32 but different USPTO Family ID.'),
41:('adjacent','medium','Firearm regulation with location/access-control classes; plausible geofencing analogue, military scope unverified.'),
42:('adjacent','medium','Weapon safety with range/position classes; may be training environment, needs text.'),
43:('adjacent','low','Portable-weapon/crossbow safety control, no autonomous military indication.'),
44:('candidate','high','Northrop area denial and communications latency with weapon/mine classes; inspect authorization freshness and lost communications.'),
45:('adjacent','medium','Discharge prevention with human-recognition class; civilian analogue pending text.'),
46:('candidate','high','Dual-mode weapon-mounted fire control; inspect operator versus automatic authority and safety enforcement.'),
47:('candidate','high','Mitsubishi threat coping plus counter-aircraft/vision classes; inspect collateral protections and firing decision constraints.'),
48:('adjacent','medium','Restrictive/selective smart-gun control; actual military/autonomous applicability unverified.'),
49:('candidate','high','Automatic target-selection weapon; inspect claimed exclusions, authorization and abort conditions.'),
50:('candidate','high','Linked automatic weapon sensing/aim control; inspect shot-selection constraints and human authority.'),
51:('candidate','high','Automated best-shot selection; inspect target-type restrictions rather than assume protection.'),
52:('candidate','high','Recognition/munition selection in automatic weapon; check safeguarded exclusions versus improved lethality.'),
53:('candidate','high','Linked human-transported weapons with neural-network classification; inspect human control and target restrictions.'),
54:('candidate','high','Explicit autonomous drone weapon subsystem; inspect actual restraint claims and authorization.'),
55:('candidate','high','Human/non-human target recognition explicitly named; recognition is not necessarily protection of humans.'),
56:('candidate','high','Autonomous linked drone weapons; inspect cross-weapon coordination restrictions and human authority.'),
57:('adjacent','medium','Location-based magazine suggests geofencing analogue; no autonomous targeting shown.')}
assert len(rows)==len(notes)==57
out=[]
for i,r in enumerate(rows,1):
 category,priority,why=notes[i]
 d=dict(r);d.update(screen_row=i,screen_category=category,review_priority=priority,screen_reason=why,screen_basis='Exported title + CPC + named applicant only; abstracts and claims absent',claims_read='no',abstract_read='no',publication_link='https://patents.google.com/patent/'+r['Document ID'].replace(' ','')+'/en',related_metadata_cluster='Bilbrey/Sitrick linked weapon applications; do not merge legally without priority analysis' if 49<=i<=56 else '',publication_date_in_requested_window=str('2021-11-15'<=r['Date Published']<='2026-11-15').lower())
 out.append(d)
base='uspto_F41A1708_20211115_20261115_metadata_screen'
with open(base+'.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
summary={'input':str(p),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'query':'F41A17/08.CPC. AND @PD>=20211115 AND @PD<=20261115','ui_total_results_reported_by_export_agent':105,'exported_rows':len(rows),'distinct_export_family_ids':len({r['Family ID'] for r in rows}),'category_counts':dict(collections.Counter(r['screen_category'] for r in out)),'priority_counts':dict(collections.Counter(r['review_priority'] for r in out)),'scope':'Complete classification of 57 exported family representatives from ONE CPC query, not all publications, not all safeguard patents. Native interface family definition/representative selection has not been independently reconstructed.','method':'Human-authored metadata triage joined and checked deterministically by Python. No abstracts or claims supplied by export; no claims read in this task. Candidate means prioritize inspection, not verified safeguard. Adjacent and provisional exclusions retained, not discarded.','date_caveat':'Date Published may be application publication or grant date according to kind code, not priority/invention date. Filing Date is not a substitute for earliest family priority.','limitations':['CPC assignment varies and may occur in either CPCI or CPCA fields; one-class query can miss relevant inventions.','57 Family IDs do not mean 57 independent inventions or technologies. Eight Bilbrey/Sitrick records (rows49-56) share inventors/filing date and overlapping titles but have distinct exported Family IDs; legal family relations require checking.','A1 application and B1/B2 grant representatives are mixed. Search hits do not establish claims survived examination or current legal status.','Metadata cannot establish deployment, operational effectiveness, ethical/legal compliance or affiliation with ASIMOV.','Google Patents URLs are generated navigation aids, not evidence of pages retrieved.'],'rows':out}
Path(base+'.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
