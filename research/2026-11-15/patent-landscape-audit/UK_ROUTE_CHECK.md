# UK patent route check — 15 November 2026

## Purpose
Check UK national-publication coverage after January 2025, without confusing a historical journal or proposed API with a current full-text corpus.

## Verified boundaries
- [GOV.UK journal guidance](https://www.gov.uk/check-the-patents-journal) directs current journal searches to https://www.search-for-intellectual-property.service.gov.uk/journal. Historical downloadable PDF/XML period is 26 March 2008 to 22 January 2025. The journal is an events/index source, not full patent details.
- [Current IPO service guide](https://www.gov.uk/government/publications/one-ipo-patents-service-details/one-ipo-patents-service-details), updated 6 November 2026, says the IP register API is under development and release timing remains unconfirmed. It should NOT be recorded as a tested/live bulk API.
- [Search guidance](https://www.gov.uk/search-for-patent) identifies the new public register and Espacenet as routes to UK details.

## Actual access tests
1. Web retrieval of current journal and register home: HTTP403.
2. Independent Python/curl GET of current journal: HTTP403, 533491-byte HTML displaying a security check specifically mentioning automated extraction/data mining. Did not solve or circumvent it.
3. Legacy journal-download URL returned a service-unavailable page through web retrieval.
4. Government guidance HTML downloaded successfully (guide144310 bytes; journal guidance69279 bytes).
5. Bounded indexed query `site:patents.google.com/patent/GB "weapon" "2025" "safety"` produced GB2604376B (2025-04-16), an arming/safety-mechanism comparator. This is not a native search or AI-safeguard relevance finding; full claims were not reviewed and no official UK publication acquired.

## Outcome
No new UK native corpus or full-claims access established. Preserve separate coverage rows for pre-transition journals, post-transition journal/register access, and non-UK family proxies. A GB family member on Google/Espacenet can aid retrieval but cannot establish UK national-only completeness. Next useful authorized route is an ordinary interactive register search or an officially available bulk service; do not invent an API endpoint or regard generic web-index searches as a complete UK search.

## Evidence
Local directory /tmp/uk-patent-route contains public government guidance HTML and a sanitized access-test record. Raw security-page tokens excluded from evidence archive.
