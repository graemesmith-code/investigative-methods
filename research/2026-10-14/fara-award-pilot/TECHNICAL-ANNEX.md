# Technical annex: FARA / federal awards pilot

**We had compared LDA and FARA; the recovered prior report does not document this award-recipient join. This pilot now performs it for the full recovered FY2025 US prime-contract archive and bounded Canadian records. It finds overlaps, not violations. Grants coverage remains incomplete.**

Prepared 14 October 2026. This annex records the completed pilot; sanitized findings are now published with user authorization. No third-party outreach occurred. No paid services, model/API billing, credentials changes or outreach. External spend: **$0**. The parked NAI investigation was not reopened or used as a recipient corpus.

## What the screen found

| Stage / unit | Denominator | Result |
|---|---:|---:|
| FARA registrant rows | 7,090 | 7,090 usable; 538 active in cached snapshot |
| FARA principal relationship rows | 17,765 | 17,750 usable; 821 active; 15 malformed/missing-date rows quarantined |
| FARA document catalogue rows | 154,309 | Discovery links only; not documents read |
| FY2025 US contract transactions | 6,639,176 | All seven archive members processed; no duplicate transaction IDs or date/type exclusions |
| US distinct nonblank raw recipient names | 101,379 | Same denominator as recovered OFAC audit; not a legal-entity count |
| US recipient name/identifier/address groups | 126,350 | 273 FARA candidate pairs: 168 registrant, 105 principal (200 normalized-exact, 73 weaker legal-form matches) |
| Candidate transaction screen | 6,639,176 transactions | 10,898 distinct candidate transactions, including historical and weak name matches |
| Active cached FARA candidate address pairs | 273 | 35: 26 registrant and 9 principal; 24 distinct role/registration/name/UEI keys |
| Direct name + building/city + time corroboration | 273 | 14 address groups, 79 actions, 37 award/IDV identifiers |
| Address-anchored legal name + stable recipient UEI bridge | 14 anchors | 21 address groups; **12 recipient/role/registration keys and 2,310 temporally overlapping actions** |
| Canadian OCL registration versions | 177,371 | 7,787 with active cached intervals; latest effective/posted date 2026-10-09 |
| FARA / Canadian lobbying exact-name version pairs | 177,371 OCL versions | 11,077 historical candidates; 22 active pairs |
| Canadian active name + address corroboration | 22 active pairs | 11 version pairs: three distinct names, four FARA role/registration keys |
| CanadaBuys 2026–27 contract-history rows | 2,083 | 1,888 distinct reference numbers; 1,531 distinct legal supplier names |
| FARA / CanadaBuys exact-name pairs | 2,083 history rows | 7 candidates across 4 source rows; **none has overlapping FARA dates** |
| Canadian lobbying / CanadaBuys name candidates | 2,083 history rows | 6,646 version pairs across 254 source rows |
| Canadian lobbying / CanadaBuys temporal candidates | 6,646 version pairs | 473; 112 also have address corroboration, across 48 distinct contract-history rows |
| Canadian funding disclosure rows | 218,466 | 22,004 associated with candidate registration versions saved; not a grant-payment comparison |
| Targeted US FY2025 grants name lookups | 3 names | Zero returned award rows; this is **not** a full grants negative |

The 12 corroborated US keys represent **11 FARA registrants and one named foreign principal**, Canadian Commercial Corporation. The registrants are Arnold & Porter Kaye Scholer, White & Case, Daniel J. Edelman, The Burson Group, ArentFox Schiff, Ruder Finn, Venable, Fleishman-Hillard, Nelson Mullins Riley & Scarborough, Hunton Andrews Kurth, and Rational 360. [Compact table](compact-candidates.csv) and [dossiers](DOSSIERS.md) preserve IDs, dates, role, reasons and discovery links.

The strongest direct Canadian active identity overlaps are The Porter O'Brien Agency Inc., Burke Consulting LLC, and Nuclear Waste Management Organization. NWMO appears separately as registrant and principal; those are two source relationships, not two organizations. Consultant-firm matches identify the firm itself. Its Canadian clients are not automatically FARA registrants, foreign principals or foreign controlled.

