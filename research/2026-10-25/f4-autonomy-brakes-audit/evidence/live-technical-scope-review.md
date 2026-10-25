# Scope review of all 58 matched SBIR descriptions

**All 58 supplied records were read and individually adjudicated; 58 distinct PIIDs have a disposition in [the CSV](live-technical-scope-review.csv).** This is technical-scope review of the matched subset, not an independently verified census of the 44,584-row SBIR source or a claim to have substantively reviewed every award in the main live-financial queue. Two records contain only keyword strings, so only 56 permit narrative mechanism review. Financial retrieval counts and technical-scope counts must remain separate.

The source is the investigator-provided `f4-live-technical-matches.json`, SHA-256 `b32a46afacd985161328794350f398450a7f318351662213e0bd17cf16e3a9b1`. All entries point to `sbir_current.jsonl.gz`, snapshot SHA-256 `05af2f39171d08aa7ab4a071549e663e159f41d2092f7bda8428cd68b22b3cfe`. The CSV preserves each provided physical-row locator, row hash and URL. Those supplied row hashes are retained as provenance, not claimed as recomputed against original archive bytes by this reviewer. The public source URL in this input is the general SBIR awards page; no unverified specific deep links were fabricated.

**Final entity QA:** [The 58-row identity audit](../audit/technical-58-identity-linkage-audit.md) confirms 57 source UEIs against complete archived financial recipient sets and cached live prime-recipient UEIs. SP470124P0068 has an explicit UEI conflict; its technical disposition applies only to the SBIR lead and must not classify the financial award. The CSV retains that conflict separately.

## Results and counting boundaries

| Primary disposition | Records | Interpretation |
|---|---:|---|
| A | 4 | Normative training/modeling or civilian-harm contextual decision-support research; not four active deployed safeguards. |
| C | 44 | Broad technical/capability candidates. Only 21 describe a core assurance mechanism; the other 23 are adjacent, classification, resilience, cyber or underspecified capability work. Do not label all 44 as autonomous-weapons assurance programs. |
| Excluded | 8 | Supply-chain/manufacturing/hardware/environmental work whose described mechanisms do not fit autonomous-weapons brakes. |
| Unknown | 2 | Keyword-only descriptions; insufficient mechanism evidence. |
| Total | 58 | No input row silently omitted; no dollars added. |

The content flag is a different axis from primary category: 12 `Yes`, 44 `No`, two `unknown`. **`No` means no explicit normative/ROE function described in the supplied abstract; it does not assert the actual award lacks one.** `Yes` includes policy alignment, cyber ROE, harm-benefit claims, vessel-class separation and even wildlife law; these are distinguished in `content_scope` and must not all be counted as weapons LOAC testing. Secondary tags preserve overlaps without duplicating awards or dollars.

## Material corrections and counterexamples

- **W5170124C0035, Explainable AI—The Art of Visualizing Trust:** the abstract explicitly addresses civilian infrastructure collateral harm and downstream food-supply consequences, with peacekeeping-oriented data/context. A-enabling decision support is justified. The exact AI mechanism, autonomy/weapon integration and test protocol remain underspecified; title-based dismissal as ordinary explainability would miss the stated normative aim.
- **W5170125C0052, TEELAWS:** adapts prior CETLAWS Bayesian modeling to ethical command-responsibility training and collateral-risk feedback. The abstract expressly distinguishes this training application from making engagement decisions. Planned West Point insertion is not a completed deployment result.
- **FA864922P1015 and FA864921P1296:** CETLAWS Phase II and its historical Phase I predecessor are substantive ethical-trust research. The Phase II abstract claims an earlier simulated ethical shoot/no-shoot demonstration; Phase I proposes literature/feasibility work and later prototype validation. These awards are separate phases of a lineage, not proof of two independent active 2026 programs.
- **N0002425CS104, N6833525C0110, N6833524C0075 and N6833524C0076:** explicitly address combatant/noncombatant or combatant/commercial vessel classification. C primary with A contribution secondary preserves that relation to distinction. Template recognition/classification is not by itself legal status reasoning or a demonstrated lawful-attack constraint. N6833524C0074’s abstract lacks the same explicit civilian distinction wording; do not import another performer’s abstract into it.
- **FA864925P0010:** the battle-damage-assessment abstract claims collateral reduction, while describing edge-ML optimization and secure runtimes. Retain the benefit claim and request a harm-evaluation protocol; do not count it as an established normative test.
- **FA945125PX001, GUARDIAN:** cites RAI and DoDD 3000.09, but the actual proposed tests concern model explainability, neural-collapse behavior and uncertainty. C primary/D secondary, with no demonstrated LOAC test established by that citation.
- **FA864924P0465:** despite “Ethics” in its title, the full abstract describes nLoop aircraft edge-case safety-of-flight evaluation. C is supported; an ethical/LOAC function cannot be established from the title.
- **W15QKN22P0057:** explicitly proposes evaluating ML behavior within operational/mission bounds in lethal armament systems. This is a concrete assurance purpose, more specific than an unconnected generic AI tool. The abstract does not identify legal bounds, a positive-authorization interface, or an enforced operational lock, so C primary and possible B contribution are appropriate.
- **N6833524C0261 and N6833523C0505, TOOL-VAN:** verification selection, specification-based retraining and prototype integration are actual described assurance mechanisms. The supplied specifications are generic; no particular normative constraint is identified. Two phases should not become two independent programs.
- **N6833524C0442:** autonomous cyber investigation claims compliance with cybersecurity rules of engagement. Preserve that constraint but keep its cyber scope explicit; do not describe it as kinetic autonomous-weapons LOAC validation.
- **FA864922P0787:** proposed physical geofence/collision-avoidance tests are a meaningful technical boundary. They do not establish a bounded lethal-engagement envelope, and proposed flight-test objectives do not prove successful execution.
- **N6833521C0549 and N6833521C0510:** only generic keywords survive in these supplied descriptions. Their parent-topic ROE requirements cannot be silently transferred into award-specific technical findings or achieved safeguards.

