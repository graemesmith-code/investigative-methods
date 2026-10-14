# Annex: rule-constrained source comparisons

**Proposed schema, 14 October 2026. No catalog parsing or new experiment has been run.** Read the [plain-English options and stopping rule](../docs/rule-based-source-comparisons.md) first. This annex describes how to preserve a conditional question without promoting assumptions to facts.

## A comparison card

| Field | Required content |
|---|---|
| `comparison_id`, `pair_ids` | Local card identifier and existing Rabbit SYS/AP or reviewed-recipe identifiers; do not renumber original records |
| `question` | One testable conditional proposition and the public-interest reason for checking it |
| `constraint_kind` | `legal`, `accounting`, `physical`, `contractual`, or `expectation`; do not merge these |
| `data1`, `data2` | Source owner, original record/identifier, URL, retrieval date, preserved evidence/hash and limitations for each side |
| `entity_bridge` | Identifier, address/ownership/location bridge as relevant, historical identity dates and confidence; record competing candidates |
| `activity_scope` | Actor, conduct, location/formation, covered population and excluded activities; state any proxy |
| `denominator` | For any rate/disparity: eligible or exposed population, numerator definition, period, exclusions and missing coverage; block the comparison if indefensible |
| `units_and_basis` | Units, dimensions, currency and price basis, gross/net, cash/accrual, magnitude type and permitted conversions as applicable |
| `times` | Event/action, signing/effective, reporting/correction and observation-window dates, time zone, granularity and uncertainty; keep these distinct |
| `jurisdiction` | Territory, actor reach, authority and unresolved jurisdiction questions |
| `rule_source` | Exact official document, clause/page, short operative excerpt, URL, retrieval date and evidence hash; or explicit absence |
| `rule_version` | Effective-from/to dates, amendments, superseded text and unresolved gaps; publication date alone is insufficient |
| `rule_verification` | Whether the text was verified against a primary source; separate this from whether it applies to this case |
| `conditions_and_exceptions` | Trigger, covered actor/activity, conditional duties, permissions, exemptions, authorizations and exclusions; preserve unknowns |
| `applicability` | `verified`, `unresolved` or `outside_scope`, with evidence for the status; a verified rule is not automatically an applicable rule |
| `observations` | Facts actually evidenced on each side, lineage/independence and counterevidence; do not substitute modeled conduct for observed conduct |
| `missing_evidence` | The precise absent record or interpretation required to test the question, and its known access status |
| `uncertainty` | Measurement, identity, historical version, scope, timing and missingness; distinguish “unknown” from “no” |
| `ordinary_explanations` | Concrete alternatives and the evidence that could discriminate among them |
| `assessment` | `candidate_rule`, `unresolved_applicability`, `missing_decisive_evidence`, `question_ready_for_check`, `ordinary_explanation_supported`, `outside_scope` or `parked`; none is a verdict |
| `priority_axes` | Importance if substantiated, access, comparability, verification effort and novelty; separate scales, reasons and “not assessed” values |
| `next_check`, `stop`, `reopen` | One bounded feasible check, budget/stop condition and the new evidence that would change the decision |

A generated rule suggestion remains `candidate_rule` until an exact official text is verified. Even after text verification, incomplete conditions or exceptions require `unresolved_applicability`. A missing operational or payment record requires `missing_decisive_evidence`. These gates prohibit a model from filling gaps with invented obligations or implied conduct. They are a proposed review procedure, not tested software. Also block candidates needing substantial harmonization in the initial pilot. Never infer payment from an obligation/termination or pumping from a disclosure window or monthly volume.

## Example 1: NAI, retained as a parked reporting question

- **DATA1:** historical OFAC designation, 11 December 2023, with identity established through name, address and identifiers.
- **RULE:** the dated program restrictions and official-business authorization, plus case-specific applicability and any other governing procurement restrictions. The DLA notice's assertion of no applicable authorization is preserved alongside the general provision. Its underlying basis remains unresolved.
- **DATA2:** eight reported positive order actions on 13–14 December, subsequent reductions and complete termination effective 11 March 2025. These are procurement records, not disbursement or delivery evidence.
- **Time distinction:** seven base rows were first reported on their action dates; one was first reported in August 2025. Same-day modification action dates differ from initial-report dates. Signed child-order documents remain missing.
- **Missing decisive evidence:** actual payment/acceptance records, original child orders/modifications, the start of restrictions and contemporaneous applicability determinations.
- **Assessment:** `parked`, editorial priority low at present; no violation or actual post-designation supplier payment established. The administrative-delay explanation is an editorial hypothesis, not a verified cause or finding of compliance.

