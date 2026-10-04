# Consequential expansion 02 — 4 October 2026

This batch develops **four proposed new investigative formulations and one refinement**. The most promising is a precise procurement calculation: did changed quantities eliminate the winning bid’s original price advantage over a compliant rival? Others examine an explicit zero-structure resettlement inventory, a drug advertisement’s authorized indication, and potentially incompatible exclusive patent grants. These are conditional tests, not findings.

There are **24 mapped substantive predicates: 16 screened and eight still unexamined**. Five screened predicates became cards; eleven were deferred, rejected or recognized as existing specializations. The map names 54 sources, but only 40 appear in screened predicates. All 344 source descriptions remain in the source manifest. The other 290 sources are not newly examined simply because they appear in that manifest. The earlier 344-source review remains a baseline, not proof that every meaningful combination is exhausted.

The previous expansion was independently reviewed and corrected to **12 new formulations and four refinements**, leaving **44 cumulative non-refinement detailed cards** before this batch. X01 refines H04; X10 specializes E02. With the four current proposals the provisional total is **48**, after independent novelty review and repairs. The earlier longlist remains **1,715 active provisional source-pair rows and 15 quarantines**. Cards, mechanisms and implementation rows are different counting units: do not add them together or describe them as thousands of independent discoveries.

## Start here

`cards.csv` and `cards.jsonl` contain the five full recipes, required original records and source-level SYS/AP provenance. `predicate-coverage.csv` is the deliberate coverage map, including exclusions and the eight outstanding questions. `source-coverage.csv` tells exactly which of the 344 sources this pass touched and distinguishes queued ideas from screened ones. `sources.jsonl` retains original join-field descriptions and hashes.

The first cheap procurement check is to find one priced bid schedule and an implementation document referencing the exact same contract. A World Bank project ID is not sufficient: one project can contain many contracts. Without rival unit prices and equivalent certified quantities, stop. The provided arithmetic helper rejects missing items, mismatched units/currencies and ineligible comparators. It cannot establish that the rival could have performed the revised work or that the winner manipulated quantities.

## Evidence and practical limits

Thirteen official-documentation entries were recorded. One public SEC exhibit was opened to inspect licence definitions and carve-outs; it was not matched to a purportedly conflicting agreement, and nothing adverse is asserted about its parties. **Zero matched record chains, zero confirmed end-to-end feasible routes and zero positive findings** were produced. The patent API’s credential requirement remains unresolved; no account was created. Paris MoU’s displayed reuse/storage restriction was recorded without storing its vessel rows or attempting extraction.

Drug-product guidance does not establish that a particular ad is unlawful. Image evidence cannot establish occupancy, displacement, compensation eligibility or a missing payment. Two exclusive licences can coexist through master/sublicence relationships, differing fields, territories, rights or dates. These ordinary explanations are mandatory gates in the cards.

## Ranking and validation

Consequence 1–5 estimates public-interest significance if a predicate proves true. Testability 1–5 measures evidence-route maturity; current cards are at most 2 (documentation/components, not demonstrated chains). Join route 1–3 denotes provisional person bridges, multi-field conditional routes or precise candidate identifiers; none certifies an actual match. Cost tier 1–4 estimates rising document/access/identity effort, with no measured cash/time promise. Separate ranks are provided. Composite = `10 × consequence + 3 × testability + 2 × join route − 2 × cost tier`; weights are editorial judgments.

**Thirteen production-artifact, eight synthetic arithmetic and three synthetic temporal checks pass.** The latter verify a fictional bid calculation and rejection gates, not any real procurement. Artifact checks verify counts, source provenance, safeguards and ranking; they do not certify semantic novelty, legal applicability or wrongdoing. Independent review has checked the four additions and identified two edge cases: prior images do not establish presence at the claimed date, and a tied-lowest bid becoming dearer is not a strict price reversal. Both are corrected in current outputs; the original ZIP remains preserved. Independent review accepts the four formulations after these repairs; the cumulative non-refinement count is 48.

## Audit and reproduction

The prior correction commit is `5a53612c2032e0801504528bee8e18b6d1a476dd`. The downloadable bundle contains both this expansion and the corrected first expansion; its original ZIP remains preserved in Git history and its original folder. Corrections include dated LDA evidence (the House-linked PDF revised February 28, 2025), separate ASIC asset/liability gates, explicit actual-security retrieval dependencies, no assumed FARA creative identifier, and X14’s relationship to the earlier same-document comparison.

