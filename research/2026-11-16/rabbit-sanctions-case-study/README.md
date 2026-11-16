# What’s the catch? Sanctions and public contracts

**16 November 2026 — a teaching example, not a finding of a sanctions violation.**

A name-and-address match linked a sanctioned company to US procurement records. Further checking found a short overlap in reported contract obligations, but no established payment, delivery or legal violation. The lead was parked because its apparent scale and reporting value were limited. This example explains how a connection between two datasets becomes a question worth checking—and why it may stop short of a story.

## The public example

The US Treasury’s Office of Foreign Assets Control (OFAC) publishes sanctions lists. USAspending publishes federal contract actions. Company names and addresses connect the records. The Federal Acquisition Regulation adds the test: purchases prohibited by sanctions generally cannot proceed unless an authorization applies.

A Python script screened **6,639,176 fiscal-year 2025 contract transactions** against **23,398 sanctions-list names and aliases**. Thirteen possible name matches emerged. One was NAI Logistics B.V., a Dutch fuel supplier linked by Treasury to Afghan former politician Ajmal Rahmani. Follow-up work across earlier years found eight reported orders dated 13–14 December 2023, just after designation on 11 December, under a military heating-fuel contract in Belgium. They recorded **$36,309.46 in positive obligations**, offset by **$15,662.32 in reductions**, leaving **$20,647.14 net**. Obligations are commitments, not proof of payment.

Four orders were reduced to zero; no later positive obligations were found in the retrieved history. Payment, delivery and the applicability of legal authorizations remained unresolved. The lead was set aside as a reporting priority, not classified as a proved “minor violation.”

The useful lesson is simple: a match is a reason to look. It is not a finding. The identity, dates, financial measure and applicable rule all have to survive checking.

## Corrections to the remembered account

- **Corruption sanctions, not terrorism sanctions.** Treasury designated NAI through the Rahmani network under Executive Order 13818 / Global Magnitsky. It did not designate the company as a terrorist in this case.
- **Heating fuel oil in Belgium.** The disputed contract specifies burner fuel oil. Older recipient records include diesel, but that does not establish the product in these eight orders.
- **No Jev use.** The original screen used a Python standard-library script, with no model calls, paid data or outreach.
- **Editorial choice, not a verified administrative explanation.** Graeme’s 14 October decision treated the limited overlap as a low reporting priority. The records do not establish why the orders were placed or reduced.

## Technical annex

### Screen and entity matching

The 18 September 2026 run contained 6,639,176 unique contract/contract-vehicle transactions, 101,379 distinct recipient names and 23,398 names/aliases representing 9,980 sanctioned entities. The script normalized Unicode, capitalization and punctuation; a separate pass stripped terminal company suffixes. It did not perform fuzzy matching. Five normalized exact candidate pairs and eight suffix-removed pairs covered 153 transactions and 72 award identifiers. The other twelve candidate pairs had conflicting locations and remained unconfirmed.

The sanctions snapshot was from September 2026. Historical designation dates therefore had to be checked independently against the dates of the procurement actions. Current list membership cannot establish historical sanctions status by itself.

NAI matched by full name and Kingsfordweg 151, Amsterdam. Procurement identifiers included UEI SLVJF3DR8MN5 and CAGE H2G78; the sanctions record used entity 44257 and Dutch registration 60346515. These identifiers help track each dataset, but they are **not a shared cross-dataset key**. Name and address supplied the corroborated bridge.

### Follow-up and financial interpretation

The follow-up recovered 244 contracts and seven contract vehicles, with 450 unique transactions dated 30 December 2014–11 March 2025. Vehicle SPE60523D9402 had 27 child orders, including 19 in fiscal year 2024. Eight reported base actions dated 13–14 December 2023 carried positive obligations; five reducing modifications offset some of that amount. Four orders were fully deobligated.

Signed copies of those eight individual orders were not recovered. Their dates are database action dates; one was first reported much later. Null outlay fields are not proof of no payment. Scheduled performance dates are not proof of delivery. The last positive obligation in the retrieved history was 14 December 2023. The later termination, on 11 March 2025, does not demonstrate 456 days of uninterrupted purchasing or payments.

### The rule and the unresolved exception

[Federal Acquisition Regulation 25.701(a)](https://www.acquisition.gov/far/25.701) connects sanctions restrictions to procurement, subject to authorization. [Treasury’s designation statement](https://home.treasury.gov/news/press-releases/jy1973) identifies the corruption rationale and NAI’s relationship to the network.

An official-US-government-business authorization was already present in **31 CFR 583.509 in 2023** ([historical regulations, PDF page 10 / printed page 654](https://www.govinfo.gov/content/pkg/CFR-2023-title31-vol3/pdf/CFR-2023-title31-vol3-part583.pdf)). The provision was renumbered 583.510 in 2024. The Defence Logistics Agency’s termination notice nevertheless states that no applicable authorization or exemption existed for the engagement. Its underlying applicability analysis was not recovered. Neither the existence of a general authorization nor the agency’s notice independently resolves the legality of each reported order or payment.

No new investigation, outreach or records request was initiated for this teaching example. It reconstructs preserved work and rechecks selected primary documentation.

### Evidence trail

The evidence below is pinned to repository revision `79a42f5299e5be24a0a0f1ef5b0959857810b128`:

- [experiments/01-ofac-baseline.md](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/experiments/01-ofac-baseline.md)
- [annexes/experiments/01-ofac-baseline.md](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/annexes/experiments/01-ofac-baseline.md)
- [code/ofac/screen_contracts.py](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/code/ofac/screen_contracts.py)
- [research/2026-10-14/nai-contract-history/README.md](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/research/2026-10-14/nai-contract-history/README.md)
- [research/2026-10-14/nai-contract-history/technical-audit.md](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/research/2026-10-14/nai-contract-history/technical-audit.md)
- [research/2026-10-14/nai-contract-history/evidence/documents/SPE60523D9402.txt](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/research/2026-10-14/nai-contract-history/evidence/documents/SPE60523D9402.txt)
- [research/2026-10-14/nai-contract-history/evidence/documents/termination-notice.txt](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/research/2026-10-14/nai-contract-history/evidence/documents/termination-notice.txt)
- [research/2026-10-14/nai-contract-history/evidence/eight-base-order-review.json](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/research/2026-10-14/nai-contract-history/evidence/eight-base-order-review.json)
- [research/2026-10-14/nai-contract-history/evidence/all-recipient-transactions.csv](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/research/2026-10-14/nai-contract-history/evidence/all-recipient-transactions.csv)

- [Preserved official-response archive](https://github.com/graemesmith-code/investigative-methods/blob/79a42f5299e5be24a0a0f1ef5b0959857810b128/research/2026-10-14/nai-contract-history/evidence/official-api-snapshot.zip).
- [Original contract PDF](https://dibbs2.bsm.dla.mil/Downloads/Awards/22NOV22/SPE60523D9402.PDF).
- [Original termination modification and notice](https://dibbs2.bsm.dla.mil/Downloads/Awards/22NOV22/SPE60523D9402_P00002.PDF).

Selected evidence files, the original script, the source-catalog audit and a checksum manifest are backed up in Google Drive. The archive inventory states exactly what was copied; it is not a claim to mirror every original input or the 6.64-million-row dataset.

### Publication boundary

This is a separately authorized teaching example. Public Rabbit source entries remain neutral. The three proposed personal usage notes stay in the research repository and are excluded from the public catalog; the 17 reusable collections and five access routes receive neutral descriptions and publisher links. Future discoveries should generate proposals, not automatic publication.
