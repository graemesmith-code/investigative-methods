# Acquired transaction sums are not complete award histories

The old native register's label `entire_award_not_allocated_to_brake_work; subawards_not_added` could misleadingly imply a complete award history. Its intended allocation warning did not establish completeness. The recovered register replaces that interpretation with:

`acquired_transaction_sum_only; acquisition_filtered_history_may_be_incomplete; not_allocated_to_safeguard_work; subawards_not_added`

Every reported archive total is a signed net of unique acquired transactions in its labeled window. Missing positive, negative and zero actions are possible. These figures are neither complete award funding nor guaranteed lower bounds. No original transaction is changed to force agreement with live figures; archive and live values must never be added.

## Exact original acquisition filters

The preserved requests and acquisition documentation are pinned to commit `28e2a1a0eed040608b5fd16228763cce19de041d`, under `research/2026-10-16/future-warfare-investments/acquisition/`. `audit/source-filter-provenance.json` records the direct source URLs and verified Git blob/SHA-256 identities for all 12 exact copies.

- The transaction download route was `/api/v2/download/transactions/`, CSV, request limit 500,000, ordinarily 2018-10-01 through 2026-09-30.
- The broad contract slices used contract award types A/B/C/D and **awarding** Department of Defense, not all awards funded by DoD through other agencies.
- The capabilities slice used keywords: quantum, autonomous, unmanned, drone, hypersonic, electronic warfare, cyber, satellite, sensor, contested logistics.
- The R&D slice required PSC Service → A.
- Research assistance used types 02/03/04/05 and listings 12.300, 12.431, 12.800, 12.910, 12.630 and 12.615.
- The DARPA slice specified its awarding subtier. FY2019 and FY2026 supplementary requests retained the substantive capability/R&D filters but used single-fiscal-year windows.

The technical annex expressly treats these as bounded slices and says keyword semantics were not fully audited. Its capabilities download count (305,768) differed from a search-count result (324,990). That discrepancy alone does not prove which actions are missing or a particular per-action keyword mechanism. Do not turn an inferred acquisition explanation into a proven API behavior.

## Historical omissions already identified in independent live review

Before the runtime loss, independent FPDS review found historical omitted actions—not merely October reporting lag—on three exact parent-aware awards. The original immutable local ledger was not altered. The recovery independently retrieved all 19 historical XML response bodies with identical SHA-256 hashes, replayed 177 identities and 2,124 fields with zero errors, and reconciled the restored original ledger again. Verified FY2019–2026 comparisons are:

| Award key | Acquired actions | Live window actions | Acquired net USD | Live net USD | Difference USD |
|---|---:|---:|---:|---:|---:|
| CONT_AWD_FD01_9700_N0017814D7932_9700 | 70 | 72 | 9,674,146.79 | 9,724,146.79 | 50,000.00 |
| CONT_AWD_N0016422F3007_9700_N0017819D7763_9700 | 6 | 19 | 5,092,898.52 | 24,423,706.49 | 19,330,807.97 |
| CONT_AWD_N0042123F3004_9700_N0017819D7484_9700 | 3 | 53 | 2,217,125.03 | 27,836,455.94 | 25,619,330.91 |

All live-window actions in that review carried PSC R425, outside the PSC-A slice; retained local actions were from capabilities-keyword extracts. Missing records included older incremental-funding modifications. This is consistent with bounded acquisition, not proof of one specific keyword-matching mechanism. The lost native addendum itself is not claimed recovered byte-for-byte; any replayed primary evidence is separately identified in the recovery manifest.

The [independent recovered XML and reconciliation package](../independent-editor-history-recovery/new-history-reconciliation.json) contains the fresh recovery wrapper, exact historical response bodies, original/current hashes and the replay. Its same-window comparison is 79 acquired actions versus 144 live-window actions; 33 additional FD01 actions predate FY2019. All 65 omitted same-window actions are individually retained.

The new export's own SQL-to-register conservation checks establish only arithmetic consistency against acquired source rows. Even zero identity or amount conflicts cannot certify complete award histories, prove a program absent, or convert whole-award spending into safeguard-specific funding.
