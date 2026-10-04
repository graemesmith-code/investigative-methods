import pathlib,json,hashlib,zipfile
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
counts=json.loads((P/'counts.json').read_text());counts['checkpoint_checks_passed']=13;counts['prior05_checks_passed']=19
(P/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
I=jl('cross-batch-ranked-routes.jsonl');R=jl('route-screen.jsonl')
intro='''# Access-grounded routes and cheapest-next-check ranking — 4 October 2026

**The count stays at 53 reviewed non-refinement formulations.** This checkpoint adds no new predicate. It checks six concrete routes, saves one EIA schema response and one bounded data row, inspects one public audit for document structure, and ranks all **67 current detailed cards: 53 non-refinement formulations and 14 refinements**. Useful applications are not counted as new tests merely because their source changes.

The most valuable result is a clearer choice of what to try next. Clinical-trial/publication, World Bank project/document and OONI/ASN routes have demonstrated identifier links in earlier small samples. They lead the ranking. That makes the next source check cheaper; it does not establish the full investigative hypothesis as executable or any wrongdoing.

## Cheapest next checks across the batches

__RANK_TABLE__

`cross-batch-ranked-routes.csv` and JSONL contain all 67 cards, source-file pointers, next checks and reasons. The ranking is an editorial readiness/effort ordering, not a statistical estimate of success. Tier1 means an identifier/document bridge was demonstrated; tier2 means one-sided metadata/sample or document anatomy; tier3 means original evidence remains unresolved; tier4 marks known access/reuse blocks. Within a tier, effort1–4 runs from a short existing-document check to unavailable instruments or access gates. These effort tiers are new comparative judgments, not quoted prices or elapsed-time estimates. Original feasibility descriptions and raw score values, original field names and scale labels are preserved separately, including baseline testability_score. Missing original scores remain null and never become zero. Baseline public-interest scores and later 1–5 consequence scores are incomparable and never enter the sorting key. Exact readiness/effort ties use test ID only for deterministic display; neighboring positions within a tie are not substantive priority differences. This ranks readiness for the next check, not the cost of reaching a meaningful investigative finding. Potential consequence scores describe a material case if established, not likely newsworthiness or yield. No card is marked full-case feasible.

## What the concrete checks established

**EIA:** Two free public API calls using the documented demonstration key returned metadata and exactly one January2024 plant-period row. The fields include plantCode, fuel/source and prime-mover dimensions, net generation, total-consumption-btu, and consumption-for-eg-btu. The saved row is an ALL aggregate, not proof of complete physical inputs. No balance was calculated. Inputs are operator-reported measurements or estimates; this is not an independent observation. The API's large total-count/warning is preserved, but only one row was requested and obtained.

**World Bank:** One five-page public audit identifies a project through its URL, a loan on the cover and a financial-year interval. Its tables offer component-level expenditure/certification and implementing-unit advance categories. They do not supply B02's required invoice/settlement chain. This supports a separate audit-accounting application—checking what “spent” means—but supplies no OECD/IATI bridge for N01. N01 remains at its original evidence-supported readiness tier 3. No new predicate, duplicate-payment finding or investigation of the sample project is claimed. Later responses and resolution were not researched.

**Norwegian ships:** Supporting Rabbit source SYS-0854/AP-1802 had a stale404 route. Current official documentation now supplies a production search link, IMO and owner-organization search fields, and a publisher-described historical-search route. The browser exposed no actual ship record. Free search is distinct from paid certification. Bareboat/title/flag/owner/mortgage roles must be reconciled before asserting incompatible registrations. This improves S03/S04/R03 applications without adding a predicate or clearing Equasis restrictions.

**Canadian ships:** Recent historical extracts require an application and payment. No extract was ordered. A current registry query cannot substitute for a historical instrument; the free older archival index has a different time scope.

**FAA:** The current layout confirms serial/model, ModeS and document-index fields. Document types concern ownership, security and related instruments; this is not a component-maintenance history. Public names can be withheld. No 60MB database was downloaded and no aircraft was matched.

**Environmental attributes:** Eleven recorded text patterns were searched across all1555 current Rabbit source blocks in five volumes, excluding the older duplicate Rabbit2 and front matter. No serial-level registry candidate matched. This is a reproducible bounded catalog search, not proof no registry exists elsewhere or under other terminology. Issuer/project names cannot replace credit serials, retirement beneficiaries and operative rights.

## Review repairs included

Independent review accepts B01/B02, bringing the non-refinement total to53. B01 now requires an issuer claim to state or demonstrably rely on the exact quantities tested. Otherwise an imbalance is only an EIA reporting-quality lead. B02's helper uses `permitted_recovery_upper`: the combined recovery cap can be below invoice cost and is separate from each funder's individual cap. The fixture with a100 invoice,60 combined cap and70 completed recoveries flags the excess. The helper does not check individual funder caps. Expansion05 now passes19 checks.

This checkpoint passes13 artifact/provenance checks, including the267+77 source count,1555-block scan, bounded API response, supporting-source hash and complete67-card inventory. An initial validation attempt incorrectly matched the text “refinement” inside “non_refinement”; the test was corrected to explicit categories. The failed attempt is preserved alongside the passing log. These checks do not validate a substantive case.

## Limits and next work

Marginal yield has fallen: six grounded route checks produced **zero new predicates**. Missing original instruments, legal scope, historical identity and settlement-level access are now the main limits. The public audit example demonstrates that limitation directly rather than assuming it. This is not a proof that every remaining catalog opportunity has been exhausted. Further productive work should use the ranked next checks to establish a missing bridge or find a genuinely different operative predicate; broad source permutations and transplanted conservation laws would not justify more counts.

The prior1,715 active provisional pair rows and15 quarantines remain a separate counting unit. The5,000 target is not supported. No bulk investigation, paid record, new account, public outreach or finding was produced.

## Audit and reproduction

Run `python code/catalog_scan.py`, `python code/build.py`, `python code/validate.py`, then `python code/package.py`. These local scripts reuse saved evidence and make no network calls. The two actual EIA calls and public document/page inspections are logged separately. Source selection and judgments were made in the existing model environment; ranking, exports, hashes and checks are deterministic.

The bundle includes the canonical source-pair-completeness baseline and corrected current expansions01–06 so every ranked card's source file is available. Earlier ZIPs remain preserved in Git and are excluded from this bundle. Historical delivery receipts describe their earlier artifacts. Original source texts remain in the repository with line/hash references; the supporting Norwegian source block is also included here.

Weekly ChatGPT and model-token telemetry are unavailable. The latest user report remains **88% at18:50 UTC**; the earlier99% change cannot be attributed solely to this task. Paid external API calls: **zero**. Free public EIA API calls in this pass: **two**.

## Detailed route decisions
'''
for a,b in [('January2024','January 2024'),('stale404','stale 404'),('all1555','all 1,555'),('to53','to 53'),('a100 invoice,60 combined cap and70','a 100 invoice, 60 combined cap and 70'),('passes19','passes 19'),('passes10','passes 10'),('the267+77','the 267+77'),('count,1555','count, 1,555'),('complete67','complete 67'),('prior1,715','prior 1,715'),('and15','and 15'),('The5,000','The 5,000'),('expansions01–06','expansions 01–06'),('at18:50','at 18:50'),('earlier99%','earlier 99%')]:intro=intro.replace(a,b)
table=['| Rank | Route | Readiness | Effort |','|---|---|---|---|']
for r in I[:10]:table.append(f"| {r['cheap_rank']} | {r['test_id']} | {r['readiness_tier']} | {r['effort_tier']} |")
intro=intro.replace('__RANK_TABLE__','\n'.join(table))
parts=[intro]
for r in R:
 parts.append('\n### '+r['route_id']+' — '+r['title']+'\n\nDisposition: '+r['disposition']+'; prior formulation: '+r['prior']+'.\n')
 for k in ['verified','constraint','next_cheapest_check','unresolved']:parts.append('\n**'+k.replace('_',' ').capitalize()+':** '+r[k]+'\n')
(P/'README.md').write_text(''.join(parts))
(P/'ranking-rubric.json').write_text(json.dumps(dict(unit='latest detailed card; includes refinements',count=67,ordering=['readiness_tier ascending','effort_tier ascending','test_id'],readiness={1:'Earlier explicit identifier/document bridge demonstrated',2:'One-side schema/sample or documentary structure verified',3:'Original evidence and exact applicability unresolved',4:'Known provider/access/reuse block'},effort='Ordinal editorial effort for next useful check, not total investigation cost;1short existing check,2bounded lookup/crosswalk,3original-document reconstruction,4external unavailable instruments or access gates.',consequence='Raw source-specific values retained for provenance only; incomparable across batches and excluded from ordering',full_case_feasibility='Not established for any card',scope='Canonical32-card baseline plus expansions01–05; historical duplicated versions excluded; six current access routes are not additional hypotheses.'),indent=2)+'\n')
(P/'progress-ledger.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in [dict(stage='review05',accepted_total=53,checks=19),dict(stage='catalog_scan',systems=1555,patterns=11,matches=0,global_absence_not_proven=True),dict(stage='bounded_evidence',api_calls=2,data_rows=1,audit_documents=1,matched_cases=0),dict(stage='ranking',cards=67,refinements=14,full_case_feasible=0),dict(stage='validation',checks_passed=13,initial_test_classification_bug_corrected=True),dict(stage='checkpoint',new_predicates=0,limit='access and operative constraints dominate',global_exhaustion_not_proven=True)]))
(P/'generation-provenance.json').write_text(json.dumps(dict(instruction='Continue source-grounded routes with original fields and public documentary exemplars; investigate Rabbit historical instruments and environmental-attribute serials; rank cheapest routes across batches; separate useful application from new predicate.',existing_model_environment=True,paid_api_calls=0,independent_review='Parent accepted53 through05; no06 additions to novelty count',data_acquisition='Two free EIA requests bounded1MiB each, one returned record; one5-page public audit read; no bulk execution',source_selection='All344 manifest retained;13 primary sources used in six concrete routes; one supporting Rabbit source854; targeted five-volume textual scan'),indent=2)+'\n')
fs=[f for f in sorted(P.rglob('*')) if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts and f.name not in ['artifact-checksums.json','delivery-receipt.json']]
(P/'artifact-checksums.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in fs},indent=2)+'\n')
roots=[P.parent/'source-pair-completeness']+[P.parent/f'consequential-expansion-0{i}' for i in range(1,7)]
z=P/'checkpoints/consequential-discovery-ranked-through-06-corrected.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for root in roots:
  for f in sorted(root.rglob('*')):
   if f.is_file() and 'checkpoints' not in f.parts and '__pycache__' not in f.parts:a.write(f,pathlib.Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as a:assert a.testzip() is None
print('ZIP',z.stat().st_size,hashlib.sha256(z.read_bytes()).hexdigest())
