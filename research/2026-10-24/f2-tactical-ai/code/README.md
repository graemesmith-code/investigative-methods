# Reproducing the F2 screen

The scripts use Python 3 standard-library modules and SQLite with JSON functions. No API credential is required for the local screen. They do not download source archives or publish anything.

Create a fresh working directory and set the environment variable `F2_ROOT` to its absolute path. Place the normalized financial, SBIR and assistance gzip JSONL files in `data/normalized/`; place the seven contract descriptive slices in `data/descriptive_sources/`. Use the exact filenames and SHA-256 values in the adjacent audit directory. These hashes identify inputs; they are not downloadable public inputs or a claim that this package redistributes the source archives. Extract the 22 normalized JSONL files into data/normalized and the seven contract descriptive JSONL slices into data/descriptive_sources, without changing filenames. Create directories `data/normalized`, `data/descriptive_sources`, `lane1`, `lane2`, `lane3` and `lane5` before running. Do not run index-building scripts over an existing populated database; they preserve rather than delete old data.

Run these scripts in order from this code directory, with `F2_ROOT` exported:

1. `python lane1_build_index.py`
2. `python lane1_enrich_financial.py`
3. `python lane1_validate_cross_sources.py`
4. `python lane1_screen_financial.py`
5. `python lane1_summarize_screen.py`
6. `python lane1_transition_markers.py`
7. `python lane2_screen_sbir.py`
8. `python lane2_join_financial.py`
9. `python lane2_screen_followons.py`
10. `python lane3_screen.py`
11. `python lane5_screen.py`

Optional deterministic known-ID checks and the selected funding extract are supplied separately. Those are exact-ID follow-through, not broad discoveries. Full SQL schema is in `sqlite_schema.sql`.

The key monetary unit in machine registers is integer cents, not dollars. Aggregate by complete award key, including parent identifiers, not by short PIID alone. Negative modifications remain in the net sum. Description joins use exact transaction keys; duplicated descriptive source appearances do not create more financial actions.

The scripts produce large intermediate registers, including an intentionally broad 89,838-award recall set. Their output hashes are preserved in the audit; they are not 89,838 investigated AI programmes. The public narrower register contains 384 positive-recent tactical combinations. Final editorial decisions are in `audit/final-selection-register.csv` and are separate from scores.

The public source files' descriptions can be generic or incomplete. Nonempty description coverage does not imply equally informative content. Classification codes are broad. First observed in the selected archive is not a company's founding date. Recipient-level follow-on matches and DARPA-to-service flags are leads, not proven technical transitions.

Live USAspending and FPDS verification was read-only and selectively performed on final candidates; this repository supplies its returned IDs, selected fields, action arithmetic, source hashes and timestamps. It does not make hundreds of thousands of live API calls when reproducing the local screen.


## Export the inspectable candidate registers

The additional exports expose candidates from the existing screens. They do not rerun online research or validate individual technologies. Set `PUBLIC_PACKAGE` to this published package and retain the existing `F2_ROOT` work directory after the original build, enrichment and screening steps.

```bash
mkdir -p "$F2_ROOT/register-exports"
python "$PUBLIC_PACKAGE/code/recover_lane1_subsets.py" \
  --package "$PUBLIC_PACKAGE" \
  --out "$F2_ROOT/register-exports" \
  --financial "$F2_ROOT/data/normalized/financial_actions.jsonl.gz" \
  --candidates "$F2_ROOT/lane1/candidate_register.jsonl"
python "$PUBLIC_PACKAGE/code/export_lane2_followons.py" \
  "$F2_ROOT" "$F2_ROOT/register-exports"
```

The Lane 1 exporter verifies the original input hash, all 384 surviving rows and the 65/36 predicates. The full candidate register was reproduced byte for byte in this recovery. The Lane 2 exporter reproduces the documented 92-case filter and retains source row numbers, score categories, exact-cent sums and full award keys. Its intermediate recipient-join count differs from the historical audit, and no original 92-row membership hash exists. Read [the dated reproduction caveat](../SCREENING_REGISTERS.md#dated-reproduction-addendum-24-october-2026) before interpreting it as historical membership. The original query did not specify SQL ordering for equal-score representatives; the export discloses the regenerated order.

The scripts also write local diagnostic outputs. Only the explicitly listed final CSV/JSON exports and public audits are in this repository; the full recipient map and large joins are not published.
