# Methods, coding and quality review

## Design and unit

A feasibility test of an attribution-sensitive codebook, using purposively discovered public sources. The unit is one distinct attributable proposition within an event/document. Preserve claim_id and event_id. Related clauses in one document are clustered, not independent observations. Repeated publication or reaffirmation is not a new policy change. An initial aspiration of five events and at most six claims per event was not achieved; distinct document provisions were retained and the clustering disclosed rather than hidden behind a balanced row quota.

Country denotes the government represented by the speaker or issuing institution, not the hosting outlet's geography. Named serving officials and official texts are distinguishable from academics, vendors, retired officials, anonymous claims, journalists and editorials. TASS publication alone is not sufficient to classify a statement as Kremlin policy. The same rule applies to US and Chinese outlets.

## Evidence and dates

Each row retains carrier/original/retrieved URLs where recorded, source locator, speaker, office, authority and verification description. Evidence origins are News-reported claim, Primary-document benchmark, Original document reached through news, and Official document republished by news. These layers are not interchangeable.

Original statement date, news date and date precision are separate. A report date can only proxy for an undated interview if labelled. An old document at a newer URL is not new policy. A restatement does not date the policy's first adoption. No capture-date field is manufactured: these were public-web reads, not verified INFINI article-body retrievals.

## Coding dimensions

- **Relevance:** tier 1 directly concerns targeting, weapons use or control; tier 2 is broader military-AI context; tier 3 is generic-AI inference only and excluded from the strict core.
- **Function:** identify, recommend/support, select, engage. A claim about decision support is not proof of autonomous engagement.
- **Stance:** prohibit, conditional permit, permit with conditions unstated, or ambiguous, as recorded. Nuclear/conventional and other scope limits must be retained.
- **Safeguards:** human role; use limits; testing and legal review; legal framework; civilian protection; scrutiny; accountability. Values distinguish requirements, advocacy/proposals, rejection and non-mention, preserving ambiguity rather than filling gaps.
- **Legal distinction:** existing-law compliance and advocacy of a new legal instrument are separate fields. Some inherited legal_instrument labels are retained for auditability; interpret them with the more specific fields and caveats, not alone.
- **Specificity and authority:** a general principle, procedural condition and operational boundary differ. Instrument status distinguishes adopted internal policy, official explanation and proposal. “Required” describes wording; it does not independently certify binding legal force, implementation or compliance.
- **Public persuasion:** not yet coded. Future frames should be tied to the actual speaker and audience, separating official justification from the reporter's framing. Missing language means not stated, not rejection.

The CSV/JSON are normalized publication exports of the reviewed set. Missing recorded values remain blank; no unsupported translations, dates or language labels were inferred to complete fields. Source quotation/excerpt fields are deliberately omitted in this public export. Paraphrases, locators and URLs remain available for checking.

## Quality review performed

All 90 rows received an AI second-pass review of metadata, attribution, dates, functions, stance and safeguard interpretation, with checks of the source events and contested passages. The review is not independent human annotation. There is no measured precision, recall, agreement, kappa or Krippendorff alpha.

Important corrections/caveats preserved:

- Chinese July 2023 carrier: academic Zeng Yi's advice was not treated as Ambassador Zhang Jun's statement. Zhang's original speech was separately consulted. Two adjacent generic-AI safeguards remain inference-only, not core targeting evidence.
- Chinese and US human-only nuclear decision statements retain nuclear scope.
- March 2026 Chinese official English and Chinese formulations are not fully equivalent; the language/version caveat must survive any later translation analysis.
- Russian rejection of “meaningful human control” terminology is not coded as rejection of every human role. Rejection of extra ethical imperatives is not automatically rejection of a legal instrument. RU-24 concerns information-processing decision support.
- The US DoDD 3000.09 text was read on an **unofficial mirror** after official hosts were inaccessible. The original-authored text is distinguished from verified official hosting. Other official/news material corroborates major requirements, but this is not cryptographic authentication of the mirrored file.
- The Russian working paper is not treated as an adopted operational rule. Its controls and proposals cannot establish actual battlefield practice.
- Two later US machine-transcript leads were not counted as verified official statements.

## What reproduction can and cannot do

Run `python verify_counts.py` in this directory to reproduce structural counts from claims.json and check the CSV export. It does not rerun search, validate source truth, measure coding accuracy, or reconstruct the entire assistant interaction. Exact search/call cost and complete prompts were not captured in a reproducible experiment log. Source links and locators support inspection, not an assurance that each current web page will remain unchanged.

Before comparative inference, define and freeze retrieval/inclusion rules; retain source bodies lawfully; record retrieval dates and publication/statement dates; log exclusions; cluster syndicated/repeated claims; validate native-language coding with qualified humans; test sensitivity to outlet and document mix.

## Methodological inspiration

These sources informed the design; their use does not validate this pilot:

- Johannes Geith, Global Policy, 2026: multidimensional state positions on autonomous weapons. https://onlinelibrary.wiley.com/doi/10.1111/1758-5899.70101
- Anna-Katharina Ferl, 2023, “Imagining Meaningful Human Control”: discourse and legitimation. https://doi.org/10.1080/13600826.2023.2233004
- Justin Grimmer and Brandon Stewart, 2013, “Text as Data”: validation and substantive interpretation. https://web.stanford.edu/~jgrimmer/tad2.pdf
- Manifesto Project Coding Handbook: proposition/quasi-sentence units. https://manifesto-project.wzb.eu/down/papers/handbook_2021_version_5.pdf
- Klaus Krippendorff, 2004: reliability in content analysis. https://doi.org/10.1111/j.1468-2958.2004.tb00738.x
- Matthew Denny and Arthur Spirling, 2018: preprocessing sensitivity. https://arthurspirling.org/documents/preprocessing.pdf

The possible contribution is an updated, validated comparison of safeguards and their public circulation, not the first quantification of national autonomous-weapons positions.
