# AER Cygnet report review method

## Scope and reproducibility

The review processes 12 user-provided PDFs locally without altering the originals. The set includes three drilling-report PDFs, three daily-completion PDFs, three service-company packages (two supplied as two parts each), and one invoice. There are 669 physical PDF pages, including two duplicated split-boundary pages and a blank invoice page.

`extract_aer.py` was executed against the local source directory. It uses PyMuPDF `get_text(sort=True)` to write page-preserving JSON and plain text, a SHA-256/size/page-count manifest, and a keyword index. The index is only a navigation aid. It does not classify compliance, identify causation, clean data, or assign timezones. A second script, `extract_service_timeline.py`, selects stage start/end times, metrics and comments while preserving physical page references. Both scripts are read-only for source PDFs. Their outputs contain source text and should remain private unless separately authorized.

The service script is a limited line selector: an end time is retained only when it appears on a selected line or elsewhere in retained text. It is not a complete stage-table parser. `extract_completion_chronology.py` preserves the executed raw-row indexing method and its known limitations in its module docstring: dataset-specific filename selection, unsorted file order, continuation text lost at page breaks, and uncorrected source inconsistencies. `check_split_boundary.py` reproduces the separate text/render comparisons. See [execution and validation details](VALIDATION.md).

## Human review and verification

Reviewers read operational narratives and stage summaries across the reports and compared daily-completion records with the Liberty service reports. Relevant pressure/rate plots and important statements were rendered with PyMuPDF and visually checked. Physical PDF page numbering starts at 1 and is used for every citation. Split files are not silently concatenated or renumbered. Identical text and rendered pixels confirmed that part a page 70 equals part b page 1 in both split packages.

## Interpretation boundaries

- Preserve former well names/UWIs in document headers and current identifiers in filenames separately. A matching licence and prior amendment record, not a guessed name change, anchors the linkage.
- Preserve the source's clock values. A report-generation GMT offset is not an operations timezone. No source operation timestamp is converted to UTC or compared to external second-level earthquake timing as an established fact until clocks are verified.
- Separate sand-bearing fracturing, pump-down, acid flushing, injection tests, milling, waiting, and mechanical repairs. A gap in fracture-stage summaries is not necessarily a gap in all fluid injection.
- Record contradictions, placeholders, unit/volume errors, copy-forward passages and wrongly labelled inserted pages without silently repairing them. Minute-scale differences between daily and contractor records are not exact measured response delays.
- A seismic message and an operational shutdown establish a recorded response, not earthquake magnitude, causal attribution, regulatory breach, notification to the regulator, or written restart authorization.
- Planned intervals and recorded stage sections are different counts. Blank rows and skipped stages do not prove missing PDF pages.
- A reported bubble-test result is an investigative lead, not a diagnosis of leak source, severity, environmental impact, or noncompliance.

## Public preservation boundary

Only reusable code, dependency information, this methodology and non-sensitive QA tests are intended for public GitHub preservation. Source PDFs, extracted text, source-derived detailed findings, personal invoice data, and private Drive links are excluded from that code/methods backup.
