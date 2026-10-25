# Count terminology clarification — no data change

This additive note clarifies the frozen actual-recovery union review (SHA256SUMS `1fd2c346e40e186369addc3fd1d43e093854bb6cfaf45b436ef78e59137154da`). That bundle and its hashes remain unchanged.

Use these distinct denominators:

- **281 corrected conflicting source appearances:** 68 selected machine-hit appearances and 213 excluded appearances.
- **69 distinct conflicted-source lead keys retained in the recovery register:** 68 lexical keys plus one nonlexical, live-seed-related key for the SP4701-24-P-0068 SBIR source.
- The SP source has **zero machine hits**. Its inclusion is an explicit related-source review, not an extra lexical hit.
- **All 69 lead keys have `financial_match=False`.** They do not inherit the financial instrument's money.

The editor independently rechecked the 69-key set from `quarantine_provenance_keys` against the actual recovery CSV (SHA256 `4b33298674e457c15098cdf518f0d2c05796ddb3fba3bf3dcd11b31494940cad`): 68 `machine_lexical`, one `live_seed_related_identity_conflict_review`, zero financial matches. In this source subset the 69 distinct provenance physical-row references also happen to correspond to 69 distinct lead keys; these coinciding counts should not be used to blur their different units.

Accordingly, shorthand messages saying **“69 selected conflicted-source appearances” should be read as “69 retained conflicted-source lead keys,” not 69 selected machine-hit appearances**. The frozen memo already distinguishes 68 machine-screen hits plus one live-related source; this note makes the denominator explicit. This is a terminology clarification, **not a newly discovered data discrepancy**, and does not change the 27,276 union, any financial amount, the quarantine result, or the final-integration gate.
