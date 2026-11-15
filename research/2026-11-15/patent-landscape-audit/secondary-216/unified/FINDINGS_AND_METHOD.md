# The 216 secondary European patent publications: deeper review
15 November 2026

## What this pass did, and did not do
The immutable 216-record queue was derived from an earlier 803-title screen, not a complete world patent universe. Four review ledgers were joined to the original EPO publication URIs; no record was dropped or silently replaced. The JSON preserves each reviewer's original assessment alongside normalized fields; the CSV is the readable index. Counts are in counts.json. This is selected substantive claims review, plus targeted description passages: **not a line-by-line reading of every specification, drawing, claim or prosecution history.** Some short claims sets were read in full; those are explicitly labelled.

The 216 publication records have **165 distinct EP publication numbers**, not 216 separate inventions. A1/A2 applications, A3 search reports, B1/B2 grants and B9 corrections can refer to different stages or versions. Even165 is not a patent-family count: related divisional applications and international counterparts still require a verified family map. A malformed source ID, EP3377840B92022-04-20, is preserved in its original field and normalized to EP3377840B9 using its canonical EPO URI.


### Final reading coverage
**202 exact EP publication records received targeted substantive claims review;2 were reviewed only through explicitly mapped WO counterparts;12 A3 search-report records had no claims reviewed. Total216.** Of the12 A3 records,11 Google pages were available without claims and EP4768001A3 had Google404 with official metadata only. The exact EP claims for EP4795475A1 and EP4795351A1 remain unverified; their WO2025082599A1 and WO2025082903A1 counterparts were read without treating them as identical EP text. Two initial chunk2 Google404 gaps were recovered and read using official EPO English claims; the original retrieval failures remain in their logs. Per-chunk totals for exact-EP/WO-only/A3 are53/0/1,49/0/5,52/0/2,48/2/4.

These are publication-level reading counts, not202 different inventions or202 proven safeguards. Every row has an auditable disposition; this is not a claim that all216 full documents were read exhaustively.

## Findings that genuinely sharpen the safeguards question

1. **An actual constraint can hide behind a bland title.** EP4229352A1 claims13–14 describe withholding an artillery fire-control solution according to a restricted-area parameter. This is a concrete firing-solution gate, not merely better targeting. It appears related to the KMW US material already identified; do not count it as a newly discovered independent invention before family reconciliation. It does not prove AI use, deployment or effectiveness. https://patents.google.com/patent/EP4229352A1/en

2. **Portable-weapon safety offers a useful, bounded comparator.** EP3948143A1 includes AI image/gesture recognition options (claims33–34); description[0117] connects detection of a person ahead of the weapon to locking firing. Permitted-area restrictions appear elsewhere in the disclosed embodiments. This is not evidence that deployed autonomous battlefield weapons distinguish civilians. https://patents.google.com/patent/EP3948143A1/en

3. **An expressly military AI disclosure leaves the rule's substance open.** Naval Group EP3812690B1 combines AI attack optimization with rules against undesirable attacks (claim3), lost-link guidance (claim4) and carrier-command priority (claim5). The inspected passages do not supply a precise civilian-protection or law-of-war test. The useful reporting question is what those rules actually contain and whether an identifiable system implemented and tested them. https://patents.google.com/patent/EP3812690B1/en

4. **Human control is mode-specific, not a binary label.** EP4271959B1 claim9 distinguishes direct, lock-on-fire, lock-on-track and autonomous modes. EP4168728B1's targeting authorization has manual-bypass provisions (claims11–12); its authorization concerns sight alignment rather than a demonstrated ethical test. EP3569966B1 claim1 permits normal firearm operation when the electronics malfunction or lose energy. These exceptions prevent describing every disclosed gate as an unconditional human veto or fail-closed protection. https://patents.google.com/patent/EP4271959B1/en ; https://patents.google.com/patent/EP4168728B1/en ; https://patents.google.com/patent/EP3569966B1/en

5. **Several attractive 'safeguards' weaken under adversarial reading.** EP4731953A1 allows engagement of a passing target in description[0044], so distinguishing incoming from passing targets is not necessarily a prohibition. BAE EP4058350A1/B1 overrides vehicle configuration to preserve a weapon sightline; it does not establish a human veto on shooting. EP4025866B1 overrides camera orientation. EP4025498B1's collateral-damage display does not enforce a casualty limit. The controlled object and the exception matter more than the word 'override', 'non-threat' or 'safety'. https://patents.google.com/patent/EP4731953A1/en ; https://patents.google.com/patent/EP4058350B1/en ; https://patents.google.com/patent/EP4025866B1/en ; https://patents.google.com/patent/EP4025498B1/en

