# Eglin collaborative autonomy contracting evidence

Research cutoff: 24 October 2026. This is a public-source procurement and programme-history audit, not a technical assessment of weapon effectiveness. No outreach or publication was conducted.

## Findings that change the story

1. **The supplied “14 active contracts” claim cannot be reproduced without its missing list or selection criteria.** The fixed F2 register contains 22 award identifiers beginning FA8651: 20 procurement contracts and two grants. Six have a latest reported current completion date after the cutoff; 16 have an earlier date. This is a date-field test, not a finding that all six are actively performing or that the other 16 have legally closed. The register itself labels these as automated candidates, not individually validated findings. It is not the complete FA8651 portfolio.
2. **TALON is not shown ending on 26 October 2026 anymore.** FPDS modification P00003, signed 2 April 2026, increased the award by $1,039,756 and extended the reported current and ultimate completion dates to 30 September 2027. The current total is $2,839,551.44. SBIR.gov still displays the original schedule and approximately $1.8 million, so it is useful for the proposal and investigator, not current financial status.
3. **EpiSci moved in the opposite direction.** Its June 2025 modification reduced current/potential value from $2,399,979 to $1,592,988 and shortened the reported completion date from 1 October 2026 to 1 October 2025. The modification is a within-scope supplemental agreement, not a termination code. Do not call it a cancellation, failure or successful completion without further evidence.
4. **GTRI's $1.65 million is obligations, not the full award value.** The supersonic-munitions order has $3,047,239 in base-and-exercised value, the same amount including all options, and a 3 September 2027 completion date. Its June 2026 funding modification alone does not establish faster research or a physical test.
5. **“Same contracting office” is supported; “all at the same base” is not.** Among the six named cases, reported principal performance places are Laurel, Maryland (both APL orders), Atlanta, Georgia (GTRI), Poway, California (EpiSci), Woburn, Massachusetts (SSCI), and Eglin AFB, Florida (Aurora). These fields also do not enumerate every laboratory, subcontractor or test range.
6. **The 22-entry slice includes one ASIMOV award, Saab RESPECT.** It is an ethics/evaluation framework, not direct evidence of weapon development. The two investigations must not count it twice as different evidence. No primary source found establishes that AFRL's Munitions Directorate performs ASIMOV's substantive independent verification and validation; the shared contracting relationship is clearer than the programme-execution relationship.

The six named awards total **$12,256,665.44 in net obligations**, versus **$13,653,904.44 in current/base-and-exercised value**. These are six specific awards, not the total cost of a weapons programme. They are not expenditure or delivery totals.

## Evidence and reproducibility

