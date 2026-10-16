# Pentagon contract announcements: five-year historical extension

This collection targets **12 September 2018–11 September 2023**, inclusive. It extends the announcement source universe around the preserved 10,000-row export; it does not produce investment estimates, editorial scores or a comparable spending series. Status and counts are recorded in `summary.json`; [coverage and gaps](COVERAGE.md) summarize the run, and missing dates are explicit in `daily_coverage.csv`.

## Access and source identity

The live Defense.gov and War.gov listing pages returned HTTP 403 in this environment on 16 October 2026. No access controls were bypassed. The collector uses the Internet Archive's free public CDX index and normal Wayback replay of **official Defense.gov pages**. Every historical record is labeled with that archive source, the original official URL, requested CDX timestamp, actual resolved retrieval URL, retrieval start time, response hash and retained HTML filename. Final parsed pages also record the parser code hash and parse time, separate from retrieval time. The response's `memento-datetime` is retained in its page metadata; redirects can select a different capture from the requested one. Archive capture dates and retrieval dates are distinct from announcement dates. Older snapshots can omit later corrections.

The first successful CDX request is saved as `discovery/cdx-contract-first3000.json`. Its exact parameters were `url=www.defense.gov/News/Contracts/Contract/Article/*`, `output=json`, `filter=statuscode:200`, `collapse=urlkey`, `fl=timestamp,original,digest,mimetype`, `limit=3000`, `showResumeKey=true`. This response contains a resume key after article 4136115, beyond the bounded candidate range 1627000–3523820. Article IDs are discovery aids, not date evidence: parsed article titles determine final inclusion. The bounds include a day before and a day after the requested window. This is **partial archive discovery**, not a census of every official publication or every URL variant. A second saved CDX response checks the older `www.defense.gov/.../Contract-View` route; no overlapping-period candidate was recovered from that response. A further fully logged `dod.defense.gov/.../Contract-View` check returned 733 URL records, including 198 unique article IDs inside the candidate bounds; all 198 were already in the main candidate list. Initial probe request timestamps were not captured; saved response hashes and the retrieval date are preserved. A subsequent fully logged CDX refresh returned HTTP 503; it is retained with its failure provenance, not treated as data.

The run uses three workers and a shared 0.8-second minimum interval between request starts. There is one request per candidate during the first pass; saved successes can be resumed without downloading them again. HTTP failures, timeouts and parse failures remain visible. A nonblocking OS lock prevents a second collector from running in the same environment. Before launch, the process list and repository were checked and no duplicate historical collector, working files or running job were found. This check does not establish the status of other environments.

## Files and paragraph extraction

- `pentagon_contract_paragraphs_history.csv` starts with the original six raw columns, followed by record identity and retrieval provenance. `contractor_name` is deliberately blank because reliable extraction of legal entities from joint awards was not part of this collection. No model scoring or selection by award amount, contractor or technology topic is applied.
- `html/*.html.gz` contains complete successful HTTP-200 responses, compressed deterministically. `response_sha256` hashes the **uncompressed response bytes**. Files may include source-site navigation and scripts; they are evidence, not executable deliverables.
- `pages/*.json` records each attempt and its complete parsed article blocks, including section headings, short notes, corrections and explicit no-award notices. The main CSV uses substantive blocks longer than 100 whitespace-normalized characters under a section, every dollar-bearing block regardless of length, and correction notes longer than 35 characters. Asterisk-led footnotes without a dollar amount and shorter material remain in the page file and HTML. Bare text separated by double BR elements is split at those source paragraph boundaries. A paragraph is one complete source block; the collector never clips its text to a character limit.
- Older source layouts use sibling DIVs; newer layouts use P elements. The parser recurses through block wrappers without duplicating nested text. Text preserves punctuation, Unicode spaces and complete inline contents. Source HTML markup is retained separately. Announcement titles supply dates, and the source page title remains intact. All-capitals headings and source-observed mixed-case agency heading variants are recognized; section text keeps the source capitalization and spelling. CSV readers use `newline=""` so embedded CR/LF characters are preserved during verification.
- `page_manifest.json`, `candidate_coverage.csv` and `retrieval_attempts.jsonl` expose results and failures. Re-parsing saved HTML can resolve a parse failure while the original attempt log remains intact. `first_pass_progress.log` preserves provisional progress and counts from the initial parser; final reprocessing, `summary.json` and the verification report supersede those counts.
- `daily_coverage.csv` lists **every calendar date**, including weekends. An unresolved date means no dated page was recovered, not proof that nothing was announced. Explicit no-award notices have a separate status. Weekday gaps include holidays and remain unresolved unless supported by source evidence.
- `combined_deduplicated_index.csv` is the only combined product. Its pointers use one-based parsed CSV record numbers, not physical text-file line numbers. Its key hashes the JSON array of announcement date, whitespace-normalized section and whitespace-normalized full paragraph. Each entry retains all file/data-row/source-URL pointers with the individual raw paragraph hashes. The top-level paragraph hash represents the first raw-text variant for that normalized key. Source CSVs are never concatenated or overwritten. Repeated wording on different dates remains separate; the key does not resolve later corrections, modifications or contract identity.
- `audit/` holds original-corpus and extraction verification evidence; `rules/` retains official threshold change documents and retrieval provenance.

