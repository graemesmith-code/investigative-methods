# Overseas-security and acquisition-context source additions

Verified 2026-10-16. This is a supplement to the existing 60-source register, not a replacement or a new estimate of investment. There are 11 distinct proposed additions plus one substantive refinement of FW-C10. A source is included because actual records exist; an indexed record is clearly distinguished from a successfully retrieved file/API.

## Best first additions

1. Microelectronics Commons: small official project sheets join money, lead/hub, readiness and technology well below broad budget lines.
2. APFIT: cohort lists and implementation reports connect procurement-transition selections to sponsors, companies, quantities and delivery plans.
3. DSCA SAMM Appendix 1: 1,246 equipment-rate/identity rows, especially useful for MASL/system crosswalks. Rates must never be counted as investment dollars.
4. IBP Investment Intelligence Center: unusually valuable DPA/IBAS portfolio, but production host is returning 502 in this environment. It is not yet an access-verified bulk source.
5. Security Force Monitor: the strongest technically bulk-ready foreign-assistance addition, although historical training is generally contextual.

## Financial interpretation

Keep at least these distinct: budget request, project selection, award/ceiling, obligation, commercial-export authorization, shipment, stockpile sale, per-item recoupment charge, and reported training cost. In particular, neither foreign sales nor recoupment rates are additive U.S. R&D spending. Domestic place of performance can support an overseas military mission; generic domestic public-service spending remains out of scope.

## OS-01 — Industrial Base Policy Investment Intelligence Center: DPA and IBAS portfolio

Priority: P1 · NEW · INDEXED_ONLY;DIRECT_FETCH_502

- **Primary URL:** https://www.businessdefense.gov/investments.html
- **Additional exact URLs:** https://www.war.gov/News/Releases/Release/Article/4525699/department-of-war-launches-interactive-investment-intelligence-center-tracking/
- **Unit:** Investment/project
- **Coverage:** Since 2015; current indexed page advertises 11-year horizon
- **Format:** Interactive HTML map, Mekko chart and portfolio explorer; no backing CSV/JSON verified
- **Join keys:** Project/title; vendor; date; funding source; place; sector; no PIID verified
- **Access test:** Official indexed page shows 427 investments, $9.85B, 300+ places, and DPA/IBAS plus location/sector/date filters. Both apex and www page requests returned HTTP 502, as did the home page. Do not label bulk ready.
- **What a record proves:** Government-reported industrial-base investment portfolio and capability purpose; the exact financial definition of each value requires checking its field label.
- **Limits:** Changing snapshot; headline total is not new annual spending. Manufacturing capability investments can overlap USAspending and press releases. Current record fields and export semantics not directly verified.
- **Free bulk opportunity:** High-value next recovery target: inspect the publicly served portfolio data when production page works; do not assume an API or scrape the search cache as the full universe.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** Military production capacity, critical materials, batteries, microelectronics/comms/sensors, unmanned systems. Indexed regions include US, Canada, UK, New Zealand; retain national-security mission rather than requiring foreign place of performance.

## OS-02 — Microelectronics Commons project-by-technology-area disclosures

Priority: P1 · NEW;DEEPENS_CONSORTIUM_LAYER · RETRIEVED_HTML_AND_PDF

- **Primary URL:** https://www.cto.mil/ct/microelectronics/commons/
- **Additional exact URLs:** https://www.cto.mil/wp-content/uploads/2025/04/Quantum-Technology-Q-Projects.pdf ; https://www.cto.mil/wp-content/uploads/2025/04/Electromagnetic-Warfare.pdf ; https://www.cto.mil/wp-content/uploads/2025/04/Secure-Edge-1.pdf
- **Unit:** Named prototype project with amount, lead/hub and technical objective
- **Coverage:** Public sheets posted April 2025; project narratives include FY2025-26 work; later revisions require versioning
- **Format:** Six technology-area PDF lists linked from official HTML; sample quantum PDF is 3 pages, 138945 bytes
- **Join keys:** Project acronym/full title; hub; lead company/lab; named partners; document date/page
- **Access test:** Official page and quantum/EW/secure-edge PDFs retrieved. Independent HTTP GET of quantum sheet returned 200 application/pdf. Quantum sample identifies CHIQPI, QUPICS and other funded projects; EW sample contains named performers and readiness objectives.
- **What a record proves:** Publicly disclosed funding and research/prototype scope that often sits below umbrella consortia and broad budget lines.
- **Limits:** Amounts are disclosed project funding, not transaction obligations. Same project can appear twice or under multiple categories/years. EW PDF repeats EPIC-BEAMS with different amounts, so no blind summing. Targets are not achieved performance.
- **Free bulk opportunity:** Download six short PDFs, parse headings/amounts/leads and retain per-page source evidence; supplement hub/year-2 announcements after deduplication. No API needed.
- **License/access:** PDFs explicitly carry Distribution Statement A, approved for public release/unlimited distribution. No dataset-specific machine-readable license found.
- **Scope:** Quantum/PNT, EW, RF communications, 5G/6G, secure edge, sensors, microelectronics fabrication and packaging, plus AI hardware. Do not classify entire Commons as AI.

