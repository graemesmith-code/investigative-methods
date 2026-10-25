# Actual recovered-register union: independent review

**25 October 2026. Local recovered Stage1 register passes the checks below. Final published integration remains pending.**

This review uses the **new** corrected recovery CSV, 75,092,372 bytes, SHA256 `4b33298674e457c15098cdf518f0d2c05796ddb3fba3bf3dcd11b31494940cad`. It is not the lost original 13,267-row register. The recovery deliberately changes the subaward/source grain, quarantines explicit recipient-UEI conflicts, and explicitly overlays known live seeds. Consequently the historical **17,858** expected union is superseded, not a target to which the recovery should be forced.

## Actual set accounting

| Exact source/instrument-key set | Count |
|---|---:|
| Published consumer register | 5,501 |
| New recovered Stage1 register | 22,603 |
| Exact intersection | 828 |
| Consumer only | 4,673 |
| Recovery only | 21,775 |
| Exact two-register union | **27,276** |
| Known live instruments | 111 |
| Live instruments missing from recovery | **0** |
| Final union after live overlay | **27,276** |

Do **not** add 111 to the union: all are already present. Recovery inclusion is 22,491 lexical-only rows, 87 lexical-and-live rows, 24 live-seed-only rows, and one live-related quarantined SBIR source. Thus 22,578 lexical rows + 24 seed-only + one related source = 22,603.

These are **source/instrument keys**, not unique awards, programs, funded safeguards, reviewed technical cases or a federal census. No money is summed across these source sets in this review.

## Financial and subaward checks

- All **1,621** directly comparable nonempty shared-key/window monetary cells agree exactly after cents-to-dollar conversion; **zero amount discrepancies**.
- **827** cells across **421** shared keys are consumer blank versus recovery `0.00`; 36 cells are blank in both. These are representation differences requiring a documented convention, not proof of no funding or monetary disagreement.
- Actual financial-match rows: consumer **3,663**, recovery **8,051**, intersection **816**, exact union **10,898**. Shared-key financial-match flags do not disagree. These are matches to acquired financial history, not current-funded-brake counts or allocated safeguard spending.
- All **7,964 SUBAWARD rows** have parent links, **zero financial-match flags**, and **no financial-window amounts**. Their source descriptions are retained without adding subaward money or assigning the parent's award money to each subaward.
- Live financial values are kept separately from the acquired-archive windows. The single FAR IDV and six prototype OtherTransactionIDV instruments remain distinct; four OT action-versus-aggregate discrepancies must not be erased in final selected money tables.

## Source-key projection and recipient quarantine

The independent pass read **133,958** provenance-sidecar rows. It linked **1,276** consumer source references to the same original current-SBIR records, with **zero physical-row disagreements**. There are **1,271** different-key provenance edges involving **1,237 consumer keys and 1,269 recovery keys**.

This proves overlapping source appearances. It does **not** justify mechanically merging full financial identities or subtracting the edge count from 27,276. Agency, parent instrument, phase and entity identity remain material. The retained metadata edge list provides explicit source IDs/hashes for any later adjudication.

The pass also checked the 281 explicit-UEI-conflict list against provenance. **Zero** conflicting SBIR source rows remain attributed to the conflicted financial award key. **69** conflicted source rows are represented under separate keys: 68 machine-screen hits plus the one live-related source. This is consistent with preserving the source lead while blocking unsupported financial/performer attribution; not all 281 source rows were selected by the lexical screen.

For **SP470124P0068**, the financial row now contains only its own government's obsolescence-research description and financial-source appearances. Its SBIR title is explicitly marked unlinked due to identity conflict, with a related unresolved-SBIR key. This resolves the local recovery's description-attribution problem. The old live-seed disposition remains a separately labeled historical annotation: final live/report tables should still use the qualified primary-description exclusion and unresolved-recipient caveat described in the separate identity review. No selected31 monetary case intersects the 281 conflicts.

## Conditions before final signoff

1. Publish/integrate the actual recovered-version inputs and their hashes; retain the recovery/loss explanation rather than marking original missing bundles delivered.
2. Use the new 27,276 exact-key union only with the grain/projection caveats above. Do not combine old 13,267/17,858 denominators with the new rows, and do not add already-included live seeds or subaward money.
3. Retain acquired-transaction-only financial attribution and acquisition-filter limitations. The three same-window historical omissions have now been independently reproduced from restored original inputs and byte-identically recovered primary XML.
4. Propagate the SP470124P0068 identity caveat into the actual final live inventory/crosswalk/disposition. Primary project-title corroboration is not proof of why recipient UEIs differ.
5. Inspect the actual final report, source links, manifests, genuine review loop and consolidated-text coverage. This local-register pass does not itself close R3-05 or establish universal absence of safeguards.

## Sources and replay

- Consumer source: [pinned a0ed CSV](https://raw.githubusercontent.com/graemesmith-code/investigative-methods/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/brakes-candidate-register.csv), SHA256 `65fab3fd33eacb78bacc2c78d500e90840d7bfc73adce7475fee0b3cd71fca1e`.
- Live identity source: [pinned a0ed combined inventory](https://raw.githubusercontent.com/graemesmith-code/investigative-methods/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/combined-live-inventory.csv), SHA256 `f8d6403fdaa87ae090804aef775f027a3bfef47a3f854e8bd8491a42cc68fa09`.
- Actual recovered Stage1 CSV is locally frozen at `/workspace/shared/f4-stage1-recovery/evidence/brakes-candidate-register.csv`, with the hash above; no unverified final public URL is fabricated.
- Recovered provenance sidecar SHA256 `2a3974b5d78d9ced2d41638b9fca53724c49c4e523bd1b5a2e27b534c0b6b21d`.

The two new Python scripts retain exact local replay paths; no network/paid calls are performed by these checks. JSON outputs contain exact-key differences, monetary representation differences and metadata-only provenance edges, not full SBIR bodies. The large already-retained input files are referenced by hashes rather than duplicated into this review bundle.
