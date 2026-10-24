# Reproducing the local checks

Python 3's standard library is sufficient. The validator is read-only and makes no network requests:

```sh
python code/validate_evidence.py
```

To reproduce the exact FA8651 prefix selection, supply the earlier 384-row register:

```sh
python code/validate_evidence.py --source-384 /path/to/lane1-tactical-candidates-384.csv
```

The immutable input is [the published CSV at commit e931fcbc6dc52c00b0565e853637a64fa95773b3](https://github.com/graemesmith-code/investigative-methods/blob/e931fcbc6dc52c00b0565e853637a64fa95773b3/research/2026-10-24/f2-tactical-ai/audit/lane1-tactical-candidates-384.csv). Original bytes: 508,667; SHA-256: `cfe921e6d629c71e1a916802f7d2395c4c6de8d453426293eba081bf202186b0`. A connector-normalized text copy used in this investigation has 508,283 bytes. Its membership was checked without claiming byte identity.

The validator checks all seven ASIMOV awards against 43 action deltas, and all twenty FA8651 procurement contracts against 124 action deltas. Two grants have no FPDS contract histories. It checks the six named-case sums, six date-field matches and the single overlapping Saab award. It does not treat date-field matches as active work or financial reconciliation as proof of capability.

## What is and is not a complete extraction replay

The CSV/JSON files are the reviewed 24 October 2026 snapshots. Exact source URLs and retrieval dates are provided. The ASIMOV `fetch_primary.py`, `fetch_archive.py` and `parse_actions.py` files preserve the original retrieval/parsing logic as research provenance. They are **not a production-grade, end-to-end replay tool**. In particular:

- Run them only in a separate working copy. They create raw responses and can overwrite derived tables beside the scripts.
- The original ASIMOV FPDS fetch requests the first page. The reviewed snapshot had at most eight returned actions per award and no next-page link, so it was complete for that snapshot. A future response with more actions requires pagination before summation.
- The parser expects nonempty valid records. If acquisition fails or returns no records, inspect the errors rather than treating an empty or partial result as evidence.
- The full Eglin acquisition was paginated and reconciled during this investigation, but a generalized live extractor is not distributed here. The exact 124 reviewed deltas and source-feed URLs are supplied; the validator reproduces their arithmetic.
- Re-fetching a mutable API later can legitimately produce different values, dates or actions. That is a new snapshot, not a failure of the archived arithmetic. Retain its retrieval times and hashes separately.
- Raw administrative fields and full copyrighted articles are deliberately excluded from this public package. Source hashes identify inspected responses; they are not substitutes for publicly retrievable contents.

The Exa ledger documents the actual historical search requests. Rerunning paid searches is not necessary to validate these local tables and may return different results or incur charges. No credentials are included.
