# Sanctions versus USAspending: bounded pilot

Completed 7 October 2026. **One credible identity match, one unresolved post-designation purchasing question, no established prohibited payment or sanctions violation.** The five-name expansion produced no additional leads within its stated search scope.

**NAI Logistics B.V. remains the sole credible identity match.** Its FY2025 hit is a vehicle termination for cause on 11 March 2025 with zero additional obligations. Independently retrieved child histories reveal eight delivery orders dated 13–14 December 2023, two to three days after designation: $36,309.46 positive obligations, −$15,662.32 adjustments, **$20,647.14 net**. These are possible new-business records requiring the original instruments, not proof of payments or actual decision timing. Four orders are fully offset; a fifth is partly reduced. All eight reported total-outlay fields are null. [Full calibration and order table](NAI-calibration.md).

A dated official-US-government-business general license offers a concrete possible lawful explanation (31 CFR 583.509 in December 2023; later 583.510). Qualification is not established. Neither a short interval nor the old vehicle automatically resolves authorization. The designation was already public; novelty of the order rows has not been established.

The other 12 pairs have name/alias matches but conflicting locations and no corporate-registration or ownership bridge. Keep them **unresolved**, with likely name collision as the strongest innocent explanation. Do not attribute their contract amounts to sanctioned entities. Two counterpart entities—Geotech Engineering and Patriot Inc.—were listed after all supplied FY2025 actions. That date finding does not exclude an untested earlier ownership-based restriction.

## Ranked reading list

Tier 1 is the supported identity/records question. Tier 2 cases are tied unresolved identity leads, not a risk ranking. Tier 3 adds a temporal reason the current-list screen cannot establish post-designation activity. Every original pair is retained, including both Digital Technologies UEIs.

| Tier | Recipient / UEI | Original actions | Listing date | Assessment |
|---|---|---:|---|---|
| 1 | [NAI LOGISTICS B.V.](dossiers/C13.md) / SLVJF3DR8MN5 | 1 | 2023-12-11 | credible identity; possible new child-order business; vehicle administrative |
| 2 | [ACS LOGISTICS LLC](dossiers/C01.md) / P7NTM9B6RG69 | 20 | 2023-12-12 | unresolved identity; likely name collision |
| 2 | [DIGITAL TECHNOLOGIES, INC.](dossiers/C02.md) / PGGGRPN3DDC7 | 38 | 2022-04-06 | unresolved identity; likely name collision |
| 2 | [GCS LLC](dossiers/C04.md) / JJXLTLEU5UN5 | 9 | 2024-10-30 | unresolved identity; likely name collision |
| 2 | [VMC, LLC](dossiers/C05.md) / DJF2Y1HE6JT6 | 3 | 2023-05-19 | unresolved identity; likely name collision |
| 2 | [ADVANCED TECHNOLOGIES, INC.](dossiers/C06.md) / FV58GN6ZNRK1 | 22 | 2018-11-05 | unresolved identity; likely name collision |
| 2 | [PHOENIX LLC](dossiers/C07.md) / HSDMSEKCW8J8 | 4 | 2024-02-23 | unresolved identity; likely name collision |
| 2 | [APSCO, LLC](dossiers/C08.md) / E9YGQYEK4NW7 | 3 | 2020-02-26 | unresolved identity; likely name collision |
| 2 | [RTS LLC](dossiers/C09.md) / XWSEFECGY3D9 | 1 | 2020-01-10 | unresolved identity; likely name collision |
| 2 | [DIGITAL TECHNOLOGIES, INC.](dossiers/C10.md) / GUGBC8JMR6X5 | 6 | 2022-04-06 | unresolved identity; likely name collision |
| 2 | [Z-AXIS, LLC](dossiers/C12.md) / DEAVQLC71338 | 3 | 2024-02-23 | unresolved identity; likely name collision |
| 3 | [PATRIOT LLC](dossiers/C03.md) / LYMKSJG6DLQ5 | 41 | 2026-04-24 | unresolved identity; all supplied rows predate identified designation |
| 3 | [GEOTECH ENGINEERING, INC](dossiers/C11.md) / NC4LP8N8L3B9 | 2 | 2025-10-14 | unresolved identity; all supplied rows predate identified designation |

