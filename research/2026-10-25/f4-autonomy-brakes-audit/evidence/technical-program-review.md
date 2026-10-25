# Technical safeguards review

Reviewed 25 October 2026 using public primary documents and project repositories. No Exa or other paid API was used for this review. This is a targeted program review, not a census or a completed funding reconciliation. A program webpage being online is not evidence of continuing appropriations, active contract performance, operational deployment, or a program of record. Table categories describe evidenced functions; secondary tags identify overlap without creating additional dollars.

## Findings that change the proposed story

The public record does not support an absolute claim that ASIMOV's completion eliminated meaningful unclassified safeguards. The Navy reported a September 2026 demonstration of translating operator-set mission authorities and constraints into autonomous execution. A September 2025 Pentagon guidebook explicitly discusses ethical testing and ROE compliance while acknowledging substantial implementation gaps. Historical normative technical work also predates ASIMOV. None of these observations, alone, proves an active, funded ASIMOV replacement or an operational, universally enforced LOAC compliance system.

Category C technologies can support lawful operation, including by improving classification accuracy or enforcing a specified boundary. Their legal significance depends on the specification, test scenarios, failure response, and deployment. A robustness benchmark alone does not demonstrate distinction, proportionality, or civilian-harm testing. Conversely, engineering methods should not be categorically declared incapable of constraining lethal behavior.

## Seventeen likely spokesperson examples