## OS-03 — APFIT selected-project cohorts and biannual implementation reports

Priority: P1 · NEW;SPECIFIC_PROGRAM_DISCLOSURE · RETRIEVED_HTML_AND_PDF

- **Primary URL:** https://ac.cto.mil/apfit/
- **Additional exact URLs:** https://calvert.house.gov/sites/evo-subsites/calvert.house.gov/files/evo-media-document/20230321-apfit-biannual-report.pdf ; https://www.war.gov/News/Releases/Release/Article/4544621/department-of-war-issues-final-fy26-apfit-awards-surpassing-2-billion-milestone/
- **Unit:** Selected procurement/transition project; implementation milestones where reported
- **Coverage:** FY2022 onward; March 2023 implementation report and July 14 2026 cohort verified
- **Format:** HTML cohort bullet lists plus congressional PDF implementation reports; overview uses image-based metrics
- **Join keys:** Project title; fiscal-year cohort/cycle; service/CCMD sponsor; performer; award date if given
- **Access test:** Program landing HTTP 200. March 21 2023 PDF HTTP 200, 603542 bytes. July 14 2026 official release retrieved with 24 procurement selections and six software selections; excludes classified selections.
- **What a record proves:** Funding selection and sponsor; historical implementation report adds companies, actual award dates, quantities and delivery plans.
- **Limits:** Selection amount is not the same as obligated award value or delivery completion. Project list and program headline figures need as-of dates; homepage can lag newer releases. No comprehensive PIID field or full current biannual archive verified.
- **Free bulk opportunity:** Collect cohort pages as small structured lists; extract historical report project sections. This is much more specific than generic press-release monitoring.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** Autonomy, resilient communications/PNT, EW, undersea sensors, expeditionary energy/manufacturing, logistics and selective software. Historical report can connect prototype to first production.

## OS-04 — State SFOPS Congressional Budget Justifications, including diplomatic security and overseas technology

Priority: P1 · NEW · INDEXED_ONLY;STATE_FETCH_BLOCKED

- **Primary URL:** https://2021-2025.state.gov/fy-2025-international-affairs-budget/
- **Additional exact URLs:** https://2021-2025.state.gov/wp-content/uploads/2024/04/FY25-Congressional-Budget-Justification-FINAL_03052024.pdf ; https://www.state.gov/wp-content/uploads/2025/05/FY-2026-State-CBJ-.pdf ; https://2021-2025.state.gov/wp-content/uploads/2022/06/FY-2023-Congressional-Budget-Justification_Final_508comp.pdf
- **Unit:** Account/bureau/subprogram request and prior-year comparison
- **Coverage:** Annual historical vintages; FY2023 and FY2025 indexed narrative inspected, FY2026 official file linked by CRS; FY2027 State file not established
- **Format:** PDF main CBJ, diplomatic-engagement Appendix 1, other appendices and supplementary foreign-operations tables
- **Join keys:** Fiscal year and vintage; appropriation/account; bureau; subprogram; country in assistance tables; page
- **Access test:** FY2025 official index names all appendices. Indexed FY2023 CBJ specifically identifies C-UAS, intrusion-detection modernization and security-engineering increments; FY2025 identifies INR technology-office resource realignment. Direct main PDF/index gives technical-difficulties/forbidden; FY2026 direct PDF 403.
- **What a record proves:** Requested resources and narrative changes for WSP/Diplomatic Security, INR, cyber/communications, embassy security and foreign military assistance.
- **Limits:** Budget is not obligation. Organizational transfers can masquerade as cuts/increases. Whole WSP/embassy account cannot be tagged novel technology. Appendix/year completeness and latest FY2027 availability not verified.
- **Free bulk opportunity:** Annual books form a free text/table corpus once access works; detailed Appendix 1 is important. No public CBJ API or clean all-year machine export verified.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** Overseas diplomatic protection, counter-UAS, secure communications, cyber, intelligence technology, overseas facilities. Filter away general diplomatic administration.

