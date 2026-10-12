# Follow-up technical results

12 October 2026. The original 100-record batch and its results remain unchanged. This is a selected follow-up, not a blind replication. The batch was checkpointed before the detailed follow-up in [FOLLOWUP_BATCH.json](FOLLOWUP_BATCH.json).

## Denominators and dispositions

- Original batch: 100 records, 35 Au, 2019–2023. 94 numerical pairs; 45 passed the preliminary narrow screen, with 19 within display precision and 26 unresolved numerical differences. A further 49 numerical pairs remain blocked by comparability gates. Five Western claims were absent and one numerical component was unavailable. Zero certified company contradictions.
- Follow-up: 25 known recurring lead records, including 10 Au. Two 2019 gold records are excluded for partial acquisition periods. The remaining 23 are parked because measurement and original-submission provenance are not closed. No lead was promoted to a contradiction. See [followup-case-ledger.json](followup-case-ledger.json).
- Additional language/provenance controls: **43 checks, 33 distinct entity/metal/years, all within the specified precision; seven Au checks represent five distinct Au years.** Composition: 25 Nexa rounded bilingual comparisons, ten Nexa SEC–SMV exact comparisons covering five metals in two years, and eight Antamina exact bilingual comparisons. The SEC–SMV checks overlap the Nexa metal-years. Do not add these to the frozen 100-record denominator or treat them as independent trials.
- Eight quarterly gold diagnostics are another view of two existing 2023 records, not eight new annual discoveries.

## 1. Nexa: original Spanish government-hosted evidence

The downloaded original company annual report hosted by Peru's SMV is marked preliminary, subject to shareholder approval, and digitally signed on 24 February 2022. It gives Cerro Lindo's 2021 fine Zn/Cu/Pb production and Ag/Au contents on PDF page 77. Each of the five quantities exactly matches the English parent SEC 20-F's same mine/year table. Both represent 100% mine output, not parent equity attribution.

The SMV-hosted 2024 company annual report is also explicitly marked preliminary and subject to shareholder approval, digitally signed on 27 February 2025. It repeats **2023** quantities on PDF pages 108–109. These exactly match the 2023 SEC filing: Zn 78,209 t; Cu 28,588 t; Pb 13,042 t; Ag 3,540,975 oz; Au 3,418 oz. The Spanish source is a later comparative disclosure, explicitly not a contemporaneous 2023 ESTAMIN submission. These are regulator-hosted preliminary company statements, not confirmed final approved annual reports or original mining returns. They are useful agreement/version evidence; no false government statement was identified.

Five years of Spanish quarterly-results annual columns also agree with the English SEC figures at display precision across these five metals. Some Spanish tables use kt, koz or MMoz. Agreement at coarse precision does not imply underlying unrounded equality. Annual-column mappings were manually reviewed after reading headings. Registry years were never substituted for production periods.

Sources, labels, reviewed column indices, values, precision allowances, page/table/line locators and fingerprints are in [followup-language-controls.json](followup-language-controls.json). Exact and rounded controls are separate. The parent SEC filing, subsidiary SMV annual report, company publication, exchange-hosted filing and ministry compilation are distinct source classes. The BVL English release is exchange-hosted, not a government filing merely because it is on BVL.

**Remaining ministry gate:** Cerro Lindo's MINEM zinc totals are still higher. The 2021 technical report describes separate concentrate streams and combined Pb+Zn impurities in copper concentrate; it does not supply the actual annual cross-product Zn assays needed for reconciliation. Planning payability percentages and metallurgical recovery coefficients are not historical correction factors. Its executive-summary production label also requires careful interpretation alongside ore tonnage/grade before importing another quantity.

## 2. Antamina: language equality and product scope

The operator's 2021 English/Spanish sustainability reports, PDF page 16, agree for Cu/Zn in the 2019, 2020 and 2021 columns. Its 2023 bilingual reports, section 3.2, also agree: Cu 421,824 t and Zn 464,116 t. These operator quantities differ from Teck's 2023 100% quantities and from MINEM's compilation. Teck's series was not silently replaced by retrospective operator figures.

A company-authored 2024 technical report, downloaded from a third-party replica, describes separate concentrate streams and explicitly labels plant recovery to each metal's principal concentrate. It supports keeping product coverage unresolved; it is not proof that MINEM aggregates all streams. The replica's hash and origin are retained, and no claim is made that its hosting independently confirms a regulatory submission.

We calculated a conditional physical test from actual reported concentrate masses. Assigning the entire 2023 Cu gap to zinc concentrate would require about 1.478% Cu in that concentrate; assigning the Zn gap to copper concentrate would require about 4.165% Zn. Across 2019–2023 the analogous requirements are roughly 1.07%–2.14% and 3.75%–4.48%. **These are inferred required compositions, not observed assays, verified plausibility bounds or a reconciliation.** Other streams, revisions and timing could contribute. The calculation is reproducible in [followup-antamina-product-hypothesis.json](followup-antamina-product-hypothesis.json). Source versions are 2021 report for 2019–2021, 2022 report for 2022 and 2023 report for 2023.

