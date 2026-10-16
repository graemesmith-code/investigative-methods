# Public R&D, security-adjacent AI, and capability-evidence sources

**Scope for this investigation:** internationally directed US national-security capabilities across AI, quantum, drones/autonomy, cyber, electronic warfare, space, sensing, communications and enabling technologies. The inventory below is deliberately broader than the final inclusion boundary. Domestic-only policing, administrative AI and unrelated civilian projects are peripheral or out of scope unless a documented international/overseas security mission connects them. Source availability is not a decision to include its whole dataset.

Verified 16 October 2026. Scope: useful additions to a Pentagon-contracts dataset, with emphasis on public records rather than proposed analyses. Access checks used official pages and small representative records/documentation, not bulk ingestion. “Could not retrieve with this tool” does not establish that a service is down. Only DTIC and SBIR have explicit publisher notices about the outages/maintenance described below.

## Most useful additions in plain English

- **SBIR/STTR award abstracts** expose much smaller, earlier-stage projects than large-contract announcements, across defense and civilian agencies. They provide actual award amounts plus identifiers that can sometimes link into procurement records.
- **DARPA/IARPA program and BAA pages** reveal the technical problem, program phases, named performers and evaluators. They do not consistently provide a transaction ledger or prove deployment.
- **The federal AI inventories** supply reported use cases, vendors, components, operational dates and development stages, especially for DHS and DOJ/FBI. They explicitly exclude DoD/DoW, intelligence-community and National Security System uses, so they cannot measure military AI comprehensively.
- **DOE/NNSA laboratory reports** expose internally funded projects hidden inside large laboratory management-and-operation contracts. **OSTI and NASA NTRS** connect research outputs to contract/report identifiers.
- **GAO and DOT&E** help distinguish money committed from technology matured, tested or actually fielded. **Patents and SEC disclosures** are useful supplementary evidence, with weaker links to government operational use.

## Priority source inventory

### 1. SBA SBIR/STTR awards, topics and firms — core award-level R&D data

