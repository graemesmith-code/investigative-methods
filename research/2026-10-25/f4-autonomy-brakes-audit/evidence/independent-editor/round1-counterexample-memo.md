# F4 brakes audit — independent skeptical-editor Round 1 source memo

Prepared 2026-10-25. Scope: free primary-web research; no Exa spending, outbound contacts, or repository writes. This memo is an initial counterexample pass, not the archive/FPDS census. Updated through approximately 14:48 UTC with independent live USAspending award and paginated transaction checks; see live-verification appendix. Dates and dollars below are identified by their actual evidence type. A document still online is not evidence that its program remains funded.

## Bottom line

Do not publish the universal claim that ASIMOV's end left no active funded public technical work on autonomous-weapons ethics/LOAC. A concrete near-cutoff counterexample is **TEELAWS**: official SBIR records identify **W51701-25-C-0052**, Perceptronics Solutions, **$1,899,998.92 live USAspending obligations**, signed **2024-10-23**, performance **2024-10-30 through 2026-10-29** (SBIR labels signing date as its start). An Army report of 2026-04-23 confirms actual West Point use/testing of software scoring tactical choices against LOAC. It is a training/decision-evaluation tool, expressly not an onboard engagement-deciding governor. Whether this satisfies a narrower definition of an ASIMOV replacement is a separate question, not a reason to omit it.

**CAMP**, a Navy/GA-ASI project announced April 2026, explicitly includes configurable ROE and AI decision thresholds for autonomous combat platforms. An official Navy September 22, 2026 report confirms a Gray Flag demonstration; its exact award/dollars and actual enforcement effectiveness remain unverified. **SEI's 2025 conduct-assurance reference architecture** includes an actual nonlethal TurtleBot4 demonstrator, but its parent CaTE pilot is explicitly reported completed in spring 2025. It is historical A/B work, not an active-cutoff program.

The categories should describe primary function, not create a false dichotomy. Engineering reliability, target-recognition performance, and bounded operating envelopes can be necessary components of legal/civilian-harm compliance without themselves encoding proportionality or distinguishing lawful targets. Conversely, an ethics label or a model-generated ethical score does not establish legally valid decisions or operational enforcement.

**Newly verified:** AFOSR awarded UT Austin $2,999,976 on August20 2026 for HAMLET ethical-reasoning design/TEV&V, performance September2026–August2031 (weapon-specific scope still to establish). DARPA CODORD has a JHU/APL order with actual additional obligations in November 2025 and April 2026, current performance through April2027; it explicitly pursues normative/deontic reasoning and evaluation. See CODORD addendum for evidence and the important non-weapons benchmark boundary.

## Strongest counterexamples and priority traces

### 1. TEELAWS — active-window normative technical training/evaluation

- Official SBA award: https://www.sbir.gov/awards/215327
- Recipient Perceptronics Solutions, Inc.; UEI MKQPJJKHDG89; Army SBIR Phase II, award year 2025; PI Spencer Kohn; contract **W51701-25-C-0052** (normalized **W5170125C0052**); **$1,899,999** is the SBIR rounded total-award field; live procurement obligations subsequently reconciled to **$1,899,998.92**, see appendix.
- Dates: SBIR labels **October 23, 2024–October 29, 2026**. Live USAspending resolves October 23 as signing/action date, with actual performance **October 30, 2024–October 29, 2026**. This overlaps the October 25 cutoff in the public record, subject to the DoD 90-day release lag.
- Abstract describes a sequential Phase II adapting CETLAWS Bayesian algorithms to military education, with collateral-risk/environmental feedback rather than autonomous engagement decisions; West Point is the initial training setting.
- Official implementation evidence: https://www.army.mil/article/291926/cadets_work_with_software_using_lethal_autonomous_weapons_systems_that_analyzes_tactical_decisions_provides_ethical_score — Eric Bartelt, April 23, 2026. Describes use/testing in PY201; scores represent confidence in LOAC compliance, and sensitivity analysis identifies factors affecting scores. Cadets design tactical decision games and ethical-reflection/coaching material.
- Classification: **A-enabling normative evaluation/training**, with D educational/governance overlap. Not demonstrated onboard A enforcement. Do not force into D merely to preserve a no-A claim.
- Resolution: live USAspending award/complete transaction history verified, see appendix. No public termination found in those records. Remaining uncertainty is recent reporting lag and actual work status, not basic award existence. Do not demand a new laboratory ablation to establish this project.

### 2. CETLAWS — predecessor outside the seven ASIMOV primes

- Author paper: Spencer Kohn, Marvin Cohen, Athena Johnson, Mikhail Terman, Gershon Weltman, Joseph Lyons, “Supporting Ethical Decision-Making for Lethal Autonomous Weapons,” Journal of Military Ethics (2024), DOI **10.1080/15027570.2024.2366094**.
- Publisher primary landing page: https://www.tandfonline.com/doi/full/10.1080/15027570.2024.2366094 ; accessible author-paper mirror: https://budef.mil.be/doc_num.php?explnum_id=272
- Funding declaration identifies AFWERX SBIR Phase II **FA864922P1015**. Authors describe Bayesian ethical-trust models with Laws of War/ROE and possible human interrogation/adjustment. This is direct funded normative-technical lineage; not proof of deployment or a funded 2026 governor.
- TEELAWS is a demonstrated non-ASIMOV continuation of this lineage. Searching only ASIMOV primes/subawardees would miss it.

### 3. Navy CAMP — advertised ROE/threshold configuration in 2026

