# Drex for document processing: lessons for investigations

Recorded: 12 November 2026. Source: [Nace.AI product announcement, 11 November 2026](https://www.nace.ai/blog/introducing-drex-for-document-processing).

## Reporting takeaway

The useful idea is a selective second look at documents. A conventional parser first turns a page into text and layout. A small decision model then checks whether the extracted line, table structure or checkbox matches the page image. The pipeline sends only disputed material for correction. In principle, that could help process large document sets cheaply while preserving more table and page structure.

For investigative work, the promising use is triage and error detection: surface suspect names, dates, amounts, table rows or checkboxes for review against the scan. The output is still a machine reading. It does not establish that a document is authentic, that an extracted claim is true, or that the system found every relevant passage. Preserve the original file and check consequential passages on the page before quoting or building a finding on them.

## What Nace says, and what that evidence supports

Nace says its Nace Document Intelligence engine plus Drex scored 0.834 on its Parse Index, compared with 0.820 for the engine alone, and ranked first among 13 listed parsers. The company says the combined system improved on three of six benchmarks, was within noise on two, and performed better on phone photos in its tests. It reports lower median correction times when the system rewrites only pages or passages it judges doubtful.

These are vendor-reported results from a product announcement, not an independent evaluation. The leaderboard includes proprietary systems, different list-price costs and a seven-score aggregate; Nace also identifies one financial-document benchmark as its own non-public set. “Within noise” is Nace's characterization; the post does not provide enough information to independently assess every test's sample size, uncertainty or statistical design. The figures justify considering a small comparison, not adopting the product or repeating the ranking as settled fact.

The clearest methodological point is narrower than the sales claim: a checker can allocate expensive review to uncertain cases rather than treating every page alike. Whether this improves results on our documents remains unknown.

## Lessons beside Jev and OCR

- **Treat scores as a reading queue, not an editorial verdict.** The repository's Jev work already shows that a high score is not a probability of newsworthiness. A document parser's aggregate score has the same limitation: it cannot decide whether a record matters or whether an apparent anomaly merits a story.
- **Keep the page image attached to extracted text.** Layout-aware Markdown and page locations may make tables easier to inspect, but retain page numbers, coordinates or image crops and the source file. Verify numbers, names, dates, negations, checkboxes and table relationships visually.
- **Test the errors that matter to reporting.** Character accuracy alone is a poor proxy for whether a system preserves a contract amount, a date, a footnote, a row-to-column relationship or an exception in a scanned policy. Measure these separately.
- **Compare against the actual baseline.** The right comparison is the current searchable text or OCR on the same pages, plus a manual reference transcription for a small stratified sample. A polished extraction is not evidence of improvement by itself.
- **Keep correction provenance.** Save the first-pass output, the model's uncertainty decision, any correction, and the final human-checked text as separate versions. A correction model can introduce a plausible but unsupported word; being more readable is not the same as being more faithful.
- **Check retrieval as well as reading.** A parser can faithfully transcribe the pages it processed while missing pages, attachments, marginalia, stamps, appendices or a relevant document altogether. Record which files and pages entered the pipeline.
- **Count the full cost.** Compare processing charges, time spent preparing files, failed pages, manual checking time and rework. A low per-page price can still be costly if the review burden shifts to journalists.

This fits the existing LightOnOCR-3 note as a possible future comparison topic. No Drex account, upload, paid run or OCR comparison was undertaken for this note.

## A bounded test if later authorized

Use a modest set of public records already in the project and known to be difficult: scanned pages, phone photos, dense tables and forms. Include the existing OCR output where available and prepare a human-checked reference for the passages that matter. Compare the current OCR, the candidate parser alone and its selective-checking mode on the same pages.

Report exact-match performance for names, dates and amounts; table row/column preservation; checkbox and negation recognition; missed-page or missing-content rate; correction errors; processing and human-review time; and cost. Stratify results by document type and scan quality. Keep examples of both successful and harmful corrections. Do not upload sensitive or unpublished source material until data handling, retention, model training and access settings are confirmed.

**Status:** this is an assessment of a vendor announcement and a proposed test design, not a test result or endorsement.

## Technical annex: source and limits

Source reviewed: Nace.AI, “[Introducing Drex for Document Processing: document processing your agents can trust](https://www.nace.ai/blog/introducing-drex-for-document-processing),” published 11 November 2026. The source is the vendor's own launch post. It describes the system as Nace Document Intelligence plus Drex, reports benchmark and speed results, and gives examples of checking OCR lines, tables and checkboxes against page images.

This review did not retrieve benchmark data, independently reproduce the scores, inspect a dataset, test an API, verify pricing in a live account, or assess the privacy terms. Benchmarks may not predict performance on government filings, engineering reports, mixed-language records or poor scans in our corpus.

Related repository notes:
- [LightOnOCR-3 assessment](../2026-11-11/lighton-ocr3-assessment.md)
- [Jev/Exa contract-search experiment](../../experiments/06-jev-exa.md)
- [ATI evidence-file guide, including the seven-page OCR release and Jev accounting](../../annexes/ati-files.md)