- **Official access:** [Data resources](https://www.sbir.gov/data-resources), [awards](https://www.sbir.gov/awards), [API documentation](https://www.sbir.gov/api).
- **Unit / coverage:** Individual award and its abstract, firm, agency/branch, phase, solicitation/topic, award date, amount and research institution. SBA says awards are downloadable from program inception; phase coverage should be checked against the policy definition rather than assuming every later commercial/Phase III contract is represented.
- **Format / joins:** Full downloads with/without abstracts; search exports capped at 10,000 rows; documented JSON/XML API. Fields include contract number, agency tracking number, topic code, solicitation number/year, UEI and legacy DUNS. These are useful candidate joins, not proof that every record maps one-to-one to a procurement action.
- **Freshness / access:** Bulk files refreshed monthly; new records need at least 24 hours to appear in search. Awards page states FY2025 was not expected complete until March 2026. API documentation currently warns of maintenance; a one-row query was not retrievable in this test. The bulk files are publisher-listed, not bulk-downloaded or validated here.
- **Meaning:** Research funding awarded. An abstract is a proposed R&D objective, not demonstrated capability or procurement deployment.

### 2. DARPA current/completed programs and R&D opportunities — program/intent layer

- **Official access:** [Program directory](https://www.darpa.mil/research/programs), [R&D opportunities](https://www.darpa.mil/work-with-us/opportunities).
- **Unit / coverage:** Current and completed program pages, technical office, program manager, problem statement, phase structure, links to solicitations/challenges and selected announcements. Public directory includes legacy completed programs but does not promise a complete historical transaction archive.
- **Format / joins:** Searchable HTML; linked PDFs and solicitation documents. Program acronym/title and BAA/solicitation number are the strongest bridges to SAM.gov notices, SBIR topics, award abstracts and reports. No general public structured award-ledger API was verified.
- **Freshness / limits:** Pages update as programs change, without a uniform reporting SLA. Classified programs and undisclosed performer/funding details remain missing. Program pages can survive after a program finishes; record program status separately from page update date.
- **Meaning:** Priorities and R&D program context. A solicitation is intended competition; a performer announcement is award/participation evidence; a program goal is not an operational capability.

### 3. IARPA programs, BAAs and performers — public intelligence R&D layer

- **Official access:** [Research programs](https://www.iarpa.gov/research-programs); representative [HIATUS program](https://www.iarpa.gov/research-programs/hiatus).
- **Unit / coverage:** Program-level objectives, start/duration/phases, BAA status and dates, prime performers, test-and-evaluation partners, summaries and Q&A. The current directory and historical program pages cover public programs; not the whole intelligence R&D budget.
- **Format / joins:** HTML plus PDF BAAs/amendments and SAM references. Join on BAA number, program acronym, performer institution and research-report contract number when available. HIATUS explicitly supplies IARPA-BAA-22-01, two prime performers and three evaluation partners.
- **Freshness / limits:** No verified complete bulk performer-award export or public amount field. Page updates are uneven; datasets sometimes require separate requests. Public participation and published papers do not expose classified transitions or downstream operational adoption.
- **Meaning:** Public research commitments and test structure. Named performer does not establish funded amount; research success does not establish IC deployment.

### 4. Grants.gov opportunities and forecasts — structured funding intent

- **Official access:** [API guide](https://grants.gov/api/api-guide), [daily XML extract documentation](https://www.grants.gov/help/xml-extract/).
- **Unit / coverage:** Funding opportunity/forecast and associated synopsis, agency, eligibility, deadlines, estimated funding/award range, opportunity and assistance-listing identifiers. Relevant to defense research grants, DHS/DOJ research and civilian dual-use programs.
- **Format / joins:** Daily ZIP/XML extract with schema; enhanced “v2” includes forecasts. The guide documents unauthenticated search2 and fetchOpportunity endpoints at api.grants.gov; some other APIs require keys. Opportunity ID/number, agency and Assistance Listing number are join candidates. Linked NOFO/BAA PDFs contain more detail.
- **Freshness / limits:** XML is a daily snapshot of the grant database, not a transaction history. Historic notice revisions may require retaining snapshots or following the opportunity record. No small POST API execution was performed with this web-only test.
- **Meaning:** Available or planned funding. Estimated totals and award ceilings must not be counted as awards, obligations or expenditures. Complements SAM opportunities; it does not replace contract solicitations.

### 5. DTIC public technical reports, public-access publications and grant abstracts — valuable but currently unavailable search

- **Official status/access:** [DTIC products and services](https://discover.dtic.mil/products-services/).
- **Unit / coverage:** Completed publicly releasable S&T reports, scholarly publications from defense and ODNI/IARPA-funded research, and descriptive abstracts of public unclassified grants.
- **Format / joins:** Normally report metadata and linked documents, with report/accession identifiers and contract or grant references where supplied. No usable current public bulk/API route verified.
- **Current blocker:** Publisher explicitly says S&T report search, public-access search and grant-award search are offline. Do not represent DTIC as a ready-to-query live corpus today.
- **Public boundary:** Controlled DTIC/R&E Gateway and Horizons require CAC/PIV/ECA access. Horizons’ richer project, budget-narrative and maturity fields are not a public substitute. Public collections exclude controlled/classified material.
- **Meaning:** Research outputs and grant descriptions, not comprehensive project spending or operational deployment. Publicly indexed older report links may still be discoverable, but coverage and live access must be checked individually.

### 6. DOE OSTI.GOV — structured research outputs and sponsor/contract links

- **Official access:** [API documentation](https://www.osti.gov/api/v1/docs), [download/coverage FAQ](https://www.osti.gov/faqs); representative [FY2025 Argonne LDRD report record](https://www.osti.gov/biblio/3025504).
- **Unit / coverage:** Research output: technical report, paper, dataset, software and other product metadata from DOE-funded work, including national-laboratory work. Publication and record-entry dates support separate time filters; historical coverage varies by product/lab.
- **Format / joins:** REST JSON/XML/BibTeX; metadata bulk routes via OAI-PMH/XML and MARC; full text when publicly available. OSTI ID, DOI, report number, DOE contract number, sponsoring/research organization and award identifiers where provided. API supports identifier and sponsor queries.
- **Access / limits:** Documentation and an indexed representative record were verified. A one-row search API probe and direct representative record fetch were not retrievable by this tool; this is not a publisher-reported outage. Public availability/full text varies; classified, controlled and unreleased work is absent.
- **Meaning:** Evidence that work produced a reported output. A lab-wide M&O contract on hundreds of papers cannot be treated as a separate investment for each output.

### 7. DOE/NNSA laboratory-directed and site-directed research reports — internal investment layer

- **Official access:** [DOE LDRD annual reports](https://www.energy.gov/cfo/listings/laboratory-directed-research-and-development-annual-reports?page=0), [FY2025 financial report](https://www.energy.gov/sites/default/files/2026-04/fy-2025-doe-ldrd-report-to-congress.pdf), [Sandia FY2025 report](https://www.sandia.gov/app/uploads/sites/156/2026/04/FY25-Sandia-Labs-LDRD-Annual-Report-SAND2026-19220R.pdf), [NNSS SDRD reports](https://nnss.gov/mission/sdrd/).
- **Unit / coverage:** Annual lab/site funding aggregates plus individual internal R&D project narratives in lab/site reports. DOE listing has FY2016–FY2025 on the checked page; older pages may extend it. NNSS explicitly releases reports each April for the prior year.
- **Format / joins:** PDFs and HTML; project number, principal investigator, laboratory, fiscal year and report identifier. OSTI records can add contract numbers/DOIs. No unified project-level bulk export verified.
- **Limits:** Financial totals and public narrative portfolios have different granularity. Not all lab research is LDRD; project-cost detail and classified descriptions vary. DOE includes civilian science labs as well as NNSA: tag sponsor/lab/mission, rather than treating all DOE research as military.
- **Meaning:** Actual internally funded research and reported outputs, distinct from lab prime-contract totals. Avoid adding LDRD costs to an inclusive M&O total without reconciling overlap.

### 8. NIJ/OJP funded projects — criminal-justice R&D awards

- **Official access:** [NIJ award directory](https://nij.ojp.gov/funding/awards/list), [funding/award documentation](https://nij.ojp.gov/funding), [AI-tagged award examples](https://nij.ojp.gov/taxonomy/term/artificial-intelligence?page=1&type=node%3Aaward).
- **Unit / coverage:** Individual grants/cooperative agreements, FY, title, originating solicitation, recipient, amount, status and linked products. NIJ says its directory includes awards since 2003; past solicitations extend back to FY2005 and link their resulting awards.
- **Format / joins:** Searchable/filterable HTML with award detail and product links, not a verified bulk/API feed. Award number, solicitation/opportunity ID, recipient and FY connect to assistance transactions and research outputs.
- **Limits:** NIJ is one justice research funder, not all DOJ/FBI purchasing. Topic tags are broad and imperfect: the AI-tagged list also returns forensic projects not self-evidently AI. Award status is not a deployed-system status. Historical and update completeness should be checked per record.
- **Meaning:** Actual research funding; linked products are outcomes. DOJ/FBI operational AI should be separately checked in the AI inventory, procurement and privacy documentation.

### 9. DHS S&T / Silicon Valley Innovation Program — prototype OTAs and transitions

- **Official access:** [SVIP-tagged public records](https://www.dhs.gov/keywords/silicon-valley-innovation-program-svip); [official machine-learning demo announcement](https://www.dhs.gov/group/13025/news/2022/04/05/dhs-st-demonstrate-emerging-technology-critical-mission-needs).
- **Unit / coverage:** Topic call, company, phase award, prototype demonstration and selected transition story. Public topic/portfolio pages and releases are useful for startup-level homeland-security technology that may not be legible in high-level contract announcements.
- **Format / joins:** HTML and program/demo PDF catalogs. Company, topic, phase, component and dates are common; agreement/award numbers and phase amounts are not uniformly present. No verified complete structured award export.
- **Access / limits:** Search index returned official portfolio entries, including named 2024 phase-one OTAs; direct DHS page retrieval failed in this tool. Treat the listings as partial and date-specific, not a current comprehensive portfolio. Historic program funding caps have changed; take amounts from each actual award.
- **Meaning:** Prototype investment and testing/transition evidence. Eligible funding maximums are not actual awards. A phase-four operational pilot is not equivalent to department-wide production adoption.

### 10. OMB consolidated federal AI use-case inventories — structured deployment-adjacent evidence

- **Official access:** [2025 repository](https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory), [data dictionary](https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory/blob/main/Validation/data_dictionary.md), [agency-source manifest](https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory/blob/main/Validation/data_sourcing_summary.md).
- **Unit / format:** CSV/XLS individual use cases, plus separate consolidated COTS uses; annual reporting with rolling repository corrections. Dictionary includes agency/component, use-case ID, development stage, operational/pilot date, vendor, contracting/in-house origin, system name and ATO-related fields.
- **Joins / limits:** Use-case ID is intended to persist but agencies may omit it publicly. Vendor and system names provide softer procurement links; contract numbers are not a standard join. Scope/schema changes and consolidation break naive year-to-year counts. “Deployed” includes actively authorized use, not a usage-volume measure.
- **Critical exclusions:** DoD/DoW, IC, National Security Systems, and much basic/applied research. Public disclosures may omit protected fields. Missing cases cannot be read as absence of AI.
- **Snapshot:** README dated April 13, 2026 gives 3,611 individual cases across 41 agencies; directly useful security-adjacent coverage includes DHS, DOJ, DOE and NASA. This is neither an investment-dollar dataset nor a military AI census.

### 11. Agency AI originals and privacy assessments — newer and more operational detail

- **Official access:** [DOJ inventory](https://www.justice.gov/si/ai-inventory), [DOJ privacy assessments](https://www.justice.gov/opcl/doj-privacy-impact-assessments); DHS XLSX documented by OMB: [2025 DHS file](https://www.dhs.gov/sites/default/files/2026-01/2025_0128_ocio-dhs-ai-use-case-inventory.xlsx).
- **Unit / format:** Agency use case/spreadsheet and system-level PIA/PDF. DOJ originals include department components; component and system names connect public FBI uses to broader DOJ records. PIA dates/versions, system names and inventory IDs where cited are join aids.
- **Freshness:** DOJ’s page updated October 7, 2026 reports 315 entries, versus OMB’s 314-row April snapshot. DOJ notes merging/renumbering, withheld information and partial releases. Prefer original files for latest state while retaining OMB normalization provenance.
- **Access:** DOJ landing and PIA index opened; linked inventory file was not rendered by this web tool. DHS file URL was verified in OMB’s retrieval manifest, not downloaded here.
- **Meaning:** Self-reported use and documented data/system design. A PIA can describe planned or conditionally approved use; it does not establish expenditure, full deployment or effectiveness. Inventory entries are not additive to contract totals.

### 12. GAO weapons assessments and DOT&E annual reports — maturity, test and delivery evidence

- **Official access:** [GAO 2026 weapon-systems annual assessment](https://www.gao.gov/products/gao-26-108457), [full GAO report](https://www.gao.gov/assets/gao-26-108457.pdf), [DOT&E annual-report archive](https://www.dote.osd.mil/annualreport), [FY2025 DOT&E PDF](https://www.dote.osd.mil/Portals/97/pub/reports/FY2025/Other/2025Annual-Report.pdf).
- **Unit / coverage:** Program/system-year assessment, schedules, cost estimates, maturity, acquisition pathway and test findings. GAO’s July 2026 report is its 24th annual assessment and covers 104 selected costly acquisition programs. DOT&E provides recurring selected system test assessments.
- **Format / joins:** HTML summaries and long PDFs/tables; report ID, fiscal year, program/system acronym and named contractor. Crosswalks to budget/program and contract IDs generally require document reading. No unified clean public program-panel API verified.
- **Limits / access:** Selected portfolios, not all programs; public versions exclude restricted details. Annual publication lags the data-collection window. GAO page opened; DOT&E FY2025 PDF was indexed but direct fetch returned 403 in this tool.
- **Meaning:** Independent evaluation and test evidence. Planned lifecycle costs are not annual obligations; successful testing is not proof of sustained operational deployment.

## Selective dual-use and contextual extensions

### 13. NASA TechPort — technology projects and maturity

- **Official access:** [TechPort](https://techport.nasa.gov/home), [current API documentation](https://techport.nasa.gov/help/api), representative [Autonomous Aerial Cargo Operations at Scale](https://techport.nasa.gov/projects/105779).
- **Unit / coverage:** Active/completed technology project, description, program, organization, project dates/status, technology taxonomy and maturity information where recorded. Homepage describes over 15,000 active/completed projects; no complete earliest-year boundary verified.
- **Format / joins:** HTML and documented REST JSON API, project ID and organization/program IDs; links to reports and other project artifacts where supplied. **Current documentation requires a token from a current authenticated TechPort session and a new token each session.** Do not rely on older anonymous API examples.
- **Access / limits:** API documentation and indexed project details verified; API not authenticated/tested. Project-maintainer update lag varies. Budget and contract-number completeness not established.
- **Meaning:** Civil aerospace technology development/maturity, relevant to autonomy, sensing, communications and space. Do not label an entire NASA project military because its technology has a possible dual use.

### 14. NASA NTRS — public technical outputs

- **Official access:** [NTRS API documentation](https://ntrs.nasa.gov/api/openapi/), representative [1984 AI/aerodynamics report](https://ntrs.nasa.gov/citations/19840023019).
- **Unit / coverage:** Citation/report with title, abstract, authors, publication/acquisition dates, report number, funding numbers and public-download metadata. Historical legacy reports and current outputs coexist; the checked record demonstrates historical rather than earliest possible coverage.
- **Format / joins:** Documented GET/POST search and citation endpoints, PDF downloads, CSV/XML export endpoints. NTRS document ID, report/patent number, funding/contract number where supplied, DOI and organization.
- **Access / limits:** Swagger documentation and a public citation opened. A one-row API query was not retrievable by this tool, so live API response shape was not validated. Public records only; not every citation supplies a public full text. Acquisition date can reflect repository migration, not research date.
- **Meaning:** Scientific/technical results. Funding acknowledgments link origins but do not quantify project investment or establish operational adoption.

### 15. ARPA-E project directory — energy technologies with selective security relevance

- **Official access:** [Search all projects](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects).
- **Unit / coverage:** Project, performing organization/type/location, funding, program/funding round and status. Indexed directory includes OPEN 2009-era projects through current selected projects, with research-area filters.
- **Format / joins:** Searchable HTML, project pages and linked program documents; project title, organization, program and any stated award identifier. No official bulk export/API was verified.
- **Access / limits:** Official directory was search-index readable; direct opening produced no extractable text. Records include “Selected,” active and alumni-like statuses, which must remain distinct. Award amount is not a payment stream. A uniform update cadence was not verified.
- **Meaning:** Civilian energy R&D investments and selection intent. Include only a relevant power, battery, grid/cyber, sensor or computing relationship; ARPA-E-wide funding must not be presented as defense/security investment.

### 16. USPTO PatentsView, government-interest records and AI Patent Dataset — invention evidence

- **Official access:** [Current PatentsView page](https://www.uspto.gov/ip-policy/economic-research/patentsview), [AIPD](https://www.uspto.gov/ip-policy/economic-research/research-datasets/artificial-intelligence-patent-dataset), [ODP bulk API/access requirements](https://data.uspto.gov/apis/bulk-data/search).
- **Unit / coverage:** Patent/application, inventors/assignees, technology classes, full text and government-interest statements. Current PatentsView page says grants/pre-grant downloads run through December 31, 2025. AIPD labels documents published 1976–2023 using a model.
- **Format / joins:** Research-grade disambiguated/long-text downloads; AIPD CSV/Stata. Patent/application numbers, assignee IDs/names and government-interest contract numbers are join candidates, with extraction/entity-resolution errors. PatentsView has moved to ODP; old endpoints should not be presumed operational.
- **Access caveat:** ODP announces account registration from June 18, 2026 and API keys. AIPD now generates temporary signed download URLs rather than ordinary direct downloads. No login, new key or bulk download attempted.
- **Meaning:** Claimed invention and sometimes government-funding provenance. Not a procurement record, spending total, production readiness or deployment. AIPD classification is probabilistic and ends earlier than current patent data.

### 17. SEC EDGAR and public-company filings — supplier context

- **Official access:** [EDGAR data APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), [access/index guide](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data).
- **Unit / coverage:** Filer submissions and financial facts; 10-K/10-Q/8-K narratives/exhibits can disclose government segments, material contracts, backlog, R&D, acquisitions and risk. Filing indexes extend from 1994Q3; XBRL required from 2009.
- **Format / joins:** Public JSON submissions/company-facts APIs without keys, HTML/inline-XBRL filings and nightly bulk ZIPs; CIK, accession number, ticker/current/former company names. CIK-to-UEI/CAGE requires a separate entity crosswalk; parent/subsidiary relationships matter.
- **Freshness / limits:** JSON updates as filings disseminate; bulk nightly around 3 a.m. ET. Public reporting companies only for much financial detail; private vendors are sparse. Company-facts APIs omit custom-taxonomy and non-entity-wide facts, so segment/backlog details often require the actual filing.
- **Meaning:** Supplier-reported commercial/financial context. Backlog includes definitions, options and estimates that differ by firm; revenue is not federal obligations. A company’s statement should not substitute for an agency’s award or deployment record.

## Optional, low-priority discovery only: licensing catalogs

[Federal Laboratory Consortium’s public FLC Business explanation](https://federallabs.org/flc-business/flc-business-faqs) verifies free no-login browsing of federal technologies, facilities and equipment. [NNSA technology transfer](https://www.energy.gov/nnsa/technology-transfer-1) links selected maturation projects and commercialization material. These can identify technology/patent names, labs and licensing opportunities, but no complete transaction-level license/royalty dataset or bulk API was verified. An “available for licensing” entry is an offer, not an executed license, investment or military deployment. Use as a supplementary pointer rather than a core investment table.

## Shared interpretation rules

1. Preserve the evidence type: **solicitation/selection intent; awarded R&D; internal project expenditure; output/publication/patent; pilot/test; fielded/operational use; supplier disclosure.** Do not merge them into a single “investment” amount.
2. Preserve original identifiers and source dates. Program acronyms, names and vendors support fuzzy linkage; they do not establish unique matches. Many research reports cite a laboratory-wide contract, and one project can generate many outputs.
3. Preserve agency/mission boundaries: homeland security, criminal justice, nuclear security, civil aerospace and energy are relevant neighbors, not automatically military activity.
4. Absence from public data does not establish absence of a program or expenditure. Classified/controlled work, reporting exemptions, withheld fields, maintenance and lags are substantial blind spots.
5. Where a live request failed, the status above distinguishes **publisher-confirmed maintenance** from **retrieval-tool limitations**. Large exports and token-gated APIs remain untested rather than “working” by assumption.
