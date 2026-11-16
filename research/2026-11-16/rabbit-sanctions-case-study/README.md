# A short example of a catch failure

A “catch” is a rule that connects two sets of records. Think of it as a net: something that seems to break the rule might turn out to be a news story.

We started with two sources in Rabbit. One is the US Treasury’s sanctions list, often called the OFAC list. It names people and companies facing financial restrictions, including for terrorism or corruption. The other, USAspending, records government contracts and the businesses receiving them.

Put them together and a question appears: was the US government doing business with a company it had sanctioned? Normally, the rules should prevent that, unless an exception allows it.

A small Python program compared 6.6 million contract records with about 23,000 names and aliases on the sanctions list. This first pass did not need artificial intelligence.

Matching names sounds easy. But “Example Ltd” and “EXAMPLE LIMITED” might be the same company. Two unrelated businesses might also share a name. We tidied the names, found 13 possible matches, then checked details such as addresses to see whether we had the same business.

One looked promising. NAI Logistics, a Dutch fuel supplier linked to an Afghan former politician, appeared on both lists. Treasury had sanctioned it as part of action against a corruption network. Looking back through its contracts, we found eight military heating-fuel orders in Belgium dated just two or three days after the sanctions began.

But the lead shrank as we checked it. Four orders had been reduced to zero. The remaining commitments came to about $21,000, and we could not establish that fuel was delivered or money was paid. We also had unresolved questions about legal exceptions.

The overlap was brief, the amount modest, and wrongdoing remained unproven. We decided the lead was not strong enough to pursue as a story.

The net caught a lead. Checking it showed why a match on two lists is only the start.

## Technical annex

### Screen and entity matching

The 18 September 2026 run contained 6,639,176 unique contract/contract-vehicle transactions, 101,379 distinct recipient names and 23,398 names/aliases representing 9,980 sanctioned entities. Jev was not used; the screen made no AI model calls. The script normalized Unicode, capitalization and punctuation; a separate pass stripped terminal company suffixes. It did not perform fuzzy matching. Five normalized exact candidate pairs and eight suffix-removed pairs covered 153 transactions and 72 award identifiers. The other twelve candidate pairs had conflicting locations and remained unconfirmed.

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
