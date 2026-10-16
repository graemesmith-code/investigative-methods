# Future warfare investments: recovered experiment data

This folder preserves the original data recovered on 16 October 2026 from Graeme Smith's Mac Downloads folder for the September 2026 Pentagon/Jev/Exa experiment. It supports a new source-mapping investigation. Scores and search matches are leads for investigation, not proven unpublished stories, evidence of wrongdoing, or validated measures of future military investment.

## Preserved exports

| File | Bytes | Verified contents |
| --- | ---: | --- |
| `raw/pentagon_contract_paragraphs_10000.csv` | 10,652,658 | 10,000 unique full announcement paragraphs; 713 source-page URLs; announcement dates 2023-09-12 through 2026-09-25. |
| `scored/pentagon_jev_results-4.csv` | 12,494,754 | Same 10,000 records and exact source-field values; 10,000 unique record IDs; all records marked success with eight populated scores and no recorded errors. |
| `coverage/coverage_0707a32e.csv` | 483,979 | 100 lead/result pairs: ten ranked leads, ten results each, 96 distinct result URLs. Full announcement paragraphs, queries, article metadata, assessments, reasons and highlights. |
| `coverage/coverage_0707a32e.json` | 547,665 | Ten lead records with nested hits and original Exa response objects; run metadata, queries and highlights. |

The files retain their original bytes and filenames. Sources were `/Users/gsmith/Downloads/` plus the corresponding filename. The local originals were not edited. `SHA256SUMS` covers these four exports and this README; run `shasum -a 256 -c SHA256SUMS` from this folder to verify a download.

## Schema and execution provenance

Raw columns: `announcement_date`, `service_or_agency_section`, `contractor_name`, `raw_paragraph_verbatim`, `source_url`, `source_page_title`. Paragraph lengths are 177–9,482 characters; 1,273 contractor-name cells are blank. The full paragraph remains available in those records.

The scored export adds `record_id`, eight scores (`newsworthy`, `further_reporting`, `unusual`, `consequences`, `failure_exception`, `reporting_question`, `relationship`, `public_should_know`), processing/error fields, human-label/reporter-note fields, and model/question-set/timestamp metadata. Returned model is `jev-1.13.0`; requested model is `jev-latest` for 100 records and `jev-1.13.0` for 9,900. Question set is `editorial-v1`. Recorded analysis timestamps run from 2026-09-27T21:12:21.752739+00:00 to 2026-09-28T05:52:21.148155+00:00.

Exa run `0707a32e95ba45dfbe868db5f2912279` requested ten leads and completed all ten without recorded errors. Created: 2026-09-29T11:56:21.172138+00:00; finished: 2026-09-29T11:56:53.419149+00:00. Its recorded method is one Exa auto search with highlights per ranked lead. Every coverage `record_id` joins to the scored corpus. The ten leads' announcement dates range from 2024-06-13 through 2026-07-17.

## Limits and publication review

- Nine leads are labeled `Possible match`; one is labeled `No clear match in results`. The CSV repeats each lead's label across its ten result rows. These are heuristic coverage signals; no clear match is not proof of no prior coverage. Read the linked sources before using a result in reporting.
- Exa responses preserve highlights and article metadata, not full article bodies. Publication dates are present for 76 of 100 result rows. Search queries may contain truncated paragraph prefixes even though the announcement text is preserved in full.
- All human labels are `Unlabelled`; reporter-note fields are empty. This backup does not add editorial judgments, classifications, searches or source-mapping documents.
- This is the announcement corpus, distinct from the small USAspending procurement sample, OFAC transaction/sanctions datasets, and the separate 200-headline filter trial.
- Pre-publication review found no credential patterns, private notes, or local home paths in the four exports. Email addresses occur only inside public procurement/article highlights: two Space Force contacts and a publication customer-service address. No data was redacted or omitted from these four exports.
- The archive preserves export provenance and recorded timestamps; it is not an independent revalidation of every announcement, score, or article. No paid APIs or project code were run during recovery or backup.
