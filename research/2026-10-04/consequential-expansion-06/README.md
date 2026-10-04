# Access-grounded routes and cheapest-next-check ranking — 4 October 2026

**The count stays at 53 reviewed non-refinement formulations.** This checkpoint adds no new predicate. It checks six concrete routes, saves one EIA schema response and one bounded data row, inspects one public audit for document structure, and ranks all **67 current detailed cards: 53 non-refinement formulations and 14 refinements**. Useful applications are not counted as new tests merely because their source changes.

The most valuable result is a clearer choice of what to try next. Clinical-trial/publication, World Bank project/document and OONI/ASN routes have demonstrated identifier links in earlier small samples. They lead the ranking. That makes the next source check cheaper; it does not establish the full investigative hypothesis as executable or any wrongdoing.

## Cheapest next checks across the batches

| Rank | Route | Why it is near the front | Remaining gate |
|---|---|---|---|
| 1 | R05 — Trial registration and publication | Earlier sample demonstrated registry-reference linkage and retrieved the trial. | Historical protocol/outcome versions and actual published analysis. |
| 2 | R11 — World Bank project and underlying document | Earlier sample linked project ID to an agreement text. | Exact operative condition and independent implementation evidence. |
| 3 | R12 — OONI measurement and ASN context | Earlier samples demonstrated the network-identifier route. | Historical attribution, measurement quality and alternative outage explanations. |
| 4 | N01 — Aid-account definitions and audit reconciliation | New public audit demonstrates reported/certified amounts and loan/date context. | Compatible scope and original accounts; no automatic cross-donor comparison. |
| 5 | B01 — Plant energy-conversion balance | Live schema and one aggregate row expose distinct total and allocated inputs. | Complete physical boundary, uncertainty, and claim reliance on tested quantities. |
| 6 | V01 — Fund concentration constraint | Official field dictionary and corrected conservative-bound helper. | Exact fund/class mandate, verified canonical holdings and measurement bounds. |
| 7 | R01 — OFAC and procurement actions | Earlier source samples demonstrate award-to-action retrieval. | Actual identity, restriction scope/date, exceptions and original action meaning. |

`cross-batch-ranked-routes.csv` and JSONL contain all 67 cards, source-file pointers, next checks and reasons. The ranking is an editorial readiness/effort ordering, not a statistical estimate of success. Tier1 means an identifier/document bridge was demonstrated; tier2 means one-sided metadata/sample or document anatomy; tier3 means original evidence remains unresolved; tier4 marks known access/reuse blocks. Within a tier, effort1–4 runs from a short existing-document check to unavailable instruments or access gates. These effort tiers are new comparative judgments, not quoted prices or elapsed-time estimates. Original feasibility descriptions and scores are preserved separately. Potential consequence scores describe a material case if established, not likely newsworthiness or yield. No card is marked full-case feasible.

## What the concrete checks established

**EIA:** Two free public API calls using the documented demonstration key returned metadata and exactly one January 2024 plant-period row. The fields include plantCode, fuel/source and prime-mover dimensions, net generation, total-consumption-btu, and consumption-for-eg-btu. The saved row is an ALL aggregate, not proof of complete physical inputs. No balance was calculated. Inputs are operator-reported measurements or estimates; this is not an independent observation. The API's large total-count/warning is preserved, but only one row was requested and obtained.

**World Bank:** One five-page public audit identifies a project through its URL, a loan on the cover and a financial-year interval. Its tables offer component-level expenditure/certification and implementing-unit advance categories. They do not supply B02's required invoice/settlement chain. This is a useful simpler N01 application—checking what “spent” means—but not a new predicate, duplicate-payment finding or investigation of the sample project. Later responses and resolution were not researched.

**Norwegian ships:** Supporting Rabbit source SYS-0854/AP-1802 had a stale 404 route. Current official documentation now supplies a production search link, IMO and owner-organization search fields, and a publisher-described historical-search route. The browser exposed no actual ship record. Free search is distinct from paid certification. Bareboat/title/flag/owner/mortgage roles must be reconciled before asserting incompatible registrations. This improves S03/S04/R03 applications without adding a predicate or clearing Equasis restrictions.

**Canadian ships:** Recent historical extracts require an application and payment. No extract was ordered. A current registry query cannot substitute for a historical instrument; the free older archival index has a different time scope.

**FAA:** The current layout confirms serial/model, ModeS and document-index fields. Document types concern ownership, security and related instruments; this is not a component-maintenance history. Public names can be withheld. No 60MB database was downloaded and no aircraft was matched.

**Environmental attributes:** Eleven recorded text patterns were searched across all 1,555 current Rabbit source blocks in five volumes, excluding the older duplicate Rabbit2 and front matter. No serial-level registry candidate matched. This is a reproducible bounded catalog search, not proof no registry exists elsewhere or under other terminology. Issuer/project names cannot replace credit serials, retirement beneficiaries and operative rights.

## Review repairs included

Independent review accepts B01/B02, bringing the non-refinement total to 53. B01 now requires an issuer claim to state or demonstrably rely on the exact quantities tested. Otherwise an imbalance is only an EIA reporting-quality lead. B02's helper uses `permitted_recovery_upper`: the combined recovery cap can be below invoice cost and is separate from each funder's individual cap. The fixture with a 100 invoice, 60 combined cap and 70 completed recoveries flags the excess. The helper does not check individual funder caps. Expansion05 now passes 19 checks.

