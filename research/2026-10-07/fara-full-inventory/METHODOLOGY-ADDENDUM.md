# How this investigation worked—and what it cannot tell us

English-first briefing for the requested morning email · 7 October 2026

Imagine checking two sets of school forms. One says who hired a representative; another says who owns or directs the organization being represented. A difference is a reason to check the paperwork, not proof that someone lied. The names, dates, job being done and rules must all match first. That was the basic idea of this experiment.

**The result remains a bounded negative finding:** we did not establish concealed foreign control behind a major lobbying campaign. TransCanada is a historical 2010 parent-disclosure question, not a contemporaneous LDA/FARA collision. Honda and Novartis quarterly reports explicitly identify foreign parents, so earlier concealment interpretations were withdrawn. The [final report](REPORT.md) ranks useful follow-up questions, not guilt.

LDA means the Lobbying Disclosure Act: its filings describe lobbying clients and work, and ask about certain foreign interests. FARA means the Foreign Agents Registration Act: its filings describe certain work for foreign principals. A registrant is the person or firm filing; a client hires it; a foreign principal is the represented foreign party; an owner may be another legal entity entirely. Those labels are not interchangeable.

## Where the idea and evidence came from

**Rabbit supplied the map, not the case evidence.** The saved Rabbit catalogue named US Senate Lobbying Disclosure data and DOJ FARA eFile/bulk data as sources that could be compared. The repository's X04 card turned that pair into a test: compare an explicit negative foreign-entity answer with dated ownership evidence about the same legal client. The [saved source card](../lobbying-control-pilot/source-card.json) traces these to SYS-0117 and SYS-0118, in references/rabbit/originals/Rabbit2(1).txt at lines 7734 and 7776. The card explicitly said no substantive filing had yet been tested. The attached guide could not be transferred, so the repository card and the user's quoted item 10 supplied the starting definition.

**The actual documents came from elsewhere.** Initial browser searches targeted the official DOJ filing domain with phrases such as “Exhibit-AB-2025” and “wholly” or “shareholders.” The exact queries are preserved in the [first technical annex](../lobbying-control-pilot/TECHNICAL-ANNEX.md). They produced a frozen convenience sample of 19 indexed FARA documents, including inaccessible results and government/individual exclusion controls. They did not start with a list of famous companies. But search-engine indexing and ownership-related wording inevitably shaped what appeared.

Next came official LDA API queries and original print forms; DOJ reports to Congress; user-supplied official DOJ CSV exports; and the five official House 2025 XML archives. Ownership leads were checked against original company accounts, SEC filings and corporate-registration documents available without payment. IAI's 2024 financial statements were obtained through Germany's lobbying register; its 2025 statements came from IAI's website. Jev did not discover those documents. Rabbit was not a live case-search engine in this pilot, and catalogue descriptions were never treated as proof of ownership.

## The wider IAI pattern

IAI means Israel Aerospace Industries. Think of a corporate family tree: a parent company, an intermediate company and operating subsidiaries. Our initial Stark document led us into that tree. Reading IAI's ownership table then led to ELTA North America and IAI North America. This is a source-driven expansion, but it is **not three independent, randomly discovered examples**. The cases share ownership documents and arose from following the same family tree. Their concentration cannot establish an IAI-wide pattern of concealment or an incidence rate for Israeli or other foreign companies.

| Relationship | What the originals show | What that supports |
|---|---|---|
| Stark / Bramer and Emanuel | Two LDA registrations answer No. The FARA contract identifies Stark → IAI North America → IAI; company accounts give ownership snapshots. | A specific unanswered disclosure question. Separate firms and engagements must be kept separate. Acquired 2025 outside income is $136,500, below the major threshold. |
| ELTA North America / CR Federal | LDA registration answers No; IAI accounts name a wholly owned same-named subsidiary. A product sheet corroborates an address, not a legal registration number. | A smaller lead requiring a firm legal-entity bridge and filing-date chain. No exact ELTA FARA Exhibit A was acquired. |
| IAI North America / Emanuel | The parent IAI is expressly disclosed at 100%, including in an amendment; the previous quarterly report already named it. | At most an ultimate-parent completeness question. It is wrong to describe all foreign ownership as hidden. Aircraft/Aerospace names need authoritative reconciliation. |
| IAI North America / Pillsbury | The original registration lists both IAI and the State of Israel, with zero contributions. | An affirmative-disclosure counterexample. Later blank additions fields do not erase the earlier disclosure. This does not certify every aspect of legal compliance. |

