# F6 occurrence screening and intake contract

Version `f6-screen-0.6`. Full output belongs on Drive. Whole source snapshots stay in private consumer working storage pending rights review.

## What is screened

One record represents a specific document/version. Input `sources.jsonl` provides `document_id`, `source_url`, retrieval date, source-byte SHA256, legal entity, product/version, customer/contract, jurisdiction, document/effective dates, governing/incorporated/superseded status, access depth and rights disposition. Unknown fields remain null and create review gaps; they are never inferred from a company name.

Provide either a UTF-8 `text_path` relative to the input file or explicit `segments` containing `page`, `clause` and `text`. Plain extracted text uses form-feed page boundaries; an HTML document is one text unit unless separately segmented. Preserve the original source hash and the separate extracted-text hash. For PDFs, reconcile actual page count against extracted segments and record image/OCR status, appendices, tables, footnotes, attachments and any missing sections. Empty, partial, truncated or image-only text must never support an absence claim.

Explicit `incorporated_references` records should identify `to_document_id` or URL, invoking page/clause, incorporation wording/status, required-versus-informative status, retrieval/disposition and governing hierarchy. Each linked source receives its own versioned source row. A link is not automatically a customer duty. Missing accessible linked terms remain a coverage gap. The pipeline emits these chains without inventing incorporation.

## Pattern and semantic passes

The versioned lexicon covers direct IHL/LOAC anchors; unlabelled concepts; plausible indirect language; and generic legal/ethical/risk-allocation language. It includes initial French, German, Spanish and Dutch legal labels. This is a starter lexicon, not comprehensive multilingual recall. Other languages and less literal formulations require original-language review with labelled translations. No weapon/autonomy keyword co-occurrence is required.

Each detected occurrence retains a deterministic ID, page/clause where supplied, line, character and UTF-8 byte offsets, context span/hash, signal ID, version/access metadata and linked instrument chain. Every repeated occurrence remains present. Passage hashes permit a separate deduplicated count; document and version counts remain distinct. A machine category is provisional: even an explicit acronym or article number can be a false positive.

Human review JSONL uses a `document_id`, exact `text_sha256`, kind and reviewer. `adjudication` references an `occurrence_id`, classification, confidence, rationale and `negation_exception_status`. `semantic_addition` supplies character bounds and a rationale for an overlooked passage; no keyword is required. `full_document_semantic_review` records completion of the semantic pass against the exact text hash. Reviews fail on a stale hash. Reviewers must retain original wording privately and compare translations to originals.

The five possible adjudicated classes are explicit IHL reference; substantive law-of-war concept without the label; plausible indirect connection; generic legal/ethical language with no established IHL link; rejected false positive. Candidate control categories A–F and evidence levels 1–5 are separate from those reference classes. A policy saying "applicable law" is retained as a possible link, not promoted as an IHL restraint. Negations, exceptions, overrides and customer-duty allocations require passage-specific review.

All machine candidates start `not_promoted`, with unknown authority, trigger, consequence and applicability. Editorial integration may promote only reviewed records with exact evidence, contrary evidence and traceable version/customer scope. The screen itself cannot establish a legal conclusion.

## Rights-aware occurrence accounting

All locations and classifications remain auditable. Public occurrence rows default to offsets, hashes and an authored paraphrase. A source-specific explicit quotation budget may allow up to 20 words in aggregate in the screen output; remaining occurrences retain locations without copying more source text. This budget is not a legal determination or a licence to quote other parts without accounting. The editor must aggregate quotation across all report/register/memo outputs and use the source-specific copyright allowance or obtain specific redistribution authority before adding source copies. Stable original links permit inspection without public rehosting.

No full proprietary manual, publicly filed confidential-marked appendix, weapon-operation instructions or unreviewed raw snapshot belongs in the public package. Government/public-domain or openly licensed source copies may be included only with a recorded rights/access disposition. No signed download URL, credential or unrelated contact data is retained in public logs.

## Recall and false-positive audit

Before final release, manually review every promoted passage and its surrounding clauses, exceptions and incorporation chain. Record a reproducible sample drawn from (a) documents with no machine hits and (b) non-hit pages/sections inside hit documents. Use a declared seed, sample frame and rate; include language, source type, OCR and extraction strata where present. Record selection before reading, reviewer, spans reviewed, missed references, false positives and changes to the lexicon. Rerun after lexicon changes and preserve old code/lexicon hashes and counts. A synthetic regression suite is not a recall measurement.

The appendix pilot selected 11 non-hit pages using seed `F6-2026-10-26-01` and a 10% rate. Extracted-text review added five low-confidence semantic candidates, including general safety/ethics and amendment language; these are not five established IHL references. The independent raster-OCR pass described below is complete, but full semantic/image completeness is not certified, so no overall recall percentage is claimed. Machine-zero documents may support "no reference found" only after extraction completeness, image checks, full semantic review and the stated scope are documented. Inaccessible/missing sections remain excluded from that conclusion.

## Expected team transfer

Transfer an authored whitelist and member hashes through Library. Include lane memos, raw source observations separated from conclusions, source/version register, exact occurrence locations and short aggregate evidence, entity/customer resolution, query/access logs, exclusions/rights decisions, contradictions and actual editorial histories. For full-text screening, provide lawful consumer-readable primary text where authorized, or a stable public source plus exact document identity, hash, extraction/page inventory and detected-location register. Receipt of an authored memo alone does not establish that the coordinator screened the primary document in full.

Do not include private data, confidential-source material, raw operational annexes or signed links in an authored public transfer. Publicly accessible confidential-marked litigation exhibits require a specific minimal-extract disposition and must not be rehosted wholesale.

## Release checks

The mechanical validator checks file sizes, supported lightweight Git payloads, source/occurrence/candidate foreign keys and basic promoted-record fields. `--final` also requires an external acceptance artifact; it cannot generate one. These checks do not certify legal accuracy, source completeness, novelty, rights clearance or independent review. The manifest must distinguish source bytes checked locally, Drive metadata checked, and exact Drive bytes read back.

## Independent extraction cross-check

The pilot also completed local raster OCR of all 130 pages. A second machine pass produced 35 physical spans and no new page/signal pairs compared with the original 36 machine spans. OCR missed a liability-disclaimer term on PDF page 85; the original occurrence is retained. The master remains 41 occurrences including five semantic additions. These variants are one source compilation, not two sources or additive controls. Per-page hashes and differences are on Drive. Selected visual checks and complete raster OCR do not certify complete semantic recall. `ocr_crosscheck.py` provides the portable local workflow; `compare_extractions.py` checks same-source byte identity and detection-count differences.

Candidate quotation is linked to the occurrence record rather than copied into a second table. Orphan review records and unknown review kinds fail rather than disappearing silently. `control_id` remains null and `unique_control_countable` false until a separate normalized control review establishes scope and version relationships.

## Integrated candidate boundary

This document describes the coordinator pilot, not a uniform rerun of every native source. See TECHNICAL_NOTES.md for lossless integration, separate denominators, full accessible extracted-text scope and remaining review gaps. The later POST_FREEZE_SKYDIO_CORRECTION.md governs the original document-wide phrase flag and ED-006 shorthand; that flag cannot establish clause-local legal effect.