6. **Civilian autonomy supplies testable design comparisons, not proof of military adoption.** EP4196859B1 separates an independent safety monitor from vehicle control; EP4644058A1 escalates from slow/stop commands to actuator-power disconnection; EP3727766B1 expands an uncertainty region when a human is no longer detected; EP4198714A1 conditions rule changes on validation; EP3735620B1 requires human approval of an industrial motion plan. These sharpen interview questions about independence, uncertainty and revalidation. None establishes ASIMOV lineage or weapons uptake. https://patents.google.com/patent/EP4196859B1/en ; https://patents.google.com/patent/EP4644058A1/en ; https://patents.google.com/patent/EP3727766B1/en ; https://patents.google.com/patent/EP4198714A1/en ; https://patents.google.com/patent/EP3735620B1/en

## Updated methodology
- Titles prioritize reading, never decide absence. The initial 216 label was a queue, not a finding.
- Record two independent axes: domain (weapon, military nonweapon, civilian autonomy, ordinary mechanical safety) and mechanism (authorization, inhibit, abort, boundary, monitor, validation, ordinary aiming, none established).
- For any promoted safeguard capture **protected party/object; trigger; action controlled; claim or description location; independent/dependent/optional status; operating mode; override direction; failure response; assumptions; and evidence of adoption/testing**. Do not confuse recognizing a person, recognizing protected status, and causally preventing an attack.
- Read exceptions and relevant dependent claims plus surrounding descriptions before promotion. Guardrails can be optional, overridable, alert-only or fail-operational.
- Keep source access, extracted section availability, semantic reading depth and inference separate. An A3 search-report page with no claims and a404 are not negative evidence of safeguards. A downloaded full document is not a fully read document.
- Preserve exact EP sources and mapped WO sources separately. Official B871 mapping supports a counterpart relationship, not identical EP claim scope. Never silently fill an EP gap with WO claims.
- Preserve original-language passages and identify machine translations. EP2984440B1's Google claim16 presents an apparent friend/foe wording contradiction; do not silently repair or quote it as settled without checking the official source.
- Same-number application/grant versions stay separate in the audit. Deduplicate families only after verified mapping, and retain material changes between claims sets.
- Keyword screening is a retrieval aid, not a negative conclusion. 'Target' may mean an ammunition-delivery destination; 'override' may mean camera or vehicle control; physical protection may protect the weapon platform rather than civilians.
- An independent reproducible12-record claims sample is documented in the companion QC note. It is a development check, not a statistical recall estimate. After freezing revised criteria, use a fresh held-out negative sample to test missed safeguards. This pass cannot prove completeness of the broader patent search.

## Editorial bottom line
The stronger answer is not 'we found no guardrails' or 'patents prove weapons are safe.' We found disclosed technical controls, ambiguities and explicit exceptions. The next evidential bridge is from a specific claim/embodiment to an identifiable product, configuration and test result. Patents alone do not supply implementation, deployment, effectiveness, procurement, current legal status or compliance. No ASIMOV adoption or battlefield use is established by this review.

## Reproduction and audit
Run integrate.py against records.json and chunk1/review.json, chunk2/notes.json, chunk3/review.json, chunk4/review.json. The script enforces216 records and216 unique canonical URIs, preserves raw reviewer schemas, and reports publication-kind and reading-status counts. Per-chunk acquisition files, raw HTML/XML, extracted text and scripts form the underlying evidence. Local paths are working locations, not external source citations. SHA256 manifests identify the exact saved files.

### Separate official acquisition result
The EPO XML acquisition ledger covers all216 requested rows:136 returned claims-bearing XML,78 metadata only, and2 errors. These are **acquisition** counts, not additional reading counts or unique inventions. Google Patents reproductions supplied many substantive claims missing from the selected EPO XML representation. A metadata-only representation does not mean the patent office has no full document. The unified index records official status and URL separately from the reviewer source.


## Evidence archive
Public-source originals, per-record ledgers, extracted text, acquisition logs and SHA-256 manifest: https://drive.google.com/file/d/1azsmsVWxZgz652fSf3gWOO4FQJiwFKI0/view
