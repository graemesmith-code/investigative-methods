# F5 global autonomy brakes — integrated review candidate

**Status: source bundles and both reporting lanes are integrated; the parent’s independent global release review remains open. This is not a final-completion claim.** Evidence cutoff: 25 October 2026. Immutable F4 baseline: `fa55e8d3d7c69bfc1051279185c7c88df8e92cb6`; b08baa4 is an earlier durable checkpoint.

Read [report.md](report.md), the [ranked 75-source reading pack](READING_PACK.md) and the five [thematic dossiers](memos/). [EDITOR_HANDOFF.md](EDITOR_HANDOFF.md) exposes the actual financial inventory/source archive. [MERGE_AND_GLOBAL_REVIEW.md](MERGE_AND_GLOBAL_REVIEW.md) records source/framing and provenance corrections awaiting independent closure.

## Verified data and boundaries

[Drive folder](https://drive.google.com/drive/folders/1JjNctZzLVUzuu0K469FS0cutxsZ4K1sS); [complete manifest](DRIVE_DATA_MANIFEST.json). Twelve file objects have exact-byte native readback, owner and inherited sharing checks. The frozen independent source bundle contains 42 whitelisted authored payloads plus 3 controls: five source memos and 37 non-memo payloads, all retained on Drive. Its TRANSFER_MANIFEST maps every payload; the outer manifest inventories all 3 controls. Logical archive paths are not invented standalone Drive file IDs. Raw PDFs/full texts/images/operational annexes are excluded.

The financial set remains **108 identities: 107 FAR two-view reconciliations plus one FPDS-only OT**, with **1,192 USAspending actions / 1,195 FPDS actions**, **113 negative FPDS actions** and **389 zero-dollar FPDS actions**. All 102 archive candidates and five targeted FAR follow-ups were hydrated. Anduril’s USAspending mapping is unverified. Exact source/accounting details and schedule discrepancies are in [financial methods](FINANCIAL_METHODS_AND_FINDINGS.md).

The patent registers reconcile **28 input rows →23 distinct publications / 19 reporting clusters**, after five exact publication overlaps and six cluster overlaps. The initial 16 publications / 13 families and native 12 clusters are historical input scopes, not additive totals. Every input row, legal-status limit and quarantined lead is preserved on Drive. Official grant PDF access for three cases does not establish current status, ownership, deployment or certification. [Patent search scope](PATENT_SEARCH_SCOPE.md).

The source master preserves **380 observations /308 distinct URLs**. These are not 308 independent studies or fully inspected source bodies. All 75 ranked sources have explicit access states; zero generic “see memo” access cells remain. The 104 unpromoted URLs whose body depth is undocumented are labelled bibliographic/discovery only. Journalistic novelty is separate from retrieval provenance.

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

[VERIFICATION.md](VERIFICATION.md) distinguishes checkpoint/local tests, independent financial recomputation, native readbacks and pending global release review. Four regressions and 412-source-body accounting passed. No hosted CI success is claimed.

## Spending and morning handoff

118 Exa requests reported $0.826 new cost; conservative opening $5.735, cumulative $6.561/$20, headroom $13.439. No uncertain requests, open reservations or cache hits. Provider response costs are not audited invoices. No other paid service was used.

[Briefing notes](BRIEFING_NOTES.md) remain provisional. No email was sent or automation created here; the parent owns the single 06:00 Europe/Rome (05:00 UTC), Monday 26 October briefing.

The [additional targeted integrated editorial review](https://drive.google.com/file/d/1_P3NjG-nz7QFkSY5NKnQ_FeSL_JuNx-V/view?usp=drivesdk) found no unresolved high/medium semantic objection within its stated scope and independently conserved source/patent inventories. Its exact 10,431-byte artifact was natively read back (SHA256 `bfab626e06d881e92257808471e05d829d928122ca660a61697d3c956172ebdc`). It is separate from the parent’s still-pending final release review.
