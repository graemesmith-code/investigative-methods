# IHL / LOAC research: contract and institutional breadcrumb map

Research snapshot: 16 October 2026. This extends the earlier funding note with primary USAspending award and transaction records, subcontract links, named investigators, and evidence of outputs. It is an institutional-funding investigation, not a technical guide to developing weapons.

## Findings that materially change the earlier picture

1. **The Air Force-to-Army chain is real, and now includes a demonstrated training application.** The 2024 CETLAWS paper names its Air Force award. SBA explicitly identifies Army TEELAWS as its sequential successor. West Point reported classroom testing in April 2026. A newly found $49,998 Air Force award from 2021 is a strong earlier-project lead, although its formal Phase I linkage still needs an original SBIR abstract or award document.
2. **All seven ASIMOV prime awards are now resolved to primary procurement records.** They report **$20,495,054 in combined prime obligations**, against **$39,475,202 in combined base-and-all-options values**. These are seven-award figures, not an IHL-specific allocation, outlays, or the program's budget. Subcontracts must not be added to these totals.
3. **The subcontract network is much richer than the seven-prime announcement.** Primary records connect the primes to MIT, UPenn, ASU, UVA, Virginia Tech, George Mason, SIFT, Charles River Analytics, Duality, Shadowbox, David Barnes LLC and Aechelon. Some university/company announcements identify collaborators absent from reported-subaward data.
4. **A concrete continuation exists after ASIMOV:** CoVar's April 2026 PPADM/VectoredAI announcement explicitly invokes its ASIMOV-derived GEARS software. This is an adjacent human-AI decision research continuation; it does not establish operational targeting use or a restarted ASIMOV program.
5. **A separate civilian-harm funding bridge is identifiable:** CDAO funded CNA's “Civilian Harm and Responsible AI” task through ONR, with $500,000 obligated. DSCA separately funded CNA evaluation and HII civilian-harm curriculum work. None of these records alone proves transfer of the Civilian Protection Center of Excellence's staff, authority or work.

## 1. Perceptronics: early ethical-trust award → CETLAWS → TEELAWS → West Point

### Procurement chain