## OS-05 — State OBO recently completed overseas facility project portfolio

Priority: P2 · NEW · RETRIEVED_HTML;API_DENIED

- **Primary URL:** https://oboportfolio.state.gov/recently-completed/
- **Additional exact URLs:** https://oboportfolio.state.gov/obo-projects-portfolio/ ; https://oboportfolio.state.gov/chiang-mai/
- **Unit:** Embassy/consulate project fact sheet
- **Coverage:** Rolling recently completed list; 21 linked project cards observed; example completed 2025
- **Format:** HTML project pages, project budget and performance narratives
- **Join keys:** Mission/city/country; project title; contractor; completion year; URL
- **Access test:** Index and Chiang Mai page retrieved. Example provides $273M project budget, contractor, completion year and building-performance systems. WordPress pages endpoint test returned 401 Unauthorized; no API access claimed or further probing attempted.
- **What a record proves:** Overseas infrastructure project scope, disclosed budget, participants and reported completion.
- **Limits:** General buildings are contextual only; include novel security/resilience technology only when stated. Project budget is not all technology spend. All-projects/planning page is under construction; under-construction-projects URL returned 404.
- **Free bulk opportunity:** Small public HTML corpus can be collected from the working recently-completed links. No working public REST export verified.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices. Credited photography is separate from factual project data.
- **Scope:** Overseas diplomatic facilities, resilient energy/controls and security infrastructure. Useful bridge to State CBJ and USAspending using contractor/location/time.

## OS-06 — DDTC Section 655 Direct Commercial Sales authorizations and shipments

Priority: P2 · NEW;COMPLEMENTS_FMS · RETRIEVED_HISTORICAL_PDF;CURRENT_INDEXED_ONLY

- **Primary URL:** https://www.pmddtc.state.gov/ddtc_public?cat=Report&id=ddtc_public_portal_news_and_events&timeframe=12month
- **Additional exact URLs:** https://deccspmddtc.servicenowservices.com/sys_attachment.do?sys_id=06f22f571be4bc90c6c3866ae54bcb3e ; https://www.pmddtc.state.gov/deccs?id=ddtc_public_portal_news_and_events&p=4
- **Unit:** Country/territory/organization by USML category and report fiscal year
- **Coverage:** Annual historical reports; FY2020 data sample verified; FY2024 and FY2025 current reports indexed
- **Format:** PDF tables. FY2020 search title says .xlsx but actual response is PDF, 30 pages, 717056 bytes
- **Join keys:** Report FY; country/organization; USML category/subcategory; quantity; authorized value; shipped value
- **Access test:** FY2020 attachment GET returned HTTP 200 application/pdf and PDF magic bytes. Current public portal loads only a JS shell in plain fetch; official indexed page lists FY2025 report (857KB) released May 26 2026 and FY2024 (672KB) April 25 2025.
- **What a record proves:** Authorized commercial export value and reported shipment value; distinct from government-to-government FMS notifications.
- **Limits:** Neither approvals nor shipments are U.S. government R&D investment; authorizations may never be used and shipments need not derive from licenses issued that year. Coarse USML categories cannot isolate novel technologies. No vendor-level licensing ledger.
- **Free bulk opportunity:** Country/category PDF extraction, one file per year. Do not advertise XLSX just because title contains .xlsx; use response type. No bulk API verified.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** Exported defense electronics, sensing, space, aircraft and other articles; contextual demand/technology-transfer layer.

## OS-07 — DSCA SAMM Appendix 1 nonrecurring-cost recoupment dataset

Priority: P1 · NEW;ENTITY_AND_COST_CONTEXT · RETRIEVED_HTML;HTTP200

