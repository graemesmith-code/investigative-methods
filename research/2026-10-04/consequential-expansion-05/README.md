# Six-lens breadth checkpoint — 4 October 2026

This pass screened **24 concrete predicates across 48 source descriptions**, using six discovery lenses. It retains **two proposed new formulations** and **one refinement**. Seven ideas were rejected, four deferred, seven recognized as deferred refinements, and three recognized as repeats. The lenses did not automatically generate valid tests.

The most promising addition asks whether an important plant-performance claim survives a complete energy balance. It requires measured consumption and generation for the same physical boundary—not fuel purchases, electricity sales or a comparison with a typical plant. The other asks whether independent completed reimbursements for one eligible cost exceed the funding permitted by the operative instruments. Two funders reporting the same transfer, or an advance later reconciled, do not establish duplicate recovery.

Both remain **source-level proposals**. Documentation confirms useful definitions and possible access routes; no plant, invoice, payment, member or company records were matched. Neither is classified end-to-end feasible. A legislative conflict-declaration route is retained as a refinement, not counted as new merely because the decision maker is an MEP.

## What each lens yielded

| Lens | Decisions and useful exclusions |
|---|---|
| Conserved quantities | B01 energy-conversion proposal. Rainfall minus evapotranspiration cannot establish illegal pumping; arms and displacement datasets lack compatible complete stock/flow units. |
| Mutually exclusive statuses | No new card: shipping flags need historical legal instruments, multiple network origins can be authorized, radio licences can reuse frequencies, and mineral rights can cover different interests. |
| Prerequisites and sequence | No new card: advances can precede delivery; trial ethics and financing-condition sequences refine existing X07; DSCA notices do not define every arms-transfer authorization sequence. |
| Beneficial-interest conflicts | REF-MEP is a useful explicit-statement route. Procurement and charity relationships largely repeat E08; role names do not establish beneficial interests or incompatible employment. |
| Double claims | B02 constrained cost recovery is proposed new. Shared paper acknowledgements are not duplicate cost claims; carbon units and renewable attributes need exact serial/right evidence. |
| Operations versus representations | No new card: sunk-vessel, fuel-input, construction and species examples mostly specialize existing precise-assertion tests. Registry presence and remote nonvisibility are not operational facts. |

`candidate-screen.csv` gives a concrete predicate, named sources, semantic comparison, discriminating evidence and stopping condition for every branch. `source-coverage.csv` preserves all 344 descriptions and distinguishes the 48 used here from those without a concrete candidate in this batch. It does not claim that every pair among the 344 has been individually researched. Original SYS/AP identifiers, field descriptions, line provenance and block hashes remain in the manifest.

## Corrected cumulative counts

Independent review accepts **51 non-refinement formulations through expansion 04**. Q01 is now a refinement of the original S06 donor-eligibility/incorporation/refund predicate. Q02, Q03 and V01 were accepted as defensible new formulations, without claiming they are independent abstract mechanisms. With B01/B02 pending review the provisional count is **53**.

The prior **1,715 active provisional directional source-pair rows plus 15 quarantines** remain a different counting unit. The 5,000 target is not met and no source permutation, date parameter or rewording has been counted to inflate it.

This bundle also includes the reviewed repairs: Q02 distinguishes never-completed or misattributed transfers from completed contributions later refunded; Q03 join confidence is reduced to 2 until the legal-guarantor/reporting-perimeter crosswalk is documented. V01 requires one selected filing vintage, source hashes/row locators, reviewed canonical holding identity, aggregate/detail resolution and conservative exposure/denominator bounds. Its 26 checks include aliases for the same economic position, mixed revisions, aggregate rows and rounded marginal excesses. Those are evidence requirements, not claims that software can authenticate a caller's manifest.

## Documentation and validation

Eight documentation observations are recorded. EIA definitions distinguish consumption, generation and incoming electricity. OCDS/IATI transaction identifiers can help trace a payment path but do not guarantee invoice publication or independent flows. World Bank guidance is used for document anatomy; an actual financing instrument must establish the cost constraint. Both attempted European Parliament PDF opens returned unusable verification pages; the log preserves those failures. Search excerpts are not promoted to verified current legal applicability.

