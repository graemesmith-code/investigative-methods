# Bounded acquisition: US security investments beyond AI

**Completed acquisition and validation: 2026-10-16T22:11:23.494571+00:00 UTC.** Actual files were downloaded, opened and parsed. This is a reusable evidence corpus for quantum, drones/autonomy, sensors, cyber, space, hypersonic systems, electronic warfare and logistics research; **record counts are not counts of investments, and no spending total or novelty ranking is asserted**.

The FY2019–FY2026 selection window covers these spending slices: **342,900 DoD R&D contract actions** and **88,273 research-grant actions**, with text, award/transaction/entity keys and separate monetary fields. An additional capability-keyword extract extends beyond R&D classifications. The index across selected awarding-DoD slices contains **712,186 unique transaction keys**; overlap is retained as provenance, not extra money.

## What is ready

| Collection | Actual parsed records | Main boundary |
|---|---:|---|
| DoD R&D contract ZIP — 82,693,277 bytes | 342,900 prime actions; 131,534 subaward rows | FY2019–FY2026, awarding DoD, PSC A; prime count matches independent API count |
| DoD research-grant ZIP — 15,958,687 bytes | 88,273 prime actions; 14,143 subaward rows | Six research Assistance Listings, FY2019–FY2026 |
| DoD capability-keyword ZIP — 47,414,894 bytes | 305,768 prime actions; 31,308 subaward rows | Ten capability terms; **search/download count routes differ** |
| DARPA contract ZIP — 2,417,982 bytes | 12,057 prime actions; 4,869 subaward rows | FY2019–FY2026; overlaps other extracts |
| SBA award file with abstracts — 394,911,278 bytes | 219,649 raw; 25,770 selected; **25,769 exact-deduplicated** | Reported FY2019–FY2026 defense and selected DOE awards; latest year incomplete |
| Grants.gov full XML ZIP — 78,292,394 bytes | 83,576 raw; 3,283 selected | Opportunity/forecast intent, not awarded spending |
| Budget/research finance | 38,600 OMB account/year/measure/vintage cells; 256 DARPA program-title rows; 123 DOE lab/year financial rows | DARPA PB2025; DOE through FY2025; distinct requests, authority, outlays and institutional costs |
| Specific capabilities | 57 Commons project headers; ten FY2022 APFIT projects; full Sandia FY2025 report | Original project narratives and exact amount labels |
| Institutional/classification context | 862 FFRDC rows across 41 institutions; all 99 Federal Funds table workbooks; complete PSC workbook | Overlapping survey dimensions, table units and lookup versions preserved |

Full source tables, canonical Parquet/JSONL, a typed **`financial_actions.parquet`** view of unique signed action obligations, full page evidence and original raw payloads are outside Git. There are **701 physical source-report pages**, including explicitly flagged OCR. [DATASETS.csv](DATASETS.csv) is the starting file map; [normalized file inventory](validation/normalized_manifest.json) provides exact derived-file sizes, rows and hashes. Use the typed action view **instead of**, not in addition to, its source rows.

## Findings that change how the data should be used

- **The two official SBA bulk links differ.** The newer awards-page file is primary; the older data-resources file is a superseded comparison snapshot. Do not combine them. The retained newer subset has only 156 FY2026 rows and performance starts through 23 January 2026; an October server timestamp does not establish current-year completeness.
- **Search/download count routes differ for the keyword family.** The broad export has 305,768 prime actions, exactly matching the download-count endpoint, while the search-count endpoint reports 324,990. Separate FY2019/FY2026 exports likewise match download counts and the broad file's year-specific key sets. The 19,222-record difference between search and download counts remains unexplained; it is not proven missing data. R&D/grant/DARPA prime counts are independently checked. [Comparison](validation/count_export_comparison.json)
- **Money must keep its meaning.** Obligations, cumulative award values, options/ceilings, outlays, requests and institutional expenditure are separate. Sandia's $260.6M excluding program-management costs and DOE's $265.38M total accompany the same 536-project portfolio. One Commons “$1.10” amount lacks scale and stays unresolved. [Field dictionary](validation/monetary_fields.csv) · [Example](evidence/financial_basis_examples.json)
- **Missingness and ambiguity remain visible.** Spending extracts retain their native keys and populated UEIs; syntax is not registry verification. The selected SBA file has 15 missing UEIs, 13 DUNS syntax flags and 41 different-content groups sharing a source composite. Those versions are not silently merged.

Validation: **362 passing checks, 0 integrity errors, 4 coverage warnings**. Retained downloaded payloads total **1,127,854,484 bytes**, comfortably below 15 GB; normalized/source-preserving views total **884,011,827 bytes**. Raw hashes, ZIP CRCs, record counts, dates, identifiers, signs and monetary parse checks are recorded in [checks.json](validation/checks.json).

**QA correction:** Restore verification rejects empty selections, missing payloads and hash mismatches. Normalization binds snapshot metadata to the exact input file; two-vintage regression tests exercise this. Commons, APFIT and DARPA extracted projects carry mandatory snapshot/retrieval lineage. Regex tags (including hypersonic) are retrieval features, never novelty judgments. 84 of 96 spending descriptions in the revised example are under 200 characters; SBIR/project narrative enrichment is essential before novelty scoring. See [QA evidence](validation/qa_smoke_test.json).

## Reuse and remaining limits

Read the [technical annex](TECHNICAL_ANNEX.md) for exact source bounds, units, date semantics, duplicate/overlap policy, field dictionaries, dependencies and commands. [SOURCE_DECISIONS.csv](SOURCE_DECISIONS.csv) accounts for all 89 register entries. The original announcements and historical collection are unchanged.

**SAM was not acquired:** documentation requires authorized keys; unauthenticated probes returned 404, and no key/account was created. Several direct defense budget fetches failed; working DARPA/GovInfo/OMB alternatives are explicit. No separate monthly File C corpus, complete OTA ultimate-performer ledger, classified universe or complete latest-quarter coverage is claimed.

[Pipeline interfaces](design/PIPELINE_INTERFACES.md) prepare later capability/novelty scoring, uncertain relationships, newsworthiness, Exa checks and journalist dossiers. The **128-record deterministic dry run** retains untagged records for later model review, includes all relationship endpoint envelopes and keeps scores null; **zero model and Exa calls** were executed. No paid sources, whole scholarly graphs or standalone NIH corpus were acquired. No email was sent by this worker; the parent handles the morning email.

**All six archives are retained in private Library (1,449,208,374 bytes).** Four corrected archives are version 1; both raw archives are unchanged. [STORAGE.md](STORAGE.md) provides exact identities and restore instructions; [BUNDLE_MANIFEST.json](BUNDLE_MANIFEST.json) and [checksums](BUNDLE_SHA256SUMS) identify the retained bytes. Workspace persistence alone is not guaranteed.
