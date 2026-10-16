# Durable acquisition archives

**All six archives were saved successfully in private ChatGPT Library**, confirmed 2026-10-16 21:58:35 UTC. Every reported stored size matches the corresponding local archive; Library identity/version metadata was applied locally. Total archive bytes: **1,456,331,783**.

The task workspace remains available at `/workspace/task-data/future-warfare-investments/`, with archives at `/workspace/task-data/fwi-bundles/`. Workspace persistence is **not independently guaranteed**; use the confirmed Library copies for retention. No large data was committed to GitHub.

| Exact Library filename | Bytes | Library file ID |
|---|---:|---|
| `FWI-20261016-raw-sbir-snapshots.tar.gz` | 267,807,774 | `libfile_52a1b244ee0481918f64d0335aed7b93` |
| `FWI-20261016-raw-other-sources.tar.gz` | 352,286,033 | `libfile_5e847f29fc04819190a737e9eb9b3763` |
| `FWI-20261016-normalized-rd-contracts.tar.gz` | 298,091,981 | `libfile_73d770aecd84819190d75cca211793c9` |
| `FWI-20261016-normalized-capabilities.tar.gz` | 193,265,183 | `libfile_42799e02d6a48191b79d01305ca2d993` |
| `FWI-20261016-normalized-research-context.tar.gz` | 344,416,024 | `libfile_2c5e90bd409081918f53e9a9d5bf841a` |
| `FWI-20261016-provenance.tar.gz` | 464,788 | `libfile_172a4a390abc8191a8a0938be70ab5cc` |

[BUNDLE_SHA256SUMS](BUNDLE_SHA256SUMS) contains complete archive checksums; [BUNDLE_MANIFEST.json](BUNDLE_MANIFEST.json) lists every archive member, exact sizes/hashes, Library IDs, File Service IDs, authoritative Library paths and reported version numbers. [The retention receipt](validation/library_retention_receipt.json) records all six successful outcomes. The raw archives contain all 54 payloads (1,127,854,484 uncompressed/downloaded bytes); the normalized archives contain 895,792,383 bytes of source-preserving and derived views. These are overlapping representations, not additive financial records.

## Restore exactly

1. In Library, search an exact filename above, or reference its Library file ID. Download all six archives into one directory, along with `BUNDLE_SHA256SUMS` from this repository. The Library paths are the root filenames shown above; copies remain private to the current user.
2. Verify the archive bytes and extract into a new empty task-data directory:

```bash
sha256sum -c BUNDLE_SHA256SUMS
mkdir -p /workspace/restored-fwi-20261016
for archive in FWI-20261016-*.tar.gz; do
  tar -xzf "$archive" -C /workspace/restored-fwi-20261016
done
export ACQUISITION_DATA_DIR=/workspace/restored-fwi-20261016
/workspace/acquisition-venv/bin/python research/2026-10-16/future-warfare-investments/acquisition/code/retrieve.py --verify-only
```

The archive paths are relative `raw/`, `normalized/` and `provenance/`; extraction does not require the original environment. The provenance archive captures the validated pre-upload code/report checkpoint. Final Library receipts/checksum index are maintained here on GitHub to avoid circular archive hashes. Install the pinned dependencies using the technical annex before running scripts.

## Retrieval alternatives and limits

Exact raw URLs, UTC retrieval times and SHA-256 values are in [http_manifest.jsonl](validation/http_manifest.jsonl). `retrieve.py` can download missing payloads and verify the original checksums. Mutable SBA/Grants.gov files and regenerated USAspending exports can change; a later successful download is a new snapshot unless its hash matches. Generated USAspending links can expire; exact bounded request JSON remains in `evidence/`. The Library snapshots preserve the actual bytes acquired in this pass.

The worker upload helper initially failed before transfer because its app relay returned HTTP401. The existing authorized native Library save route succeeded for every archive; no credentials/accounts were created and no access bypass was used. No email was sent by this worker.