This batch passed **18 checks: eight artifact/provenance checks and ten synthetic arithmetic checks**. The synthetic helpers demonstrate conservative physical bounds and constrained-cost arithmetic; their gates require independently reviewed evidence. They do not discover identity matches or resolve the flow graph. A low balance or lack of an excess flag never establishes compliance.

Priority remains an editorial score: `10 × consequence + 3 × testability + 2 × join confidence − 2 × cost`, with separate consequence/testability ranks. Scores are not probabilities of wrongdoing. B01 is more testable than B02 because public physical-measure definitions are available, while B02's invoice/settlement chain is still an access dependency. Name-only routes remain provisional.

Run `python code/design.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py`. These local scripts perform no API calls. Source selection and semantic comparisons were authored in the existing model environment; exports, ranking, consistency checks and calculations are deterministic. The ZIP contains the corrected current expansions 01–05; earlier ZIPs and delivery receipts remain preserved separately in Git.

## Continuation boundaries

This is an incremental breadth checkpoint, not evidence that all further discovery is exhausted. The 24 examined candidates have explicit dispositions. Further work on them now has concrete dependencies: an exact plant boundary and issuer-to-plant bridge; a published cost-level financing/settlement chain; historical ship-registration instruments; or serial-level environmental-attribute records. Advancing those routes requires the indicated evidence rather than another paraphrase. New discovery can still examine other catalog predicates and documented supporting Rabbit sources. No public outreach, accounts, bulk execution or paid APIs were used.

Automatic weekly ChatGPT allowance and model-token telemetry are unavailable. The latest user report remains **88% at 18:50 UTC**. The earlier 99% to 88% change cannot be attributed solely to this work. Paid external API calls: **zero**.

## Detailed cards

### B01 — Material plant-performance claims versus a complete energy-conversion balance

proposed_new; priority 1; consequence 5/5, testability 2/5, join confidence 2/3, cost 2/4.

**If:** IF a material financing, subsidy or operating-performance claim identifies an exact fuel-fired plant and reporting interval, and comparable official generation and total consumed-energy records are available for its complete physical boundary.

**Then:** THEN test whether even a conservative lower bound on electrical energy produced exceeds a conservative upper bound on all energy inputs, after resolving revisions and boundary flows. An unresolved excess identifies incompatible evidence requiring correction or explanation, not automatically fraud.

**Basis:** Energy conservation supplies a physical bound, unlike a discretionary industry-efficiency benchmark. Net generation converted to energy cannot exceed all consumed inputs over a closed, reconciled system interval. Finite storage changes and every external energy contribution must be bounded. A ratio below the bound says nothing about honest reporting or economic efficiency.

**Join:** Issuer CIK/accession and exact plant passage → documented facility/operator/location crosswalk → EIA plant code, year/month, prime mover and fuel/source rows. Aggregate each physical input/output once; reconcile combined-cycle combustion and steam equipment so recovered internal heat is not new external input. A company name or regional series is not a plant match.

**Scope:** US EIA-covered plants with fuel-only generation and a verified boundary. Begin with a simple non-CHP plant; defer CHP, hybrid solar/wind, pumped/battery storage, nuclear, imported steam or waste heat unless every contribution and allocation is independently reconciled. Use consumed fuel, not purchases; use full total fuel input, not only fuel statistically allocated to electricity. Same period and corrected filing vintage.

**Ordinary explanations / disqualifiers:** Missing fuel/source or unit; Fuel purchases confused with consumption; Electricity receipts or sales confused with generation; Heat-content basis or unit conversion mismatch; Gross/net/direct-use differences; Rounding or uncertainty explains excess; Thermal or electrical stored-energy release; Internal recovered steam double-counted; Plant/prime-mover boundary mismatch; Revised or estimated data; Claim refers to contractual attributes rather than physical performance

**Required evidence:** Original material claim and its exact metric; Plant identity crosswalk; Complete generation and all energy-input records for matching boundary/period; Data definitions, heat-content basis and revision history; Evidence excluding or measuring imported energy and storage changes; Conservative output/input bounds and tolerance

