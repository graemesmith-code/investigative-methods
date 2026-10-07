# Technical annex — completed bounded pilot

The README is the current result. `technical-annex.md`, `recovery-status.json` and `reattachment-recovery-status.json` preserve earlier access failures and are superseded by successful repository recovery. No failed Library transfer was bypassed.

## Baseline and reproducibility

Original ZIPs were read as Git blobs from `origin/main`, commit `218de208b504372e06f73abae79de1e2e21d25a1`, at the two user-supplied `experiments/` paths. The working branch was not reset or merged over unrelated work. ZIP members were checked for absolute paths, `..`, symlinks, a 150 MB total uncompressed bound, and CRC errors before extraction. Raw archives are preserved under `baseline/`.

`baseline/manifest.json` records archive hashes and members. `baseline-file-hashes.json` hashes recovered local files. The SDN XML SHA-256 is `ab7951b5b70c22068903f1e571362f4358b90f2b983a966f322c82dffeca8170`, matching the original metadata. Both packages' shared OFAC bytes agree. Original report bytes agree with `evidence/ofac/original-report.md`. Subset counts and the original matching fixture passed. Full FY2025 corpus totals were not independently rerun; the 1.9 GB source archive remains excluded.

Every dossier points to the original JSONL SHA-256 and one-based line numbers. Original rows retain transaction/award keys, UEIs, CAGE codes, addresses, action dates, modifications, obligations and ceiling/outlay fields. Dossier compact rows preserve each matched action. No cumulative award value, ceiling or repeated outlay field is summed as payments. All amount arithmetic uses decimal values. Positive and negative obligations remain separate.

Designation additions were checked against archived dated OFAC notices. C06 requires two dates: 5 November 2018 Government-of-Iran identification and 21 September 2020 EO13382 designation, as described in Treasury release sm1130. Both predate the supplied transactions. This clarification was appended after evaluation; its exact original Jev state is preserved, not overwritten. This is not a complete history of every program, removal, authorization, or ownership-based restriction.

## Jev interface, budget and controls

The verified interface is `POST https://api.typesafe.ai/v1/systemone`, pinned `jev-1.13.0`, with state plus typed questions. It does not return arbitrary explanatory prose or unconstrained extracted quotations. We therefore supplied bounded choices and exact source passages, preserving both candidate selection and evidence references. This is source-grounded classification/extraction from supplied options, not an independent discovery or blind assessment.

Current official model documentation gives $0.042 per million input tokens, free outputs, and 64,000 input tokens maximum. A full-context call is $0.002688; the adapter reserves $0.003 before every network attempt. A separate SQLite ledger enforces a $9 internal total cap against the $10 authorization ceiling. Request JSON is capped at 16,000 bytes; all prepared requests passed. Failed or uncertain calls retain full reservations. No automatic retries, redirect following, alternate paid providers, credential creation or TLS bypass. Keys are read only from supported environment variables and are never written to requests or logs.

The adapter reuses the transactional reserve/cache/settlement logic in `code/ati/pipeline.py`, changing only the provider set, experiment namespace, cap, output ledger, current-price gate and typed-choice validation. It does not run disabled Alberta scripts or reuse their ledger. SQLite and exported JSON contain the same 21 successful attempts; the unsuccessful *quality control* was a successful billed API call, fully included. Total conservative accounting is 2,443 microdollars ($0.002443), rounded up per call from observed input usage. This is a reproducible usage estimate rather than an invoice. No uncertain network costs remain.

Eight offline tests cover reservation cap, non-Jev rejection, retained timeout costs and blocked retry, caching and rounding, invalid usage, typed-choice validation, exact-passage rejection and redirect refusal. Synthetic control v1 stopped at a compound short-interval judgment (0.54, below the preset 0.8 positive threshold). The literal-record replacement scored 0.96; the other five atomic controls passed their 0.2 negative thresholds. Original successful identical calls were served from the ledger cache, not billed again. Failed v1 evidence is retained. These six fixtures do not estimate a model accuracy rate.

Thirteen real dossier evaluations followed. Model activity labels are not final case classifications: the identity gate prevents applying unrelated recipients' obligations to designated entities. `jev/human-overrides.json` preserves corrections/clarifications. All raw API responses, model usage, exact prompts, options and probabilities are retained. Those probabilities and confidence fields are not calibrated probabilities of identity or wrongdoing.

## Stage 2 scope and validation

The budget was frozen at at most three supported original candidates and five validated names each. Only NAI met the identity threshold; five names were selected from the original 11 December 2023 Treasury notice's same designation group. Jev selected exact passage P1 for all five. Code checked literal passage equality, offsets, names and original OFAC records; a human review retained the disjunctive owned/controlled/acting-on-behalf language. Neither direct NAI ownership, exact percentages, aliases nor intermediary roles were inferred. Cyprus NAI Logistics Limited is separate from the Dutch B.V.

OFAC FAQs 398 and 401, dated 11 August 2020 and 13 August 2014 respectively, are archived. Control or association does not alone establish automatic coverage under the 50% rule; ownership aggregation requires evidence. Here the five names are separately designated as of 11 December 2023, so no ownership-derived coverage is claimed. No earlier ownership dates or percentages have been established.

The search cap was implemented as one contracts page and one IDV page per validated name, 20 rows each, within FY2024–FY2025. All ten queries returned zero results and no next page. A mixed award-type request failed schema validation (HTTP 422); its error and request are retained. The corrected separated requests did not broaden the name, date or total-row budget. There were no access/rate failures. Nulls are query-specific, not absence findings across all records. No full corpus rerun or extra seed expansion took place.

## Reproduction commands

From repository root:

```sh
python -m unittest discover -s research/2026-10-07/sanctions-contract-pilot/scripts -p 'test_*.py' -v
python research/2026-10-07/sanctions-contract-pilot/baseline/sanctions-screen-evidence-2026-09-18/check_screen.py
python research/2026-10-07/sanctions-contract-pilot/scripts/verify_final.py
```

`build_dossiers.py` documents original subset checks and compact construction; exact evaluated states remain in request files. `report.py` regenerates current reports without calls. `nai_history.py` documents the bounded official child-history retrieval and reuses existing cached records. `evaluate.py` and `expand.py` preserve paid-call procedures, but `jev/COMPLETE` now disables further live calls. Do not reset or replace the ledger to replay. New research would need a separate explicit scope and preserved cumulative accounting.

The compact chat bundle excludes large raw archives and full HTML snapshots. The repository retains all recovered original archives, raw public responses, source manifests, prompts, responses, SQLite ledger, readable report and code. No confidential credential is included. Underlying purchasing instruments, invoices, payment records, specific licenses and ownership registries remain unobtained; their absence is an evidence limit rather than proof of illegality or legality.