- Primary company release, Navy public-release approval **SPR-2026-0217**: https://www.ga-asi.com/ga-asi-selected-by-us-navy-pma-281-for-collaborative-autonomy-mission-planning-and-debrief-project
- Dated **April 20, 2026**; GA-ASI selected by NAVAIR **PMA-281** for Collaborative Autonomy Mission Planning and Debrief (**CAMP**). Describes a government-sponsored demonstration intended for a 2026 Fleet exercise; integrations include Joint Digital Autonomy Range/JSE, MQ-20 Avenger with Government Reference Implementation autonomy.
- Explicit functionality includes ROE configuration, AI decision thresholds, behavioral tasking, mission debrief, human-centered oversight and target-engagement scenarios.
- Classification: **A/B candidate** plus C infrastructure. A primary contractor's announced capability is evidence of planned scope, not independent proof of enforcement effectiveness, delivered demo, award dollars, or ongoing funding.
- Official implementation follow-up: https://www.dvidshub.net/news/575299/navy-demonstrates-collaborative-autonomy-mission-planning-future-combat-aircraft — Navy story by Jamie Cosgrove, **September 22, 2026**, reports Gray Flag 2026 demonstration at Point Mugu using MQ-20, with end-to-end planning, execution and review. Human authorities and limitations are included in translated plans. Office is styled **PMX-281**, program manager Capt. Todd “Toby” Keith. This establishes a real demonstration, not an independently validated law-of-war guarantee.
- Resolution: find task/order/OTA and latest actions; determine whether constraints block execution or parameterize planning. No dollar attribution until matched.

### 4. CMU SEI conduct-assurance architecture — FFRDC visibility blind spot

- https://www.sei.cmu.edu/library/reference-architecture-for-assuring-ethical-conduct-in-laws/ ; DOI **10.1184/R1/28700720**; published **April 11, 2025**.
- Authors: Andrew O. Mellinger, Eric Heim, Andrew Schellenberg, Emily Newman, Tyler Brooks, Chuck/Charles Loughin (publisher varies presentation of name).
- Technical scope: rules specified and entered into ML-enabled lethal-autonomy systems; decomposition into component values; validation, dissemination, traceability, and testability throughout development. It is expressly about conduct assurance, not only crash avoidance.
- Classification: **historical A technical-design/assurance and B demonstrator**, D guidance overlap. Full report verifies a nonlethal implementation; neither operational weapons deployment nor active October 2026 CaTE funding is established. SEI is a defense-sponsored FFRDC, so task evidence matters more than the broad vehicle title.
- Full primary PDF: https://www.sei.cmu.edu/documents/6225/CaTE_LAWS_Reference_Architecture_9VryTJo.pdf . Printed p63 identifies DoD funding under **FA8702-15-D-0002**. Case study pp37–58 describes a TurtleBot4 implementation with 58 requirements, 28 formalizing ethical values, conduct-governor components and human-permission/de-escalation scenarios. Engagement was simulated through lights/speaker; not a lethal deployed system. Its rules presume a formalization of ethical values rather than solving every contextual legal judgment.
- **Currentness resolved negatively:** official SEI project page created October 2025 says CaTE concluded in 2025, with work completed that spring: https://www.sei.cmu.edu/projects/cate-increasing-warfighter-trust-autonomous-systems-accelerate-adoption-cutting-edge-capabilities/ . Collaborators included NREC and JHU/APL. Do not infer active CaTE from an active sponsor contract.
- Operator funding page https://sei.cmu.edu/work-with-us/ distinguishes old **FA8702-15-D-0002** expired ordering but performance 2015-07-27–2030-06-29; new **FA870225DB003** base/current 2025-07-01–2030-06-30 and optional ordering 2030–2035. These broad vehicles do not establish a continuing conduct-assurance task or allocable safeguard dollars.

### 5. RAIDER / N193-141 — ROE constraints inside an autonomy-enablement program

- Navy-origin SBIR topic mirrored at https://navysbir.com/n19_3/N193-141.htm and https://navysbir.us/n19_3/N193-141.htm ; “Resilient Autonomous Subsystems for Unmanned Air Systems,” opened 2019-09-24, closed 2019-10-23.
- Topic requires autonomous planning to respect operator-provided ROE, including geographic, temporal, behavioral constraints; discusses noncombatant maneuvers. RAIDER derives from DARPA CODE. The objective also enables denied-communications autonomous missions. Normative constraint and autonomy acceleration are not mutually exclusive.
- Important limitation: advanced/Phase II work **may become classified**; public solicitation cannot establish unclassified implementation at every maturity stage.
- Official SBA award: Weather Gage Technologies **N68335-21-C-0549**, **$1,499,179** total award amount, **2021-06-10–2024-11-18**, https://www.sbir.gov/awards/192723 . Expired on this record; not an active-cutoff counterexample without follow-on.
- Navy transition guide identifies Soar Technology **N68335-21-C-0510** (guide ending date 2022-11-30), DSOARS-R/SwarmMATE; https://navyfst.com/wp-content/uploads/2023/03/2023-ITS-Tech-Guide.pdf . These are traces to verify, not live dates.
- Selection record also names Barnstorm and Stottler Henke: https://navysbir.us/19_3-selections.html . Search all four performers and transition vehicles.

## Important scope/classification controls

### 6. ANSR