Excluded rows remain in the register for auditability: SP470124P0068, HDTRA124P0013, W5170124C0063, SP470123C0057, SP470122P0039, SP470122P0038, W31P4Q20C0021 and FA930219P1008. The last concerns legally motivated nonlethal wildlife management, which illustrates why even explicit legal/nonlethal vocabulary is not sufficient for the weapons taxonomy.

## Review limits

Abstracts often describe proposals and future demonstrations. The CSV deliberately labels mechanisms as proposed where appropriate and attributes earlier success claims to the abstract. It is not a full statement-of-work review, an independent replication, an assessment of current award performance, or proof a capability has been fielded. This review adds no contract, program-count or category-dollar total. Source-row money and options were not used to infer safeguard budgets.

All 58 supplied keys were checked for one-to-one coverage and uniqueness in the CSV, and dispositions sum to 58. The input remained private; only short authored paraphrases, source locators and hashes appear here. No paid calls, credentials or outreach were used.

## Final primary-source crosswalk and ANSR scope check

Eight known specific SBIR award links were added in `technical_primary_url`, while retaining the original generic archive URL in both `source_url` and `archive_source_url`. URL provenance is explicit in `technical_url_basis`. The Arete link [218265](https://www.sbir.gov/awards/218265) was checked against **N0002425CS104**, not incorrectly assigned to its older Phase I. Pages [208942](https://www.sbir.gov/awards/208942) and [209955](https://www.sbir.gov/awards/209955) support the nLoop flight-safety and Black Box Simplex/reachability mechanisms described above. [EpochGeo 209584](https://www.sbir.gov/awards/209584) failed web-open but subsequent direct HTTP retrieval succeeded; the recorded scope finding remains based on the hashed archived abstract.

The [CMU SymAnt thesis](https://www.ri.cmu.edu/app/uploads/2025/06/Symant.pdf), dated 25 October 2025 on its cover, explicitly acknowledges ANSR grant **FA8750-23-2-1015**, plus ARL grants W911QX24F0049 and W911NF2320007, on printed page ix / PDF page 9. Its technical abstract evaluates prediction of human actions from short videos, including kitchen datasets; this is a concrete neuro-symbolic research output, not demonstrated LOAC testing. The URL’s `/2025/06/` upload path does not replace the document’s stated date. No award dollars were inferred or added.

The UCSC projects page `https://hybrid.soe.ucsc.edu/projects` timed out through web-open, then returned HTTP503 on direct retrieval. This reviewer could not verify its exact FA95501910169 funding linkage or scope from the page; main-audit indexed evidence remains separately identified.

Direct retrieval receipts, 25 October 2026:

| Source | HTTP | Bytes | SHA-256 |
|---|---:|---:|---|
| CMU SymAnt PDF | 200 | 1552078 | 5cab42b3262158145caf3daf1a3b8eaaf8627f6a60f9f73b9b757a8980559f99 |
| SBIR 208942 | 200 | 37097 | 21b6ccfd8f6859bee11534817f6ea9052ed5962ecbc2f9c1d3d5806e1377057d |
| SBIR 209955 | 200 | 38414 | 93270056c8ff357ce29ace6d4a900696d053d272c22d6c47186bd5e50aa240eb |
| SBIR 209584 | 200 | 36251 | 80c7cb73f249644260fc16e6a5f5f28817507438dc415cbe04f4c991775f321a |
| SBIR 218265 | 200 | 35688 | 8ea69f6929a9952edcd162ef16dd67393b0828fd262db5bbf3bda42bac3a6e92 |
| UCSC projects page | 503 | — | Failed; no source-body hash claimed |

## Entity-attribution update

The58 rows review SBIR source content. A separate full-history recipient check supports57 associations by source/archive/cached-live prime UEI; SP470124P0068 has a conflicting source UEI and is retained as an unlinked SBIR lead. Its financial award is excluded from selected safeguards cases on its own primary material-obsolescence description, not by importing the conflicting SBIR abstract. Source-content hashes alone do not establish recipient identity. See [the identity audit](../audit/technical-58-identity-linkage-audit.md) and [281 quarantined source appearances](sbir-entity-linkage-conflicts.csv). Technical source-category counts remain descriptions of those source abstracts, not58 independently confirmed financial scope transfers.
