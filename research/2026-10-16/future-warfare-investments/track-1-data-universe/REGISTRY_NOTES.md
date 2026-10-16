# How the source registers fit together

Updated 16 October 2026.

## Counts and deduplication

The [consolidated register](SOURCE_REGISTER.csv) has **89 source entries**. It starts with the original 60 and adds **29 distinct entries**. These are editorial units for finding data, not 89 independent financial datasets or a claim to exhaustive coverage.

The two expansion passes supplied 38 rows: 26 research/bulk rows (19 proposed additions and seven refinements) and 12 overseas-security rows (11 proposed additions and one refinement). Both added DDTC Section 655 reports; that duplicate is merged under **FW-X06**, with **FW-OS06** retained as a contributing identifier. The eight refinement rows are folded into nine original entries because the GovInfo refinement affects both B08 and B12. They do not increase the source count.

The register uses **79 editorial source-family labels**, compared with 51 in the initial inventory. One new entry extends an existing civilian-security-budget family to State. Family labels group related holdings; they do not imply independent observations or statistical comparability.

The [change crosswalk](REGISTER_CHANGES.csv) preserves all 38 incoming identifiers and their canonical destinations. The original expansion working registers remain available as [research/bulk input](expanded_bulk_register.csv) and [overseas-security input](overseas_security_sources.csv). Their original NEW/AMEND labels describe the individual research pass before cross-inventory reconciliation.

## Access and verification

The [bulk-access register](BULK_ACCESS_REGISTER.csv) holds **37 expansion route entries** after merging the DDTC duplicate. It is a focused supplement, not an exhaustive list of every bulk route in the original corpus. It distinguishes complete small-file retrieval, bounded payload samples, official offers not downloaded, APIs, document collections, authentication, paid products and failures. A successful header or a small shard does not mean the complete dataset was downloaded.

Original entries not retested carry `BASELINE_ROUTE_NOT_REPROBED`; this does not mean a bulk route is unavailable. The first inventory's verification details remain attached. Later successful OSTI/NTRS samples improve specific access findings without proving all records or full texts are accessible. The DSIP topic-archive refinement does not establish that the separate SBIR awards API works. GovInfo's structured budget files do not make every budget PDF machine-readable.

Priority labels retain the source passes' original vocabularies (for example Core/Contextual/Limited-access and High/Reference). They are qualitative research priorities, not a unified numeric ranking. For collection decisions, use the overview and the actual access/coverage fields together.

## Historical coverage and joins

The requested main window begins in **September 2018**. The [published announcement extension](../history/README.md) adds 18,819 substantive paragraphs for 12 September 2018–11 September 2023; the original 10,000-row export remains unchanged. The [combined index](../history/combined_deduplicated_index.csv) contains 28,818 unique paragraph keys. Archive discovery is partial, 59 weekdays lack a recovered page, and the original export's oldest day is truncated at the page level. [Coverage details](../history/COVERAGE.md) explain why periods are not directly comparable.

Register coverage fields still describe source holdings rather than asserting completed ingestion of every listed dataset. Commerce Business Daily's 1996–2001 archive is optional earlier context, outside the requested main window.

Stable source IDs identify register entries. Award PIIDs, UEIs, CAGE codes, programme elements, project numbers, grant IDs, DOIs, report IDs and fund codes are potential joins, with different levels of reliability. Budget totals usually lack a universal award identifier. Name matches, duplicate portal views and publications acknowledging a large laboratory contract should not be treated as new awards.

Keep each financial measure and vintage: request, authority, obligation, outlay, expenditure, ceiling, export authorization, shipment and property value remain distinct. Changes in reporting thresholds, agency organisation, archive availability and award revisions affect longitudinal comparisons. Classified work, OTA ultimate performers and subcontract tiers remain substantial gaps.

[Return to Track 1](README.md)
