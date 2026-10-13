> Historical initial-pass snapshot. Current opportunity classification is in [the revised report](../../REPORT.md); original audit judgments and counts are preserved here.

# Coverage, stages and gaps — 13 October 2026

**1,752 organization-source records; 1,751 works after one identified cross-organization coauthored duplicate.** 1,665 records carry an in-window publication/republication/catalog date; 87 need date verification. PPLAAF migration dates are not verified original-publication dates. These are publication/investigation leads, not uniformly confirmed substantive reports.

**Acquisition and screening:** 498 source records with underlying fulltext acquired/available (PDF, substantive HTML or browser text; not 498 downloaded PDFs). 489 nonempty text files were keyword-indexed, mapping to 483 report works. 79 organization-source records were context-screened (78 unique works); 69 screens used sources recorded fulltext-acquired, ten used partial-source text. 30 organization-source records received deep assessment of selected relevant sections (29 unique works). **Zero finalists or finalist-retained sources.** These are not counts of entire reports read cover to cover.

The coauthored 2025 UK PSC-register report appears in TJN and Open Ownership; each organization gets credit in the matrix, but totals identify the duplicate. Translation and PDF versions remain in original team manifests and nested source_versions. No automatic cross-language translation equivalence is claimed. Known mirrors were explicitly merged; unidentified mirrors remain a limitation.

| Organization | Enumerated | Dated in window | Fulltext acquired | Machine-screened works | Context screens | Deep section reads | Finalists |
|---|---:|---:|---:|---:|---:|---:|---:|
| Global Witness | 194 | 194 | 2 | 0 | 2 | 2 | 0 |
| Global Financial Integrity | 42 | 41 | 1 | 0 | 1 | 1 | 0 |
| OCCRP | 89 | 89 | 0 | 0 | 1 | 1 | 0 |
| Tax Justice Network | 110 | 110 | 0 | 0 | 1 | 1 | 0 |
| Public Eye | 102 | 102 | 15 | 15 | 4 | 1 | 0 |
| Spotlight on Corruption | 61 | 61 | 2 | 0 | 2 | 2 | 0 |
| The Sentry | 79 | 2 | 0 | 0 | 2 | 2 | 0 |
| Sherpa | 41 | 41 | 11 | 11 | 4 | 3 | 0 |
| C4ADS | 20 | 11 | 0 | 0 | 1 | 1 | 0 |
| Basel Institute on Governance | 321 | 321 | 294 | 294 | 6 | 5 | 0 |
| Natural Resource Governance Institute | 299 | 299 | 38 | 38 | 11 | 1 | 0 |
| Open Ownership | 109 | 109 | 0 | 0 | 3 | 2 | 0 |
| Transparency International | 224 | 224 | 74 | 72 | 19 | 3 | 0 |
| PPLAAF | 53 | 53 | 53 | 53 | 14 | 1 | 0 |
| AntAC | 8 | 8 | 8 | 0 | 8 | 4 | 0 |

## Per-organization boundaries

| Organization | Exact boundary / remaining gap | Evidence |
|---|---|---|
| Global Witness | Catalog pages 2–8; newest page 1 omitted. Direct raw 403;194 browser extracts mostly partial, not full reports read. Older archive coverage incomplete. | [Team ledger](../../teams/global_trade/findings.md) |
| Global Financial Integrity | 41 dated+1 undated method. Cached catalog inconsistencies/challenges; older decade coverage incomplete.35 browser acquisitions mostly landing/body extracts; no direct PDFs. | [Team ledger](../../teams/global_trade/findings.md) |
| OCCRP | Purposive 88 investigation catalog records+1 methodological project, not all 150 archive pages. Batch-body attribution errors excluded; no full original PDF acquisition. | [Team ledger](../../teams/kleptocracy/findings.md) |
| Tax Justice Network | English official reports catalog 110.77 primary report-type candidates,33 adjacent posts/briefings. Acquisition predominantly abstracts/partial browser text; not all reports downloaded. | [Team ledger](../../teams/secrecy_ownership/findings.md) |
| Public Eye | Reports catalog only, English preferred and 17 explicit translated mirrors merged. Magazines/other languages not exhaustive;429 halted broader acquisition. | [Team ledger](../../teams/global_trade/findings.md) |
| Spotlight on Corruption | All 8 archive pages;63 entries minus 2 explicit duplicates. Broad court/enforcement publication archive, not every court document; raw requests 403. | [Team ledger](../../teams/legal_enforcement/findings.md) |
| The Sentry | 79 canonical works including 88 landing-page versions/9 translations.77 canonical dates unverified; only selected originals read. Unattributed browser segments excluded. | [Team ledger](../../teams/kleptocracy/findings.md) |
| Sherpa | Legacy research/publication categories;41 eligible records.19 API bodies empty;2024–26 newer categories incomplete. Translation deduplication may remain incomplete. | [Team ledger](../../teams/legal_enforcement/findings.md) |
| C4ADS | 20 canonical reports;9 dates unverified. Archive pagination 404/direct 403; underlying procurement/trade evidence inaccessible in checked examples. | [Team ledger](../../teams/kleptocracy/findings.md) |
| Basel Institute on Governance | English-focused sitemap publications;321 after exclusions/deduplication. Includes publication-type leads, not all financial-investigation reports. Some unidentified language duplicates possible. | [Team ledger](../../teams/legal_enforcement/findings.md) |
| Natural Resource Governance Institute | 455 English/publications URLs;452 landing acquisitions;299 in-window.38 works selected for 45 PDFresponses/44 unique PDFs. Not all papers acquired; non-English catalog gaps. | [Team ledger](../../teams/secrecy_ownership/findings.md) |
| Open Ownership | Official 123 catalog cards deduped to 109 records;89 primary reports/briefings/research,20 adjacent blogs. Other languages/not-all original fulltexts acquired. | [Team ledger](../../teams/secrecy_ownership/findings.md) |
| Transparency International | 221 global-secretariat English catalog records+3 purposiveTI Ukraine/DOZORRO methodological cases.19 global pages covered; Knowledge Hub/national chapters not exhaustive.72 localPDFs;2018 article 403/index-only. | [Team ledger](../../teams/integrity_whistleblowers/findings.md) |
| PPLAAF | 21 substantial cases+32 country reports.96 language versions→55 English-preferred→53 afterstub/duplicate exclusions. CMS dates can be migration/republication dates; first publication history unverified. | [Team ledger](../../teams/integrity_whistleblowers/findings.md) |
| AntAC | Ukraine identity verified;8 purposive browser sources, raw 403. Major 2016–17,2019–22, Ukrainian-language and older archive gaps; not a decade census. | [Team ledger](../../teams/integrity_whistleblowers/findings.md) |

## Reproduce the counts

Run `python scripts/consolidate.py` then `python scripts/build_coverage.py` from any working directory. [source-inventory.jsonl](../../source-inventory.jsonl) preserves per-record stages, original inventory/line pointers, date precision and rationale. [machine-screen-inventory.jsonl](../../machine-screen-inventory.jsonl) preserves parsed-text hashes/keyword offsets and maps all489screen records to source IDs. [coverage-counts.csv](../../coverage-counts.csv) and [totals.json](totals.json) are derived outputs. Raw URL discoveries and out-of-window exclusions remain in team files, outside these headline totals.

Machine keywords are a broad relevance index, not a semantic conclusion. A low or zero hit count is not evidence that a report lacks an opportunity. No exhaustive recall was measured. The purposive contextual sample cannot establish that the entire decade contains no other strong opportunities.
