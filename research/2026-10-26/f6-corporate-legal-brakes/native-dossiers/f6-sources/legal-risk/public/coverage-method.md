# Legal risk coverage and reference screening

Cutoff and retrieval date 26 October 2026. This lane used only free public research, with no outreach, paid query, docket purchase, login, permission change or restricted-annex access.

## Denominators and access

The source register has **49 source records**. **37 full extracted documents** and **two scoped sections of one additional enacted act** were machine-screened. **11 records were not fully processed** because retrieval failed or returned maintenance/challenge content. PDF text extraction covers **389 pages**. The processed corpus contains **1,597,667 characters**. HTML page counts are not invented.

The enacted NDAA was downloaded as a full 4.6 MB HTML source, but ONLY §§ 801 and 876 are in this lane's screened corpus. The remaining act is expressly out of the selected screening scope. For PDFs, complete extracted text includes appendices and footnotes where present as text; images/scans were not OCRed. No statement of complete image coverage or fully verified layout is made. The 2024 US Code 2441 PDF initially interleaved columns under layout extraction; default reading-order extraction replaced it for screening, while the earlier text remains private. The primary web PDF rendering separately corroborated the operative jurisdiction/certification passages.

**Access correction:** HTTP 200 did not mean a document was obtained. LR07, LR21 and LR26 were challenge/maintenance bodies and have been reclassified as failures. LR10/LR26 French original judgment, LR40 Lockheed 2024 supplier terms and LR41 historical ASBCA raw PDF were not promoted from snippets. LR41's full web PDF view was available but the raw full text was not processed; it remains discovery-only in this corpus. OLRC preliminary pages LR19/LR29/LR48/LR49 failed 404/503; indexed official text is only bounded currentness corroboration. This applies especially to 18 USC 2441 and 50 USC 1431. Current FAR and enacted 2025 NDAA were separately obtained.

The exact 30-name panel appears in company-coverage.csv/json. Only RTX and Boeing have direct company-specific promoted evidence in this lane. The other names received an attempted grouped indemnity discovery query with poor precision, not a thorough individual contract audit. Wrong Shield AI financial/cybersecurity entities were rejected. This is not a percentage-of-companies-with-safeguards denominator. Other team lanes own additional company research.

## Lexicon and semantic method

Version **legal-risk-v1.2** is supplied as lexicon.json and executable screen_references.py. It includes English direct IHL anchors, protection concepts, indirect legal/governance signals, generic applicable-law/export/insurance language, and selected German/French/Swedish equivalents. No autonomy/weapon co-occurrence requirement is used. Every regex match is retained with source ID, exact short matched phrase, extracted PDF page or HTML scope, text line, character offsets, version, source hash, access depth, context hash and duplicate link. Full surrounding copyrighted source passages are not republished; promoted passages have authored context and exceptions in evidence records.

The final register contains **1,288 lexical occurrences plus 3 manually added semantic occurrences =1,291 total**. The deduplication key retains every occurrence but links exact normalized contextual repeats; **1,287 unique contextual occurrences** remain under this narrow key. This is not a count of unique safeguards or unique legal propositions. Different versions/languages remain separate.

All **246 explicit-anchor candidates and 92 concept candidates** were context-reviewed by the lane researcher, grouping repeated statutory/procedural references while retaining every locator. **22 false positives** were identified: ordinary legal/nondiscrimination uses of distinction, The Hague as a location, and Rome Statute Article 36 concerning judges rather than Additional Protocol I weapons review. The rest are classified as explicit IHL references, clear protection concepts or plausible/generic legal connections according to context. Crimes against humanity and broad international-criminal-law titles are not automatically treated as IHL-specific. UN declarations remain attributable to the declaring state. Old/revoked amendment/EO notes are not current law. French translated party submissions are not converted to holdings.

The remaining **303 indirect and 647 generic lexical candidates** remain conservatively retained and not individually adjudicated, except where linked promoted passages were separately reviewed. Review_status and linked_record_ids make that distinction explicit. Thus **341 occurrence rows are context-reviewed**, including the 3 manually added rows. **29 normalized evidence records** are promoted with explicit applicability/counterevidence. A source link to a promoted record does not promote every candidate occurrence in that source.

