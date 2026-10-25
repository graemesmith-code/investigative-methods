# Identity linkage check for 58 SBIR technical-scope rows

**One explicit recipient-UEI conflict was independently confirmed: SP470124P0068.** The other 57 rows have the source’s explicit UEI present in the complete archived financial recipient set for a unique full award key with that PIID, and the same UEI in the cached live USAspending prime-recipient record. This supports the 57 content associations at the entity/award-identifier level; it does not independently validate statements of work, test results, deployment or current program status.

Deliverables: [all 58 linkage rows](technical-58-identity-linkage-audit.csv) and [detailed evidence/receipts](technical-58-identity-linkage-audit.json). The technical-scope CSV now carries a separate identity-status column. No financial record, dollar total or primary/secondary category was changed by this review.

## Confirmed conflict

| Field | Archived SBIR lead | Archived financial and cached live prime |
|---|---|---|
| PIID | SP4701-24-P-0068 | SP470124P0068 |
| Entity name | Rapid Global Business Solutions Inc (RGBSI) Aerospace & Defense | RAPID GLOBAL BUSINESS SOLUTIONS, INC |
| Explicit recipient UEI | VFBVNNPZLKL5 | DVB6AGJG7WZ7 |
| Agency/parent scope | DoD / Defense Logistics Agency; no parent supplied in this SBIR row | CONT_AWD_SP470124P0068_9700_-NONE-_-NONE- |
| Source locator | sbir_current.jsonl.gz physical row 3480 | Full financial history and cached USAspending award response |

The SBIR description concerns material-obsolescence forecasting and was outside the weapons-brakes scope **as a SBIR lead**. The identity conflict means that exclusion cannot determine the scope of the financial award. Similar legal names, shared PIID or a matching source-content hash do not resolve the disagreement. No novation, subsidiary, corporate lineage or agency-error explanation is asserted.

The stored original SBIR source-record SHA-256 is `d42fced8a922eee4e5c905ef82b1601df13dfa819b6c9dfec9763a08910bf4e7`; its original source-snapshot SHA-256 is `05af2f39171d08aa7ab4a071549e663e159f41d2092f7bda8428cd68b22b3cfe`. The cached live award response SHA-256 is `909089e6ea1f49e240b710aad0b0573f45ae68f9f2dac0e293a9431d2f6da480` and was rehashed before reading recipient identity. Both financial and live recipient sets exclude the SBIR UEI in this check.

## Method and exact denominator

1. Re-read all **25,770 physical rows** of the accessible `sbir_current.jsonl.gz` file, recovering the exact 58 physical rows used by the technical review. This file is one part of the broader reported SBIR corpus; 25,770 is not represented as the 44,584-row total. All 58 contract identifiers and record hashes matched the investigator-provided technical subset.
2. Scan all **712,186 physical rows** of `financial_actions.jsonl.gz`. For every matching PIID, retain every full award key, every legal name, all 12-character UEI-shaped recipient entity keys, and nine-digit DUNS separately across the entire history. No first-row recipient shortcut was used. Every one of these 58 PIIDs maps to a unique financial full award key in this input.
3. Resolve all matching records from the frozen `live-award-register.json` snapshot to cached raw USAspending responses. Rehash each response against its recorded SHA-256; read the explicit **prime** recipient UEI, legal name, awarding agency, parent award and parent-recipient UEI separately. Parent-recipient identity was not substituted for the prime.
4. Compare explicit source UEIs with **all** archived financial recipient UEIs and cached live prime-recipient UEIs. DUNS differences were never treated as UEI conflicts, and a nine-digit key was never relabeled as a UEI. No fuzzy name merge or entity inference from PIID alone was used.

Scope and parent/agency fields are retained in the audit JSON and CSV rather than assumed from short identifiers. The technical subset’s source URL is the general SBIR awards page; the exact archived row and record hash identify the specific source content.

## Input receipts

| Input | SHA-256 |
|---|---|
| sbir_current.jsonl.gz compressed bytes | 523734ebbb86f656ed64c96bc821baf370a9cb2294ac114f46f46ba0ea798940 |
| financial_actions.jsonl.gz compressed bytes | 366c6294aa7d703e37affcab94ad835876943e1d6d6a5565867d5a14728e19e5 |
| f4-live-technical-matches.json | b32a46afacd985161328794350f398450a7f318351662213e0bd17cf16e3a9b1 |
| live-award-register.json snapshot used | ce38c01a18fcb96df5c220f9a163a787200a857a24c18f0e14a0512ec726c481 |

The per-row JSON includes financial physical-row locators and verified live-response hashes. Source files and caches remained private; no addresses, personal compensation data or full third-party bodies are included. This audit required no new API calls or expenditure. The main audit owns any resulting financial-scope disposition and publication regeneration.

## Financial-scope and hash-domain clarification

SP470124P0068’s own primary award description identifies SBIR PhaseI topic L242-005-130, material-obsolescence prediction under uncertainty; the $99,767 amount remains its financial record. Exclusion from selected safeguards totals can rest independently on that primary description. The unresolved SBIR recipient relationship is not claimed resolved.

Normalized JSONL line3480 without its line terminator has SHA256 `23904c11e58ae794e168bfd7255d0938fc384e300ebb103d4006e24352fe625d`. The record’s stored original source-record hash is `d42fced8a922eee4e5c905ef82b1601df13dfa819b6c9dfec9763a08910bf4e7`. These refer to different byte domains, not a content mismatch. Both fields are retained in the reproducible audit.