Primary: https://www.darpa.mil/research/programs/assured-neuro-symbolic-learning-and-reasoning . Solicitation **HR001122S0039**; currently listed manager Susmit Jha (web listing only, not separately interview-verified). Goal combines symbolic reasoning and learning for robustness, safety/risk evidence and predictability. **C by demonstrated public program summary**; ability to encode rules does not alone prove LOAC semantics. A particular performer/test may qualify A/B, so inspect abstracts rather than declaring the entire architecture legally irrelevant. Primary 2025 paper funding trace includes **FA8750-23-2-1015**: https://www.ri.cmu.edu/app/uploads/2025/06/Symant.pdf . Funding acknowledgment does not establish current obligation balance.

### 7. TIAMAT

Primary FY2025 DARPA budget text explicitly includes ROE among “semantic anchors” for transferring autonomy from simulation to real environments: https://www.darpa.mil/sites/default/files/attachment/2024-11/u-rdte-mjb-darpa-pb-2025-06-mar-2024-final.pdf (PE 0602303E, IT-04; printed Volume 1 p.74). It lists FY2024 **$10m** and FY2025 **$17m** plans; **budget plans, not obligations or normative spending totals**. Classification **C primary/A-relevant candidate**, not a proven LOAC test suite. Inspect actual solicitations/performer outputs and which rules are evaluated. Commercial lead **HR00112490431** needs primary verification; do not present as verified award facts from this memo.

### 8. JATIC / SHIELD

Government testimony explicitly describes JATIC robustness, adversarial resilience, comprehensibility/trust, competence: https://docs.house.gov/meetings/AS/AS35/20230309/115478/HHRG-118-AS35-Wstate-MartellC-20230309.pdf . Government demo (taken 2024-04-15, posted 2025-02-28) uses VisDrone object detection/classification: https://www.dvidshub.net/video/953966/jatic-capability-demonstration-april-2024 . **C, with possible B human-factors contribution**; object-detection benchmarks alone are not civilian/combatant legal distinction.

CDAO's RAI tool list describes ~100 illustrative open-source tools and cautions that inclusion is not endorsement/approval: https://www.ai.mil/Portals/137/Documents/Resources%20Page/2024-12GenAI-Responsible-AI-Toolkit.pdf . The assessment is named **SHIELD**, not a system that autonomously blocks weapons. **D assessment/process plus linked C tooling**, with possible specific A content to inspect. Do not conflate it with Shield AI or MDA's SHIELD contract vehicle.

### 9. AFRL RTA / STARS

https://www.afresearchlab.com/stars-2/ describes reinforcement-learning satellite control, close-proximity RTA, human delegation interfaces and testing. **C with human-interface B-relevant component**, no demonstrated weapons-LOAC criterion. AFRL July 28, 2026 primary report describes neural-network satellite-bus control in orbit and watchdog/RTA testing: https://afresearchlab.com/afrl-demonstrates-neural-network-control-of-satellite-bus-in-orbit-2/ . This is useful contemporaneous implementation evidence, not normative restraint or dollar evidence. New 2026 topic lead **DAF26BZ01-NV008**, Runtime Assured Autonomy, should be checked at official DSIP/SBIR; a solicitation is not an award.

### 10. TETRAS A2WSD and Quasistatics — easy overclaims to reject

The title of **FA248722FA002** in procurement mirrors is **Autonomous and Automated Weapon System Design (A2WSD)** under TETRAS, not a narrowly specified ethics audit. Commercial mirrors disagree on values and show broad subcontract supplies/services. This editor reconciled live primary obligations to $48,989,772.86 (38 transactions), see appendix; coordinator must read actual tasks; count only demonstrably allocable safeguards dollars, not entire vehicle ceilings. Do not copy the user's $39m as established.

**FA864926P0093**, Quasistatics, was independently verified in live USAspending as touch-secure near-field key loading for attritable UAS/smart munitions, $74,771 obligated, June 24–September 28, 2026, one transaction. See appendix. A cryptographic key loader can secure provisioning without guaranteeing positive human authorization of a specific target. Treat **C/B-candidate**, not confirmed B, and do not call active at cutoff absent extension.

## Round 1 editor challenges and resolution criteria

1. **Existence versus maturity:** Does the inventory include TEELAWS, CAMP, SEI and RAIDER? Resolve by source/award IDs and scope fields; separately label framework, prototype, training use, demonstrated enforcement, and operational deployment. An absence claim must specify which maturity is absent.
2. **Active and funded:** For each candidate, obtain latest actions, current/potential end, obligations and termination evidence as of cutoff. Performance overlap is positive evidence, not proof all money remains available. Expired original award is not proof no successor.
3. **Count units:** Count programs, awards, tasks, papers and tools separately. Use normalized PIID + parent/agency for awards; never sum parent IDV ceilings with child orders or subawards with their primes.
4. **Technical content:** Identify the actual constrained variable/test oracle, who supplies the rule, and whether output is advisory or blocks action. A ROE label may encode only a geographic box; a safety envelope may nonetheless implement a lawful commander's restriction.
5. **Symmetric taxonomy:** Do not lower the bar for ASIMOV (a benchmark program, not an onboard governor) while requiring replacements to be operational governors. Do not raise the bar for counterexamples after finding them. Training scoring can be A-enabling without being an equivalent replacement.
6. **C is not legally irrelevant:** Check target-error, uncertainty, abort and operating-envelope pathways to preventing unintended engagements. No dedicated normative test is not the same as no contribution to LOAC compliance. Also do not claim reliability proves lawful targeting.
7. **SHIELD/JATIC/TETRAS:** Inspect tasks, not acronyms. Separate voluntary workflow advice, actual software, legally focused scenarios, and generic engineering test infrastructure. Find allocable dollars or explicitly say unavailable.
8. **FFRDC/OTA blind spots:** Search broad sponsor task descriptions, performer papers and transition news. No ethics keyword in award title is not a dispositive negative. Preserve public/classified uncertainty.
9. **Performer lineage:** Search beyond ASIMOV primes; TEELAWS proves a separate federal normative lineage. For ASIMOV authors publishing in 2026, read funding acknowledgments and contract dates before calling papers new money.
10. **Program of record:** Define the acquisition meaning before using this phrase. An R&D benchmark like ASIMOV may not itself be a program of record. Avoid changing denominator from R&D to acquisition to manufacture disappearance.
11. **Time and funding precision:** Publication date, crawl date, fiscal-year label, award action date and period of performance are distinct. Requested budget amounts are not obligations; “current award value” is not paid spending.
12. **Publication threshold:** A defensible narrow finding may be that no equivalent active public operational normative-benchmark program was verified in searched sources, with listed unresolved candidates. It cannot establish universal absence, classified absence, effectiveness of surviving brakes, or causal harm from a canceled option without additional evidence.

