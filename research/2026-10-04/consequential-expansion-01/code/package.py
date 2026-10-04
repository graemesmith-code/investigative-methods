"""Produce readable review material and a bounded follow-on screen, without APIs."""
import json,csv,pathlib,collections,subprocess,zipfile,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
follow=[
('Y01',[71,24],'Ship broadcast identity in physically incompatible places','defer_missing_raw_observations','T01; S04','Two products can reuse one AIS feed. Raw timestamp/position provenance, identifier reassignment and track interpolation must be excluded before identity deception is a distinct supported test. A sanctions label does not repair this gap.'),
('Y02',[76,78],'Duplicate aircraft identity in simultaneous flight tracks','defer_identity_and_physics','T01','Registration is not broadcast identity, ownership is not operation, and decoded tracks are not independent observations. No raw-message schema or physically constrained observation was established in this pass.'),
('Y03',[111,64],'Same resource pledged to incompatible creditors','defer_missing_legal_instruments','D05','Project/borrower overlap cannot establish the collateral, priority, exclusivity or operative amendment. Requires two actual executed financing/security instruments and asset schedule; current catalog fields do not provide those facts.'),
('Y04',[82,83,84],'Arms delivery exceeds public sales approval','reject_noncomparable_stage','F02','DSCA notification is a possible sale, not necessarily the final export authorization or delivered quantity. SIPRI and UNROCA cover differing stages/categories; a notification-to-delivery count is not a defensible authorization breach.'),
('Y05',[246,252],'Patent omits government rights despite research grant','defer_scope_and_prior_art','H03','Patent funding acknowledgement and award match are only entry points. Subject-invention status, exact funding instrument, operative law, invention timing and title-election/disclosure records are needed. Public-funded-to-patent overlap was already covered; no additional verified obligation established here.'),
('Y06',[117,118],'Payments in two lobbying systems are inconsistent','reject_noncomparable_accounts','I05; X04; X06','LDA estimates and FARA principal-level receipts/disbursements have different scope and accounting windows. Difference alone is not a missing-money test; specific contradictory declarations and traceable ad items are already developed in X04/X06.')]
rows=[dict(candidate_id=i,source_ids=s,idea=t,disposition=d,nearest_existing=n,reason=r,review_basis='bounded model-authored follow-on screen; catalog and prior mechanism comparison only; no new documents or records') for i,s,t,d,n,r in follow]
(P/'follow-on-screen.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
with (P/'follow-on-screen.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
cards=[json.loads(x) for x in (P/'new-formulations.jsonl').read_text().splitlines()]
screen=[json.loads(x) for x in (P/'candidate-screen.jsonl').read_text().splitlines()]
counts=dict(screened_candidates=40,initial_screen=34,follow_on_screen=6,new_conditional_mechanisms=12,existing_mechanism_refinements=4,not_developed=24,exact_card_duplicates=0,semantic_novelty_review='independent review supplied through parent; X01 and X10 reclassified; no empirical truth certification',detailed_cards=16,baseline_detailed_cards=32,cumulative_detailed_cards_excluding_refinements=44,baseline_active_pair_rows_unchanged=1715,baseline_quarantined_rows_unchanged=15,original_source_manifest=344,source_descriptions_used_in_screen=len({i for r in screen+rows for i in r['source_ids']}),documentation_entries=24,documentation_access_failures=1,new_record_probes=0,tests_executed_against_records=0,confirmed_feasible_end_to_end=0,positive_findings=0,artifact_checks_passed=18,new_paid_external_api_calls=0,weekly_chatgpt_allowance='unavailable',model_token_counter='unavailable')
(P/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
intro='''# Consequential source-test expansion — 4 October 2026

This checkpoint proposes **12 proposed new conditional investigative mechanisms**, plus **four refinements of existing mechanisms**. It develops 16 detailed cards from 40 explicitly screened ideas; 24 ideas were not developed. These are ways to look for evidence, not allegations or results. No records were matched or tests executed in this expansion; no complete route is yet confirmed executable.

The strongest next checks follow waste from a reporting sender to its actual authorized receiver, compare a fixed resource-contract obligation with covered receipts, and compare direct physician payments with an explicit article disclosure. Other useful directions concern required reclamation security, precise assay quotations, double-counted clinical participants, and cross-border deregistration asset conditions. Each card supplies falsifiers and the next cheapest check.

The prior 32 detailed cards remain intact, bringing the cumulative total to **44 detailed cards excluding the four refinements**. The earlier longlist remains **1,715 active provisional source-pair rows plus 15 quarantined rows**. Those rows and these mechanisms are different counting units and must not be added together. We have not reached 5,000 defensible independent tests and have not padded the output to do so.

## Use this checkpoint

Start with `new-formulations.csv` or the cards below. Read the mandatory evidence and ordinary explanations before choosing a case. `sources.jsonl` preserves all 344 normalized Rabbit descriptions with original SYS/AP provenance. A catalog description documents a proposed route; it does not confirm current availability. RCRAInfo historical permit/manifest evidence is explicitly declared as a supporting extension outside the 344-source frame.

This pass prioritizes public-health evidence, political disclosure, extractive obligations and public financial exposure after the earlier sanctions-first sweep. All 344 descriptions had received source-level review in the earlier baseline; this expansion is a targeted mechanism search, not a new exhaustive review of every directed pair. The second bounded screen adds six reasoned exclusions rather than stretching weak overlaps into new cards. No claim is made that all future discoveries are exhausted.

## Ranking

Scores are editorial triage, not measured likelihoods of wrongdoing. Consequence (1–5) estimates potential public-interest harm if the predicate proves true. Feasibility (1–5) measures route maturity: 1 is conceptual/limited documentation, 2 is documented components, 3 would require relevant records, 4 a demonstrated linked component and 5 an end-to-end reproducible test. Every current card is at most 2. Join route (1–3) distinguishes provisional person/name bridges, multi-field conditional routes and precise candidate identifiers; it never certifies an actual identity match. Burden (1–4) estimates increasing document, identity, access and historical-record effort. No dollar/time estimate is empirically verified.

The composite is `10 × consequence + 3 × feasibility + 2 × join route − 2 × burden`. Importance, feasibility and composite ranks are separate columns across all 16 cards, including the four labeled refinements. Filter `kind=new_mechanism` when seeking new ideas. Composite weights are subjective and editable. Small rank differences should not determine a newsroom investigation.

## Evidence and limits

There are 24 official-documentation entries, including one failed CISA access attempt recorded explicitly. No record availability is confirmed by those entries. Current ASIC guidance supports the voluntary-deregistration asset-condition framework, but route, date, economic interest and exceptions remain case-specific. E07 is a historical 2016 guidance copy, and E09 is an older semiannual instruction sheet. Neither is labeled current. E24 is the official House-linked guidance, cover revised February 28, 2025 and rechecked on October 4, 2026; its introduction explicitly disclaims force of law. Case-specific and filing-date applicability still require checking. NIH reporting tests must use submission dates and applicable exceptions, including BESH policy changes. The cybersecurity refinement has no verified applicable current deadline and permits no active probing.

Eighteen production-artifact checks pass. They test counts, provenance, ranking reproducibility, evidence references and required safeguards, not the truth of any allegation or legal applicability. Exact fingerprint uniqueness does not demonstrate semantic independence; novelty was reviewed manually against prior mechanisms and cards. Independent review identified X01 as an H04 refinement and X10 as an E02 commercial-sourcing specialization; both corrections are applied here. The other twelve formulations remain provisional and conditionally distinct, not record-validated. The original ZIP is preserved as a superseded snapshot; current CSV/JSONL and this guide contain the correction.

## Reproduce and audit

From this directory run `python code/screen.py`, `python code/author.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py`. These commands make no network/API calls. Authoring scripts contain the model-authored judgments; deterministic code exports, scores and checks them. The baseline is pinned in `baseline-manifest.json`; earlier experiments are preserved. `candidate-screen.*` and `follow-on-screen.*` retain rejected, deferred, duplicate and supporting ideas with reasons. `evidence/documentation.jsonl` records sources and limited observations; `evidence/access-log.jsonl` records the failed request.

The generation instruction was to seek consequential mechanisms beyond the prior bounded sanctions-first pass, compare each with the 65 original mechanism definitions and 32 detailed cards, make every necessary third source explicit, and reject identifier coincidences, unsupported absences and parameter-only variants. Generation and review used the existing model environment. No new paid external API calls were made. Neither a weekly ChatGPT allowance meter nor a model token counter was available; a historical user-reported balance is not current telemetry.

The next work is selective evidence validation: obtain one lawful, small record chain for a high-ranked mechanism, then reassess identity, historical coverage and cost. Unresolved routes include actual historical security held, full contractual amendments, original article disclosures, raw broadcast provenance and operative security instruments. Missing evidence remains a blocker to executing the relevant test, not to preserving the conditional discovery card.

## Detailed cards
'''
parts=[intro]
for r in cards:
 parts.append(f"\n### {r['test_id']} — {r['title']}\n\nKind: {r['kind']}. Composite rank {r['triage_rank']}; consequence {r['consequence_score']}/5, feasibility {r['feasibility_score']}/5, join route {r['join_route_score']}/3, burden {r['burden_tier']}/4.\n")
 for key,label in [('initial_observation','If'),('expected_observation','Then'),('possible_finding_and_basis','Why it matters / basis'),('operational_join','Join'),('temporal_geographic_scope','Scope'),('ordinary_explanations_and_falsifiers','Ordinary explanations / disqualifiers'),('mandatory_evidence','Required evidence'),('next_cheapest_check','Next cheapest check'),('novelty_vs_baseline','Novelty'),('access_status','Access evidence')]:
  v=r[key];parts.append(f"\n**{label}:** "+('; '.join(v) if isinstance(v,list) else v)+'\n')
 parts.append('\n**Catalog provenance:** '+ '; '.join(f"{s['sys_id']} {s['name']} ({s['file']}:{s['line_start']})" for s in r['source_manifest'])+'\n')
 parts.append('\n**Documentation:** '+', '.join(r['documentation_ids'])+' in evidence/documentation.jsonl. All case applicability remains unverified.\n')
(P/'README.md').write_text(''.join(parts))
(P/'progress-ledger.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in [dict(stage='initial_screen',considered=34,developed_new=12,refinements=4,not_developed=18),dict(stage='follow_on_screen',considered=6,developed_new=0,not_developed=6,scope='additional transport identity, collateral, arms, patent obligation and lobbying accounts checks'),dict(stage='validation',artifact_checks_passed=18,record_tests_executed=0,coverage='bounded expansion complete; no global exhaustive-mechanism claim',next='selective source-record chains and independent novelty review')]))
# Independent structural guards for follow-on screen and manifest.
source_ids={int(json.loads(x)['sys_id'][-4:]) for x in (P/'sources.jsonl').read_text().splitlines()}
assert all(set(r['source_ids'])<=source_ids for r in rows)
assert len({r['candidate_id'] for r in rows+screen})==40
assert counts['new_conditional_mechanisms']+counts['existing_mechanism_refinements']+counts['not_developed']==40
print(json.dumps(counts,indent=2))
