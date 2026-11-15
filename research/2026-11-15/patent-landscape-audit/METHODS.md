# AI-weapons safeguards: patent coverage audit
Date: 15 November 2026

## Finding and scope
The October 25 F5 patent register is a targeted seed set, not a plausibly exhaustive patent universe. This November 15 pass broadens discovery and designs the reproducible corpus search still required. It does NOT certify completeness, conduct a patent-validity opinion, establish deployment, or identify every NATO-country filing.

The prior review had 28 input rows, 23 distinct publications and 19 reporting clusters. These are not interchangeable counts. An audit of its Exa log identified 36 patent-directed discovery searches; many assignee searches contained a literal year rather than an enforced date range. No native classification/full-text export or complete paginated retrieval is evidenced.

## Work executed in this pass
1. Re-examined the prior search scope, source register, patent memo and search log.
2. Executed 16 US-oriented web-index discovery queries. Exact strings and returned search responses are archived in us_patent_search_log_2026-11-15.json.
3. Ran allied discovery queries aimed at EP, CA, GB, FR and DE records. Search-engine site prefixes do not reliably enforce jurisdiction. These are discovery queries, not native-office corpus searches.
4. Examined selected publication pages and selected grant documents/family links; separated newly surfaced leads from proven additions to the complete prior machine register.
5. Preserved retrieved public patent PDFs without modifying their bytes, with a provenance/hash manifest, in the new dated Google Drive folder. Interrupted or invalid PDFs are not evidence and are not uploaded.
6. Left the accepted October 25 snapshot unchanged.

Evidence folder: https://drive.google.com/drive/folders/1Vfsm1-VdctsYAv44bBm6XNZ0fw3An7a1
Prior snapshot: ../2026-10-25/f5-global-autonomy-brakes/

## Candidate leads, not an exhaustive inventory
- Tufts US11861511B2: intelligent-system safe/norm-conforming/ethical behavior. https://patents.google.com/patent/US11861511B2/en
- Hybrid Vision US11733697B2: control-system lead. https://patents.google.com/patent/US11733697B2/en
- BAE US11473880B2: additional safeguards lead requiring claim/family review. https://patents.google.com/patent/US11473880B2/en
- Smart Shooter US12540785B2: additional safeguards lead requiring claim/family review. https://patents.google.com/patent/US12540785B2/en
- MBDA EP3608622B1: weapon system; priority 2018, application publication 2020 and grant 2023 illustrate why a five-year priority-only cutoff misses relevant granted claims. https://patents.google.com/patent/EP3608622B1/en
- FR3099823A1: operator/timestamp logging lead. https://patents.google.com/patent/FR3099823A1/en
- EP4370864A1: safing lead. https://patents.google.com/patent/EP4370864A1/en
- MBDA US12292263B2: training-only comparator, not evidence of an operational weapon safeguard. https://patents.google.com/patent/US12292263B2/en

Known cross-border overlap matters: CA3268069A1 and EP4599207A1 belong to the existing Kongsberg lead; GB2586854B belongs to an existing BAE family. A national publication is not a new invention. Existing Kongsberg anchor: https://patents.google.com/patent/US11946710B1/en

## Recommended reproducible coverage design, not yet executed
Core window: publications from 15 November 2021 through 15 November 2026, including applications, grants, relevant corrected documents and continuations. Separately retain older family members and earlier foundational patents reached by citations, shared priority, inventors or relevant classifications. Record priority, filing, publication and grant dates in separate fields.

Search US, EPO, UK, Canada, and PCT/WO routes; add relevant French/German native-language records and national registers where family coverage or legal status needs it. Record jurisdiction of filing separately from applicant nationality, owner and deployment country. Do not assume innovators always file in the US first.