## What Jev added—and did not

Jev agreed with the code/source assessment on the one strong identity and 12 weak identities. It added a consistent set of structured judgments and correctly rejected payment inference and the tested alias/ownership inventions. It found no new entity relationship or factual lead beyond the sources and ordinary code. The user-defined options and dossier context constrain this test: this was not a blind accuracy study or an open-ended entity-discovery benchmark.

The original screen already identified NAI and its zero-dollar termination. The useful new factual work—historical designation comparisons, child-order retrieval, separate positive/negative amounts, and the dated government-business authorization—came from official records and code. Jev selected the supported NAI follow-up after being supplied that work.

Jev's weaknesses are retained. One broad short-interval control scored 0.54 and failed the pre-set threshold, so candidate calls stopped. A narrower literal record question scored 0.96; six atomic controls then passed. In candidate output, activity labels often ignored unresolved identity: 12 labels required an identity gate/clarification. It also called Geotech's actions predesignation correctly but labelled Z-AXIS and Phoenix administrative; those labels are not legal clearance. [All overrides](jev/human-overrides.json), [failed control](jev/controls/evaluation.json), [revised controls](jev/controls-v2/evaluation.json).

## Bounded expansion

Only NAI qualified. The original Treasury designation notice supported five separately named members of the same disjunctive Rahmani designation group: NAI Logistics Limited, Fidelis Logistic and Supply Services, Secure Movement Logistics Services, Orbit International FZE, and RG Group FZE. Exact passage offsets/hashes and Jev selections were checked against the original notice and separate OFAC entries before search. These are **not established NAI subsidiaries or aliases**; exact ownership percentages and intermediary roles are unknown. Each is separately designated, so coverage is not inferred from association or the 50% rule.

Ten bounded USAspending queries—contracts and IDVs separately for each name, FY2024–FY2025, at most 20 rows per query—returned zero rows with no next page. This is a null result within these names, filters and dates, not proof of no historical, subcontractor, alias or differently reported activity. No extra seeds were introduced to fill a quota. [Exact extraction and search log](expansion/validated-extractions.json), [null results](expansion/search-summary.json), [rejections](expansion/rejections.json).

## Evidence and cost

Both original ZIPs were recovered from private repository main commit 218de208b504372e06f73abae79de1e2e21d25a1, safely extracted and CRC-checked. Shared OFAC files match byte-for-byte; SDN hash matches the original source manifest; report matches the preserved repository report. The recovered subset confirms 13 pairs, 153 distinct transactions, 72 awards, 9,980 entities and 23,398 names/aliases. The full-run counts of 6,639,176 transactions and 101,379 distinct recipient names remain original-run metadata, not newly recomputed corpus counts. No bulk redownload. [Recovery checks](recovery-verification.json), [original archives and hashes](baseline/manifest.json).

**New Jev usage-derived conservative cost: US$0.002443 across 21 paid calls.** This includes the failed control and its revision; each call is rounded up to the next microdollar. It is not an invoice. No other paid service. Prior Alberta spending is excluded. The $9 internal reservation cap and $10 authorization ceiling were never approached. [Exact prompts, responses and ledger](jev/ledger.json).

Eight offline guard tests and the original matching fixture passed; original subset counts, child sums and pagination were checked. [Technical annex and reproduction](FINAL-TECHNICAL-ANNEX.md). No outreach, credential changes, TLS bypass or resumed Alberta investigation.

## Remaining questions

Obtain original NAI order/modification instruments and purchasing timestamps; establish authorization scope for the actual transactions; review delivery acceptance and payment evidence if available. For any other candidate, first obtain a dated corporate identity/ownership bridge before attributing activity. Corporate registers, private licenses, original purchasing instruments, universal sanctions history and all NAI awards were not comprehensively obtained. The two bounded pilot stages are complete with those evidence limits; the result is a reading list, not verification of misconduct.