- **Primary URL:** https://samm.dsca.mil/appendix/appendix-1
- **Additional exact URLs:** https://samm.dsca.mil/appendix/appendix-1-usml11
- **Unit:** Major-defense-equipment recoupment-charge row
- **Coverage:** Living table; sample effective dates span 1970s-2026; historical rates partly preserved
- **Format:** HTML complete listing plus USML-category tables; index advertises 1246 records, military electronics 143
- **Join keys:** MASL; system; model; item; category; effective date; special-country note; policy-memo number
- **Access test:** Index/category table retrieved. Military-electronics page HTTP 200, 438049 bytes. Columns include current/prior charge, effective/expiration dates, notes and policy-memo links.
- **What a record proves:** Published per-item nonrecurring-cost recovery charge plus equipment identity/version and policy change.
- **Limits:** Charge is neither unit procurement price nor total R&D cost/spending. MASL can repeat for special-country rates and revisions; nulls and expired rows exist. Deduplicate by composite key and preserve notes.
- **Free bulk opportunity:** Parse finite HTML category tables or complete-list link. No authentication needed for tested table. Excellent lookup corpus; no JSON/CSV export claimed.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** MASL/NSN-like crosswalk for radars, EW, C-UAS, guidance, sensors, communications and platforms. Strong enrichment, not a spend ledger.

## OS-08 — DSCA SAMM generic-code and security-cooperation authority/fund-code crosswalks

Priority: P2 · NEW;LOOKUP_TABLES · RETRIEVED_HTML

- **Primary URL:** https://samm.dsca.mil/appendix/appendix-4
- **Additional exact URLs:** https://samm.dsca.mil/appendix/appendix-4-h ; https://samm.dsca.mil/program/S333 ; https://samm.dsca.mil/program/MSI
- **Unit:** Equipment generic-code or program/fund-code reference row
- **Coverage:** Current living references with policy-memo revisions; Section 333 table includes recent appropriation fiscal years
- **Format:** HTML linked generic-code tables and program-specific fund/authority tables
- **Join keys:** Three-character generic code; budget activity/project; program authority; fund code; Treasury account/FY; policy memo
- **Access test:** Appendix 4, communications code table and Section 333 page retrieved. S333 table maps codes to appropriation years and expiry/cancellation periods.
- **What a record proves:** Classification/authority relationships necessary to interpret assistance cases and prevent fund-year/country-code errors.
- **Limits:** Not public award or notification microdata. Do not infer that SOCIUM/DSAMS case crosswalks are publicly downloadable just because the manual describes them. Snapshot changing codes.
- **Free bulk opportunity:** Small finite HTML table corpus; preserve expired/reused code versions and source date. No standalone bulk API verified.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** Equipment classes including R&D, communications and construction; Section 333 and Indo-Pacific maritime-security authority context.

## OS-09 — Security Force Monitor foreign military training dataset

Priority: P2 · NEW;BULK_READY_CONTEXT · SAMPLE_API_HTTP200;BULK_LINK_VERIFIED_NOT_DOWNLOADED

- **Primary URL:** https://trainingdata.securityforcemonitor.org/
- **Additional exact URLs:** https://trainingdata.securityforcemonitor.org/state-department-data ; https://trainingdata.securityforcemonitor.org/state-department-data/training-data.json?_size=1 ; https://trainingdata.securityforcemonitor.org/state-department-data.db
- **Unit:** Foreign training activity extracted from State/DoD annual reports
- **Coverage:** Homepage describes 2001-2021; actual sampled row is FY2000/1999-2000 report. Last substantive report update 2020-21; reprocessed in 2024
- **Format:** Datasette JSON, CSV, SQL and downloadable SQLite DB advertised 556.3MB; 255007 main-table rows
- **Join keys:** training:id:admin UUID; country ISO3; program/course; units; dates; source/citation IDs; original source URL/page
- **Access test:** GET training-data.json?_size=1 returned 200 JSON, 4345 bytes, count 255007, pagination next_url and license fields. No large database downloaded.
- **What a record proves:** Reported training course, recipient/delivery unit, trainees and cost with original-report provenance.
- **Limits:** Historical context and technology-absorption/training only; exclude ordinary training from novel-capability totals. Date missingness and rows explicitly marked unverified require source checks. Preserve report vintage to avoid repeated planned/actual events.
- **Free bulk opportunity:** Public paginated JSON or CSV; exact full SQLite download link is on dataset page. Use bounded queries first, then download once if ingestion is authorized.
- **License/access:** CC BY 4.0 explicitly verified in site/API. No API key required in sample; published rate limits not found. Avoid costly repeated full-table queries.
- **Scope:** Overseas partner capacity, selected technical/cyber/aviation/sensor training; not a current procurement ledger.

