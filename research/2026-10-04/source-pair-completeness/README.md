# Final bounded source-pair completeness checkpoint

The catalog pass assessed **344 sources** and **65 mechanisms**. This follow-up checks an important gap: reviewing sources and mechanisms does not systematically review all compatible pairs.

Start with the **[nine recommended next tests](recommended-next-tests.csv)**. Each has a pair-specific consequence rationale, linking/access burden, required evidence and cheapest next check. The larger [inventory](candidate-inventory.csv) retains mechanism-level triage; its scores must not be described as individually assessed newsworthiness.

The [32 detailed cards](reviewed-recipes.csv) contain the earlier 27, corrected where needed, plus five additional formulations:

- Later papers affirmatively relying on a retracted result, after checking exact citation context and chronology.
- A serious ship defect recurring after documented rectification, with original reports and reuse permission.
- Selective network interference distinguished from a general outage using compatible observations.
- Actual fishing inside an area with a verified activity-specific restriction, rather than assuming all protected areas prohibit fishing.
- A precise issuer compliance claim contradicted by a final finding for the same facility, operator and period.

These are **conditional designs, not findings**. No positive case, full investigative predicate or bulk investigation was executed.

## Coverage and counts

| Layer | Coverage | What it does not establish |
|---|---:|---|
| Individual catalog assessment | 344 sources | Current availability or every pairing |
| Mechanism-family review | 65 | Individual review of every expansion |
| Named-identifier audit | 70 unordered pairs | Actual identity/record compatibility |
| Outside original rules both ways | 45 of those 70 | 45 new hypotheses |
| Selected event/role clusters | 12 | Exhaustive semantic combinations |
| Enumerated cluster alternatives | 61 directed pairs | Independent review beyond the 12 representatives |
| Detailed cards | 32 | 32 executed or necessarily independent mechanisms |
| Active inventory | 1,715 rows | Independently validated hypotheses |
| Geography quarantines | 15 rows | Active candidate status |
| Full audit inventory | 1,730 rows | Additional active candidates |
| Earlier rejects / duplicates | 797 / 8 | Useful hypotheses excluded forever |
| Full investigations confirmed/executed | 0 / 0 | — |

The 70-pair and 61-pair layers overlap and use different directionality; do not sum them. The 117,992 ordered-pair universe remains policy enumeration. Broader pair discovery is open. Five thousand defensible tests were not established and were not manufactured by rewording or parameter expansion.

## Independent-review repairs

W09 and geoBoundaries election reasoning now point to **SYS-0201 SAGE**, not SYS-0200 Light Every Night. E01 (0030→0058), C05 (0282→0209) and F04 (0269→0009) are explicitly registered as [supplemental proposed pairs](supplemental-pair-register.csv) outside the original mechanism memberships; they are not silently counted as emitted representatives.

N05 now specifies a US State Department request with an explicit case/document crosswalk and an actual reading-room version comparison. Without that counterpart, it is labeled a single-source response-document check. Reading-room absence does not prove nonresponse.

Active, quarantined and raw counts now propagate consistently through the pair universe, source coverage, progress, counts and active mechanism totals. Twenty-six tests pass, including semantic source-role and membership checks, saved linking values, IMO type separation and trade-flow reversal.

## Reproduction and costs

Read the concise [methodology and cost assessment](METHODOLOGY-AND-COST.md). It explains code's actual bookkeeping savings, the remaining expensive reasoning, and a bounded cheap-model evaluation that has **not** been run. Runtime evidence records local code only; weekly ChatGPT usage and token telemetry remain unavailable. Paid external API calls: zero.

From the repository root:

```sh
python research/2026-10-04/source-pair-completeness/code/reproduce.py
```

This uses saved source text and earlier evidence. No network, model API or investigative record requests are made. Earlier frozen checkpoints remain preserved. Review `named-identifier-assessment.csv`, `event-role-clusters.csv`, and `event-role-pairs.csv` for admitted, deferred and rejected paths and their limits.
