# OTA identity and financial-schema resolution

Verified 25 October 2026 using free public primary endpoints. No Exa, paid API, credential, authentication workaround, or outreach was used. This is a supplemental financial view; it does not modify the earlier live register automatically.

## Material correction

Four agreements previously unresolved or missed by a FAR-only Atom parser are present in the **same public FPDS Atom feed**. Their payload is `https://www.fpds.gov/FPDS` **OtherTransactionIDV**, with identity under `OtherTransactionIDVID/OtherTransactionIDVContractID` and financial/date/description fields under `contractDetail`. Looking only for `content/f:award` yields zero parsed awards even when the XML contains these records. Complete pagination is not sufficient without schema coverage.

These are funded **prototype Other Transaction** records. They must not automatically be treated like an ordinary unfunded FAR parent IDIQ. Conversely, the term IDV is not a license to add parent values to child spending. The JSON preserves exact primary agency/PIID identities; the eight USAspending probes did not resolve a generated key, so no USAspending-style key is invented.

## All visible primary actions

All four feeds returned six distinct visible actions, one page each and no next link. All 24 actions were parsed; no duplicate conflicts or unparsed entries occurred. The formal verification has four HTTP200 FPDS receipts and eight HTTP404 USAspending probes. Four earlier exploratory FPDS probes are separately inventoried with original-byte hashes and file timestamps explicitly identified as file timestamps, not reconstructed HTTP-start times.

| PIID | Program lead | Visible actions | Sum of visible action obligations | Feed aggregate obligations | Aggregate minus visible sum | Latest visible current end | Latest visible potential end |
|---|---|---:|---:|---:|---:|---|---|
| HR00112490431 | TIAMAT / University of Texas at Austin | 6 | $1444520.00 | $1444520.00 | $0.00 | 2026-04-30 | 2027-10-30 |
| HR00112590088 | CODORD / RTX BBN DONATELLO | 6 | $1653574.00 | $1998788.00 | $345214.00 | 2026-05-09 | 2027-02-10 |
| HR00112590097 | CODORD / Barnstorm KRADL | 6 | $1449955.00 | $1336460.00 | $-113495.00 | 2027-04-05 | 2027-04-05 |
| HR00112590089 | CODORD / USC DROIDDS | 6 | $1500553.00 | $1500553.00 | $0.00 | 2027-05-31 | 2027-05-31 |

**Only TIAMAT and USC reconcile their visible action sums to the feed aggregate.** BBN and Barnstorm have real, unresolved discrepancies. These must not be silently reconciled or treated as verified aggregate obligations in an additive total. The discrepancy could reflect omitted, delayed or corrected data, but this review did not establish its cause. The latest visible end is a record date, not direct observation of present work. DoD public release delays remain relevant.

### USC CODORD / DROIDDS

`HR00112590089` names University of Southern California and DROIDDS, Data Efficient Robust Ontology Induction for Deontic Compliant Decision Support. A July2025 action explicitly names CODORD. Its latest March25,2026 action adds **$487,415** and extends the current and potential ends to **May31,2027**. Visible obligations and the aggregate both equal **$1,500,553**. This is primary affirmative evidence of funded deontic research beyond the JHU/APL support order, not an unresolved nonexistent contract.

### RTX BBN CODORD / DONATELLO

`HR00112590088` explicitly names DONATELLO and CODORD. Visible action obligations sum **$1,653,574** versus a **$1,998,788** feed aggregate, leaving **$345,214** unexplained. The March27,2026 action adds **$690,737**. The latest visible current end remains **May9,2026**, while potential end is **February10,2027**. Neither the potential date nor the aggregate proves current October performance or explains the missing delta.

### Barnstorm CODORD / KRADL

`HR00112590097` names KRADL, Knowledge and Rule Authoring for Deontic Logic; other modifications explicitly name CODORD. A zero-dollar April2025 modification instead uses the DONATELLO title, a description discrepancy retained in the full actions. The March27,2026 action adds **$549,979** and has current/potential end **April5,2027**. Visible obligations sum **$1,449,955**, but the aggregate is **$1,336,460**, a **negative $113,495 difference**. No correction is guessed.

### UT Austin TIAMAT