## OS-10 — DLA Strategic Materials annual plans and monthly stockpile transactions

Priority: P2 · NEW · INDEXED_ONLY;DIRECT_FETCH403

- **Primary URL:** https://www.dla.mil/Strategic-Materials/Announcements/
- **Additional exact URLs:** https://www.dla.mil/Portals/104/Documents/Strategic%20Materials/Announcements/3256%20FY24%20AMP_ACQ.pdf?ver=OIWiKRKy4OcCHuS0W3kpGw%3D%3D ; https://www.dla.mil/Portals/104/Documents/Strategic%20Materials/Announcements/3263%20BOA%20All%20January%202025%20Sales.pdf?ver=5gTwGguZ_35BYO--rtK8IA%3D%3D
- **Unit:** Material/unit/FY planned ceiling or material/month sale/award line
- **Coverage:** Index currently shows FY2024-2026, with earlier archive completeness untested
- **Format:** Annual material plan PDF tables and recurring announcement PDFs
- **Join keys:** DLA-SM announcement number; solicitation/amendment; material; unit; month/FY; named company where disclosed
- **Access test:** Indexed annual acquisition plan exposes material/unit/ceiling quantity. Indexed Jan2025 BOA table exposes quantity sold, approximate value and companies. Index and acquisition-plan GET returned 403.
- **What a record proves:** Planned maximum acquisition/disposal quantities or announced stockpile sale quantities/value.
- **Limits:** Stockpile sales are disposals/revenue, not government procurement expenditures. AMP ceilings are potential quantities, not purchases; some company names withheld. Ordinary commodities need a specific defense capability/supply-chain link.
- **Free bulk opportunity:** Finite annual/monthly PDF corpus, inexpensive to extract when accessible. Separate acquisition plans, disposal plans and actual sales in schema.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** Critical defense materials, energetics, batteries, radar/IR substrates and manufacturing dependencies; contextual industrial-base evidence.

## OS-11 — DLA R&D program and active solicitation portfolio

Priority: P2 · NEW;INTENT_TO_AWARD_CROSSWALK · INDEXED_ONLY;DIRECT_FETCH403

- **Primary URL:** https://www.dla.mil/Information-Operations/Research-And-Development/
- **Unit:** R&D program / BAA or contract vehicle
- **Coverage:** Living portfolio; indexed active solicitations span 2023-2030
- **Format:** HTML table of program descriptions, solicitation IDs, date windows, contract types and dollar ceilings
- **Join keys:** Solicitation number; program; date window; contracting office; later PIID links via SAM/USAspending
- **Access test:** Official indexed page describes 14 programs. Sample: strategic-materials BAA SP4701-25-B-0001, Jan2025-Jan2030, $95M; forging BAA SP4701-25-B-0002, $50M. Direct GET returned 403.
- **What a record proves:** R&D acquisition intent and a precise solicitation-to-program crosswalk for finding downstream awards.
- **Limits:** Ceilings are not awards or obligations; programs mix advanced materials with process/logistics modernization. This complements SAM opportunities rather than creating an independent additive spending total.
- **Free bulk opportunity:** Parse small live table; follow exact solicitation IDs in SAM existing universe. No independent award API verified.
- **License/access:** Free public federal source; no dataset-specific license or published API/rate limit verified. Preserve attribution, document vintage, and any third-party rights notices.
- **Scope:** Contested/global logistics, additive manufacturing, strategic/rare-earth materials, digital twins and supply-chain technology; keep ordinary administrative IT separate.

## OS-12 — NSTXL S2MARTS/TReX public project notices with award-status updates

Priority: P2 · REFINEMENT_OF_FW-C10_NOT_NEW_FAMILY · INDEXED_PUBLIC_RECORDS;DIRECT403_TIMEOUT