Use several retrieval routes: function/claim vocabulary; CPC/IPC branches and neighboring classes; assignee/inventor aliases; citation/family expansion. Search safeguards by mechanism, not only by the word ethical: authorization, abort/veto/inhibit, target restrictions, protected/non-combatant objects, no-fire zones, confidence/uncertainty, communications-loss behavior, runtime assurance, auditability, rules-of-engagement and human control. Keep generic machinery safety, weapons training and operational weapons separate.

Retain query language, exact query, endpoint, execution timestamp, enforced date field/window, result totals, pagination/export counts, failed/truncated queries, document identifiers and hashes. Deduplicate publications to families without collapsing distinct continuations or claims. Independently inspect borderline exclusions. Check whether known positive patents are recovered; compare complementary search routes and inspect their unique additions. Stop only on documented coverage/saturation criteria, not an arbitrary result count.

## Explicit limitations and barriers
- Web discovery is not a bulk search. The whole US/allied corpus has not been retrieved in this pass.
- PatentsView's downloadable research-data boundary identified in this audit is 31 December 2025; it cannot by itself establish complete 2026 coverage.
- EPO OPS limits results accessible for a single query (2,000), requiring partitioning; it does not provide US claims full text. Credentials, rates and current service access must be verified before execution.
- EPO Register access returned 403 in this environment. No missing record or adverse status is inferred.
- Recent unpublished applications, secrecy restrictions, trade secrets, defensive publication and unpatented engineering remain outside public-patent completeness.
- Patent language is evidence of a claimed invention, not product adoption, effective safeguards or legal compliance.
- Candidate novelty against every prior machine-register entry remains unverified.

Official coverage references:
https://www.uspto.gov/patents/search/patent-public-search
https://patentsview.org/download/data-download-tables
https://www.epo.org/en/searching-for-patents/data/web-services/ops
https://www.epo.org/en/searching-for-patents/technical/publication-server

## Storage and preservation
Methods and small authored audit notes belong in GitHub; full patent texts, raw search responses and original PDFs belong in Drive. New Drive folder inherits the existing journalism-folder reader sharing; no permissions were changed. Only public source evidence is stored there. Hash manifest records exact retained bytes. A partial archive is not a comprehensive evidence corpus.

## Retrieval receipts and current access tests
Evidence manifest with SHA-256 and source URLs: https://drive.google.com/file/d/1tMNbePd61vw-uqKRpZi0tbAviu8KA-Mt/view
Four official USPTO PDFs archived: US11861511B2, US11733697B2, US11946710B1, US11473880B2. EP3608622B1 archived from the Google patent-image mirror of the EPO grant. The US12540785B2 download failed with HTTP/2 INTERNAL_ERROR and no incomplete PDF was uploaded.

Native-access tests recorded OPS 403 fair-use response, PatentsView 503 upstream error and timeouts for legacy/Google XHR/ODP routes. These are observations in this environment, not proof of a global outage, no matching patents or an exhausted corpus. Logs are archived unchanged. The fallback log's US11946710B2 URL is a wrong kind-code probe; the correct anchor is US11946710B1, whose official PDF was subsequently obtained. Test logs are evidence of access attempts, not coverage.

## Allied discovery query receipt
Exact query strings supplied by the allied-search researcher (all web-index discovery):
- site:patents.google.com/patent/EP autonomous weapon "safety"
- site:patents.google.com/patent/CA weapon "human" autonomous
- site:patents.google.com/patent/GB "weapon" "safety" "BAE" 2023
- site:patents.google.com/patent/CA "weapon" "safety-critical"
- site:patents.google.com/patent/EP "weapon" "ethical"
- site:patents.google.com/patent/FR arme autonome "sécurité" Thales
- site:patents.google.com/patent/DE Waffensystem Autonomie Sicherheit Rheinmetall
- site:patents.google.com/patent/GB "autonomous" "inhibit" weapon
- site:patents.google.com/patent/CA "autonomous" "engagement" weapon

Later access clarification: the public USPTO browser interface loaded successfully despite the API/command-line failures above. A structured-query feasibility test is being checked separately. Opening the interface is not evidence of a completed native corpus search.
