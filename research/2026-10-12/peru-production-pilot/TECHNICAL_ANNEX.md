# Technical annex: fixed Peru production experiment

## Design and result

The batch was frozen at 13:56 UTC on 12 October 2026 and committed before the pilot comparisons. Its SHA-256 is `cbcf4b2093eb408eefa7da2984fe723100a8226bfa5fa1b244989f076b3e7a7f`. It contains 100 company–metal–calendar-year records: 20 series across 2019–2023, 11 operator groups, including 35 gold records. This is a purposive feasibility sample of internationally reporting companies, not a random sample of Peru's mining industry.

The protocol labels 2023 as 20 development records and 2019–2022 as 80 transfer records. These are chronological reuse labels, **not a blinded statistical holdout**: historical comparatives were visible during source work and definitions evolved during review. The earlier Southern molybdenum comparison was a known positive control. We retained every selected record.

| Measurement | Observed result |
|---|---:|
| Ministry production observations | 100/100 |
| Western claim objects located | 95/100 |
| Complete numerical pairs | 94/100 |
| Raw numerical differences beyond reporting precision | 62/94 |
| Raw numerical agreements within reporting precision | 32/94 |
| Eligible for a preliminary contained-metal screen | 45/100 |
| Within precision in that screen | 19/45 |
| Unresolved differences in that screen | 26/45 |
| Other comparability blocks | 49/100 |
| Missing Western observations | 5/100 |
| Missing component within a Western claim | 1/100 |
| Proven incompatible company representations | 0 |

The 45 are a **generous preliminary coverage measure**, not 45 certified apples-to-apples pairs. In particular, the exact coverage of metals across different concentrate products remains unresolved for Antamina and Nexa. The frozen target of at least 80 defensible reusable comparisons was not met. Gold outcomes are four within precision, one unresolved initial-screen difference, 29 comparability blocks and one missing numeric component.

## Evidence and attribution

Peru's mining ministry publishes free annual workbooks and downloadable monthly-production archives. The production index says the statistics are based on ESTAMIN monthly and DAC annual declarations. The archive supplies legal operator, plant, processing stage, process and monthly metal quantities. We extracted 307 selected operator/metal/plant rows, including some ancillary metals outside the fixed comparison batch. All 100 frozen records have relevant detailed rows. The 95 observations already present in the annual summary reproduce from the detailed records to within 0.01 of the native reporting unit. Detailed records supplied the five Yanacocha silver observations missing from our annual-summary selection.

We did **not** obtain the original company-submitted returns and their complete amendments for these observations. A ministry compilation provides strong investigative attribution, but an unexplained compilation difference alone does not prove what the company submitted, what version superseded it, or that the ministry transcribed it correctly. No automatic false-statement or legal conclusion follows.

Western provenance varies: SEC-hosted filings/exhibits, company annual reports and investor-results releases. The Hudbay results releases and company-hosted Teck/Hochschild reports meet the user's expanded investor-disclosure scope; their use here does not establish that those exact documents were filed with a government. Source class must remain visible in implementation.

## Comparison rules

Use the same legal operator and mine population, 100% production rather than attributable ownership, calendar period, actual metal, product stage, unit and evidence version. Exclude sales, payable metal sold, gold-equivalent measures and group totals when the host row is mine-specific. Do not infer comparability from a match. Do not interpret a dash as zero: the 2022 Julcani gold component blocks the Buenaventura 2022 arithmetic.

Base units are tonnes for copper, molybdenum and zinc; grams for gold; kilograms for silver. Exact conversions are 0.45359237 tonnes per thousand pounds and 31.1034768 grams per troy ounce. The source's precious-metal ounce convention was reviewed; a future extractor must distinguish troy from ambiguous ounces explicitly. One full last-displayed unit per summed component is the conservative reporting-precision allowance. This is more permissive than nearest-unit half-step rounding. It is **not** an assay uncertainty model or a statistical confidence interval. Ministry figures have much finer displayed precision; binary-float residues do not explain the substantive gaps.

A raw numerical flag can exist on a blocked record, solely as diagnostic arithmetic. The runner never promotes a flag to a proven contradiction. The proof fields for assertion identity, original host submission and reconciled correction history remain false in this experiment.

Preliminary eligibility was applied at series level to Southern, Hudbay, Antamina and Nexa (45 records), using explicit mine/contained-metal descriptions. Newmont, Pan American and Ares gold were treated consistently as blocked where leached/poured/refined/assay cutoff was unbridged, including numerical agreements. Freeport's recoverable-metal series is blocked for both copper and molybdenum. These semantic judgements were made during the pilot, not independently validated in advance; future runs must freeze them before evaluating new years.

## Verification and limitations

All 62 raw alerts have an explicit disposition in the review ledger; all remaining records are also retained there. Ten of the 32 apparent agreements were selected deterministically with seed 20261012 and re-read against originals. No transcription error was found in that ten-record sample, but five remain semantically blocked. This is a same-assistant second pass, not independent review or a measured extraction error rate.

Thirteen code controls pass, covering exact conversions, a deliberately injected discrepancy, incomplete observations, mismatched metadata, ambiguous units, precision boundaries, and preservation of the frozen denominator. Synthetic controls validate arithmetic/gate behavior; they do not establish real-world contradiction-detection sensitivity. The runner took about 0.004 seconds for cached reviewed observations; that is **not** end-to-end acquisition, extraction or review throughput.

HTML tables were parsed with code; PDF tables and difficult labels received assisted manual review/transcription. No unattended AI translation/extraction pipeline, token-cost benchmark, per-case time study, independent gold standard, precision/recall estimate or population prevalence estimate was produced. Current documents were retrieved on 12 October 2026, often presenting historical comparatives or revised ministry compilations. We cannot reconstruct the exact public evidence available at each original filing date.

## Scaling decision

Acquisition and deterministic arithmetic scale. Semantic identity and claim provenance are the bottlenecks. This pilot supports a limited public-record investigation of four recurring leads (La Arena, Shahuindo, Antamina and Cerro Lindo), plus Hudbay/Southern as useful reconciliation controls. It does not support deploying an automatic accusation detector.

Next, freeze an operator-specific mapping only after a public technical report, production-return exhibit or explicit reconciliation establishes its product scope and stage. Apply that mapping unchanged to new years, record wall time and manual touches, and review every alert plus a random sample of agreements. Park a series if those public evidence gates cannot be closed. Keep government-to-government contradiction candidates separate from investor-to-government inconsistencies.
