# Register membership and acquisition-history limits

The registers answer different questions. Their row counts must not be added as
though each were a disjoint population of distinct safeguards or programs.

| View | Purpose | What its count does not establish |
|---|---|---|
| `evidence/brakes-candidate-register.csv/.json` | Canonical and supplementary archive screen with complete descriptions, preliminary terms/tags and exact source-key financial linkage where available | Confirmed safeguards, unique real-world awards when SBIR/document keys differ, or complete federal award histories |
| `evidence/live-award-register.json` | Exact standard public award records and disclosed contract/assistance histories | Technical acceptance, actual performance, or all recent/nonpublic activity |
| `evidence/ota-resolution-review.json` and `ota-keyword-followup-records.json` | Separately parsed public FPDS OtherTransactionIDV prototype identities and actions | A zero-obligation FAR parent vehicle, or automatically reconciled money where aggregate/action gaps remain |
| `evidence/available-register-membership.csv` | Compact exact-key source/instrument membership across the available archive, standard live and OTA records | Distinct real-world award/program count or any combined financial total |
| `audit/parallel-register-reconciliation.json` | Records original producer loss and the actual separately versioned recovery comparison | A distinct-award count, a second financial population, or permission to merge by recipient/short PIID |

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

## Verified recovery version comparison

The original independent producer lost its output bodies and scripts before verified publication. Its retained metadata is at `audit/independent-stage1-retained-metadata.json`; historical expectations of13,267 keys or17,858 combined keys were never independently observed here and are not actual counts. The earlier approval resolved and is no longer a gate.

The [recovery-v1 guide](../evidence/independent-stage1-recovery-v1/README.md), [storage map](../evidence/independent-stage1-recovery-v1/storage-map.json) and [canonical manifest](../evidence/independent-stage1-recovery-v1/canonical-manifest.json) locate complete gzip registers and the multipart canonical package. The source CSV is the logical `evidence/brakes-candidate-register.csv` inside that archive; no standalone plain recovery CSV or 127 MB JSON is implied.

A separately versioned **recovery-v1** core is now compared against the frozen consumer register. It is a rebuilt version, not asserted byte-equivalent to the lost original. The observed recovery CSV SHA256 is `4b33298674e457c15098cdf518f0d2c05796ddb3fba3bf3dcd11b31494940cad`; its manifest SHA256 is `7d49fa1ba294a5a9c3f578230c5fe348d17b92f6fecf56fb514d1272e50830de`. Both input hashes remained stable during comparison.

| Exact-key view | Count |
|---|---:|
| Frozen consumer screen | 5,501 |
| Recovery-v1 screen and explicitly marked live seeds | 22,603 |
| Exact shared keys | 828 |
| Consumer only | 4,673 |
| Recovery only | 21,775 |
| Exact union of source/instrument keys | **27,276** |

All 105 standard live and six OTA identities already occur in recovery-v1, including 87 lexically discovered and 24 seed-only rows. Adding 111 again would double-count. `evidence/parallel-key-membership.csv` retains each register's row and categories; `evidence/combined-key-membership.csv` adds source membership flags without copying large descriptions or summing money. **27,276 is not a distinct-award, program, or verified-safeguard count.**

Actual acquired-ledger matches are 3,663 consumer and 8,051 recovery, with 816 shared keys: an exact-key union of 10,898 ledger-matched keys, still not an allocated safeguards portfolio. Prefix-shaped keys alone give different counts and are not the financial denominator. Across the three comparable windows, 1,621 common nonempty monetary cells agree exactly in integer cents; none differ. Another 827 fields across 421 keys pair consumer blanks with recovery 0.00. Those representations remain explicit: a ledger-matched award may have no actions in a window, while an unmatched source lead is not known to have zero funding. No null value is silently filled and no money is added across screens.

Recovery includes 7,964 subaward-only rows, all without financial matches or window amounts; their parent links are provenance, not extra prime spending. Identity-quarantine counts use separate units: 281 conflicting source appearances comprise 68 machine-hit and 213 excluded appearances; 69 retained conflicted-source lead keys comprise 68 lexical plus one SP live-related lead, all without financial attribution. The SP470124P0068 financial award is a separately identified live-seed-only obsolescence row ($99,767 acquired obligations), not normative-safeguard spending. The consumer's guard correctly does not select that financial row on the conflicted SBIR description.

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