| Example | Classification and concrete function | Status and editorial limit | Primary evidence |
|---|---|---|---|
| ASIMOV | A primary; D secondary. Quantitative benchmarks for ethical difficulty and autonomous-weapons performance in military-value scenarios. | DARPA marks the program complete. It expressly did not build weapons, autonomous systems, or autonomy algorithms. Program-page completion does not establish option nonexercise, reasons, or absence of continuation elsewhere. | [DARPA program](https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values); [December 2024 explanation](https://www.darpa.mil/news/2024/asimov-approaches) |
| ANSR | C primary. Hybrid neuro-symbolic algorithms, assurance evidence, robustness, and mission risk. | Public page describes research, not an acquired operational weapons safeguard. Planned autonomous ISR demonstrations include situation understanding and safe maneuver; no explicit proportionality/civilian-harm benchmark established here. | [DARPA program](https://www.darpa.mil/research/programs/assured-neuro-symbolic-learning-and-reasoning); [selected teams and demonstration](https://www.darpa.mil/news/2023/ansrs-ai-questions) |
| TIAMAT | C primary; potential A/B secondary for detailed review because its shared simulation semantics explicitly include ROE. | Main goal is rapid robust sim-to-real autonomy transfer. Mentioning ROE does not demonstrate legal testing, fielded enforcement, or a completed normative benchmark. Do not suppress this overlap. | [DARPA program](https://www.darpa.mil/research/programs/transfer-from-imprecise); [program-authored paper](https://ar5iv.labs.arxiv.org/html/2503.11007) |
| Assured Autonomy | C primary. Continual safety and functional correctness assurance for learning-enabled cyber-physical systems, including runtime monitoring. | DARPA marks complete; tools can persist after a research program ends. Available tools are distinct from evidence of current funding or military deployment. | [DARPA program](https://www.darpa.mil/research/programs/assured-autonomy) |
| GARD | C primary. Robustness against adversarial ML inputs; repeatable evaluations and defensive tools. | DARPA marks complete. Armory, ART, APRICOT and associated resources remain outputs; no explicit LOAC compliance function established by the program description. | [DARPA program](https://www.darpa.mil/research/programs/guaranteeing-ai-robustness-against-deception) |
| CAML | C primary; B secondary for operator understanding and appropriate autonomy assignment. Self-assessment and communication of competence. | Correct official expansion is **Competency-Aware Machine Learning**. DARPA marks complete. Insight into competence is not a guaranteed human veto or target authorization mechanism. | [DARPA program](https://www.darpa.mil/research/programs/competency-aware-machine-learning) |
| JATIC / MAITE / NRTK | C primary; D secondary. Common AI T&E interfaces, reproducibility and model testing, including natural robustness. | MIT Lincoln Laboratory's MAITE repository identifies JATIC sponsorship. Kitware's archived `nrtk-jatic` package migrated into NRTK in May 2025; repository archival must not be misreported as program termination. No ethics-specific test demonstrated in reviewed descriptions. | [CDAO testing resources](https://www.ai.mil/Initiatives/About/Resources/Pathway-to-AI-Readiness/Testing-and-Evaluation/); [MAITE](https://github.com/mit-ll-ai-technology/maite); [migration notice](https://github.com/Kitware/nrtk-jatic/blob/main/README.md) |
| RAI Toolkit / SHIELD | D primary. Life-cycle risk identification, responsible-use bounds, stakeholder review, accountable officials and decision gates. | Toolkit existence is a real governance counterexample, not proof every weapon is technically constrained. The official GenAI variant is December 2024. The [2024 official CSIAC webinar](https://csiac.dtic.mil/wp-content/uploads/2024/08/Webinar_CSIAC_The-DoDs-Approach-to-Responsible-AI-and-the-RAI-Toolkit_v3.pdf), PDF page 14, identifies singular SHIELD as a toolkit assessment/planning process with six classes of activities; it is not independently established here as a funded weapons testbed; avoid turning the prompt's plural “SHIELDS” into a separate program. | [CDAO RAI resources](https://www.ai.mil/Initiatives/About/Resources/Pathway-to-AI-Readiness/Responsible-AI/); [official GenAI toolkit](https://www.ai.mil/Portals/137/Documents/Resources%20Page/2024-12GenAI-Responsible-AI-Toolkit.pdf) |
| AFRL safe autonomy / RTA | C primary. Runtime safety filters and recovery, with collision-avoidance applications. | AFRL's June 2023 profile names Kerianne Hobbs as safe autonomy and space lead, ACT3. This historical affiliation is not verified as her October 2026 role. The profile does not establish a current award total or LOAC benchmark. | [AFRL/AFMC profile](https://www.afmc.af.mil/News/Article-Display/Article/3420237/afrl-researcher-impacts-community-with-runtime-assurance/) |
| Project Linchpin | C primary; D secondary. Shared sensor-AI MLOps with model V&V and adversarial/Trojan management. | Army August 2023 briefing describes a pre-program activity and projected program initiation in 2026. That forecast must not be reported as proof a program of record was established. Sensor confidence/security can support lawful targeting without demonstrating normative testing. | [Army briefing](https://cpeisw.army.mil/wp-content/uploads/2023/09/Project-Linchpin-Approved-for-Release-1.pdf) |
| TETRAS / FA248722FA002 | C/D provisional. Broad T&E order; precise AI and weapons-assurance workshare requires statement-of-work and transaction review. | USAspending indexed primary page reports $48,989,772.86 obligations, $117,485,156 current and $241,826,327.70 potential value, end 14 March 2028, 38 transactions. These are distinct fields, not a validated ethics budget. Live reconciliation is required before using totals. | [USAspending full award key](https://www.usaspending.gov/award/CONT_AWD_FA248722FA002_9700_FA248718D4700_9700) |
| TALON / FA865124CB024 | C primary. Bayesian information gain and next-look sensor coordination to improve target classification. | SBIR gives original $1,799,795 and October 2026 end; inherited local FPDS audit reports updated $2,839,551.44 and September 2027. Preserve snapshot distinction and verify current history. TRL7 refers to the existing RAPTOR stack, not proof of maturity of new TALON algorithms. | [SBIR award and abstract](https://www.sbir.gov/awards/208992) |
| DCIST | C primary; B secondary research on human interaction/mission specification. Collaborative autonomy, resilience, guarantees and adversarial environments. | Army webpage specifies September 2017–September 2027 and university research consortium. A scheduled period is not proof of continuing outlays or a program of record. University involvement alone does not imply ASIMOV continuation. | [Army DCIST](https://arl.devcom.army.mil/cras/dcist-cra/); [technical report W911NF-17-2-0181](https://arl.devcom.army.mil/arlreport/arl-tr-9435/) |
| STRONG | C primary; B secondary research on human-agent coordination and trust. | Army describes a ten-year fundamental research alliance with seedling/extension cycles. Human teaming does not establish positive human target authorization or an abort guarantee. | [Army STRONG](https://arl.devcom.army.mil/cras/strong-cra/) |
| CAMP | B primary; possible A secondary. Converts operator-set mission authorities, limitations and constraints into autonomous aircraft mission information. | Navy reports an end-to-end MQ-20 demonstration at Gray Flag in September 2026. This is stronger than a proposal but does not establish combat use, universal enforcement or an attributable award amount. | [Navy, 22 September 2026](https://www.navy.mil/Press-Office/News-Stories/display-news/Article/4608456/navy-demonstrates-collaborative-autonomy-mission-planning-for-future-combat-air/) |
| CaTE / RAAEC | A primary; B/C secondary. Physical research proxy tested normative conduct governance with emulated effects. | Pilot concluded spring 2025. Technical demonstration strengthens the counterexample; no deployment maturity or current CaTE funding is established. | [SEI project](https://sei.cmu.edu/projects/cate-increasing-warfighter-trust-autonomous-systems-accelerate-adoption-cutting-edge-capabilities/); detailed limits below |
| CODORD / DONATELLO | A-enabling primary; B/C secondary. Norm-oriented compliance reasoning expressly includes autonomous-system ROE. | Recent funded research outputs; current award periods and obligations require live reconciliation. Civilian deontic benchmarks are not weapons LOAC validators. | [Separate CODORD review](codord-review.md) |

## Additional adversarial counterexamples and open checks

**CETLAWS:** The 2024 peer-reviewed paper [Supporting Ethical Decision-Making for Lethal Autonomous Weapons](https://www.tandfonline.com/doi/pdf/10.1080/15027570.2024.2366094) describes a Bayesian ethical decision model, human-set Laws-of-War/tactical thresholds, transparent strike/no-strike recommendations, and initial trials. This is A/B research, not merely collision avoidance. Its abstract presents operational employment as a future possibility. A secondary award index identifies Phase II FA864922P1015 ($750,000; May 2022–December 2023); that amount/status still requires a primary live award check. A 2024 paper does not establish active 2026 funding.

**RAIDER / Navy topic N193-141:** [The 2019 Navy SBIR solicitation](https://navysbir.us/n19_3/N193-141.htm) requires autonomous planning to satisfy operator objectives and ROE, including unexpected noncombatant maneuvers, and asks for assurance that decisions are appropriate. A/B/C overlap is justified. A requirement is not an award, validated guarantee, current funded program, or ASIMOV successor. Trace selected performers and follow-ons rather than count this topic as funded dollars.

**ResilienX FA864926P0169:** Public secondary index gives explainable-AI model-health monitoring for unmanned-aircraft ecosystems, a $74,973 Phase I, June–September 2026. No primary award/abstract successfully verified in this review. Keep as C candidate and explicitly unresolved, not an active A/B example.

**CAMP chronology and people:** The September Navy primary source names Captain Todd “Toby” Keith as PMX-281 program manager and identifies Strike Planning & Execution Systems under the Program Acquisition Executive for Munitions. It verifies those affiliations in September 2026; earlier PMA-281 branding and an April demonstration must be separately dated. The September event must not be conflated with an earlier reported flight.

## What the 2025 autonomous-systems test guide actually says

The [September 2025 DT&E of Autonomous Systems Guidebook](https://www.cto.mil/wp-content/uploads/2025/10/DTE-of-AS-GB.pdf), printed pages 51–52, explicitly identifies difficulty translating ethical behavior into testable requirements and the lack of clear established standards for implementing/testing the five ethical principles. It also connects ethics to assurance cases, simulation, runtime assurance, teaming and task-based certification. Printed page 124 describes LVC examination of ROE compliance; printed pages 172–173 discuss withholding task certification when trustworthiness is insufficient. This is D guidance with A/B/C technical methods, not evidence those methods are universally implemented or separately funded. Its 2025 date does not establish compliance with a later alleged 2026 deadline. The [February 2025 AI-enabled systems companion](https://www.cto.mil/wp-content/uploads/2025/02/TE_of_AIES_Guidebook_Final_26Feb25.pdf) separately connects testing with responsible-AI policy and human-system integration.

## Reporting questions that would resolve the remaining distinctions

1. For CAMP/RAIDER, what executable constraint types, noncombatant scenarios, communications-loss responses and failed-test outcomes are publicly documented? Are mission constraints immutable onboard, or can autonomy amend them?
2. For ANSR/TIAMAT, did ROE or neutral-entity handling become acceptance criteria, and where are the relevant benchmark definitions and results?
3. For JATIC and the RAI Toolkit, which specific test components measure civilian harm, distinction, proportionality or ethical decision-making, and which programs are required to run them?
4. For the guidebook, which recommendations became enforceable acquisition gates, who accepts residual ethical risk, and what public evidence shows a task certification withheld or deployment stopped?
5. For CETLAWS and ASIMOV performers, which award identifiers fund post-base continuation? An employer or research-topic overlap is insufficient to establish transfer.

No source outreach was performed. No raw third-party document bodies are redistributed in this note. Dollar figures marked provisional are excluded from any defensible aggregate until the main audit reconciles them against primary transaction histories.

## Direct retrieval receipts

Direct HTTP receipts on 25 October 2026 (UTC). These hashes identify retrieved bytes, not an endorsement of content or a permanent version. Navy HTTP retrieval was forbidden; its primary text was inspected through web search/open. The initial Python request attempt failed because the optional requests package was absent; urllib then completed the listed fetches. Raw bodies were not saved or published.

```json
[
  {
    "url": "https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values",
    "status": 200,
    "bytes": 39641,
    "sha256": "c763692d52e5c37fc8e9daea651ff80ca226ff1e0f1f843cbc2699c8a49e6aea"
  },
  {
    "url": "https://www.darpa.mil/research/programs/assured-neuro-symbolic-learning-and-reasoning",
    "status": 200,
    "bytes": 40449,
    "sha256": "0782c41482c585ddc221bebd313fb680020c012b50be81ae727e48f7c9a57410"
  },
  {
    "url": "https://www.darpa.mil/research/programs/assured-autonomy",
    "status": 200,
    "bytes": 41966,
    "sha256": "a7a3088ebf5edee092531337b791774a5132f3e1be1744c0058a5e1424e6371c"
  },
  {
    "url": "https://www.darpa.mil/research/programs/guaranteeing-ai-robustness-against-deception",
    "status": 200,
    "bytes": 39716,
    "sha256": "fdc84fb0ecc3ce101eb30f8649982686b914f8a8e361832c37f707c76da63728"
  },
  {
    "url": "https://www.darpa.mil/research/programs/competency-aware-machine-learning",
    "status": 200,
    "bytes": 37964,
    "sha256": "752cb5f10f8fa321650f25b88ecce6f6e6f705b0018f86c62abda118946ccbee"
  },
  {
    "url": "https://www.darpa.mil/research/programs/transfer-from-imprecise",
    "status": 200,
    "bytes": 41956,
    "sha256": "d1e43a4117eb962b3c5a7e77fc204a10892450e1844aa9b6526d853f3e5d87d6"
  },
  {
    "url": "https://www.cto.mil/wp-content/uploads/2025/10/DTE-of-AS-GB.pdf",
    "status": 200,
    "bytes": 3012164,
    "sha256": "8495e06209072a9a6e05300a1580bbfa1ed93b2fbec418b897dbffafa28e60f7"
  },
  {
    "url": "https://arl.devcom.army.mil/cras/dcist-cra/",
    "status": 200,
    "bytes": 220861,
    "sha256": "7e7c3fb342e923b8b7f632ae7b165d7637bb62985480894f57528cc659493690"
  },
  {
    "url": "https://arl.devcom.army.mil/cras/strong-cra/",
    "status": 200,
    "bytes": 227685,
    "sha256": "7212c948f6107449c7749d9fcd96fc3fafc3006641b165c569a0d11db2c63539"
  },
  {
    "url": "https://raw.githubusercontent.com/mit-ll-ai-technology/maite/main/README.md",
    "status": 200,
    "bytes": 5522,
    "sha256": "2043ee1424013d6433a7bd3b49cdc1b1defc4b287bda9a4ff6f9396b64edd0b4"
  },
  {
    "url": "https://navysbir.us/n19_3/N193-141.htm",
    "status": 200,
    "bytes": 18908,
    "sha256": "dd863ef2c8b8b7fe3e3654712778746f1dcfb66a34ec31d80c535e5ef5871198"
  },
  {
    "url": "https://www.navy.mil/Press-Office/News-Stories/display-news/Article/4608456/navy-demonstrates-collaborative-autonomy-mission-planning-for-future-combat-air/",
    "error": "HTTP Error 403: Forbidden"
  },
  {
    "url": "https://www.sbir.gov/awards/208992",
    "status": 200,
    "bytes": 36996,
    "sha256": "17958a13bc476b33e9e3ec73ce075cf15085647bc3f46560b8e46da3932c95b1"
  }
]
```

## Additional checks requested by the editor

**CaTE timing:** [SEI’s project page](https://sei.cmu.edu/projects/cate-increasing-warfighter-trust-autonomous-systems-accelerate-adoption-cutting-edge-capabilities/) explicitly says the USD(R&E)-requested pilot concluded in spring 2025. Its outputs include the Reference Architecture for Assuring Ethical Conduct in LAWS and the CaTE Development/TEVV Guidebook. The existence and later publication of these A/B/C/D research outputs must not be recast as proof of a newly funded 2026 program or ASIMOV follow-on.

**SHIELD scope:** The official CSIAC webinar cited in the table calls SHIELD a life-cycle planning/assessment process routing users to tools and tracking concerns. PDF page 17 calls its gates recommended considerations; pages 13 and 20 distinguish available toolkit components from dashboards or integration work still in development in that presentation. It is a real governance tool, with technical-tool links, rather than a demonstrated onboard weapons governor. Its named presenter, Drew Brooks, was Lead Scientist for Responsible AI Tools in the 2024 presentation; no current 2026 role is inferred from that document.

**Current CDAO people:** The [current CDAO leadership page](https://www.ai.mil/Leadership/news/) identifies Cameron Stanley as Chief Digital and AI Officer, Andrew Mapes as acting principal deputy, David Jin as acting deputy for Enterprise Mission Area, and Kaleb Redden as deputy for Strategy, Governance and Partnerships. Jin’s biography specifically describes his previous AI Assessment and Assurance division leadership and work on T&E/continuous monitoring. These are current page roles, not proof that Jin presently runs JATIC or the RAI division. The 2023 toolkit release’s Diane Staheli/Craig Martell roles are historical. Specific 2026 JATIC product-owner and RAI-division leadership remains unverified in this review.

## Round-two evidence refinement: demonstrated normative prototype

The April 2025 [SEI Reference Architecture report](https://www.sei.cmu.edu/documents/6225/CaTE_LAWS_Reference_Architecture_9VryTJo.pdf) is stronger evidence than a design framework alone: Appendix A reports a physical TurtleBot4 research proxy and six months of development/testing (printed p35 / PDF39). It generated 58 requirements, including 28 ethical-value formalizations (p37 / PDF41). A scenario includes human permission, de-escalation and surrender (p38 / PDF42). Effects were emulated using lights/audio; this was not a weapon demonstration (pp54–55 / PDF58–59). It is A/B technical research, not proof of operational readiness: collateral-damage evaluation was excluded, human interaction was limited, and some simulated responses were preauthorized (pp54–55). The authors explicitly deny deployment-level maturity (p58 / PDF62). Legal markings attribute support to DoD contract FA8702-15-D-0002 (p63 / PDF67); no CaTE-specific dollar allocation is stated.

The [SEI contracting page](https://www.sei.cmu.edu/work-with-us/) distinguishes predecessor FA8702-15-D-0002’s expired ordering period from performance through 29 June 2030. Successor FA870225DB003 has base ordering/performance 1 July 2025–30 June 2030, with an option through June 2035. The [May 2026 sponsor guide](https://www.sei.cmu.edu/library/dod-work-sponsor-user-guide/) confirms these are broad FFRDC vehicles. Their continuing availability does not establish continued CaTE funding or justify assigning all vehicle dollars to ethical safeguards. The pilot ended spring 2025, as the project page states.

The [DVIDS copy of the Navy CAMP release](https://www.dvidshub.net/news/575299/navy-demonstrates-collaborative-autonomy-mission-planning-future-combat-aircraft) confirms the September 22, 2026 date and is directly retrievable, resolving the earlier Navy-host retrieval gap without altering that logged 403.

Direct retrieval, 25 October 2026: SEI PDF HTTP200, 2,582,006 bytes, SHA256 `89b061396da45f58ff8b9c7fc24a46e57a08a6ea460b749beedfb998a8a6ca88`; DVIDS HTTP200, 68,991 bytes, SHA256 `da597407ae9336c5b051c22005b1926afc2ae12227f954a9be39084d50771ec0`. Raw PDF was retained privately in temporary storage for text extraction, not added to the publication package. One web follow-up timed out; direct PDF extraction resolved it.
