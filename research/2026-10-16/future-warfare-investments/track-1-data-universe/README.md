# Track 1: the public-data universe for US international security capabilities

**Updated 16 October 2026.** The useful universe is much wider than contracts mentioning AI. It spans money, institutions and people, technical requirements, research outputs, industrial capacity, facilities and international transfers. Together these sources can describe individual investments and long-running patterns, but they observe different stages and should retain separate meanings.

Scope is **US national-security capability for international engagement**, including quantum computing and sensing, drones and autonomy, cyber, electronic warfare, communications, space, advanced sensors, materials, directed energy and enabling power/logistics. Domestic place of performance does not exclude a project supporting an overseas military mission. Conversely, a foreign collaborator or an advanced technology does not by itself establish a security mission. Domestic policing and routine administrative AI remain outside scope unless a documented international-security connection warrants inclusion.

## The historical window

The [historical extension](../history/README.md) now supplies **18,819 substantive paragraphs from 1,245 in-period pages** for **12 September 2018–11 September 2023**. It sits alongside the unchanged original 10,000-row export covering September 2023–September 2026. The [combined index](../history/combined_deduplicated_index.csv) has **28,818 unique paragraph keys**, with pointers to both source files.

This is **partial public-archive coverage**, not a census of announcements. The collection uses Internet Archive copies of official pages because live listings returned 403. No recovered page was found for 59 weekdays; holidays and undiscovered pages remain possible. The original export contains only the first 20 of 29 source paragraphs on its oldest day, consistent with a 10,000-row cap. These differences preclude treating paragraph counts or dollar figures as comparable complete investment totals. [Coverage, validation and gaps](../history/COVERAGE.md)

The wider source register describes each source's holdings and retrieval status. Completion of this announcement-archive collection pass does not mean the other listed datasets have all been downloaded.

