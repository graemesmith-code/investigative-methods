# Independent quality check of the secondary EP queue

15 November 2026. This check is separate from the acquisition/screening agent's classifications. It tests a reproducible small sample, not total recall.

## Executed sample and reading depth

Input: archived 803-title-triage.csv recovered from Drive file 1p1XBvQzIb4M5m_iKY_CQA-UHHr1kgwUC. Filter screen_category == secondary-title-candidate (216 rows), retain original order, select random.Random(20261115).sample(rows,12). Sample metadata saved in sample12.json. All 12 Google Patents HTML pages downloaded successfully and claims-section text extracted. Selected claim language read for each; this is a claims-oriented check, NOT an exhaustive description/prosecution/legal-status review. German-original bilingual renderings used for EP4229352A1 and EP4508503A1; automated English translation is not an authoritative legal translation. No relevance score or precision/recall percentage inferred from this small, publication-level sample.

## Results

Every source below is https://patents.google.com/patent/[publication_id]/en . Captured HTML and extracted claims accompany this note.

| Publication | Classification in this check | Evidence and caution |
|---|---|---|
| EP4229352A1 | Weapon safeguard lead | Claims13–14 consider a restricted/blocking area and withhold a fire-control solution according to that parameter. A substantively relevant constraint buried under a general fire-guidance title. Likely counterpart of previously reviewed KMW US20230392899A1: family reconciliation required before calling it a new invention. AI use/deployment not established. |
| EP3569966B1 | Weapon control with material exception | Claim1 controls firing by preselected rules but expressly permits normal firearm operation if the electronic apparatus malfunctions or loses energy. This is not a universal fail-closed safety barrier; rules need examination, and safety purpose cannot be inferred merely from electronic gating. No operational-performance inference. |
| EP4644058A1 | Adjacent robotics safety | Claims1/13 monitor parameters, request slowdown/stop at one condition and disconnect actuator power at another; claim11 separates monitor from robot-internal control signals. Service robot, not proof of weapon use. |
| EP4196859B1 | Adjacent autonomy safety | Claim1 independent safety-rider system monitors vehicle limits and intervenes; claim3 permits disabling automated-driving control. Road/vehicle safety comparator, not weapon use. |
| EP4508503A1 | Adjacent autonomy validation | Claim1 cross-checks independent movement estimates with plausibility tests; claims9/25 reference functional-safety standards. Does not establish weapons applicability or ethical reasoning. |
| EP4239433A1 | Military autonomy/control comparator | Claims1/10 continue team coordination under communication denial using estimated teammate trajectories; claims3–9 concern detection/mission changes. Navigation/avoidance and mission continuity, not demonstrated civilian-protection or human-authorization guardrail. Do not equate 'communications denied' with automatic safe stop. |
| EP3726178B1 | Military coordination, no ethical guardrail established | Claims1/7/8 permit remote cross-vehicle control and human crew control of other weapons; claim9 regulates convoy distance. Not a universal human authorization constraint on firing. |
| EP4394307B1 | Training comparator | Claim1 includes user-actuated dummy-weapon release; claims9/10 confirmation signal. Training system, not evidence operational autonomous weapon permission rules. |
| EP4025866B1 | Weapon architecture, no ethical safeguard established | Claims chiefly concern UAV configuration; claim5 overrides camera orientation, NOT attack authorization. Claim7 remote/autonomous travel. Do not count generic 'override' as a firing veto. |
| EP4109033B1 | Accessory/control hardware | Claims concern grip and accessory switches; no AI weapon safeguard established in reviewed claims. |
| EP4745511A1 | Mechanical firearms safety | Claim14 concerns preventing an inadvertent strike during sudden movement. Mechanical firing-pin safety, not AI ethical guardrail. |
| EP3241107B1 | Logistics robotics | Claims concern warehouse order picking and robot-human positioning. No weapon or explicit ethical safeguard established in reviewed claims. |

## Method changes justified by this check

1. **Keep all 216 in the evidence ledger.** Title priority is scheduling only. Do not convert no keyword hit, no file, or a metadata stub into an exclusion.
2. **Use two independent axes:** (a) domain: weapon / military non-weapon / civilian autonomy / mechanical or unrelated; (b) mechanism: authorization, prohibition/inhibition, abort, constraint, fail-safe, monitoring/validation, ordinary precision, or no relevant mechanism established. This prevents ordinary robotics safety inflating the weapons count while retaining transferable ideas.
3. **Separate document sections:** record what the abstract says, what the description offers as an example, and what numbered independent/dependent claims actually require. Record alternatives, exceptions and timing. EP3569966B1 demonstrates fail-open exceptions; EP4025866B1 demonstrates an 'override' can apply only to a camera.
4. **Normalize translations and concept families, not just literal keywords:** restricted area/blocking parameter/Sperrgebiet/Sperrparameter; power isolation vs 'stop'; denied communications can mean continued autonomy, not restraint. Treat glossary additions found here as development data, not a held-out test.
5. **Record acquisition status separately from reading status:** HTTP success, content type, publication kind/date, claims-present, description-present, language, extraction success; then semantic reading depth and reviewer. Count original-language and translated versions once. Preserve and follow WO counterparts for EP stubs; never count them as read full texts.
6. **Family and version reconciliation before totals:** applications, grants and corrections are different documents, not independent inventions. Review changed grant claims when relying on application language. Preserve exact publication identifiers and original EPO URI.
7. **Independent validation after revised screening:** freeze this sample and the known positive patents as development examples. For a meaningful false-negative test, draw a new held-out sample from genuinely low-scored full texts AFTER the rules are frozen, stratify languages/domains, and have a second reader adjudicate disagreements. Our current 12-publication sample cannot estimate corpus recall, and all216 reading cannot measure omissions outside the original803.
8. **Do not infer deployment or absence:** a relevant claim identifies an investigative lead. It does not show ASIMOV connection, procurement, product implementation, reliability, legal compliance, or that an actual product lacks other safeguards.
