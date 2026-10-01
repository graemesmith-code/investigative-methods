# Evidence and artifact inventory

For the original September notebook, seven selected Library sources were materialised to readable local bytes. Each ZIP was listed and unpacked before selection. This repository contains a small, curated set; the complete archives were not uploaded.

The table below inventories that original selection. The later [Canadian ATI archive](../research/2026-10-01/ati-live/README.md), [historical-test annexes](../annexes/README.md) and [Rabbit reference](../catalogs/README.md) have separate provenance.

## Included evidence

| Artifact | Source | What it can establish | Selection |
|---|---|---|---|
| [Original OFAC report](ofac/original-report.md) | sanctions-screen-results-2026-09-18.md | Historical screen counts, assessment, limitations and reproduction account | Original bytes |
| [OFAC source metadata](ofac/source-summary.json) | sanctions-screen-evidence-2026-09-18.zip; duplicated in ofac-step1-2026-09-18.zip | Snapshot date, entity/name counts and XML hash | Original bytes |
| [Contract input metadata](ofac/contract-source.json) | sanctions-screen-evidence-2026-09-18.zip | Archive URL, byte size, date metadata and hash | Original bytes |
| [Screen summary](ofac/screen-summary.json) | results/screen-summary.json in sanctions evidence ZIP | Count fields and screen scope | Derived copy omitting lengthy per-member file metadata |
| [NAI transaction excerpt](ofac/nai-transaction-excerpt.json) | results/candidate-transactions.jsonl in sanctions evidence ZIP | Selected recorded identity/action fields and zero obligation | Derived; one row, 14 transaction fields |
| [API manifest](api-samples/manifest.csv) | defense_observatory_api_samples_2026-09-19.zip | Twenty historical capture entries and status notes | Original bytes; referenced raw paths refer to the source archive, not files included here |
| [Large transactions](api-samples/usaspending_large_defense_transactions.csv) | Same API archive, normalized/ | Example money-ledger schema and descriptions | First 3 of 10 rows, all columns |
| [Special studies](api-samples/usaspending_defense_studies_b5.csv) | Same API archive, normalized/ | Example intent-ledger descriptions | First 5 of 25 rows, all columns |
| [Legal entities](api-samples/gleif_lockheed_lei_records.csv) | Same API archive, normalized/ | Example public corporate identifiers | First 3 of 5 rows, all columns |
| [Announcement feed](api-samples/defense_gov_contract_announcements.csv) | Same API archive, normalized/ | Example official publication links and dates | First 3 of 10 rows, all columns |
| [Exa overview](exa/overview-1.csv) | Overview 1.csv | Ten summary labels, priorities and result counts | Original bytes, including abbreviated lead labels and byte-order mark |
| [Artifact hashes](artifact-hashes.json) | Curated included evidence above | File integrity fingerprints | Generated during notebook preparation; excludes itself and this inventory |

API CSV selections are illustrative, not representative samples or performance estimates. Original cell values were retained; CSV serialization was regenerated. The archive contains 14 normalised extracts, not just these four selections. The manifest records nine usable source families plus failed-access captures; those historical counts were checked against the unpacked archive.

## Supporting code

[OFAC scripts](../docs/reproduction.md) retain the original `prepare.py`, `screen_contracts.py` and `check_screen.py` bytes from the sanctions evidence ZIP. The `ofac-step1` source contains duplicate preparation inputs; no duplicate upload was needed. The full XML, names, entities, candidate groups, full matching transaction rows, package-generation script and multi-gigabyte contract archive are excluded.

The [news retrieval script](../code/newsapi/check_newsapi_sources.py) comes from `check_newsapi_sources.py`. Only the generation-attribution prose in its introductory comment was removed; executable logic is unchanged. No result logs accompanied this source.

`jev-investigative-journalism-design.md` was read as a design proposal. Its narrow-role architecture informed [the method explanation](../docs/method.md); the full design, broad catalogue claims, historical pricing and unrelated topics were not copied.

## Missing evidence

| Experiment | Missing material | Consequence |
|---|---|---|
| OFAC | Complete historical vehicle/order history and final identity/legal checks | No payment or screening-failure conclusion |
| Public-source pilot | Collector code and measured cost/time ledger | Samples demonstrate historical access, not a repeatable production collector |
| Headline prototype | Pinned source revision, exact WSJ THAAD control, queries and responses | Cannot diagnose or measure retrieval failure fully |
| The News API | Saved report/JSON, actual quota and bill | 27 requests and no errors remain user-reported |
| Paragraph prototype | Code revision, prompts and full input corpus | Publication alone cannot establish ranking performance |
| Jev + Exa | Ten original paragraphs, corpus date range, ranking outputs, queries, 100 article pairs, URLs/text and manual decisions | Cannot verify novelty or revised classifications |
| Jev + Exa costs | Per-run Jev/Exa usage, invoice allocation, retries and review time | Cannot calculate actual cost per useful lead |
| Anduril prior coverage | Exact links and saved-result membership | Retrieval-versus-classification diagnostic remains unresolved |

No emails, credentials, private contacts, household material, personal financial records or unrelated nonproliferation work are included. Raw sources containing broader fields were kept outside the upload selection. Public corporate identifiers in the selected records are retained because they support professional source verification.

[Home](../README.md) · [Experiments](../experiments/README.md)