The directly corroborated US Canadian Commercial Corporation records use the old O'Connor Street building. The exact same legal name and UEI `FA38CTVQM319` bridges to the other address records in this archive, producing 2,184 temporally overlapping actions for that recipient. This is a transparent derived crosswalk: **FARA itself supplies no UEI**. The 2,310 total counts actions, including modifications, zero obligations and deobligations, rather than payments or new awards.

## Inputs recovered before new retrieval

All three supplied FARA CSVs and both OFAC ZIPs were already in the project. The OFAC ZIPs contain sanctions data and a screened subset, not the full USAspending corpus. The saved OFAC audit reports 6,639,176 FY2025 actions and 101,379 recipient names, but retains only 153 screened candidate transactions. Neither ZIP contains grants or all award years.

The specified baseline commit `b316096e140175f81838cd5028eb2d0b7a59fa28` and prior branch were absent from this checkout. Its REPORT and ANNEX were recovered from the public repository at that exact commit and saved under `evidence/`. They describe the LDA/FARA comparison, not the requested award join. This finding is limited to the recovered report, annex and current checkout; no assertion is made about unseen work elsewhere.

The necessary full US archive was therefore retrieved from the exact saved official URL. It is 1,914,255,016 bytes and reproduces SHA-256 `792f6b3ee67afd4d4e9eb7f3463a083f80efaf13279a7a1bfaba6fecfd6443da`. Its seven filenames are dated 2026-09-07; official listing URL is dated 2026-09-06 and HTTP Last-Modified is 2026-09-14. All these dates are retained in `evidence/prior-ofac-contract-source.json`; none is silently treated as an award date.

Rabbit2 SYS-0120 / AP-0121 / MAP-00145 establishes the Canadian federal lobbying route. Rabbit5's visible Canadian procurement entries were provincial; they were not assumed to be a federal mapping. Official OCL and CanadaBuys direct files supplied by the parallel source researcher were checked and retrieved. The OCL dictionary was accessible here and verifies registration types, version IDs, effective/end dates and funding fields.

## Matching and time rules

Registrants and principals are independent source roles. A principal row represents an agent relationship, not a unique principal entity or necessarily a foreign government. The source name and all dates are retained. Historical and active results stay separate. “Active” means registration date on/before **2026-10-06**, and no termination or termination after that date, in the supplied cached FARA file; it does not certify live status on 14 October. All 821 active principal rows also attach to active registrants in this snapshot. Exact award action dates are compared with the recorded half-open registration intervals. Termination-day actions are conservatively excluded.

Names use Unicode normalization, case folding and punctuation normalization. Terminal legal-form removal is a distinct weaker candidate pass. No fuzzy, brand, parent, affiliate or beneficial-owner matching is performed. Business-name aliases are preserved but not used as identity evidence. Generic Canadian supplier placeholders such as `None` are removed before matching. Fifteen malformed FARA principal rows are preserved in [EXCLUSIONS.json](EXCLUSIONS.json), without guessing repairs.

The second pass permits only controlled postal abbreviations and building-level address equality, with matching city and state where supplied. Suite differences remain visible. A stable recipient UEI is carried only from an address-corroborated anchor to the exact same legal name and UEI. It never links an affiliate or parent automatically. Canadian legal, standardized and operating supplier names are discovery fields, not interchangeable legal identities; the source field and full supplier record are retained. Canadian lobbying matching uses English entity names; French-only names can be missed.

Counterexamples matter. Patriot Strategies is an active exact-name temporal candidate, but its FARA and award addresses differ, so it was not promoted. Lighthouse Public Affairs has different US/Canadian geography and remains a collision risk. Stark Aerospace's FARA relationship starts after the FY2025 contract period; this prevents a contemporaneous overlap claim despite the exact name. The weaker Rolls-Royce Inc./Corporation and FTI LLP/Inc. matches remain name candidates. No name-only candidate is counted as a verified identity.

## Disclosure comparisons and remaining gaps

X04's original test requires the actual LD-1 declaration, actual FARA Exhibit A ownership/control facts, the same legal client, dates and applicable threshold. X06 requires an itemized foreign-principal campaign-financing record and an exact ad/creative/placement bridge. A federal award overlap supplies neither test. Contract obligations are not campaign money or receipts.

