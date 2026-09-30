FINANCIAL CRISIS WARNING-SIGNAL PILOT
Run date: 2026-09-30 UTC
Purpose: inexpensive reproducible information-triage example, NOT a validated crisis predictor.

Files
- occ2004.pdf, occ2005.pdf, occ2006.pdf: official source PDFs fetched by download_sources.py; not bundled in this repository
- download_sources.py: source downloader (Python standard library)
- analyze_occ.py: coordinate-aware table extraction, category-coverage and percentage-total checks, signal calculation and vintage comparison
- occ_retail_all_vintages.csv: all 160 retail category/year rows across the three editions (48+56+56)
- results.json: calculated results, threshold sensitivity, cross-vintage audit and SHA256 hashes
- report.txt: findings and source links
- Visual source checks were completed during the original run; intermediate page images are not bundled here

Reproduce
Requires Python 3 and Poppler pdftotext. Uses no Python third-party package, model inference or paid API.
1. python download_sources.py (required on a fresh checkout; source URLs and original hashes are in source_manifest.json)
2. python analyze_occ.py
3. Inspect results.json and occ_retail_all_vintages.csv
4. Check source PDF pages indicated by each CSV row. The script asserts complete categories, expected row counts, exactly three numeric cells, and percentage totals within 1 point of 100.

Protocol and limits
Score = percent of relevant-product respondents easing standards minus percent tightening.
Product respondents vary: in 2006, high-LTV home equity had 19 banks and residential real estate 62, within an overall survey of 73. These are not percentages of all 73 banks or loan-dollar shares. The script validates category coverage, expected row counts and percentage totals, not underlying product-specific respondent denominators.
Threshold >=10 percentage points, with sensitivity >=1 and >=20.
The threshold and source choice were selected retrospectively after reading the data. NOT preregistered.
Population: every retail category in each survey (8 in 2004 and 2005; 7 in 2006). Consumer leasing drops from 2006 and is never silently called a non-alert.
The yearly rows in a given edition are not a panel of the identical banks. No pooling as individual mortgage outcomes.
No held-out predictive labels, loan loss outcomes, sensitivity/specificity or causal estimates were computed.
Historical 1999-2003 readings shown from later editions are descriptive histories, not verified earlier-publication snapshots.
The comparator is a no-LLM table parser/rule, not an LLM. A further blinded LLM comparison remains unperformed.

Release provenance
2004 announcement: 2004-11-09, https://www.occ.gov/news-issuances/news-releases/2004/nr-occ-2004-102.html
2005 announcement: 2005-07-28, https://www.occ.gov/news-issuances/news-releases/2005/nr-occ-2005-74.html
2006 announcement: 2006-10-18, https://www.occ.gov/news-issuances/news-releases/2006/nr-occ-2006-116.html
Observation periods are 12 months ending March 31 of each survey year, NOT the publication dates.
The current OCC catalog misleadingly labels these editions with generic December dates. Use the contemporaneous announcements instead.
PDF metadata for 2004: created 2004-10-19, modified 2004-10-27
PDF metadata for 2005: created 2005-07-26, modified 2005-07-28
PDF metadata for 2006: created/modified 2006-10-19, a day AFTER the release announcement
These PDFs were fetched in 2026. No independent historical WARC/archive proves exact historical byte identity. Exact first-publication date of the present 2006 PDF is unverified. Do not use exact-day lead-time claims.

Observed tool barriers
OCC direct PDF downloads and pdftotext worked. Web PDF screenshots returned cache misses, so locally rendered source pages were checked instead. Direct Federal Reserve HTML download returned HTTP403 although web-tool reading worked. Opening Countrywide's 2005 10-K via the web tool failed although indexed SEC search text was available. No paid/credentialed alternate feed used.

Before comparing a rerun, compare downloaded hashes with source_manifest.json. Unlike the Enron script, this parser does not enforce pinned hashes automatically. analyze_occ.py overwrites results.json and the CSV in its working directory; retain the versioned originals for comparison.
