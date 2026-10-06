# Alberta earthquake / hydraulic-fracturing experiment — final bounded results

**Two candidate earthquake groups occur near three wells with overlapping reporting date windows. No packet establishes noncompliance, pumping after a threshold event, missing restart consent, or causation.** This is a bounded shutdown-threshold proximity screen, not a complete compliance survey or a disposal-injection test. All nine catalogue-event-well representations remain **indeterminate**.

The 2020–2025 Edmonton-local study period and the Fox Creek, Brazeau and Red Deer order areas were selected from rule applicability and public dataset coverage before inspecting company names or earthquake results. The actual public records—not a famous-company or scandal seed—surfaced this cluster. Earlier experiments remain unchanged.

## What the records show

| Candidate group | NRCan record | Candidate AGS counterpart | Why it needs caution |
|---|---|---|---|
| February 22, 2025, 07:05:18 MST | `ca2025dscb`, **ML 3.1** | `9289785`, one second earlier, **MLy 2.09**, industry M 2.49; origin 1.373 km away | Estimates straddle the SO7 ML 3.0 shutdown threshold. These are separately labelled magnitude types; no automatic equivalence or contemporaneous operator knowledge is assumed. |
| February 24, 2025, 23:32:36 MST (February 25 UTC) | `ca2025dwzq`, **ML 3.76** | `9289976`, one second earlier, **MLy 3.12**, industry M 3.25; origin 0.169 km away | Current local-magnitude estimates exceed 3, but actual pumping, detection timing, formation and response remain unknown. |

Cross-catalogue associations are candidate matches within ten seconds and ten kilometres, not proven event identities. The nine representations comprise six NRCan event-well packets and three AGS MLy sensitivity packets; they are not nine discoveries. Twenty-three reporting-window pairs reduce to those nine representations.

The wells are licences **0515889**, **0516327**, and **0516328**, respectively UWIs `00/15-28-037-28W4/0`, `00/07-33-037-28W4/0`, and `00/02-33-037-28W4/0`. Both recorded surface and bottomhole points lie in SO7 Appendix B outside Appendix A. Screen distances are approximately 1.04–1.54 km to bottomholes and 2.73–3.33 km to surface points. Current records label the licensee Parallax Energy Operating Inc. and the projected/terminating formation DUVERNAY FM. **Those are current labels and geological proxies, not verified historical operator or stimulated-stage identities.**

Summary windows include February 15–28 and narrower ranges. Their exact derivation was not independently established. They neither show continuous pumping nor prove an injection after either earthquake. Manual 027 describes fracture treatment dates and separate general operation dates; this does not establish the lineage of the public summary's Start_Date/End_Date columns. The 57 relevant ingredient rows and their original physical line numbers are saved in [candidate-ingredient-rows.json](results/candidate-ingredient-rows.json).

## Coverage and limits

The full AER disclosure download contains **595,923 ingredient rows** (219.8 MB uncompressed), deduplicated into 42,025 reporting groups, of which 16,391 overlap the study period. Surface-or-bottomhole area screening retains **2,692 groups / 1,328 UWIs**: Fox Creek 2,062, Brazeau 14, Red Deer 616. These are reporting groups, not necessarily distinct jobs or an exposure denominator. Repeated ingredients, stage counts and water values are preserved rather than summed.

The corrected local-period AGS catalogue contains **9,668 events; 9,647 (99.78%) lack ML**. MLy sensitivity is separate. The second, fixed-box NRCan catalogue contains **651 events: 513 ML, 135 MLy, 3 Mw**. Mw never substitutes for ML. Mutable catalogue snapshots, monitoring completeness, absent numerical location uncertainties and retrospective revisions preclude claims that other operations had no relevant earthquakes.

Current surface and licence joins match every period group. Within scoped groups, five projected formations and two terminating formations are missing; even present values do not establish stimulated intervals. Historical operator identity remains unresolved. The February monthly volumetric lookup matches zero target well IDs, so facility-operator history checks examine **zero linked facilities**. That is not corroboration of an operator or proof of no injection.

The screen evaluates possible proximity/date overlap at the inclusive red magnitudes: Fox Creek 4.0 ML, Brazeau 2.5 ML, Red Deer 3.0 ML. It does **not** evaluate yellow notification/mitigation duties, prohibited-zone fracturing, all plan-specific disposal requirements, or every possible SO6/SO7 red-clause reach. The latter clauses do not expressly repeat the five-kilometre condition; the study's 5 km screen plus 0.5 km sensitivity must not be represented as their complete legal scope. Full rule dates, formations, maps and restarts are in [RULES.md](RULES.md).