## Boundaries / unresolved work

Live USAspending award and complete paginated transaction checks were independently performed by this editor and reconciled, as below. No FPDS reconciliation completed: first exact-PIID Atom attempt returned HTTP400. Coordinator is pursuing FPDS. Direct publisher PDF retrieval for CETLAWS returned 403; same paper obtained from Belgian defense library mirror, so not a substantive content blocker. Initial SEI download click failed but succeeded using its returned page reference; full report funding statement and implementation were subsequently read. National-lab/other-agency initial search surfaced generic Sandia autonomy and IC/NIST frameworks but **did not establish a funded normative weapons-benchmark successor**; this is a limited search negative, not an exclusion of those agencies. More focused follow-up remains useful after coordinator inventory.

No external contacts, uploads, financial spending, or repository mutations occurred. Local authored memo only. Await coordinator inventory for explicit Round 2, then reconciled near-final findings for Round 3. Discovery/currentness checks continue independently while waiting.


## Update: maritime distinction and live primary-award reconciliation (approximately 14:36 UTC)

### N232-092 — classification relevant to distinction, not complete legal target judgment

Official RDRTec Phase II record https://www.sbir.gov/awards/218158 identifies **N68335-25-C-0110** and a robust maritime classifier separating combatant from commercial vessels. It seeks an automated pipeline for airborne imagery. Official Areté sibling https://www.sbir.gov/awards/218265 identifies **N00024-25-C-S104**, NSAM Multi-Sensor Fusion, with the same explicit combatant/noncombatant objective. These belong at least in **A-enabling/C overlap**, not an unexplained C-only exclusion. Vessel type is not full contextual lawful-target status; neither source establishes a proportionality judgment or onboard attack veto.

Navy-origin topic mirror https://navysbir.com/n23_2/N232-092.htm states insufficient imagery may return no classification and a human will generally adjudicate. It also warns Phase II may become classified. Thus public funding/objective is established, but the implementation's unclassified status, operational effect and normative sufficiency need distinct labels. The mirror itself says unofficial copy; the official SBIR award abstracts independently corroborate the objective.

Areté's SBIR record is stale: live primary procurement data show more funding and extension through 2028. This illustrates why using a past end date to assert disappearance is unsafe.

### Live USAspending award and complete transaction summaries

All below were retrieved directly from https://api.usaspending.gov/api/v2/awards/{generated_unique_award_id}/ and POST https://api.usaspending.gov/api/v2/transactions/ with award_id, page, limit=100, sort=action_date, order=desc. Each transaction list was traversed until hasNext=false. For every matched row the federal-action-obligation sum equals the award's total_obligation. These are **USAspending reconciliations, not FPDS cross-verification**. Full request/response hashes and JSON are in local live/ and live-extra/; generated keys/URLs also in editor-verified-candidates.csv/json.

| Award | Obligations | Current end | Latest action | Transactions | Meaning |
|---|---:|---|---|---:|---|
| FA864922P1015 | $750,000.00 | 2023-12-11 | 2023-09-05 | 2 | A;B-candidate |
| FA864926P0093 | $74,771.00 | 2026-09-28 | 2026-06-24 | 1 | C;B-candidate |
| N6833521C0549 | $1,499,179.00 | 2024-11-18 | 2023-11-15 | 4 | A/B-candidate;C |
| N6833521C0510 | $999,459.00 | 2023-08-19 | 2023-05-10 | 6 | A/B-candidate;C |
| FA248722FA002 | $48,989,772.86 | 2028-03-14 | 2026-06-26 | 38 | C;unallocated broad vehicle |
| FA864926P0169 | $74,973.00 | 2026-09-30 | 2026-06-24 | 1 | C |
| FA945326CX013 | $708,340.99 | 2031-07-16 | 2026-06-16 | 3 | C;A-relevant candidate |
| W5170124C0174 | $1,899,970.59 | 2026-01-07 | 2025-06-24 | 4 | C |
| W5170125C0052 | $1,899,998.92 | 2026-10-29 | 2025-04-28 | 2 | A-enabling;D |
| N6833525C0110 | $998,716.00 | 2027-02-11 | 2025-02-11 | 1 | A-enabling;C |
| N0002425CS104 | $1,393,577.00 | 2028-08-18 | 2026-07-14 | 3 | A-enabling;C |
| FA864925P0010 | $1,249,987.00 | 2026-09-16 | 2025-11-20 | 3 | C;A-benefit claim |