Run `python code/design.py`, `python code/evidence.py`, `python code/validate.py`, then `python code/package.py` from this folder. No command makes network or paid API calls. Source selection, novelty judgments and card text are model-authored and visible in the scripts; code exports, ranks, checks and performs the limited arithmetic. Official pages were inspected separately and cited in `evidence/documentation.jsonl`; a single-document observation and non-attempted access routes are logged separately. The generation instruction was to seek previously unexamined consequential predicates, favor exact document identities and inexpensive falsification, compare against prior work, preserve refinements without counting them new, and leave explicit unresolved coverage.

Weekly ChatGPT allowance and model-token telemetry were unavailable. Paid external API calls: **zero**. No bulk investigation, outreach, new account, paid download or active probing occurred.

## Remaining coverage

Eight priorities remain explicitly unexamined, not rejected: permitted-donor trading conditions; insurance representations against engineering findings; charity political-benefit transactions; land-transfer consent clauses; unit-outage market disclosures; borrower debt perimeter; claimant compensation completeness; and component-level maintenance certifications. Each map row names the sources, prior mechanism to compare, original records needed and reason it is not yet executable. Some will likely be refinements. No exhaustion claim is made.

## Detailed cards

### Z01 — Quantity changes that reverse the competitive price ranking

proposed_new; priority rank 1. Consequence 5/5; testability 2/5; join route 3/3; cost tier 3/4.

**If:** IF a public works procurement has at least two compliant priced bids on the same item schedule, and the eventual certified quantities differ from the evaluation quantities.

**Then:** THEN price the actually delivered common basket at each eligible bidder’s contemporaneous submitted bid unit rates, comparing that ranking with the original price ranking (separate from the award decision) and examining how quantities changed.

**Basis:** This is a transparent counterfactual cost comparison, not a finding of rigging or proof the rival would have performed the work. A sharp reversal concentrated in items the winner priced unusually high merits examining the change rationale and what was foreseeable at award.

**Exact join:** OCDS ocid + buyer identifier + contract/lot number → exact procurement reference in the World Bank project documents → bid ID + item code + unit + currency + pricing date → certified item quantities. World Bank project ID alone cannot match a contract. Item numbers local to different schedules are not automatically equivalent.

**Scope:** One contract/lot and equivalent scope, quality, delivery obligations and tax basis; compare the version used at award with actual certified work and every approved amendment; separate gates for quantity-dependent rates, fixed charges, changed specifications, rate adjustments and rival performance. Do not transfer US FAR rules to a non-US procurement.

**Ordinary explanations and disqualifiers:** Rival disqualified or technically noncompliant; Legitimate unforeseeable scope change; New item or revised specification lacking an equivalent rate; Quantity-dependent discount or rate-adjustment clause; Inflation, exchange, taxes or mobilization priced differently; Nonprice evaluation justified the award; Rival lacked capacity for revised work

**Required original records:** Original solicitation and bill of quantities; All compared signed bid schedules and evaluation eligibility; Signed contract and rate-adjustment provisions; Approved change orders and reasons; Certified final item quantities, separating paid from merely authorized quantities; Exact project-to-contract reference

**Next cheapest check:** First open a bid tabulation and one implementation document for the same contract number. Stop the arithmetic if rival unit rates, item equivalence or actual quantities are absent; total award values cannot replace them.

**Novelty:** E03 measures common ownership and E07 funded delivery; this tests how the evaluation quantity basket interacts with competing unit-rate schedules. A changed total alone is not a new test.

**Access evidence:** OCDS stage and bid-extension documentation supports candidate structure, not publisher completeness. No real bid/quantity chain retrieved; World Bank-priced schedules may be undisclosed.

**Method:** For every eligible bidder b, compute original=sum(q0_i*p_bi) and counterfactual=sum(q1_i*p_bi) only on a fully equivalent complete basket. Report adjustments, excluded items and sensitivity; never extrapolate missing prices. A strict reversal requires the winner to have been cheaper than the same comparator originally and dearer later; initial tie-to-loss is reported separately. A reversal is a question about procurement design/change control, not intent.

