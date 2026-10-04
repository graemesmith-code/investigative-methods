import pathlib,json,hashlib,zipfile,collections
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
cards=jl('cards.jsonl'); ranks=jl('cross-batch-ranked-routes.jsonl'); screen=jl('candidate-screen.jsonl')
counts=dict(primary_manifest=344,primary_sources_this_batch=len(set(s for c in cards for s in c['primary_source_ids'])),screened_branches=9,screened_branch_dispositions=dict(collections.Counter(r['disposition'] for r in screen)),proposed_new=2,new_refinements=1,previously_reviewed_non_refinement_formulations=53,provisional_total_if_accepted=55,ranked_detailed_cards=70,ranked_refinements=15,documentation_entries=11,partial_document_render=1,records_acquired_this_batch=0,matched_investigations=0,positive_findings=0,confirmed_end_to_end_feasible=0,checkpoint_checks_passed=14,artifact_checks=8,synthetic_checks=6,paid_external_api_calls=0,weekly_last_user_report_remaining=88,weekly_telemetry='unavailable')
(P/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
intro='''# Two proposed tests and a seismicity refinement — 4 October 2026

**53 previously reviewed formulations, plus two proposed additions pending independent review.** This checkpoint offers an honest provisional total of 55, not 5,000. The complete ranking contains 70 detailed cards: those 55 formulations and 15 refinements. None is a demonstrated wrongdoing finding or a confirmed end-to-end feasible investigation.

The two additions test whether media explicitly attributed to a later incident already existed before it, and whether an earlier publicly available clinical-trial disclosure contains every required element of one patent claim. The Alberta refinement checks the actual scope of a hydraulic-fracturing seismicity order and what evidence would establish continued operation or unauthorized restart. It improves an existing approval-before-action test and is not counted as new.

## What a journalist can try cheaply

Start J01 by reading the exact caption. If it does not assert capture during the event, stop. If it does, seek one authenticated earlier response for the original media itself. An old web page containing a later replayed image proves nothing about the image's age. Even a successful contradiction concerns that particular attribution, not the truth of the whole incident.

Start J02 with one granted US claim, one historical trial version and one discriminating claim limitation. Ingredient overlap or a trial start date is insufficient. The complete claim-specific priority chain, public availability, enabling disclosure, statutory regime and exceptions require specialist review before asserting invalidity. No patent/trial pair has been acquired here.

For Alberta, obtain actual stage-level operation evidence before comparing it with a qualifying seismic event. The November 2024 Order 2A rescinds Order 2 and has a specific geographic and formation scope. Its 4.0 ML threshold cannot be replaced casually with a catalog's preferred Mw magnitude. A multi-day operation end date does not prove injection after an event; missing indexed consent does not prove there was no consent. No operation/event case has been tested.

## Count, coverage and ranking

All 344 normalized descriptions remain in the manifest, with SYS/AP identifiers, original-file line ranges and text hashes. Earlier work reproduced 267 explicitly labeled descriptions in Rabbit2(1).txt plus 77 in Rabbit3.txt, and 1,555 systems / 2,516 access points across the five current volumes. All 117,992 possible directed pairs were enumerated for policy screening; that does not mean every pair received individual documentary research. The earlier broad longlist contained 1,730 conditional pair rows, subsequently 1,715 active and 15 quarantined. Those rows must not be confused with independently defensible mechanisms.

This pass revisits seven primary sources and records nine decision branches: three main proposals and six reasons to reject or defer weaker variants. Nine branches are not nine hypotheses. The 5,000 target remains unjustified; useful further work depends increasingly on original records and operative instruments, rather than more combinations of shared fields.

The cross-batch CSV/JSONL sorts only by readiness tier, next-check effort tier, then test ID for deterministic ties. Original consequence/testability values and scale labels remain separately visible; incompatible scales never enter the sort. Readiness 1 indicates an earlier demonstrated identifier/document bridge, 2 a one-sided sample or anatomy, 3 unresolved original evidence, and 4 known access/reuse barriers. All three current cards remain at readiness 3. This is a ranking of next checks, not the cost or probability of a meaningful finding. N01 remains at tier 3: an unrelated World Bank audit did not validate its OECD/IATI route.

## Evidence and limits

Eleven official documentation entries support this pass. The ClinicalTrials guide rendered incompletely, and no historical study record was verified. No restricted Airwars material was accessed, no account was created, and no bulk AER dataset was downloaded. External AGS and USPTO support is explicitly identified without inventing Rabbit SYS identifiers. Catalog availability remains unverified until the actual needed record is obtained; documentation alone is not a completed join.

Fourteen checks pass: eight artifact/provenance/ranking checks and six synthetic chronology cases. The chronology helper compares bytes and bounded timestamps after externally supplied authentication gates; it does not authenticate media or interpret captions itself. Synthetic examples are not real incidents.

Weekly usage is unmetered. The latest user report was 88% remaining at 18:50 UTC; the earlier 99% figure does not establish this task's consumption. Paid external API calls: zero. No new API sample calls or matched records in this batch.

## Files and reproduction

Use `cards.csv` or the detailed cards below first. `cross-batch-ranked-routes.csv` contains all 70 cards with source-file pointers. JSONL retains nested evidence requirements. `candidate-screen`, `source-coverage`, `sources`, `evidence/documentation.jsonl`, `evidence/access-log.jsonl`, and the provenance/ledger files form the audit trail. Run `python code/build.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py` from this directory; these scripts reuse saved judgments and make no network calls.

The downloadable ZIP includes the canonical 32-card baseline and current expansions 01–07. Historical ZIPs remain preserved in Git and are excluded from this bundle. Earlier delivery receipts describe their historical artifacts. Original Rabbit texts remain in the repository under the paths recorded in the manifests.

## Detailed cards
'''
parts=[intro]
for c in cards:
 parts.append('\n### '+c['test_id']+' — '+c['title']+'\n\nStatus: '+c['kind']+'.\n')
 for k in ['initial_observation','expected_observation','basis','operational_join','temporal_geographic_scope','ordinary_explanations_and_disqualifiers','mandatory_evidence','next_cheapest_check','novelty_comparison','access_evidence']:
  v=c[k];v='; '.join(v) if isinstance(v,list) else v
  parts.append('\n**'+k.replace('_',' ').capitalize()+':** '+v+'\n')
(P/'README.md').write_text(''.join(parts))
(P/'ranking-rubric.json').write_text(json.dumps(dict(ordering=['readiness_tier','effort_tier','test_id'],unit='detailed card, including refinements',raw_scores='Preserved with original scales, not comparable across batches and not sorting keys',next_check_not_full_investigation=True,new_cards_readiness=3),indent=2)+'\n')
(P/'generation-provenance.json').write_text(json.dumps(dict(instruction='Fresh creative pass: independently assess media chronology, trial-disclosure patent anticipation and Alberta seismicity; preserve prior ranking corrections and distinguish additions from applications.',generation='Existing model environment; manual source-level reasoning and primary documentation checks; deterministic code exports/validation',independent_review='53 accepted previously; J01 and J02 proposed pending parent review',paid_calls=0,records_acquired=0,limitations='No claim of exhaustiveness beyond the completed policy sweep and recorded individual source reviews'),indent=2)+'\n')
(P/'progress-ledger.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in [dict(stage='prior_checkpoint',accepted=53,ranked=67),dict(stage='new_screen',branches=9,primary_sources=7,proposed_new=2,refinement=1),dict(stage='documentation',entries=11,partial_render=1,case_records=0),dict(stage='validation',artifact=8,synthetic=6,passed=14),dict(stage='delivery',accepted=53,pending_independent_review=2,provisional=55,ranked=70,full_case_feasible=0)]))
fs=[f for f in sorted(P.rglob('*')) if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts and f.name not in ['artifact-checksums.json','delivery-receipt.json']]
(P/'artifact-checksums.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in fs},indent=2)+'\n')
z=P/'checkpoints/consequential-discovery-ranked-through-07.zip'
roots=[P.parent/'source-pair-completeness']+[P.parent/f'consequential-expansion-0{i}' for i in range(1,8)]
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for root in roots:
  for f in sorted(root.rglob('*')):
   if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts:a.write(f,pathlib.Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as a:assert a.testzip() is None
print(json.dumps(dict(path=str(z),bytes=z.stat().st_size,sha256=hashlib.sha256(z.read_bytes()).hexdigest())))
