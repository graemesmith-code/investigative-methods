# Acquisition data retention

The complete raw and normalized task data is retained at `/workspace/task-data/future-warfare-investments/`. Workspace persistence is **not independently guaranteed**. All 54 raw payloads were present and hash-checked, totaling 1,127,854,484 bytes; normalized/source-preserving views total 895,792,383 bytes.

Six portable archives are being prepared outside Git. Their exact contents, sizes and SHA-256 checksums will appear in `BUNDLE_MANIFEST.json`. A successful durable Library save has **not yet been confirmed in this checkpoint**; this file will be replaced with the actual per-file save outcome. No large raw or normalized files are committed to GitHub.

Raw retrieval URLs, timestamps and checksums are already published in `validation/http_manifest.jsonl`. `code/retrieve.py` verifies recovered bytes; it can re-request a bounded USAspending export if its generated URL expires. A regenerated/mutable source is a new snapshot and may not reproduce the old checksum.