`HR00112490431` explicitly names TIAMAT and rapid autonomy transfer. Six visible actions sum **$1,444,520**, exactly matching the feed aggregate. The latest February26,2026 modification is **$0**, with current end **April30,2026** and potential end **October30,2027**. Last positive funding is **November4,2025**. The original current-period performance ended in the visible record; the potential end must not be called an exercised active period. Aggregate exercised value is **$1,444,520**, versus **$5,334,694** all-options value. Values/options are not additional spending.

## Technical and lineage boundaries

DARPA's [CODORD page](https://www.darpa.mil/research/programs/codord) explicitly connects deontic reasoning with law, ethics and dynamic rules of engagement. Its public DAR/DeonticBench outputs concern general regulatory domains; the funding records do not establish weapons-specific normative testing, fielded enforcement or legally correct operational decisions. TIAMAT's autonomy-transfer purpose is C assurance/transfer research with possible A/B contributions; exact ROE test content still requires technical evidence. Separate CODORD agreements awarded to an RTX-related performer do not prove continuation of ASIMOV PhaseII.

The initial four-ID pass left SRI's identifier unresolved; the targeted keyword follow-up below closes that identity gap. No exhaustive OTA-program census is claimed. There is no independent USAspending cross-system financial reconciliation for these four records. The evidence is primary FPDS record existence and internal visible-action-versus-aggregate checks, explicitly separated from technical effectiveness and current implementation.

## Reproducibility and evidence

- `code/verify_ota_sources.py`: exact known-PIID queries, payload-schema parsing, all next-link traversal and exact Decimal sums.
- `evidence/ota-resolution-review.json`: four full summaries and all 24 derived actions with source URL, retrieval time and raw-response SHA256.
- `evidence/ota-verified-actions.csv`: all 24 action rows, no financial filtering.
- `audit/ota-retrieval-log.json`: all 12 formal requests, eight failures, and four exploratory probe receipts.

Raw XML bodies remain private. Each exact public primary feed is linked in its JSON/actions. This review closes the **identity/parser** gaps; two initial financial discrepancies, task-level scope and operational effects remained open at that snapshot; see the additional SRI/SIFT identities and their discrepancies below.


## Targeted keyword follow-up: SRI and SIFT identities resolved

At the parent investigator's request, nine bounded public queries covered `CODORD`, `"HUMAN-AI" "DEONTIC"`, `DONATELLO`, `KRADL`, `DROIDDS`, `TIAMAT`, explicit description-field CODORD/deontic searches and `"SRI" "DEONTIC"`. All eleven returned pages were traversed without HTTP failure. The description-field deontic query returned23 records over three pages, while generic CODORD returned only two USC actions. Thus an ordinary keyword result is not a complete agreement history.

The scan preserved and excluded two unrelated historical keyword collisions: a Donatello street address in a2003 contract and TIAMAT port services in a2018 Coast Guard record. DARPA-prefix identity and explicit program/deontic text were required for the program lead view. This is a targeted discovery rule, not a global census.

Two newly discovered exact identities were then independently fetched by PIID using the full OtherTransactionIDV parser, with six actions each and complete pagination:

| Agreement | Recipient/function | Visible action obligations | Feed aggregate | Difference | Current/potential end |
|---|---|---:|---:|---:|---|
| HR00112590099 | SRI International, SOLON text-to-deontic-logic work under CODORD | $1,500,019 | $1,999,992 | +$499,973 | 2027-04-05 |
| HR00112590098 | Smart Information Flow Technologies (SIFT), CODORD | $1,537,850 | $1,999,705 | +$461,855 | 2027-04-05 |

SRI's latest visible March25,2026 action adds **$499,972**. SIFT also has a positive March25,2026 action. Both records explicitly name CODORD in their description histories and their disclosed current periods overlap October25. Their aggregate-versus-visible-action discrepancies remain unresolved and must not be silently added as reconciled money. No USAspending cross-system reconciliation is asserted.

The exact SRI identity gap is now **closed**. SIFT's new CODORD agreement matters to the named-performer trace, but a different normative research award does not by itself establish ASIMOV PhaseII continuation. Actual delivered weapons-law tests, deployment, task allocation and four prototype aggregate discrepancies remain open.

Additional artifacts: `audit/ota-keyword-followups.json` (all query scopes/pages, collisions and two exact follow-up receipts); `evidence/ota-keyword-followup-records.json`; `evidence/ota-keyword-followup-actions.csv`; `code/verify_ota_keywords.py`; `code/verify_codord_extra.py`. No paid request or source outreach occurred.