[Original NAI evidence and dated parked decision](../research/2026-10-14/nai-contract-history/README.md). The 2023 rule version matters: §583.502 was reserved then; its 2024 paragraph (e) cannot be retrospectively applied to December 2023 orders.

## Example 2: Alberta, with the operational side missing

- **DATA1:** seismic observations, independently attributed catalogue records, typed magnitude, event time, location and catalogue revision. Candidate cross-catalogue associations remain provisional.
- **RULE:** the correct dated order and mapped location/formation; magnitude basis; notification/shutdown duties; and permission conditions **if a qualifying shutdown and restart occurred**. A screen radius does not replace the exact clause's reach.
- **DATA2 needed:** historical operator and actual stimulated interval, stage-level pumping, stop/restart timestamps and contemporaneous monitoring/detection records. These remain missing in the existing study.
- **Observed proxy:** reporting-date windows and current licence/geological labels. They cannot establish continuous pumping, triggered notification, post-event pumping or an actual restart.
- **Assessment:** `missing_decisive_evidence`. Absence of a publicly retrieved restart approval is not proof that approval was absent, particularly when restart itself has not been established.

[Existing Alberta findings](../research/2026-10-06/alberta-seismic-injection/README.md) and [operative-rule review](../research/2026-10-06/alberta-seismic-injection/RULES.md). This note does not expand that investigation.

## Attributable commitments: a separate cheap route

Capture the named speaker/organization, original dated statement and exact attributable promise, beneficiary/location, deadline, measurement and qualifications. Compare it with independent records of the promised outcome. Record whether it is an operative contractual commitment, another specific public promise or a vague aspiration; do not promote a political promise to a legal duty. An extension, amended scope or unavailable outcome record can defeat the comparison. This is a proposed schema example, not a newly researched case.

## Example 3: a physical balance, not a legal obligation

For a specified tank, facility or watershed over a specified interval:

`closing stock − opening stock = measured inflows − measured outflows + documented adjustments + residual`

Define the system boundary, all material flows, stock measurements, conversions, timing and losses before interpreting the residual. Include measurement uncertainty and unobserved-flow bounds. An open system with unmeasured inflows or outflows does not support a conservation-based accusation. A large residual only identifies a measurement, scope or activity question unless independently corroborated. Accounting balances also need consolidation boundaries, accrual/cash basis, adjustments and restatements. Neither track automatically supplies a legal duty.

## Pilot output and honest evaluation

The proposed 12-description / up-to-30-candidate / five-source-check pilot should produce a small table, not a full-catalog score:

| Existing pair | Verified constraint and scope? | Decisive observations available? | Importance if substantiated | Access | Comparability | Verification effort | Novelty | Decision / next fact |
|---|---|---|---|---|---|---|---|---|
| Example placeholder | Not yet assessed | Not yet assessed | Not yet assessed | Not yet assessed | Not yet assessed | Not yet assessed | Not yet assessed | No pilot result |

Use “not assessed” rather than inventing scores. Before generation, fix the 12-description selection rule, bank provenance and time/document limits. Keep all generated candidates and all five verification outcomes, including rejections and blocked cases. Record importance separately from evidence readiness and novelty. Two improved cards plus one feasible cheap decisive-check nomination would justify considering another bounded batch; they would not establish recall, precision, legal accuracy, model reliability or investigative novelty. No nominated check is executed by this proposal.

## What was read for these options

Only the existing catalog guide/provenance, existing source-pair review documentation and a small recipe excerpt, the NAI report, and existing Alberta findings/rule summaries were read. No full Rabbit volume or pair universe was parsed. No new enforcement cases, legal rules or operations records were researched; no model or paid calls, experiments or outreach were initiated. The catalog originals and investigation evidence remain preserved.

[Options and recommended pilot](../docs/rule-based-source-comparisons.md) · [Main guide](../docs/method.md)
