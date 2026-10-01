# Correction: department and request number identify an ATI record

Corrected 1 October 2026, after delivery. No new API calls or spending.

`make_plans.py` originally selected the first row matching a request number, without its department. The frozen corpus contains 77 request numbers shared by GAC and DND. Among the 14 selected clusters/audits/control, two numbers collide: Nanisivik A-2025-02587 and medical fairness A-2025-02382. Nanisivik was correctly attached to DND. The medical-fairness audit was the only misattachment. All ten shortlist clusters, the other two audits and the C22 control were checked against the corpus; their identities are unchanged.

| Medical-fairness audit | Department | Pages | Disposition | Score |
|---|---|---:|---|---:|
| Original mistaken attachment: Mexico evacuation | GAC (`dfatd-maecd`) | 0 | NE | 1.982 |
| Correct intended record: DMEDPOL fairness/accommodation | DND (`dnd-mdn`) | 303 | DP | 1.524 |

The actual Exa query was `Canadian Armed Forces medical policy procedural fairness disability accommodation DMEDPOL`. It targeted the intended topic and returned fairness guidance and grievance decisions. It did **not** search the Mexico topic. However, all ten subsequent Jev coverage screens combined the medical-fairness question with the unrelated GAC source summary. Those screens and the previous low-priority audit conclusion are invalid; a corrected screening rerun is pending. Correcting the metadata does not validate the original search's coverage or prove the 303-page packet contains no new information. The packet remains unread. Two other audits retain valid identity associations; three audit searches were attempted.

The original coverage plans are preserved in [coverage-plans-original.json](coverage-plans-original.json). Original result envelopes, model screens, raw corpus, full ranking, API-stage executed source and per-attempt ledger/accounting remain unchanged. Their medical-fairness entries must be read with this correction. Current plans, editorial decisions and shortlist CSV contain corrected metadata and an explicit invalid-screening status. [Identity review](identity-review.json) maps every lead to its composite identity, records all 17 saved search associations and counts the 140 coverage and 28 branch screens. The three expansions and five branches concern unaffected leads.

Current code resolves `(owner_org, request_number)`, rejects missing/duplicate identities and mismatched source metadata before API transport, and carries composite identities in future screen output. It deliberately refuses the old malformed result plans; historical results must not be silently relabeled as corrected rerun inputs. Regression tests exercise department collisions, source mismatch and missing/duplicate identity. No paid API execution was performed for this correction.
