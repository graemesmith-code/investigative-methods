import pathlib,json,collections,hashlib,zipfile
P=pathlib.Path(__file__).resolve().parents[1];jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
C=jl('cards.jsonl');R=jl('priority-subchecks.jsonl');Q=jl('priority-coverage.jsonl')
counts=dict(requested_priorities=8,priorities_substantively_screened=8,recorded_subchecks_and_gates=24,subchecks_are_not_independent_mechanisms=True,proposed_new_formulations=2,retained_refinement_cards=5,total_new_detailed_cards=7,dispositions=dict(collections.Counter(r['disposition'] for r in R)),source_manifest=344,sources_in_this_screen=len({n for r in R for n in r['source_ids']}),documentation_entries=18,failed_access_requests=1,matched_investigations=0,substantive_record_pairs_acquired=0,confirmed_end_to_end_feasible=0,positive_findings=0,artifact_checks_passed=16,prior02_reviewed_non_refinement_cards=48,provisional_cumulative_non_refinement_cards=50,new03_independent_novelty_review='complete: Q01 S06 refinement; Q02/Q03 accepted as formulations',prior01_new=12,prior01_refinements=4,prior02_new=4,prior02_refinements=1,prior_active_pair_rows=1715,prior_quarantines=15,priority_set_source_discovery_complete=True,all_catalog_predicates_exhausted=False,paid_external_api_calls=0,weekly_chatgpt_allowance='automatic telemetry unavailable',user_reported_weekly_remaining_percent=88,user_report_time='2026-10-04 18:50 UTC',earlier_user_report_percent=99,attribution='11 percentage-point change cannot be attributed solely to this work',model_token_counter='unavailable')
(P/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
intro='''# Eight-priority follow-through — 4 October 2026

All **eight requested priorities** now have substantive source-level decisions. This pass records **24 subchecks and gates**, not 24 independent hypotheses, and retains **two proposed new formulations plus five useful refinements**. It does not claim all opportunities across the 344 sources are exhausted.

Independent review found Q01 overlaps S06’s existing donor-eligibility, incorporation and refund checks. Q01 remains detailed but is now a refinement. Historical checkpoint counts are superseded by this correction.

A concrete example: a party reports accepting a corporate donation and supplies a company registration number. That number could identify an overseas establishment rather than the UK-incorporated entity suggested by the donor’s brand. The cheap first check is the original donation record, exact company entry and any return/amendment—not a name search or an assumption that dormant accounts prove illegality. The full card keeps incorporation, actual business activity, historical rules and receipt disposition separate. This is a hypothetical method, not a finding about a donor.

The two proposed additions test actual charity assets transferred as a candidate-campaign contribution, and an express sovereign-guarantee disclosure against an operative guarantee instrument. A charity’s employees donating personally, or a sovereign’s loan commitments exceeding a debt aggregate, do not meet those predicates.

## What each priority yielded

| Priority | Decision | Why |
|---|---|---|
| Corporate donor eligibility | S06 refinement Q01 | Exact company identity, actual eligibility at receipt, and acceptance/return history; dormant status alone is insufficient. |
| Insurance representations | Refinement REF-INS; other routes deferred/rejected | Specific signed answer versus established contemporaneous condition refines P05; policy coverage against required protection refines X08. Allegations prove neither. |
| Charity political benefits | New proposal Q02 | Actual organizational asset contribution to a candidate campaign, distinct from employee activity and a lobbying-reporting discrepancy. |
| Consent clauses | Refinement REF-CONS | Covered legal transfer before required consent refines X07; shareholder changes, notice, waivers and deemed consent need separate checks. |
| Outage disclosures | Refinement REF-OUT | Same-unit availability versus output refines R14. Publication lateness needs historical notice evidence; market-profit claims were rejected. |
| Debt completeness | New proposal Q03 | Explicit guarantee disclosure versus original operative instrument; no completeness assumed from an aggregate or blank reporting form. |
| Compensation | Refinement REF-COMP | Recognized entitlement/availability versus possession refines X02/X07; approved escrow is a real alternative explanation. |
| Maintenance certifications | Deferred; recurrence recognized as P02 refinement | No original component certificate/life-history chain established. Aircraft registration and later failure cannot fill that gap. |

Every priority has three separately reasoned branches in `priority-subchecks.csv`, including source IDs, evidence requirements, novelty comparison and stopping condition. There is no generic “covered” label standing in for those branches. `priority-coverage.csv` resolves G16–G23 from the preceding queue. `source-coverage.csv` distinguishes this pass’s sources from the rest of the 344-source manifest.

## Counts and review status

Independent review accepted the preceding four additions after repairs, leaving **48 non-refinement detailed cards**. With the current two proposals the provisional total is **50**, with Q02/Q03 accepted by independent review as formulations, not necessarily independent abstract mechanisms. The first expansion remains corrected to 12 new formulations and four refinements; the second has four new formulations and one refinement. Seven current cards include five refinements, so they do not add seven to the novelty total.

The earlier longlist remains **1,715 active provisional source-pair rows plus 15 quarantines**. Those implementation rows are not the same counting unit as mechanisms or detailed cards. We have not reached 5,000 defensible independent tests and have not padded the count.

## Prior repairs included

The bundle includes corrected current outputs from expansions 01 and 02 while their original checkpoints remain preserved in the repository. The bid helper now distinguishes an initially tied-lowest bid becoming dearer from a strict same-rival price reversal, reports rival margins and item contributions, and requires explicit pricing/specification/performance gates. Losing bidders have submitted bid rates, not contractual rates. The inventory card now requires presence at the claimed observation date/interval; an older image alone is insufficient, and demolition, relocation and removal are falsifiers. Inventory observation date and legal eligibility cutoff are separate.

The second expansion passes **13 artifact checks, eight synthetic arithmetic checks and three synthetic temporal checks**. This batch passes **16 artifact checks** covering counts, provenance, ranking and safeguards. These checks do not establish empirical truth, semantic novelty or legal applicability.

## Evidence and access

Eighteen documentation entries were recorded. The current UK statutory page failed to render with an unsupported XHTML content type; the log preserves that failure, and the dated 2024 view is not labeled current law. Current regulator guidance is a documented starting point, not case-specific legal adjudication. The current blank SEC Form 18-K was inspected; its categories, exceptions and incorporation by reference prevent assuming a complete guarantee universe. The 2018 World Bank guidance distinguishes its explanatory role from the Standard and describes conditional escrow arrangements. The maintenance standards page surfaced is explicitly historical, not verified current authority.

**Zero matched investigations, zero acquired substantive record pairs, zero confirmed end-to-end feasible routes and zero positive findings.** No named donor, charity or borrower was investigated. No new account, credentials, paid PACER fetch, bulk data collection or outreach occurred. Historical exemption evidence, insurance exhibits, actual consents, historical outage versions, guarantees, claimant compensation and component logs remain case-level dependencies.

## Ranking and reproduction

Consequence 1–5 is potential public-interest significance if proven; testability 1–5 is route maturity (every current card is at most 2); join route 1–3 distinguishes provisional name/entity bridges from precise candidate identifiers; cost tier 1–4 estimates rising access/document effort. No score certifies an actual match or a measured cost. Composite = `10 × consequence + 3 × testability + 2 × join route − 2 × cost tier`, with separate consequence/testability ranks. These are editorial priorities, not probabilities of wrongdoing.

Run `python code/design.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py` from this folder. The scripts make no API calls. Source selection, branch decisions and card text are model-authored in the existing environment; deterministic code exports, ranks and validates them. The generation instruction was to substantively examine all eight named priorities, retain only defensible distinct predicates, preserve refinements and original evidence dependencies, and stop rather than manufacture novelty. Original SYS/AP identifiers, line provenance and hashes remain in `sources.jsonl` and card manifests.

The bundle is `checkpoints/consequential-expansions-through-03-corrected.zip`. Historical delivery receipts refer to their original separate checkpoint artifacts, which are preserved in Git rather than nested again in this ZIP. Code, CSV/JSONL, documentation observations, access failures, supporting dependencies and validation logs are included.

## Why this priority pass stops here

Each of the eight priorities has now been examined through its stated subchecks; all have a retained, refined, rejected or deferred disposition. Remaining work would require acquiring particular original records or developing a genuinely different predicate. The current instruction excludes matched investigations, so this pass stops at the completed source-level priority sweep. That is a boundary for this batch, not a claim that the catalog has no more opportunities. Work continues beyond this checkpoint under the renewed instruction: further source-level discovery beyond Q02–Q03 and source-grounded discovery around investment mandates, precise search-response assertions and evidence independence. No matched investigation is being performed.

Automatic weekly ChatGPT allowance and model-token telemetry are unavailable. The user reported **88% remaining at 18:50 UTC on October 4**, compared with an earlier 99%; the 11 percentage-point change cannot be attributed solely to this work. Paid external API calls: **zero**.

## Detailed cards
'''
parts=[intro]
for c in C:
 parts.append(f"\n### {c['test_id']} — {c['title']}\n\n{c['kind']}; priority rank {c['priority_rank']}; consequence {c['consequence']}/5, testability {c['testability']}/5, join route {c['join_route']}/3, cost tier {c['cost_tier']}/4.\n")
 for key,label in [('if_observation','If'),('then_expected','Then'),('basis','Basis'),('join','Join'),('timing_geography','Scope'),('ordinary_explanations_and_disqualifiers','Ordinary explanations / disqualifiers'),('required_original_records','Required original records'),('next_cheapest_check','Next cheapest check'),('novelty','Novelty'),('access_evidence','Access evidence')]:
  v=c[key];parts.append('\n**'+label+':** '+('; '.join(v) if isinstance(v,list) else v)+'\n')
 parts.append('\n**Provenance:** '+'; '.join(f"{s['sys_id']} {s['name']} ({s['file']}:{s['line_start']}; {', '.join(s['all_ap_ids'])})" for s in c['source_manifest'])+'\n')
 parts.append('\n**Documentation:** '+', '.join(c['documentation_ids'])+' in evidence/documentation.jsonl.\n')
(P/'README.md').write_text(''.join(parts))
(P/'progress-ledger.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in [dict(stage='prior_review_repairs',expansion01_new=12,expansion01_refinements=4,expansion02_new=4,expansion02_refinements=1,cumulative=48),dict(stage='eight_priority_screen',prior_gap_ids=[q['prior_gap'] for q in Q],subchecks=24,subchecks_not_independent_mechanisms=True),dict(stage='development',new_proposed=2,refinements=5,record_pairs=0),dict(stage='validation',artifact_checks=16,positive_findings=0),dict(stage='stop',reason='All eight named priorities have substantive branch decisions; unresolved original-record dependencies or different predicates are needed for further progress. No global exhaustion claim.',remaining='Independent novelty review; authorized record pilots or newly prioritized gap set')]))
(P/'baseline.json').write_text(json.dumps(dict(expansion01_corrections='5a53612c2032e0801504528bee8e18b6d1a476dd',expansion02_core_repairs='e7a4644',reviewed_non_refinement_cards=48,prior_active_pair_rows=1715,quarantines=15,prior_review_corrections=json.loads((P.parent/'consequential-expansion-02/review-corrections.json').read_text())),indent=2)+'\n')
roots=[P.parent/('consequential-expansion-0'+str(i)) for i in [1,2,3]]
for root in roots:
 fs=[f for f in sorted(root.rglob('*')) if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts and f.name not in ['artifact-checksums.json','delivery-receipt.json']]
 (root/'artifact-checksums.json').write_text(json.dumps({str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in fs},indent=2)+'\n')
z=P/'checkpoints/consequential-expansions-through-03-corrected.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for root in roots:
  for f in sorted(root.rglob('*')):
   if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts:a.write(f,pathlib.Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as a:assert a.testzip() is None
print(json.dumps(counts,indent=2));print('ZIP',z.stat().st_size,hashlib.sha256(z.read_bytes()).hexdigest())