The starting population is [audit/lane1-tactical-candidates-384.csv at fixed commit e931fcbc6dc52c00b0565e853637a64fa95773b3](https://github.com/graemesmith-code/investigative-methods/blob/e931fcbc6dc52c00b0565e853637a64fa95773b3/research/2026-10-24/f2-tactical-ai/audit/lane1-tactical-candidates-384.csv). Every FA8651-prefixed row in its 384-entry tactical register is retained in `fa8651-cohort-audit.csv`, including weak or peripheral matches. No discretionary filter was applied to manufacture a count of 14. The local register was retrieved as connector text with line endings normalized, so it is not claimed to be byte-identical to the published CSV.

All 22 current award records were independently retrieved from the official USAspending API on 24 October 2026. All 124 published FPDS actions across the 20 contracts were retrieved, including pagination. Sums of action-level obligation changes, base-and-exercised value changes and base-and-all-options value changes reconcile exactly to each current USAspending contract record. The two grants do not have FPDS contract histories and are marked accordingly. USAspending and FPDS share underlying reporting; this reconciliation checks consistency, not two independent confirmations of delivered capability. The companion `fa8651-contract-actions.csv` preserves the action-level evidence and source URLs.

Current award totals are cumulative; action values are changes, not new cumulative totals. Current completion is the reported performance period for the current contract configuration. Potential completion/value and unexercised options are separate concepts. A modification, a payment, a contract award, a proposal, a simulation result, a physical demonstration and production procurement are not interchangeable evidence.

The public record has a lag. [GAO explains that DoD procurement data is subject to a 90-day publication delay](https://www.gao.gov/blog/2019/11/13/the-data-act-checking-in-on-spending-transparency). Consequently, absence of a visible late-2026 action cannot prove no action occurred. The audit's precise claim is about records visible at the cutoff, not a real-time operational census.

## The six named cases

### Johns Hopkins APL supersonic NCA

**FA865124FB043**, “Supersonic Weapon Network Collaborative and Autonomous (NCA) Program,” is a cost-plus-fixed-fee delivery order under **FA865123DA002**, not a standalone production contract. It was signed and began on 22 July 2024, with $1.2 million initially obligated against $4,998,538 in current/potential value. Funding-only actions eventually obligated the entire $4,998,538. The last positive funding action was 1 April 2026. A zero-dollar within-scope agreement on 28 May 2026 extended completion from 21 July to **30 September 2026**. The reported period therefore precedes the cutoff.

The current record identifies **Laurel, Maryland** as principal place of performance, FA8651 AFRL RAZ as awarding office and F1TBTA AFRL RW RWTA HANGAR 421 as funding office. PSC AC13 is experimental development. The title establishes the research subject, but no exact public platform, live-test result, production transition or named investigator was established for this order. [Official award](https://www.usaspending.gov/award/CONT_AWD_FA865124FB043_9700_FA865123DA002_9700/).

### Johns Hopkins APL graph-neural-network guidance

**FA865125FB046**, “Network Collaborative Autonomous Weapon Guidance with Graph Neural Networks,” is another cost-plus-fixed-fee delivery order under **FA865123DA002**. Its only published action was signed **1 May 2025**, with performance from **5 May 2025 to 4 August 2026**. Obligations, current value and potential value are each **$182,775**. PSC AC12 denotes applied research. Performance is recorded in **Laurel, Maryland**, with the same awarding and funding offices as the larger APL order.

A small research order with a technically specific title is not proof of a deployed graph-neural-network weapon. No directly linked technical paper, public investigator, physical test or production platform was established. Nor does the shared parent vehicle prove it is a phase of the larger supersonic order. [Official award](https://www.usaspending.gov/award/CONT_AWD_FA865125FB046_9700_FA865123DA002_9700/).

### Georgia Tech supersonic collaborative autonomy

**FA865125FB053**, “Collaborative Autonomy for Supersonic Munitions,” is a cost-plus-fixed-fee delivery order under the GTRI UARC vehicle **FA865121D0016**. It was signed and began **5 June 2025** and reports completion on **3 September 2027**. The base action obligated $1.35 million against a **$3,047,239** current/potential value. A **24 June 2026** funding-only modification added $300,000, making current obligations **$1.65 million**, without changing completion or total value.

The record specifies **Atlanta, Georgia**, FA8651 AFRL RAZ as awarding office and F4FBQT AFRL RQT as funding office; PSC AC13 is experimental development. GTRI has an independently documented Golden Horde history, but that does not establish that the same software, engineers or platform execute this later supersonic order. No exact flight-test or production milestone was established. [Official award](https://www.usaspending.gov/award/CONT_AWD_FA865125FB053_9700_FA865121D0016_9700/).

### Aurora REACH

**FA865124FB054**, “Networked Collaborative Autonomous (NCA) Weapon Reachability for Weapon Target Assignment (WTA) (REACH),” is a cost-plus-fixed-fee delivery order under **FA865121D0022**, the swarm-munitions R&D vehicle. Signed **24 June 2024**, performance began the next day. The original $495,807 order was expanded in March 2025; current obligations and both value measures are **$992,813**. Successive date changes produced a **19 December 2025** reported completion date. The last positive funding was **8 July 2025**, and the last signed modification was administrative, **18 September 2025**.

Unlike the other five named cases, its principal performance place is **Eglin AFB, Florida**, although the recipient is based in Manassas, Virginia. Its funding office is F1TBTA AFRL RW RWTA HANGAR 421 and its PSC AC12 is applied research. The title supports a research effort on coordinating assignments, not an inference about a specific live weapon, fully autonomous release authority or an operational deployment. No exact public investigator or platform was established. [Official award](https://www.usaspending.gov/award/CONT_AWD_FA865124FB054_9700_FA865121D0022_9700/).

### EpiSci collaborative-weapons learning

**FA865123CB002**, “Deep Model-Based Reinforcement Learning for Collaborative Autonomous Weapons,” is a firm-fixed-price definitive contract. FPDS identifies **SBIR Phase III** actions. It was signed **25 September 2023**, with performance starting **1 October 2023**. Original current/potential value was $2,399,979 and completion was 1 October 2026. On **3 June 2025**, P00006 added $197,297 in obligations while reducing current/potential value by $806,991 and moving completion to **1 October 2025**. Current obligations and both value measures are **$1,592,988**. These apparently contrary movements are compatible: more of a smaller award became obligated.

Performance is **Poway, California**; the funding office is F1TBTA AFRL RW RWTA HANGAR 421. Phase III is a procurement-programme classification, not evidence of serial production or operational fielding. EpiSci's December 2021 release documents Golden Horde **simulation** participation, but does not establish a flight test under this exact 2023 contract. [Official award](https://www.usaspending.gov/award/CONT_AWD_FA865123CB002_9700_-NONE-_-NONE-/); [EpiSci historical announcement](https://www.episci.com/newsroom/episcis-tactical-ai-competes-in-the-golden-horde-colosseum).

### Scientific Systems TALON

**FA865124CB024**, “Tactical Autonomous Look Optimization Network,” is a firm-fixed-price definitive contract and **SBIR Direct to Phase II** award, signed and begun **31 July 2024**. It originally obligated **$1,799,795.44**, with completion on 26 October 2026. The **2 April 2026** within-scope agreement raised obligations/current/potential value to **$2,839,551.44** and extended both dates to **30 September 2027**. A **21 July 2026** within-scope modification changed no financial total or completion date.

Performance is **Woburn, Massachusetts**; the latest normalized funding-office label is F4FBEQ AFRL RGF. SBIR.gov names **Fabrizio Santini** as principal investigator. Its abstract describes proposed research using SSCI's existing RAPTOR autonomy stack as a development testbed, and simulation compatible with Colosseum. Its TRL 7 claim concerns the underlying stack, **not demonstrated maturity of the newly proposed TALON algorithms**. No TALON-specific live weapon platform or physical test was established. [Official award](https://www.usaspending.gov/award/CONT_AWD_FA865124CB024_9700_-NONE-_-NONE-/); [SBIR award and proposal abstract](https://www.sbir.gov/awards/208992).

The original AF241-D015 topic puts the research in the context of confidence and correctness in target classification, including the risk that repeated, dependent observations falsely inflate confidence. This is a reason to investigate assurance, not a reported solution or test result. The topic explicitly uses a Direct-to-Phase-II route, so generic aggregator text describing a funded Phase I predecessor is not evidence of such an award. [Official solicitation, topic AF241-D015, printed page 49](https://media.defense.gov/2023/Nov/28/2003348086/-1/-1/0/AF_SBIR_241_DP2.PDF). Direct PDF retrieval returned HTTP 403; the relevant topic text was available in the search index. The award's Direct-to-Phase-II classification is independently on SBIR.gov.

## Parent vehicles and why their ceilings are not extra spending

- **APL FA865123DA002**: single-award IDIQ signed 16 December 2022, reported completion 15 December 2027, current ceiling **$99.8 million**. Its remit is broad weapons modeling, simulation, engineering, analysis, testing and fundamental S&T. The parent itself records zero obligations; individual orders carry obligations. Do not add its ceiling to its orders or call the whole vehicle AI spending. [Official parent](https://www.usaspending.gov/award/CONT_IDV_FA865123DA002_9700/).
- **GTRI FA865121D0016**: single-award IDIQ signed 13 September 2021, latest reported completion 31 August 2028, ceiling **$49.9 million**, zero obligations at parent level. [Official parent](https://www.usaspending.gov/award/CONT_IDV_FA865121D0016_9700/).
- **Aurora FA865121D0022**: single-award IDIQ signed 30 September 2021, reported completion 14 September 2026, ceiling **$5 million**, zero obligations at parent level. [Official parent](https://www.usaspending.gov/award/CONT_IDV_FA865121D0022_9700/).

These ceilings and dates come from current award records. An older Air Force base-contract list still shows APL at $49.9 million and EpiSci at $2.4 million through October 2026, illustrating why a dated institutional list cannot replace an action-history audit. Its $0 child-order rows do not mean no money was committed. [Air Force historical portfolio list](https://www.afrl.af.mil/Portals/90/Documents/SB/AFRL_Active_OTSB-SB_Contracts.pdf).

## The surrounding cohort is mixed

The complete CSV gives every award its current financial values, date fields, principal place of performance, awarding/funding agencies and offices, exact parent, scope note and evidence URLs. The six date-field matches are TALON, Dynetics FA865124FB014, GTRI FA865125FB053, Systems & Processes Engineering FA865126CB007, APL FA865126FB014, and GTRI CHASM FA865123FA038. This list includes a proximity sensor and broader AI-guidance research: being within a reported period is not the same as being an autonomous collaborative weapon.

Other retained entries cover a magnetometer, a seeker, image capture for AI training, autonomous-flight grants, electronic-effects munitions and the ASIMOV evaluation framework. QUADTEAM's abbreviated title alone is insufficient to establish what it does, and its current awarding-office label is DCMA Northeast despite its historical FA8651 identifier.

The screen also omits relevant infrastructure. GTRI **FA865123FA001** explicitly funded Golden Horde Colosseum hardware-in-the-loop integration, **$2,565,087**, from **23 November 2022 to 15 April 2025**, under FA865120D0070. It is not in the fixed 22-entry slice. Its current record was modified 31 October 2025, after the reported performance end; that modification timestamp alone does not extend performance. [Official award](https://www.usaspending.gov/award/CONT_AWD_FA865123FA001_9700_FA865120D0070_9700/).

A second perimeter example is OKSI **FA865124CB025**, “Best Look Fusion for cUAS Engagements,” from the same AF241-D015 topic as TALON. Its SBIR proposal names APKWS hardware. That platform is **not evidence of TALON's platform**. This example is outside the 22 and has not received the full financial-history audit here. [SBIR source](https://www.sbir.gov/awards/208985).

## What the location evidence does and does not establish

FA8651 is an Eglin-linked AFRL contracting code; an [official acquisition hierarchy](https://www.acq.osd.mil/asda/dpc/ce/p2p/docs/training-presentations/2019/P2P-Symposium-PIEE-Hierarchy.pdf) places it there. Older records call the office RWK; current normalized records often say RAZ. Neither label establishes where every person works or where software is tested.

The six named capability-research awards have Air Force funding, while the ASIMOV overlap has DARPA funding and Air Force awarding. Across all 22, only Aurora REACH, Dynetics FA865124FB014 and SAIC FA865122F2118 report Eglin as principal performance place. The two grants report multi-state performance, not their university headquarters. Historical Golden Horde flights used White Sands Missile Range; a launch aircraft's home unit at Eglin is not the same fact as a test's location.

The defensible institutional question is therefore: **Did the Eglin organisation only administer ASIMOV awards, or did it also provide technical evaluation, data or staff?** The published ASIMOV BAA describes a government IV&V team spanning DARPA, testing, modeling and services, but the evidence reviewed does not name AFRL/RW's precise execution role. Absence of a public name is not proof of no role. A separate, older AFRL programme also called ASIMOV studied swarms and communications; it must not be conflated with DARPA's ethics-benchmarking programme.

## Novelty hypotheses and contrary evidence

- **Hypothesis: a distributed research network is carrying collaborative-weapons concepts into supersonic and learning-based guidance.** Supporting evidence is the exact APL and GTRI order titles, common broad research vehicles, and documented institutional Golden Horde experience. Contrary evidence: the titles do not name fielded systems, technical leads or flight milestones, and no exact award-to-platform bridge was established.
- **Hypothesis: assurance infrastructure matters as much as the visible weapons.** Supporting evidence includes TALON's confidence problem, Colosseum simulation history, the explicit GTRI hardware-in-the-loop integration order and ASIMOV's separate evaluation purpose. Contrary evidence: shared office or supplier does not establish shared algorithms, data, tests or governance.
- **Hypothesis: TALON received a substantive funding and schedule extension while other named efforts reached or shortened their recorded periods.** This is directly supported by modifications, more precise than saying the whole portfolio accelerated. Contrary evidence to an acceleration claim includes EpiSci's reduced value/shortened period and JHU's funding-only modifications. A bigger ceiling or later end can mean more scope, more time or administrative adjustment, not faster progress.
- **Hypothesis: a technical talent and supplier network links earlier demonstrations to newer autonomy companies.** Chris Gentile is documented in EpiSci's 2021 Golden Horde work, at Merlin in 2025 and at Mach in the current company biography. This establishes a career trajectory, not transfer of proprietary software, a particular award or classified knowledge.

A claim that the United States now fields an autonomous supersonic missile swarm is **not supported by these procurement records**. A claim that military researchers and suppliers are being funded to explore collaborative sensing, guidance and coordination is well supported. Publicly demonstrated earlier collaboration should be explained separately from current contract ambitions.
