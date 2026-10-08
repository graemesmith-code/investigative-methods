# First evidence and coverage report

## Selection and technical result

The pilot enumerated PDF anchors from two official catalogue pages, deduplicated URLs, required exactly 14 parliamentary issues plus one evaluation, downloaded serially and validated PDF signatures. Each body has SHA-256, size, source and discovery URL. Poppler extracted all 676 pages using layout mode; page counts were checked against `pdfinfo`. Citation fragments use **physical PDF page numbers**, not printed page numbers. No exact PDF duplicates occurred. The chronology is filename/catalogue based, not inferred from directory dates.

25 pages had fewer than 80 extracted characters. They were flagged, not called blank or assumed to require OCR. A separate local Tesseract probe rendered all 25 of these pages (11 outputs exceed 80 characters, including cover/title and map text) and saved its output in `results/ocr-lowtext.json`; primary text remains unchanged. Text extraction can still miss text in images on otherwise text-rich pages, misorder columns, corrupt glyphs or collapse tables. No full visual audit or recall estimate was attempted. PDF p9 and p54 of the final report were rendered and visually checked for the acreage comparison below; neither issue was an OCR artefact.

The initial first-PDF HTTP 200 response was an archive notice, not a PDF. Following its explicit public “Continue to publication” link with the notice as Referer returned the PDF; subsequent PDF requests use that same public notice flow. This is distinct from the 403-denied LAC body, which was not retried. See download log. Source-check failures were CJOC catalogue 403 and one obsolete Publications terms URL 404; neither was retried. The catalogue links the actual [Canada.ca terms](https://www.canada.ca/en/transparency/terms.html). No public mirror or redistributed website was created; this private analysis copy is not a determination of downstream commercial publication rights.

## Tests executed and what survived

`code/discovery.py` scans page text for irrigation scope, benchmark changes, monitoring gaps and cost-comparison language. It produced **372 overlapping candidate contexts**, not 372 findings. The assistant selected a ten-page review packet from those contexts and read the surrounding pages. This purposive retrieval has no measured precision/recall and no independent model adjudication.

### 1. Acreage definitions: retain as a narrow verification question

The [final report PDF p9, printed p1](https://publications.gc.ca/collections/collection_2012/bcp-pco/CP12-2-14-2012-eng.pdf#page=9) describes 30,000 hectares as additional and prospective. Its [p26, printed p18](https://publications.gc.ca/collections/collection_2012/bcp-pco/CP12-2-14-2012-eng.pdf#page=26) uses a 17,200-hectare pre-project comparison. The [p54 table, printed p46](https://publications.gc.ca/collections/collection_2012/bcp-pco/CP12-2-14-2012-eng.pdf#page=54) instead has a 20,000-hectare baseline and 30,000 total target, marked only partly achieved with measurement still pending. These qualifications matter: the source did not assert that all the projected irrigation benefits had already been measured.

The [fifth report p26](https://publications.gc.ca/collections/collection_2009/bcp-pco/CP12-2-5-2009E.pdf#page=26) also has the total-target formulation. The [evaluation pp36–37, printed pp28–29](https://publications.gc.ca/collections/collection_2016/amc-gac/FR5-95-2015-eng.pdf#page=36) explains differing baseline/target concepts and the difficulty of measuring irrigated area using vegetation imagery. Therefore, simple subtraction is not a valid estimate of falsely claimed land. Possible explanations include editorial shorthand, differing definitions of improved versus newly irrigated land, revised survey coverage, and seasonal measurement.

**Status:** a source-grounded wording/definition discrepancy, not verified deception or a novel story. Required next evidence: underlying 2007/08 feasibility study, 2009 inception report, 2011–13 monitoring definitions and September 2014 project evaluation, followed by contemporaneous review/receipt records if any stronger claim survives.

### 2. Benchmark revisions: reject a generic concealment inference

The [fifth report p13](https://publications.gc.ca/collections/collection_2009/bcp-pco/CP12-2-5-2009E.pdf#page=13) openly explains an ANA benchmark change associated with changing deployment organization. The government's [September 15, 2009 release](https://www.canada.ca/en/news/archive/2009/09/fifth-quarterly-report-afghanistan-released.html) also announced revised benchmarks. A machine noticing a changed denominator is useful for retrieval; it is not evidence that the change was hidden. A meaningful test would freeze geographic/operational scope and compare both definitions over the same period.

### 3. Construction versus service: useful exclusion/control

Final-report school completion figures and the 2015 evaluation measure different things: buildings completed or repaired versus functionality, teaching, security and enrolment. A later nonfunctioning school does not automatically falsify an earlier completion count. Security deterioration, scope differences and double counting require school-level verification, with identifying details minimized. No protected pupil/teacher case records were collected.

**Novelty control passed:** Canadian Press reporting dated [March 16, 2015](https://infotel.ca/newsitem/afghanistan-audit-signatureprojects/cp32314565) already covered irrigation measurement uncertainty, school construction problems and limited outcomes. These broad findings fail the novelty gate. Graeme Smith's existing body of work must also be included before any promotion: [TVO's 2021 description of Ghosts of Afghanistan](https://tvo.me/tvo-original-ghosts-of-afghanistan-reveals-the-true-face-of-the-auforever-warau/) explicitly frames gaps between stated objectives and lived outcomes. This pilot did not watch the film or audit his complete Globe archive/books.

### 4. Cost-output comparator: queue, not allegation

Evaluation p36 points to a difference between implementing agencies' cost-output ratios. A valid financial comparison requires contract scope, canal difficulty, security costs, time period, output quality and currency/price basis. The cited project evaluation is a targeted acquisition lead. No improper payment, waste amount, procurement violation or misconduct has been established.

### 5. Knowledge/action timeline and release-version diff: blocked by absent bodies

A credible knowledge test needs a dated warning, a verified recipient/receipt, a later incompatible public statement about the same project and a reason routine explanations fail. This pilot contains retrospective evaluation rather than that complete chain. OIC 2026-53 provides a version-diff test case but no actual email versions were acquired. Inquiry exhibit citations similarly are not exhibit contents. These tests remain designs, not executed substantive comparisons.

## Novelty search coverage and limits

Six free web search queries were used for topical novelty checks: `Canada Afghanistan 2015 evaluation Dahla schools non functioning aid report CBC Globe Mail`; `"2026 OIC 53" Colvin`; `"Afghanistan" "benchmark" "2009" "Dahla" revised`; `Afghanistan "additional 30,000 hectares" Canada`; `"Dahla" "total" "2012" "Globe"`; `"Canada" "Afghanistan" "schools" "Graeme Smith"`. No claim of a comprehensive news review is made. Some results were irrelevant. The [NATO Association commentary](https://natoassociation.ca/was-it-worth-it-canadas-intervention-in-afghanistan-and-why-we-left-too-soon/) repeats the additional-acreage language; this demonstrates circulation, not independent validation or absence of prior criticism. Paywalled Globe archives, French reporting and full inquiry evidence were not exhaustively checked. “No exact match found” cannot support “unreported.”

## Decision thresholds

- **Acquisition go:** official public body actually downloads; war-relevant scope/date identifiable; permitted copying route; source checksum and stable page anchors; at most 5 new bodies/20MB before another checkpoint.
- **Discovery go:** at least one candidate yields same-scope claims and a concrete named missing record. This pilot meets that modest threshold for irrigation definitions and monitoring sources.
- **Novelty go:** primary evidence contains a consequential fact beyond published reports/inquiry findings, survives targeted English/French and Graeme-work checks, and has independent corroboration or a defensible documentary chain. None meets it yet.
- **Stop or pivot:** another small batch merely reproduces the 2015 evaluation; relevant bodies require applications/outreach; access is denied; personal-risk review is needed; or scope/measurement reconciliation explains the discrepancy.
- **Front-page assessment:** editorial judgment only after strong novelty and corroboration. No candidate here earns that claim.
