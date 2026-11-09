# Research funding, outputs and tests for AI weapons reporting

- **Rabbit addition:** RAB-AIWEAPONS-20261109
- **Reviewed:** 9 November 2026
- **Inventory:** 26 source/route reviews: 24 named collection reviews, including unavailable DTIC, plus SAM/USAspending maintenance and a Crossref access correction. These are not 26 newly verified APIs or new global SYS records.
- **Files:** [Full structured register](sources.json) and [spreadsheet-ready CSV](sources.csv). Each record includes access limits, join keys, cautions, current verification and historical checks.
- **Scope:** Public-source investigative reporting about research intentions, funding, outputs, demonstrations and transition. No new full dataset ingestion, authenticated API test, account/key creation, purchase or provider outreach.

The AI-weapons work exposed a gap between transaction data and evidence of what research produced. SBIR abstracts, program documents, technical outputs and test accounts can explain a project that has only a generic spending description. Institutional surveys and audits add financial context around universities, laboratories and nonprofits. Keep these evidence types distinct: a research goal, award, paper, accessible code release, accepted deliverable, demonstration and fielded capability are different findings.

This addition reconciles selected gaps from the [89-entry source register](../../../research/2026-10-16/future-warfare-investments/track-1-data-universe/SOURCE_REGISTER.csv) and [37-route bulk register](../../../research/2026-10-16/future-warfare-investments/track-1-data-universe/BULK_ACCESS_REGISTER.csv). It does not import all those rows as new Rabbit systems. The original 1,555 SYS records, 2,516 AP records, exports and historical verification dates remain unchanged.

## Start with these structured sources

