# Afghan government PDFs: screened reading selection

> **Scope correction (15 October 2026): This package screens only the unknown-language category. It does not fulfil the broader request for all languages other than English, Dari/Farsi and Pashto. Separately labelled foreign-language categories still require a complete search. See [the correction](../SCOPE-CORRECTION.md).

## Findings

The content screen retained **two leads** from the existing 239-record corpus. It excluded **236 records** and left **one damaged record unresolved**.

| Decision | Records |
|---|---:|
| English, Farsi/Dari and/or Pashto content excluded | 235 |
| Photograph with no substantive document text excluded | 1 |
| Other-language material retained | 2 |
| Damaged source unresolved | 1 |

The initial corpus was a selection from FinePDFs' **unknown** language configuration. It had not been adequately screened for the requested languages. Unknown is not evidence of foreign-language content.

### 1. Russian railway / consignment form — original item 17

- Host: ara.gov.af.
- Source filename: نمونه بارنامه.pdf (“sample waybill”).
- Russian field labels occur in FinePDFs page segment 3: sender, departure station, consignee, destination station, wagon, cargo and customs formalities.
- **Readable extracted text is available, but the original recovered PDF is truncated and cannot be opened reliably.** Its archive payload is exactly 1,048,576 bytes. A fresh live-source attempt returned HTTP 502.
- Crawl date: 21 July 2024. Publication date is not established. The 2021-07 URL directory is only a path clue.
- This is a form/template lead. The extraction does not establish a completed shipment, a specific partner or a bilateral agreement.

### 2. Gorash page in Turkmen and Dari — original item 117

- Host: mobta.gov.af.
- Source filename: gorash4 (95).pdf.
- Full one-page original PDF is available; the printed page is numbered 4 and dated **20 Saratan 1395**.
- The right-hand half contains a substantial Turkmen article; some lower-middle verse is Turkmen. Other columns contain Dari. Retained because it contains substantial material outside the excluded languages.
- The masthead identifies Gorash as a Turkmen publication of the Ministry of Borders and Tribal Affairs. The ministry's [1399 annual report, printed page 11](https://www.mobta.gov.af/sites/default/files/2021-02/%DA%AF%D8%B2%D8%A7%D8%B1%D8%B4%20%D8%B3%D8%A7%D9%84%20%DB%B1%DB%B3%DB%B9%DB%B9%20%D9%85%D8%A7%D9%84%D9%8A.pdf) also describes Gorash publishing in Turkmen in Jowzjan.
- A domestic minority-language audience is the most plausible interpretation of this page. Its language alone does not establish a foreign diplomatic audience.
- Crawl date: 20 February 2019.

## Reading package

The downloadable package supplied in the conversation is `afghan-government-screened-reading-package.zip`. Extract it and open `START-HERE.html`. It includes the original Gorash PDF and page image, Russian extracted-text reading copy, full 239-record audit, source metadata, and clearly labelled damaged Russian PDF bytes in the technical folder. The bulk reading files are not duplicated in this repository.

## Coverage and limits

Text excerpts were reviewed for every record; complete available extractions were swept for script anomalies; native PDF text extraction was attempted again. **147 selected page images from 75 records** were inspected, prioritising failed extraction and contradictory language tags. Long repetitive documents were sampled. This is not a word-by-word or image-by-image review of every original page.

Sixteen language exclusions depend on incomplete or text-only sources and remain provisional. Item 137, a truncated Higher Education Weekly PDF, is unresolved: recovered spreads show Dari/Pashto and an English masthead, while later content is damaged or missing. It is not included as a foreign-language lead.

Short logos, agency headers, stamps, proper names and conventional religious formulae were not counted as substantive other-language sections. In particular, item 185 is an **English table of Chinese employees**; the filename does not make it a Chinese-language document. Item 130 is an English scholarship list with incidental Thai website text.

Scope is the existing unknown-configuration corpus only. Separately labelled Chinese, Russian, Arabic and other FinePDFs configurations have not been searched in this follow-up. No conclusion about the total number of foreign-language Afghan government PDFs follows from these two survivors.

## Audit files

- `screening-audit.jsonl`: one decision per original record, with language observations, notes, source URL, crawl date, provenance, source completeness and visually inspected pages.
- `screening-summary.json`: counts.
- `METHODS.txt`: technical account and limitations.
- `visual-pages.json` and `extra-visual-pages.json`: page-review log.

These are assisted editorial screening judgments, not output from a validated automatic language classifier. The audit keeps original item numbers so decisions can be compared with the first package.
