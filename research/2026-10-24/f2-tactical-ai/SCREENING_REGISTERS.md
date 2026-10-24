# Inspectable screening registers

These files expose the machine-generated candidate lists behind the F2 screen. They are discovery outputs, not lists of verified AI weapons, investigated projects or proven procurement transitions. The main report separately identifies the cases reviewed in depth and the unresolved evidence questions.

## Direct files

- [Lane 1 tactical candidates, 384 rows](audit/lane1-tactical-candidates-384.csv). Awards combining AI or autonomy terms with weapons or contested-environment terms, with positive net obligations dated 2024 onward in the supplied archive. The [lossless JSON register](audit/lane1-tactical-combination-register.json) preserves the original structured fields.
- [Lane 1 first-observed-recipient cases, 65 rows](audit/lane1-first-observed-recipients-65.csv). A subset of those 384 awards. At least one linked recipient's earliest action across all 712,186 archive transactions falls on or after 1 January 2024. The 65 award cases involve 60 distinct qualifying entity keys. The CSV includes the matching recipient keys and earliest dates. This does not mean the company was founded in 2024 or first won a government contract then.
- [Lane 1 explicit Phase III candidates, 36 rows](audit/lane1-explicit-phase-iii-36.csv). A different subset drawn from the broader 89,838 candidate-award register: positive 2024-onward net obligations, an AI or autonomy keyword category, and a Phase III or Phase 3 match in an evidence description. Only six of the 36 overlap the 384 tactical candidates. These are textual screening hits, not individually verified SBIR Phase III transitions; technical predecessor lineage still requires evidence. The phrase may come from an older action, and matching uses the original stored evidence descriptions, capped at six per award.
- [Lane 2 high-scoring nonexact follow-ons, 92 rows](audit/lane2-high-scoring-nonexact-followons-92.csv). Candidates selected from 7,374 award keys represented by 18,741 recent transactions for broad-screen SBIR recipients. They have no exact PIID match in the SBIR corpus, a positive recent obligation sum and a representative description score of at least seven. This is a recipient-linked discovery list, not proof that the newer award continued the earlier SBIR technology.
- [The screening and joining scripts](code/README.md), including their input requirements and dependency order.

## The different denominators matter

Lane 1's four broad routes produced 89,838 award keys. Of those, 884 combined AI/autonomy and weapons/contested terms, and 384 had positive 2024-onward obligations. The 65 first-observed-recipient cases are within the 384. The 36 Phase III cases are selected independently from the broader register and must not be described as 36 of the 384. The overlap is six, not 36.

Lane 2's 92 cases come from a separate recipient-linked financial-description screen. Its 7,374 award-key denominator and 18,741 transaction denominator cannot be substituted for Lane 1's counts. A contract identifier, a full award key and an SBIR title/recipient key are also different units.

The Lane 2 score is three points for an AI term, four for a tactical term and three for a transition term. Thus a score of seven does not necessarily contain an AI term: tactical plus transition also scores seven. The export retains the matched categories so readers can distinguish these routes. Within each award, the original method chose the first maximum-scoring description encountered in the SQL result stream. The original query did not specify an ORDER BY; the export records the representative source row number and rerun order rather than implying a stronger tie-breaking guarantee. The positive funding test uses the sum of the linked recent transactions, not the value of that representative transaction.

## Dated reproduction addendum 24 October 2026

The full Lane 2 export is reconstructed by rerunning the published filter, not a byte-for-byte recovery of a preserved original 92-row list. All archive and extracted-input hashes matched, and the exact SBIR-to-financial join reproduced byte for byte. The recipient-linked intermediate did not reproduce its old hash: the broader nonexact PIID count is **2,834 in the rerun versus 2,809 in the original report**, and **9,006 versus 8,921** across all SBIR recipients. These discrepancies remain unresolved and are not silently replaced.

The unchanged final filter still yields **92**, with matching final controls of 18,741 transactions, 4,416,585 description characters and 7,374 award keys. No original 92-case membership file or membership hash was preserved, so matching totals do not prove identical historical membership. The number of membership differences is unknown. No flags were altered to force agreement. The [original and reconstructed audits](audit/lane2-reconstruction-comparison.json) are supplied side by side. The selected report dossiers rely on separately checked contracts and test sources; this export does not change those facts or promote new cases.

## Interpretation and provenance

All amounts retain integer cents as the authoritative calculation unit. Positive net obligations are not outlays, deliveries, contract ceilings or evidence that the whole award financed AI. Multiple contracts from one recipient are not automatically the same programme. Source coverage is selected FY2019–2026 material, with action dates through 30 September 2026, not a census of Pentagon spending.

These inspectable exports were regenerated deterministically from the same hash-verified source archives and original screening scripts. They add access to existing candidate rows, not new research or paid searches. Their audit files record predicates, counts, overlaps and source/output hashes. The original report's findings, funding evidence and historical grades are unchanged.

The published source archives' hashes identify the required inputs; the archives themselves are not redistributed here. See [source archive identities](audit/source-archives.json), [Lane 1 subset audit](audit/lane1-subset-audit.json), [Lane 2 export audit](audit/lane2-followon-export-audit.json) and [package checksums](SHA256SUMS).
