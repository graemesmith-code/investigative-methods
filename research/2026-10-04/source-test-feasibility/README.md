# Investigative test discovery: feasibility checkpoint, 4 October 2026

Start with **[18 reviewed recipes](reviewed-recipes.csv)**. Each states an observation, what to check, why it could matter, the exact linking problem, ordinary explanations, required auxiliary evidence and the next cheap check. These are proposals for reporting, not findings about any person or organization.

The original 1,730 rows are **mechanically screened candidates generated from 65 model-authored mechanisms**, not 1,730 independently reasoned or validated hypotheses. The updated [candidate inventory](candidate-inventory.csv) corrects ranking and trade-direction errors without inflating the count. Ten existing candidates received bespoke review; eight additional source-pair ideas are recorded separately. Do not add the 18 review cards to the candidate count.

Useful routes emerged around public-contract action histories, trial-registration references, World Bank project documents, power generation and emissions, network censorship, satellite identifiers, insider filings and information-order compliance. The most consequential proposed findings still depend on identity, dates, measurement boundaries or additional documents. The newsroom priority order is editorial judgment, not a probability of wrongdoing.

## What was established

- 344 source descriptions normalized with original SYS/AP IDs and provenance; 117,992 ordered pairs covered by the admission policy, not individually researched.
- 2,535 mechanism expansions: 1,730 retained candidates, 797 substantive rejections and eight deduplications.
- 18 source-specific review cards, spanning 16 mechanisms/ideas, with distinct falsifiers. These reviews used the same model session and are not independent review.
- All 139 unused sources revisited at catalog-triage level; 31 received source-specific reasoning. The other 108 require deeper work.
- Three linking components demonstrated with bounded public samples: a deposited trial number to its registry record, a World Bank document to its project, and an OONI ASN to a network lookup. The network response warned of stale history, so historical attribution remains unverified.
- Zero fully executable investigations established, zero bulk investigative tests executed, zero paid API calls.

One World Bank agreement text was fetched successfully. Its index date was in the future relative to this research date: read the document and verify chronology rather than trusting the index. An award returned by a 2025 spending search began in 2016: retrieve individual actions before interpreting interval spending. Null action classifications remain unresolved. All sampled identifiers are plumbing examples, not sanctions matches or allegations.

## What changed after review

The first checkpoint is preserved in its committed ZIP. Its navigation now points here. Phase-two code is isolated under `code/generator`; it does not overwrite the frozen first generator.

1. Provisional/name-only joins stay at testability 1 even when both sources have documentation.
2. Unverified routes cannot receive cost tier 1. Paris MoU and other known authorization/credential barriers receive tier 3; the burden is not a quoted monetary price.
3. F02 consistently starts with a non-EU reporter in Comtrade and inspects the reciprocal EU-member-reported Comext flow. Comext also contains non-EU data.
4. Building footprints indicate structures, not residents. Modeled population indicates estimated population, not exposure or harm. Separate review cards require the appropriate evidence.
5. Tailings scenarios require routing and an engineering scenario. Trial-publication comparisons require registry history, full text and protocol/analysis-plan context.
6. Automated candidates are labeled as such. The claim that reaching 5,000 would necessarily require padding has been withdrawn: this bounded pass does not establish a maximum number of defensible tests.

## Ranking and reproducibility

[Ranking and provenance](METHODS.md) explains which decisions came from model reasoning and which came from deterministic rules. Mechanism-level potential is separate from testability, identifier confidence and cost. Review priorities in the 18 cards are ordinal editorial judgments; equal priorities are allowed. A high priority is not a verified lead.

Reproduce the deterministic inventory from the repository root:

```sh
python research/2026-10-04/source-test-feasibility/code/generator/build.py --stage full
python research/2026-10-04/source-test-feasibility/code/author_reviews.py
python research/2026-10-04/source-test-feasibility/code/compile_review_annexes.py
python research/2026-10-04/source-test-feasibility/code/test_integration.py
```

Review prose is stored in the authoring scripts; regeneration does not reperform model reasoning or external checks. Do not rerun probes by default. Samples and their timestamps/hashes are in [the evidence ledger](evidence/probes.jsonl); official documentation observations are in [the documentation manifest](evidence/documentation.jsonl). Twelve production/integration checks passed. Passing them validates these limited invariants, not legal applicability or the truth of hypotheses.

## Next work and limitations

Deep-review the remaining 108 unused descriptions; then specialize remaining mechanisms and candidate pairs in diverse batches. Prioritize acquisition of exact historical schemas, ownership evidence, complete trial versions and unit crosswalks. Review source permissions before records are collected. Paris MoU storage authorization, Equasis registration, Companies House and energy API credentials remain genuine access gates; no new accounts or permission requests were initiated.

No source-pair absence can support an allegation without demonstrated coverage. No OFAC overlap establishes a violation without actual identity, the applicable restriction, dates, jurisdiction and exceptions. The entire 344-source policy sweep is complete; a source-by-source feasibility investigation and full validation of all 1,730 candidates is **not** complete.

No weekly ChatGPT allowance or model-token telemetry is available in this environment. The user's earlier 99% remaining report is historical, not a current reading. Paid external API spending in this work: zero.
