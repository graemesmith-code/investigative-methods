# Investment limits and evidence checks — 4 October 2026

This checkpoint screens **12 further predicates** and retains **one proposed new formulation and three refinements**. The new proposal tests actual disclosed fund positions against a binding concentration limit. A small official CVM dictionary confirms the relevant fields; no portfolio holdings or matched cases were acquired.

The useful insight is a one-sided test: when a limit uses an additive, nonnegative exposure measure, verified visible positions may already exceed the limit even if other positions are confidential. A visible total below the limit cannot establish compliance. The exact fund/class mandate, denominator, testing date, issuer group, netting rules and permitted exceptions must be resolved first. The repaired arithmetic helper requires a reviewed evidence manifest: one selected filing vintage, source-file SHA-256 and row locators, canonical holding identity across aliases, and aggregate/detail resolution. It rejects repeated source rows, repeated canonical holdings, mixed revisions and aggregate rows. Unique caller-made IDs alone are insufficient. The helper now requires conservative exposure lower bounds and a positive denominator upper bound, with an explicit uncertainty/rounding gate; a marginal excess of point estimates is inconclusive. The manifest itself requires source review; software cannot authenticate it or detect deliberately false canonical mappings.

The other cards improve methods already counted: an explicit connected-issuer flag against control evidence, a precise records-custody assertion against authenticated custody evidence, and claimed independent corroboration against the actual evidence chain. Counting these as three new mechanisms would inflate novelty. Eight further branches are rejected or deferred with reasons in `candidate-screen.csv`.

## Current totals and boundaries

There are **51 reviewed non-refinement formulations** after Q01 was reclassified as a refinement and Q02, Q03 and V01 were accepted by independent review, not 51 independently validated investigations. Earlier implementation enumeration remains **1,715 active provisional directional source-pair rows and 15 quarantines**. These counts use different units and must not be added together. The original 344-source manifest and SYS/AP provenance are retained. Every source has already received an individual source-level review in the earlier deep-review phase; that does not establish every possible predicate or pair as feasible.

The first 5,000-test target has not been justified. No total was padded through variants, source substitutions or parameter multiplication. No matched investigation, positive finding or end-to-end feasible route is claimed in this batch. All four cards require original records before execution.

## What was verified

The official CVM metadata ZIP is only **10,094 bytes**. Its raw bytes, SHA-256, 12 dictionary files, decoded text and parsed fields are saved under `evidence/`. Identifier fields vary by portfolio block: an ISIN is not universally present, fund/class identifiers differ from issuer identifiers, and reported net assets are not the same as gross portfolio assets. Browser access to the ZIP failed because of its content type; a bounded public download succeeded. The access log retains both outcomes.

Six documentation observations distinguish verified metadata from unresolved legal applicability and record access. CVM's current consolidated regulation is recorded as a lead; no universal cap or cure deadline is asserted. DOJ guidance supports the distinction between search methods and search results: a missed record alone does not establish an unlawful search. No agency contact, account creation, paid database use, bulk download or active technical probing occurred.

Validation passed **26 checks: nine artifact/provenance checks and seventeen synthetic arithmetic checks**. The latter cover positive and nonpositive lower bounds, equality at the cap, duplicate positions, wrong dates, negative denominators, unsupported negative exposure and an unknown measurement basis. They validate software behavior, not the legal applicability or feasibility of a real investigation.

## Ranking and reproduction

Consequence (1–5), testability (1–5), join-route confidence (1–3) and cost (1–4) remain separate. The editorial priority score is `10 × consequence + 3 × testability + 2 × join confidence − 2 × cost`; separate consequence and testability ranks are supplied. Scores are judgments, not probabilities of wrongdoing. A strong hypothetical identifier route is not an identity match.

Run `python code/design.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py` from this folder. Export/ranking/validation are deterministic; the existing model environment authored the source decisions and card text. Regeneration does not download data or call APIs. The original source texts, line ranges, SYS/AP IDs and hashes remain linked through `sources.jsonl` and each card's manifest.