- **TEELAWS:** signed/action 2024-10-23, performance starts **2024-10-30**. Original obligation $1,899,998.92; 2025-04-28 administrative modification P00001 $0. No 2026 new money is demonstrated; preexisting obligated support overlaps 2026. SBIR's October 23 start is not the procurement performance-start field.
- **RDRTec:** potential end 2028-02-11 versus current 2027-02-11; all-options $1,297,050 versus $998,716 obligated.
- **Areté:** three actions, latest 2026-07-14; obligations $1,393,577 versus stale SBIR $696,782. Current/all-options contract values $1,393,577/$1,990,819.
- **TETRAS:** obligations $48,989,772.86, not the user-premise $39m; base/exercised value $117,485,156 and all-options $241,826,327.70. No entire-value attribution to ethics.
- **Spectral:** only $708,340.99 obligated; $11,919,827 base/all-options value is not spending.
- **Quasistatics/ResilienX/Linchpin:** these specific records end before cutoff. This is not proof of program termination or no subsequent awards.
- **Soar legacy:** N6833521C0510 current recipient is ACCELINT AI, LLC, showing why recipient-name-only lineage screening fails.
- **No exact contract result:** HR00112490431 (OTA) and FA87502321015 (grant) were not found by the contract-only search, which is not a program-absence result. Coordinator must use applicable non-FAR/assistance routes.

**Publication limitation:** official FPDS https://www.fpds.gov/common/html/public_welcome_text.html states DoD detailed contract data have a 90-day release wait; https://sam.gov/contract-data likewise refers to restricted 90-day data. As of October 25, approximately the newest quarter can be absent. Do not represent complete pagination as complete knowledge of all recent real-world actions. “Record-active” and “record performance ended” are deliberate qualifications.

**Additional source leads, not counted as active normative programs:** IARPA BENGAL primary page https://www.iarpa.gov/index.php/research-programs/BENGAL describes an 18-month 2026 effort with Los Alamos T&E partnership addressing hallucinations, information leakage, poisoned inputs; C not a demonstrated weapons-law benchmark. NASA/AFRL VIRAP nonreimbursable agreement https://www.nasa.gov/saa/domestic/42435_IA1_42435_AFRL_VIRAP_Fully_Executed.pdf addresses flight-path RTA/V&V, C, each party funding its participation subject to funds, no transferable dollar total. Sandia “Autonomous Systems, Artificial Intelligence and Safeguards” (2018) is nuclear-safeguards context, not an autonomous-weapons legal brake; keyword false-positive guard.


## New Round 1 counterexample: CODORD — verified 2026 funding, normative authoring/testing

**Classification: A-enabling technical normative authoring/evaluation, not a verified weapons LOAC governor or ASIMOV-equivalent weapons benchmark.** DARPA's official CODORD page explicitly names compliance with laws/ethics, dynamic ROE, command intent, and allied authority differences as applications. It identifies USC, RTX BBN and SRI as performers and lists 2026 outputs. https://www.darpa.mil/research/programs/codord . This cannot be omitted from a broad inventory of public funded normative technical safeguards simply because published demonstrations are general legal reasoning rather than target engagement.

**Direct funding/currentness:** Live USAspending award **HR001125F0028**, JHU/APL, parent **HR001122D0001**; signed **2025-03-03**, performance **2025-03-04–2027-04-16**; **$2,481,841 obligations**, **$3,259,077 base/exercised value**, **$3,321,820 all-options value**. All four transaction pages/records were retrieved; sum matches award obligations. Base March3 2025 +$331,818; P00001 April14 2025 +$1,029,336; P00002 November3 2025 +$250,000; P00003 April20 2026 +$870,687. Latest action is a supplemental agreement for work within scope. Thus this is actual 2026 money, not merely a 2026 paper or an old appropriation with long nominal performance. Source: https://api.usaspending.gov/api/v2/awards/CONT_AWD_HR001125F0028_9700_HR001122D0001_9700/ . The two later modifications use generic UARC-services language; no task SOW acquired. Do not assert JHU/APL is the independent T&E lead or allocate every dollar to weapons LOAC from this record alone. JHU/APL UARC is not the same entity/role as JHU university researchers subcontracting to BBN.

**Concrete testing design:** Official information slides (pp14–16) require delivered software/models and common programmatic tests, independent T&E, correctness of answers versus manually authored logic, and authoring labor-effort measurements, across at least three use cases. Phases are 12+12 months. These are specified deliverables/metrics, not achieved-results evidence. https://www.darpa.mil/sites/default/files/attachment/2024-11/codord-info-session-distro-a.pdf . Official FAQ says the T&E team chooses common domains and runs semantic correctness assessments; performer prototype OTs have up to $2m combined base+option, including any cost sharing—not a program obligation total. https://www.darpa.mil/sites/default/files/attachment/2024-11/codord-faqs.pdf . The separate JHU/APL support order exceeding $2m must not be misread as contradicting a performer-proposal cap.

**Performer evidence and boundaries:** RTX's August28 2025 award announcement describes DONATELLO, human-in-the-loop translation of regulations into executable logic; team includes JHU and Stony Brook. It names no award dollars. https://www.rtx.com/news/news-center/2025/08/28/rtx-bbn-technologies-to-empower-ai-to-understand-and-apply-regulatory-legalese . DARPA-linked DeonticBench (April6 2026) actually tests tax, airline baggage, housing and immigration rules, not weapons LOAC. https://arxiv.org/html/2604.04443v1 . USC CODORD **HR00112590089** is linked by author funding acknowledgment https://aclanthology.org/2025.acl-long.1012.pdf and PI CV https://www.jaypujara.org/pdf/pujara_cv.pdf . Exact live OTA dollar/date records remain unresolved; contract-only and IDV USAspending searches returned no exact result. Commercial mirrors have inconsistent/malformed durations and are not used as verified values. Exact-PIID FPDS Atom attempt returned HTTP400; no successful FPDS check claimed.