The publicly filed Wheaton 2025 AIF repeats Teck-like historical quantities. Repetition is not independent measurement validation. No original company ESTAMIN return and amendments closing the stream/assay question were obtained. Park all ten Antamina lead records.

## 3. Gold: period, commercial deductions and quarterly tests

Pan American's 2023 AIF gold-segment table footnote 3 specifies rounding to the nearest hundred. It does not label these mine quantities payable production. The Q1 SEC table separately reports production and total payable production and defines the latter as commercial-contract deductions. We used mine production, not ounces sold or the separate payable subtotal.

The 2019 acquisition date excludes the first part of the year from the company figures. The 2024 La Arena company figure excludes December following the sale. No proportional annualization is allowed.

The Shahuindo technical report describes recovery, doré assay and overseas refining. Testing doré in La Arena's laboratory does not establish pooled production, inventory transfers or misallocation. No annual assay/cutoff reconciliation was located. The company's 2023 sustainability data book is downloadable but its production sheet contains group totals and refers to the fourth-quarter report; it does not supply the missing mine bridge.

Quarterly 2023 comparison used MINEM's saved monthly plant rows, Q1 SEC table 26, Q2 and Q3 company reports PDF page 27, and Q4 SEC annual MD&A table 76. The company quarters sum to the reported annual 97.1 koz La Arena and 140.1 koz Shahuindo. All eight differences exceed one full 0.1 koz display increment. Ministry-minus-company differences in kg:

| Mine | Q1 | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---:|
| La Arena | +7.8576 | −15.2267 | −8.7044 | −23.3248 |
| Shahuindo | +27.5471 | +18.0272 | +23.8190 | +16.8974 |

Thus the observed gap is not restricted to the fourth quarter. This does not eliminate monthly lag, assay revisions, processing-stage differences or inventory accounting. No causal explanation is assigned. See [followup-gold-quarterly.json](followup-gold-quarterly.json), which retains monthly values, exact conversions, source fingerprints and locators. The sum of decimal-string monthly observations can differ in immaterial final decimal places from a displayed annual workbook cell; it does not affect these comparisons.

## 4. Free API and acquisition evidence

The Nexa Peru website's public file-manager JavaScript exposed two POST routes under company ID `fa653160-ea78-4cd6-897a-335d2c6c4b9f`. Live probes returned available year buckets 2014–2026 and 45 unique document IDs/URLs across 2019–2024. Actual downloads confirmed that at least one `es_ES` entry contains English text. Some annual reports sit under their publication-year bucket, while fourth-quarter results sit under the performance-year bucket. Publication-date metadata can also be a placeholder. These fields cannot certify language or period.

[FREE_API.md](FREE_API.md) documents exact requests. Seventeen arithmetic/gate/input controls passed, including four new guards against incompatible units, a dash becoming zero, duplicate check inflation and stale agreement outside the allowance. The packaged source fetcher also live-retrieved the SMV 2021 PDF with the exact saved fingerprint. The packaged registry client was live-tested on both routes; its two observed requests took about two seconds combined on this run. That is metadata acquisition latency, not full document extraction, comparison throughput or AI cost. Larger PDFs are expensive to read regardless of registry speed.

All 40 unique successful follow-up downloads were checked against saved SHA-256 bytes. Failed attempts and subsequent successes are retained separately in [followup-access-log.jsonl](followup-access-log.jsonl); the successful-source manifest does not hide them. Raw third-party PDFs are not committed. URLs, request bodies, fingerprints, short factual observations and six small registry snapshots plus the year list are retained. A successful HTTP result alone is not a claim-validity test.

## 5. Trade and prior coverage

The original successful company-level SUNAT declarations were reread to rule out a table-column transcription error. The ambiguous repeated assay/weight/value allocation remains. No foreign consignee/shipment quantity match was obtained. No country aggregate was used as company evidence. Trade remains parked under the gates in [TRADE_CHECK.md](TRADE_CHECK.md).

[MEDIA_NOVELTY.md](MEDIA_NOVELTY.md) records prior coverage and access limitations. Spanish Gestión already reported the two Pan American gold quantities; Nexa and Antamina publish their company quantities in Spanish. English industry reporting repeats MINEM quantities. No exact mismatch investigation was located, but novelty is not established by search absence.

## Implementation decision

Automate observed document registries, fingerprinting, unit arithmetic and clean SEC–SMV comparisons. Require a reviewed assertion contract covering mine population, period, ownership, product streams, stage, assay and cutoff. Retain original submitted returns and superseding versions before certifying a contradiction. Preserve uncertainty and move irresolvable cases to parked status. Additional tokens can help locate and interpret available evidence; they cannot certify missing assertions. This experiment establishes neither fraud-detection accuracy nor a general end-to-end cost benchmark.