The ZIP `checkpoints/consequential-expansions-through-04-corrected.zip` includes the corrected current outputs for expansions 01–04. Earlier ZIPs remain preserved in Git and are excluded from the new bundle to avoid recursive copies. Historical delivery receipts refer to those earlier separately committed artifacts.

## Remaining work

Independent review accepts Q02–Q03 and V01 as defensible new formulations, without asserting independent abstract mechanisms. The most valuable feasibility steps are one exact operative fund/class mandate with its dated measurement rule; a maintenance component certificate/life-history chain; and an actual case-number bridge for the request-response route. The current work remains source-level discovery, so these are dependencies, not instructions to bulk-execute tests. Original records, current case-specific legal applicability and coverage would need separate verification. No global exhaustion claim is made, and future screens should begin with a distinct consequential predicate rather than reword these cards.

Automatic weekly ChatGPT allowance and model-token telemetry are unavailable. The last user-reported figure was **88% remaining at 18:50 UTC**, compared with an earlier 99%; that 11 percentage-point change cannot be attributed solely to this task. Paid external API calls: **zero**.

## Detailed cards

### V01 — Verified fund holdings versus a binding concentration limit

proposed_new; priority 1; consequence 5/5, testability 2/5, join confidence 3/3, cost 2/4.

**If:** IF an operative fund/class mandate sets a precisely defined issuer or group concentration cap applicable at a stated test time, and dated disclosed positions can be attributed to that exact exposure group.

**Then:** THEN calculate the exposure using the mandate’s numerator/denominator and timing rules, reconcile corrections and permitted exceptions, and identify only unresolved excesses—not a breach from a raw portfolio percentage.

**Basis:** A material deviation from a binding investment limit can expose investors to risk they did not agree to bear. If the measure is strictly additive and nonnegative, verified disclosed exposure alone can provide a lower bound even with confidential positions. A low lower bound never proves compliance; no universal CVM cap or cure deadline is asserted.

**Join:** CVM CNPJ_FUNDO_CLASSE plus DT_COMPTC → exact fund/class registry and operative mandate → issuer ID in the appropriate CDA block (CNPJ_EMISSOR or typed CPF_CNPJ_EMISSOR) or verified security crosswalk → VL_MERC_POS_FINAL and correctly scoped VL_PATRIM_LIQ or other prescribed denominator. CD_ISIN occurs in some blocks only. OpenFIGI is optional instrument mapping, not proof of issuer group/control. Do not conflate fund, class and subclass.

**Scope:** Brazilian regulated fund/class and dated mandate; same competence date and valuation basis. An acquisition-time cap cannot be tested from end-month positions alone. Confirm passive market-movement exceptions, transition/cure windows, special fund classes and whether exposure is gross, net, look-through or issuer-group based.

**Ordinary explanations / disqualifiers:** Wrong fund/class or mandate version; Cap applies only at acquisition; Permitted passive exceedance or cure period; Netting/hedges or look-through change prescribed exposure; Wrong issuer grouping; Confidential aggregate double-counted with released detail; Liabilities make NAV differ from assets; Corrected filing or valuation basis; Identifier lost leading zeros or person mistaken for company

**Required evidence:** Operative fund/class mandate and relevant dated rules; Class/fund registration mapping; Dated holdings and filing revisions; one selected vintage, original-file hashes and row locators; reviewed canonical holding identity across row aliases; aggregate/detail reconciliation (helper accepts individual positions only); Verified issuer/security/group identity; Same-basis positive denominator and conservative upper bound; per-position exposure lower bounds or documented rounding/measurement tolerances; Applicable exceptions and transaction history when needed

**Next cheapest check:** Read the exact cap and its timing/measurement rule first. Then inspect a single dated disclosed position and class denominator. Stop if the mandate cannot be tied to that class or the exposure cannot be measured without unsupported netting assumptions.

**Novelty:** F03 compares aggregate exposure/liquidity categories; X14 compares supposedly identical statements. This tests binding portfolio constraints against positions. One-source CVM routes may suffice; optional OpenFIGI mapping is not counted as another independent test.

