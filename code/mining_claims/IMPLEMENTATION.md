# Implementation handoff

The next deliverable is an independently reviewable claim pair from a second reporting period for each surviving project. Keep the four inspected specimens as regression controls. Do not expand the six parked cases until their named blockers are resolved from accessible evidence.

## Sequence

1. **Complete extraction.** Replace the manual Western ledger with extractors that return the original text, page/table or cell, number, unit, date and qualification. Preserve the manual entries as a comparison benchmark. Start with Peru, whose two sides already have working numerical extraction.
2. **Build a dated document inventory.** Record filing date separately from the date the claim describes. Record amendments, issuer, submitting subsidiary, recipient authority/process and document version. Do not infer a historical effective date from today's retrieval date.
3. **Make entity and category bridges reviewable.** Use dated legal identifiers, licences and ownership relationships. Store the evidence for each bridge. Ity's project population and the distinction between direct and group ownership are required inputs, not string-matching conveniences.
4. **Add translation-assisted claim capture.** Extract original-language passages with enough surrounding text to retain footnotes. A proposed translation must preserve negation, qualifiers, dates, units, reporting basis and company/government attribution. Store original and translated spans together; reject unsupported inferences. Translation proposes structured claims; it does not approve comparability or decide a contradiction.
5. **Introduce new years under new contracts.** Source changes first create a review task. Only a reviewed contract may enter the comparator. Revisions must have explicit supersession links; do not compare a corrected filing to an obsolete claim as if both were current.
6. **Prepare an evidence packet for each candidate.** Include both source versions, source locations, original passages, translations, scope bridge, numerical normalization, tolerances, date alternatives, amendment check and why all permitted interpretations are incompatible. Do not publish automatically.

## Definition of ready for a first live batch

- All four baseline specimens reproduce from verified originals, with manual steps visible until replaced.
- Each new period has affirmative company attribution on both sides and a dated entity/metric bridge.
- Newly automated extractions agree with the inspected specimens and reject a plausible wrong table, column, company or period.
- Missing data, preliminary figures, changed sources, incompatible accounting bases and unresolved dates produce a blocked case with a reason.
- A synthetic contradiction is detected; all plausible legitimate rounding, currency and date interpretations are exhausted.
- The batch produces its own source and decision log. Failures are counted separately from consistent pairs; a blocked fetch is never counted as an agreement.

## Technical annex: next data model

Extend the current observation format with `claim_id`, `source_id`, `source_sha256`, `issuer`, `submitting_entity`, `receiving_process`, `project_identifiers`, `filed_at`, `effective_dates`, `original_language`, `original_span`, `translation`, `locator`, `value`, `unit`, `population`, `measurement_basis`, `qualifications`, `amends_claim_id`, and `review_record`.

Keep the original number string. Currency needs direction as well as a number: XOF per USD is different from USD per XOF. Physical units need a substance and basis: fine molybdenum is different from tonnes of concentrate. Ownership needs a relationship: group economic interest is different from direct legal shares. Source declarations, government receipts and reconciled results must remain distinct fields.

The current comparator is intentionally bounded to the four contracts. It is not a general schema validator or a secure ingestion service for arbitrary untrusted JSON. Add formal schema validation, stronger provenance validation and per-case extraction failure reporting before accepting outside submissions or running unattended.