**Editor challenge:** What is the report's defensible denominator—operational weapons governors, weapons-specific ethical benchmarks, military normative-authoring R&D, or all technical safeguards? CODORD decisively challenges universal absence of the last two categories, while not establishing the first two. Resolve by explicit category/maturity fields and a documentary chain from current award to tested program domains; do not demand undisclosed lab experiments or shift the definition after finding it.

### Additional pending A leads, not funded-active conclusions

- FY2026 MURI Topic2 (AFOSR), **Ethical Constructs and Adaptive Learning Systems**, solicits adaptable ethical codes/metrics/normative procedures for DoD autonomous systems. Proposed start May1 2026; anticipated <=$1.5m annually over five years is a ceiling/plan, not award. Initial exact-title grant API search was empty. **Superseded by broad grant search: HAMLET FA9550261B207 now verified, see later addendum.** Official amended notice pp56–57: https://www.onr.navy.mil/media/document/funding-announcement-n0001425sf002-amendment-0001 . Search absence does not prove no grant.
- **ARMOR 2025** paper published April30 2026, Virginia Tech: 519 doctrinal questions across Law of War, ROE and Joint Ethics Regulation; tests LLM military decision-support knowledge, not weapon execution. https://arxiv.org/html/2605.00245v1 . No federal funding acknowledgment established from HTML, so do not count as federally funded or ongoing program. The name's 2025 label is not its publication date. Dataset construction arithmetic in text needs review before relying on its exact process claims (545 minus21 is not519); existence/scope remain clear, validity not independently certified.


## B boundary check: funded weapon systems can contain real human-control brakes

Do not require a separately named safeguard research program before acknowledging a technical human-veto component. Conversely, do not count a munition's entire procurement value as safeguard expenditure.

**Switchblade** is a concrete B-bearing system. Official Fort Hood public-affairs story dated September25 2025 (posted September26; live-fire September15) describes operator target selection and the ability to wave off a strike mid-flight. https://www.dvidshub.net/news/549283/1st-cavalry-division-conducts-first-switchblade-600-live-fire-fort-hood . The 2025 Switchblade600 Block2 datasheet retains wave-off/recommit capability: https://www.avinc.com/images/uploads/product_docs/2025_Switchblade-600b2_Datasheet_250923_v13.pdf . Army acquisition reporting explicitly connects abort to reducing collateral damage/civilian casualties: https://asc.army.mil/armyalt/Summer2023/html/29.html . These establish an intended human-control mechanism, not independently measured reliability, guaranteed control under communication denial, or a veto on an unlawful human authorization. They also do not establish which configurable mode/version is used in every deployment.

Live primary USAspending verified three child orders under **W91CRB24D0011**; all current record periods overlap cutoff. These are **system acquisition dollars with B features, not allocable B-safeguard R&D**:

| Order | Signed | Performance | Obligations | Latest action | Complete transaction count |
|---|---|---|---:|---|---:|
| W91CRB25F0094 | 2025-01-17 | 2025-01-18–2027-04-30 | $218,024,507.64 | 2026-06-25 | 15 |
| W91CRB26FA055 | 2025-12-29 | 2026-01-02–2027-06-01 | $254,732,512.77 | 2026-07-17 | 3 |
| W91CRB26FA177 | 2026-04-29 | 2026-05-01–2027-02-28 | $28,082,019.40 | 2026-04-29 | 1 |

API URLs: https://api.usaspending.gov/api/v2/awards/CONT_AWD_W91CRB25F0094_9700_W91CRB24D0011_9700/ ; https://api.usaspending.gov/api/v2/awards/CONT_AWD_W91CRB26FA055_9700_W91CRB24D0011_9700/ ; https://api.usaspending.gov/api/v2/awards/CONT_AWD_W91CRB26FA177_9700_W91CRB24D0011_9700/ . First award description explicitly names Switchblade300/600; others name LASSO. Specific product configuration/interlocks not itemized publicly in these descriptions. Base/exercised for W91CRB25F0094 is $220,119,135.12, not its obligation amount. No omnibus 'safety spending' sum is justified.

Parent official award August27 2024 was **$990m ceiling**, not obligated total; funding determined per order and then-estimated end August26 2029: https://www.defense.gov/News/Contracts/Contract/Article/3886803/ . Vendor February26 2026 press release announces **$186m** order for next-generation Switchblade, but it has **not been matched** to an exact order by this editor and must not be silently equated to the $254.7m order: https://www.avinc.com/2026/02/26/av-receives-186-million-u-s-army-delivery-order-for-next-generation-switchblade-systems/ . Do not add announced value, parent ceiling and child obligations.

**Hunter WOLF/CROWS**: official Army August21 2026 report describes an HDT Robotics/BLADE CRADA and April2026 demonstration with the 101st Airborne. It discusses adding autonomous features while retaining positive human control of lethal decisions. https://www.army.mil/article/294796/armaments_center_partners_with_industry_to_explore_concepts_for_integrating_lethal_payloads_to_unmanned_ground_vehicles . B-relevant human-interface development; no award ID/allocable federal dollars verified, no proof of a legally valid decision guarantee.