**Access evidence:** A 10,094-byte CVM metadata ZIP was downloaded and parsed; no holdings were downloaded. It confirms relevant field names and block differences. Mandate retrieval, actual class crosswalk, complete exposure and any exception remain unverified.

**Provenance:** SYS-0022 Brazil CVM open data (references/rabbit/originals/Rabbit2(1).txt:1578; AP-0023); SYS-0254 OpenFIGI API (references/rabbit/originals/Rabbit2(1).txt:16224; AP-0255, AP-0442)

**Documentation IDs:** D01, D02, D03, D04

### REF-SEARCH — A precise records-custody assertion against authenticated dated evidence

refinement; priority 2; consequence 5/5, testability 1/5, join confidence 2/3, cost 3/4.

**If:** IF an original agency response makes a specific factual assertion that an identified record was never created, received or held within a defined scope/date, and authenticated evidence appears to show the same agency component held that exact record during that scope.

**Then:** THEN compare the full request, clarification, search cutoff, response wording and actual custody evidence, considering referrals, corrections and search methods before describing a contradiction.

**Basis:** Contradictory custody claims can justify further reporting or a reviewable follow-up. A no-records search result is not a statement that a record never existed, and finding an overlooked record alone does not establish legal inadequacy, concealment or bad faith.

**Join:** MuckRock request ID → actual agency case number and full response → exact document/control number or authenticated content identity → agency component/custodian and proven control date. State Department reading-room case IDs are not automatically MuckRock request IDs. Court docket/exhibit may supply authenticated custody evidence, subject to availability.

**Scope:** Request scope and relevant control/search dates, not merely publication or archive capture date. An older public document does not establish continued custody; lawful transfer/destruction, later acquisition and different components require review.

**Ordinary explanations / disqualifiers:** Response merely says search found nothing; Different record/version or agency component; Outside agreed scope/date; Document acquired later or no longer held; Referral or link to public record instead of new production; Valid exclusion/Glomar handling; Corrected reply or adequate reasonable search despite missed record

**Required evidence:** Full request and all clarifications; Original complete response/search declaration; Exact record identity; Authenticated agency control at relevant time; Applicable procedural context and amendments

**Next cheapest check:** Read the exact response wording first. Reject a supposed contradiction if it only reports a search result. Then demand record identity and dated custody evidence before any legal inference; no new request is sent.

**Novelty:** Refinement of precise-assertion checking with D04/N05 records-access routes. Kept outside new-mechanism totals; not a redaction comparison or a blanket no-records failure detector.

**Access evidence:** DOJ guidance was inspected, including its distinction between reasonable search methods and results. No request-response/document pair acquired; no agency contact or paid court access.

**Provenance:** SYS-0136 MuckRock API (references/rabbit/originals/Rabbit2(1).txt:8765; AP-0137); SYS-0138 US State Department FOIA Virtual Reading Room (references/rabbit/originals/Rabbit2(1).txt:8849; AP-0139); SYS-0129 CourtListener and RECAP (references/rabbit/originals/Rabbit2(1).txt:8250; AP-0130, AP-1323, AP-1324, AP-1325, AP-1326, AP-1327, AP-1328, AP-1329, AP-1330, AP-1331, AP-1332, AP-1333, AP-1334, AP-1335, AP-1336, AP-1337, AP-1338, AP-1339, AP-1340, AP-1341, AP-1342)

**Documentation IDs:** D05, D06

### REF-REL — A fund’s explicit connected-issuer flag versus dated control evidence

refinement; priority 3; consequence 4/5, testability 2/5, join confidence 2/3, cost 3/4.

**If:** IF a disclosed position expressly marks the issuer as not connected to the manager/administrator, and independently verified dated control evidence appears to meet the applicable definition of connection.

**Then:** THEN reconcile the precise legal entities, role, control dates and reporting definition before identifying an unresolved flag inconsistency.

**Basis:** Potentially undisclosed related-party exposure matters, but a shared service provider, similar name or common address is not control. The field is a filing assertion, not an independently validated relationship.

**Join:** CDA fund/class CNPJ and issuer identifier → manager/administrator entity and CNPJ → official corporate control documents or GLEIF legal-registration/parent crosswalk. LEI, issuer CNPJ and manager CNPJ are distinct roles and namespaces; parent-reporting exceptions and gaps matter.

