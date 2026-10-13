# Peru holdout: what the newsroom can conclude

13 October 2026 · Private research · Five fresh Cerro Lindo 2025 metal claims

**The English SEC filing and a company-hosted, signed preliminary Spanish annual report disclose the same five 2025 production quantities. Adding AI did not improve the prepared Python workflow on this batch. No natural mismatch or wrongdoing was established.**

This is a fresh bilingual feasibility test, **not completed SEC–SMV validation**. We retrieved the English 2025 SEC 20-F and the Spanish 2025 annual report from Nexa’s public registry. A public SMV search returned an internal-error page and no verified report link. Independently acquired SEC–SMV coverage is **0/5**; SEC–company-hosted coverage is **5/5**. A digital signature and an SMV reference inside a company document do not prove regulator hosting or final approval.

The five targets were frozen before acquiring the new documents. Both new document hashes are absent from the reviewed baseline, and we found no prior Cerro Lindo 2025 production assertion in its committed controls, extracts, notes or comparative-column records. Annual-2024 documents had already been inspected, so **2024 was excluded**, including its comparative-column exposure. This freshness finding is bounded to the available committed record; unseen prior conversations or uncommitted files cannot be certified absent.

## The available figures

Both documents give the following 100% mine-output figures for calendar 2025, rather than the parent’s 83.55% equity share. Fine metal/content in concentrates is the relevant measurement; concentrate mass, zinc-equivalent output, payable production and sales are not substituted.

| Metal | SEC English | Company Spanish | Unit | Difference |
|---|---:|---:|---|---:|
| Zinc | 87,141 | 87,141 | tonnes of fine/contained metal | 0 |
| Copper | 27,081 | 27,081 | tonnes of fine/contained metal | 0 |
| Lead | 10,252 | 10,252 | tonnes of fine/contained metal | 0 |
| Silver | 3,953,241 | 3,953,241 | ounces of contained metal | 0 |
| Gold | 4,067 | 4,067 | ounces of contained metal | 0 |

The Spanish report is explicitly **preliminary, subject to annual shareholder approval**, signed 26 February 2026. Its contents mention ongoing validation. The English source is the SEC-filed 2025 annual report. Agreement between related company disclosures is not independent confirmation of physical production or proof of an original ministry submission. [Source provenance and exact locators](provenance/source-pair.json), [identical bilingual packets](packets/), and [freshness audit](provenance/freshness-audit.json) are retained.

## What the three workflows did

All arms share acquisition, text preprocessing, reviewed table/column selection, extracted quantities and deterministic arithmetic. The Python workflow required assistant preparation and reviewed layout metadata; its sub-millisecond computation is **not end-to-end throughput**. No human reviewer supplied independent labels. The source-grounded reference was prepared by the same assistant before seeing paid-arm outputs, so the scores below are conditional on that review, not a certified accuracy benchmark.

| Frozen semantic-screen result | Python with prepared templates | Python arithmetic + OpenAI Decisions | Python arithmetic + Jev |
|---|---:|---:|---:|
| Correct evidenced natural comparisons / all five targets | 5/5 | 1/5 | 5/5 |
| Valid natural comparisons unnecessarily parked against reference | 0 | 4 | 0 |
| Natural unresolved cases | 0 | 4 | 0 |
| Incorrect natural comparability acceptance | 0 | 0 | 0 |
| Correct planted-case classifications / five fixtures | 5/5 | 3/5 | 4/5 |
| Planted invalid comparison accepted as agreement | 0 | 1 | 0 |
| Planted numerical difference without a numerical-difference alert | 0 | 1 | 1 |

OpenAI accepted silver and parked the other four metals because its ownership-period gate was unknown. Both models labelled the planted changed-quantity case invalid instead of comparable with a numerical difference. OpenAI’s semantic answer also accepted a planted partial-year/equity-output footnote. These are retained observations; we did not retune prompts or repeat paid calls.

**Implementation correction, separately labelled development:** the frozen harness shared extraction and arithmetic but allowed model semantic gates to replace the Python semantic gates. That falls short of preserving all guards in “same Python plus AI.” An offline protected-hybrid replay now gives existing Python conflicts priority, preventing the planted OpenAI period acceptance. This changes that fixture to invalid; both protected model workflows classify 4/5 planted cases correctly. Natural results remain 1/5 OpenAI and 5/5 Jev. The correction was made after seeing answers, so it is **not a new clean holdout score**. Frozen outputs and scores remain available beside the [development replay](results/protected-hybrid-development.json).

## Cost and elapsed work

| Provider | Exact requested/returned model | Calls / retries | Input / output tokens | Usage-derived list cost | Conservative budget remaining |
|---|---|---:|---:|---:|---:|
| OpenAI Decisions | gpt-6-luna | 10 / 0 | 22,130 / 0 | US$0.00221300 | US$4.997783 |
| Jev | jev-1.13.0 | 10 / 0 | 25,775 / 1,896 | US$0.00108255 | US$4.998912 |

Combined usage-derived cost: **US$0.00329555**. Conservative per-call rounding accounts for US$0.003305, leaving **US$9.996695** of the new US$10 authorization. Each provider had its own US$5 ceiling. No other paid service, retry, new credential or access change was used. **Actual invoice charges are unavailable**; these figures use provider-reported usage and verified public rates, not an invoice or account-balance claim. All raw responses and budget attempts are preserved in [raw/](raw/) and [results/](results/).

The fresh five-target batch alone used US$0.00114990 OpenAI and US$0.00056217 Jev; the rest covered separately labelled planted cases. Free acquisition requests totalled about **19.09 seconds**, including provider-documentation retrieval and an unsuccessful SMV query; downloading the two production documents took **6.59 seconds**. Source inspection, preparation, searches and pre-output review were bounded by **08:49:34–08:53:21 UTC**, about 3m47s elapsed, rather than an active-human-labor measurement. Preparation script execution took 0.92s. Provider calls totalled 6.47s OpenAI and 3.11s Jev. These are component timings, not additive end-to-end labor costs. Human/editor review time, ChatGPT/subscription cost and prior fixed setup cost are **unknown**.

## Decision and limits

Keep the existing Python arithmetic, source fingerprints, period/unit guards and explicit abstention rules. This batch supplies **no demonstrated incremental benefit from selective AI** once evidence is prepared. Jev matched the baseline natural coverage, while OpenAI increased the review queue. The evidence is too small and dependent to identify a general vendor winner: five metal claims share one mine/year and one pair of related company documents. Real-world mismatch recall remains **unmeasured** because no confirmed natural mismatches were available. Planted cases are engineering checks, never discoveries or prevalence estimates.

The original 100-record, 11-operator 2019–2023 batch and 43 prior controls covering 33 distinct assertions are unchanged. The four ministry gaps remain parked. No ATI requests, third-party outreach, email, merge or deployment occurred. The parent thread owns the email summary.

Reproduction and complete limitations are in the [technical annex](TECHNICAL_ANNEX.md). The [machine-readable summary](results/summary.json) retains all five natural targets, five planted cases, provider usage and blockers.
