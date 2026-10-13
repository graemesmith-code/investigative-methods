> Historical initial-pass snapshot. Current opportunity classification is in [the revised report](../../REPORT.md); original audit judgments and counts are preserved here.

# Cheap AI and overlooked corruption-reporting tests

Graeme Smith · 13 October 2026 · selective research review

**No opportunity passed all the evidence, novelty and AI-benefit checks.** The closest practical test is to compare a public procurement decision with the documents the bidder actually submitted. Both sides were accessible in a bounded Ukrainian sample. But procurement AI screening already existed in 2018, the sample showed no contradiction, and this review did not demonstrate that a cheap model improves on ordinary parsing and human review. It belongs in a methods benchmark, not a list of newly unlocked scoops.

This is a substantial source census followed by selective reading, **not a claim to have read the entire decade**. The [coverage matrix](COVERAGE.md) separates enumeration, acquisition, machine screening, contextual reading and deeper assessment. All fifteen organizations are included; the largest gaps concern AntAC's older archives, The Sentry's publication dates, restricted downloads and unenumerated TI national chapters. No paid calls, outreach, email or live investigation occurred. **Incremental cash spend: US$0.**

## The closest usable tests, ranked as conditional designs

These are the best surviving *designs*, not retained investigative finalists. Their order reflects how cheaply a journalist can resolve the next uncertainty, rather than the severity of suspected wrongdoing. Let a defined slice of public data choose the subjects. None of the access controls is a suspect.

### 1. Does a procurement decision accurately describe the bidder's evidence?

Why it matters: a wrongly described missing qualification could exclude a bidder, while an inaccurately accepted qualification could undermine fair competition. AntAC's [25 May 2026 analysis](https://antac.org.ua/en/news/cabinet-of-ministers-allows-construction-material-prices-to-be-concealed-in-procurement-for-the-reconstruction-of-war-affected-regions/) identifies tender conditions tailored to particular contractors. That motivates checking the actual rules, evidence and decision together, rather than flagging a company's reputation.

**The test:** if a rejection says a required certificate was missing, compare that claim with the complete, timely submitted documents for that bidder and tender. A valid matching certificate would nominate a documentary contradiction for expert review. An empty keyword search would not. Certificates required only in certain circumstances need a legal-applicability check.

