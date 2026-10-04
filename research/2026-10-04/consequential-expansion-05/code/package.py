import pathlib,json,collections,hashlib,zipfile
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
C=jl('cards.jsonl');R=jl('candidate-screen.jsonl');used={s for r in R for s in r['source_ids']}
counts=dict(lenses=6,screened_predicates=24,source_manifest=344,sources_in_concrete_candidates=len(used),proposed_new_formulations=2,retained_refinements=1,detailed_cards=3,dispositions=dict(collections.Counter(r['disposition'] for r in R)),reviewed_baseline_formulations=51,pending_new_formulations=2,provisional_cumulative_non_refinement_formulations=53,independent_abstract_mechanism_count='not asserted',prior_active_pair_rows=1715,prior_quarantines=15,documentation_entries=8,failed_fulltext_accesses=2,matched_investigations=0,data_records_acquired=0,confirmed_end_to_end_feasible=0,positive_findings=0,artifact_checks=8,synthetic_arithmetic_checks=10,total_checks_passed=18,paid_external_api_calls=0,all_further_candidates_exhausted=False,user_reported_weekly_remaining_percent=88,user_report_time='2026-10-04 18:50 UTC',automatic_weekly_and_token_telemetry='unavailable',usage_attribution='Earlier 99% to latest 88% is an 11-point change, not attributable solely to this work.')
(P/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
intro=f'''# Six-lens breadth checkpoint — 4 October 2026

This pass screened **24 concrete predicates across {len(used)} source descriptions**, using six discovery lenses. It retains **two proposed new formulations** and **one refinement**. Seven ideas were rejected, four deferred, seven recognized as deferred refinements, and three recognized as repeats. The lenses did not automatically generate valid tests.

The most promising addition asks whether an important plant-performance claim survives a complete energy balance. It requires measured consumption and generation for the same physical boundary—not fuel purchases, electricity sales or a comparison with a typical plant. The other asks whether independent completed reimbursements for one eligible cost exceed the funding permitted by the operative instruments. Two funders reporting the same transfer, or an advance later reconciled, do not establish duplicate recovery.

Both remain **source-level proposals**. Documentation confirms useful definitions and possible access routes; no plant, invoice, payment, member or company records were matched. Neither is classified end-to-end feasible. A legislative conflict-declaration route is retained as a refinement, not counted as new merely because the decision maker is an MEP.

## What each lens yielded

| Lens | Decisions and useful exclusions |
|---|---|
| Conserved quantities | B01 energy-conversion proposal. Rainfall minus evapotranspiration cannot establish illegal pumping; arms and displacement datasets lack compatible complete stock/flow units. |
| Mutually exclusive statuses | No new card: shipping flags need historical legal instruments, multiple network origins can be authorized, radio licences can reuse frequencies, and mineral rights can cover different interests. |
| Prerequisites and sequence | No new card: advances can precede delivery; trial ethics and financing-condition sequences refine existing X07; DSCA notices do not define every arms-transfer authorization sequence. |
| Beneficial-interest conflicts | REF-MEP is a useful explicit-statement route. Procurement and charity relationships largely repeat E08; role names do not establish beneficial interests or incompatible employment. |
| Double claims | B02 constrained cost recovery is proposed new. Shared paper acknowledgements are not duplicate cost claims; carbon units and renewable attributes need exact serial/right evidence. |
| Operations versus representations | No new card: sunk-vessel, fuel-input, construction and species examples mostly specialize existing precise-assertion tests. Registry presence and remote nonvisibility are not operational facts. |

`candidate-screen.csv` gives a concrete predicate, named sources, semantic comparison, discriminating evidence and stopping condition for every branch. `source-coverage.csv` preserves all 344 descriptions and distinguishes the {len(used)} used here from those without a concrete candidate in this batch. It does not claim that every pair among the 344 has been individually researched. Original SYS/AP identifiers, field descriptions, line provenance and block hashes remain in the manifest.

## Corrected cumulative counts

Independent review accepts **51 non-refinement formulations through expansion 04**. Q01 is now a refinement of the original S06 donor-eligibility/incorporation/refund predicate. Q02, Q03 and V01 were accepted as defensible new formulations, without claiming they are independent abstract mechanisms. With B01/B02 pending review the provisional count is **53**.

The prior **1,715 active provisional directional source-pair rows plus 15 quarantines** remain a different counting unit. The 5,000 target is not met and no source permutation, date parameter or rewording has been counted to inflate it.

This bundle also includes the reviewed repairs: Q02 distinguishes never-completed or misattributed transfers from completed contributions later refunded; Q03 join confidence is reduced to 2 until the legal-guarantor/reporting-perimeter crosswalk is documented. V01 requires one selected filing vintage, source hashes/row locators, reviewed canonical holding identity, aggregate/detail resolution and conservative exposure/denominator bounds. Its 26 checks include aliases for the same economic position, mixed revisions, aggregate rows and rounded marginal excesses. Those are evidence requirements, not claims that software can authenticate a caller's manifest.

## Documentation and validation

Eight documentation observations are recorded. EIA definitions distinguish consumption, generation and incoming electricity. OCDS/IATI transaction identifiers can help trace a payment path but do not guarantee invoice publication or independent flows. World Bank guidance is used for document anatomy; an actual financing instrument must establish the cost constraint. Both attempted European Parliament PDF opens returned unusable verification pages; the log preserves those failures. Search excerpts are not promoted to verified current legal applicability.

This batch passed **18 checks: eight artifact/provenance checks and ten synthetic arithmetic checks**. The synthetic helpers demonstrate conservative physical bounds and constrained-cost arithmetic; their gates require independently reviewed evidence. They do not discover identity matches or resolve the flow graph. A low balance or lack of an excess flag never establishes compliance.

Priority remains an editorial score: `10 × consequence + 3 × testability + 2 × join confidence − 2 × cost`, with separate consequence/testability ranks. Scores are not probabilities of wrongdoing. B01 is more testable than B02 because public physical-measure definitions are available, while B02's invoice/settlement chain is still an access dependency. Name-only routes remain provisional.

Run `python code/design.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py`. These local scripts perform no API calls. Source selection and semantic comparisons were authored in the existing model environment; exports, ranking, consistency checks and calculations are deterministic. The ZIP contains the corrected current expansions 01–05; earlier ZIPs and delivery receipts remain preserved separately in Git.

## Continuation boundaries

This is an incremental breadth checkpoint, not evidence that all further discovery is exhausted. The 24 examined candidates have explicit dispositions. Further work on them now has concrete dependencies: an exact plant boundary and issuer-to-plant bridge; a published cost-level financing/settlement chain; historical ship-registration instruments; or serial-level environmental-attribute records. Advancing those routes requires the indicated evidence rather than another paraphrase. New discovery can still examine other catalog predicates and documented supporting Rabbit sources. No public outreach, accounts, bulk execution or paid APIs were used.

Automatic weekly ChatGPT allowance and model-token telemetry are unavailable. The latest user report remains **88% at 18:50 UTC**. The earlier 99% to 88% change cannot be attributed solely to this work. Paid external API calls: **zero**.

## Detailed cards
'''
parts=[intro]
for c in C:
 parts.append(f"\n### {c['test_id']} — {c['title']}\n\n{c['kind']}; priority {c['priority_rank']}; consequence {c['consequence']}/5, testability {c['testability']}/5, join confidence {c['join_route']}/3, cost {c['cost_tier']}/4.\n")
 for k,label in [('initial_observation','If'),('expected_observation','Then'),('basis','Basis'),('operational_join','Join'),('temporal_geographic_scope','Scope'),('ordinary_explanations_and_disqualifiers','Ordinary explanations / disqualifiers'),('mandatory_evidence','Required evidence'),('next_cheapest_check','Next cheapest check'),('novelty_comparison','Novelty'),('access_evidence','Access evidence')]:
  v=c[k];parts.append('\n**'+label+':** '+('; '.join(v) if isinstance(v,list) else v)+'\n')
 parts.append('\n**Provenance:** '+'; '.join(f"{s['sys_id']} {s['name']} ({s['file']}:{s['line_start']}; {', '.join(s['all_ap_ids'])})" for s in c['source_manifest'])+'\n')
 parts.append('\n**Documentation IDs:** '+', '.join(c['documentation_ids'])+' in evidence/documentation.jsonl.\n')
(P/'README.md').write_text(''.join(parts))
(P/'generation-provenance.json').write_text(json.dumps(dict(date='2026-10-04',instruction='Continue breadth through six discovery lenses using actual fields, public-interest consequence, discriminating evidence and plausible cheap routes. Do not turn lenses into universal templates; compare every candidate with prior formulations and save rejections.',baseline_correction_commit='627bde4',all_344_manifest_fields_inspected=True,concrete_candidates=24,existing_model_environment=True,paid_api_calls=0,semantic_decisions='Model-authored, independent novelty review pending B01/B02',automatic_enumeration='Exports and ranks only; no universal pair generation in this pass',record_investigations=0),indent=2)+'\n')
(P/'progress-ledger.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in [dict(stage='review_repairs',accepted_through04=51,q01='refinement',v01_checks=26),dict(stage='breadth_screen',lenses=6,predicates=24,sources=len(used),dispositions=counts['dispositions']),dict(stage='documentation',entries=8,failed_fulltext_accesses=2,matched_records=0),dict(stage='validation',artifact=8,synthetic=10,total_passed=18),dict(stage='checkpoint',proposed_new=2,refinements=1,provisional_total=53,global_exhaustion=False)]))
files=[f for f in sorted(P.rglob('*')) if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts and f.name not in ['artifact-checksums.json','delivery-receipt.json']]
(P/'artifact-checksums.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2)+'\n')
z=P/'checkpoints/consequential-expansions-through-05.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for i in range(1,6):
  root=P.parent/f'consequential-expansion-0{i}'
  for f in sorted(root.rglob('*')):
   if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts:a.write(f,pathlib.Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as a:assert a.testzip() is None
print(json.dumps(counts,indent=2));print('ZIP',z.stat().st_size,hashlib.sha256(z.read_bytes()).hexdigest())
