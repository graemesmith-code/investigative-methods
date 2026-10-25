# Recovery Stage 1 method and limits

## What is being reproduced

The three input archive hashes are identical to the original authorized snapshots. Twelve recovered helpers and multiple regenerated data products match their original retained hashes exactly; `audit/schema-recovery-results.json` names those proven matches. The lost main native screening script could not be recovered completely. The new core is explicitly versioned and must not be described as the same original frozen 13,267-row register.

The main implementation uses the exact recovered Round3 lexicon, with a transparent wrapper adding institutional aliases, the full ASIMOV program name, and punctuation-boundary repairs. The tokenizer preserves ROE/RAI/RTA as whole tokens, preserves V&V, IV&V, DOT&E and 3000.09, and splits arbitrary compounds such as AI.Reverie and SUSTAINMENT&RELIABILITY. Tests cover required lexicon membership, short-token false positives, known positives and the CaTE correction. A/B/C/D tags overlap and are preliminary, never verified program counts.

## Scan units and identity

- Every normalized JSONL row is read to end-of-stream and gzip CRC verification. Physical appearances are counted separately from unique transactions/awards and source-record identities.
- Contract and assistance records join only through exact generated award and transaction keys. Parent identifiers remain part of contract keys.
- SBIR identifiers remove punctuation only. A financial join requires a unique matching DoD PIID/FAIN; a supplied matching UEI is preferred. Ambiguous joins are not made. A unique PIID join lacking independent recipient validation is explicitly labeled. The mandatory post-scan identity review quarantines all 281 source appearances with explicit 12-character UEIs contradicting the financial recipient. Their descriptive leads remain separately keyed; their potential financial links are retained but no money is attributed. Legacy DUNS-format differences are not mislabeled UEI conflicts. A contradiction does not itself adjudicate novation, subsidiaries or historical identity.
- First-tier subawards have their own `SUBAWARD:` source-record keys, with the parent key separately retained. Their amounts and parent obligations are not attributed to the subrecipient. This deliberately differs from the old native register, which could surface a parent award from a subaward-only hit. The recovered original performer universe separately retains its original role-specific semantics.
- Opportunities merge by OpportunityID, including the duplicate selected-source representation. An opportunity is not a funded award. Other context documents retain source identities and are not treated as financial awards.
- Mirror Parquet files are not new financial or narrative observations. A separate exhaustive mirror/projection audit checks row equivalence; Grants.gov's flattened selected-source Parquet is a documented projection, not byte-identical JSON. The exact-deduplicated SBIR table is checked against the source row set. The unique transaction index is checked against all ledger keys; unreviewed SBIR link suggestions are not accepted as financial join authority.
- Raw transaction and subaward tables are screened for full primary/transaction descriptions, funding-opportunity goals, and institutional office/agency fields. All raw rows are accounted. Column selection is explicit in the scan log. Raw source fields are not all independent observations: repeated descriptions collapse in the unique register, but their distinct source appearances remain in provenance.
- General agency text such as Department of Defense cannot supply the domain half of an unrelated safety/ethics match. Explicit institutional anchors can independently select a lead. Every available full title/description is retained, with no character truncation. A source field that is itself an excerpt is not represented as a complete original PDF or website.

## Interpretive controls

Normative/legal concepts are paired with autonomy/AI/weapons-domain terms, or caught through direct program names. Category A includes benchmarks, evaluation and training, not only onboard governors. Common-word program aliases (for example MAGNET, GEARS, RESPECT, CAMP or RAIDER) remain leads with collision warnings. Broad reliability and institutional-only hits are separately prioritized. Funding-opportunity goals are generic solicitation scope, not proof that an individual award performs all described work; goals-only category support is explicitly flagged and excluded from the substantive high-priority A/B queue.

CaTE remains C. Quasistatics' key loading is not proof of positive target-specific human authorization; a preliminary B retrieval hit is not a confirmed B mechanism. C reliability is not a law-of-war restraint. Fiscal/calendar windows and currently recorded end dates are not evidence of current funded activity by themselves.

## Monetary rules