The direct source links and exact amounts are in the [IAI/Stark/ELTA dossier](../lobbying-control-pilot/README.md), which preserves earlier model output and must be read with the superseding [final report](REPORT.md). Stark's newer quarterly narrative also openly describes Arrow missile defense as a joint US–Israeli program. That weakens a claim of hidden international character, although it does not settle the specific ownership checkbox.

A subsidiary can be foreign-owned while doing work that falls under an exemption or a different reporting regime. Annual accounts describe ownership at stated dates, not every intervening day. Neither an ownership table nor a FARA registration alone tells us that a particular LDA answer was unlawful. We did not contact the companies, buy records or obtain private daily share registers.

## What went into the pipeline

A pipeline is simply a repeatable sequence of small jobs. Its inputs were different kinds of records, not one giant document handed to a model.

| Input | Structure and useful fields | How it was used |
|---|---|---|
| DOJ catalogue exports | Three CSV tables: registrants, foreign-principal relationships and document inventory; names, registration numbers, dates and document URLs | Find candidate relationships and original filings. A catalogue row is not the filing itself. |
| House archives | One XML document per filing version; document/relationship identifiers, client, registrant, period, amounts, foreign entities, affiliates and narratives | Screen the full acquired 2025 report-year archive consistently, preserving roles and amendments. |
| LDA API | Paginated JSON objects with UUID, client and registrant IDs, type, year, posting time and original-form URL | Locate histories and order amendments. Current API names and entity arrays are not authoritative substitutes for old printed forms. |
| Original filings | HTML forms or PDF/image documents, with sections and sometimes page numbers | Verify actual checkboxes, client names, money, ownership descriptions and activities. |
| Ownership and rule sources | Company accounts, SEC/corporate filings, statutes, regulations and dated official guidance | Check who controlled which legal entity at the relevant date, and what the rules then required. |
| Compact model dossiers | JSON with cited evidence, bounded facts, uncertainties and fixed questions | Test whether Jev could assess the evidence consistently; later test only literal checkbox extraction. |

The [provenance manifest](supplied-source-provenance.json) preserves original hashes, columns, date ranges and repairs. Scripts store hashes and original paths, so a reviewer can trace an output back to bytes rather than trust a summary.

## What ordinary code did, and what models did

**Code did the repetitive bookkeeping.** Python downloaded and paginated records, parsed CSV/XML/HTML, stored searchable SQLite tables, normalized names, generated candidate matches, kept dates and roles separate, removed duplicate filing IDs, selected amendments, added amounts and enforced spending reservations. OCR helped search selected image pages; it was not accepted as a visual checkbox judgment. These jobs do not require a language model to read every word of every archive.

Name matching began with exact normalized names, then controlled suffix/punctuation variants, then spelling similarity of at least 0.94 for sufficiently long names. A later pass searched separately within foreign-entity entries, affiliate entries and foreign-interest narratives. Narrative matching used a bounded normalized phrase of at least 12 characters and two words. These choices can miss aliases and can create false matches. A match therefore means “inspect this,” not “same legal entity proved.” For example, Bank of Canada must not be inferred from the words inside Royal Bank of Canada.

**The assistant performed source review and editorial synthesis.** It selected follow-up documents from the evidence, checked dates and legal scope, inspected selected original images, wrote and debugged the code, compared alternative explanations and drafted the report. This is AI-assisted analyst review, not an assertion that a human independently adjudicated every result. The parent also arranged native reviews. Their actual underlying OpenAI deployment/model IDs are not recorded in the permitted project evidence. The parent reports that it selected no model overrides. We cannot truthfully name a particular OpenAI model or say it was chosen over another for this work. Product branding, default-agent labels and available model menus are not execution receipts.

