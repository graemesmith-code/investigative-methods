# F5 global autonomy brakes — reviewed investigation

**Status: accepted within the independent editorial review’s stated scope, 25 October 2026, 23:05 UTC.** Evidence cutoff: 25 October 2026. Immutable F4 baseline: `fa55e8d3d7c69bfc1051279185c7c88df8e92cb6`. Independent editorial/source-accounting review passed on 25 October 2026 at 23:05 UTC for commit `b2824b47764deb9385afdcce84aa2c97aa623414` and its twelve enumerated Drive objects. All six integrated editorial objections were resolved within the stated review scope. This publication adds the verified audit bundle and status/presentation edits; it makes no material factual or monetary change. [Acceptance and audit records](https://drive.google.com/file/d/1VPy6SfRsk5_ubM_U674VZKkPTY-09bEO/view?usp=drivesdk). This is not a weapons-safety, legal-compliance, patent-status or effectiveness certificate.

Read [report.md](report.md), the [ranked 75-source reading pack](READING_PACK.md) and the five [thematic dossiers](memos/). [EDITOR_HANDOFF.md](EDITOR_HANDOFF.md) exposes the actual financial inventory/source archive. [MERGE_AND_GLOBAL_REVIEW.md](MERGE_AND_GLOBAL_REVIEW.md) summarizes the accepted source/framing and provenance corrections.

## Verified data and boundaries

[Drive folder](https://drive.google.com/drive/folders/1JjNctZzLVUzuu0K469FS0cutxsZ4K1sS); [complete manifest](DRIVE_DATA_MANIFEST.json). Thirteen file objects have exact-byte native readback, owner and inherited sharing checks. The frozen independent source bundle contains 42 whitelisted authored payloads plus 3 controls: five source memos and 37 non-memo payloads, all retained on Drive. Its TRANSFER_MANIFEST maps every payload; the outer manifest inventories all 3 controls. Logical archive paths are not invented standalone Drive file IDs. Raw PDFs/full texts/images/operational annexes are excluded.

The financial set remains **108 identities: 107 FAR two-view reconciliations plus one FPDS-only OT**, with **1,192 USAspending actions / 1,195 FPDS actions**, **113 negative FPDS actions** and **389 zero-dollar FPDS actions**. All 102 archive candidates and five targeted FAR follow-ups were hydrated. Anduril’s USAspending mapping is unverified. Exact source/accounting details and schedule discrepancies are in [financial methods](FINANCIAL_METHODS_AND_FINDINGS.md).

The patent registers reconcile **28 input rows → 23 distinct publications / 19 reporting clusters**, after five exact publication overlaps and six cluster overlaps. The initial 16 publications / 13 families and native 12 clusters are historical input scopes, not additive totals. Every input row, legal-status limit and quarantined lead is preserved on Drive. Official grant PDF access for three cases does not establish current status, ownership, deployment or certification. [Patent search scope](PATENT_SEARCH_SCOPE.md).

The source master preserves **380 observations / 308 distinct URLs**. These are not 308 independent studies or fully inspected source bodies. All 75 ranked sources have explicit access states; zero generic “see memo” access cells remain. The 104 unpromoted URLs whose body depth is undocumented are labelled bibliographic/discovery only. Journalistic novelty is separate from retrieval provenance.

All Git files stay below 100,000 bytes. No raw transaction/patent dumps, query/review logs or PDFs are committed. [SHA256SUMS](SHA256SUMS) covers all Git delivery files except itself; Drive objects and superseded byte versions are hashed in the pointer manifest. Existing F4/root files remain unchanged.

## Reproduction and review

Portable standard-library code is in [code/](code/): exact-identity lifecycle hydration, complete archive screening, independent cached-body validation, regressions, manifest construction, and `assemble_reviewed_register.py`. The older `build_reading_pack.py` reproduces the checkpoint format; it is superseded for final assembly. Raw output belongs outside Git.

```sh
python3 code/scan_safety_archive.py --archives ARCHIVES --out DATA
python3 code/hydrate_full_award_lifecycle.py --candidates CANDIDATES.csv --out DATA
python3 code/validate_hydration.py --data DATA
python3 -m unittest discover -s code -p 'test_*.py' -v
python3 code/sync_drive_manifest.py VERIFIED_RECEIPTS.json --output DRIVE_DATA_MANIFEST.json
```

[VERIFICATION.md](VERIFICATION.md) distinguishes checkpoint/local tests, independent financial recomputation, native readbacks and scoped independent acceptance. Four regressions and 412-source-body accounting passed. No hosted CI success is claimed.

## Spending and briefing

118 Exa requests reported $0.826 new cost; conservative opening $5.735, cumulative $6.561/$20, headroom $13.439. No uncertain requests, open reservations or cache hits. Provider response costs are not audited invoices. No other paid service was used.

[Briefing notes](BRIEFING_NOTES.md) summarize the accepted findings. Detailed review records, including earlier holds and their resolution, remain Drive-only in the [final audit bundle](https://drive.google.com/file/d/1VPy6SfRsk5_ubM_U674VZKkPTY-09bEO/view?usp=drivesdk).