This checkpoint passes 10 artifact/provenance checks, including the 267+77 source count, 1,555-block scan, bounded API response, supporting-source hash and complete 67-card inventory. An initial validation attempt incorrectly matched the text “refinement” inside “non_refinement”; the test was corrected to explicit categories. The failed attempt is preserved alongside the passing log. These checks do not validate a substantive case.

## Limits and next work

Marginal yield has fallen: six grounded route checks produced **zero new predicates**. Missing original instruments, legal scope, historical identity and settlement-level access are now the main limits. The public audit example demonstrates that limitation directly rather than assuming it. This is not a proof that every remaining catalog opportunity has been exhausted. Further productive work should use the ranked next checks to establish a missing bridge or find a genuinely different operative predicate; broad source permutations and transplanted conservation laws would not justify more counts.

The prior 1,715 active provisional pair rows and 15 quarantines remain a separate counting unit. The 5,000 target is not supported. No bulk investigation, paid record, new account, public outreach or finding was produced.

## Audit and reproduction

Run `python code/catalog_scan.py`, `python code/build.py`, `python code/validate.py`, then `python code/package.py`. These local scripts reuse saved evidence and make no network calls. The two actual EIA calls and public document/page inspections are logged separately. Source selection and judgments were made in the existing model environment; ranking, exports, hashes and checks are deterministic.

The bundle includes the canonical source-pair-completeness baseline and corrected current expansions 01–06 so every ranked card's source file is available. Earlier ZIPs remain preserved in Git and are excluded from this bundle. Historical delivery receipts describe their earlier artifacts. Original source texts remain in the repository with line/hash references; the supporting Norwegian source block is also included here.

Weekly ChatGPT and model-token telemetry are unavailable. The latest user report remains **88% at 18:50 UTC**; the earlier 99% change cannot be attributed solely to this task. Paid external API calls: **zero**. Free public EIA API calls in this pass: **two**.

## Detailed route decisions

### U01 — Norwegian historical registration supports sanctions asset chronology

Disposition: useful_application_refinement; prior formulation: S03/S04/R03.

**Verified:** Official IMO/organization-number search fields; current production search link; authority-described historical search.

**Constraint:** Sanctions still require actual identity, dated applicable restriction, conduct and exceptions; bareboat/title/mortgage/flag roles differ.

**Next cheapest check:** For a preselected IMO, manually check whether history and role-effective dates are visible without ordering a certificate; stop if not.

**Unresolved:** No vessel response or historical instrument obtained; paid certification is outside this work.

### U02 — Recent Canadian vessel history

Disposition: defer_cost; prior formulation: 05:M1.

**Verified:** Authority distinguishes current information, transcripts and historical research.

**Constraint:** Current registry status cannot reconstruct a past ownership or flag interval.

**Next cheapest check:** Use free historic archival index only for its stated period; otherwise retain paid-record dependency.

**Unresolved:** Recent historical research requires payment; no order sent.

### U03 — FAA identity chronology and collateral index

Disposition: schema_improvement_not_new; prior formulation: T01/T02.

**Verified:** Manufacturer serial/model and ModeS layout; document receipt/correction/type fields.

**Constraint:** N-number reuse and different collateral types defeat naive joins; registration/security records do not establish maintenance, airworthiness or passengers.

**Next cheapest check:** Verify aircraft serial/model and effective registration before a historical track; do not use an indexed lien document as a maintenance certificate.

**Unresolved:** Actual historical mapping and original instrument not acquired; public names can be withheld.

### U04 — Serial-level environmental attributes

Disposition: defer_missing_registry; prior formulation: 05:D2/D4.

**Verified:** Targeted eleven-pattern scan across1555 current Rabbit source blocks returned no registry candidate.

**Constraint:** Issuer claim, project name or generator/year is not a unique unit or attribute right.

**Next cheapest check:** Require a specifically identified registry and serial/retirement semantics before developing a card; expand catalog search terms only with a concrete lead.

**Unresolved:** No supporting Rabbit registry identified by this search; this is not proof of global absence.

### U05 — EIA plant-period input boundary

Disposition: bounded_schema_sample_improvement; prior formulation: B01.

**Verified:** Live metadata and exactly one aggregate plant-period row preserve IDs, units, total fuel input and electricity-allocated input separately.

**Constraint:** Operator-reported estimates/measurements are not independent observations; ALL aggregate alone does not prove all external energy or storage resolved. Claim must state/rely on tested quantities.

**Next cheapest check:** Check technology, source-code disaggregation and explicit claim quantities before any balance calculation.

**Unresolved:** No issuer bridge, complete plant boundary, full disaggregation, uncertainty model or balance calculated.

### U06 — Public project audit exposes access granularity

Disposition: document_anatomy_improvement; prior formulation: B02/N01.

**Verified:** One five-page audit links projectURL, loan identifier, fiscal interval and reported-versus-certified expenditure categories.

**Constraint:** Component and implementing-unit totals do not identify a uniquely reimbursed invoice or independently settled payment. Unliquidated advances differ from completed expenditure.

**Next cheapest check:** Read certification basis and find original cost/settlement references. For the simpler N01 application, compare precisely defined reported and certified expenditures at the same cutoff.

**Unresolved:** Sample lacks B02 invoice/settlement chain; no duplicate reimbursement or new finding established.