**Next cheapest check:** Read the claim and plant technology first; reject an economic or certificate claim that makes no physical assertion. Inspect one plant-period schema and all source codes before calculating. Stop if complete input or boundary evidence is unavailable.

**Novelty:** R13 and C01 compare emissions with activity; N09 uses national production as an external upper bound. B01 is a complete physical conversion-balance test with materially different input evidence. One proposed formulation; different fuels, months and plants are implementations, not new tests.

**Access evidence:** Current EIA form instructions and public data documentation inspected. Field meanings and bulk publication are confirmed; no plant rows or issuer-to-plant crosswalk were acquired. Current instructions separate consumption, generation and incoming electricity. No end-to-end feasibility established.

**Provenance:** SYS-0255 US Energy Information Administration API (references/rabbit/originals/Rabbit2(1).txt:16283; AP-0256, AP-0443); SYS-0005 SEC EDGAR (references/rabbit/originals/Rabbit2(1).txt:588; AP-0006, AP-1148, AP-1149, AP-1150, AP-1151, AP-1152, AP-1153, AP-1154, AP-1155, AP-1156, AP-1157, AP-1158, AP-1159, AP-1160, AP-1161, AP-1162, AP-1163, AP-1164, AP-1165, AP-1166, AP-1167, AP-1168, AP-1169, AP-1170, AP-1171, AP-1172)

**Documentation IDs:** D01, D02, D03 in evidence/documentation.jsonl.

### B02 — The same eligible cost reimbursed beyond its permitted funding

proposed_new; priority 2; consequence 5/5, testability 1/5, join confidence 2/3, cost 3/4.

**If:** IF operative financing instruments permit reimbursement only up to a specified eligible cost/share, and original evidence attributes two or more independent completed reimbursements to the same uniquely identified cost item.

**Then:** THEN reconstruct each payment path, permitted sharing, credits and reversals and compare the conservative lower bound of distinct net reimbursements with the conservative upper bound of the permitted reimbursable cost. Retain an unresolved excess for source-document review.

**Basis:** This is an instrument-specific cost-recovery constraint. Two project commitments or two descriptions of one transfer are not two recoveries. A payable supplier invoice can legitimately be financed through several parties, and authorized cofinancing can split its cost. No universal prohibition across all grant or results-based funding is asserted.

**Join:** World Bank project ID → exact loan/credit ID and original financing/disbursement documents → expenditure schedule/audit and uniquely identified invoice/cost item (issuer, invoice number/date, line, amount/currency) → actual settled payment references and payer/payee chain. OCDS transaction source/URI and IATI activity/transaction references can trace mirrored or onward flows, but neither necessarily publishes invoice-level identity. A shared project ID is only discovery.

**Scope:** Exact instrument, category, funded share, eligible-cost period and accounting/currency basis. Exclude results-based or unrestricted funding unless its own terms impose this cost cap. Resolve advance liquidation, prefinancing reimbursement, retention, tax, exchange rates, partial credit notes and corrections. Use historical records current to each payment.

**Ordinary explanations / disqualifiers:** Same transfer mirrored by donor and recipient; Pass-through financing counted at each stage; Advance later liquidated rather than new money; Permitted cofinancing within cost/share; Invoice number reused by different vendors or years; Credit note/refund; Different cost lines or phases; Commitment mistaken for payment; Currency or tax basis differs; Results-based payment not cost reimbursement; Revised schedule republishes old expenditure

**Required evidence:** Operative cost/share cap in every relevant financing instrument; Original eligible cost and adjustments; Evidence linking each claimed recovery to exactly that cost; Independent settlement records or an authoritative audit establishing payment; Full transfer-chain and correction/refund evidence; Conservative compatible-currency bounds

**Next cheapest check:** Open a public project audit or expenditure schedule and establish whether it names the same cost and actual financing sources. If only project-level totals are published, defer before summing anything. No requests or full investigations are initiated.

**Novelty:** N01 is aid-report reconciliation, X02 payment-obligation reconciliation and Z01 bid-rate arithmetic. This tests multiple independent recoveries against one constrained underlying cost. It is one proposed new formulation, not one per funding pair. When the funding terms do not constrain cost recovery, reject.

