import pathlib,json,collections,hashlib,zipfile
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
C=jl('cards.jsonl');G=jl('predicate-coverage.jsonl');S=jl('source-coverage.jsonl')
counts=dict(proposed_new_formulations=4,refinements=1,detailed_cards=5,coverage_predicates_mapped=24,predicates_screened=16,predicates_queued_unexamined=8,screened_not_developed=11,source_descriptions_manifest=344,source_descriptions_mapped_including_queued=54,source_descriptions_in_screened_predicates=40,new_single_document_observations=1,matched_record_chains=0,confirmed_end_to_end_feasible=0,positive_findings=0,production_artifact_checks=13,synthetic_arithmetic_checks=6,documentation_entries=13,new_failed_access_requests=0,access_routes_not_attempted=['EPO OPS credentials','Paris MoU stored reuse restricted'],prior_expansion_corrected_new=12,prior_expansion_corrected_refinements=4,prior_non_refinement_detailed_cards=44,provisional_cumulative_non_refinement_cards=48,prior_active_source_pair_rows_unchanged=1715,prior_quarantines_unchanged=15,independent_novelty_review_of_this_batch='not_yet_received',paid_external_api_calls=0,weekly_chatgpt_allowance='unavailable',model_token_counter='unavailable')
(P/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
intro='''# Consequential expansion 02 — 4 October 2026

This batch develops **four proposed new investigative formulations and one refinement**. The most promising is a precise procurement calculation: did changed quantities eliminate the winning bid’s original price advantage over a compliant rival? Others examine an explicit zero-structure resettlement inventory, a drug advertisement’s authorized indication, and potentially incompatible exclusive patent grants. These are conditional tests, not findings.

There are **24 mapped substantive predicates: 16 screened and eight still unexamined**. Five screened predicates became cards; eleven were deferred, rejected or recognized as existing specializations. The map names 54 sources, but only 40 appear in screened predicates. All 344 source descriptions remain in the source manifest. The other 290 sources are not newly examined simply because they appear in that manifest. The earlier 344-source review remains a baseline, not proof that every meaningful combination is exhausted.

The previous expansion was independently reviewed and corrected to **12 new formulations and four refinements**, leaving **44 cumulative non-refinement detailed cards** before this batch. X01 refines H04; X10 specializes E02. With the four current proposals the provisional total is **48**, pending independent novelty review. The earlier longlist remains **1,715 active provisional source-pair rows and 15 quarantines**. Cards, mechanisms and implementation rows are different counting units: do not add them together or describe them as thousands of independent discoveries.

## Start here

`cards.csv` and `cards.jsonl` contain the five full recipes, required original records and source-level SYS/AP provenance. `predicate-coverage.csv` is the deliberate coverage map, including exclusions and the eight outstanding questions. `source-coverage.csv` tells exactly which of the 344 sources this pass touched and distinguishes queued ideas from screened ones. `sources.jsonl` retains original join-field descriptions and hashes.

The first cheap procurement check is to find one priced bid schedule and an implementation document referencing the exact same contract. A World Bank project ID is not sufficient: one project can contain many contracts. Without rival unit prices and equivalent certified quantities, stop. The provided arithmetic helper rejects missing items, mismatched units/currencies and ineligible comparators. It cannot establish that the rival could have performed the revised work or that the winner manipulated quantities.

## Evidence and practical limits

Thirteen official-documentation entries were recorded. One public SEC exhibit was opened to inspect licence definitions and carve-outs; it was not matched to a purportedly conflicting agreement, and nothing adverse is asserted about its parties. **Zero matched record chains, zero confirmed end-to-end feasible routes and zero positive findings** were produced. The patent API’s credential requirement remains unresolved; no account was created. Paris MoU’s displayed reuse/storage restriction was recorded without storing its vessel rows or attempting extraction.

Drug-product guidance does not establish that a particular ad is unlawful. Image evidence cannot establish occupancy, displacement, compensation eligibility or a missing payment. Two exclusive licences can coexist through master/sublicence relationships, differing fields, territories, rights or dates. These ordinary explanations are mandatory gates in the cards.

## Ranking and validation

Consequence 1–5 estimates public-interest significance if a predicate proves true. Testability 1–5 measures evidence-route maturity; current cards are at most 2 (documentation/components, not demonstrated chains). Join route 1–3 denotes provisional person bridges, multi-field conditional routes or precise candidate identifiers; none certifies an actual match. Cost tier 1–4 estimates rising document/access/identity effort, with no measured cash/time promise. Separate ranks are provided. Composite = `10 × consequence + 3 × testability + 2 × join route − 2 × cost tier`; weights are editorial judgments.

**Thirteen production-artifact checks and six synthetic arithmetic checks pass.** The latter verify a fictional bid calculation and rejection gates, not any real procurement. Artifact checks verify counts, source provenance, safeguards and ranking; they do not certify semantic novelty, legal applicability or wrongdoing. No independent novelty review of this second batch has yet been received.

## Audit and reproduction

The prior correction commit is `5a53612c2032e0801504528bee8e18b6d1a476dd`. The downloadable bundle contains both this expansion and the corrected first expansion; its original ZIP remains preserved in Git history and its original folder. Corrections include dated LDA evidence (the House-linked PDF revised February 28, 2025), separate ASIC asset/liability gates, explicit actual-security retrieval dependencies, no assumed FARA creative identifier, and X14’s relationship to the earlier same-document comparison.

Run `python code/design.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py` from this folder. No command makes network or paid API calls. Source selection, novelty judgments and card text are model-authored and visible in the scripts; code exports, ranks, checks and performs the limited arithmetic. Official pages were inspected separately and cited in `evidence/documentation.jsonl`; a single-document observation and non-attempted access routes are logged separately. The generation instruction was to seek previously unexamined consequential predicates, favor exact document identities and inexpensive falsification, compare against prior work, preserve refinements without counting them new, and leave explicit unresolved coverage.

Weekly ChatGPT allowance and model-token telemetry were unavailable. Paid external API calls: **zero**. No bulk investigation, outreach, new account, paid download or active probing occurred.

## Remaining coverage

Eight priorities remain explicitly unexamined, not rejected: permitted-donor trading conditions; insurance representations against engineering findings; charity political-benefit transactions; land-transfer consent clauses; unit-outage market disclosures; borrower debt perimeter; claimant compensation completeness; and component-level maintenance certifications. Each map row names the sources, prior mechanism to compare, original records needed and reason it is not yet executable. Some will likely be refinements. No exhaustion claim is made.

## Detailed cards
'''
parts=[intro]
for r in C:
 parts.append(f"\n### {r['test_id']} — {r['title']}\n\n{r['kind']}; priority rank {r['priority_rank']}. Consequence {r['consequence']}/5; testability {r['testability']}/5; join route {r['join_route']}/3; cost tier {r['cost_tier']}/4.\n")
 for key,label in [('initial_observation','If'),('expected_observation','Then'),('logical_or_legal_basis','Basis'),('operational_join','Exact join'),('timing_geography','Scope'),('ordinary_explanations_and_disqualifiers','Ordinary explanations and disqualifiers'),('required_original_records','Required original records'),('next_cheapest_check','Next cheapest check'),('novelty_comparison','Novelty'),('access_evidence','Access evidence'),('reproducible_method','Method')]:
  v=r[key];parts.append('\n**'+label+':** '+('; '.join(v) if isinstance(v,list) else v)+'\n')
 parts.append('\n**Provenance:** '+'; '.join(f"{s['sys_id']} {s['name']} ({s['file']}:{s['line_start']}; APs {', '.join(s['all_ap_ids'])})" for s in r['source_manifest'])+'\n')
 parts.append('\n**Evidence references:** '+', '.join(r['documentation_ids'])+' in evidence/documentation.jsonl.\n')
(P/'README.md').write_text(''.join(parts))
(P/'progress-ledger.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in [dict(stage='prior_corrections',new=12,refinements=4,prior_cumulative=44,original_checkpoint_preserved=True),dict(stage='coverage_mapping',predicates=24,screened=16,queued_unexamined=8,source_ids_in_screened=40),dict(stage='card_development',new_proposed=4,refinements=1,not_developed_from_screened=11),dict(stage='validation',artifact_checks=13,synthetic_checks=6,empirical_chains=0),dict(stage='remaining',gap_ids=[g['gap_id'] for g in G if g['status']=='queued_unexamined'],overall_exhausted=False)]))
# Archive checksums cover inputs and outputs, excluding archives/receipts generated after publishing.
for root in [P.parent/'consequential-expansion-01',P]:
 files=[f for f in sorted(root.rglob('*')) if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts and f.name not in ['artifact-checksums.json','delivery-receipt.json']]
 (root/'artifact-checksums.json').write_text(json.dumps({str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2)+'\n')
z=P/'checkpoints/consequential-expansions-reviewed-plus-02.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for root in [P.parent/'consequential-expansion-01',P]:
  for f in sorted(root.rglob('*')):
   if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts:a.write(f,pathlib.Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as a:assert a.testzip() is None
print(json.dumps(counts,indent=2));print('ZIP',z.stat().st_size,hashlib.sha256(z.read_bytes()).hexdigest())
