# Coverage and remaining gaps

Built at 2026-10-16T13:58:09.281411+00:00. Requested period: 2018-09-12 through 2023-09-11, inclusive.

**Partial public-archive coverage; publication completeness is not established.**

- 1,247 candidate article IDs; 1,247 attempted; 1,247 successfully parsed (including out-of-period boundary controls).
- 1,245 in-period pages; 2 explicit no-award dates; 18,819 complete substantive paragraphs.
- 1,245 dates supported by recovered pages; 581 calendar dates without a recovered page, including 59 weekdays. Weekends and holidays are not proof of nonpublication.
- 0 unresolved candidate retrieval/parse failures; see `candidate_coverage.csv` and `retrieval_attempts.jsonl`.
- Combined index: 28,818 unique keys and 28,819 source-row pointers, including the original 10,000 rows.

| Year (requested-window portion only) | Paragraphs | Supported dates | Unresolved weekdays |
| --- | ---: | ---: | ---: |
| 2018 | 1,538 | 73 | 6 |
| 2019 | 3,952 | 248 | 13 |
| 2020 | 3,993 | 251 | 11 |
| 2021 | 3,665 | 249 | 12 |
| 2022 | 3,422 | 250 | 10 |
| 2023 | 2,249 | 174 | 7 |

`daily_coverage.csv` enumerates every date and `monthly_coverage.csv` aggregates the same evidence. Supported dates include explicit no-award notices; paragraph counts exclude headings and retained footnotes. An unresolved date is a gap in this recovery, not a finding that no announcement exists. Discovery came from a bounded public CDX response, not an official census.

## Candidate failures

No discovered candidate remains in a failed state. Undiscovered pages and date gaps remain possible.

## Verification and comparability

All 1,247 retained response files passed byte-hash checks. Validation errors: 0; body-reconstruction warnings: 0; pages with dollar-bearing nonrecord blocks: 0. See `audit/verification.json` and `audit/page_extraction_checks.csv`.

The original export remains unchanged. Its oldest day contains the first 20 of 29 source paragraphs, demonstrating a cutoff consistent with a 10,000-row cap. Its full selection configuration remains unavailable. The historical period also crosses the 1 October 2020 announcement threshold change ($7 million to $7.5 million); the original period crosses the 1 October 2025 change ($7.5 million to $9 million). Archive coverage, reporting thresholds, source revisions and selection differ. Do not treat these paragraph counts or dollar figures as comparable complete investment totals.
