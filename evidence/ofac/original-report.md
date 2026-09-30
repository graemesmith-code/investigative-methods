# US federal contracts versus OFAC: first screening results

Prepared 18 September 2026. **No sanctions violation or failed screening has been established.**

Screened **6,639,176 unique contract and contract-vehicle transactions**, representing **101,379 distinct recipient names**, against **23,398 names and official aliases** for **9,980 current OFAC SDN entities**.

The name comparison produced **13 candidate pairs** (OFAC entity × recipient name × UEI), involving **153 transactions** and **72 award identifiers**. These counts are screening alerts, not violations.

**Assessment:** One candidate, NAI Logistics B.V., matches by name and street address. Its only FY2025 hit is a zero-dollar termination of a contract vehicle. The other 12 candidate pairs have conflicting recipient and OFAC locations and remain unconfirmed. Nothing in this first pass establishes a failed OFAC check.

## What was compared

- Contract action dates: 1 October 2024–30 September 2025 (FY2025); all agencies. The archive includes both ordinary contract actions (award type codes A/B/C/D) and contract vehicles (IDVs, whose award type is blank). Both were screened. This is broader than the initially requested A/B/C/D custom export.
- The ready-made USAspending archive is a September 2026 snapshot of FY2025 records; its precise source metadata is in contract-source.json.
- OFAC list publication date: 17 September 2026. Only entries marked Entity were retained. Individuals, vessels and aircraft were excluded. Strong and weak aliases were retained and distinguished.
- The contract field screened was recipient_name. Case and punctuation were normalised. A second, separately labelled pass removed common terminal company suffixes, such as LLC and Ltd. No fuzzy spelling match was attempted.
- Exact after normalisation: 5 candidate pairs. Suffix-removed: 8 candidate pairs.
- Duplicate transactions skipped: 0; out-of-period rows: 0; other award types excluded: {}; blank recipient names: 3.

## Candidate review table

Countries and cities below come directly from the two source records. Different locations lower confidence, but do not conclusively rule out a branch or affiliate. No common ownership is inferred. Full addresses, identifiers, matching aliases and original contract rows are in the evidence package.

| Contract recipient | UEI | Recipient city / country | OFAC entity and ID | OFAC city / country | Match method | Actions / awards |
|---|---|---|---|---|---|---|
| ACS LOGISTICS LLC | P7NTM9B6RG69 | COEUR D ALENE, ID, USA | AIRCRAFT COMPONENTS LOGISTICS LTD (46068) | Krasnoyarsk, Russia | legal_suffix_removed | 20 / 8 |
| ADVANCED TECHNOLOGIES, INC. | FV58GN6ZNRK1 | NEWPORT NEWS, VA, USA | ADVANCED TECHNOLOGIES COMPANY OF IRAN (25647) | Tehran, Iran | legal_suffix_removed | 22 / 11 |
| APSCO, LLC | E9YGQYEK4NW7 | REDMOND, WA, USA | AMANA SANITARY AND PAINTS COMPANY L.T.D. (28534) | Ghobeiri, Lebanon | legal_suffix_removed | 3 / 1 |
| DIGITAL TECHNOLOGIES, INC. | GUGBC8JMR6X5 | STERLING, VA, USA | LIMITED LIABILITY COMPANY DIGITAL TECHNOLOGIES (36423) | Moscow, Russia | legal_suffix_removed | 6 / 2 |
| DIGITAL TECHNOLOGIES, INC. | PGGGRPN3DDC7 | ONTARIO, CA, USA | LIMITED LIABILITY COMPANY DIGITAL TECHNOLOGIES (36423) | Moscow, Russia | legal_suffix_removed | 38 / 21 |
| GCS LLC | JJXLTLEU5UN5 | LOMA, CO, USA | GIGANT COMPUTER SYSTEMS LLC (50905) | Moscow, Russia | normalized_exact | 9 / 7 |
| GEOTECH ENGINEERING, INC | NC4LP8N8L3B9 | MORRISDALE, PA, USA | GEOTECH ENGINEERING LIMITED (55921) | Hong Kong, China | legal_suffix_removed | 2 / 2 |
| NAI LOGISTICS B.V. | SLVJF3DR8MN5 | AMSTERDAM, , NLD | NAI LOGISTICS B.V. (44257) | Amsterdam, Netherlands; Sharjah, United Arab Emirates | normalized_exact | 1 / 1 |
| PATRIOT LLC | LYMKSJG6DLQ5 | COLUMBIA, MD, USA | PATRIOT INC. (57139) | Ajeltake Island, Marshall Islands | legal_suffix_removed | 41 / 11 |
| PHOENIX LLC | HSDMSEKCW8J8 | MONONA, WI, USA | FENIKS (47650) | Gryazi, Russia | legal_suffix_removed | 4 / 3 |
| RTS LLC | XWSEFECGY3D9 | WALLA WALLA, WA, USA | REPUTABLE TRADING SOURCE LLC (28296) | Muscat, Oman | normalized_exact | 1 / 1 |
| VMC, LLC | DJF2Y1HE6JT6 | SAINT LOUIS PARK, MN, USA | LIMITED LIABILITY COMPANY VOSKHOD MANAGEMENT COMPANY (43223) | Moscow, Russia; Vladivostok, Russia | normalized_exact | 3 / 1 |
| Z-AXIS, LLC | DEAVQLC71338 | DENVER, CO, USA | Z AXIS LLC (47535) | Moscow, Russia | normalized_exact | 3 / 3 |

