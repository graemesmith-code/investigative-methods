# Bounded native EP search expansion, 15 November 2026

## Actual query scope and counts
Four lanes through EPO Linked Open EP Data SPARQL, using 2021-11-15..2026-11-15 publication dates inclusive:
1. Exact inventive CPC F41H7/005, no keyword filter:32 publications.
2. Inventive or additional CPC URI prefix F41, English title containing safe/inhibit/restrict/authoriz/authoris/collateral/control/autonom/identif/friend/target/prevent/abort/interlock/human:460 returned rows,459 publication identifiers. Duplicate title variant explains extra row.
3. Inventive or additional CPC prefix G05D1-, English title containing safe/inhibit/restrict/authoriz/authoris/collateral/weapon/military/abort/interlock/human/ethic:284 joined class rows,155 publications.
4. Inventive or additional CPC prefix F41A17-, no title keyword restriction:440 joined class rows,269 publications.
Union:803 publication identifiers across604 EP application identifiers. These are NOT803 relevant inventions, NOT604 patent families, NOT full text review counts. Corrections and grants/applications may be separate publications.

The first lane2 query selected class as output, hit LIMIT1000 and was truncated. Retained as diagnostic f41-safety-titles.json. Corrected query f41-distinct.sparql omits class from SELECT, returned460 rows and did not hit cap. Only corrected result enters ep-native-union.csv. Other lane results below respective caps.

Files contain exact queries, JSON responses and union metadata. API endpoint https://data.epo.org/linked-data/query via URL-encoded query parameter, Accept application/sparql-results+json. Tests were bounded occasional discovery requests, not sustained bulk harvesting.

## Important limits
Title terms are high-noise and low-recall proxies: safeguards may appear only in description/claims; 'safety' often describes industrial robotics or ordinary mechanical gun safeties. CPC prefixes omit relevant F42, B64, G06, H04 and other fields. Only English titles in selected lanes. Native EP data does not replace UK/Canada/other national-only or WO searches. Publication dates do not mean invention/priority dates, and old priorities may be relevant. API results depend on live service coverage and classification updates. Query exhaustion is not landscape completeness.

## Prioritized official XML downloads
Eight publications selected by title for checking: EP4599207A1, EP3915421A1, EP3942242A1, EP4025861A1, EP3745077B1, EP3726178B1, EP3882560B1, EP3882561B1. Exact linked representation URLs obtained through prioritized.sparql response, not guessed. download-log.json records final successes and failures. XML parsed to count description and claims sections, which are language sections rather than unique claims.

Confirmed distinctions:
- EP4599207A1 is an official metadata-only Euro-PCT stub, no description/claims; its B870 field points to WO2024074456, published2024-04-11. Web tool successfully read WO2024074456A1 on Google Patents, but direct local download returned a1103-byte blocker, not a full-text evidence copy. Do not upload that HTML as patent evidence.
- EP3942242A1 is a metadata-only stub pointing to WO2020186336,2020-09-24.
- EP4025861A1 is a metadata-only stub pointing to WO2021044113,2021-03-11.
- EP3915421A1 contains actual description/claims: Rade Tecnologías authorization of personal weapon users, not demonstrated AI safeguard. Useful exclusion/control example.
- EP3745077B1 contains actual multilingual description/claims: shooting-range weapon interlock; not automatically an AI civilian-protection safeguard.
- EP3726178B1 contains actual multilingual description/claims: networked military-unit cross-vehicle sensor/weapon control. Inspected English claims are not themselves proof of an ethical guardrail.
- Final two friend/foe records are candidates for later substantive assessment; acquisition alone is not claim review.

This pass improves EP-native candidate coverage and provides an official-text route. It does not justify claiming all available documents have been collected.

## Official references
https://www.epo.org/en/searching-for-patents/data/linked-open-data
https://link.epo.org/web/linked_open_ep_data_user_guide_en.pdf
https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/data
https://patents.google.com/patent/WO2024074456A1/en

## Preserved evidence archive
Raw query responses, union metadata, eight official XML files, download log and SHA-256 manifest: https://drive.google.com/file/d/1of3derJLxgnSpzp15O3W-Geo-WQCTNzq/view . Archive preserves the explicitly labelled truncated diagnostic separately from the corrected final query output. It excludes the failed Google HTML response.