## What would make this testable

1. Original stage-level pump, stop and restart timestamps, actual stimulated intervals and trajectories for the three wells.
2. Contemporaneous earthquake monitoring/detection records, magnitude basis and version history, especially the February 22 catalogue disagreement.
3. Dated operator/licence-transfer records and, **if restart occurred after a qualifying shutdown**, applicable written AER consent and accepted plan records.
4. Official derivation of summary date/stage columns to interpret the reporting windows correctly.

Ordinary explanations remain viable: no pumping at event time; prompt cessation; later activity under written consent; or separate stages and pauses within the date window. Thirty-three near-but-nonoverlapping records are retained as temporal controls. A noise complaint's `SourceInCompliance=No` is unrelated to the seismic EDGE identifier and is explicitly excluded from seismic conclusions.

Actual free official sources were retrieved and inspected: disclosure and water-source tables, AGS and NRCan catalogues, complete ST37 infrastructure, Petrinex licences, January/February monthly volumes, facility operator history, current disposal inventory, incident/complaint tables and public application searches. Public application searches returned zero applications for the three licences; **not finding public consent does not establish its absence**. The Tableau browser route stopped at a certificate warning; no TLS bypass occurred. Well Infrastructure was refreshing/404, with alternative infrastructure acquired. Fine records offered through paid catalogues were not purchased. See [technical annex](TECHNICAL-ANNEX.md) for actual schemas, access failures and reproducibility.

## Jev result and cost

**Jev was not reliable enough to decide operational facts.** The first pilot stopped on its second synthetic control: despite no evidenced restart, it scored unresolved restart permission 0.82, contrary to the explicit instruction. Version 2 changed the task to literal evidence extraction; it did not demonstrate a generalized repair of conditional reasoning.

On 12 labelled synthetic fixtures, 34/36 atomic answers matched labels at an illustrative 0.5 cutoff. Under the preset 0.2–0.8 abstention band, **26/36 were decided correctly and 10 abstained; only 5/12 fixtures were fully decided**. Crucially, **7/8 positive pumping atoms and 3/4 positive restart atoms abstained**. Only one fixture supplied positive consent evidence. This small designed set is not an accuracy estimate, and model-reported probabilities are not calibrated task probabilities or probabilities of wrongdoing. All prompts, raw responses, failed results and corrected offline gate interpretations are preserved.

One real, fixed-indeterminate cluster was then submitted solely to rank existing evidence gaps. Scores on a 0–3 importance scale were: time-resolved operations 2.94; window schema 2.33; contemporaneous magnitude 1.78; historical identity 1.67. These are editorial suggestions. **The first acquisition priority did not change; lower scores do not remove mandatory gaps or discard packets.** This one case does not show incremental ranking value. No model factual or compliance decision was requested or accepted.

**15 successful calls; 11,858 observed input tokens; conservative token-based estimate US$0.000507**, including per-call upward rounding (unrounded list-price calculation US$0.000498036). This is not an invoice. No retries, pending/failed reservations or other paid service calls. All calls use one cumulative ledger, US$0.003 reservations, a US$9 internal stop beneath the newly authorized US$10 cap. Live replay of the archived first pilot and completed gap call is disabled. Details: [Jev audit](jev/METHOD-REPAIR.md), [machine-readable cost/evaluation](jev/final-audit.json).

## Deliverables and review corrections

[Protocol](PROTOCOL.md), [rules](RULES.md), [technical annex / reproduction](TECHNICAL-ANNEX.md), [evidence packets](results/evidence-packets.json), [denominators](results/extended-denominators.json), [boundary figure](results/rule-boundary-review.png), exact source URLs/hashes in `sources/manifest.jsonl`, and complete lossless archive pieces in `sources/multipart/` are in this private repository.

Independent review corrected the UTC/local-year mismatch (old AGS 9,669 → corrected 9,668), removed a geographic prefilter, added raw-row references and join missingness, dated rule references, and narrowed Jev claims. The two candidate event groups are unchanged. Earlier source snapshots and checkpoint commits are preserved. This completed experiment identifies a specific unresolved records question; it establishes **no violation and no basis for an accusation**.
