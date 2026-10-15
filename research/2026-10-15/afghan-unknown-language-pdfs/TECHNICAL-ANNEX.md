# Technical annex: Afghan gov.af documents in FinePDFs unknown

Prepared 15 October 2026. This annex records the selection and the limits that matter when interpreting the result.

## Selection

Source: [HuggingFaceFW/finepdfs](https://huggingface.co/datasets/HuggingFaceFW/finepdfs), using its Parquet file inventory. The scan read the url column from every row group in all 14 files under configuration unknown: 13 train files and one test file. It checked **17,123,442 rows in 17,129 row groups**. The final pass completed every row group with no unresolved scan errors.

A record matched when the lowercased hostname parsed from its URL equalled gov.af or ended in .gov.af. A substring in a path, or a domain such as gov.af.example.org, did not match. This found 239 records and 228 distinct URLs. Repeated dataset records were retained; they can represent separate captures. The host total removes a leading www. only.

After filtering, complete dataset rows were fetched for the matches. manifest.jsonl keeps dataset IDs, language scores and dates, source URLs, WARC file and byte offset, and Parquet file/row-group/row position. selection-audit.json reports the source files and scan coverage.

## What the language category establishes

The dataset label unknown means automated language identification did not return a language. It does not mean the text is in another language. Language identification may fail on short text, mixed scripts, tables, numbers, forms, scans and OCR errors. We did not manually classify each PDF. The 239 are candidates for expert review, not a measured count of documents outside English, Pashto and Dari.

The separately identified language configurations were not scanned. This package cannot answer how many Afghan-government-hosted PDFs are in Chinese, Arabic, Russian, English, Pashto, Dari or all other languages combined. Nor does the hostname prove Afghan-government authorship: official sites may host donor, contractor, international-organization or third-party documents. Government documents hosted outside gov.af are excluded.

## Retrieving the PDFs

For each record with an archived Common Crawl pointer, the recovery script requests the relevant WARC byte range, decompresses the record and extracts its HTTP response body. It tries the current source URL if the archive is absent or partial. The manifest distinguishes archived captures from current-site responses and records partial status, PDF end-marker check, page count where available, size and SHA-256.

Results: **221 complete PDFs, 8 partial PDFs and 10 without a recovered PDF**. Current-site responses may differ from older captures. A partial file may still render but may omit pages. PDF parsing succeeded for all 221 complete files; first-page previews rendered for 222 files.

Common Crawl’s [CDXJ index guide](https://www.commoncrawl.org/cdxj-index) and [download guide](https://commoncrawl.org/get-started) document byte-range WARC retrieval.

## Interpretation limits

- FinePDFs includes deduplication, extraction and OCR processing. Its text can differ from the original PDF. is_truncated is the dataset’s field; recovery.partial is a separate check of the recovered WARC/PDF.
- Crawl dates run from 23 March 2017 to 12 February 2025. They are not publication dates. A document can predate its crawl by years, and an old file may later be re-served at the same URL.
- The corpus includes Republic-era documents and later crawls. Crawl date alone does not establish which government authored a document.
- Source URLs and government hosts are observable facts. Authorship, language, novelty, diplomatic purpose and story value require document-level review.
- Failed downloads do not erase dataset records: their URLs, metadata and extraction provenance remain in the manifest.

## Reproduction

The Parquet inventory endpoint used was:

    https://datasets-server.huggingface.co/parquet?dataset=HuggingFaceFW%2Ffinepdfs

The selection expression was:

    host = (urlsplit(url).hostname or "").lower()
    match = host == "gov.af" or host.endswith(".gov.af")

selection-audit.json gives each input Parquet file’s split, row count, row-group count and match count. manifest.jsonl carries each match back to its dataset row.

