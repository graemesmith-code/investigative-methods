# Technical annex

## Legal and temporal matrix

| Issue | Rule applied | Primary source and temporal scope |
|---|---|---|
| LDA foreign owner | Section 1603(b)(4): identify qualifying foreign entity, including at least 20% equitable ownership; control and interested-affiliate alternatives also matter. Contribution amount reporting is separate; a zero contribution does not erase ownership identification. | [2024 US Code, 2 USC 1603](https://www.govinfo.gov/content/pkg/USCODE-2024-title2/html/USCODE-2024-title2-chap26-sec1603.htm), subsection (b)(4); acquired original LD1 section 14 repeats the alternatives |
| Indirect chain | Joint guidance’s wholly owned chain example requires foreign parents up the chain; the guidance is advisory, not a judicial ruling. Do not confuse domestic subsidiary with ultimate foreign owner. | [Joint LDA guidance](https://lda.senate.gov/ldaguidance.pdf), registration section, foreign entities; revision 28 February 2025. Statutory rule also checked in 2024 edition; no new 2025 rule is retroactively assumed |
| Registration thresholds | 2021–24: firm income $3,000 per client/quarter; in-house expenses $14,000. From 1 January 2025: $3,500/$16,000. These exemptions do not change the 20% ownership threshold. LDA lobbyist/contact/time tests also apply. | [House historical notices](https://lobbyingdisclosure.house.gov/), March 2021 and January 2025 notices; [Senate thresholds](https://www.senate.gov/legislative/Public_Disclosure/new_thresholds.htm) |
| Updates | Quarterly reports include changes to registration information; LD2 new-entity fields are not a fresh denial of the original disclosure. Registrations, amendments, additions and removals must be read as chronology. | [2 USC 1604(b)(1), 2024](https://www.govinfo.gov/content/pkg/USCODE-2024-title2/html/USCODE-2024-title2-chap26-sec1604.htm); original LD2 sections 27/28 |
| FARA Exhibit A/B | Exhibit A identifies each nonexempt foreign principal; B records agreements. Changes to exhibits within 10 days are addressed by **28 CFR 5.201(b)**. Section 5.208 does not supply this deadline. Exhibit C under 5.201(c) concerns the registrant, not an automatic ownership register for every principal. | [2025 annual CFR, Part 5](https://www.govinfo.gov/content/pkg/CFR-2025-title28-vol1/html/CFR-2025-title28-vol1-part5.htm), 5.201, 5.208–.209; actual acquired forms revision 10/23 |
| FARA exemptions | Section 5.304(b)/(c) makes commercial exemptions activity-specific; government ownership alone does not decide all conditions. Under 5.307 the LDA exemption does not apply when a foreign government/party is the principal beneficiary. No entity-wide exemption conclusion is made. | Same annual CFR; [DOJ FARA FAQ](https://www.justice.gov/nsd-fara/frequently-asked-questions). Proposed 2025 regulatory revisions are not treated as enacted rules |

The pilot assesses 2024–25 documentary questions. Older LDA records are historical-chain retrievals; it makes no liability claim under pre-2008 thresholds. Financial statements dated March 2025/2026 describe earlier year ends. They provide retrospective source evidence, not proof that a filer saw them when filing. The English IAI statements are a convenience translation; the Hebrew version is authoritative. No daily share-register continuity has been independently certified.

## Acquisition and cohort definition

Repository start: `research/2026-10-04/consequential-expansion-09/START-HERE.md`, baseline `c29762cac5f31aa5b7886da446f3f6647288ddfb`; recovered X04 formulation in `source-card.json`. Initial checkout `218de208...`; separate branch `research/lobbying-control-pilot-20261007`; checkpoint `d4e63f0`. Prior sanctions guard and tests were read from remote commit `0edf7130942e817c12b7a23d7d0f9038ed74ec11`, not assumed present locally. No relevant `.agents/skills` files were available. Unrelated repository content was preserved.

First ownership searches (verbatim):

- `site:efile.fara.gov/docs/ "Exhibit-AB-2025" "Corporation" "owns"`
- `site:efile.fara.gov/docs/ "Exhibit-AB-2025" "wholly"`
- `site:efile.fara.gov/docs/ "Exhibit-AB-2025" "shareholders"`

Expansion searches (verbatim):

- `site:efile.fara.gov/docs/ "2025" "Exhibit A" "wholly-owned subsidiary"`
- `site:efile.fara.gov/docs/ "2025" "Exhibit A" "shareholders are"`
- `site:efile.fara.gov/docs/ "2025" "Exhibit A" "percent owned"`

These searches yielded nine initial and seven further unique documents, plus three earlier government access controls. `cohort.json` freezes the resulting 19, including four failed originals. Boilerplate “corporation” hits were retained as controls, not silently dropped. This is an indexed convenience cohort. The source card did not contain a prior original-filing cohort to reuse.

LDA client-name searches used every readable principal’s mapped query, plus Bulgaria/Rwanda aliases and auxiliary blocked-document candidate searches (Apex, Havas, Qatar Investment, Romanian-American). Those candidate names are not promoted to verified FARA identities. Ownership-driven expansion followed Stark’s IAI chain and the US subsidiaries named in IAI’s original table: ELTA North America and IAI North America/Israel Aerospace. All 28 exact parameter sets, counts and pagination endpoints are in `sources/lda-*-summary.json`. Four corporate history queries omit the year filter; others use 2025. `next` is followed because the server caps pages at 25 despite a request for 100.

Original HTML/PDF filings are saved under their UUIDs. Some `.html` files are PDFs because the server returned that original format; extraction checks magic bytes. `filing-index.csv` preserves registrant IDs, client IDs, original URLs, dates, periods and local paths. Name normalization never merges separate registrants. Different client IDs are not treated as different corporations without checking original addresses; shared names are not sufficient for merging.

Browser PDF extraction supplied FARA originals where executor requests were denied. It did not supply local PDF bytes or a visual checkbox inspection; FARA ownership interpretation uses the explicit narrative appendix. Browser search/open exports are partial provenance aids, not full original PDF archives. Manual dossier notes cite physical pages. The downloaded IAI 2024 report was text-extracted and visually checked on physical page 55; its hash is in `source-hashes.json`. Two HTTP-200 files (`iai-2024-press.html`, `stark-ms2024.html`) are challenge pages, **not verified originals**, and are excluded from evidence claims. The manifest records HTTP results, not evidentiary quality.

## Pipeline and replay

From repository root, the following runs are offline and incur no charges:

```sh
python -m unittest discover -s research/2026-10-07/lobbying-control-pilot/scripts -p test_guard.py
python research/2026-10-07/lobbying-control-pilot/scripts/refine.py
python research/2026-10-07/lobbying-control-pilot/scripts/final_iteration.py
python research/2026-10-07/lobbying-control-pilot/scripts/summarize.py
```

`refine.py` first imports `build_dossiers.py` to rebuild the fixed initial dossiers, then adds audited second-pass findings. `final_iteration.py` adds the contract-chain/full-history evidence. These scripts preserve model outputs. `summarize.py` deduplicates UUIDs, selects the latest filing within registrant/client/year/quarter, excludes registrations from annual totals, retains missing values, and generates chronology/coverage/audit/spending files. `complete_history.py` is a free-network replay for the four acquired corporate queries, with four download workers. `acquire.py` provides bounded TLS-verified retrieval, immutable cache, source hashes and pagination. Search discovery is reproducible from saved queries/cohort, but search-engine rankings can change; it is not a deterministic national census.

The baseline in `refine.py` uses explicit audited flags: identity bridge, dated ownership evidence, original “No,” partial-chain question. It assigns high for supported explicit mismatches, medium for unresolved explicit/partial questions, low for no pair/already disclosed, and abstains for unavailable originals. Human extraction is an input to both baseline and Jev. It is not an autonomous information-extraction benchmark.

`evaluate.py` requires explicit `--live`; `guard.py` blocks live calls after `jev/COMPLETE` exists. Do not remove this sentinel or reset the ledger for a replay. Provider requests, raw responses, distributions, model version and observed token usage are archived. Do not interpret the model’s reported confidence as calibrated probability of wrongdoing.

## Iteration audit

| Stage | Added evidence/action | Result |
|---|---|---|
| Calibration | Eight synthetic tasks, including later acquisition, earlier disclosure, different client, funding confusion and document instructions | Initial compound positive control scored .78 against .80 threshold; stopped before cases. Rephrased as literal extraction scored .90. Earlier failed result retained. All final eight passed; this is tuned calibration |
| 1 | All 19 frozen dossiers; Stark initially later-only ownership | Jev overcalled Stark; raised Haiti/Congo despite unresolved identity; abstained on four unavailable originals |
| 2 | 2023/24/25 ownership snapshots; ELTA original/address; IAI parent amendment and Pillsbury negative; Haiti/Congo originals; Harena amendment | Comparative order Stark, IAI/Emanuel, ELTA. Haiti remained medium; Pillsbury negative received medium despite already-disclosed finding |
| 3 | All 137 corporate-history originals; Stark contract intermediate chain, signatures, scope and fees; unrelated GlobalPoint amendment rejected | Comparative order unchanged. Stark high; IAI/Emanuel high; ELTA medium. Exact-day control still marked not established. Editor retains qualified lead status, not model legal conclusions |

Final Jev classification of “documentary mismatch” alongside “control not established” remains internally cautionary. `jev/audit.json` flags this mechanically. The model helped structure questions but did not discover the ownership document, improve the joins, or resolve the legal uncertainty. Extraction and source review drove the improvements. No held-out recall, precision or accuracy claim is justified by this small nonrandom cohort.

## Spending enforcement

Only existing `JEV_API_KEY`/`TYPESAFE_API_KEY` integration was used; no keys were printed or saved. Current official [model documentation](https://docs.typesafe.ai/models) and [API documentation](https://docs.typesafe.ai/api) were checked before calls; authenticated model-list access succeeded. Pinned model `jev-1.13.0`; verified input price $0.042/million, free output, maximum 64,000-token context. Full-context input cost is $0.002688; each transaction first reserves $0.003. Bodies are capped at 16,000 bytes. SQLite `BEGIN IMMEDIATE`, durable reservations, no automatic retries/redirects, strict response/usage validation and retained uncertainty reservations enforce the bound. Eight offline tests cover these failure paths.

Total: 42 successful calls, including failed calibration wording, 19 first-stage dossiers, seven second-stage, three third-stage and four comparative choices. Usage-based rounded accounting: $0.002858. Maximum if every full reservation were retained: $0.126. Internal cap $14, authorized cap $15. No provider invoice was available. The inherited ledger schema mentions Exa in a generic note, but the guard allows only Jev and no Exa request was made.

## Remaining evidence gaps

No certified FARA bulk corpus, complete principal-specific FARA amendment history, four blocked cohort originals, exact-day private share registers, or underlying LDA-firm instructions were acquired. Original corporate reports support year-end ownership, not intent. No response from any named party was sought because outreach was outside authorization. The report should not be published as an accusation.