## The strongest observed identity match: NAI Logistics B.V.

NAI Logistics B.V. matches by full name and street address: Kingsfordweg 151, Amsterdam. Its OFAC ID is 44257. The contract recipient UEI is SLVJF3DR8MN5. This is a strong identity lead; matching corporate registration numbers would provide additional confirmation.

[OFAC added NAI Logistics B.V. on 11 December 2023](https://ofac.treasury.gov/recent-actions/20231211), naming the same Amsterdam address and Dutch registration number 60346515. The current snapshot still includes the company.

The saved FY2025 record for vehicle SPE60523D9402, modification P00002, has action date **11 March 2025**, action type **TERMINATE FOR CAUSE**, and **$0.00 federal action obligation**. It is an IDV modification, not a new A/B/C/D contract award. [USAspending vehicle record](https://www.usaspending.gov/award/CONT_IDV_SPE60523D9402_9700/).

This row records termination after designation. It does not establish that the government awarded new business, made a prohibited payment, or failed an OFAC check. Nor does the interval between designation and recorded termination show that work continued during that interval. The worthwhile follow-up is the vehicle history and its delivery orders between designation and termination, including any FY2024 activity. That history has not been reconstructed in this first pass.

## Examples of weak name collisions

Digital Technologies, Inc. in the contracts file is at 760 S Rochester, Ontario, California. [The company website](https://www.digitaltechnologies-inc.com/) gives that address. The matched OFAC company (36423) is Limited Liability Company Digital Technologies, at 19 Vavilova Street, Moscow. This looks like a name collision; no connection has been established.

Patriot LLC is recorded in Columbia, Maryland. [Its website](https://www.patriotllc.net/about/) describes a Columbia-based technology contractor founded in 2005. The suffix-removed match is Patriot Inc. (57139), a Marshall Islands entity established on 6 December 2024. These differences support treating this as a weak name collision, not an allegation.

## How to verify the remaining candidates

1. Open the OFAC entry at https://sanctionssearch.ofac.treas.gov/Details.aspx?id=NUMBER, using the OFAC ID above. Compare full names, addresses, registration numbers and websites with the contractor identified by its UEI and CAGE code in the saved contract rows.
2. If identity survives that check, locate the original OFAC designation announcement and any later removal or amendment. Compare the effective designation date with each action date. The saved current list is not a historical list.
3. Inspect what each action actually did. An amendment, correction, zero-dollar action or deobligation is not evidence that a new contract was awarded or money paid after designation.
4. Check the applicable restrictions and any authorisations or exemptions before alleging a violation. The records alone do not reveal what checks a procurement office performed.

## Limits of this first pass

This is a simple direct-recipient name screen. It does not screen recipient_name_raw, trading names, parent names, subsidiaries, beneficial owners, subcontractors, individuals or other sanctions lists. It misses spelling variations and entities removed from the SDN list before this snapshot. A clean result is not a clean bill of health. A name alert is not evidence of wrongdoing.

Apart from the NAI designation check and the initial identity comparisons above, historical designation dates and corporate identity have not been fully verified. No payments or contract-value totals are reported. No paid data, Jev calls or external outreach were used.

## Sources and reproducibility

- [Official USAspending contract archive](https://files.usaspending.gov/award_data_archive/FY2025_All_Contracts_Full_20260906.zip)
- [Official OFAC SDN XML](https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.XML)
- [OFAC guidance on assessing name matches](https://ofac.treasury.gov/faqs/5)

The accompanying ZIP contains the sanctions snapshot, scripts, source metadata, screen counts, all candidate groups, and original matching contract rows. The 1.9 GB full contract archive is not included; its URL, byte size and SHA-256 are preserved. Reproduction needs that exact archive; a later official snapshot may differ.

To reproduce with Python 3.11 or later, place the downloaded archive beside the scripts and run: `python3 screen_contracts.py fy2025-full.zip results`. No third-party Python packages or API key are needed.

Matching logic was checked with a synthetic direct match, suffix match, unrelated name and duplicate transaction. Every CSV member was read to completion (including ZIP CRC verification during reading).
