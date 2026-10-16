# Technical annex

Dataset: HuggingFaceFW/finepdfs. Source parquet inventory and exact row-group coordinates accompany this report. Search selected Russian, Arabic varieties, Turkish/Ottoman and Hindi/Fiji Hindi partitions. Broad host candidate rule: hostname ends in .af or contains afghan. Ownership then reviewed; this can miss official sites on unrelated foreign domains.

Rows: Russian 16,602,197; Arabic 1,592,085; Turkish 1,700,676; Hindi 880,544. Total 20,775,502. Files: 76,39,13,8 respectively. The first scan left nine network gaps; a checkpointed retry completed every file, with no final errors. Summary seconds_this_run records retry time only, not end-to-end labour. No reliable API dollar-cost measurement was available; do not infer cost from scan speed.

Workflow: fetch parquet metadata and URL columns, extract full candidate rows; screen host ownership and language; recover original Common Crawl WARC byte ranges where possible, falling back to current site; inspect target-language PDF content; deduplicate recovered positives by SHA-256. WARC truncation and missing PDF EOF are tracked. Positive PDFs must open with pages; no repaired/partial file is counted as a positive. Current-site replacements are identified explicitly, not silently equated with historical bytes.

The downloader uses bounded archive decompression and stops when the requested gzip member ends. Some Common Crawl records were truncated at collection and cannot be repaired by repeated downloading. PDF images remain essential because generative OCR can invent plausible Arabic. Every positive has visual page references. Non-positives marked extracted-text screening are provisional on that evidence; they are not represented as exhaustive image inspections.

Reproduction: install requirements.txt; run scan_languages.py (48 network workers by default), recover.py, then recover_streaming.py to retry archive failures. Review manually before rebuilding package. Source states are resumable. Scripts use a sibling afghan-chinese-deps directory if present, otherwise normal Python imports. Human review decisions are in review-notes.json; do not treat them as an automatic classifier.