| Project / award | Primary money measure | Recorded period / evidence |
|---|---:|---|
| Ethical Trust Calibration for Lethal Autonomous Robots, **FA864921P1296** | $49,998 obligated; same current and potential value | 14 Apr–14 Jul 2021; Air Force SBIR/STTR contracting office, funding office F4FBEQ AFRL RGF. Similar title, same recipient and sponsor make it a strong predecessor lead; formal Phase I relationship not yet verified. [USAspending API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_FA864921P1296_9700_-NONE-_-NONE-/) |
| CETLAWS, **FA864922P1015** | $750,000 obligated; same current and potential value | 2 May 2022–11 Dec 2023. Original obligation $750,000; 5 Sep 2023 modification added $0. [USAspending API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_FA864922P1015_9700_-NONE-_-NONE-/) |
| TEELAWS, **W5170125C0052** / W51701-25-C-0052 | $1,899,998.92 obligated; same current and potential value | Initial action 23 Oct 2024, USAspending performance start 30 Oct 2024, end 29 Oct 2026. SBA rounds to $1,899,999 and uses 23 Oct as start. [USAspending API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_W5170125C0052_9700_-NONE-_-NONE-/), [SBA abstract](https://www.sbir.gov/awards/215327) |

Perceptronics UEI: **MKQPJJKHDG89**. SBA identifies **Spencer Kohn** as TEELAWS principal investigator and **Elan Freedy** as business contact; topic AF211-CSO1, agency tracking FX211-CSO1-0051. It explicitly says Army educational work modifies CETLAWS algorithms, provides collateral-risk/environmental feedback rather than engagement decisions, and initially embeds in West Point training. It also expresses an ambition for eventual operational adoption: an ambition is not a fielding record. No subawards were returned for the two later awards; that does not rule out consultants or unreported relationships. [SBA](https://www.sbir.gov/awards/215327)

### Paper and professional network

The June 2024 paper **“Supporting Ethical Decision-Making for Lethal Autonomous Weapons,” DOI 10.1080/15027570.2024.2366094**, explicitly acknowledges FA864922P1015. It reports an initial Bayesian legal/ethical decision-support prototype and fictional-scenario evaluation, with wargaming/training as immediate applications and operations as prospective. Named researchers include Spencer Kohn, Marvin Cohen, Gershon Weltman and AFRL's Joseph Lyons. Acknowledgments identify government technical contacts **Joseph Lyons**, **Brandi Kutter**, earlier **David Farrell**, and consultant retired Army Col. **Jon Campbell**. These are research/oversight links, not evidence that each institution procured or deployed the prototype. The paper is a useful source for evaluations and limitations, not independent validation of complete IHL compliance. [Original article](https://www.tandfonline.com/doi/full/10.1080/15027570.2024.2366094), [Belgian defence-library copy](https://budef.mil.be/doc_num.php?explnum_id=272)

### Actual training output and transition leads

West Point's **23 April 2026** report documents TEELAWS testing in **PY201, Philosophy and Ethical Reasoning**. Perceptronics worked with the academy's Department of Law and Philosophy. The 2026 cadets were **Boston Graf, Maksymilian Olszowka and Elizabeth “Ezra” Bardales**; their adviser was **Maj. Grace Ryan**. Graf had worked on the project since August 2024 with the preceding capstone group. The report describes LOAC-related scoring and coaching within training scenarios, and says the team had presented to **Army DEVCOM and IBM**. Broader use in Basic Officer Leadership Courses was a cadet's hope, not a procurement or adoption announcement. This establishes a classroom demonstrator; it does not establish operational deployment, a released evaluation dataset or independent legal validation. [Official Army/West Point report on DVIDS](https://www.dvidshub.net/news/563402/cadets-work-with-software-using-lethal-autonomous-weapons-systems-analyzes-tactical-decisions-provides-ethical-score)

**Next evidence to seek:** final TEELAWS report and deliverable list; West Point PY201 evaluation results; 2025 and 2026 capstone abstracts; subsequent procurement citing the same PI, UEI, topic or project; any formal DEVCOM/BOLC transition agreement. Do not infer funding from a demonstration audience.

## 2. ASIMOV: seven primes and the reported subcontract network

DARPA's current page explicitly labels ASIMOV **complete**. Its December 2024 announcement said it was developing evaluation benchmarks, not weapons, autonomous systems or autonomy algorithms. The intended institutional customer was the **developmental/operational testing community**. DARPA also said eventual tools were intended to be publicly available; this check did not establish a complete final public repository for all teams. [Current status](https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values), [scope and performers](https://www.darpa.mil/news/2024/asimov-approaches)

### Primary award ledger

All seven are DARPA-funded, AFRL-awarded contracts under solicitation **HR001124S0011**. Dates below are latest API fields, not a claim that work continued until every potential date.

| Prime / PIID | Total obligation | Base + all options | Current end | Potential end | Last modified |
|---|---:|---:|---|---|---|
| Kitware / FA865125CB001 | $3,961,000 | $8,261,001 | 2025-10-31 | 2026-10-31 | 2025-09-09 |
| RTX Corporation / FA865125CB002 | $999,956 | $999,956 | 2025-11-30 | 2025-11-30 | 2025-09-10 |
| Systems & Technology Research / FA865125CB003 | $3,136,423 | $6,270,311 | 2025-10-31 | 2026-10-31 | 2025-09-10 |
| CoVar / FA865125CB004 | $3,498,700 | $6,995,555 | 2025-10-27 | 2026-08-14 | 2026-01-20 |
| UNSW / FA865125CB006 | $2,729,992 | $5,723,397 | 2025-10-31 | 2026-10-31 | 2025-06-30 |
| Saab / FA865125CB007 | $2,979,931 | $5,041,849 | 2026-03-31 | 2026-03-31 | 2026-03-19 |
| Lockheed Martin / FA865125CB018 | $3,189,052 | $6,183,133 | 2025-10-31 | 2026-10-31 | 2025-09-09 |
| **Seven-prime sum** | **$20,495,054** | **$39,475,202** | | | |

Each underlying primary award is linked in [primary award ledger](ihl_prime_awards.csv). Direct examples: [Kitware API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_FA865125CB001_9700_-NONE-_-NONE-/), [CoVar API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_FA865125CB004_9700_-NONE-_-NONE-/), [Saab API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_FA865125CB007_9700_-NONE-_-NONE-/). These financial records are more precise than announcement headlines. In particular, a potential ceiling is not an obligation. The earlier DARPA budget figures remain separate and must not be added to this ledger.

### Network edges confirmed by reported subawards

| Prime | Reported subrecipient | Reported amount(s) | Subaward identifier / useful detail |
|---|---|---:|---|
| Kitware | Charles River Analytics | $314,988 | K004749-00-S05 |
| Kitware | Duality Robotics | $205,620 | K004749-00-S03 |
| Kitware | Shadowbox LLC | $152,592 | K004749-00-S06 |
| Kitware | University of Pennsylvania trustees | $140,000 | K004749-00-S04 |
| Kitware | David Barnes LLC | $104,999 | K004749-00-S02 |
| RTX | SIFT | $60,000 | 2611239; CALVIN |
| RTX | Virginia Tech | $17,850 | 2611241; CALVIN |
| STR | Aechelon Technology | $288,925 | DM24-3334; image/sensor-generation support |
| STR | George Mason University | $150,000 | 2025-0018 _GEORGE MASON UNIVERSI; decomposition of principles into attributes/observables |
| Saab | MIT | $1,089,681 | 65010; DARPA ASIMOV research |
| Lockheed Martin | University of Virginia | $60,000; $40,000; $100,000 | Three reported rows sharing 4106527004, dated Dec 2024, Jan 2025, Jul 2025 |
| Lockheed Martin | Arizona State University | $40,000; $60,000; $60,000 | Three reported rows sharing 4106525286, dated Dec 2024, Jun 2025, Aug 2025 |

Source: USAspending `/api/v2/subawards/`, POST with each primary generated award ID, page 1, limit 100; all responses reported no next page. The exact 16 rows are preserved in [reported subaward ledger](ihl_reported_subawards.csv). **Do not add these amounts to prime obligations.** Lockheed's multiple rows are retained as reported rather than pretending they represent six distinct subcontracts or six institutions. Absence of a reported subaward is not proof of absence of a collaborator.

### Investigators, named approaches and continuations

- **Kitware:** PI **Arslan Basharat**. Its announcement names **Duality AI, Charles River Analytics, University of Pennsylvania, Shadowbox, David Barnes LLC and Veraitech**. Veraitech is announced but absent from the five reported subawards retrieved here. The $3.9m announcement aligns with the approximately $3.961m current award, while the $8.261m record includes potential options. [Kitware announcement](https://www.kitware.com/kitware-awarded-3-9m-darpa-contract-to-develop-standards-for-evaluating-ethics-in-ai-driven-military-technologies/)
- **Saab/MIT RESPECT:** Saab leads **Devesh Upadhyay** (PI) and **Christopher Vo**; MIT leads **Chuchu Fan** and **Nicholas Roy**. A named evaluation framework plus a $1.089m MIT subaward is a strong contract-to-academia link. [Saab announcement](https://www.saab.com/markets/united-states/us-newsroom/stories/2025/darpa)
- **UNSW/ASU:** project **Adversarial Generative Ethics for Autonomous Weapon Systems**, led by **Deane-Peter Baker**. UNSW's announcement names its computing and law units and ASU CHART. **Spring Berman's university CV** reports an ASU project total of $1,093,239 within a $5,723,397 overall project; this is a project-total disclosure, not verified obligations. It lists UNSW colleagues **Hussein Abbass, Erandi Hene Kankanamge, Natalia Jevglevskaja**, and ASU colleagues **Nancy Cooke, Kathryn Johnson, Theodore Pavlic**. It supplies a second ASU edge, distinct from the Lockheed subcontract. [UNSW announcement](https://www.unsw.edu.au/news/2025/01/unsw-awarded-contract-to-develop-framework-for-measuring-ethical), [Berman CV](https://search.asu.edu/profile/1943720/cv)
- **RTX CALVIN:** the primary subaward descriptions expand this as **Criteria for AI with Legally Informed Values and Nonmaleficence**. The SIFT and Virginia Tech edges are presently stronger evidence than generic generated descriptions on commercial contract mirrors. Named PIs and final outputs remain unresolved.
- **CoVar GEARS:** **Pete Torrione** is the senior publicly quoted lead; **Thomas Powers** independently records ASIMOV consulting with CoVar on his university CV. Duality's involvement is publicly announced even though no CoVar subaward appeared in this API response. [University CV](https://www.udel.edu/content/dam/udelImages/bidenschool/Documents/cvs/Thomas-Powers_CV.pdf)
- **Follow-on lead, not just speculation:** CoVar's **9 April 2026** announcement of a DARPA Direct-to-Phase-II **PPADM** award names **VectoredAI**, collaborator **Jim Neidhoefer**, and explicitly connects its approach with ASIMOV-developed GEARS. The award number and amount were not recovered in the bounded procurement search. This establishes an announced adjacent continuation in human-AI decision/trust research, not an IHL-specific spending amount or weapon deployment. [Company release](https://www.prnewswire.com/news-releases/covar-awarded-direct-to-phase-ii-darpa-sbir-contract-for-predictive-psychological-architectures-for-decision-making-ppadm-302738479.html)

**High-value missing documents:** seven final technical reports; whether options were declined, terminated or simply never exercised; ELSI advisory membership and recommendations; common evaluation rubric; final benchmark/tool releases; transition agreements with test organizations. A potential end date cannot answer these questions.

## 3. CODORD: legal-language research network and public outputs

DARPA's program manager is **Benjamin Grosof**. The official program names **USC**, **RTX BBN** and **SRI** as performer groups and explicitly proposes applications to ROE, commander's intent and allied legal authorities. This is broader rules-to-logic research, not exclusively targeting or IHL. [DARPA program](https://www.darpa.mil/research/programs/codord)

### Funding / institutional branches

- **USC DROIDDS, HR00112590089.** UCLA's **Guy Van den Broeck** funding page identifies PI **Jay Pujara**, with co-investigators Van den Broeck and **Vibhav Gogate** at UT Dallas. UT Dallas reports a **$44,960 first increment**, and **$299,825 expected if phase 2 is funded**; neither is the entire USC award. [UCLA funding page](https://web.cs.ucla.edu/~guyvdb/funding/), [UT Dallas disclosure](https://engineering.utdallas.edu/innovation/2025-research-awards/)
- Pujara's own CV records **$1,014,000** for DROIDDS but prints a **6/23–12/25** period, inconsistent with CODORD's 2024 announcement and 2025 award trail. Treat the amount as a self-reported grant figure needing reconciliation, **not verified current obligations**, and do not silently fix the dates. Commercial mirrors suggest a $2m ceiling. This check did not retrieve a primary OT transaction ledger for USC. [CV, funding section p.3](https://www.jaypujara.org/pdf/pujara_cv.pdf)
- **RTX BBN DONATELLO.** Primary company reporting identifies PI **Brian Ulicny**, with **Johns Hopkins University and Stony Brook University** on the team. Stony Brook separately identifies **Paul Fodor**. **HR00112590088** is a useful commercial-procurement-mirror identifier; it is not promoted here to primary-verified obligations. [RTX announcement](https://www.rtx.com/news/news-center/2025/08/28/rtx-bbn-technologies-to-empower-ai-to-understand-and-apply-regulatory-legalese), [Stony Brook announcement](https://news.stonybrook.edu/?p=246566)
- **SRI:** DARPA lists a 2026 unpublished manuscript by **J. Cadigan, M. Wessel and L. Morgenstern** on translating regulatory text and repairing/explaining errors. The public program page establishes this research branch; exact award ID, amount and published deliverable remain open.
- **Separate JHU Applied Physics Laboratory task HR001125F0028**, under **HR001122D0001**: **$2,481,841 obligated**, **$3,259,077 base/exercised**, **$3,321,820 all options**, performance **4 March 2025–16 April 2027**, last modified **20 April 2026**. It explicitly names CODORD. The record does not specify its evaluation/integration role, so do not infer one. Do not conflate APL's direct task with Johns Hopkins' academic role on BBN's team. [Primary API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_HR001125F0028_9700_HR001122D0001_9700/)

### Outputs available for examination

DARPA links USC's **LOGicalThought** (2026), BBN-team **DeonticBench** and **DAR: Deontic Reasoning with Agentic Harnesses**, as well as statutory/tax-reasoning papers. These are useful evidence of continuing research output, not proof of funded phase-2 exercise or deployed ROE software. [DARPA output list](https://www.darpa.mil/research/programs/codord)

**DeonticBench** supplies 6,232 tasks across tax, airline policies, housing and immigration. Its public repository provides hard/smoke splits and links the full dataset on Hugging Face. This is a free, inspectable legal-reasoning artifact, but its domains are civilian and its performance cannot be reported as an IHL benchmark result. The README records a **26 May 2026 correction** to reference programs with flawed legal reasoning, trivially true logic or hardcoded outputs. Any analysis should pin the corrected dataset/version and distinguish initial-paper scores from later artifacts. No paid inference or credentials are required merely to inspect/download the data. [Paper](https://arxiv.org/abs/2604.04443), [public repository](https://github.com/guangyaodou/DeonticBench)

**Next evidence:** primary OT award/modification data for USC, BBN and SRI; exact subaward identifiers; phase-2 go/no-go decisions; APL statement of work; government evaluation metrics; outputs involving actual ROE versus civilian legal examples. One paper acknowledging a broad award does not make all of its subject matter IHL research.

## 4. Civilian-harm funding adjacent to the legal-AI projects

These are distinct from the above autonomy research and do not by themselves prove a CP CoE successor.

| Funder / awarding route → recipient | Award / project | Obligated / potential | Recorded period |
|---|---|---:|---|
| CDAO / ONR → CNA | N0001424FT171 under N0001422D7001; Civilian Harm and Responsible AI; project 0007.5957.F580.01 | $500,000 / $550,000 | 1 Jul 2024–31 Oct 2025 |
| DSCA / ONR → CNA | N0001423FT077 under N0001422D7001; formative evaluation of civilian-harm mitigation in security cooperation; project 0007.5806.F218.00 | $518,000 / $518,000 | 1 Jun 2023–31 Dec 2024 |
| DSCA / WHS → HII Mission Technologies | HQ003423F0437 under HQ003423D0016; civilian-harm curriculum development | $40,609.49 / $40,609.49 | 1 Sep 2023–29 Feb 2024 |

Primary sources: [CDAO/CNA task](https://api.usaspending.gov/api/v2/awards/CONT_AWD_N0001424FT171_9700_N0001422D7001_9700/), [DSCA/CNA task](https://api.usaspending.gov/api/v2/awards/CONT_AWD_N0001423FT077_9700_N0001422D7001_9700/), [DSCA/HII task](https://api.usaspending.gov/api/v2/awards/CONT_AWD_HQ003423F0437_9700_HQ003423D0016_9700/).

The especially useful next join is CNA publication metadata and acknowledgments containing the **project numbers**, then author histories and any successor task orders. Awarding agency and funding customer differ here: describing all three as “Navy projects” would obscure CDAO and DSCA sponsorship.

## 5. Existing coverage, claim boundaries and reproducibility

- This is **not a novelty claim**. West Point public affairs documented TEELAWS; companies and universities announced ASIMOV teams; trade media repeated them. Sian Troath's **“The Intellectual Inheritance of Machine Learning and the Ethics of Algorithmic War”** discusses ASIMOV and CODORD and cites the public announcements. The contribution here is connecting those sources to primary obligations and subaward records. [Article](https://doi.org/10.1017/S0892679426100434)
- **Direct legal/ethical modeling:** CETLAWS and training successor TEELAWS. **Evaluation/assurance:** ASIMOV. **General legal-rule reasoning with proposed military applications:** CODORD. **Civilian-harm institutional research/training:** CNA/HII tasks. These categories overlap, but must not be collapsed into “deployed IHL targeting AI.”
- **Money discipline:** obligations are commitments, not cash outlays; potential values include unexercised options; university totals can include anticipated phases; program budgets cover a different scope; subawards are inside prime awards. None is an interchangeable measure of IHL-only expenditure.
- **Time discipline:** USAspending documents a **90-day delay for DoD procurement data**. Retrieval date, last-modified date, performance start/end, original action date and fiscal year are separate. No post-July 2026 record in an October snapshot is not evidence of no activity. [Official data guide](https://www.usaspending.gov/data/about-the-data-download.pdf)
- **Identifier discipline:** use normalized PIIDs and generated unique award IDs, keeping parent PIIDs for task orders. Do not join by title alone. The ASIMOV portfolio is partly hidden behind generic descriptions such as “Autonomy Rules” and “Architecture Ethical Framework.” Keyword-only search misses those awards.
- **Scope of search:** exact-award primary retrieval plus bounded 2020–16 Oct 2026 USAspending keyword searches, up to 100 records per term, for law of armed conflict, laws of war, ethical autonomy fragment, deontic, civilian harm, ethical trust, and predictive psychological; each returned no next page. Empty results do not establish absence because descriptions, OT coverage and search indexing vary. CODORD OT IDs returned 404 in the standard award endpoint; no program-wide financial total is inferred.
- **Evidence saved:** 14 primary award snapshots, 16 reported subaward rows, transaction responses for the original nine awards, search responses and a retrieval manifest. JSON is preserved with whitespace normalized; manifest timestamps are retrieval-completion file timestamps. CSVs retain last-modified dates and direct API URLs. The USAspending graphical award pages could not be rendered by the web tool, while the primary API responded successfully; use the API/raw record for verification.

### Deliverables

- [primary award ledger](ihl_prime_awards.csv): normalized primary award ledger, financing fields, agency offices, dates, IDs and source URLs.
- [reported subaward ledger](ihl_reported_subawards.csv): original reported subaward rows, preserving repeated subcontract numbers.
- [evidence directory](evidence/): primary API JSON and [retrieval manifest](evidence/retrieval_manifest.json).

The research involved no outreach, paid services, credential creation or procurement actions. Public-source records and the reports are published here under the investigation materials request.
