# EP metadata triage and bounded claim inspection, 15 November 2026

## Executed scope
Input: expanded/ep-native-union.csv, 803 publication identifiers, 604 EP application identifiers. Applied reproducible title-pattern triage to all 803 using screen.py: 25 priority title candidates, 216 secondary candidates, 562 lower-priority/unreviewed. These are work-queue labels, not confirmed relevance findings. Pattern choice was informed by an initial title scan and is not an independent recall test; no statistical accuracy inferred. No abstract or claim text was used by the triage script. No lower-priority item is conclusively excluded.

Selected eight publication claim sets for substantive inspection: EP3882560B1, EP3882561B1 (already downloaded in expanded/); EP4647709A1, EP4653796A1, EP4033309A1, EP4111281B1, EP4293311A1, EP3732432B1 (six new official XML files). This is 8 documents, not 8 independent inventions or complete family/prosecution histories. Official source URLs were retrieved from EPO Linked Open Data representation records, not guessed. query.sparql and representations.json record the lookup; download-log.json records acquisitions. EP4293311A1 official XML claims are German, not English: original German plus Google Patents translation were checked. The initial English-only extractor yielded an empty claims text; corrected text file explicitly labels German. The XML itself always contained claims.

## Findings and limits

1. EP3882560B1 and EP3882561B1, Diehl Defence, priority 20 March 2020, grant publication 31 August 2022. Claim 1 in each describes aborting an ongoing attack after recognition of a friendly-identification signal. This is a concrete friendly-fire mitigation concept, not general civilian discrimination. Other claims address the companion defensive equipment. The two documents share inventors, dates and technical subject matter; treat as closely related until formal family reconciliation. Neither establishes deployment, tested reliability, or machine learning.
Sources: https://patents.google.com/patent/EP3882560B1/en and https://patents.google.com/patent/EP3882561B1/en

2. EP4647709A1, Raytron, publication 12 November 2025. Claim 1 moves a sight into an abnormal mode when aiming at/tracking a human. Claim 5 explicitly adds deep-learning human recognition. Claim 6 offers several alternative responses, including warnings, display disruption, shutdown, or trigger-lock instruction. Claim 7 includes manual revocation. Therefore a universal non-overridable firing prohibition would be a false reading. Civilian/hunting context, not demonstrated military deployment. This is a useful anti-misuse comparator, not evidence a military system adopted it.
Official source: https://data.epo.org/linked-data/representation/publication/EP/4647709/NWA1.xml

3. EP4653796A1, Raytron, publication 26 November 2025. Claim 1 disables the sight after detecting a shot while aiming at a human; claim 2 adds an abnormal sighting mode beforehand. Important timing: this does not by itself prevent the first shot. The application frames civilian hunting use. Published US counterpart exists (US12510331B2), so do not count the EP record as a separate invention. No effectiveness or field-use evidence checked.
Source: https://patents.google.com/patent/EP4653796A1/en

4. EP4111281B1, Ericsson, priority 24 February 2020, grant publication 8 July 2026. Claim 1 adapts operating limits to communication-link performance. Claim 7 specifies returning to a designated location or halting when connection is inoperable. General autonomous robotics, not weapon-specific proof. Relevant loss-of-control comparator; it is not a universal human kill switch.
Source: https://patents.google.com/patent/EP4111281B1/en

5. EP4033309A1, Hamilton Sundstrand, publication 27 July 2022. Claims 1/9 describe user-commanded weapon management; claims 3/4 and 11/12 permit software updates changing tasks. No specific ethical/civilian-protection safeguard established by this claim review. Retain as an update/revalidation accountability lead, not as evidence guards exist or are absent in a product.
Source: https://patents.google.com/patent/EP4033309A1/en

6. EP4293311A1, 21strategies, publication 20 December 2023. Claim 8 expressly permits learning/adaptation during deployment after initial training; claim 10 likewise adapts control rules after training. This is a weapon-control architecture, not a verified guardrail. Google family table lists EP only, not proof of no other filing. Useful question: what retesting bounds changes made after initial validation? Do not infer unsafe operation or deployment. Google's citation list points to Helsing DE102025101672A1, which remains an unreviewed national-document lead.
Source: https://patents.google.com/patent/EP4293311A1/en

7. EP3732432B1, BAE Systems Bofors, priority 28 December 2017, grant publication 5 February 2025. Six claims concern autonomous guidance/reconnaissance and pre-programmed target identification, not an explicit human veto or civilian safeguard. Description mentions reducing collateral damage through precision, which should not be conflated with ethical decision criteria. Already has US family counterpart US11499807B2. No absence-of-safeguards finding about an actual product.
Source: https://patents.google.com/patent/EP3732432B1/en

## Scope remaining
795 of 803 EP publications were not substantively claim-reviewed in this pass; some were inspected elsewhere. Family deduplication across US/EP/WO/national records is pending. Title patterns do not reliably find safeguards buried in claims or descriptions. Wider classes and national-only documents remain outside this union. This pass improves coverage but cannot justify 'all relevant patents' or 'all available documents'. None of these patents proves ASIMOV involvement, deployment, actual performance, or legal compliance.

## Preserved evidence
Title-triage CSV, six new official XML files, extracted claims (German explicitly labelled where applicable), query response, acquisition log and SHA-256 manifest: https://drive.google.com/file/d/1p1XBvQzIb4M5m_iKY_CQA-UHHr1kgwUC/view . The two previously acquired Diehl XMLs remain in the earlier expanded-EP evidence archive.
