# Patent search coverage and merged denominator

The initial second-lane pass below is a historical input. It has been reconciled with the independently reviewed native register: **28 input rows, five exact-publication overlaps →23 distinct publications; six cluster overlaps →19 reporting clusters**. All input identities/status dispositions are preserved in the Drive provenance package. These clusters are reporting groups, not legal-equivalence or deployment findings.

Targeted official-source work subsequently retrieved Kongsberg, BAE and Anduril grant PDFs from USPTO’s public image endpoint and visually checked selected covers/claims. Anduril’s appended 14 October 2025 Certificate of Correction resolves the specific earlier wording ambiguity. This changes document-access/claim verification, not current legal-status or ownership-chain verification. All current-status limits remain row-specific; a failed PDF request is not a status-register attempt. Source snapshot hashes and selected rendered-page comparisons are retained on Drive; whole-PDF byte variation was not assigned an unverified cause.

## Initial second-lane search and limits

Cutoff: 25 October 2026. This file distinguishes search coverage from validated findings. The parent is the sole paid Exa spender. Exa queries 23–40 and 75–92 were issued by the parent; the reporter read their saved results, then checked promoted documents using free public retrieval. Query result counts measure returned results, not a count of a company's patents or a complete patent universe. Broad relevance search can return a different owner, an old publication, a civilian use, or a patent with no restraint claim.

The CSV `patent-assignee-search-coverage.csv` records the exact queries, result counts and adjudication notes. It covers nineteen names when Boeing and Aurora are listed separately; the original directive groups them together. Raytheon/RTX are treated as an assignee group, not presumed legal identity of every subsidiary.

The reporting pass also searched combined F41G/F42B/F42C/G05D1/B64U class terminology with restraint words (human-in-the-loop, abort, interlock, geofence, keep-out, confidence threshold, non-combatant) in ordinary web discovery. This was not a native CPC database export. The documented free query included:

`site:patents.google.com ("F41G" OR "F42B" OR "F42C" OR "G05D1" OR "B64U") ("Allen Control Systems" OR "Shield AI") ("safe" OR "abort" OR "interlock")`

The classifications of retained documents were read on their publication pages; relevant safety architecture may occur outside the requested classes. Kongsberg's clear human-authorization disclosure, for example, includes F41A/F41H. No CPC search result has been treated as proof of deployed functionality.

## Database routes actually attempted

- Google Patents: public pages, metadata, claim text, family links and selected reproduced grant PDF were read. This is the substantive patent-text route used here. No attempt to exhaust Google Patents' entire index is claimed.
- USPTO: publication and PatentCenter/Assignment links were identified on Google pages; USPTO guidance on patent rights was read. No authoritative USPTO prosecution-history or chain-of-title audit was completed. At that checkpoint Anduril’s wording was provisional because the reproduced grant PDF was inconsistent; the subsequent official correction certificate resolves that specific issue, as recorded above. Current status and ownership remain unverified.
- EPO/Espacenet: official register, Espacenet and publication-server routes were attempted for BAE's EP family. Those exact-document accesses failed in this environment. EP4025861A1's public reproduced text/metadata and family link were verified through Google Patents. Its status is not represented as independently certified by the EPO.
- WIPO/PCT: WO2025019462A1, WO2024074456A1 and WO2023167712A2 were checked through Google Patents' public reproductions. Direct PatentScope access for WO2025019462 returned 403. No circumvention or authenticated account was used. A WO international publication is not a worldwide patent grant.

The initial second-lane `patent-safeguards-register.csv` had 16 publication records representing 13 families/comparators; the current combined register is 23 publications / 19 reporting clusters. Three family-member rows are expressly marked not to count as independent inventions. The thirteen representatives include one explicitly civilian delivery comparator and general aerospace/vehicle assurance. Do not publish 16 as 16 military weapon brakes, or 13 as 13 deployed safeguards. Patent-source verification hashes identify retrieved rendered documents, not official status certificates or immutable patent-office files.

## Negative finding discipline

For Shield AI and Allen Control Systems the searches did not yield a verified in-window patent to promote in this bounded pass. This says nothing definitive about unpublished applications, defense secrecy, licensed technology, technical safeguards without patents, alternative assignee names, or patents omitted by relevance ranking. The same caution applies to all screened names without a promoted patent.

Observed false associations were retained in adjudication notes: NASA geographic containment returned under ShieldAI/Northrop/GeneralAtomics searches; Breault electronic safe-and-arm under AeroVironment/Elbit/IAI; Toyota monitoring under Boeing/Aurora. The exact document owner and publication date control, not the words in the query. Older MBDA/Raytheon examples were not promoted as 2022–26 publications.