## Original corpus is capped, not an exhaustive comparison period

The original export has 10,000 unique paragraphs from 713 dated pages, ordered newest date first, 12 September 2023–25 September 2026. Its SHA-256 remains `bf717bac8ad92d8c4d7d4aa6371b73b64580f0df7f3f9708cf2d798af895349c`.

The archived 12 September 2023 source has **29 substantive paragraphs**. The export contains exactly the **first 20**, ending with the BAE Bradley modification, and omits the following nine. All 20 match the source prefix after whitespace normalization. This demonstrates a page-level cutoff consistent with a 10,000-row cap, while the retained paragraphs themselves are complete. It does not independently validate every other source page or prove the original collector's exact selection logic. The previous collector and configuration were searched for in the refreshed repository and available workspace but were unavailable; the original collector revision/sampling rules remain unverified. The original export is preserved unchanged. The nine omitted boundary paragraphs are audit evidence outside this historical extension's requested period and are not silently added to the history CSV.

See `audit/original_corpus_audit.json`, `audit/original_boundary_comparison.csv`, the retained complete boundary response and its provenance. Do not compare paragraph counts or totals across the two periods as if they have uniform coverage.

## Announcement thresholds and financial limits

| Applicable dates within the combined time span | DFARS 205.303(a)(i) threshold | Primary evidence |
| --- | ---: | --- |
| 12 September 2018–30 September 2020 | More than $7 million | [2018 DFARS version](https://www.acq.osd.mil/dpap/dars/dfars/html/r20180824/205_3.htm); [2020 amendment](https://www.govinfo.gov/content/pkg/FR-2020-09-29/html/2020-21122.htm) replaces $7 million with $7.5 million |
| 1 October 2020–30 September 2025 | More than $7.5 million | [DFARS Case 2019-D036, effective 1 October 2020](https://www.govinfo.gov/content/pkg/FR-2020-09-29/html/2020-21122.htm) |
| 1 October 2025 onward | More than $9 million | [DFARS Case 2024-D002, effective 1 October 2025](https://www.govinfo.gov/content/pkg/FR-2025-08-25/html/2025-16205.htm) |

The rule covers face value excluding unexercised options, including modifications, with special treatment for undefinitized actions and orders under previously announced ceilings. A published paragraph can represent a ceiling, modification, exercised option or obligation. Paragraph dollar figures cannot be summed into a defensible investment series without action-level interpretation and deduplication. Public announcements exclude much classified/nonpublic activity and smaller actions; publishing practices and archive coverage vary. The source site's generic $7.5 million footer is not used to override dated regulatory changes. No attempt is made here to assess legal compliance.

## Reproduce or resume

From the repository root, using Python 3.11 or newer:

```sh
python -m venv /tmp/pentagon-history-venv
/tmp/pentagon-history-venv/bin/pip install -r research/2026-10-16/future-warfare-investments/history/code/requirements.txt
HISTORY=research/2026-10-16/future-warfare-investments/history
/tmp/pentagon-history-venv/bin/python "$HISTORY/code/collect_history.py" discover
/tmp/pentagon-history-venv/bin/python "$HISTORY/code/collect_history.py" collect
/tmp/pentagon-history-venv/bin/python "$HISTORY/code/collect_history.py" reparse
/tmp/pentagon-history-venv/bin/python "$HISTORY/code/audit_original.py"
/tmp/pentagon-history-venv/bin/python "$HISTORY/code/verify_history.py"
/tmp/pentagon-history-venv/bin/python "$HISTORY/code/report_coverage.py"
```

`discover` deterministically regenerates candidates from the retained CDX batch. `fetch-discovery` makes the documented public CDX query and saves a separately named response plus provenance; a refreshed response must be reviewed before replacing the candidate basis. `collect --limit N` supports a bounded access test; `collect` retries failed candidates but skips saved successes. `reparse` uses only retained bytes, then rebuilds coverage and index. `build` rebuilds products from current page files without network requests. Do not run competing mutation commands: all entrypoint commands share the same lock. Dependency versions are frozen in `code/requirements.txt`. No account keys, paid APIs, model services or scoring are used by the collector. After generating the reports, `sha256sum -c SHA256SUMS` from this `history/` directory verifies the retained package; the separate parent-folder checksums still verify the untouched originals.
