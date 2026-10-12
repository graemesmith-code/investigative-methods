# Mining disclosure comparison starter

Four narrowly approved comparisons; four consistent specimens; no established contradiction. Start with the [readable account](../../experiments/11-mining-disclosure-pairs.md). The [full audit](../../annexes/mining-claims-audit.md) explains the judgments behind the code.

## Run the inspected examples

From the repository root, with Python 3.10 or later:

```sh
python code/mining_claims/run.py
python -m unittest discover -s code/mining_claims -p 'test_*.py' -v
```

These commands need no credentials, network or additional packages. The first command labels its output `audited_fixture_replay`: saved observations demonstrate the comparisons. The tests include deliberately altered numbers; those artificial gaps are not research findings.

## Re-extract the inspected originals

Install the workbook reader in your usual Python environment. Set a descriptive user agent with your contact address before downloading; replace the example address.

```sh
python -m pip install -r code/mining_claims/requirements.txt
export RABBIT_HTTP_USER_AGENT='Rabbit mining research your-address@example.org'
python code/mining_claims/sources.py
python code/mining_claims/extract.py
python code/mining_claims/run.py --observations code/mining_claims/output/extracted-observations.json
```

The downloader retrieves the 16 distinct documents supporting the four contracts, including documents needed for the scope checks. Use `--case RAB-MIN-02` to retrieve just one case, or `--all-audit` for all 31 audit sources. Extraction currently requires all four cases. If originals are already present, pass their directory with `--cache /path/to/originals` to both source and extraction commands. Source filenames must match the manifest IDs, including the `.bin` names used for three Excel files.

```sh
python code/mining_claims/sources.py --verify-only --cache /path/to/originals
python code/mining_claims/extract.py --cache /path/to/originals
```

Every original is checked against its saved SHA-256 fingerprint and byte count. A changed document, unavailable URL, HTML landing page masquerading as a PDF, or missing workbook cell stops the relevant operation. A changed fingerprint means review is needed, not misconduct. No approval transfers automatically to a new filing. Download logs and downloaded files stay in the ignored cache directory.

## What has and has not been implemented

| Component | Present behavior |
|---|---|
| Four case files | Exact project, period, metric, evidence locations and permitted comparison. |
| Source retrieval | Free public URLs, paced downloads, file checks, immutable version matching and local access log. Access can change after the recorded test. |
| Host extraction | Reads all four company-attributed workbook specimens, including Essakane's embedded workbook. |
| Western extraction | Peru's per-mine production table is parsed from SEC HTML. Ity royalties/FX and Kibali/Essakane ownership use explicit manually reviewed entries tied to verified source versions. |
| Meaning and attribution | Preserved audit judgments; the software does not rediscover or prove the entity bridges and reporting definitions. |
| Comparison | Decimal arithmetic, conservative production precision, royalty FX intervals, ownership across every admissible date. |
| Output | `consistent`, `contradiction_candidate`, or `blocked`. A candidate still needs extraction and amendment review before reporting. |
| Live monitoring / AI translation | Not implemented. No scheduled process, API key, model call or paid service. |

## Four implementation files

| File | First production task | Acceptance condition |
|---|---|---|
| [peru-2023.json](cases/peru-2023.json) | Generalize the per-mine table parser to adjacent years, explicitly locating year headers and preliminary footnotes. | A new period cannot inherit the 2023 approval; Mexico, sales, gross concentrate and preliminary figures are rejected. |
| [ity-2024.json](cases/ity-2024.json) | Extract the Western royalty row and currency note; build a dated three-company licence crosswalk. | Both royalty components for SMI, SMD and SMF are complete; payment-date FX and unchanged company figures are verified. Negative payments need a separate calculation. |
| [kibali-2023.json](cases/kibali-2023.json) | Extract the Western group-interest statement with its effective period and attribution. | The system distinguishes economic interest from direct registered shares and does not infer an AngloGold comparison from the Barrick specimen. |
| [essakane-2023-2024.json](cases/essakane-2023-2024.json) | Extract dated Western ownership statements and independently resolve the outer-to-embedded workbook relationship. | Both original date labels survive; any alert is incompatible under both; the June 2025 change is never compared as if it applied in 2023/2024. |

## Technical annex: handoff and data contract

`cases/` contains the reviewed contracts. `fixtures/observations.json` contains the checked numbers, original-source fingerprints, context and gate states. `fixtures/manual-western-claims.json` identifies the Western assertions that still require manual review. `fixtures/expected-results.json` records the fixture replay. The [numeric controls](../../research/2026-10-12/mining-claims/numeric-controls.json) retain finer evidence locations; the [implementation plan](IMPLEMENTATION.md) orders the remaining work.

An observation must name its case, schema version, complete source set and matching context. Unknown, missing, non-finite and negative values are handled explicitly; a blank is never changed into zero. Gates are only assertions of completed research review. A caller setting them to `true` does not itself establish truth or comparability. Current extraction reuses those judgments only after verifying every pinned source.

The source archive is an evidence index with checked extracts, not a duplicate of all third-party reports. The public URLs, original retrieval times, hashes and sizes are preserved in the [source manifest](../../research/2026-10-12/mining-claims/source-manifest.json). The code does not silently use a replacement edition if the exact one becomes unavailable.