| Local entry | Source | Practical route and main limit |
|---|---|---|
| 01 | [SBA SBIR/STTR](https://www.sbir.gov/awards) | Monthly full CSV, advertised 290 MB with abstracts or 65 MB without; search export at most 10,000 rows. API still has a maintenance notice. |
| 02 | [DSIP/service topics](https://www.dodsbirsttr.mil/topics-app/) | Topic/solicitation documents complement awards. DSIP returned 403 today; no uniform bulk API verified. |
| 03 | [DVIDS](https://api.dvidshub.net/docs/search_api) | Keyed search and asset API, 50/page and 1,000-result window. Preserve event, publication and update dates. |
| 04 | [DOE OSTI](https://www.osti.gov/api/v1/docs) | Public research metadata API and documented harvesting routes. Direct documentation failed today; October sample success is historical. |
| 05 | [NASA NTRS](https://sti.nasa.gov/harvesting-data-from-ntrs/) | Public API and separate advertised bulk metadata. API document specifies 500 requests/15 minutes, 100/page and 10,000/query. |
| 06 | [Federal Audit Clearinghouse](https://www.fac.gov/data/download/current/) | Keyless full/year CSV tables; separate keyed API capped at 20,000 results/request. Audits have thresholds and reporting lag. |
| 07 | [NCSES FFRDC R&D](https://ncses.nsf.gov/explore-data/microdata/ffrdc-research-development) | Annual institutional files, latest listed FY2025. Before 2001, coverage is academically administered centers only. |
| 08 | [NCSES HERD](https://ncses.nsf.gov/explore-data/microdata/higher-education-research-development) | Annual institutional CSV/SAS ZIPs, latest listed FY2024; main and short-form populations need separate treatment. |
| 09 | [NCSES Federal Funds R&D](https://ncses.nsf.gov/surveys/federal-funds-research-development/2024-2025/) | Agency/performer/country tables. Keep FY2024 actuals separate from FY2025 estimates. |
| 10 | [NCSES Federal S&E Support](https://ncses.nsf.gov/surveys/federal-support-survey/2024) | Institutional/agency obligation tables, latest reviewed FY2024; not another award ledger to add to USAspending. |

IDs run from RAB-AIWEAPONS-20261109-01 to -26. Published sizes are advertised figures unless the register explicitly identifies an October payload measurement. Today's review did not repeat those historical downloads.

**Retention affects source choice.** [DVIDS terms](https://api.dvidshub.net/docs/tos) require cache updates and removal of withdrawn assets. [NASA's API documentation](https://sti.nasa.gov/docs/20221122_OpenAPI_Documentation.pdf) requires at least weekly redistribution checks and removal/resynchronization when records or documents become unavailable. An unrestricted permanent redistribution archive should not be promised from either route.

## Add program and test documents separately

| Local entry | Collection | What it contributes |
|---|---|---|
| 11–12 | [DARPA](https://www.darpa.mil/research/programs) and [IARPA](https://www.iarpa.gov/research-programs) | Program phases, BAAs, amendments, performers and output links. No comprehensive public award-ledger API established. |
| 13 | [Defense justification books](https://comptroller.war.gov/Budget-Materials/FY2027BudgetJustification/) | R-2/R-2A narratives and procurement details above individual contracts. Current index returned 403; prior sample retrieval is labeled. |
| 14–16 | [DD 1414](https://comptroller.war.gov/BudgetExecution/DD1414_Base_for_Reprogramming_Actions/), [DD 1415](https://comptroller.war.gov/Budget-Execution/ReprogrammingFY2026/) and [DD 1416](https://comptroller.war.gov/Budget-Execution/1416QrtlyRptsfy2026/) | Baseline, reallocations and quarterly program allocations. All three current direct index checks failed; no clean bulk API claimed. |
| 17–18 | [GAO oversight](https://www.gao.gov/products/gao-26-108457) and [DOT&E](https://www.dote.osd.mil/annualreport) | Selected-program cost, maturity and test findings. GAO landing read; DOT&E current PDF indexed, archive fetch 403. |
| 19–20 | [DIU](https://www.diu.mil/solutions/portfolio/catalog) and [AFWERX/SpaceWERX](https://spacewerx.us/accelerate/stratfi-tacfi/) | Prototype outcomes, company/cohort names and transition claims. Separate selections, obligated dollars, ceilings and private matching capital. |
| 21 | [ATI](https://www.ati.org/rd-project-awards/) and [NSTXL](https://nstxl.org/rapidly-delivering-next-generation-space-prototypes/) | Performer clues behind consortium awards. First-party manager disclosures, not complete government ledgers; ATI's table is rolling and reports ceilings. |
| 22–23 | [APFIT](https://ac.cto.mil/apfit/) and [Microelectronics Commons](https://www.cto.mil/ct/microelectronics/commons/) | Selected projects and technology-area sheets. APFIT landing read; Commons government landing now returns 404, so historical PDF checks remain historical. |
| 24 | [DTIC](https://discover.dtic.mil/products-services/) | **Unavailable/discovery-only:** publisher says public reports, publications search and grant search are offline. Controlled access is not a public replacement. |

The [budget inventory](../../../research/2026-10-16/future-warfare-investments/sources/budgets.md) and [procurement inventory](../../../research/2026-10-16/future-warfare-investments/sources/procurement.md) preserve fuller October findings. An access failure in this review is not proof that a publisher permanently removed a resource; only DTIC has the explicit outage notice described above.

## Correct and enrich existing Rabbit entries

**25. SAM is already covered.** SYS-0055 in [the September Rabbit2 revision](../../../references/rabbit/originals/Rabbit2%281%29.txt) already reviews opportunities, attachments, modifications, Other Transactions, subawards and history limits. USAspending SYS-0054/0934 also exists. Retain zero-dollar extensions and negative modifications alongside funded actions. Keep current versus potential end dates and obligations versus options separate. SAM/FPDS and USAspending are overlapping representations. The [current opportunities API](https://open.gsa.gov/api/get-opportunities-public-api/) returns the latest active version; use its documented history route for earlier notice versions.

**26. Crossref's monthly snapshots are not the free tier.** This dated correction supersedes the conflicting SYS-0250/AP-0251 access-price pairing: [Crossref provides a free annual full release, paid Metadata Plus monthly snapshots and an optional requester-pays AWS route](https://www.crossref.org/documentation/retrieve-metadata/bulk-downloads/). The public REST API is separate. The preserved original is not silently rewritten.

Other existing sources need better recipes rather than duplicate entries:

- **Wayback SYS-0133:** compare dated page states and preserve corporate terms; capture timestamps bound observed changes, not the dates decisions occurred.
- **OpenAlex SYS-0249, arXiv SYS-0459, Zenodo SYS-0454, Semantic Scholar SYS-0462 and OpenAIRE SYS-0467:** retain funder/contract identifiers, acknowledgments and output type. Inspect actual accessible files and licenses before describing a release. An empty index search does not establish that no deliverable exists.
- **PatentsView SYS-0252:** current ODP migration/account conditions and government-interest fields are covered in the [same-day patent supplement](../patents-20261109/README.md), rather than duplicated here.
- **Find a Tender SYS-0431 and Sell2Wales SYS-1120:** preserve notice/attachment versions and distinguish planned signature, award and implementation.
- **Federal AI inventory SYS-1487:** its military, intelligence-community and National Security System exclusions prevent treating it as a weapons census.

## A bounded validation workflow

1. Choose known cases and non-military controls before searching a wider population. Record which examples seeded the search.
2. Join topic/BAA, award, institution and output identifiers with explicit confidence. Keep the quoted matching passage and source version; a company-name match is insufficient.
3. Reconcile units and money stages. Requested, enacted, reallocated, obligated, expended, ceiling and private-match amounts belong in separate fields. Neither survey totals nor subawards are automatically additive to prime awards.
4. Build an evidence timeline from intent through output, acceptance, test and transition. Record missing stages without treating public silence as proof of failure or success.
5. Test small permitted slices for coverage, duplicated pages, missing files and historical completeness before scaling. Preserve rights and withdrawal obligations with the source metadata.

The [ASIMOV findings](../../../research/2026-10-25/asimov-collaborative-weapons/evidence/asimov/primary-findings.md) and [software-access review](../../../research/2026-10-25/asimov-collaborative-weapons/evidence/asimov/software-access-review.md) illustrate why these distinctions matter. Adding a catalog source does not establish that an earlier bulk screen independently discovered a pre-seeded lead.

[Rabbit catalog guide](../../README.md) · [Preserved originals and provenance](../../../references/rabbit/README.md)
