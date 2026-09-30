# Costs and limitations

We are trying to invent cheap reporting methods, but the supplied evidence does not yet establish an actual cost per useful lead. Unknown spending is recorded as unknown, never as zero.

| Run | Observed paid use or reported volume | Actual total cost | Main missing measure |
|---|---|---|---|
| OFAC baseline | No paid data or model calls | Unknown | Computing, download, storage and review time |
| Public-source pilot | No-key routes and public demo-key route; blocked sources documented | Unknown | Request ledger, engineering and review time |
| Headline filter | Published prototype; failed known control reported | Unknown | Hosting, search/model usage and review time |
| The News API check | 27 requests, 16 outlets, no errors user-reported | Unknown | Saved responses, quota, bill and review time |
| Paragraph prototype | Published historically | Unknown | Build/hosting cost and per-run usage |
| Jev + Exa | 10,000 paragraphs user-reported; ten leads with ten-result counts inspected | Unknown | Jev tokens/calls, Exa billed operations, retries and reviewer minutes |

Historical vendor price estimates are planning assumptions. They may omit prompt overhead, retries, text retrieval, hosting and human review. They are not recorded costs of these runs and are not used here to calculate a bill.

## What to record next time

Keep provider, model/version, requests, retries, billed tokens or operations, invoice-period attribution, currency, cash charged, credit consumed, storage and reviewer minutes. Record free credits separately from cash. If an invoice covers multiple runs and cannot be allocated, keep that uncertainty explicit.

Once a reviewer has defined and counted worthwhile leads, calculate **cash cost per worthwhile lead** and **review minutes per worthwhile lead**. Also report missed important controls. If there are no useful leads, report the spend and zero useful leads rather than dividing by zero.

## Limits that affect conclusions

- A current list is not a historical status check; name matches do not prove identity or wrongdoing.
- Contract obligation, ceiling, value and payment are different measures.
- Successful API access does not establish complete records, lawful republication or current service availability.
- Search can miss known coverage; silence is not a novelty verdict.
- A top-ten list says little about important records discarded earlier.
- Model scores need calibration against human-reviewed examples; small score differences do not establish editorial distinctions.
- Original paragraphs, queries, articles, prompts and decisions are required to reproduce the latest ranking and search run.

No live search-provider tests, paid calls or outreach were performed while assembling this notebook. Prototype publication status is historical; present functionality remains untested.

[Home](../README.md) · [Run template](../templates/run.md)