This matters for comparing periods. The Pentagon's announcement threshold rose from $7 million to $7.5 million in October 2020, then to $9 million in October 2025. The [historical collection's dated rule references](../history/README.md#announcement-thresholds-and-financial-limits) document both changes. FPDS public search migrated to SAM; identifiers and access routes changed. Award modifications revise earlier totals, agency structures move, and public DoD procurement data have a 90-day delay. Today's snapshot is neither an unchanged historical record nor a complete view of the latest quarter. [Procurement source details](../sources/procurement.md)

## 1. Public money: requests, allocations, awards and reported expenditure

The central spine remains defense and security-agency budget books, appropriations and congressional tables, reprogramming records, and USAspending/SAM award actions. Detailed RDT&E project narratives and procurement exhibits can name efforts hidden inside broad accounts. File C can connect some awards to Treasury accounts, though there is no universal budget-project-to-contract crosswalk. [Initial budget inventory](../sources/budgets.md), [procurement inventory](../sources/procurement.md)

The expansion adds **institutional research expenditure**. NCSES surveys describe federally funded research centres, universities and nonprofits, including agency sponsorship, research categories and international performers. These fill a different gap from individual awards: internal laboratory effort and institutional funding can disappear inside large management contracts or mixed research portfolios.

The **Federal Audit Clearinghouse** adds auditees, federal programme expenditure, audit findings and funding relationships. It can expose research and assistance funding that ordinary prime-contract searches miss. Its pass-through table identifies upstream organisations; it is not a complete recipient-to-subrecipient network. Audit thresholds and reporting lag create exclusions. [Research-finance and audit expansion](EXPANDED_ATLAS.md)

Keep the measure attached: a requested dollar, enacted authority, obligation, outlay, survey expenditure and procurement ceiling are different quantities. Different portals often reproduce the same award.

## 2. Institutions and people: who performs the work

University and laboratory surveys, **MURI team rosters**, grant abstracts, contractor identifiers and reported subawards identify organisations beyond the prime recipient. Programme announcements and publications can add investigators, collaborating universities and laboratories that procurement descriptions omit.

**Crossref and OpenAlex** widen this into research metadata: authors, affiliations, funders, award numbers, outputs and international collaborations. The **Open Funder Registry**, UEIs, CAGE codes, DOIs and institutional identifiers provide joining aids. Names and affiliations remain time-dependent; a researcher appearing in two projects does not establish a transfer of money, software or responsibility. Government funding fields can be missing or incorrectly deposited. [Research-metadata sources](EXPANDED_ATLAS.md)

## 3. Technical demand, prototypes and industrial capacity

SAM solicitations and attachments, Grants.gov opportunities, DSIP/SBIR topic archives, DARPA/IARPA pages and DIU disclosures describe what agencies want and what has been tried. These often explain a capability more clearly than an award's short text.

Several less-obvious additions reveal named work below umbrella awards:

- **Microelectronics Commons:** short official project sheets connect quantum, electronic warfare, RF communications and secure-edge projects to funding, hubs, leads and partners. Duplicate project appearances and differing amount labels require care.
- **APFIT:** project cohorts and implementation reports connect prototype-to-procurement selections to sponsors, companies and, in historical reports, quantities and delivery plans.
- **Industrial Base Policy's investment portfolio:** a promising DPA/IBAS view of manufacturing capacity and supply-chain investments. The public page was indexed, but direct retrieval returned 502; its underlying export was not verified.
- **DLA R&D and strategic materials:** programme/solicitation tables, acquisition plans and stockpile reports expose logistics, advanced manufacturing and material dependencies. A planned ceiling or stockpile disposal is not a procurement expenditure.
- **Consortium project disclosures:** NSTXL public notices enrich the existing ATI/consortium layer with performer and project details. Public fragments do not establish a complete ultimate-performer ledger.

[Overseas-security and acquisition-context additions](OVERSEAS_SECURITY.md)

## 4. Technical outputs and evidence of maturity

OSTI, NASA NTRS, laboratory-directed research reports, patents, programme publications and technical project libraries reveal what was produced. Small live OSTI and NTRS API responses were successfully checked in this pass, improving on the first map's access uncertainty. Grant/contract acknowledgments can connect an output to its sponsor; a laboratory-wide contract number still cannot identify a distinct investment for every paper.

GAO assessments, DOT&E reports and transition records help distinguish proposed capability, research output, testing and deployment. **SERDP/ESTCP** contributes installation resilience, energy, protective materials and related defence-support technology. Civilian NASA/NIH/NSF records need actual mission or funding evidence before entering this security investigation. Patents establish invention and rights relationships, not an expenditure or a fielded capability. [Expanded research sources](EXPANDED_ATLAS.md), [original capability evidence](../sources/research.md)

## 5. Physical infrastructure and the overseas footprint

Technology depends on bases, test ranges, laboratories, communications, power and logistics. **Base Structure Reports**, **Federal Real Property Profile**, overseas embassy project pages, and **Navy/NAVFAC environmental reviews** provide complementary views of that physical estate. **EPA's EIS database** is a discovery layer for environmental documents, with different coverage for metadata and full documents.

Overseas construction and environmental appendices can specify hardening, utilities, sensors or operational changes absent from award summaries. Property inventories measure an existing stock; environmental alternatives are proposals; facility budgets cover far more than novel technology. State's public overseas-project portfolio has usable HTML pages, but its tested WordPress endpoint returned 401 and was not pursued. [Infrastructure sources](EXPANDED_ATLAS.md), [State/OBO sources](OVERSEAS_SECURITY.md)

## 6. International flows and partner capability

State budget justifications add Diplomatic Security, INR, secure communications and overseas protection to the agency map. They remain partly access-limited; current-year completeness is not established.

ForeignAssistance.gov, FMS notifications, **DDTC Section 655 commercial-export reports**, **Census ECCN exports**, and the **Security Force Monitor foreign-training dataset** observe different international flows. DSCA **SAMM equipment/recoupment and authority/fund-code tables** add useful system identities and classification bridges.

US assistance, foreign-funded purchases, export permissions, actual shipments and training costs are not interchangeable. SAMM recoupment charges are neither equipment prices nor total R&D costs. The training dataset is historical and contextual; a technical course does not prove a new weapons purchase. [International-source inventory](OVERSEAS_SECURITY.md)

## 7. Previous reporting and supplier context

The original news layer remains essential: defence/space trade outlets, government-IT coverage, national investigations, local company/laboratory reporting and supplier filings. Media Cloud and GDELT are discovery/metadata options with incomplete coverage. Nexis and Factiva remain licensed candidates with no verified project entitlement. A metadata download does not confer rights to reproduce article text. [Media access details](../sources/media.md)

## The clearest free collection opportunities

The [bulk-access register](BULK_ACCESS_REGISTER.csv) gives exact routes, sizes, authentication, rights and test scope. The most useful manageable additions include:

| Source | What is available | What was actually checked |
|---|---|---|
| NCSES Federal Funds | 99 Excel tables in a 1.17 MB ZIP, including foreign-performer tables | Complete ZIP inspected |
| FFRDC research microdata | FY2025 CSV/SAS ZIP, 29.8 KB | Complete file inspected; 862 CSV records |
| HERD and institutional support | Annual research-expenditure/obligation bundles | Official download links checked; payloads not downloaded |
| Federal Audit Clearinghouse | Current CSV tables and historical files | Live CSV sampled; use annual slices rather than assuming a full 561 MB download occurred |
| Grants.gov | Daily opportunity XML ZIP, 78.3 MB for the checked date | ZIP header/sample and full size checked; full extract not ingested |
| Microelectronics Commons / APFIT | Small project PDFs and cohort lists | Representative PDFs and public pages retrieved |
| DSCA SAMM | Equipment-rate and authority/code HTML tables | Representative tables retrieved |
| Security Force Monitor | Paginated JSON/CSV and a listed 556.3 MB SQLite database | One live API sample checked; full database not downloaded; CC BY 4.0 verified |
| OSTI / NTRS | Free programme-readable research metadata | Small API records inspected; this is not a universal full-text corpus |
| OpenAlex / Crossref | Large free scholarly-metadata releases | OpenAlex manifest/small shard and Crossref documentation/API sample checked; whole graphs not downloaded |

OpenAlex's checked funder subset is about 11.16 MB; the complete graph is hundreds of gigabytes. Crossref's annual free torrent is 208 GB compressed; its AWS mirror is requester-pays and monthly snapshots are paid. Small subsets and files should not be confused with complete corpus retrieval.

**Keep access categories separate.** Publisher-listed downloads are less verified than a working payload sample. SAM APIs can be free but require accounts/keys. DTIC public searches report an outage; NSF's current export page showed no files; PatentsView migrated and its tested legacy download failed; several defence/State sources were indexed but not retrieved. No restricted route, membership library or paid corpus is represented as freely available bulk data.

Commerce Business Daily's verified 1996–2001 archive is optional historical context **outside the September 2018-onward main window**, not a priority for that backfill.

## Registers and limits

- [Consolidated source register](SOURCE_REGISTER.csv): 89 source entries, with actual coverage, mission boundaries, joining identifiers and verification details
- [Bulk-access register](BULK_ACCESS_REGISTER.csv): 37 expansion route entries; it does not replace the original core award/budget download routes
- [Register reconciliation](REGISTRY_NOTES.md) and [change crosswalk](REGISTER_CHANGES.csv): 29 additions, eight refinement records folded into nine existing entries, and one cross-inventory duplicate coalesced
- [Expanded research/bulk atlas](EXPANDED_ATLAS.md) and [overseas-security detail](OVERSEAS_SECURITY.md): full source explanations

The missing public universe remains substantial: classified intelligence, ultimate OTA performers, subcontract tiers, hidden internal research, restricted attachments and clean links from budgets through contracts to operational systems. A larger source map reduces blind spots; it does not make those gaps disappear or establish that an unmatched investment is unreported.

[Back to the two-track overview](../OVERVIEW.md) · [Track 2: the IHL deep dive](../track-2-ihl/README.md)