**Provenance:** SYS-0052 Open Contracting Data Registry (references/rabbit/originals/Rabbit2(1).txt:3010; APs AP-0053); SYS-0145 World Bank Documents & Reports API (references/rabbit/originals/Rabbit2(1).txt:9143; APs AP-0146); SYS-0058 World Bank Projects & Operations (references/rabbit/originals/Rabbit2(1).txt:4148; APs AP-0059)

**Evidence references:** D01, D02, D03 in evidence/documentation.jsonl.

### Z03 — A specific drug advertisement versus the product’s authorized indication

proposed_new; priority rank 2. Consequence 5/5; testability 2/5; join route 2/3; cost tier 2/4.

**If:** IF a preserved advertisement directed at Canada makes an affirmative therapeutic indication/population claim for an exactly identified drug product, and the contemporaneous authoritative monograph limits that product to a different indication or explicitly excludes that population.

**Then:** THEN compare the complete creative and landing page with the authorization in force, establishing whether it is promotional advertising, the intended audience, the responsible advertiser and the precise product.

**Basis:** Health Canada identifies promotion outside authorized indications as a concern. An ingredient match, an educational discussion or an off-label clinical prescription does not by itself establish improper advertising; case-specific legal assessment remains necessary.

**Exact join:** Meta ad ID → preserved exact creative and landing-page URL/date → displayed DIN or independently verified brand + strength + dosage form + company → DPD drug_code/DIN → monograph/version/effective date. Ingredient alone is not a product key. Wayback timestamp is capture time, not proof of first publication or audience.

**Scope:** Canadian-directed communication, specific audience and actual running dates, with authorization then in force. General commercial ad historical retention and geographic coverage must be checked; no absence inference from an archive search.

**Ordinary explanations and disqualifiers:** Disease-awareness message without product promotion; Non-Canadian audience or different national product; Different formulation/strength; Authorization changed before the ad; Full context qualifies a cropped statement; Scientific exchange not advertising; Unaffiliated impersonation or reseller attribution; Off-label prescribing confused with promotion

**Required original records:** Complete ad, disclosure and landing page; Audience/geography and run-date evidence; Exact product bridge including DIN where possible; Contemporaneous approved monograph and authorization changes; Advertiser responsibility and promotional-context evidence

**Next cheapest check:** Select a creative with a precise product and indication, then verify DIN and monograph. Stop if only ingredient similarity or an undated screenshot is available.

**Novelty:** H05 compares marketed products to trial evidence; X06 traces who financed an ad. This compares an actual promotional claim with the exact product’s authorized scope. It is not a broad medical efficacy judgment.

**Access evidence:** DPD API documentation confirms DIN and product fields; official advertising guidance read. No ad or monograph paired; Meta historical access remains unverified.

**Method:** Transcribe the full relevant claim with context; separately record product, indication, population, audience and dates. Build a side-by-side comparison to the applicable monograph text, resolving each mismatch and amendment before escalation.

**Provenance:** SYS-0278 Health Canada Drug Product Database API and bulk data (references/rabbit/originals/Rabbit3.txt:598; APs AP-0279, AP-0466); SYS-0143 Meta Ad Library (references/rabbit/originals/Rabbit2(1).txt:9059; APs AP-0144); SYS-0133 Internet Archive Wayback Machine APIs (references/rabbit/originals/Rabbit2(1).txt:8639; APs AP-0134)

**Evidence references:** D05, D06, D07 in evidence/documentation.jsonl.

### Z02 — An explicit zero-structure resettlement inventory contradicted by dated imagery

proposed_new; priority rank 3. Consequence 5/5; testability 1/5; join route 2/3; cost tier 3/4.

**If:** IF an operative project inventory expressly states that no physical structures existed within a precisely mapped acquisition or inundation area at a specified inventory observation date or explicitly defined interval.

**Then:** THEN establish independently corroborated physical structures present at the exact claimed date or during the explicitly claimed zero-structure interval, wholly within that same area, reconcile the inventory definition, and inspect later plan revisions.

**Basis:** A verified omitted physical asset can undermine the stated impact assessment. Imagery of a structure cannot establish occupancy, the number displaced, ownership, compensation eligibility or an unpaid claim. The test concerns a specific physical inventory statement, not demographic estimation.

**Exact join:** World Bank project ID → exact document/version/page and project component → inventory polygon and claimed observation date/interval (distinct from legal eligibility cutoff) → Landsat scene/product ID, acquisition timestamp, georegistration and visible object. JRC water history can contextualize later inundation but cannot substitute for the operative acquisition polygon.

