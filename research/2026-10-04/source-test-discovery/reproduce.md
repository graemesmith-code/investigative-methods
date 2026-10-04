# Reproduce and extend the design audit

Use Python 3 from the repository root. The core generation uses only the standard library, no credentials, network calls, model API or paid service. Original Rabbit files are required at their existing repository paths.

```sh
python research/2026-10-04/source-test-discovery/code/build.py --stage full
python research/2026-10-04/source-test-discovery/code/capabilities.py
python research/2026-10-04/source-test-discovery/code/test_validation.py
python research/2026-10-04/source-test-discovery/code/finalize.py
```

The early checkpoint is immutable history. Do not rerun `--stage early` over it: subsequent fixes intentionally changed the design and availability context. Use Git's early commit or a separate directory if reproducing that snapshot. Review CSVs are session-authored judgments, not manufactured by the generation script; rerunning review_sample.py merely creates a pending-review selection and overwrites its output.

`probe_samples.py` is an optional, intentionally separate network step with three fixed free requests, 200 kB response caps and 20-second timeouts. It does not screen actors or run hypotheses. Do not rerun it just to reproduce the longlist: saved responses, hashes and failures are already in evidence/. No API key is supplied and no access restriction is bypassed.

Promote a recipe to feasible only after verifying schema, access terms, actual fields, entity/identifier compatibility, temporal/geographic coverage, cardinality and a small reproducible record example. Record the precise request, retrieval time, response hash and why the observed data can test the predicate. An executed join remains a lead, not a finding. A legally established assertion additionally requires the correct current and historical instrument, dates, jurisdiction, conduct and exceptions.

Read sources.jsonl for exact AP descriptions; join-field-dictionary.csv for namespace constraints; source-coverage.csv for all 344 dispositions; pair-universe.csv.gz for policy coverage; rejected.jsonl for exclusions. Not-admitted pairs were not proven useless. For new work, add a model-authored mechanism with a substantively new evidence or falsification path; do not multiply thresholds, years, prose variants or upstream mirrors.

The full bundle contains research artifacts and code, not duplicated copyrighted third-party bulk datasets. Original Rabbit text remains in the private repository; the normalized AP descriptions preserve catalog provenance. Source-level sample records are included solely as availability evidence and are not associated with an allegation.