**DIU SWAP-USV Sprint2** public solicitation **PROJ00721**, responses due November30 2026, specifies human-in-the-loop safety interlocks, remote arming/dearming and abort. https://www.diu.mil/work-with-us/submit-solution/PROJ00721 . At most a B requirement candidate, **not an awarded or delivered system**. Page publication date not established from the primary page; tertiary October19 reference suggests pre-cutoff presence, but do not elevate to independently verified dated publication. Use to challenge a blanket claim that acceleration solicitations abandon human-control requirements, not to tally current funding.


## New late-2026 funded ethical-TEV&V grant: HAMLET (replaces the unresolved MURI lead)

**HAMLET — Humans and Autonomous Machines Learning to Effectively Team: Design and TEV&V for Adaptive Ethical Reasoning**, **University of Texas at Austin**, grant **FA9550261B207**, is a concrete recent funded normative-technical project. Live USAspending full record and complete transaction retrieval show a single **new-award action August20 2026, $2,999,976 obligated**, performance **September1 2026–August31 2031**. AFOSR is awarding/funding office; recipient UEI **V6AFQPN18437**. Assistance Listing12.800. https://api.usaspending.gov/api/v2/awards/ASST_NON_FA9550261B207_097/ . The grant explicitly identifies opportunity **NOFOAFRLAFOSR20250002**, the FY2026 MURI notice previously identified. It does not identify a topic number, but its title strongly corresponds to Topic2; label that correspondence an inference unless independently documented.

The official Topic2 text seeks integration and evaluation of adaptive ethical codes in compact autonomous systems potentially used by DoD, beyond generic bias/fairness/transparency. https://www.onr.navy.mil/media/document/funding-announcement-n0001425sf002-amendment-0001 (pp56–57). **Classify HAMLET as A-enabling ethical-autonomy design/TEV&V; explicit weapon-specific LOAC scenarios, PI/team, deliverables and measured results remain unverified.** Funding and current record period are strong, while effectiveness/military-weapon application are separate. It is not an acquired operational program of record by virtue of a MURI grant. Do not count the solicited potential $7.5m five-year budget as actual funded amount, or extrapolate $2,999,976 to every year. No reported subawards does not establish there are no collaborators.

**Investigative lesson:** an exact search for the solicitation topic title returned nothing. A broad **ethical** search in DoD **grants**, not contracts, found the renamed award. The action is less than90 days old and already public: the documented DoD90-day **contract** reporting restriction must not be applied automatically to assistance records. Grant/action completeness remains bounded by public reporting, but this is direct evidence of new funding in August2026, before the asserted September/October policy deadlines, not just a stale webpage.

### Further verified assistance leads and negative controls

These records are identified to prevent a contracts-only or weapons-keyword-only blind spot, not to inflate the count of proven weapon safeguards. Exact technical inspection is still needed before inclusion in strict A/B totals:

| Grant / recipient | Obligations | Performance | Latest action | Technical boundary |
|---|---:|---|---|---|
| **FA86552417047**, Manchester, **CASPER++** | $618,340 | 2024-09-15–2029-09-14 | 2026-09-10 | Cognitive architecture for ethical/transparent social robot collaboration; weapon-specific scope not verified |
| **W911NF2510079**, Syracuse | $457,080 | 2025-04-01–2029-03-31 | 2026-01-28 | Human judgments of AI moral violations; potentially social-science/enabling, not established technical weapon restraint |
| **FA95502310036**, George Mason | $399,412 | 2022-11-25–2025-11-24 | 2024-02-12 | Qualification system for robot moral agency; historical period, no follow-on established |
| **FA95502010342**, Clemson | $870,257 | 2020-09-18–2025-09-17 | 2024-07-29 | Ethical/unethical behavior and trust in human-autonomy teaming; historical period, not an operational governor |

For each, the primary full-award endpoint is `https://api.usaspending.gov/api/v2/awards/ASST_NON_{grant-number}_097/`. Each transaction set fully paginated; respectively3,4,2,7 records. CASPER++ has **new September10 2026 continuation $195,580**, following July1 2025 +$195,580 and September10 2024 +$227,180. Keep unrelated medical ethics, organizational leadership and human-morality grants as explicit false positives, not hidden candidate count inflation.

**Editor resolution request:** Inventory HAMLET, disclose why it qualifies as broad normative-autonomy research but is not yet verified a weapons-specific ASIMOV replacement. Obtain grant abstract/award synopsis or primary institutional research description without contacting anyone. If unavailable, preserve that exact scope gap; do not turn it into 'no ethical technical funding exists.'


## Reporter-supplied Georgia Tech lead — independent verification

**W911NF261A113**, Georgia Tech Research Corp, title *A Computational Framework for Explainable, Normative, and Justified Agency*. Primary live record: https://api.usaspending.gov/api/v2/awards/ASST_NON_W911NF261A113_097/ . **$129,902 obligations**, one new-award action **March27 2026**, performance **April1 2026–March31 2029**. Exact project-specific technical paper/PI or weapon connection not located. Classify normative-agency adjacent/A-enabling candidate, not verified weapon LOAC safeguard. Pat Langley's similarly titled2019 AAAI paper https://ojs.aaai.org/index.php/AAAI/article/view/5049 is conceptual background only; no evidence it establishes this grant's team, direct lineage or funding. Do not attribute to Ronald Arkin merely because Georgia Tech received it.

## CAMP funding gap closed — January 2026 order, with modification-text caveat