- **Primary URL:** https://nstxl.org/categories/2022/
- **Additional exact URLs:** https://nstxl.org/categories/s2marts-research/ ; https://nstxl.org/categories/microelectronics-commons/
- **Unit:** Public consortium project/opportunity record
- **Coverage:** Indexed 2022/2023 cohorts and later updates through 2025-26; full archive extent unverified
- **Format:** HTML category archives and project pages; some content explicitly members-only
- **Join keys:** Consortium; project number; project title; awardee(s); award date; RFS date; parent OT if supplied
- **Access test:** Indexed records expose project 22-13 KANAGAWA awardees/date and project 23-07 boron-nitride research award to Purdue (Jan9 2024). Direct category GET 403 and web fetch timeout.
- **What a record proves:** Project-level performer selection and scope, often more granular than consortium-manager federal awards.
- **Limits:** A category archive is not a complete award database; money often absent, pages are mutable, some details require membership. Do not use membership-only data or imply public bulk availability.
- **Free bulk opportunity:** Public HTML/archive parsing where accessible; only narrow record examples verified by indexing. No API/export verified.
- **License/access:** Private consortium-manager source. Public access does not establish an open-data redistribution license; no explicit dataset license verified.
- **Scope:** Trusted microelectronics, photonics, hypersonic test materials, simulation/training and research prototypes. Enrich existing FW-C10 rather than count a second financial universe.

## Promising-looking sources not promoted to a new data universe

- **JCTD / RDER / Defense Innovation Acceleration:** no new complete public project-level feed verified. Existing defense J-books remain the correct ingestion layer. Do not present JCTD as a current stand-alone program without vintage checks: GAO-26-107664 says DIA followed its 2023 cancellation/reorganization. Public RDER summaries and agency execution lines can overlap. Source: https://files.gao.gov/reports/GAO-26-107664/index.html .
- **Foreign Comparative Testing:** public overview PDF retrieved, including aggregate technology/project and transition statistics; no current complete named-project table/API established. Good context, not yet a separate bulk award universe. Sources: https://ac.cto.mil/pe/fct/ and https://ac.cto.mil/wp-content/uploads/2025/08/FCT_101Brief_2025_Approved.pdf .
- **Office of Strategic Capital:** financing announcements and SBIC fund lists exist, but a public complete loan/guarantee/technical-assistance ledger was not verified. Loans, subsidies, guarantees, fund leverage, conditional commitments and private matching capital must remain separate. Start at https://www.cto.mil/osc/ . Existing general release and budget rows can carry available disclosures until an actual portfolio export is verified.
- **Section 333 / 1226:** program guidance and budget lines exist, but no complete current public case-level notification/export dataset was verified. The SAMM describes internal SOCIUM/DSAMS and notification-to-LOA crosswalks; that description is not public access. Public authority/fund-code tables are separately retained as OS-08.
- **CIP Security Assistance Monitor:** its own guide says security-sector-assistance data is not currently publicly displayed and foreign-training detail is available on request. Displayed arms-sale visualizations offer downloads, but the dataset has CC BY-NC-SA 4.0 terms with commercial use prohibited absent agreement. Do not label the entire detailed database free/open bulk. Source: https://internationalpolicy.org/data-guide/ .
- **Test-range / experimentation notices:** not counted as separate additions without a verified structured project or funding corpus. Individual notices belong in the existing SAM opportunities and environmental/oversight universes.
- **DSCA Historical Sales Book / EDA / ForeignAssistance.gov:** already covered by FW-C16 and FW-C17; no duplicate source family added here.

## Probe artifacts and scope of test

Only small samples were retrieved: one 4.3KB training JSON record, public HTML pages, a 603.5KB APFIT report, a 717KB DDTC report and a 139KB quantum project sheet. This source-retrieval pass used no full training database, authenticated API, paid source, membership portal or outreach. Publication of the research materials is a separate authorized step.

The OBO public WordPress pages query returned 401 and was not pursued. Working public HTML had already been retrieved. IBP returned 502 on the production root and investments page. DLA/NSTXL returned 403; these sources stay indexed-only.

Machine-readable companion: overseas_security_sources.csv. HTTP probe metadata: overseas_probe_log.json. Local sample filenames are evidence artifacts, not public user-delivery links.