**Access evidence:** World Bank disbursement guidance confirms several payment methods and supporting-document types; OCDS and IATI definitions supply possible flow links. Public availability of the needed original invoices, settlements and complete financing chain has not been established. Zero matched projects or cost items.

**Provenance:** SYS-0145 World Bank Documents & Reports API (references/rabbit/originals/Rabbit2(1).txt:9143; AP-0146); SYS-0059 World Bank Finances (references/rabbit/originals/Rabbit2(1).txt:4190; AP-0060); SYS-0052 Open Contracting Data Registry (references/rabbit/originals/Rabbit2(1).txt:3010; AP-0053); SYS-0057 IATI Datastore (references/rabbit/originals/Rabbit2(1).txt:3885; AP-0058, AP-1273, AP-1274, AP-1275, AP-1276, AP-1277, AP-1278, AP-1279, AP-1280, AP-1281, AP-1282, AP-1283, AP-1284, AP-1285, AP-1286, AP-1287, AP-1288, AP-1289, AP-1290, AP-1291, AP-1292)

**Documentation IDs:** D04, D05, D06 in evidence/documentation.jsonl.

### REF-MEP — A file-specific no-conflict declaration versus a verified private interest

refinement; priority 3; consequence 5/5, testability 1/5, join confidence 1/3, cost 3/4.

**If:** IF a member expressly declares no conflict for a specific parliamentary file and dated evidence establishes an actual private financial or organizational interest affected by that precise matter.

**Then:** THEN reconcile the exact member, file, declared scope, interest type and dates, plus any disclosure, authorization or resolution, before describing an unresolved inconsistency in the statement.

**Basis:** A hidden relevant private interest can affect public trust in a legislative decision. A broad sector interest, a disclosed role, or a register contact name alone does not establish a prohibited conflict. Permission to act despite a disclosed conflict is distinct from a false no-conflict statement.

**Join:** EP member ID and procedure/document ID → original signed file-specific declaration and actual role → dated company registration/role/ownership evidence. EU Transparency Register ID links an organization or client, not an individual beneficial owner. Resolve the person beyond name and distinguish employer, director, shareholder and contact roles.

**Scope:** Specific file and declaration/appointment interval. Use operative rules at that date; older codes differ. Not every private interest is a conflict and public asset declarations are not assumed available. No automatic recusal requirement is asserted.

**Ordinary explanations / disqualifiers:** Namesake; Role or ownership ended earlier; Only broad-class interest; Interest already within declared scope; No affirmative no-conflict assertion; Disclosed conflict with permitted participation; Register contact not beneficial owner; Different legal entity or legislative file

**Required evidence:** Exact original declaration and file; Member identity and role dates; Verified private interest and economic relevance to the file; Applicable dated definition and declaration scope; Other disclosures, amendments and any permission/resolution

**Next cheapest check:** Find the original file-specific statement before searching company names. If it is absent, do not infer a denial. Establish one documented member-to-entity bridge before broad ownership exploration.

**Novelty:** Refinement of H04 conflict disclosure and REF-REL explicit relationship flags. This provides an additional legislative implementation route without adding to the non-refinement total.

**Access evidence:** Official search-index text, including a dated 2024 rules excerpt, identifies declaration routes and limits. Both current and dated PDF opens returned unusable HTML pages. No actual member, declaration, company interest or case-specific rule matched; access failure preserved.

**Provenance:** SYS-0122 European Parliament Open Data Portal (references/rabbit/originals/Rabbit2(1).txt:7955; AP-0123); SYS-0119 EU Transparency Register (references/rabbit/originals/Rabbit2(1).txt:7818; AP-0120); SYS-0004 UK Companies House Public Data API (references/rabbit/originals/Rabbit2(1).txt:296; AP-0004, AP-0005, AP-0541, AP-1223, AP-1224, AP-1225, AP-1226, AP-1227, AP-1228, AP-1229, AP-1230, AP-1231, AP-1232, AP-1233, AP-1234, AP-1235, AP-1236, AP-1237, AP-1238, AP-1239, AP-1240, AP-1241, AP-1242); SYS-0010 France INPI National Business Register (references/rabbit/originals/Rabbit2(1).txt:1074; AP-0011)

**Documentation IDs:** D07, D08 in evidence/documentation.jsonl.
