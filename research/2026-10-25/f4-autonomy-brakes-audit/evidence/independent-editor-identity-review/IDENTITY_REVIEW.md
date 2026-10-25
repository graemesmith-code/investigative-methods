# Recipient-identity contradiction: selected-claim cross-check

**25 October 2026. Independent check of the 281-row recovery-review conflict list, snapshot SHA256 `8acaee4f35a853262ee0094d636aa80932baa190dcd87b826a4b3076e1634e9a`.**

## Result

- **Zero** conflicts intersect the 31 selected/adjacent reviewed-case rows.
- **One** intersects the 58 technical crosswalk rows and the 111 live financial instruments: **SP470124P0068**, SBIR current physical row 3480, raw award-data row 6127.
- An additional normalized-PIID discovery comparison yields the same single intersection; no exact-key-only omission was found in these three reviewed sets.
- No selected A/B/C subtotal changes follow from this intersection. This is not a claim that all 281 joins are harmless or that every other entity join has been validated.

## Affected row and evidence

The SBIR record names Rapid Global Business Solutions Inc (RGBSI) Aerospace & Defense and explicitly supplies UEI **VFBVNNPZLKL5**. The acquired financial record for `CONT_AWD_SP470124P0068_9700_-NONE-_-NONE-` names RAPID GLOBAL BUSINESS SOLUTIONS, INC and supplies **DVB6AGJG7WZ7**. Both the original normalized SBIR row and the financial-actions stream were independently reread for this check. Similar names do not resolve the legal-entity contradiction.

The retained live award's own government description, however, identifies **SMALL BUSINESS INNOVATIVE RESEARCH PHASE I - L242-005-130 PREDICTING FUTURE DOD MATERIAL OBSOLESCENCE UNDER UNCERTAINTY**. This independently corroborates the project/topic against the SBIR obsolescence-risk proposal. The financial instrument's own reported obligation is **$99,767**. Its technical crosswalk disposition was “Outside autonomy-brakes scope,” and it was not in the selected money totals.

This is a useful distinction: a disputed recipient UEI does not erase the direct primary-award project description, but an exact project/PIID/source-hash match does not establish why the legal-entity UEIs differ. Possible explanations such as novation, affiliated entities, source error or identifier reuse are **not established** and must not be asserted as facts or wrongdoing.

## Required correction

1. Preserve the financial instrument and its own primary description/amount, independently of the SBIR recipient attribution.
2. Preserve the SBIR descriptive lead and mark its recipient link unresolved; do not silently attach its technical claims to a verified legal entity.
3. For the live row, an exclusion based on the primary obsolescence-research description may remain if the basis is stated explicitly. Replace a bare `excluded_after_technical_abstract_review` with a qualified disposition, for example: **“Outside selected scope on the primary award's obsolescence-research description; same-project SBIR proposal identified, recipient-UEI relationship unresolved.”** If the primary description is not used as the exclusion basis, the financial row's deeper technical scope must remain unverified rather than inheriting a confident exclusion from the conflicted entity join.
4. The 281-row wider screen must quarantine unsupported recipient/performer attribution without deleting the underlying source lead or assigning another award's money. Legacy DUNS differences are not themselves explicit UEI contradictions.
5. Distinguish hash types. For row3480, the conflict list's `source_row_sha256` (`23904c11…`) is a normalized-line hash; the original record's stored `record_sha256` (`d42fced8…`) is the provenance field used by the technical crosswalk. Their difference is not evidence of corruption. Label each precisely.

The earlier 58-row hash/physical-row verification remains valid as a **source-linkage** check; it was never sufficient proof of a recipient-identity join. Final editorial signoff should verify that the qualified disposition/caveat propagates into the actual integrated live inventory, technical crosswalk and source-join audit.

## Reproducibility and sources

`review_identity_intersections.py` snapshots the conflict-list bytes, compares the three pinned review tables, independently rereads the original SBIR and financial streams for the intersecting row, and records hashes. `identity-conflict-intersections.json` retains the exact affected rows and the new original-source checks. `conflict-identifiers-only.json` is a metadata-only copy of all 281 conflict rows, excluding full abstract bodies. The source review found 280 distinct conflicting financial keys and 68 machine-screen-selected keys; those broader screen selections are **not** the 31 reporter-selected monetary cases.

- [Pinned combined live inventory](https://github.com/graemesmith-code/investigative-methods/blob/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/combined-live-inventory.csv)
- [Pinned 58-row technical crosswalk](https://github.com/graemesmith-code/investigative-methods/blob/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/live-technical-scope-review.csv)
- [Pinned reviewed cases](https://github.com/graemesmith-code/investigative-methods/blob/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/reviewed-cases.csv)
- [Primary award endpoint](https://api.usaspending.gov/api/v2/awards/CONT_AWD_SP470124P0068_9700_-NONE-_-NONE-/), whose retained result is included in the [pinned full live record](https://github.com/graemesmith-code/investigative-methods/blob/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/evidence/live-award-register.json).