A free [Prozorro tender API sample](https://public.api.openprocurement.org/api/2.5/tenders/bc2b85df808042fa8157d6ddbf79d0c6) supplied original qualification rules, bidder staffing evidence and the award decision. Exact tender, lot, bid, award and document-version IDs connect the records. The sampled decision and staffing table were compatible; the full qualification and correction history was not adjudicated. Both streams are original claimant documents in one publication system, not independent proof that a qualification is true.

Cheap AI could propose pairs between differently worded Ukrainian requirements, evidence and decision reasons. Code already retrieves files, extracts ordinary text, joins IDs and checks dates. A procurement specialist must resolve conditional rules, lawful substitutions and corrections. Missing documents or a lawful exception are the strongest innocent explanations.

**Why it is held:** [DOZORRO described AI screening in 2018](https://dozorro.org/blog/yak-shtuchnij-intelekt-dozorro-monitorit-zakupivli), including winner selection and disqualification risks; [proBI already supports document/proposal analysis](https://dozorro.org/tools/pro-bi). A transparent, version-aware comparison could still be useful, but its unmet capability and time saving have not been established. First compare 20 data-selected tenders against these existing workflows and a basic text-search baseline. Stop if complete histories are unavailable or expert legal interpretation consumes the saving. Estimated review: 8–16 specialist hours, rate unknown; free-download/code gate cash $0. A future token-only pass would likely cost dollars, not hundreds, under the explicit assumptions in the [cost annex](../../annexes/why-now-and-costs.md). No paid pilot was run.

[Evidence, original passage, tests, joins and stop rules](../../teams/integrity_whistleblowers/findings.md).

### 2. Do a company's shareholder and control declarations agree at the same date?

Why it matters: a measurable class of inconsistent public ownership declarations could make a registry less useful for tracing corporate control. Global Witness's [The companies we keep](https://globalwitness.org/documents/466/The_companies_we_keep.pdf) already proposed cross-checking shareholder information against the register of people with significant control. That register records certain ownership or control relationships; it is not proof of the true beneficial owner.

**The narrow test:** for an ordinary company at incorporation, compare a natural person's holding of more than 25% of a single share class with the company's applicable control declaration at that date. Check the complete share denominator, voting rights, exemptions, nominees and later corrections. [Current Companies House guidance](https://www.gov.uk/government/publications/people-with-significant-control-summary-guidance/summary-guidance-for-companies-register-of-people-with-significant-control-pscs) describes the threshold; a historical comparison must use the rules operative then. Current ownership cannot substitute for historical ownership.

A free incorporation PDF and separately published control page for an ordinary access-control company agreed. The PDF was searchable: ordinary code could extract the relevant fields. There was no inconsistency and no need for AI in this control.

**Why it is held:** Global Witness had already suggested the comparison using a 2018 snapshot. An AI benefit might exist for difficult historical images or irregular rights language, but that sample and benchmark were not run. Later confirmation statements describe changes, so reconstructing history requires a baseline and intervening changes. First test 30 registry-selected incorporation records; use code alone if it works. A nominee arrangement, different voting rights or filing timing could resolve a mismatch. Free-tool gate cash $0 assuming existing hardware; legal-review time and any OCR compute remain unmeasured.

[Independent access control, original passage and temporal safeguards](../../annexes/audit/audit.md).

### 3. Is a newly disclosed mining payment absent from the matching recipient disclosure?

Why it matters: a genuine omission from a government's disclosure universe could affect accountability for public revenue. NRGI and Sherpa show how fragmented payment reports and inconsistent categories make this laborious. Their existing work also supplies warnings against treating every numerical difference as missing money.

**The test:** compare the same legal entity or bridged project, government recipient, payment category, cash period and currency treatment. Check whether an externally reported payment lies outside the government's documented disclosure universe after thresholds, exclusions and adjustments. Company total minus government total is not enough.

The free 2023 DRC EITI report, annex workbook and same-year company payment report were acquired. But the needed detailed reconciliation annex was a placeholder pointing to a separate workbook that was not acquired. A tempting US$21.9 million Kamoa residual was already published by EITI; another apparent royalty difference lacked a defensible entity/project, currency and payment-category bridge.

**Why it is held:** the key evidence is missing, the sampled gap is old news, and the workbook is already structured. AI could suggest multilingual category mappings, but cannot invent receipt allocations or contracts. First acquire the missing public annex and establish three complete issuer-year controls. Stop numerical comparison until all accounting definitions match. Free-tool acquisition gate cash $0; tax, translation and review time unmeasured.

[Original bottleneck, acquisition manifest and definitions](../../teams/secrecy_ownership/findings.md) · [independent failed-bridge audit](../../annexes/audit/audit.md).

## What was deliberately excluded

The [rejection ledger](REJECTIONS.md) records concrete failures across all fifteen organizations. Especially consequential exclusions were:

- **Trade gaps as firm wrongdoing:** aggregate imports and exports do not identify an individual company's false invoice; product, valuation, timing and transport definitions differ.
- **Names as transactions or hidden control:** a sanctions identity match or corporate relationship cannot prove a prohibited payment, bribery or concealed direction. Decisive bank or internal records often remain private or leaked.
- **GPU configurations as smuggling:** C4ADS's server-label blind spot is specific and potentially interesting, but original Chinese procurement retrieval failed and the vendor-to-configuration bridge remained incomplete. A purchase notice would still not prove delivery or an unlawful export.
- **Quiet regulators as absent enforcement:** published decisions do not provide a complete universe of supervisory action.
- **Construction price gaps without equivalent materials:** no matched specification, unit, tax, transport and period pair passed; legal publication exceptions also matter.
- **AI ownership discovery from closed registries:** cheaper models do not open a registry or establish lawful bulk-processing permission. Restricted Lumen processing is excluded.

## What is actually new in 2026?

There is evidence of new prices and stronger advertised model capabilities, not evidence that these reporting methods were previously impossible. [GPT-4o mini already offered cheap text/image processing in July 2024](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/). [Luna's July 2026 price reduction](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) and [Haiku 5.5's October launch](https://www.anthropic.com/claude-haiku-5-5) make another benchmark worthwhile. Vendor claims are not journalism-specific validation.

The useful next result would be measured: does a model preserve evidence and save expert review time on difficult documents, compared with code and existing NGO tools? This review supplies the corpus, controls and stop rules for that question. It does not establish a newly discovered allegation, a confirmed AI saving, or a hidden-record breakthrough.

[Coverage and gaps](COVERAGE.md) · [complete inventory](../../source-inventory.jsonl) · [technical log](../../TECHNICAL-LOG.md) · [reproducibility instructions](../../README.md).