Primary live USAspending order **W31P4Q26F0015**, parent IDIQ **W31P4Q22D0025**, recipient **General Atomics Aeronautical Systems, Inc.**: **$1,988,634 obligations**, same base/exercised/all-options amount, signed **January28 2026**, performance **January29 2026–January29 2027**. https://api.usaspending.gov/api/v2/awards/CONT_AWD_W31P4Q26F0015_9700_W31P4Q22D0025_9700/ . Army **W6QK ACC-RSA** is awarding office; **Navy NAVAIR** funding office. It is a cost-plus-fixed-fee delivery order under an Army IDIQ, not the unrelated NAVAIR MQ-9 BOA asserted by a commercial AI-generated summary. No generic IDIQ ceiling should be attributed to CAMP.

Complete two-transaction history: original January28 **+$1,988,634**, description explicitly *TASK ORDER TO SUPPORT JSIL NAVY COLLABORATIVE AUTONOMY MISSION PLANNING AND DEBRIEF*. April28 **P00001 $0**, within-scope supplemental agreement, instead described *JSIL UNITED STATES MARINE CORPS (USMC) SERVICE LEVEL TRAINING EXERCISES (SLTE) PHASE 5A*. This discrepancy could be reused administrative text or a scope adjustment; the actual modification/SOW is unavailable, so preserve the ambiguity rather than asserting every current dollar solely funds CAMP or that April28 added funds. Full-award description continues to identify CAMP. Commercial GovTribe parent table gives **$3,977,268 (twice primary obligations)**; primary award total and transaction sum agree on **$1,988,634**. Use primary amount, not the doubled secondary figure.

Combined with GA-ASI's April20 2026 release specifying ROE configuration and AI thresholds (NAVAIR-approved), and the official Navy September22 2026 account of actual Gray Flag demonstration, this closes the prior **no matched award** gap: CAMP is funded, record-active, weapons-linked mission-planning technical work with A/B-relevant constraints. https://www.ga-asi.com/ga-asi-selected-by-us-navy-pma-281-for-collaborative-autonomy-mission-planning-and-debrief-project ; https://www.dvidshub.net/news/575299/navy-demonstrates-collaborative-autonomy-mission-planning-future-combat-aircraft . The Navy describes translating human-planned roles, timing, authorities and limitations into execution on an MQ-20 surrogate. It does **not** establish independent legal reasoning, adversarial constraint tests, guaranteed enforcement, every platform/mode, or an allocable normative-feature budget. Exclude its entire order from an additive **normative-safeguard spending** total, but do not omit it from the substantive inventory merely because allocation is unknown.

Raw complete live records, request log and script: `/tmp/f4-editor/live-camp/`, `/tmp/f4-editor/verify_camp.py`.

## CASPER++ technical-scope check — genuine active grant, not demonstrated LOAC benchmark

Manchester's primary recruitment document identifies **Angelo Cangelosi**, reference **SAE-026934**, 48-month research associate position, and project goals of computational architecture for shared-goal/intention inference, trust and task arbitration in heterogeneous human–robot teams: https://www.jobs.manchester.ac.uk/Job/GetJobAdvertDocument?Id=96973&JobId=30455 . The lab's current-project page likewise describes CASPER++ as trust/theory-of-mind work: https://corolab.uk/about-us/ . These sources substantiate technical activity rather than merely an ethical title; neither establishes a weapon-specific normative test.

A concrete 2025 output by **Tien Pham and Angelo Cangelosi**, *Pay Attention to What and Where? Interpretable Feature Extractor in Vision-based Deep Reinforcement Learning*, acknowledges the **exact current grant FA8655-24-1-7047** on its first page and evaluates visual interpretability on **57 Atari games**: https://www.inf.uni-hamburg.de/research/projects/trail/publications/pdfs/2025-04-pham-ijcnn.pdf . This is **C/enabling interpretability output**, not demonstrated LOAC-rule enforcement. Do not conflate it with the earlier CASPER paper, first published **March14 2024** despite its October2025 journal issue, which acknowledges **FA9550-19-1-7002** and tests a simulated kitchen: https://link.springer.com/article/10.1007/s12369-024-01116-2 . Nor should the interpretable-output example establish that all current CASPER++ work lacks normative reasoning; its broader deliverables remain incompletely public. Preserve active-funding evidence while qualifying scope.


## CaTE linkage correction: common broader pilot, distinct funding and technical task

**Edge Case Research FA864924P0520**, *Mission Assurance for Autonomy and Reinforcement Learning with Carnegie Mellon University*, is **STTR PhaseII**, not the funding record for SEI's complete ethical architecture. Primary abstract https://www.sbir.gov/awards/210029 names CMU as research institution, Michael Wagner as PI, and RL assurance/hazard assessment/metrics as work. It explicitly links to an assurance framework produced for CaTE, so do **not** call this an established unrelated acronym collision: SEI's own guidebook expands CaTE as Center for Calibrated Trust Measurement and Evaluation. The specific award is **C assurance**, with no verified normative-law test; common ecosystem does not prove common deliverable funding.

Primary full-award endpoint https://api.usaspending.gov/api/v2/awards/CONT_AWD_FA864924P0520_9700_-NONE-_-NONE-/ : obligations **$1,799,899**, signed **May1 2024**, performance **May2 2024–February2 2026**, two transactions, latest **January7 2026**; no post-end continuation established. SBA uses May1 as start, whereas USAspending separates signing/performance. Raw records: `live-cate/`. SEI broader pilot ended spring2025 according to its project page, but that does not mechanically terminate every related award; conversely this STTR's longer2026 period does not demonstrate the ethical-governor task continued.
