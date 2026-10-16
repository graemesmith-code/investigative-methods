# Interfaces for later analysis — designs only

No model classifier, novelty/newsworthiness scoring service, Exa request or stronger-model dossier run was executed in this acquisition pass. The dry run uses only explicit identifiers, dates, amount parsing, text length and the regexes in `code/normalize.py`. Its flags describe readiness, not novelty, significance, legality or public-interest findings.

## 1. Evidence envelope and eligibility

Read canonical Parquet/JSONL for text-oriented work; use `*_source.parquet` for full structured source fields. The [canonical schema](canonical_record_schema.json) defines identifiers and lineage. Every candidate must retain `document_id`, `source_record_id`, `source_url`, `raw_locator`, source snapshot hash/vintage, UTC retrieval time, exact excerpt and source-specific date/money semantics. A source portal link without a unique record URL requires the accompanying raw locator and identifiers.

Eligibility fields are independent: `security_mission_evidence`, `international_engagement_evidence`, `capability_evidence`, `administrative_or_domestic_only`, `money_interpretation_ready`, `date_interpretation_ready`, `duplicate_or_overlap_risk`, `needs_human_review`. Each takes `supported`, `contradicted`, `unknown` or `not_applicable`, with evidence references. A DoD sponsor supports a security connection, but does not establish technological novelty or international engagement. Domestic performance is not an exclusion. DOE and DHS text matches require mission review. Medical/basic research and broad accounts remain candidates/context until reviewed.

## 2. Novelty and capability scoring

Input: evidence envelope + source narrative + appropriation/program/award identifiers + dated capability taxonomy + prior source records. Output: `capability_labels[]`, `novelty_score` (nullable), `novelty_basis` (new science, engineering step, application, scale or claimed transition), `maturity_claim`, `comparison_baseline`, `evidence_refs[]`, `uncertainties[]`, `model_and_prompt_version`, `review_status`. Separate what the source claims from what independent evidence supports. A new modification, fresh announcement or high dollar amount is not inherently a novel capability. Acquisition regex tags are only retrieval features.

## 3. Relationships and capability clustering

Use a graph of evidence-backed candidate relationships rather than irreversible entity merging. An edge has `left_document_id`, `right_document_id`, `relation_type`, `basis`, `confidence`, `valid_time`, `evidence_refs`, `review_status`, `contradictions` and `alternative_explanations`.

Relations include `same_reported_award`, `same_award_candidate`, `same_entity_candidate`, `same_program_element`, `same_capability_candidate`, `component_of`, `successor_to`, `co_developed_with`, `mentions`, `financial_representation_overlap`, and `unresolved`. Exact native USAspending award keys can group modifications. SBIR contract text, PIIDs without agency/parent context, similar acronyms, PE references and names create candidates, not automatic merges. A paper acknowledging a lab-wide contract does not identify a separate investment. Cluster IDs are stable review objects; memberships and evidence versions can change. Preserve competing clusterings.

## 4. Cluster newsworthiness

Input: reviewed cluster + timelines + monetary measures with grain/vintage + capability/maturity evidence + independent coverage evidence. Output: nullable component scores for novelty, consequence, specificity, scale relative to a defensible baseline, maturity/transition, international implications, accountability and reporting gap; rationale and evidence for each; contradiction log; `human_editor_decision`. Do not rank only by ceilings or add repeated obligations/budget lines. `No match` in the present acquisition is never evidence of no previous reporting.

## 5. Exa coverage checks

A request object would contain cluster ID, names/acronyms/PIIDs, source dates, bounded date ranges, alternative spellings, exact query strings, retrieval mode, source inclusion/exclusion rules, maximum requests and explicit cost approval. Response records need canonical URL, title, publisher, date, query, matched cluster claims, source excerpt and coverage status (`substantive`, `mention`, `unrelated`, `uncertain`). Deduplicate syndicated articles and distinguish first report from source announcement. Store the queries and negative results with run date; absence remains search-limited. The included dry-run requests set `execute=false` and `max_requests=0`.

## 6. Stronger-model journalist dossiers

Input: reviewed evidence/relationship graph and coverage results. Produce a short lead; verified facts; financial timeline with separate requests, authority, obligations, outlays and ceilings; capability/operational claims; performers and uncertain affiliations; what is actually new; prior reporting; international relevance; contradictory evidence; unresolved questions and suggested source interviews. Every factual claim must cite source-record links and exact evidence excerpts. The model may propose reporting leads, not manufacture facts, perform financial aggregation across grains or resolve uncertain relationships silently. Include counterarguments and a human fact-check queue. No contacting people is authorized by this design.

## Reusable transport

`pipeline_request.example.json` is a versioned batch contract. Add results as a new layer keyed to evidence IDs; never overwrite raw text or ingestion validation. Deterministic dry-run features and proposed queries are in `validation/dry_run.json` and `samples/dry_run_candidates.jsonl`. They are explicitly unscored.

## Existing announcement adapter

The unchanged original and historical announcements remain first-class later inputs. Use `../history/combined_deduplicated_index.csv`: its columns are `dedup_key`, `announcement_date`, `service_or_agency_section`, `paragraph_sha256`, and JSON `pointers`. Each pointer supplies file, data row, source URL and paragraph hash. An adapter can use `announcement:<dedup_key>` as its evidence ID and dereference the original/history CSV's `raw_paragraph_verbatim` without editing either collection. Retain existing original-file checksums and per-paragraph SHA-256. Announcement date is a publication date, not necessarily action date; announced face value, options, ceilings and explicitly obligated-at-award funds need separate interpretation. Existing paid-pilot scores/coverage outputs are historical annotations, not new validated labels or proof of novelty/no prior reporting. This pass does not rescore them.


The correction pass adds hypersonic retrieval features and keeps untagged records in the deterministic example as `untagged_requires_model_review`. No regex match is required for later novelty review. Short spending descriptions require enrichment from SBIR abstracts and program/project narratives before judging capability or novelty. Every example relationship endpoint must resolve to an included evidence envelope; `smoke_test.py` enforces this alongside mandatory lineage on the Commons, APFIT and DARPA project inputs. Source-specific context/lookup tables listed in `validation/table_roles.json` need an adapter before this evidence interface.
