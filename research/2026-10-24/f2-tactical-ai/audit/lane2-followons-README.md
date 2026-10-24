# Lane 2: 92 reconstructed follow-on screening candidates

- [Spreadsheet-ready CSV](lane2-high-scoring-nonexact-followons-92.csv)
- [Lossless JSON with full descriptions and joins](lane2-high-scoring-nonexact-followons-92.json)
- [Export definition, checks and hashes](lane2-followon-export-audit.json)
- [Original versus reconstructed audit](lane2-reconstruction-comparison.json)
- [Portable export script](../code/export_lane2_followons.py)

These are 92 screening candidates, not 92 verified AI weapons or proven SBIR transitions. They were reconstructed from the original, hash-verified October 16 archive using the published filter. They are not a recovered copy of an independently preserved original 92-row file.

The filter starts with 18,741 transactions dated January 1, 2024 onward from recipients linked to the broad SBIR screen. They group into 7,374 complete award keys. A candidate has a non-exact normalized SBIR PIID, a maximum description score of at least 7, and positive net obligations in that transaction cohort. Score components are AI terms (3), tactical terms (4), and transition terms (3). Tactical plus transition language can pass without any AI term.

The CSV and JSON retain full award keys, exact integer-cent obligation aggregates, representative descriptions, all available descriptions, score components and recipient/SBIR join fields. Negative modifications remain in the net amount. This amount is not an award ceiling, outlay, all-time award total, or newly checked current obligation. Recipient matches are leads, not technical lineage.

The original script selected the first encountered highest-scoring transaction as representative, with no explicit SQL ORDER BY. Stable rank ties retain the regenerated award-stream order. Source transaction row numbers and award-stream order are included so users can see that choice.

## Recovery caveat

All source archive and extracted-input hashes matched. The exact-PIID join file was reproduced byte for byte. The reconstructed recipient-join file did not match its old byte hash, however: broad-recipient non-exact PIIDs are 2,834 rather than the earlier 2,809; across all SBIR recipients they are 9,006 rather than 8,921. These discrepancies remain disclosed and unresolved, not silently corrected.

The unmodified final filter still returns 92, and the final description-screen controls match: 18,741 transactions, 4,416,585 description characters and 7,374 award keys. But no original 92-row membership file or membership hash survives, so equal counts do not prove identical membership. The number of historical membership differences cannot be established. Original and reconstructed audits are supplied side by side. No flags were changed to force the count.