**Scope:** Project-specific inventory observation date/interval, separately recorded legal eligibility cutoff, and actual acquisition boundary, with image cloud/shadow/resolution sufficient to identify the object. Applicable safeguard framework and cutoff must be established for any later compliance interpretation.

**Ordinary explanations and disqualifiers:** Inventory excludes the particular structure class; Mapped component or boundary changed; Object is rock, temporary equipment or model artifact; Earlier structure demolished/relocated/removed before the claimed date; Image timing does not establish presence at the claimed date; Already inventoried in an annex or amended plan; Georegistration puts the object outside the area; Structure existed but no resident or compensation entitlement follows

**Required original records:** Original signed/operative inventory and all spatial annexes; Inventory observation date/interval, separate eligibility cutoff and definitions; Contemporaneous image metadata and pixels; Independent corroboration of structure interpretation; Amendments and actual project boundary; Separate claimant/occupancy/compensation records before making those claims

**Next cheapest check:** Read the exact inventory sentence and map before downloading imagery. If Landsat cannot resolve the alleged structure, defer or identify a lawful higher-resolution source explicitly; do not treat a detection model as ground truth.

**Novelty:** C02 estimates exposure around a hazard; R11 follows project/document milestones. This asks whether a particular zero-asset inventory is falsified by a physical counterexample at the claimed date/interval. It is not an additional population-overlay pairing.

**Access evidence:** World Bank framework documentation establishes inventory context; no project inventory or usable image pair sampled. The earlier project-document component sample does not confirm these fields for this predicate.

**Method:** Record the exact claim, polygon and cutoff; require clear evidence of presence at the claimed date/interval; an earlier image alone fails, and any inference of persistence needs independent temporal corroboration. Report only the minimum verified physical counterexamples, positional uncertainty and any ambiguity; do not multiply structures by a population ratio.

**Provenance:** SYS-0145 World Bank Documents & Reports API (references/rabbit/originals/Rabbit2(1).txt:9143; APs AP-0146); SYS-0103 USGS Landsat data (references/rabbit/originals/Rabbit2(1).txt:6713; APs AP-0104); SYS-0058 World Bank Projects & Operations (references/rabbit/originals/Rabbit2(1).txt:4148; APs AP-0059); SYS-0115 JRC Global Surface Water (references/rabbit/originals/Rabbit2(1).txt:7375; APs AP-0116)

**Evidence references:** D04 in evidence/documentation.jsonl.

### REF-DISC01 — A lobbyist’s explicit conviction declaration versus the actual judgment

refinement; priority rank 4. Consequence 4/5; testability 2/5; join route 1/3; cost tier 2/4.

**If:** IF a registration expressly denies a covered conviction for a listed lobbyist, while an independently verified identity bridge leads to a final federal/state judgment involving a covered offense.

**Then:** THEN compare the actual declaration and amendments with the judgment, applicable filing-date rule and conviction disposition; do not treat a complaint, charge or same name as a conviction.

**Basis:** The 2024 published US Code includes a specified conviction disclosure in 2 USC 1603(b)(7), and official guidance revised February 2025 describes it. Those sources do not resolve a specific person’s identity, offense coverage, vacatur or present filing applicability.

**Exact join:** LDA filing ID and listed lobbyist → independently corroborated person identity → court + docket + judgment document + convicted offense/statute + disposition date. Name-only joins remain provisional; CourtListener search completeness is not established.

**Scope:** Federal or state judgment and actual filing-date applicability; current rule changes, amended filings, vacatur and the distinction between person and employer all require review.

**Ordinary explanations and disqualifiers:** Different person; Only charges or dismissed case; Noncovered offense; Vacated or otherwise legally altered conviction; Employer convicted rather than lobbyist; Amended disclosure; Declaration field absent because not applicable rather than affirmative denial

**Required original records:** Original complete filing and amendments; Final judgment and subsequent disposition; Independent identity corroboration; Covered-offense legal analysis; Applicable statutory version

**Next cheapest check:** Check the exact form field and a known judgment’s disposition first. Stop before any publication if the identity bridge is only a matching name.

**Novelty:** An additional statutory application of the disclosure-consistency family exemplified by X04. Kept as a refinement, not added to new-mechanism totals.

