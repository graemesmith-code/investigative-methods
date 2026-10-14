# Reproduce the completed pilot

Analysis uses Python’s standard library. PDF rendering additionally uses installed ReportLab. No paid service, model or credential is required. Pinned snapshots define these findings; newer live inputs may differ.

## Inputs

Existing repository inputs: research/FARA_All_*.csv and the two experiments/OFAC evidence ZIPs. New US/Canadian bulk files are omitted from publication. Obtain the exact snapshots in SOURCE-MANIFEST.json / SOURCE-LEDGER.json, verify byte counts and SHA-256, and place under this directory’s ignored evidence/ folder:

- FY2025_All_Contracts_Full_20260906.zip
- canada-registrations.zip
- canada-dictionary.xlsx
- canada-contract-history.csv

FARA encoding is CP1252. Fifteen principal rows are quarantined, not guessed into alignment. If the original online archive has expired/changed, that is a replay limitation. Complete inspected sources remain local to the original pilot.

Extract results/screen-summary.json and results/contract-source.json from experiments/sanctions-screen-evidence-2026-09-18.zip into evidence/prior-ofac-screen-summary.json and evidence/prior-ofac-contract-source.json for prior-audit verification. Old LDA/FARA dossiers and three grant query responses are provenance, not an instruction to repeat collection.

## Local execution from repository root

```bash
python research/2026-10-14/fara-award-pilot/reproduce.py research/2026-10-14/fara-award-pilot/evidence/FY2025_All_Contracts_Full_20260906.zip
python research/2026-10-14/fara-award-pilot/canada.py
python research/2026-10-14/fara-award-pilot/review.py
python research/2026-10-14/fara-award-pilot/summarize.py
python research/2026-10-14/fara-award-pilot/verify.py
python research/2026-10-14/fara-award-pilot/publication.py
python research/2026-10-14/fara-award-pilot/render_public_report.py
```

reproduce.py reads all seven contract members and creates local FARA entities, recipient index, candidate actions and counts. canada.py reads full primary/funding exports and bounded history with firm/client roles separate. review.py applies exact name/address/time gates and same-name/UEI expansion. summarize.py deduplicates actions and computes decimal obligations. verify.py checks saved census, candidates, dates and accounting. publication.py writes sanitized tables and reconciled dossiers. render_public_report.py renders reports locally without network calls.

Raw intermediates remain ignored. Public tables are CANDIDATE-SCREEN.csv, US-RESULTS.csv, CANADA-RESULTS.csv, compact-candidates.csv and amounts.csv. Do not bulk-add evidence. README and technical annex are authored accounts; regenerate the amount narrative before publication.py, which adds its scope clarification.

## Expected results

273 candidate pairs; 12 US recipient-role-registration keys; four Canadian role keys representing three names. Direct scope: **14 groups / 79 actions / 37 award-or-IDV IDs**. Expanded scope: **21 groups / 2,310 actions / 1,719 award-or-IDV IDs**. The direct actions are included in the expanded set, not added. Money is expanded obligation changes, not payments.

US census: 6,639,176 transactions and 101,379 recipient names, archive hash matched to prior audit. Canadian/review summaries reproduced; saved evidence and amounts verified. Publication does not rerun the broad US analysis or collect new inputs. Canadian history’s seven FARA candidates have zero temporal pairs; this is not a comprehensive Canadian negative.

PUBLICATION-SHA256SUMS fingerprints public files. Source manifests fingerprint omitted inputs. Opaque group IDs cannot replace withheld original addresses for independent replay.