Only unique `financial_actions` rows supply archive obligation sums. Every signed value, including deobligations, is preserved as integer cents. Award snapshots, options, ceilings, outlays, SBIR reported award amounts and subaward amounts are never added. IDV parent ceilings are not combined with child orders. A missing financial join is null, not zero.

All totals mean **net obligations within acquired transactions**, not complete award histories, dedicated safeguards spending, or guaranteed lower bounds. Acquisition filters may exclude old positive, negative or zero actions. Internal exact-key agreement establishes consistency within this corpus, not completeness against current federal records. See `FINANCIAL-SCOPE-ADDENDUM.md` and its exact source-request evidence.

FY2019–2026 spans 2018-10-01 through 2026-09-30; FY2024–2026 starts 2023-10-01. CY columns use action dates starting January 1. The acquired ledger ends September 2026; archive retrieval time does not extend its coverage into October. End dates are selected by latest action date, then last-modified date; tied conflicting fields remain null with alternatives. Source date histories are retained in their compressed sidecar.

## Live/known-seed overlay

The 111 independently reviewed live financial identities pinned to commit `a0ed4b2c24083287120c1bb8523652f959ffd1b6` are explicitly unioned with lexical candidates. Six are prototype OTs; one standard record is a parent IDV. A seed-only row is not retroactively called a lexical hit. Machine categories, live scope review and live financial values remain separate. Archive and live dollars must never be added. `audit/live-seed-crosswalk.json` reports exact presence in the full ledger and lexical register.

## Reproduction

Materialize the three authorized Library inputs using the current Library workflow, preserving identities; do not copy credentials or guess download URLs. In a fresh output root with the supplied `code/`, use Python 3.12 and PyArrow 26.0.0 for Parquet. The main stages are:

```text
python code/extract_recovery_inputs.py --root ROOT --archives ARCHIVE1 ARCHIVE2 ARCHIVE3
python code/enrich_source_dates.py
python code/compress_date_enrichment.py
python code/validate_date_enrichment.py
python code/validate_description_completeness.py
python code/extract_additional_source_narratives.py
python code/normalize_extra_narratives.py
python code/build_performer_continuation_universe.py
python code/validate_performer_universe.py
python code/test_recovery_lexicon.py
python code/recovery_screen.py --root ROOT
python code/supplement_acquisition_program_fields.py --root ROOT
python code/quarantine_sbir_identity_conflicts.py --root ROOT
python code/export_recovery.py --root ROOT
```

Recovered helper paths derive ROOT from their containing `code/` directory. The main screener refuses to overwrite an existing work database. The exact live overlay is an input, not a new live query. Complete logs and any explicit supplement/QA commands are inventoried in the final manifest. Runtime timestamps legitimately differ between reruns; scientific data hashes are compared where deterministic. A partial initial recovery run was deliberately stopped before completion to repair metadata-domain pairing; its working files are not final evidence.

An independent code review also caught that the selected `dod_acquisition_program_description` column was not part of the base narrative extractor. The explicit supplement screens every occurrence and preserves every distinct value/frequency before export. The observed lexical hit is LGM-35A SENTINEL, which is flagged as a program-name collision—not asserted to be a safeguard program. Projection hashes refer to the declared screened columns, not an unmodified full Parquet row; exact source-file hashes and physical row locators permit reproduction.

The base run also stopped at an overstrict count assertion on the SBIR deduplicated table. Independent exhaustive proof shows it is exactly keep-first by stored `record_sha256`: 25,770 source appearances become 25,769 content records because one identical HQPHOTONICS record has two different raw locators. Both original appearances were already screened; no description was omitted. The resume branch verifies every reused file hash and exact database row count, reads both gzip sidecars through CRC verification, and resumes only wholly unprocessed streams. `audit/sbir-current-exact-dedup-proof-recovery-v1.json` preserves the proof. Source-row hashes in this package refer to normalized JSON-line bytes without terminal newline, not the source's separately stored `record_sha256` field.

## Inherited blindspots

This is a full scan of bounded public/unclassified input slices, not a census of all federal awards, every OTA, classified programs, non-DoD funders, or changes through the report cutoff. No absence inference is justified merely by a missing lexical hit, absent archive action, expired recorded end date, or unidentified parent/subaward relationship. Known positive calibration and the independent live overlay mitigate, but do not eliminate, those limitations.
