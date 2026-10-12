# Methodology and reproduction guide

This guide organizes the method recorded in the [complete saved findings](FINDINGS.md); it does not claim recovery of the original executable workflow. All ten candidate profiles and their particular limits are there.

## Source discovery and attribution

Use SEC submissions and bulk filing indexes to locate original narrative exhibits, not companyfacts as a substitute for mine tables. Use the Canadian ESTMA bulk CSV for discovery, then follow WEB_LINK to the original return: converted CAD values and duplicate parent/subsidiary rows need care. Use Companies House extractives JSON with reporting end dates, versions and amendments retained. For host records, follow the national annex links and identify the company-submitted column or original form. An EITI revenue field disaggregated by company can still be a government assertion.

Recorded discovery results include the SEC Q1 2024 index (4.49 MB; 370,321 filing entries), ESTMA CSV (53,258,265 bytes; 114,594 records; observed year labels 2021–2026), 52 UK all-company 2024 reports, and Rio Tinto's 2015–2025 reporting years with historical versions. These are original reported observations, not freshly reproduced corpus counts.

## Access and failed routes

The original study accepted access only after download/opening and parsing sufficient to match the named company or project. All ten candidate pairs met that recorded standard. Wider access counts are 88 requests = 85 HTTP 200 + three failed routes. Philippine MGB returned 403, one Senegal EITI company-revenue API route returned 403, and Mongolia's live reporting portal returned 502. Exact failed URLs and the complete ledger are missing. Accessible Mongolia and Guinea PDFs did not yield equally strong final pairs; Kamoa was excluded because its company capital declaration marker was “Non”.

## Comparison procedure

1. Preserve source URL, original bytes/hash, source version, exact page/cell, literal language, units and company-attribution evidence.
2. Match project and legal entities using the identifiers in each profile. Preserve parent/subsidiary and project-component bridges explicitly.
3. Align dates, reporting periods, amendments, physical/economic definitions, ownership level, recipients and 100%/attributable scope.
4. Retain blanks and non-responses as unknown. Keep company and government declarations separate, including original, adjustment and final columns.
5. Translate candidate claims while retaining the original assertion. Have a human approve ambiguous terms and mappings.
6. Express numerical claims as permissible intervals incorporating units, rounding and valid transaction-date FX bounds. For positive local payments L and local-units-per-USD rates in [r_min, r_max], use [L/r_max, L/r_min]. Handle mixed currencies, refunds and offsets by component.
7. Apply all eight approval conditions listed in the findings before returning INCOMPATIBLE CLAIMS. Otherwise return COMPATIBLE WITH PRECISION or REVIEW REQUIRED. Incompatibility alone does not establish intent or identify the erroneous statement.

The Peru aggregation is (19,771 + 9,740) × 1,000 pounds × 0.00045359237 tonnes/pound. The two independently rounded rows allow combined ±0.45359237 tonnes. Ity requires six cells from three companies, not SMI alone. Fekola requires the amended Western return and identical dividend entitlement and gross/net treatment before a verdict. Essakane requires resolving the embedded form's 31/12/2023 capital date despite its 2024 header.

## Instructions for a future reproduction

A future authorized reproduction should retrieve the exact linked source versions, record retrieval time and SHA256, respect normal access restrictions and SEC descriptive User-Agent/pacing requirements, and extract the precise source locators in each profile. For Essakane, inspect the XLSX ZIP's embedded workbook and relationship as well as the ordinary sheets. Preserve original language and translations alongside each claim. Document source changes separately rather than silently replacing the original snapshot.

No original scripts were recovered, so there is no original command that can be honestly supplied. Future implementation must be labelled new work. The page's suggested pilots and expansions have not been performed as part of this archive.

## Check this archive offline

Run `python3 scripts/validate_archive.py` from this directory. It checks exact saved Markdown, all block hashes, ten profile headings, aggregate count arithmetic, URL inventory and specimen conversion bounds. `python3 scripts/check_links.py` makes current HEAD requests to the recovered URLs and writes a separate dated log. The latter is an archival availability check, not the original 88-request access run; failures remain failures without access bypasses.
