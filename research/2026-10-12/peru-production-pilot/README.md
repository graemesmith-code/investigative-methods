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