**Scope:** Position date, control effective interval and definition in force for that fund class. Do not apply a generic connectedness or beneficial-ownership percentage.

**Ordinary explanations / disqualifiers:** Shared service provider without legal connection; Different affiliate or date; Accounting parent differs from applicable control; Corrected flag; Different reporting definition; Incomplete GLEIF parent coverage

**Required evidence:** Original position flag; Manager/administrator identity; Applicable definition; Dated underlying control documents; Corrections and filing history

**Next cheapest check:** Confirm the exact meaning of EMISSOR_LIGADO and identify the manager before querying ownership. Do not infer a flag error from a common custodian.

**Novelty:** Refinement of X04 disclosure consistency and E08 related-party verification. Useful new implementation route, not a new mechanism count.

**Access evidence:** Metadata confirms the flag exists in multiple blocks. No actual flag, manager or control record matched; legal definition is unresolved.

**Provenance:** SYS-0022 Brazil CVM open data (references/rabbit/originals/Rabbit2(1).txt:1578; AP-0023); SYS-0001 GLEIF LEI data (references/rabbit/originals/Rabbit2(1).txt:5; AP-0001, AP-1133, AP-1134, AP-1135, AP-1136, AP-1137, AP-1138, AP-1139, AP-1140, AP-1141, AP-1142, AP-1143, AP-1144, AP-1145, AP-1146, AP-1147)

**Documentation IDs:** D01, D02

### REF-EVID — Claimed independent corroboration that reuses one underlying source

refinement; priority 4; consequence 4/5, testability 1/5, join confidence 1/3, cost 2/4.

**If:** IF a high-consequence published synthesis expressly treats multiple reports as independent corroboration, and full provenance suggests those reports derive from one underlying witness, document or press statement.

**Then:** THEN reconstruct the reporting chain and each report’s independent contribution, and reassess only the stated corroboration claim after collapsing demonstrably shared evidence.

**Basis:** Counting repetitions as independent evidence can overstate confidence. Syndication alone does not prove the underlying event false, and a reused article can contain new independent reporting.

**Join:** GDELT source URL and time → Media Cloud story URL/date → actual full article, citations and original source → archived version where available. URL equality, content digest or event-ID overlap is a clue, not proof of the same witness or independent reporting.

**Scope:** Version and publication chronology of the synthesis and source reports; source access and archival completeness must be established. Different datasets may intentionally report different units of one event.

**Ordinary explanations / disqualifiers:** Article adds original reporting; Same event confirmed by different witnesses; Synthesis never claims independence; Wire service reports independently verified later; Missing original obscures chain; Different event/claim units

**Required evidence:** Exact independence claim; Full articles and referenced originals; Documented reporting/provenance chain; Evidence of each independent contribution; Original versus updated versions

**Next cheapest check:** Trace two cited reports to their stated originals before counting sources. If the original source cannot be established, mark dependence unknown rather than assuming either independence or duplication.

**Novelty:** Refinement of X11 evidence independence; switching from overlapping trial participants to reused reporting is not counted as a new mechanism. No plagiarism or fabrication inference.

**Access evidence:** Catalog fields support URL/date leads only; no articles fetched or provenance chain demonstrated. Full-text access remains unverified.

**Provenance:** SYS-0095 GDELT (references/rabbit/originals/Rabbit2(1).txt:5992; AP-0096, AP-1373, AP-1374, AP-1375, AP-1376, AP-1377, AP-1378, AP-1379, AP-1380, AP-1381, AP-1382, AP-1383, AP-1384, AP-1385, AP-1386, AP-1387, AP-1388, AP-1389, AP-1390, AP-1391, AP-1392); SYS-0141 Media Cloud Search API (references/rabbit/originals/Rabbit2(1).txt:8975; AP-0142); SYS-0133 Internet Archive Wayback Machine APIs (references/rabbit/originals/Rabbit2(1).txt:8639; AP-0134)

**Documentation IDs:** No new full-text documentation acquired; catalog-only implementation lead.
