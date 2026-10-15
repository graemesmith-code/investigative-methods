# Afghan government PDFs: unidentified-language scan

> **Content screening update (15 October 2026):** The follow-up screen retained **two leads** (Russian extracted form text and a mixed Turkmen/Dari newspaper page), excluded 236 records, and left one damaged record unresolved. See [screened results and all 239 decisions](screened/README.md).

The complete scan found **239 records** in the FinePDFs unknown-language partition whose URLs are on gov.af or a subdomain: **228 distinct URLs** across **56 hosts**. The records span FinePDFs crawl dates from 23 March 2017 to 12 February 2025.

**These are not 239 confirmed foreign-language documents.** The unknown label means the dataset could not identify a language. Dari, Pashto and English may be present, and many records are forms or tables. Separately identified Chinese, Arabic, Russian and other language partitions are outside this count. Hosting on a government domain does not establish authorship.

The full local inspection bundle includes first-page previews and extracted text. This public repository preserves the record index, method and recovery script; it does not republish the source PDFs or extracted body text.

## Counts

| Item | Count |
|---|---:|
| FinePDFs records | 239 |
| Distinct source URLs | 228 |
| Government hosts | 56 |
| Complete recovered PDFs | 221 |
| Partial recovered PDFs | 8 |
| PDF not recovered here | 10 |

The complete copies comprise 202 Common Crawl captures and 19 files fetched from current source websites. A current copy may differ from the historical file. “Complete” means the retrieved file had no observed archive truncation and contained a PDF end marker; it is not a claim about the source document’s authenticity or original completeness.

## Files

- manifest.jsonl: one record per dataset row, with source URL, language fields, crawl date, Common Crawl pointer, dataset row provenance and recovery status. It omits extracted text and local-only file paths.
- selection-audit.json: all 14 scanned Parquet files and row-group coverage.
- summary.json: headline counts.
- download_pdfs.py: optional recovery script. It tries the cited Common Crawl capture first, then the current government URL if needed. It writes recovered PDFs under pdfs/ and updates the manifest.
- TECHNICAL-ANNEX.md: method, evidence and limits.

## Try it

Clone or download this folder. Install Python 3, then run:

    python3 -m pip install -r requirements.txt
    python3 download_pdfs.py

The script checks for existing local PDFs before downloading. Use python3 download_pdfs.py --retry to retry missing and partial copies. It limits each current-site PDF and decompressed archive record to 100 MiB.

Dataset: [HuggingFaceFW/finepdfs](https://huggingface.co/datasets/HuggingFaceFW/finepdfs). This is a processed, deduplicated Common Crawl dataset. A dataset crawl date is not necessarily the document’s publication date.