**The recorded paid model was Jev `jev-1.13.0`.** That exact identifier appears in both requests and responses. It was used because the user explicitly asked to test Jev, with a pinned version, saved prompts/responses and a hard budget guard. Its first task was to assess compact cited dossiers for identity, dated control, disclosure, campaign size, innocent explanation, missing evidence and follow-up priority, including an abstention option. Later it received only HTML checkbox fragments and fixed answer choices. These were structured outputs, not independent investigations. We have no evidence about Jev's underlying architecture and do not label it an OpenAI model.

Documents were treated as untrusted evidence. Model instructions expressly said to ignore instructions embedded in them. Synthetic controls included malicious instruction text, missing fields, both/neither boxes checked, later acquisitions and misleading assumptions. The ordinary parser provided a model-free comparison.

## Why the Jev legal ranking was withheld

A model can sound confident while mixing incompatible claims. Saved Jev outputs sometimes called a case a documentary mismatch while saying contemporaneous control was not established; a real affirmative-disclosure counterexample still received an elevated priority. A revised atomic synthetic-control set passed, but that did not cure the real-case inconsistencies or validate legal judgments. The [audit](../lobbying-control-pilot/jev/audit.json), [control results](../lobbying-control-pilot/jev/controls/evaluation.json) and earlier failed control file retain this history.

The narrower test was frozen before new paid calls: read the checked answer in section 14, without deciding whether it was true or lawful. Both Jev and the HTML parser passed all 16 listed test items. However, there were only **two distinct real-form payloads plus six synthetic payloads**; eight listed results reused cached answers. This was not 16 independent real documents. It demonstrated no accuracy advantage over code, and it did not validate a suspicion ranking. The [protocol](../lobbying-control-expansion/jev/protocol.json) and [results](../lobbying-control-expansion/jev/results.json) show exactly what was tested.

The biggest improvements came from more original evidence and better field coverage. Reading quarterly narratives corrected the Honda/Novartis leads. Reading amendments changed PPD's apparent $1.2 million quarter to $120,000 and Arm's $1.1 million quarter to $110,000. A later blank additions box does not mean a previously named owner vanished. These are reasons to reconstruct a filing history before asking a model to rank it.

## Exactly which years and how much of US lobbying?

**This was not the full US lobbying corpus.** The broadest uniform LDA input was all five downloaded House archives labeled report year 2025: four quarters and the registration archive. They contain **109,389 XML records**, all marked 2025: **101,537 quarterly documents and 7,852 registration/amendment documents**. The latter are 7,010 registrations and 842 amendments. The quarterly total includes regular reports, amendments, terminations and amended terminations. It represents **97,567 distinct relationship-quarters plus 3,970 additional versions**, not 101,537 independent campaigns. There were no duplicate document IDs or byte-identical XML duplicates across those five archives.

Signing dates run from 1 January 2025 through **2 October 2026**. A form reporting 2025 can be amended in 2026. A signing date is not a receipt date; these archives are not a census of everything received during calendar 2025. The [archive scope audit](archive-scope.json) gives every report-type count and each archive's date range. The method did not cover every historical LDA year nationally, all future amendments, state/local lobbying, unregistered activity or every conceivable name alias.

The separate, targeted original-form collection spans **report years 1999–2026**. It contains **4,143 distinct LDA originals**, including 1,287 for 2025 and 94 for 2026; all other years were selected histories, not national samples. Of the 4,143, **3,658 HTML forms** passed structural narrative parsing, **485 PDF/image documents** required abstention from that extraction, and **only five selected image pages** were visually adjudicated in the final image-review log. Those five do not represent all image documents. The exact annual breakdown is in [methodology-audit.json](methodology-audit.json).

The DOJ CSV input is broader in historical dates but shallower in document reading: **7,090 registrant rows, 17,765 principal relationships and 154,309 document rows**, including **126,480 distinct PDF URLs**. Registrant and principal registration dates range from 1942 to 2 October 2026; document date stamps extend to 6 October 2026 and include an anomalous year-0200 entry that was preserved and flagged. The full supplied catalogue was acquired; the full set of PDFs was not. A row advertising a public-office document is not online access to its contents. Blocked files were not counted as absent filings.

## Selection, exclusions and the meaning of “major”

