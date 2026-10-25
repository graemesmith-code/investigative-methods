# Recovered historical-action evidence and new reconciliation

This is a new recovery package, not the original lost editor integration supplement or Stage1 addendum.

All 19 primary FPDS XML pages were re-read through their exact URLs recorded in the pinned a0ed4b2 action export. **Every recovered body has exactly the historical SHA256 recorded in that public export.** Thus these primary response bytes really were recovered identically, even though their local wrapper/receipt files are new. Current recovery timestamps are separate from original source retrieval dates.

The new XML parser verifies all 177 full action identities and 2,124 fields against the retained export. A separate new reconciliation rereads the restored original 712,186-row financial-actions source. All 79 shared acquired actions agree on dates and money; the same FY2019–FY2026 window has 144 live actions, leaving 65 missing from the acquired history. Results reproduce the previous differences:

- FD01 / N0017814D7932: 70 acquired vs 72 live-window actions; $50,000 difference. The two omitted actions are mod32 zero and mod63 +$50,000.
- N0016422F3007 / N0017819D7763: six vs19; $19,330,807.97 difference.
- N0042123F3004 / N0017819D7484: three vs53; $25,619,330.91 difference.

These are acquisition-filtered sums, not complete award histories. Old actions are missing, so release delay alone does not explain the gaps. The exact API per-action matching cause remains unproved. Missing deobligations are possible, so an acquired sum is not necessarily a lower bound. No selected safeguard case subtotal is changed by these three illustrative nonselected awards.

`new-history-reconciliation.json` preserves source gzip/export hashes, exact monetary results and all missing action identities. `acquired-three-award-actions.json` contains only the 79 relevant government financial rows, not the full original archive. `primary-response-recovery.json` records exact URLs, historical hashes and current recovery outcomes. The new replay scripts are retained; no paid calls were made. Prior published `acquisition-history-coverage.json` and `acquisition-history-missing-actions.csv` are also recovered without claiming they are the lost independent authored files.

Pinned retained sources:
- https://github.com/graemesmith-code/investigative-methods/blob/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/fpds-verified-actions.csv
- https://github.com/graemesmith-code/investigative-methods/blob/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/audit/acquisition-history-coverage.json
- https://github.com/graemesmith-code/investigative-methods/blob/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/acquisition-history-missing-actions.csv
