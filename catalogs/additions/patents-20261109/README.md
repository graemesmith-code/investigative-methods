# Patent bulk data for investigative reporting

- **Rabbit addition:** RAB-PATENTS-20261109
- **Reviewed:** 9 November 2026
- **Inventory:** 12 access-route entries. Several use the same underlying records and are not independent corroboration.
- **Status:** Official documentation and published access conditions reviewed. No bulk collection, account creation, credential generation, purchase, provider outreach or authenticated API test.
- **Files:** [Machine-readable source review](sources.json), including coverage, authentication, cost, limits, original SYS crosswalk and verification limits.
- **Context:** [Rabbit guide](../../README.md). This dated supplement preserves the original exports, IDs and historical totals.

## Rabbit already covers patents

[Volume 1](../../../references/rabbit/originals/Rabbit2%281%29.txt) contains **SYS-0252 PatentsView** and **SYS-0253 EPO Open Patent Services**. [Volume 3](../../../references/rabbit/originals/Rabbit4.txt) adds **SYS-0766 WIPO PATENTSCOPE**, **SYS-0772 USPTO Patent Public Search**, **SYS-0774 USPTO Assignment Search** and national services including CIPO, IP Australia, J-PlatPat, CNIPA, KIPRIS, UK IPO, INPI and DPMAregister.

The gap is in current bulk-access instructions, not the existence of patent coverage. Many national entries describe manual search rather than a verified mass-download route. This review is selective, not an audit of every national patent office.

## Important changes and choices

**Start with US PatentsView bulk tables for a manageable research dataset, and DOCDB for international bibliographic/family discovery. Add full text only where the reporting question needs it.** The US AI Patent Dataset can supply candidate labels for historical research, with human checks.

- **PatentsView has moved to ODP.** USPTO announced a temporary pause of legacy search and APIs from 20 March 2026. This review did not verify their resumption. Use the current bulk products rather than assume the old API is available. [Migration notice](https://content.govdelivery.com/accounts/USPTO/bulletins/40e8c67)
- **ODP is account-gated.** USPTO registration became required from 18 June 2026; API access has its own key process. No login, identity verification or key was attempted. [Official access notice](https://www.uspto.gov/subscription-center/2026/uspto-open-data-portal-require-registration-access-beginning-june-18-2026)
- **EPO has several free bulk products.** Its current list includes DOCDB, INPADOC, EP full text, EBD and Register data. Free pricing does not remove the license conditions. [Current product list](https://www.epo.org/en/service-support/ordering/patent-information-products)
- **PATENTSCOPE is not a bulk-harvesting route.** WIPO prohibits robots and bulk downloads from the search system; licensed PCT products are separate. [Official FAQ](https://www.wipo.int/en/web/patentscope/faqs_patentscope)

## Choose the layer needed

| Route | Best use | Main constraint |
|---|---|---|
| 01. USPTO ODP raw full text | Reproduce searches across published US applications and grants | Account access, historical format changes and current download limits need checking |
| 02. PatentsView tables and long text | Link inventors, organizations, technology classes and government-interest statements | Research data with modelled links; current page reports through December 2025 |
| 03. US AI Patent Dataset | Build a historical AI candidate set | Covers 1976–2023; AI labels do not identify weapons |
| 04. EPO DOCDB | Worldwide titles, abstracts, citations and families | No full text/images; backfile about 200 GB zipped |
| 05. EPO INPADOC | Add legal-event timelines | Reporting varies by authority; verify important status claims nationally |
| 06. EP full text | Search descriptions and claims in EP publications | Full backfile about 3.53 TB zipped; Euro-PCT text gaps |
| 07. EBD | Follow weekly EP publication and bibliographic changes | Not a complete cumulative history |
| 08. EP Register bulk | Study procedural history | Snapshot excludes the underlying All documents collection |
| 09. PATSTAT / TIP | Relational statistical analysis | Free TIP and conditional bulk access differ from legacy paid PATSTAT Online |
| 10. EPO OPS | Targeted enrichment and bounded document retrieval | OAuth, weekly volume allowance and fair-use throttles |
| 11. Google BigQuery public patent tables | Search and join without hosting the full corpus | Compute can cost money; dataset freshness not tested |
| 12. WIPO licensed PCT products | Fill PCT text or document gaps | Product-specific payment and reuse rights |

The full IDs run from RAB-PATENTS-20261109-01 to -12. Follow each record's source links before a new collection. Listed sizes are approximate publisher descriptions, not measured downloads.

### EPO reuse warning

The [database license](https://www.epo.org/en/service-support/ordering/raw-data-terms-and-conditions) permits internal use and qualifying derived products, but restricts redistribution of the database or data as such. It requires attribution and security measures, and includes subscription/renewal provisions even where the current price is free. Confirm the applicable agreement before ordering. Do not commit acquired bulk records to a public repository on the strength of this catalog entry.

## A future mass-search workflow

1. **Fix the question and population.** Select named employers, subsidiaries, programmes, countries and a date range. For AI-weapons reporting, keep broad AI terms separate from military context, and distinguish a company-wide patent from evidence about a particular product or contract.
2. **Start with a small known set.** Use patents already independently identified as relevant and several non-military AI controls. Compare keyword, CPC/IPC and AI-dataset approaches. Record missed known examples before scaling.
3. **Acquire a bounded licensed snapshot.** Preserve provider, release, publication/application number, country, kind code, language, original file, hash and retrieval date. Record failed downloads and missing fields. Use bulk files and documented APIs; stop at access refusals. Numeric limits that remain unverified in this review must be checked first.
4. **Search fields separately.** Index title, abstract, claims and description locally. Retain the exact matching passage and query version. Keep source-language text alongside any translation, and distinguish applicant assertions from examiner or legal findings.
5. **Deduplicate by a declared family rule.** Count publications, applications and families separately. Preserve priority, filing, publication, grant and event dates as distinct fields. Publication lag means recent years cannot be compared naively with mature years.
6. **Resolve people and companies cautiously.** Preserve applicant/assignee names as filed, proposed corporate matches and confidence. Use separate assignment records and national registers for material ownership claims. Do not treat disambiguated IDs as proof of common ownership.
7. **Corroborate the reporting lead.** Join patent government-interest references, named contractors and technology descriptions to contracts, budget documents, technical papers, tests and job postings. A patent claim does not establish deployment, military use, a working capability, funding receipt or wrongdoing.

Keep secrets, unpublished applications and personal contact information outside the collection design. Export only what is needed for reporting and what the provider's terms allow. This is a proposed workflow; no patent screen or finding about a company was produced here.

## Verification limits and next check

ODP product pages and EPO's bulk-distribution application did not expose readable file listings through the research tool. The official documentation supports their existence, but successful download, payload completeness, current credentials and numeric ODP quotas remain untested. Google BigQuery tables were not queried; the example repository's April 2026 archival date alone does not prove that the data stopped updating.

The smallest useful next experiment is one authorized US research-table slice plus a few known patent records, with a coverage and family-deduplication check before a larger download. No paid subscription or cloud-compute commitment is needed to decide that scope.
