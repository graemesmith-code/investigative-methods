# F4 independent skeptical review — actual Round 2

**Reviewed snapshot:** `9cdcb8e363e138067db42cc6a87383ec336f8dea`, 2026-10-25. [Reviewed cases](https://github.com/graemesmith-code/investigative-methods/blob/9cdcb8e363e138067db42cc6a87383ec336f8dea/research/2026-10-25/f4-autonomy-brakes-audit/evidence/reviewed-cases.csv), [all107 dispositions](https://github.com/graemesmith-code/investigative-methods/blob/9cdcb8e363e138067db42cc6a87383ec336f8dea/research/2026-10-25/f4-autonomy-brakes-audit/evidence/live-candidate-disposition.csv), and all five companion files read. CSV line numbers below include the header.

**Verdict:** the financial snapshot is substantially sound and unusually explicit about limits. It is not yet a technically adjudicated global inventory or evidence for universal absence. No final report/verdict is present at this commit; missing canonical-archive integration is acknowledged work in progress, **not an error**. Issues below distinguish actual row gaps from gates for the forthcoming report. Reporter response and revised artifacts are needed before Round3.

## What passes

- Independently recomputed **22 selected rows**:13A,3B,5C, plus excluded mixedTETRAS. Totals match exactly: A$31,019,162.92; B$4,487,272; C$5,597,607.02. Record-overlap subsets correctly yield5A/$9,774,108.92,1B/$1,988,634,2C/$3,547,892.43. These are cumulative whole-award amounts, not available balances or allocated safeguard spending; snapshot already says so.
- **107 distinct candidate rows;105 retrieved records=86contracts+18assistance+1IDV;2 unresolved.** No duplicate award keys in this snapshot, and no selected-row amount differs from its live-register record. All86 report exact FPDS/API reconciliation; this editor did not independently rerun all86.
- **20 overlapping awards** independently retrieved by this editor have identical obligations. Independent fresh CAMP FPDS fetch returned the exact same41583-byte response/hash as Reporter, two actions totaling$1,988,634. XML retained in this review bundle.
- Retained log genuinely contains **381 unique request observations:356HTTP200,7HTTP404,18HTTP422**. Counts reconcile. Initial unscoped-FD01 request-ledger loss is candidly disclosed;416 unmatched cached bodies are not miscounted as416 requests. No basis to allege fabricated completeness.
- Assistance is correctly separated from FPDS contracts; TETRAS/parent vehicle excluded; subaward revisions not added; ASIMOV maturity is not inflated into a fielded governor. Secondary category tags do not add dollars.

## R2-01 — HIGH: technical adjudication is not reproducible from finance-only row sources

**Affected:** every reviewed-case `source_url`; disposition lines18–94 in particular, including55 `C_candidate;B_possible`,7 `scope_unresolved`, and lines19/22 A-candidates FA864924P0465/FA864921P1296. The sole row source is a USAspending financial endpoint, which often does not establish the stated mechanism or classification. Descriptions such as `873AUTHORITY` or `RESEARCH AND DEVELOPMENT` are clear examples.55 C candidates remain description-level, not rejected safeguards.

**Resolve:** publish a concise technical-source crosswalk: award/program key, primary technical URL, actual mechanism/test, weapon link, maturity, what is unverified, and inclusion reason. Prioritize high-signal current-period leads, not every weak lexical hit: **FA239124CB020** runtime assurance (throughOct31 2026); **FA95501910169** assured-autonomy center (throughMar31 2027); **FA87502321015** ANSR-linked hybridAI (throughAug1 2027). The latter's research output explicitly acknowledges that grant: https://www.ri.cmu.edu/app/uploads/2025/06/Symant.pdf . Maintain unreviewed status if source access fails. No impossible field ablations are requested.

**Category rule:** lack of an explicit weapons-law acceptance test is not a reason to reject **C** safety/reliability. Conversely, ATR robustness alone is not contextual legal distinction. Distinguish this mechanism from normative evaluation, but admit its potential legal-compliance contribution. Five selected C rows cannot represent the entire C portfolio.

## R2-02 — HIGH: CAMP's material modification ambiguity is absent from the committed snapshot

**Affected:** reviewed line15; disposition line102; B accounting. The committed seven files contain neither `SLTE` nor `PHASE5A`, despite the assertion that this caveat was retained. Independent FPDS and USAspending evidence show:

- **January28 2026:** original+$1,988,634, explicitly Navy collaborative-autonomy mission planning/debrief.
- **April28 2026 P00001:** $0, within-scope change; description instead says USMC service-level training exercises, Phase5A.
- SignedJan28 versus startJan29; currentendJan29 2027. Army contracting, NavyNAVAIR funding.

Primary [award](https://api.usaspending.gov/api/v2/awards/CONT_AWD_W31P4Q26F0015_9700_W31P4Q22D0025_9700/); FPDS exact query is recorded in `camp-fpds-proof.json`. Neither copied administrative text nor substantive scope change may be assumed without the modification/SOW.

**Resolve:** put this caveat in the row/report, not only private messages. Retain the funded/current weapons-linked candidate: Navy's actual September2026 demonstration is good activity evidence (https://www.dvidshub.net/news/575299/navy-demonstrates-collaborative-autonomy-mission-planning-future-combat-aircraft). Add a separate **allocability** field. Whole-order inclusion in a clearly named selected-case finance statistic is mathematically permissible; it must not become an allocated B-safeguard expenditure total. Exclusion from such a safety total must not erase qualitative B evidence.

## R2-03 — MEDIUM: broadA selection criterion is not consistent enough to reproduce

**Affected:** HAMLET reviewedline11/disposition100 versus CASPER++101, Georgia103 and other adjacent grants. HAMLET is included in broadA while its exact weapons scope is unknown; adjacent grants are excluded for unknown weapons scope. That may be defensible because HAMLET's official topic specifically concerns adaptive ethical codes, but that distinction is not encoded in the row rule. No automatic inclusion or exclusion is warranted.

**Resolve:** split **strict weapons-normative**, **broader normative-autonomy/enabling**, **human training**, and **perceptual/classification-enabling** views; retain A/B/C overlaps. Explain why HAMLET meets broad normative criteria while CASPER++ may mainly concern trust/intention inference. Primary Manchester job document and exact-grant output support that distinction: https://www.jobs.manchester.ac.uk/Job/GetJobAdvertDocument?Id=96973&JobId=30455 ; https://www.inf.uni-hamburg.de/research/projects/trail/publications/pdfs/2025-04-pham-ijcnn.pdf (Atari interpretability, notLOAC). The MURI-topic-to-HAMLET linkage is a strong title/NOFO inference, not a directly recorded topic-number assignment. Do not assign Georgia's PI from institution alone.

## R2-04 — HIGH for final reporting: temporal and funding predicates need a visible matrix

**Affected:** all107 disposition rows; selected rows10–15 and18–22. Selected current-end/overlap flags are correctly calculated, but dispositions do not expose start/end/action dates. A future PoP is not evidence that work continued after a policy change, and a recent modification is not necessarily fresh money.

**Resolve:** expose signed/start/currentend, last public action, last **positive** obligation, termination/completion evidence, independent activity evidence and reporting limitation. Required examples: TEELAWS original2024 funding but April2026 Army use; CODORD positiveApril20 2026 increment; HAMLET newAugust20 2026 award; CASPER++ positiveSeptember10 2026 continuation; CAMP Januaryfunding/April$0/Septemberdemo. Label current-period sums as cumulative obligations of record-overlapping awards, not2026 funding or unspent budgets. Clarify fiscal2024–2026 versus calendar2024–cutoff; WeatherGage's $499,948 FY inclusion but zero calendar2024 is a valid boundary difference, not an error. Source proof is in the editor's frozen raw transaction bundle and [official TEELAWS use account](https://www.army.mil/article/291926/cadets_work_with_software_using_lethal_autonomous_weapons_systems_that_analyzes_tactical_decisions_provides_ethical_score).

## R2-05 — HIGH gate, not a current false claim: protect the verdict from the census fallacy

**Affected:** forthcoming report/headline. Snapshot rightly disclaims a census and universal negative. Keep that protection when converting tables into conclusions:55C-candidate,7scope-unresolved,7normative-adjacent,2A-candidate and2unresolved identities remain. **HR00112490431** and **HR00112590089** OTA/identifier gaps are not absence evidence. Program/task/tool/award counts must stay distinct: sevenASIMOV awards do not mean sevenprograms.

**Resolve:** state the precise tested proposition and adjudicate strongest contrary cases explicitly. A broad claim that funded technical normative work disappeared is incompatible with CODORD/HAMLET; no technical safeguards at all is incompatible with documented B mechanisms. A narrower failure to locate a public, active weapons-ethics benchmark matching ASIMOV's scope may survive, but only with an equivalent R&D maturity bar and disclosed search boundary. TEELAWS training, CAMP constraint workflow, and Switchblade wave-off cannot be discarded merely because they do not solve autonomous legal reasoning.

## R2-06 — MEDIUM: source-check status and provenance must survive integration

**Affected:** `verification_route`, inherited technical titles, forthcoming methodology. The381 retained requests contain **zero directSAM.gov requests and zeroSBIR.gov requests**; that does not mean those sources were never examined by other workers. Current finance routes correctly say FPDS/API, so no false verification claim is presently found.

**Resolve:** publish an explicit requested-source status matrix—directly retrieved, inherited with exact artifact provenance, not applicable, attempted/failed, or not performed—for SAM/SBIR/USAspending/FPDS. A zero-result FPDS grant query is not a missing-contract finding; same-pipeline FPDS/USAspending reconciliation checks money, not independent technical corroboration. Keep the DoD90-day **contract** restriction separate from assistance visibility; publicAug/Sep2026 grants are counterexamples to indiscriminately applying90days to everything. Do not invent timestamps for the lost first-pass ledger or claim an all-attempt count.

## R2-07 — MEDIUM integration gate: preserve one denominator across parallel archive passes

**Affected:** pending canonical and auxiliary integration, not a current duplicate error. No duplicates were found among105 live records. The performer trace itself warns alias searches overlap. Coordinator's additional scans cannot be summed with the independent Stage1 screen as disjoint populations.

**Resolve:** stable generated award key for funding; separate provenance edges for each input archive/file/row/search/source. Report input rows, unique awards, unique program families, new live additions and exclusions separately. Reconcile original90 to actual107 additions without treating repeated discovery as a new award. Show disjoint/overlap counts for canonical versus auxiliary data, not merely two totals. Parent/subaward dollars remain excluded from double counting.

## Specific identity correction to retain

Edge Case **FA864924P0520** is a separate C task, but not established to be an unrelated `CaTE` acronym collision: its primary abstract explicitly partners CMU and builds on an assurance framework produced for CaTE (https://www.sbir.gov/awards/210029). SEI ethical architecture is one output of the broader calibrated-trust pilot. Do not attribute the STTR's $1,799,899 to that ethical prototype or infer its continued operation from the STTR period. Current public record endsFeb2 2026; January7mod is a zero-dollar address change. This row was absent from the107 snapshot, plausibly pending integration; absence here is not accused as an archive failure.

## Round3 acceptance test

Reporter responds to R2-01 through07 with accepted/rebutted/unresolved, exact changed file/row, and evidence. Round3 checks actual revised artifacts and draft verdict, not assurances that edits will happen. Financial-pass findings need not be redone unless inputs change. No publication acceptance yet; no assertion the initial snapshot committed a universal-negative error it explicitly avoided.
