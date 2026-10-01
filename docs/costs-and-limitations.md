# What these experiments cost—and what is still unknown

The best recorded spending is from the Canadian ATI run. Most earlier experiments lack a complete usage ledger. **Unknown is not zero**, and a small API charge is not the full cost of doing journalism.

| Experiment | Recorded paid use | What is not measured |
|---|---|---|
| Sanctions-name comparison | No paid data or model calls | Computing, downloads, storage and review time |
| Public-source trial | Public/no-key routes and one demonstration-key route; no complete charge ledger | Actual request charges, engineering and review time |
| Headline prototype | Unknown | Build, hosting, search/model usage and review |
| Sixteen-outlet news check | 27 requests reported; charges and quota unknown | Saved response logs, bill and review time |
| Paragraph prototype | Unknown | Build, hosting, model usage and review |
| September contract Jev/Exa top-ten trial | Actual per-run charges unknown | Calls/tokens, retries, invoice attribution and review time |
| October Canadian ATI run: Jev | **USD0.061954 estimated** from observed tokens across **1,402 calls** | Audited invoice, taxes/fees, cash-versus-credit settlement and labour |
| October Canadian ATI run: Exa | **USD0.119 API-reported** across **17 searches** | Same invoice and labour limitations |
| Enron and bank-survey exercises | No paid data or model API calls | Platform inference, source-reading and preparation time |
| Preliminary ATI source check | No Jev/Exa paid calls; eighteen free-web queries recorded | Platform and human time |
| Requested OpenAI comparison | **USD0; no API calls** | Blocked on a missing key; no comparison result |

ATI combined usage accounting is **USD0.180954**. It is not a verified cash debit or tax-inclusive bill. It includes ranking, coverage assessments and follow-up passage assessments, including the ten medical-fairness assessments later invalidated. No additional calls were made to correct metadata or restructure this notebook. The [exact ATI cost record](../research/2026-10-01/ati-live/cost-summary.json) and [sanitized accounting](../research/2026-10-01/ati-live/ledger-accounting.json) preserve the details.

## What to record next time

Keep paid charges and free credits separate. Record the provider, requests, retries, tokens or operations, currency, period covered by the bill and minutes spent reviewing. If a shared bill cannot be allocated to one trial, say so. Historical prices in an annex are planning assumptions at the stated date, not current quotes or evidence of actual payment.

Once you have defined a useful reporting question, count those accepted after checking and show both cash spending and review time. If none survive, report that outcome and the spend rather than inventing a cost per useful lead.

## Limits that change how to read a result

- A name match needs identity, date and context checks.
- An alarming request can have no records behind it; a partly disclosed file can still be uninformative.
- A working connection does not establish completeness or ongoing availability.
- A search can miss known reporting. Silence does not establish novelty.
- A top-ten list says little about good material rejected earlier.
- Historical cases chosen after a scandal cannot establish foresight. Today's models may already know the ending.
- Model scores and confident wording are not verified editorial judgments.

[Home](../README.md) · [Experiments](../experiments/README.md) · [Run record](../templates/run.md)
