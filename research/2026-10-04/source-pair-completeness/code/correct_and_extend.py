import pathlib,json,csv,shutil
P=pathlib.Path(__file__).resolve().parents[1];OLD=P.parent/'source-test-deep-review';load=lambda p:[json.loads(x) for x in p.read_text().splitlines()]
def jl(n,rows):(P/n).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
def cs(n,rows):
 with (P/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)
M={m['key']:m for m in json.loads((P/'mechanisms.json').read_text())};mech=load(OLD/'mechanism-review.jsonl')
for r in mech:
 if r['mechanism']=='W09':r['preferred_source_b']='SYS-0201'
 a,b=int(r['preferred_source_a'][-4:]),int(r['preferred_source_b'][-4:]);m=M[r['mechanism']];ok=a in m['a'] and b in m['b'];r['membership_status']='emitted_rule_representative' if ok else 'supplemental_proposed_pair_outside_original_rule';r['supplemental_reference']=None if ok else 'supplemental-pair-register.csv#'+r['mechanism'];r['review_depth']='mechanism-specific reasoning; representative membership explicit; no actual pair execution'
jl('mechanism-review.jsonl',mech);cs('mechanism-review.csv',mech);cs('supplemental-pair-register.csv',[r for r in mech if r['supplemental_reference']])
remaining=load(OLD/'remaining-108-reviews.jsonl')
for r in remaining:
 if r['sys_id']=='SYS-0171':r['partner_sys_id']='SYS-0201';r['partner_name']='Small-Area Global Elections (SAGE)'
jl('remaining-108-reviews.jsonl',remaining);cs('remaining-108-reviews.csv',remaining)
# Carry the complete source ledger forward with references to preserved review layers.
allrows=list(csv.DictReader((OLD/'all-344-source-reasoning.csv').read_text().splitlines()))
for r in allrows:
 if r['sys_id'] not in {x['sys_id'] for x in remaining}:r['review_file']='../source-test-deep-review/'+r['review_file']
cs('all-344-source-reasoning.csv',allrows)
cards=load(OLD/'reviewed-recipes.jsonl')
for r in cards:
 if r['review_id']=='N05':
  r['title']='State Department request response and reading-room publication'
  r['initial_observation']='IF a MuckRock request to the US State Department is marked fulfilled and the correspondence supplies an explicit State case identifier plus identifiers for released documents.'
  r['expected_observation']='THEN compare the final response and attachments with the same identified documents, if published in the State reading room, to check whether versions or redactions materially differ. Reading-room absence is not nonresponse.'
  r['operational_join']='MuckRock request ID → State case ID in correspondence → exact original document identifier and version/page. Topic/title similarity is insufficient.'
  r['mandatory_auxiliary_inputs']=['State-specific request and complete final response','Exact reading-room document crosswalk','Both document versions and release dates'];r['historical_scope']='US State Department only; distinguish request completion, reading-room publication and declassification dates.'
  r['ordinary_explanations_and_falsifiers']='No reading-room counterpart, later declassification, amended response or different document version. Without the explicit crosswalk this remains a single-source response-document check.'
  r['proposed_falsifier']=r['ordinary_explanations_and_falsifiers'];r['next_cheapest_check']='Inspect one State request’s response letter for a case/document identifier that actually resolves in the reading room; do not infer missing agency action from search absence.'
  r['feasibility_status']='State_specific_crosswalk_unverified; fallback_single_source_check';r['supersedes']='third-checkpoint N05 generic agency framing'
