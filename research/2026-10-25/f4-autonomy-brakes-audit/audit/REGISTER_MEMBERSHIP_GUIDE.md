# Register membership and acquisition-history limits

The registers answer different questions. Their row counts must not be added as
though each were a disjoint population of distinct safeguards or programs.

| View | Purpose | What its count does not establish |
|---|---|---|
| `evidence/brakes-candidate-register.csv/.json` | Canonical and supplementary archive screen with complete descriptions, preliminary terms/tags and exact source-key financial linkage where available | Confirmed safeguards, unique real-world awards when SBIR/document keys differ, or complete federal award histories |
| `evidence/live-award-register.json` | Exact standard public award records and disclosed contract/assistance histories | Technical acceptance, actual performance, or all recent/nonpublic activity |
| `evidence/ota-resolution-review.json` and `ota-keyword-followup-records.json` | Separately parsed public FPDS OtherTransactionIDV prototype identities and actions | A zero-obligation FAR parent vehicle, or automatically reconciled money where aggregate/action gaps remain |
| `evidence/available-register-membership.csv` | Compact exact-key source/instrument membership across the available archive, standard live and OTA records | Distinct real-world award/program count or any combined financial total |
| `audit/parallel-register-reconciliation.json` | Records the unavailable original independent-screen comparison and conditional versioned recovery | An observed independent union, a second financial population, or permission to merge by recipient/short PIID |

## Available-source membership

At the hashed snapshot recorded in `audit/available-register-membership.json`,
5,501 archive keys, 105 standard live records and six OTA primary identities form
an exact-key union of **5,585 source/instrument keys**. The archive/standard exact
intersection is 27; 78 standard identities are not exact keys in that archive
screen; all six OTA primary identities are distinct schema-specific keys.

These are deliberately **source keys**, not 5,585 proven distinct awards. An
archive SBIR key may refer to the same real award as a fully qualified live
procurement key. Such possible equivalence needs agency, parent and transaction
evidence; no short-PIID or company-name merge is silently performed. The two
formerly unresolved standard target searches that have separately verified OTA
identities remain explained in the audit. Their absence from a contract parser
was not program-absence evidence.

The original independent Stage1 comparison is **unavailable because the producer runtime lost its original output bodies and scripts before verified publication**, as reported by the parent at18:55. The earlier GitHub approval resolved successfully; approval is no longer the blocking dependency. `audit/independent-stage1-retained-metadata.json` preserves metadata for135 expected files, not their original contents. `audit/parallel-register-reconciliation.json` records this loss and the metadata hash.

The consumer's complete scan remains authoritative: all three hash-verified archives, its original screening script and outputs remain intact. The **5,585-key available-source index is complete for its stated inputs**. Historical parent-reported expectations of13,267 independent keys and a17,858-key combined union were never independently observed here and must not be reported as actual counts. If a verified recovery version arrives, compare its actual membership, financial-match flags and hashes under a distinct version; do not force those expectations or treat the same supplied corpus as new disjoint activity.

## Complete acquired inputs are not complete acquisition histories

`audit/acquisition-history-coverage.json` and
`evidence/acquisition-history-missing-actions.csv` independently compare three
selected histories against the canonical financial table by exact transaction
identity, action date and integer cents. Both sides use the same fiscal window:
**FY2019–FY2026, October 1, 2018 through September 30, 2026**.

| Complete award identity | Acquired archive actions | Disclosed live actions in same window | Missing historical actions | Live minus acquired obligations |
|---|---:|---:|---:|---:|
| `CONT_AWD_FD01_9700_N0017814D7932_9700` | 70 | 72 | 2 | $50,000.00 |
| `CONT_AWD_N0016422F3007_9700_N0017819D7763_9700` | 6 | 19 | 13 | $19,330,807.97 |
| `CONT_AWD_N0042123F3004_9700_N0017819D7484_9700` | 3 | 53 | 50 | $25,619,330.91 |

All **79 shared exact actions** agree on dates and cents. The 65 missing actions
include old history, not just the newest quarter. Therefore source acquisition
coverage is a separate limitation from the DoD contract-publication delay. The
exact acquisition/filtering cause is not established here; no invented raw
provenance is supplied and no canonical ledger is patched.

This is a selected positive demonstration of a history-coverage gap, not an
estimate of all missing actions in the corpus, an allegation that acquired
amounts were corrupted, or evidence that these whole broad orders are
safeguard-specific spending. Internal reconciliation of all supplied rows can
pass while the acquired source history remains incomplete.

## Reproduce

Run `python3 code/reconcile_available_registers.py --sqlite PATH` after creating
the canonical screen SQLite database. It hashes the source registers before and
after reading, refuses ambiguous identities, and writes only derived membership
and history-evidence files. Run `code/reconcile_parallel_registers.py` separately
against the final independent CSV or gzip snapshot, with explicit column/unit
mapping if needed. Both scripts preserve the input registers and produce no
combined safeguards-dollar estimate.