The experiment expanded in three steps. First came the 19-document indexed FARA sample and its IAI ownership-led follow-ups. Second came a 2025 LDA API screen of 780 filings with a million-dollar reported amount, involving 259 client IDs. Annual/amendment retrieval yielded 1,184 forms and exposed inflated or corrected initial figures; 27 selected all-years histories and missing-registration searches broadened that stage. That selection could miss campaigns spread over several smaller quarters. Its “255 major relationships after amendments” count belongs to that earlier screen, not the later FARA-linked cohort, and must not be added to it.

Third, the five-archive House screen covered every acquired 2025 relationship and compared it with every supplied FARA principal row. Client-name matching produced **598 candidate edges across 222 House relationships**. Only **29 relationships** had a principal-period overlap with 2025. Historical matches were retained separately: an old FARA relationship is a discovery clue, not proof of current control. Additional role matching produced **576 edges across 149 relationships**. The union was **343 relationships**, not 371, because some appeared in both searches.

Of that union, **25 relationships** met the numeric major threshold and received original-based materiality/disclosure review. The other **318 did not qualify on the acquired numeric data**; they were not cleared legally. Unmatched names also were not cleared. The 25 are a discovered review cohort, not an estimate of the prevalence of undisclosed ownership. Only one initial client-matched major candidate also had a catalogued FARA period overlapping 2025; the historical category should not be presented as current cross-regime conflicts. The role-based screen deliberately retains express disclosures, many of which weaken rather than strengthen the hypothesis.

“Major” means at least **$1 million in one year's reported outside income or in-house expenses for a registrant–client relationship**, with latest relevant amendments selected. Those two measures are not added together. Neither is automatically foreign funding. Preliminary archive selection used signing date/document ID; selected major amounts were checked against API posting chronology and original forms. The [triage list](cohort-triage.json), [client-match coverage](full-match-coverage.json), [role-match coverage](full-role-coverage.json) and [original reconciliation](major-original-reconciliation.json) preserve the selection and its limits.

## Tokens, dollars and the whole-experiment question

Tokens are chunks of text a model processes or returns. Downloading 109,389 XML files does not mean all their text was sent to Jev—or that their byte sizes reveal how much text the assistant processed.

| Saved Jev ledger | Actual calls | Reported input tokens | Reported output tokens | Estimated cost |
|---|---:|---:|---:|---:|
| First pilot | 42 | 67,526 | 11,087 | $0.002858 |
| Expansion | 8 | 4,111 | 328 | $0.000177 |
| Total | 50 | 71,637 | 11,415 | $0.003035 |

That is **83,052 provider-reported Jev tokens**, counted once per actual ledger attempt. Repeated saved response files and cache hits are not counted again. Tokens are measured provider response fields; dollars are estimates from those fields and the then-verified $0.042 per million input-token price, free output and per-call upward rounding—not an invoice. The sum of conservative reservations for the 50 actual calls was **$0.15**, under the same authorized $15 ceiling. Expansion accounting carried forward the first stage's full $0.126 reservations, so its top-level $0.126177 accounting figure is not an extra bill to add to the first stage. No calls were made in the full-inventory continuation or this addendum.

**Total token burn for the whole experiment is unknown, with no credible upper bound from the available records.** The Jev counts exclude the parent conversation, executor reasoning, native/cloud reviews, tool processing and any earlier Rabbit/source-inventory creation. No permitted telemetry measures those components. The user's reported 90% weekly allowance remaining does not translate into tokens, dollars or this experiment's consumption. Counting words in saved documents would give false precision because we cannot reconstruct how often text was processed or how the platform accounts for reasoning, caching and tools. The honest answer is an audited Jev subtotal, not a fabricated whole-experiment estimate.

## Reproduce this addendum without spending anything

Run `python research/2026-10-07/fara-full-inventory/audit_methodology.py` from the repository root. It reads only saved project ledgers and audit files, sums actual attempts, checks totals and writes methodology-audit.json with hashes of its inputs. It makes no network or model requests and reads no credentials or session logs. The [first ledger](../lobbying-control-pilot/jev/ledger.json) and [expansion ledger](../lobbying-control-expansion/jev/ledger.json) are the token evidence; the saved price-verification files distinguish pricing from provider usage.

This addendum changes no case findings and starts no new research. It is material for the parent's scheduled email; no email was sent by the executor.
