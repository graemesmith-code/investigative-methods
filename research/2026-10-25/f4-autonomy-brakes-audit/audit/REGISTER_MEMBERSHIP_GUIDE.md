# Register membership and acquisition-history limits

The registers answer different questions. Their row counts must not be added as
though each were a disjoint population of distinct safeguards or programs.

| View | Purpose | What its count does not establish |
|---|---|---|
| `evidence/brakes-candidate-register.csv/.json` | Canonical and supplementary archive screen with complete descriptions, preliminary terms/tags and exact source-key financial linkage where available | Confirmed safeguards, unique real-world awards when SBIR/document keys differ, or complete federal award histories |
| `evidence/live-award-register.json` | Exact standard public award records and disclosed contract/assistance histories | Technical acceptance, actual performance, or all recent/nonpublic activity |
| `evidence/ota-resolution-review.json` and `ota-keyword-followup-records.json` | Separately parsed public FPDS OtherTransactionIDV prototype identities and actions | A zero-obligation FAR parent vehicle, or automatically reconciled money where aggregate/action gaps remain |
| `evidence/available-register-membership.csv` | Compact exact-key source/instrument membership across the available archive, standard live and OTA records | Distinct real-world award/program count or any combined financial total |
| `evidence/parallel-key-membership.csv` | Exact-key comparison with the independent Stage1 screen, once that source is materialized and compared | A second independent financial population or permission to merge by recipient/short PIID |

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

The independent Stage1 source is still pending in this executor at this note's
creation. Its exact snapshot comparison is recorded separately in
`audit/parallel-register-reconciliation.json`. Neither its candidates nor its
input rows may be added to this view as new disjoint federal activity.

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
