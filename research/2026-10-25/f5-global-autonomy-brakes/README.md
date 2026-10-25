# F5: Global architecture of autonomy brakes

Completed public-source investigation, evidence cutoff 25 October 2026. This is new F5 reporting and live retrieval, anchored to immutable F4 commit `fa55e8d3d7c69bfc1051279185c7c88df8e92cb6`.

Start with [report.md](report.md), then the ranked [75-source reading pack](READING_PACK.md). The five [thematic dossiers](memos/) cover Five Eyes/AUKUS, NATO/EDF, US safety boards, patents, and legal review/software updates. Read [financial methods and findings](FINANCIAL_METHODS_AND_FINDINGS.md) for exact award identities, schedule discrepancies and full-lifecycle corrections; [patent search scope](PATENT_SEARCH_SCOPE.md) documents database and negative-result limits.

The key finding is an overlapping assurance architecture with documented friction and incomplete public visibility of configuration-specific implementation. F5 does not prove a global absence of controls, universal effectiveness, named JSP936 failures or named unlawful bypasses.

## Data and verification

[Drive data folder](https://drive.google.com/drive/folders/1JjNctZzLVUzuu0K469FS0cutxsZ4K1sS) contains ten uploaded objects. [DRIVE_DATA_MANIFEST.json](DRIVE_DATA_MANIFEST.json) lists every object, including early checkpoints, with exact view URL, bytes, SHA256, row count or non-tabular designation, and readback/ownership/sharing evidence. The raw financial archive has 418 members including its inventory; the public supporting package has 14. Each inventory lists every payload file; its own hash is retained in the outer manifest. Historical snapshots overlap and must not be added to final counts.

Final financial set: **108 identities = 107 FAR two-view reconciliations + one FPDS-only OT**; **1,192 USAspending actions / 1,195 FPDS actions**, **113 negative FPDS actions**. The original archive sweep yielded 102 candidates; five targeted FAR follow-ups and one separate OT followed. Anduril's USAspending mapping remains unverified.

The patent register has **16 publications / 13 representative families**, including civilian/general-assurance comparators. The master source-observation register has **145 distinct source URLs**, with aliases and separate evidence-quality/currentness/implementation/funding/novelty fields. These counts are not numbers of deployed safeguards.

[VERIFICATION.md](VERIFICATION.md) records tests and limitations. [SHA256SUMS](SHA256SUMS) covers every Git delivery file except itself; Drive object hashes are in the manifest. No file in this new Git path exceeds 100,000 bytes; no raw transaction/patent dumps or PDFs are committed. Existing F4/root files are preserved.

## Reproduction

Portable Python standard-library scripts are in [code/](code/). Supply your own local paths; output raw data outside Git:

```sh
python3 code/scan_safety_archive.py --archives ARCHIVES --out DATA
python3 code/hydrate_full_award_lifecycle.py --candidates CANDIDATES.csv --out DATA
python3 code/validate_hydration.py --data DATA
python3 -m unittest discover -s code -p 'test_*.py' -v
python3 code/sync_drive_manifest.py VERIFIED_RECEIPTS.json --output DRIVE_DATA_MANIFEST.json
```

The hydrator needs exact generated identities or an explicitly observed native FPDS identity. The archive is a discovery index. Do not substitute a PIID-only search result or infer missing award keys. Native Drive uploads and raw-byte readback precede receipt creation; the manifest tool does not perform uploads or fabricate success.

## Spending and briefing

118 new Exa requests reported **$0.826**, equal to reserved new exposure. Opening conservative exposure **$5.735**, cumulative **$6.561**, remaining hard-ceiling headroom **$13.439**. No uncertain requests, open reservations, or cache hits. Provider response costs are not an audited invoice. Current pricing was checked at https://exa.ai/pricing before spending; no contents, generated summaries or other paid services were used.

[Briefing notes](BRIEFING_NOTES.md) provide a compact handoff. This task sent no email and created no automation; the parent owns the single 06:00 Europe/Rome (05:00 UTC) Monday 26 October briefing.