new=[
('P01',[250,249],'Later affirmative reliance on retracted evidence',
'IF a Crossref-linked publisher notice establishes a retraction of an exact article DOI on a known date.',
'THEN use OpenAlex references to identify later papers citing that work and read their full text for affirmative reliance on the withdrawn finding without acknowledging its status.',
'Exact normalized DOI → OpenAlex work ID → cited-by edge; confirm the referenced article, not the retraction notice or another version.',
'Worldwide scholarship; compare original online/acceptance dates, notice date and publication versions. A later issue date alone is insufficient.',
['Publisher retraction notice and affected scope','Full citing passage and bibliography','Online/acceptance/version chronology','Public-interest significance of the asserted medical/policy result'],
'Citation criticizes the paper, discusses the retraction, predates notice acceptance, or relies on an unaffected result. Crossref and OpenAlex can share Retraction Watch status.',
'Read one notice and one eligible citing passage; metadata citation edges alone do not support a finding.',
'Continued reliance on invalidated clinical or policy evidence may be consequential; this is a new research-integrity test, not an inference that citation itself is misconduct.',['P-D01','P-D02']),
('P02',[74,75],'Recurrence after recorded ship-defect rectification',
'IF an original Paris MoU inspection records that a particular serious defect on an identified ship was rectified, with the component and date clear.',
'THEN examine a later Tokyo MoU report for the same ship and defect to determine whether the condition recurred or the apparent repair claim warrants explanation.',
'Typed IMO ship number plus inspection date and specific deficiency/equipment identity; an IMO company number or generic defect category is insufficient.',
'Same vessel across the two regimes and ordered inspection dates; preserve changes of operator, repairs and permitted onward voyages.',
['Permitted original inspection reports','Exact action/deficiency codes and component description','Rectification confirmation and repair/owner history'],
'New damage, different equipment, changed operator, coding reuse or lawful repair-port arrangements explains recurrence. No assumption that every deficiency forbids departure.',
'Confirm record/reuse permission and whether public reports identify the exact defect; do not collect restricted records before authorization.',
'Repeated serious ship defects can affect worker safety and coastal communities, but available access and report detail make this costly.',['P-D03']),
('P03',[146,260],'Selective interference versus general network loss',
'IF repeated public OONI web-connectivity observations show a specific destination failing on a known ASN during a defined interval, with control measurements available.',
'THEN compare contemporaneous IODA signals for that ASN and other destinations to determine whether broad connectivity loss plausibly explains the apparent blocking.',
'Exact ASN with valid assignment interval plus compatible probe geography and timestamps; ASN-wide measurements cannot automatically describe every subscriber.',
'Same network, locality and narrow time window; account for collector availability and monitoring changes.',
['Raw existing OONI measurement and controls','IODA signal coverage/baseline','Historical ASN attribution','Failure-mode and destination comparison'],
'OONI anomaly is a false positive; routing/hosting failure affects only this site; probes and IODA observe different network segments. Normal aggregate reachability does not prove deliberate censorship.',
'Inspect a small existing public anomaly/control set and signal coverage; launch no active probes. Prior AS21928 sample has no anomaly and is not a positive case.',
'Discriminating censorship from general outage can materially change a high-consequence public explanation; no actor intent is inferred.',['D14','D15']),
('P04',[71,229],'Fishing activity in a specifically restricted marine area',
'IF a Protected Planet area has a verified marine boundary and an authoritative rule that prohibited the relevant fishing activity on a stated date.',
'THEN examine permitted Global Fishing Watch observations for a correctly identified vessel within that boundary and verify whether the activity actually was fishing covered by the rule.',
'Verified vessel identity, dated positions and spatial intersection with the operative marine boundary; model confidence and positional uncertainty retained.',
'Same boundary version and event time; jurisdiction, gear, zone exceptions and permits explicitly checked.',
['Operative area-specific fishing rule','Dated boundary and permits/exceptions','Vessel identity and independent activity corroboration','AIS and classifier coverage'],
'Protected status permits fishing, vessel transits, gear is exempt, position is erroneous or activity classifier is wrong. Absence of AIS is not evasion.',
'First read the actual area restriction and verify both API access routes; discard cases lacking a specific rule before obtaining track samples.',
'Possible fishing in a legally restricted area differs from static industrial overlap, but this remains a legally conditional design with credential and activity-verification costs.',[]),
('P05',[38,5],'Specific issuer compliance claim versus a final facility finding',
'IF an SEC issuer filing makes a precise factual claim about the absence of a specified class of violation at an identified operating facility during a defined period.',
'THEN read the relevant final EPA enforcement finding for that same facility and period to determine whether it contradicts the actual words of the claim.',
'ECHO facility identity → operator at event time → documented issuer consolidation/ownership → exact filing passage. Similar company names are insufficient.',
'US facility, actual finding and claim reporting intervals; retain settlement, appeal and reporting cut-off dates.',
['Exact filing claim and qualifications','Original final finding and procedural status','Historical operator/issuer crosswalk','Definition of the claimed violation category'],
'Finding is an allegation, different subsidiary, outside the period or explicitly qualified/disclosed. A materiality threshold may narrow the claim; no securities-law breach inferred.',
'Read the precise issuer claim first, then one matching final case document; discard vague boilerplate that makes no falsifiable assertion.',
'A demonstrably contradictory safety/environmental assertion to investors can be consequential; this differs from enforcement-to-funding overlap and is constrained to concrete factual claims.',[])
]
for rid,ids,title,initial,expected,join,time,aux,stop,nextcheck,why,docs in new:
 r={k:None for k in cards[0]};r.update(review_id=rid,base_recipe_id='SUPPLEMENTAL-'+rid,source_ids=ids,title=title,feasibility_status='source_specific_conditional_not_executed',initial_observation=initial,expected_observation=expected,operational_join=join,historical_scope=time,consequential_finding_and_basis=why,mandatory_auxiliary_inputs=aux,ordinary_explanations_and_falsifiers=stop,proposed_falsifier=stop,next_cheapest_check=nextcheck,source_specific_priority_reason=why,evidence_doc_ids=docs,sample_labels=[],reviewer='same model; no independent review of final five cards',bulk_investigative_execution=False,check_actually_performed='Catalog/cluster reasoning and listed documentation read; no positive case or full predicate tested.')
 cards.append(r)