The independent legal review identifies the appropriate next US record as the actual dated offer/SAM immediate/highest-level owner representation, where applicable, rather than a blanket FARA prohibition. Applicable DFARS, award-specific lobbying clauses/SF-LLL, and grants/program rules need their own dated scope. These records were not obtained. See [FAR 52.204-17](https://www.acquisition.gov/far/52.204-17), [DOJ FARA FAQ](https://www.justice.gov/nsd-fara/frequently-asked-questions), and the dossier-specific missing evidence. No inaccessible disclosure is described as absent.

For Canada, procurement contracts are excluded from lobbying government-funding disclosures. A genuine comparison needs actual grants/nonrepayable contributions **received**, matched to the registration's completed financial year and amendments; award value alone is insufficient. Consultant contract-award lobbying and in-house activities also have different scope. See [OCL registry](https://lobbycanada.gc.ca/app/secure/ocl/lrs/do/guest) and [Lobbying Act](https://laws-lois.justice.gc.ca/eng/acts/L-12.4/FullText.html). A consultant firm's unrelated FARA engagement does not establish control of its Canadian client.

Exact blockers and limits:

- Canadian TBS all-federal contracts and grants files returned HTTP 403. This is an access gap, not zero recipients or missing disclosures.
- Four attempted original FARA PDFs returned HTTP 403. Bulk rows and catalogue links are evidence; the PDFs were not read, and no ownership/campaign conclusions are promoted.
- US grants were limited to three saved FY2025 award-name searches: Canadian Commercial Corporation, Patriot Strategies LLC and Sasakawa Peace Foundation USA. Zero returned rows applies only to those query spellings, filters and snapshot; aliases/subrecipients/full grants corpus remain untested.
- CanadaBuys history is a bounded **PSPC-managed** procurement slice, not all federal procurement, grants, or all years. Structural changes in March–April 2026 removed some administrative duplicates and individual call-ups. Historical identifier and address coverage is incomplete.
- Prime-recipient joins do not cover subawards, historical beneficial owners, agents' ordinary clients, payments, all fiscal years or historical statuses omitted from cached files. No FARA-to-UEI or cross-border business-number mapping was available directly.

## Reproduce and inspect

Run from the project root, with Python standard library only:

```bash
python research/2026-10-14/fara-award-pilot/reproduce.py research/2026-10-14/fara-award-pilot/evidence/FY2025_All_Contracts_Full_20260906.zip
python research/2026-10-14/fara-award-pilot/canada.py
python research/2026-10-14/fara-award-pilot/review.py
```

`us-summary.json`, `canada-summary.json`, `review-summary.json` and `additional-counts.json` contain machine-readable stage counts. `us-candidates.csv` / JSON preserve all candidates; `us-candidate-transactions.jsonl` preserves raw action identifiers and selected original award fields; `us-recipient-index.jsonl` is the recovered full recipient index. `us-address-anchored-uei-overlaps.json` records the stable-identifier bridge. Canadian candidate JSON/JSONL retains version/client IDs, dates, entity roles and source-row references. [EXCLUSIONS.json](EXCLUSIONS.json), input manifests, `retrieval-ledger.json` and `PUBLICATION-SHA256SUMS` provide provenance and gaps. Individual OCL page URLs are constructed from sourced client/version IDs; the saved bulk row is the retrieved evidence, not a claim that each page was read.

Large inputs and raw intermediates remain local and ignored. Only an explicit sanitized publication allowlist is committed. The findings justify targeted record checks; they do not establish contradictory disclosures or violations.


## Follow-up verification and amount findings

All three FARA CSVs, all seven US contract CSV members, the entire Canadian primary registration CSV, the entire Canadian funding CSV and the entire bounded CanadaBuys history CSV were read. Other members of the Canadian registration ZIP were not analyzed. Original FARA PDFs were not read.

Of the 35 active US address pairs, 31 have FY2025 actions inside their FARA interval. Four do not. The 14 direct address anchors resolve to 12 recipient/role/registration keys; carrying only the same legal name and UEI produces 21 address groups and 2,310 actions.

The original compact candidate table and DOSSIERS.md retain the direct-anchor scope of 79 actions. AMOUNTS.md and amounts.csv use the expanded 2,310-action scope. Net amounts are changes in obligations, not cash payments, contractor revenue, campaign financing or total award ceilings. The reported Canadian government-funding amounts are self-reported financial-year disclosures, not independently verified grant payments.

The Canadian and review scripts were rerun with identical summary counts. summarize.py reconstructed the 12 keys and 2,310 actions using exact decimal arithmetic. verify.py passed saved census, candidate, temporal, UEI, amount and Canadian output checks. No broad US analysis or downloads were repeated. Run `python research/2026-10-14/fara-award-pilot/summarize.py` and then `python research/2026-10-14/fara-award-pilot/verify.py` after the earlier steps.

The catalogue contains 32 anomalous URL pointers, including a future-looking date in a URL and zero-date filenames. These are retained in catalogue-url-anomalies.json, not silently repaired. They do not drive identity or action-date counts and are not documents read.

No case establishes a violation or a contradictory disclosure under an applicable rule. Further reporting would need actual dated ownership/control representations, award-specific lobbying/payment evidence, or qualifying grant receipts matched to the disclosure financial year. Procurement omission does not meet the Canadian government-funding test.


## Publication scope and counting clarifications

A principal registration number identifies its agent registration, not a unique principal. CCC’s 5971 identifies its separate agent; NWMO appears as both registrant and principal under 7186. Neither role implies foreign-government status or ownership/control.

**79 direct actions** across 14 groups and 37 award/IDV IDs are included in **2,310 expanded same-name/UEI actions** across 21 groups, 12 keys and 1,719 award/IDV IDs. Never add these scopes. All public monetary totals use expanded action obligations, not payments. Published compact-candidates.csv now includes both scopes; the earlier local direct-only table is not the public table.

Of 35 active candidates (32 exact and 3 weaker), 31 have overlapping FY2025 actions; four do not. Canadian history dates are 2026-04-01–2026-09-25. Canadian primary counts are registration versions; 112 address/time matches are version pairs across 48 contract rows, not 112 organizations. English-name matching can miss French-only records.

The entire FARA CSVs, seven US CSV members, Canadian primary/funding files and bounded history were read. Other Canadian ZIP members were not used for parent/beneficiary/activity inference. Principal action matching uses the relationship’s recorded half-open interval; comprehensive historical reconstruction from original PDFs was not possible.

The Canadian dictionary defines amount as last completed financial-year funding in Canadian dollars, with a separate current-year expected-funding flag. Client funding is not consultant income. NWMO’s two roles do not double its C$5,423,515.35 disclosure. Blocked grant inputs prevent receipt reconciliation.

The Canadian/review scripts reproduced saved summaries. Amount/evidence checks passed without repeating the US collection. SOURCE-MANIFEST.json records input hashes, SOURCE-LEDGER.json records URLs/failures, and RESULTS-SUMMARY.json combines stage counts. EXCLUSIONS.json withholds raw address fields. Public candidate group IDs are opaque and refer to withheld address groups; source hashes/row IDs permit inspection, but the public table alone cannot reproduce address equality. PUBLICATION-SHA256SUMS covers published files only.

There are 32 anomalous catalogue URL pointers, including zero-date filenames and a future-looking filename. No PDF was read or repaired. These do not determine registration/action intervals; the publication generator omits them from corroborated discovery links.

General grants do not create a universal foreign-agent disclosure duty. DFARS foreign-government-control/proscribed-information restrictions have their own scope, exceptions and waivers; later proposals are not operative FY2025 rules. Canadian consultant/in-house lobbying, its later foreign-influence registry and security-sensitive procurement rules are distinct, not a blanket retrospective FARA prohibition. No candidate establishes a contradictory declaration under an applicable rule.


## Conservative identity scope

Address agreement is a positive anchor, not a necessary condition of legal identity. Mismatches remain unresolved in this baseline, not rejected: an overseas headquarters, operating office, branch or separately incorporated subsidiary can explain them. Affiliates must stay distinct but can merit dated ownership/control review. A subsequent expanded principal-resolution investigation is separate and is not published as a finding here.

Historical SAM bulk layout does not contain the owner-representation fields needed for this test. API record-date filters are not proof of historical-version access. The missing record is an actual dated versioned Reps & Certs report and relevant offer-specific changes under FAR52.204-8(d); archived SAM verification is addressed by FAR4.1201(c). Late FY2025 agency deviations can change clause numbering/scope, so verify the actual solicitation, clause/version and amendments rather than assume52.204-17 applies universally. None of these dated entity-specific answers was verified in this baseline.