## Manual nonhit and recall test

Purposive, not random, design: examine short no-hit documents in a language underrepresented by the initial English lexicon, then documents where insurance/export language risks false-positive IHL attribution.

- LR22 German StGB 27: initial lexical zero; full 444-character text reviewed. Added **Beihilfe**, labelled translation assistance/aiding. This is general intentional-assistance law imported through VStGB 2, not an independent company IHL policy.
- LR23 German OWiG 30: initial lexical zero; full 3,684-character text reviewed. Added **Geldbuße gegen juristische Personen**, labelled translation fine against legal persons. Corporate administrative liability context, not ICC corporate jurisdiction.
- LR20 German FinFisher prosecutor release: initial lexical zero; full 7,870-character text reviewed. Added **Ausfuhrgenehmigung**, labelled translation export licence. An indictment allegation, not a conviction or IHL safeguard.
- LR24 FAR 28.305 and LR25 DFARS 250.104-3-70: independent editor read complete extracted texts. War-hazard coverage is an insurance/loss-allocation counterexample, not an IHL restraint. Separate 10 USC 3861 authority matters; no AI approval inferred.
- LR09 Stockholm court status: independent editor read Swedish and English paragraphs and confirmed future judgment/pending status. A page-level 24 June stamp does not establish the exclusive date of subsequently updated content.
- LR06 RTX full consent: promoted clauses manually read with exceptions, privilege protection, nondebarment and nonlicence-promise counterevidence. No direct IHL link established; legal-department support and automation are not automatically product restraints.

The expanded German/Swedish v1.2 pass added 28 direct-anchor occurrences, all manually context-reviewed. The scoped SAMM follow-up discovered LR46 C4.4.18.4's explicit LOAC reference and LRE29 was added. These are **documented recall improvements**, not evidence that semantic recall is now perfect.

## Incorporation and exclusion chains

- FAR 50/PL85-804 -> contractor request -> risk definition/insurance evidence -> approval/denial memo -> incorporated 52.250-1 -> claim/payment. Only governing framework verified; named AI request/incorporation/exercise unresolved.
- PL119-60§ 876 qualifies older FAR approval delegation for advanced nuclear systems/components; 90 days means decision, not deemed approval.
- RTX consent -> covered scope -> independent official SOW/delegation -> reviews/audits/board escalation. Consent verified; SOW, completed audit and named export decision not obtained.
- SAMM chapter 8 -> UAS Principles-of-Use agreement -> DSCA 20-31 historical 2020 FMS/BPC notes -> current Appendix 6 note list. Current public list omits named note and refers to CAC-only 6A; current note/actual LOA not verified; no repeal or universal continuation inferred. CAC access not attempted.
- SAMM chapter 4 C4.4.18 -> governmental transfer/training-support gate with explicit LOAC purpose. No operational targeting instructions republished, no named customer contract established.
- Lafarge US plea -> Attachment A corporate admissions and Attachment C compliance commitments. French 2026 issuer status is a separate jurisdiction/procedure. Plea term completion/extension not checked.

## Reproduction and rights

Preserve the source URLs, raw source SHA256 and extraction hash from sources.json. Re-fetch only freely available sources where permitted; protected/inaccessible sources remain exclusions. The code operates on locally held extracts and will not bypass access or publish anything. Its input layout is a workspace with private/LRxx.txt and public/sources.json plus evidence.json; run `python screen_references.py --workspace /path/to/legal-risk-workspace`. Raw bytes are not in the whitelist or transfer package. Public matched phrases are minimal; lengthy source paragraphs, protected standards, full manuals and operational weapons details are excluded.

Query-log.csv/json is explicitly a family-level reconstruction, not a verbatim complete provider trace. The exact recent query-request supplement records available request strings; source fetch URLs/timestamps/errors provide a complete 49-record acquisition trail. No absence conclusion applies to inaccessible, image-only, truncated, unprocessed or unadjudicated material. An unfinished semantic classification is not reported as zero IHL references.