jl('reviewed-recipes.jsonl',cards);cs('reviewed-recipes.csv',cards)
# Pair-specific recommended queue; dimensions manually justified, composite mechanically reproducible.
ratings={
'R01':(98,1,1,3,'Public contract actions and a dated restriction can identify a material public-money issue; name identity and legal scope dominate cost.'),
'R05':(92,2,4,2,'Explicit NCT reference makes linking cheap; expensive work is historic protocol/outcome interpretation. Saved example is retrospective and cannot supply a prospective baseline.'),
'R11':(94,2,4,2,'Project ID and original agreement are linked; education-project commitments are concrete, but routine amendments and unreliable index dates must not become allegations.'),
'N09':(89,1,2,2,'A physical-output upper bound can be decisive after proving completeness, compatible measures and a facility-province bridge; these are not yet verified.'),
'P01':(92,2,4,3,'Exact DOI makes identity strong; critical versus affirmative citation requires full text, chronology and a credentialed/metered access route if OpenAlex content is used.'),
'P02':(96,1,4,3,'Ship-ID linking is precise if typed, but permission and original defect detail block a cheap record comparison.'),
'P03':(94,2,3,2,'Public measurement routes make a bounded check plausible; probe locality, historical ASN and signal comparability remain interpretation costs.'),
'P04':(94,1,2,3,'Marine conservation stakes are high, but exact legal restriction, permits, API credentials and fishing classification dominate cost.'),
'P05':(95,1,1,2,'A concrete investor assertion can be falsified; operator-to-issuer history and finality of enforcement are manual identity/evidence burdens.')}
queue=[]
for rid,(impact,testability,confidence,cost,reason) in ratings.items():
 r=next(r for r in cards if r['review_id']==rid);queue.append(dict(review_id=rid,source_ids=r['source_ids'],public_interest_score=impact,testability_score=testability,join_confidence_score=confidence,burden_tier=cost,triage_score=round(.65*impact+5*testability+3*confidence-4*(cost-1),2),pair_specific_reason=reason,evidence_gaps=r['mandatory_auxiliary_inputs'],next_cheapest_check=r['next_cheapest_check'],cost_scope='initial bounded triage; not quoted execution price',status='not_executed'))
queue.sort(key=lambda r:-r['triage_score']);queue=[dict(rank=i+1,**r) for i,r in enumerate(queue)];cs('recommended-next-tests.csv',queue);jl('recommended-next-tests.jsonl',queue)
print('Detailed cards',len(cards),'pair-specific recommended queue',len(queue))
