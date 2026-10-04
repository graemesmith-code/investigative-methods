import pathlib,json,collections,hashlib,zipfile
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
C=jl('cards.jsonl');R=jl('candidate-screen.jsonl')
counts=dict(screened_predicates=12,proposed_new_formulations=1,retained_refinement_cards=3,detailed_cards=4,dispositions=dict(collections.Counter(r['disposition'] for r in R)),source_manifest=344,sources_in_this_screen=len({s for r in R for s in r['source_ids']}),documentation_entries=6,metadata_samples=1,metadata_sample_bytes=10094,failed_access_attempts=1,successful_metadata_fallbacks=1,matched_investigations=0,substantive_record_pairs_acquired=0,confirmed_end_to_end_feasible=0,positive_findings=0,checks_passed=17,artifact_checks=9,synthetic_arithmetic_checks=8,accepted_baseline_non_refinement_cards=48,pending03_novelty_review=3,pending04_novelty_review=1,provisional_cumulative_non_refinement_cards=52,prior_active_pair_rows=1715,prior_quarantines=15,all_catalog_predicates_exhausted=False,paid_external_api_calls=0,user_reported_weekly_remaining_percent=88,user_report_time='2026-10-04 18:50 UTC',automatic_weekly_meter='unavailable',model_token_counter='unavailable',usage_attribution='Earlier user report was 99%; 11 percentage-point change cannot be attributed solely to this task.')
(P/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
intro='''# Investment limits and evidence checks — 4 October 2026

This checkpoint screens **12 further predicates** and retains **one proposed new formulation and three refinements**. The new proposal tests actual disclosed fund positions against a binding concentration limit. A small official CVM dictionary confirms the relevant fields; no portfolio holdings or matched cases were acquired.

The useful insight is a one-sided test: when a limit uses an additive, nonnegative exposure measure, verified visible positions may already exceed the limit even if other positions are confidential. A visible total below the limit cannot establish compliance. The exact fund/class mandate, denominator, testing date, issuer group, netting rules and permitted exceptions must be resolved first. The arithmetic helper enforces input gates; it cannot verify those real-world facts.

The other cards improve methods already counted: an explicit connected-issuer flag against control evidence, a precise records-custody assertion against authenticated custody evidence, and claimed independent corroboration against the actual evidence chain. Counting these as three new mechanisms would inflate novelty. Eight further branches are rejected or deferred with reasons in `candidate-screen.csv`.

## Current totals and boundaries

There are **48 previously reviewed non-refinement cards**, plus **three proposals in expansion 03 and one here awaiting independent novelty review**: **52 provisionally**, not 52 independently validated investigations. Earlier implementation enumeration remains **1,715 active provisional directional source-pair rows and 15 quarantines**. These counts use different units and must not be added together. The original 344-source manifest and SYS/AP provenance are retained. Every source has already received an individual source-level review in the earlier deep-review phase; that does not establish every possible predicate or pair as feasible.

The first 5,000-test target has not been justified. No total was padded through variants, source substitutions or parameter multiplication. No matched investigation, positive finding or end-to-end feasible route is claimed in this batch. All four cards require original records before execution.

## What was verified

The official CVM metadata ZIP is only **10,094 bytes**. Its raw bytes, SHA-256, 12 dictionary files, decoded text and parsed fields are saved under `evidence/`. Identifier fields vary by portfolio block: an ISIN is not universally present, fund/class identifiers differ from issuer identifiers, and reported net assets are not the same as gross portfolio assets. Browser access to the ZIP failed because of its content type; a bounded public download succeeded. The access log retains both outcomes.

Six documentation observations distinguish verified metadata from unresolved legal applicability and record access. CVM's current consolidated regulation is recorded as a lead; no universal cap or cure deadline is asserted. DOJ guidance supports the distinction between search methods and search results: a missed record alone does not establish an unlawful search. No agency contact, account creation, paid database use, bulk download or active technical probing occurred.

Validation passed **17 checks: nine artifact/provenance checks and eight synthetic arithmetic checks**. The latter cover positive and nonpositive lower bounds, equality at the cap, duplicate positions, wrong dates, negative denominators, unsupported negative exposure and an unknown measurement basis. They validate software behavior, not the legal applicability or feasibility of a real investigation.

## Ranking and reproduction

Consequence (1–5), testability (1–5), join-route confidence (1–3) and cost (1–4) remain separate. The editorial priority score is `10 × consequence + 3 × testability + 2 × join confidence − 2 × cost`; separate consequence and testability ranks are supplied. Scores are judgments, not probabilities of wrongdoing. A strong hypothetical identifier route is not an identity match.

Run `python code/design.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py` from this folder. Export/ranking/validation are deterministic; the existing model environment authored the source decisions and card text. Regeneration does not download data or call APIs. The original source texts, line ranges, SYS/AP IDs and hashes remain linked through `sources.jsonl` and each card's manifest.

The ZIP `checkpoints/consequential-expansions-through-04.zip` includes the corrected current outputs for expansions 01–04. Earlier ZIPs remain preserved in Git and are excluded from the new bundle to avoid recursive copies. Historical delivery receipts refer to those earlier separately committed artifacts.

## Remaining work

Independent novelty review of Q01–Q03 and V01 remains pending. The most valuable feasibility steps are one exact operative fund/class mandate with its dated measurement rule; a maintenance component certificate/life-history chain; and an actual case-number bridge for the request-response route. The current work remains source-level discovery, so these are dependencies, not instructions to bulk-execute tests. Original records, current case-specific legal applicability and coverage would need separate verification. No global exhaustion claim is made, and future screens should begin with a distinct consequential predicate rather than reword these cards.

Automatic weekly ChatGPT allowance and model-token telemetry are unavailable. The last user-reported figure was **88% remaining at 18:50 UTC**, compared with an earlier 99%; that 11 percentage-point change cannot be attributed solely to this task. Paid external API calls: **zero**.

## Detailed cards
'''
parts=[intro]
for c in C:
 parts.append(f"\n### {c['test_id']} — {c['title']}\n\n{c['kind']}; priority {c['priority_rank']}; consequence {c['consequence']}/5, testability {c['testability']}/5, join confidence {c['join_route']}/3, cost {c['cost_tier']}/4.\n")
 for k,label in [('initial_observation','If'),('expected_observation','Then'),('basis','Basis'),('operational_join','Join'),('temporal_geographic_scope','Scope'),('ordinary_explanations_and_disqualifiers','Ordinary explanations / disqualifiers'),('mandatory_evidence','Required evidence'),('next_cheapest_check','Next cheapest check'),('novelty_comparison','Novelty'),('access_evidence','Access evidence')]:
  v=c[k];parts.append('\n**'+label+':** '+('; '.join(v) if isinstance(v,list) else v)+'\n')
 parts.append('\n**Provenance:** '+'; '.join(f"{s['sys_id']} {s['name']} ({s['file']}:{s['line_start']}; {', '.join(s['all_ap_ids'])})" for s in c['source_manifest'])+'\n')
 parts.append('\n**Documentation IDs:** '+(', '.join(c['documentation_ids']) or 'No new full-text documentation acquired; catalog-only implementation lead.')+'\n')
(P/'README.md').write_text(''.join(parts))
(P/'generation-provenance.json').write_text(json.dumps(dict(date='2026-10-04',method='Existing model environment; no new paid API calls. Deterministic export, ranking, deduplication decisions and arithmetic validation.',instruction='Continue beyond eight-priority checkpoint. Explore investment mandates, precise custody assertions and evidence independence. Retain a new mechanism only when its predicate differs substantively. Save rejected/deferred candidates and do not mistake metadata verification for feasibility.',novelty_decisions='V01 proposed new; REF-REL, REF-SEARCH, REF-EVID treated as refinements; independent review pending.',parent_baseline_commit='85fdce9946e8c973845df2d6e4501086db01f079',paid_calls=0,token_counter='unavailable'),indent=2)+'\n')
(P/'progress-ledger.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in [dict(stage='screen',predicates=12,distinct_new_proposed=1,refinements=3,rejected=4,deferred=3,refinement_deferred=1),dict(stage='metadata',source='CVM CDA dictionary',bytes=10094,holdings_records=0,failed_browser_attempt=1,bounded_download_succeeded=True),dict(stage='validation',artifact_checks=9,synthetic_arithmetic_checks=8,passed=17,matched_cases=0),dict(stage='checkpoint',reviewed_cards=48,pending_novelty_review=4,provisional_total=52,all_catalog_predicates_exhausted=False)]))
used={s for r in R for s in r['source_ids']}
(P/'source-coverage.jsonl').write_text(''.join(json.dumps(dict(sys_id=s['sys_id'],name=s['name'],screened_in_this_batch=int(s['sys_id'][-4:]) in used,candidate_ids=[r['candidate_id'] for r in R if int(s['sys_id'][-4:]) in r['source_ids']]))+'\n' for s in jl('sources.jsonl')))
files=[f for f in sorted(P.rglob('*')) if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts and f.name not in ['artifact-checksums.json','delivery-receipt.json']]
(P/'artifact-checksums.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2)+'\n')
z=P/'checkpoints/consequential-expansions-through-04.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for i in range(1,5):
  root=P.parent/f'consequential-expansion-0{i}'
  for f in sorted(root.rglob('*')):
   if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts:a.write(f,pathlib.Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as a:assert a.testzip() is None
print(json.dumps(counts,indent=2));print('ZIP',z.stat().st_size,hashlib.sha256(z.read_bytes()).hexdigest())
