# Job postings as an investigative source

- **Rabbit addition:** RAB-JOBS-20261109
- **Reviewed:** 9 November 2026
- **Inventory:** 15 access-route entries across 13 providers. Multiple routes from one provider are not additional independent sources.
- **Status:** Primary documentation and selected public career pages reviewed. No bulk collection, recurring monitor, signup, purchase or outreach was performed. API payload access is not established by this review.
- **Files:** [Detailed machine-readable source catalog](sources.json). Each record contains access status, endpoint, authentication, coverage, pagination, dates, costs/rights, verification limits and primary sources.
- **Catalog context:** [Rabbit guide](../../README.md). Original exports, SYS/AP identifiers and historical totals remain unchanged.

## What to use first

**For a historical baseline, start with USAJOBS bulk metadata plus announcement text, and Sweden's downloadable Platsbanken archive. For contractor hiring, build a selected employer panel using documented public ATS feeds.** Use commercial full-text data only when its coverage and license justify the cost.

ClearanceJobs and ClearedJobs.net are relevant to the subject but their published terms restrict aggregation. Neither should be treated as a ready-made bulk source. A tool sold as a scraper does not supply the missing rights.

| Entry | Route | Practical assessment |
|---|---|---|
| 01 | [Greenhouse Job Board API](https://docs.greenhouse.io/job-board) | Public per-employer JSON with full descriptions; good prospective panel candidate |
| 02 | [Lever Postings API](https://github.com/lever/postings-api/blob/master/README.md) | Public per-employer JSON, paged with skip/limit; search locally |
| 03 | [Ashby public postings](https://developers.ashbyhq.com/docs/public-job-posting-api) | Per-board published jobs; exclude direct-link-only listings |
| 04 | [Ashby partner feeds](https://developers.ashbyhq.com/docs/dedicated-partner-job-feeds) | Hourly JSON/XML, but partner approval and employer opt-in required |
| 05 | [SmartRecruiters Posting API](https://developers.smartrecruiters.com/docs/endpoints) | Public company list/detail route; keep internal-posting access out of scope |
| 06 | [USAJOBS historic metadata](https://developer.usajobs.gov/api-reference/get-api-historicjoa) and [full text](https://developer.usajobs.gov/api-reference/get-api-announcementtext) | Explicit no-key bulk endpoints; useful federal hiring baseline |
| 07 | [USAJOBS current Search](https://developer.usajobs.gov/api-reference/get-api-search) | Key required; capped queries, not the preferred historical export |
| 08 | [Swedish historical files](https://data.arbetsformedlingen.se/annonser/historiska/) and [JobStream](https://data.arbetsformedlingen.se/dataservice/jobstream/) | CC0 archive and change feed; strong open European option |
| 09 | [ClearanceJobs](https://about.clearancejobs.com/terms-of-service) | Permission required for mass retrieval/indexing; no public export located |
| 10 | [ClearedJobs.net](https://clearedjobs.net/site-terms) | Aggregation restricted; negotiate a feed before collection |
| 11 | [Adzuna](https://developer.adzuna.com/docs/search) | Search API returns description snippets; research licensing and attribution conditions apply |
| 12 | [LinkUp](https://www.linkup.com/products/custom-feeds) | Commercial full/differential files; candidate for cross-employer full-text coverage |
| 13 | [Lightcast](https://docs.lightcast.io/lightcast-api/reference/overview-global-job-postings) | Commercial posting search and historical filters; verify entitlement and source evidence |
| 14 | [Coresignal](https://docs.coresignal.com/api-introduction/requests/bulk-collect/get-requests) | Commercial API plus prepared bulk files; verify chosen product and credits |
| 15 | [NLx Research Hub](https://nlxresearchhub.org/data-access) | New requests paused for a 2027 transition; current confidentiality terms also constrain reporting |

The complete IDs are RAB-JOBS-20261109-01 through -15. Status labels in sources.json distinguish documented access from agreement-dependent or paused routes. A free key, public endpoint or readable page is not a blanket license to collect, retain or republish all content.

## How to mass-search in a future investigation

### 1. Define a population that can be measured

Start with a fixed employer panel and a dated question, for example: **Which suppliers began advertising for AI-related work in a named military programme, and what changed before and after a documented contract award?**

Maintain an employer register with legal and trading names, subsidiaries, verified career URL, ATS provider, board token, geography, date verified and reason for inclusion. Use registries and procurement records to resolve corporate identity. Staffing firms and primes may advertise for the same end customer; retain that uncertainty.

Seed routes observed during this review include Anduril's Greenhouse board token `andurilindustries` and [Palantir's Lever board](https://jobs.lever.co/palantir), token `palantir`. [Helsing's own jobs page](https://helsing.ai/jobs) is another relevant discovery lead, but no ATS token is assigned here. Verify every employer-to-board link before collection. These examples do not imply misconduct or show that any particular vacancy concerns a weapon.

### 2. Acquire once, search locally

For each route, clear the stated access and reuse conditions first. Request public job advertisements only. Applicant profiles, resumes, internal jobs and recruiter messages are outside this design.

- For USAJOBS, collect bounded agency/date windows from both historical endpoints, follow the returned continuation links, then join metadata and text by control number. Log missing joins.
- For Swedish history, choose only the necessary years or quarters and one appropriate version of each file. Use a current snapshot plus JobStream changes for prospective coverage.
- For employer ATS feeds, resolve a known board and retain complete authorized responses at a modest, documented cadence. A daily interval is a proposed starting point, not an established permission or a monitor created by this task.
- For a licensed vendor, request a small employer/date coverage sample before buying a larger export. Ask for full descriptions, stable IDs, original URLs, historical versions, update/removal events and permission for evidence retention and publication.
- Follow documented pagination, respect response limits and Retry-After, cache when supported and stop on access refusals. Record failed requests and interrupted pages instead of silently reducing the count. No bypasses or guessed private endpoints.

Use SQLite full-text search, DuckDB or another local index over approved text. This avoids sending every search back to a provider and lets a reporter rerun the same query against a dated snapshot. Implementation and an end-to-end collection test remain future work.

### 3. Preserve observations and versions

Keep source fields separate from derived fields. The minimum useful schema is:

| Group | Fields |
|---|---|
| Identity | source/provider, employer/board, source posting ID, requisition ID when available, canonical/source URL, location(s) |
| Text | title, duties, requirements, other description sections, original language, content hash, raw-response reference |
| Source dates | publication, update and closing dates exactly as supplied, with their documented meanings |
| Observation dates | fetched_at UTC, first_seen, last_seen, last_successful_board_fetch, absent_on_successful_fetch |
| Provenance | exact request without credentials, retrieval status, page/cursor, expected/received totals, collector version, terms-review date |
| Analysis | employer-match confidence, duplicate-cluster ID, matched terms and evidence passage, classification reason, human-review status |

Preserve new content hashes as versions instead of overwriting text. A disappearance after a successful complete response is an observed removal, not a confirmed hire. An outage, truncated page, changed board token or missing employer is **unknown**, not zero hiring. Reappearance may be a repost rather than a new role.

Count both raw advertisements and deduplicated requisitions, with the method disclosed. Different locations, languages and aggregators may repeat one requisition. One advertisement may recruit several people; some are evergreen, contingent on contract award or only expressions of interest. Neither ad count nor vacancy removal measures actual hires.

Never use a present-day revised ad as though that text was known at an earlier date. Provider publication dates, first observation, most recent publication and most recent modification are separate facts. Preserve time zones and the date precision actually available.

### 4. Search the work, not just the word “AI”

Run separate broad and narrow searches, retaining the query version and matched passages.

- **AI methods:** artificial intelligence, machine learning, computer vision, perception, sensor fusion, reinforcement learning, autonomous systems, multi-agent, edge AI.
- **Military context:** defence/defense, national security, military customer, mission systems, ISR, command and control, counter-UAS, targeting, weapon integration and programme/product names.
- **Corroborating context:** clearance requirement, named customer, contract identifier, test site, deployment team, export-control language or explicitly contingent funding.
- **Non-weapons controls:** AI used in recruiting, finance, general enterprise support or marketing; a military employer's generic company introduction; ambiguous words such as “target” and “mission”.

Require meaningful context in duties or requirements rather than a match only in repeated corporate boilerplate. Do not require a clearance keyword for every candidate: relevant European, commercial-dual-use and unclassified jobs may omit it. Conversely, clearance alone says little about AI or weapons.

Use local-language terms and reviewed translations when extending outside English. Report exact-match and semantic results separately. If a model helps classify passages, retain the original evidence, model/version and review outcome; do not feed restricted text into an external service without the necessary rights and authorization.

Review a sample of both hits and non-hits. Record false positives and missed known examples before expanding the panel. A useful output is a dated employer/programme/skill table with linked evidence and uncertainty, not a ranking of supposedly secret weapons projects.

### 5. Corroborate the lead

A posting supports the narrow claim that an employer advertised particular work at an observed time. It does not establish delivery, operational deployment, actual hiring, technical performance or unlawful conduct.

Check the strongest leads against contracts and amendments, budget lines, company filings, patents, product announcements, tests and public statements. Match dates, legal entities and programme identifiers. A change in ad language may reflect a template revision, ATS migration or recruitment strategy rather than a programme change.

Useful reporting questions include whether an advertised capability predates a public announcement, whether a named programme appears across several suppliers, and whether engineering demand shifts after a contract. Each needs independent records and a chance for affected parties to explain before publication. No outreach has been initiated.

## Access and verification ledger

This pass read provider documentation, terms and selected public pages. It did not download a job corpus or test completeness. Two bounded API attempts, a Palantir Lever request with limit=1 and a single Anduril Greenhouse job, were not retrievable through the web tool. That is a tool-result limitation, not evidence that those APIs are down.

Commercial prices and negotiated rights are unverified. No trial plan, API key, partner feed or data-use agreement was accepted. No automated monitor was scheduled. No personal candidate data, credentials or full third-party advertisement text is included in this public addition.

Before implementing a collector, recheck current documentation and terms, verify a small known-positive sample, reconcile counts and pagination, and test additions, edits, removals and failed fetches. Keep the resulting raw evidence in an appropriately restricted research store; publish only what the applicable rights and reporting purpose support.

[Back to Rabbit](../../README.md) · [Detailed source records](sources.json)