**Access evidence:** Official statutory edition and dated guidance read; no named lobbyist or court record searched. Not a claim of comprehensive current-law verification.

**Method:** Keep identity and legal applicability as separate gates. Require an affirmative incompatible declaration; missing search hits cannot demonstrate disclosure failure.

**Provenance:** SYS-0117 US Senate Lobbying Disclosure data (references/rabbit/originals/Rabbit2(1).txt:7734; APs AP-0118); SYS-0129 CourtListener and RECAP (references/rabbit/originals/Rabbit2(1).txt:8250; APs AP-0130, AP-1323, AP-1324, AP-1325, AP-1326, AP-1327, AP-1328, AP-1329, AP-1330, AP-1331, AP-1332, AP-1333, AP-1334, AP-1335, AP-1336, AP-1337, AP-1338, AP-1339, AP-1340, AP-1341, AP-1342); SYS-0125 GovInfo API (references/rabbit/originals/Rabbit2(1).txt:8082; APs AP-0126)

**Evidence references:** D10, D11 in evidence/documentation.jsonl.

### Z04 — Apparently incompatible exclusive grants over the same patent right

proposed_new; priority rank 5. Consequence 4/5; testability 1/5; join route 3/3; cost tier 3/4.

**If:** IF two executed, concurrently operative public agreements purport to grant independent parties exclusivity over the same specific patent right, field of use and territory.

**Then:** THEN reconstruct the grant chain, scope, amendments and conditions to establish whether both exclusive grants can coexist, rather than inferring a conflict from the word exclusive or a shared patent family.

**Basis:** A genuine unresolved incompatibility can materially affect investors or a critical technology’s commercialization. Most apparent overlaps can be lawful sublicences, retained fields, territorial divisions or conditional transactions; contractual interpretation is case-specific.

**Exact join:** EDGAR CIK/accession/exhibit → executed agreement/schedule → exact application/publication/grant number with country and kind code → patent-family/status crosswalk if needed → legal grantor, grantee, field, territory, operative interval and sublicense rights. Patent family membership is not identity of enforceable rights.

**Scope:** Rights at the effective/closing dates, not SEC filing date. Same legal right and substantive use/territory; distinguish applications, national grants, continuation claims and ownership from licences.

**Ordinary explanations and disqualifiers:** Lawful master licence and sublicense chain; Carved-out field or territory; Successive term or terminated agreement; Closing condition not satisfied; Retained research rights; Different national/continuation claims; Amended or consented grant; Material schedule redacted

**Required original records:** Both executed agreements and patent schedules; All amendments/terminations and closing evidence; Grant-chain and sublicense permissions; Exact patent identifiers and rights scope; Unredacted necessary field/territory terms

**Next cheapest check:** Read definitions of field, territory and sublicense authority first. One reviewed public exhibit explicitly carves out fields and territories, illustrating why keyword overlap must be rejected. Do not seek a second party until the first right is precisely defined.

**Novelty:** X09 tests an issuer title assertion against a registry; this tests coexistence of two operative contractual grants. H03 maps research to patents. EPO is identity/scope support; two SEC exhibits can suffice without inventing a separate cross-source allegation.

**Access evidence:** One SEC exhibit was opened to inspect fields and exceptions, not investigate its parties. No conflicting agreement pair found or sought. EPO OPS requires credentials; no registration or API call made. Missing schedules make a candidate non-executable.

**Method:** Represent each grant as (right, grant chain, field, territory, effective interval, conditions). Require verified nonempty overlap in all dimensions and an actual incompatibility after permissions and carve-outs; a shared family or simultaneous exclusive labels fails this test.

**Provenance:** SYS-0005 SEC EDGAR (references/rabbit/originals/Rabbit2(1).txt:588; APs AP-0006, AP-1148, AP-1149, AP-1150, AP-1151, AP-1152, AP-1153, AP-1154, AP-1155, AP-1156, AP-1157, AP-1158, AP-1159, AP-1160, AP-1161, AP-1162, AP-1163, AP-1164, AP-1165, AP-1166, AP-1167, AP-1168, AP-1169, AP-1170, AP-1171, AP-1172); SYS-0253 EPO Open Patent Services (references/rabbit/originals/Rabbit2(1).txt:16165; APs AP-0254, AP-0441)

**Evidence references:** D08, D09 in evidence/documentation.jsonl.
