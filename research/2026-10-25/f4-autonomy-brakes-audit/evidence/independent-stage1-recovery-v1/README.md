# Verified independent recovery-v1 register and complete package

This is a **new versioned rerun**, not a claim to reproduce the lost original register. All141 canonical files—375,285,567 stored bytes—are preserved unchanged in the exact public archive parts. The original package SHA256 is `2fda8de2231b5bed45041a7846a89b11fce50a7c82671b6b176eeb2630d2094c`; canonical manifest SHA256 is `7d49fa1ba294a5a9c3f578230c5fe348d17b92f6fecf56fb514d1272e50830de`.

## Fast-access complete registers

- [Full candidate CSV, gzip](brakes-candidate-register.csv.gz): all22,603 rows and full descriptions; expands to75,092,372 bytes.
- [Full candidate JSON, gzip](brakes-candidate-register.json.gz): complete127,610,577-byte JSON, losslessly encoded because its plain size exceeds the GitHub file limit.
- [301 A/B review leads](ab-high-priority-review.csv): priority candidates, not301 verified programs.
- [Canonical manifest](canonical-manifest.json), [all-file storage mapping](storage-map.json), [logical compression map](publication-representation-map.json).
- Preserved authored methods: [original recovery guide](canonical-README.md), [methods](METHODS-RECOVERY.md), [financial limits](FINANCIAL-SCOPE-ADDENDUM.md).

The register has22,578 lexical keys,24 live-seed-only instrument keys and1 separately retained identity-conflict lead.8,051 keys match the acquired financial ledger;7,964 separately keyed subaward reports carry no parent obligations. The two-register union with the consumer’s5,501 keys is27,276 source/instrument keys, **not distinct programs or necessarily distinct awards**. All111 initial live instruments are already included; they are not added again. Preliminary categories overlap and do not constitute a safeguards spending total.

## Exact complete package

Download all three parts in this directory: [part0000](package.tar.gz.part-0000), [part0001](package.tar.gz.part-0001), [part0002](package.tar.gz.part-0002). Their order, sizes and SHA256 values are in the storage map. Concatenation restores the original212,754,687-byte tar.gz without recompression. Each public file is below100MiB.

From the F4 package directory, run:

```sh
python3 code/restore_stage1_recovery.py --destination /absolute/private/stage1-recovery-v1
```

The script verifies every part, the full archive, and every canonical member before installing it; it rejects unsafe paths and existing different files. The canonical `SHA256SUMS` verifies139 member files plus `manifest.json`; the checksum file cannot hash itself. Gzip sidecars retain complete logical data, with expanded sizes/hashes and any intentionally excluded private runtime inputs recorded in the publication-representation map. No rows, descriptions or authored files are silently truncated.

The fast-access files are duplicate encodings/copies of canonical members, not new observations or money. Archived transaction-window nets can omit historical modifications and are not complete award histories or guaranteed lower bounds. Blank/zero semantics, entity conflicts and source/financial identities remain explicit. The original lost13,267-key version is historical; its old counts/hashes are not forced onto this rerun.
