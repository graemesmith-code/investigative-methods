# Public procurement, award and opportunity data for future-warfare research

**Scope for this investigation:** internationally directed US national-security capabilities across AI, quantum, drones/autonomy, cyber, electronic warfare, space, sensing, communications and enabling technologies. The inventory below is deliberately broader than the final inclusion boundary. Domestic-only policing, administrative AI and unrelated civilian projects are peripheral or out of scope unless a documented international/overseas security mission connects them. Source availability is not a decision to include its whole dataset.

Verified 16 October 2026. This is a source inventory, not an analysis plan. It is scoped to additions around an existing corpus of roughly 10,000 DoD announcement paragraphs from September 2023–September 2026. “Verified” below means the official landing page, documentation or representative record was inspected; it does not mean an entire dataset was downloaded or every authenticated API was tested.

## Editorial highlights

- The biggest additions to the press-release corpus are transaction-level award histories, pre-award requirements and attachments, first-tier subcontract reports, and named performers behind consortium awards. These are different record universes, not interchangeable measures of investment.
- A material break occurs inside the corpus: DoD's announcement threshold increased from $7.5 million to $9 million on 1 October 2025. The rule concerns face value excluding unexercised options; it does not make each paragraph a new obligation. [Current rule and change date](https://www.acq.osd.mil/dpap/dars/dfars/html/current/205_3.htm), [historical rule](https://www.acq.osd.mil/dpap/dars/dfars/html/r20240815/205_3.htm).
- FPDS is now a legacy system name, not the current public search destination. SAM says ezSearch was decommissioned on 24 February 2026 and public contract-award search requires a free SAM account. Do not build an access description around the old anonymous ezSearch interface. [GSA migration notice](https://sam.gov/fpds).
- Other Transactions need a separate coverage statement. SAM's current Contract Awards API explicitly includes OT agreements, orders and IDVs. USAspending should not be assumed to contain the same complete OT universe. A new law approved on 11 September 2026 requires centralized automatic OTA reporting within three years, with an interim reporting provision. This is a reporting transition, not proof that the new data are already available. [Public Law 119-106](https://www.govinfo.gov/content/pkg/PLAW-119publ106/pdf/PLAW-119publ106.pdf).
- Foreign-sales notifications also moved: DSCA announced on 26 February 2026 that future posts would appear at State. Old DSCA URLs alone are no longer a current feed. [Official DSCA notice](https://www.dsca.mil/press-media/major-arms-sales?page=56).

## 1. USAspending prime contracts and transaction histories

**Institution / coverage:** U.S. Treasury, Bureau of the Fiscal Service. Federal award data begin in FY2001 through custom downloads; the Advanced Search interface begins in FY2008. The public last-updated endpoint returned **10/16/2026** during this check. DoD and USACE procurement publication is delayed 90 days; publication date is not award date. [Current disclosures, updated 6 October 2026](https://www.usaspending.gov/data/about-the-data-download.pdf), [live update endpoint](https://api.usaspending.gov/api/v2/awards/last_updated/).

**Unit and content:** Both award-level summaries and transaction-level base awards/modifications. Financial fields distinguish action obligations, cumulative obligations, base/exercised value and potential value. Other useful fields include description, dates, recipient and parent, awarding versus funding agency/office, NAICS, PSC, competition, set-asides and locations. This is the principal structured complement to the daily announcement paragraphs, including smaller awards and subsequent actions.

**Access:** Free search and CSV download at [Advanced Search](https://www.usaspending.gov/search); [Custom Award Data](https://www.usaspending.gov/download_center/custom_award_data); free public V2 API, with no key requested by the tested endpoint. The [endpoint catalog](https://api.usaspending.gov/docs/endpoints) documents award, transaction, IDV, subaward, account and bulk-download routes; `/api/v2/search/spending_by_transaction/`, `/api/v2/transactions/`, `/api/v2/awards/<AWARD_ID>/` and `/api/v2/download/transactions/` are relevant. No bulk export was initiated.

**Join keys / reliability:** `contract_award_unique_key` joins summaries and transactions; `award_unique_key` connects award/account files. PIID is an important component rather than a globally sufficient key. Preserve awarding-agency and parent-IDV identifiers, and modification/transaction identity. Recipient UEI and historical DUNS/parent fields support entity linkage, but one corporate group may have multiple legal-entity identifiers. [Treasury field/identifier guide](https://www.usaspending.gov/data/Federal-Spending-Guide.pdf).

**Limits:** Award descriptions can be generic or erroneous; classified/nonpublic activity is not recoverable from public descriptions. Obligations may be negative deobligations. A ceiling is not money already spent. The latest months of the DoD series remain incomplete even when the site was refreshed today. OT completeness requires separate verification; an OT label in a glossary is not evidence of full coverage.

## 2. USAspending first-tier subawards and SAM subaward reporting

**Institution / unit:** Treasury displays prime-recipient reports originating in SAM. The former FSRS system was retired on 8 March 2025. Records identify a first-tier subcontract/subgrant and its relationship to a prime award, with reported amount/date, subrecipient, location and description. This can expose specialist technology firms absent from prime-only announcements, but is not a complete multilevel defense supply-chain map.

**Access / keys:** [USAspending Search](https://www.usaspending.gov/search), subaward CSV downloads and [V2 `/api/v2/subawards/`](https://api.usaspending.gov/docs/endpoints). Useful identifiers are the prime award key/PIID, subaward/report identifier and subrecipient UEI or legacy DUNS where populated. Name-only matches are weaker; subaward identifiers are not equivalent to prime PIIDs.

**Coverage / lag / quality:** Reporting is generally due by the end of the following month. Treasury warns about duplicate, late, inconsistent and missing reports, including repeated cumulative amounts. Migration introduced additional duplication controls, but does not repair all historical data. Do not add subcontract value to prime obligations as if it were additional federal spending. [Treasury subaward disclosures](https://www.usaspending.gov/data/about-the-data-download.pdf).

**Important current discrepancy:** Treasury's October 2026 PDF still describes a $30,000 cutoff. Acquisition.gov records **first-tier subcontract reporting changing to $40,000 on 1 October 2025**. Thus the generic disclosure should not be applied as a timeless current contract threshold; grant and contract rules also differ. [Official threshold change table](https://www.acquisition.gov/threshold-changes), [FAR clause prescription](https://www.acquisition.gov/far/4.1403).

## 3. USAspending award-to-account financial records (File C)

**Institution / years:** Treasury and reporting agencies; account financial data start in FY2017 Q2. File C contains award financial data by Treasury Account Symbol, program activity, object class and emergency-funding code, including obligations and outlays. It adds funding-account context that most announcement paragraphs omit.

**Access / keys:** [Account download center](https://www.usaspending.gov/download_center/custom_account_data) and [API award funding/account endpoints](https://api.usaspending.gov/docs/endpoints); shared award keys and TAS enable linkage. Treasury distinguishes successful links from “unlinked” records, which can lack recipient or procurement attributes. This does not create a guaranteed link to an R-1 program element or P-1 line.

**Current caveats:** Award outlays before FY2022 are potentially incomplete; agencies now submit monthly. FY2026 introduces Program Activity Reporting Key (PARK) in place of legacy program-activity code/name, without a guaranteed one-to-one crosswalk. DoD procurement-related File C/D1 records are affected by the 90-day hold. [Treasury current data disclosure](https://www.usaspending.gov/data/about-the-data-download.pdf).

## 4. SAM Contract Awards / former FPDS, including Other Transactions

**Institution / years / unit:** GSA; contract action records and modifications, IDVs and their orders, plus OT agreements/orders/IDVs. Historical FPDS records migrated; this check did not establish a single uniform earliest year for every record class. [Current search landing page](https://sam.gov/contract-data), [contracting portal](https://sam.gov/contracting).

**Detail / keys:** PIID, referenced-IDV PIID, solicitation ID, document type, signed date, contracting/funding organization, recipient, competition and performance information. These support direct links to an announcement's contract number; agency/parent context remains necessary. [SAM's public field/search description](https://sam.gov/contract-data).

**Current API reality:** [Contract Awards API documentation](https://open.gsa.gov/api/contract-awards/), production `https://api.sam.gov/contract-awards/v1/search`. Free account and API key required; default nonfederal personal user without a role gets **10 requests/day**. JSON search allows 100 records/page and first 400,000 results; asynchronous CSV/JSON extracts allow first 1,000,000. These are documented limits, not a tested account entitlement. Data include action obligation, exercised/all-options values, non-government dollars and OT agreement type. Public “revealed” DoD data require 90 days; unrevealed access is restricted to eligible DoD users. Immediate/domestic-parent details also differ by access level. No authenticated API request was made.

**Access caveat:** The portal still displays language about future retirement of the FPDS Atom feed; that does not verify its current operability. The documented SAM API is the reliable current specification to cite, not a promise that a legacy Atom workflow will survive.

## 5. What the OT data can and cannot reveal

**Primary evidence source:** [GAO-25-107546, September 2025](https://files.gao.gov/reports/GAO-25-107546/index.html), covering FY2021–FY2024 with detailed tables and case studies, available as free HTML/PDF. This is an audit/data-quality source, not a live award feed.

**Crucial distinction:** A reported recipient may be the consortium manager, a consortium or the actual project performer. GAO explains that large amounts attributed to ATI include funding distributed to consortium projects, not just ATI's own work. New performer fields were added in June 2022. Among 2,431 applicable FY2023–FY2024 records reviewed, 84% correctly identified performers; 395 instead identified the manager. Modification-based consortium structures particularly impede performer identification, while project-based awards can have separate award numbers. The audit also finds incomplete tracking of prototype-to-FAR production transitions and nontraditional-company participation. These findings limit what apparently precise recipient totals mean.

**Related official map:** [GAO-22-105357 and updated recommendation status](https://www.gao.gov/products/gao-22-105357) describes the consortium map and explains why dollars by individual consortium remain incomplete. A list of consortium managers is not itself a project-award list.

## 6. SAM Contract Opportunities, full notice text and attachments

**Institution / universe:** GSA; presolicitations, solicitations, sources-sought/special notices, award notices and sole-source notices. [Public search](https://sam.gov/opportunities) requires no account for ordinary opportunity search. It provides the pre-award requirements missing from award summaries; RFP/BAA/CSO attachments can identify technical goals, anticipated quantities, transition plans, evaluation criteria and contract structures.

**Access / API:** [Public opportunities API documentation](https://open.gsa.gov/api/get-opportunities-public-api/); production `https://api.sam.gov/opportunities/v2/search`. API key required. Maximum 1,000 records/page and one-year date windows; the documentation says it returns the latest active version and directs historical versions to Data Services. Active notices update daily and archived notices weekly. Do not confuse it with the separate Opportunity Management API used for notice administration.

**Keys / values:** `noticeId` is the notice identifier; `solicitationNumber` links versions/related procurement and potentially later contract records, but is not a guaranteed clean PIID crosswalk. Fields include title, agency hierarchy, dates/deadlines, notice type, NAICS/PSC, set-aside, place, description link, attachment links and award data where supplied. Estimated budgets or award-notice values are not necessarily action obligations.

**Historical / access gaps:** [Historical FBO/SAM extracts](https://sam.gov/data-services/Contract%20Opportunities/daily/historical) visibly include legacy feed files dated 1999 and 2001. This verifies historical files exist, not continuous complete coverage since 1999. Some attachments are controlled or require approved access; a publicly visible notice does not make every technical file public. Cancellations, amendments and archived notices are distinct states.

## 7. DoD daily announcements and agency press releases

**Sources:** Existing [Defense.gov contracts URL](https://www.defense.gov/News/Contracts/) and current [War.gov contracts listing](https://www.war.gov/News/Contracts/). Free HTML, date/archive search, one daily page containing multiple award/modification paragraphs. Defense.gov's direct fetch failed during this check; indexed current official contract listings are on War.gov. Preserve exact article/date/paragraph provenance rather than treating hostname change as a new award.

**Fields / keys:** Usually contractor and location, announced amount, pricing/vehicle, purpose, performance location/end date, funds obligated at award, appropriation/fiscal year, competition, contracting office and PIID. PIID is the strongest bridge to structured records, but formatting variants and multiple contracts per paragraph occur.

**Coverage and amount semantics:** The public-announcement rule excludes unexercised options from its face-value test. Initial indefinite-delivery awards can be announced at estimated face value while orders within that amount are not separately announced under that rule; undefinitized actions use not-to-exceed amounts. Therefore this source is neither a full award census nor an obligation ledger. [DFARS 205.303](https://www.acquisition.gov/dfars/part-205-publicizing-contract-actions).

**Adjacent value:** Agency-specific program/award releases can add project names, operational customers, tested milestones and production transitions. These remain selective communications rather than standardized transaction datasets.

## 8. DIU commercial solutions catalog, solicitations and annual/transition reports

**Institution / years:** Defense Innovation Unit. The [Commercial Solutions Catalog](https://www.diu.mil/solutions/portfolio/catalog) currently contains entries with completion years 2017–2026 and some undated entries. Unit is a successful/transitioned project-company solution; fields include project, portfolio, company and completion year, with individual detail pages. Free HTML; no documented public bulk/API product verified.

**Meaning / keys:** Excellent capability and performer context. Catalog entry IDs and project/company/year combinations are useful source keys, but no universal PIID/UEI crosswalk was verified. Being listed indicates a successful or transitioned prototype available for acquisition; it does not state the amount obligated or adoption across every military service. Success memos are available through DIU rather than automatically published as a full public dataset. [Representative 2026 tactical-compute entry](https://www.diu.mil/solutions/portfolio/catalog/a0T83000000H7M3EAK-a0hcr00000FCFInAAP).

**Pre-award:** [Open pathways/solicitations](https://www.diu.mil/work-with-us/open-solicitations) offers CSOs, challenges and commercial-acceleration opportunities with deadlines and requirement narratives. Current openings were visible, but the landing page is not a complete historical solicitation archive.

**Longitudinal reports:** [FY2022 report hub](https://www.diu.mil/fy22-year-in-review) links annual reports back to 2017 and notes a calendar-to-fiscal-year shift beginning FY2021. [The URL labeled `2024-annual-report-files`](https://www.diu.mil/2024-annual-report-files/index.html) actually displays **FY2023** content. It distinguishes obligated prototype funding from production-contract ceilings and provides project spotlights. Do not label it “FY2024 report” from the URL alone; a newer annual report was not verified in this pass.

## 9. AFWERX / SpaceWERX STRATFI, TACFI and transition disclosures

**Institution / sources:** Department of the Air Force innovation programs; [SpaceWERX award showcase](https://spacewerx.us/accelerate/stratfi-tacfi/), [FY2024 AFWERX/SpaceWERX annual report PDF](https://spacewerx.us/wp-content/uploads/2024_AFWERXSPACEWERX_AnnualReport_Cleared_AFRL-2025-2954.pdf), [AFWERX program/funding descriptions](https://afwerx.com/get-funded/).

**Unit / coverage:** Showcase entries identify company, program year and STRATFI/TACFI category; visible cohorts run from PY2020 through PY2025, with some award-status dates. Reports contain aggregate counts, funding and transitions plus selected companies/projects. Free HTML/PDF; no comprehensive downloadable award API verified here.

**Joins / limits:** Company name, program year, project and underlying SBIR award/contract number if individually published; generally not a uniform UEI-linked ledger. Program selections, awarded companies, SBIR dollars, other government matching funds and private matching capital are different quantities. An announced matched total is not entirely federal investment. The official [portfolio link](https://spacewerx.us/ventures/portfolio/) currently says “Portfolio coming soon,” so it should not be described as an available detailed database. SBA's SBIR award database is a separate complementary source for underlying research award records.

## 10. Consortium-manager project award disclosures

### ATI: unusually useful public project table

[ATI Project Awards & Highlights](https://www.ati.org/rd-project-awards/) is a first-party consortium-manager source, not a government financial database. The current table explicitly covers **the last 12 months** and lists consortium/program, award date, member name and **ceiling**. Visible rows run into September 2026. This adds actual performer names behind umbrella awards to ATI and spans areas such as armaments, naval systems, missiles, training and microelectronics.

Free HTML; no public API/bulk format verified. Program acronym + date + member + ceiling identify a row but do not guarantee uniqueness. The table lacks a universal PIID/UEI and can contain multiple awards to one member on one date. Press highlights add project scope for selected awards. It is a rolling disclosure, with heterogeneous programs including civilian health work, not a complete historical DoD obligation ledger.

### NSTXL / SOSSEC and individual consortia

[NSTXL's first-party SpEC page](https://nstxl.org/rapidly-delivering-next-generation-space-prototypes/) confirms open opportunities can be explored free although submission requires membership. Its [2022 review](https://nstxl.org/2022-year-in-review/) illustrates project names, performers and values contingent on milestones/options. [SOSSEC consortium pages](https://sossecinc.com/sossec-consortium/) describe sponsoring offices, technical scope and umbrella vehicles. Individual consortium pages and releases are useful first-party disclosure fragments, not interchangeable with a full project-level award feed.

Join reliability varies: some individual releases publish the parent OT/contract and project number, others only names. Membership directories show eligibility/community, not that every member won government funding. Detailed solicitations may be member-only or export-controlled; public front pages do not imply public access to those files.

## 11. CDAO Tradewinds: opportunity data, not an open award database

**Source / unit:** [Current Tradewinds opportunities](https://www.tradewindai.com/opportunities) and [marketplace access description](https://www.tradewindai.com/tradewinds-opportunity), operated for CDAO; public special topics, shopping notices and notices of intent expose problem statements, requesting/contracting activities, control numbers and dates. [Representative SAM open-call record](https://sam.gov/workspace/contract/opp/55a3870bf71a4bf088c583752324a6aa/view) includes a publicly listed announcement attachment and solicitation identifier W519-23-S-CTSM.

**Access / limits:** Public webpages and selected PDF notices are free. Current access guidance states the marketplace buyer view is for government users with .gov/.mil email; the full assessed solution library should not be advertised as an anonymous downloadable dataset. No open award API was verified. A supplier's “awardable” status means acquisition eligibility following assessment, not a completed contract or obligation. Join keys are control/solicitation numbers, solution/company names and any later explicitly disclosed award number. It adds demand and technology vocabulary while leaving major financial-disclosure gaps.

## 12. DARPA R&D opportunities and program pages

[DARPA R&D opportunities](https://www.darpa.mil/work-with-us/opportunities) and [Contracts Management Office](https://www.darpa.mil/about/offices/contracts-management) identify BAAs, research announcements, SBIR/STTR topics, RFPs and contract/grant/OT mechanisms. Unit is a solicitation/program and its associated documents; keys are BAA/solicitation number, program acronym and office. Free public pages/PDFs and SAM/Grants.gov links; no comprehensive DARPA award-ledger API verified.

This adds requested capabilities, program structure and performers named in program/award releases. A BAA's total anticipated funding is a solicitation envelope, not an actual award total. Research and prototype pathways are mixed; classified or restricted attachments remain outside the public universe. Historical coverage depends on the program page/document archive rather than a verified uniform start year.

## 13. Entity identifiers: SAM registry and DLA CAGE Search

**SAM:** [Entity Information](https://sam.gov/entity-information), [Entity Management API](https://open.gsa.gov/api/entity-api/), [entity extract API](https://open.gsa.gov/api/sam-entity-extracts-api/). Public entity data include UEI, legal name, registration, addresses, business types, NAICS and PSC. JSON and CSV/extract routes require an account/API key; sensitive or CUI access is a separate restricted product. Registrants opting out of public display are not all visible publicly. Current registration data are not a complete historical corporate-ownership database.

**DLA:** [CAGE Search](https://cage.dla.mil/Search) reached a usage-agreement landing page; [official June 2025 guide](https://www.acq.osd.mil/asda/dpc/ce/p2p/docs/cap-sums/8_Commercial%20and%20Government%20Entity%20%28CAGE%29/Procure-To-Pay%20Capability%20Summary%20-%20CAGE%20Search%20Inquiry.pdf) confirms searches by CAGE, UEI, legal name and location. A CAGE identifies an entity/facility at a location, not necessarily an entire consolidated company. No general anonymous bulk CAGE API entitlement was established.

**Value:** These are join-support registries, not investment data. They can disambiguate a startup from a similarly named supplier and connect site-level awards; name or parent-company changes require caution.

## 14. DLA DIBBS: component-level procurement adjunct

[DIBBS](https://www.dibbs.bsm.dla.mil/) is the DLA supply procurement portal. Its [official introduction](https://www.dla.mil/Portals/104/Documents/SmallBusiness/DIBBS%20Solicitations%20-%20With%20Notes.pdf?ver=dmjLD_fLHf3ZHVtbk5cX0Q%3D%3D) documents RFQ, RFP/IFB, award and download functions. Unit is a supply solicitation or award, potentially useful for NSN/part/quantity/vendor detail below the daily DoD announcement threshold.

The live entrypoint reached the DoD warning/consent screen. This pass did not proceed into a representative award, verify an API, or establish historical/bulk-award coverage; treat it as a verified official source requiring a focused access check. Contract/solicitation number, NSN and CAGE are the natural bridges. Technical data can be separately restricted. High volume of routine sustainment means this is a supplementary component source, not a ready-made “emerging technology” list.

## 15. Foreign Military Sales notifications: State, DSCA and Federal Register

**Current / historical:** [State Arms Sales: Congressional Notifications](https://www.state.gov/arms-sales-congressional-notifications/) is the officially designated destination for new posts; [DSCA announcement/archive](https://www.dsca.mil/press-media/major-arms-sales?page=56) directs pre-December-2024 entries to its older library. State's direct page fetch failed in this check; the route is verified through DSCA's own notice, not through inspection of all current State posts.

**Unit / fields:** One proposed sale notification, often with country, equipment quantities, estimated total, major-defense-equipment component, contractors, rationale and support/training. Notification/transmittal number is the strongest key across releases and Federal Register; country, item names and dates are secondary. It is not a PIID, signed procurement contract or proof of delivery. Below-threshold and classified activity are not a complete public universe.

**Alternative official access:** [Federal Register representative June 2026 notification](https://www.federalregister.gov/documents/2026/06/17/2026-12128/arms-sales-notification) was accessible and includes transmittal 26-64, proposed quantities/value, policy justification and sensitivity text. [Federal Register API documentation](https://www.federalregister.gov/developers/documentation/api/v1) and [GovInfo format/coverage guide](https://www.govinfo.gov/help/fr) support free document retrieval; GovInfo offers 1995-present XML/PDF/text and earlier scanned volumes. The notification universe does not necessarily extend to every year of the underlying publication archive.

**Lag:** Register publication can be much later than congressional notification. Preserve both dates. These sources add foreign demand and exported capability detail, but notification estimates must not be counted as realized U.S. military investment.

## 16. DSCA Historical Sales Book and Excess Defense Articles

**Sales Book:** [Official publications landing page](https://www.dsca.mil/Resources/Publications/Article/4049946/dsca-historical-sales-book) lists the [FY1950–FY2024 book](https://media.defense.gov/2025/Jul/01/2003746467/-1/-1/1/FY_2024_HISTORICAL_SALES_BOOK_COMPLETE.PDF), published July 2025. Country/international-organization historical aggregates provide context separate from individual notification estimates. PDF; no API verified. The direct PDF fetch failed during this check, so its complete table schema and a later FY2025 edition were not verified. Country/year are the main joins, not contractor PIID.

**EDA:** [Official Excess Defense Articles page and database link](https://www.dsca.mil/Programs/Defense-Trade-and-Arms-Transfers/Excess-Defense-Articles) describes notified transfers with country, article, quantity, implementing agency, grant/sale, acquisition/current values, transfer status and status-change date. It excludes potential offers not yet notified. This can distinguish actual transfer status from proposed sales but mostly concerns existing equipment, not new R&D investment. The public description was verified; the full database's current export format and year completeness were not.

## 17. ForeignAssistance.gov: security-assistance spending context

**Institution / access:** Current U.S. government foreign-assistance portal; [data downloads](https://foreignassistance.gov/data?country=Israel) displayed update date **30 September 2026** and complete CSV/API, budget CSV/XLSX, and country-summary exports. [API documentation](https://foreignassistance.gov/api-docs) lists V2 JSON routes for complete transactions and country/sector/managing/funding-agency aggregates. No bulk dataset was fetched.

**Unit / fields / years:** Transaction-level obligations and disbursements plus separately labeled budget data; country summaries in current/constant dollars from 1946 and sector summaries from 2001. Country, fiscal year, funding/managing agency, sector and activity descriptions are available organizing dimensions. Project/award identifiers must be checked in the chosen extract before promising a PIID join.

**Limits / added value:** Useful for Foreign Military Financing and other security assistance in a wider fiscal context. It is not a detailed weapons-acquisition ledger and does not make foreign-funded FMS purchases equivalent to U.S. aid. Latest-year reporting completeness varies by series. Budget request, allocation, obligation and disbursement are separate states.

## Coverage boundaries common to this lane

1. No public source here guarantees complete classified, intelligence-community or subcontract-tier visibility.
2. Acquisition vehicles, individual orders, modifications, consortium project awards and program selections are different units. A source's dollar label must travel with the record.
3. Available joins range from strong composite award identifiers to weak project/company names. No universal public key links every budget line, requirement, prototype, production purchase and fielded system.
4. “API exists” and “anonymous bulk access exists” are different claims. This pass verified documentation and representative public pages, not account entitlements or a production ingestion run.
5. Primary-government sources were preferred. ATI/NSTXL/SOSSEC and Tradewinds are identified as first-party operator/manager disclosures where appropriate; they are useful additions but not substitutes for government financial records.
