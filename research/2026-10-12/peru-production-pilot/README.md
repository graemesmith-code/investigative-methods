# Peru production comparison pilot — 12 October 2026

A fixed 100-record experiment, including 35 gold records, comparing English company disclosures with Spanish official production records for Peru, 2019–2023.

**Finding:** sources can be acquired and numbers compared in bulk; automatic company contradictions have not been established. The pilot did not meet its 80-of-100 comparability target. There are recurring, identifiable leads for further public-record work.

Start with [NEWSROOM_BRIEF.md](NEWSROOM_BRIEF.md). It is written for an editor without a technical background.

| File | Purpose |
|---|---|
| [NEWSROOM_BRIEF.md](NEWSROOM_BRIEF.md) | Plain-language findings, gold leads, editorial recommendation |
| [RESULTS.md](RESULTS.md) | Every frozen record, including blocked and missing cases |
| [TECHNICAL_ANNEX.md](TECHNICAL_ANNEX.md) | Methods, gates, precision, limitations and scaling assessment |
| [CASE_REVIEW.md](CASE_REVIEW.md) | Findings and unresolved questions for each operator |
| [TRADE_CHECK.md](TRADE_CHECK.md) | Tested Peru customs route and destination-country limitations |
| [SOURCES.md](SOURCES.md) | Download URLs, retrieval results and evidence map |
| [IMPLEMENTATION.md](IMPLEMENTATION.md) | What runs now and concrete remaining implementation work |
| [comparison-input.json](comparison-input.json) | Reviewed observations and evidence gates for all 100 cases |
| [results.json](results.json) / [summary.json](summary.json) | Reproducible output and counts |
| [host-detailed-rows.json](host-detailed-rows.json) | Selected ministry monthly rows, plant/process labels and locators |
| [host-version-audit.json](host-version-audit.json) | Bulk totals checked against the annual summary |
| [review-ledger.json](review-ledger.json) | Per-record review disposition, including every raw alert |
| [agreement-audit.json](agreement-audit.json) | Deterministic sample of apparent agreements checked against originals |
| [source-manifest.json](source-manifest.json) | Source hashes, URLs and access outcomes |
| [frozen-batch.json](frozen-batch.json) / [PROTOCOL.md](PROTOCOL.md) | Pre-comparison selection and protocol |

Run from the repository root:

```bash
python code/peru_production_pilot/screen.py
python -m unittest discover -s code/peru_production_pilot -p 'test_*.py' -v
```

The comparison runner uses only the Python standard library. The acquisition and extraction helpers have separate dependencies described in the implementation notes. No contradiction or illegality is asserted by this dataset.

## Additional source and language follow-up

Start with [FOLLOWUP_NEWSROOM.md](FOLLOWUP_NEWSROOM.md). [FOLLOWUP_TECHNICAL.md](FOLLOWUP_TECHNICAL.md) documents the selected 25-record follow-up, gold quarterly diagnostics, 43 overlapping control checks and parked cases. No confirmed contradiction was found. Nexa SEC–SMV quantities agree exactly in two sampled years, including gold. The original 100-record counts above are unchanged.

- [FREE_API.md](FREE_API.md): tested free Nexa registry and implementation client.
- [MEDIA_NOVELTY.md](MEDIA_NOVELTY.md): prior reporting and implications for novelty.
- [followup-language-controls.json](followup-language-controls.json): reviewed bilingual/government-hosted values and fingerprints.
- [followup-case-ledger.json](followup-case-ledger.json): every selected annual lead's disposition.
- [followup-source-manifest.json](followup-source-manifest.json): tested downloads and replay information.

```bash
python code/peru_production_pilot/replay_language_controls.py
```

This replays reviewed arithmetic, not unattended extraction or claim-identity certification.
