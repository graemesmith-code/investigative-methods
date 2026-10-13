# Technical annex: bounded three-arm experiment

## Provenance and authorization

Base: `c319cce044c416a90bb4b7e5ac81d49ec63fb11f` on `mining-claims-four-case-starter` (draft PR3). New isolated worktree `/workspace/peru-holdout`; result branch `peru-holdout-2026-10-13`. Existing `work` checkout was preserved. Repository privacy verified by `gh repo view`: `isPrivate=true`. No repository AGENTS.md or applicable local `.agents/skills` files were found. Work ran wholly in the saved cloud environment; the user’s Mac was not used.

Delegated authorization allowed a new ceiling of US$5 per OpenAI/Jev, US$10 combined, existing credentials only, and private GitHub results. No other paid provider, credential/access changes, outreach or email were used. Credentials came from existing environment variables; no values or authorization headers were logged or committed.

## Freeze and source eligibility

[protocol.json](protocol.json), [questions.json](questions.json) and [pre-acquisition hashes](provenance/freeze.json) were written before downloading or reading new-year answers. Targets: Zn, Cu, Pb, Ag, Au, Cerro Lindo, calendar2025. No padding or additional year was added. All five remained in the denominator. The source/reference packets were hashed before provider calls in [packet-freeze.json](provenance/packet-freeze.json); the runner was hashed in [runner-freeze.json](provenance/runner-freeze.json). None of those inputs were changed after scoring. Prepaid offline Python replay was performed to verify prepared input shapes; no model outputs were available then.

Freshness audit examined all43 committed Peru baseline files, prior downloaded-source hashes,33 control assertions, notes, comparative headings/locators, and a repository-wide tracked-text search. Twenty-five distinct prior Cerro metal/year keys cover2019–2023. The2024 SMV annual document was explicitly read in the prior follow-up, making2024 exposure possible even though scored exact comparisons used2023.2024 is therefore excluded.2025 mentions in the relevant records were publication/signature dates, other-company2025 documents and registry year lists, not Cerro2025 production. The two fresh document hashes do not match any99 saved baseline hashes. Prior uncommitted history is unavailable, so freshness is conditional on the available record, not an assurance about every historical assistant context. The baseline-wide same-line search also produced unrelated “annexation”/case-insensitive substring hits; those are retained rather than silently treated as Cerro assertions.

Source identities and locators:

- English: SEC20-F `0001292814-26-001787`,2025 first annual column, printed page57, zero-based lxml HTML table301. The preceding mine-production paragraph identifies Cerro Lindo. A separate producing-mine paragraph identifies it as wholly owned by Nexa Peru despite the parent’s83.55% ownership of the subsidiary. The table is metal contained in concentrates, not zinc equivalent.
- Spanish: Nexa public2026 registry bucket entry `13062f6d-2242-1632-38da-7c9a8d6cb775`, Memoria Anual Integrada2025. PDF pages1(signature/preliminary),7(full calendar-year and report scope),16–17(mine and concentrate description/table4).2025 is the second annual column after2024. `tmf` is explicitly tonelada métrica fina. Silver/gold are contenidos in Oz.
- Spanish source class is company-hosted signed preliminary report. We did not retrieve a2025 SMV-hosted copy. The ordinary public SMV form search (company59/year2025) returned HTTP200 with Error500 content and no document link. Search failure does not prove no filing exists. No login, new access or contact was attempted.

Registry snapshots and every free request—including the failed SMV response—are logged under [provenance/](provenance/). Original PDF/SEC full bytes remain in `/workspace/peru-holdout-cache`, outside Git, with hashes and public URLs. Only selected factual rows and short scope excerpts are committed. `pdftotext -layout` and lxml supplied common preprocessing; no paid OCR or translation API was used. Spanish evidence was supplied in the original language, so no unreported translated evidence was substituted.

## Workflows and reference limitations

The Python template parses scalar rows from manually selected HTML table301 and Spanish table4/column2025. Assistant selection of captions, source dates, scope snippets and layout is preparation, explicitly outside computed runtime. Preparation is not autonomous end-to-end extraction. Missing fields abstain; no amount of model confidence fills evidence.

Five categorical questions independently assess entity/operation, full period/ownership basis, measurement/product, units, and source versions/preliminary status. Options supported/conflict/unknown have identical descriptions across providers. Highest-probability choice is the frozen rule; confidence is retained raw and never considered evidence of truth. The same packets are JSON `state` for Jev and serialized JSON `input` for Decisions; endpoint-native question schemas differ, evidence and semantic questions do not. Each arm uses Decimal arithmetic after gates. The executable harness supports t/kt and oz/koz/MMoz within their declared unit family; it abstains/rejects unsupported dimensions rather than silently using more general conversions. This batch required no cross-family conversion.

The inherited tolerance convention is one displayed unit per component, summed: integer-vs-integer here permits2t or2oz. All five natural differences are exactly zero, so tolerance choice is immaterial. Missing/dash values remain missing, never zero. Model judgments do not calculate differences, certify physical truth, or imply wrongdoing.

The [source-grounded reference](reference-review.json) was saved before paid outputs. It was made by the same assistant preparing evidence, not a separate blind human or independent-model reviewer. Natural labels are therefore nonindependent reference judgments. The Spanish scope and mine-unit production are taken as full100% mine output; parent ownership is not a proportional multiplier. OpenAI’s four unknown ownership-period choices expose interpretive uncertainty/review demand, not proven failures against an independent truth set. Reference labels were not altered after seeing those outputs.

Frozen semantic arms shared preprocessing/extraction/arithmetic but substituted model semantic gates for the reviewed Python gate layer. The approved “same Python plus AI” requirement should preserve deterministic explicit conflicts. That implementation omission was discovered after scoring; it is honestly recorded as development. [Protected hybrid replay](results/protected-hybrid-development.json) preserves existing Python conflict gates before shared arithmetic, so OpenAI’s planted partial-period acceptance is stopped. No paid output was regenerated, reference changed, or prompt tuned. Report frozen results and development results separately; do not call the correction another blind holdout. There is no model-derived gain over prepared Python in either track.

## Engineered checks and denominators

Exactly five fixtures, labelled engineered in every packet, never natural findings:

1. Zinc quantity increased10%, all comparison identities unchanged; expected comparable numerical difference.
2. Spanish full year changed to2024; expected invalid period comparison.
3. Spanish zinc changed to volume m3; expected invalid dimension/product comparison.
4. Spanish zinc unavailable/dash; expected insufficient evidence.
5. Spanish footnote changed to acquisition-half-year and83.55% attributable output; expected invalid period/ownership comparison.

Quantity fixture changes the Spanish table scalar and extracted scalar; the English original remains a factual English comparison source. Different quantities do not justify discarding same-assertion comparability. Both model arms instead marked semantic conflicts and did not produce the intended numerical-difference alert. This is a false parking/classification, not a false agreement. The OpenAI ownership fixture is the one frozen semantic false acceptance. Separate metrics count error returned as agreement, numerical-alert miss, exact four-way fixture correctness, and guard-protected behavior. See [summary.json](results/summary.json).

Natural dependence: one mine, one full year, two related issuer documents, five correlated metal rows. There are not five independently sampled companies or document pairs. Fixtures reuse one packet and add no independent natural coverage. No confirmed real mismatch was available; natural mismatch recall is unmeasured. All frozen targets stay in the denominator; the failed SMV acquisition is separately0/5 rather than disappearing behind the company-hosted success.

## Interfaces, costs and cumulative guards

Primary official documentation was retrieved13October and hashed: [OpenAI Decisions](https://developers.openai.com/api/docs/guides/decisions), [OpenAI model details](https://developers.openai.com/api/docs/models/gpt-6-luna), [TypeSafe models](https://docs.typesafe.ai/models), [TypeSafe HTTP API](https://docs.typesafe.ai/api). Archived copies and retrieval fingerprints are in provenance. Decisions uses `POST https://api.openai.com/v1/decisions`; only `gpt-6-luna` was documented as supported, input US$0.10/M, no output/cache charges for this endpoint. Generic Luna Responses output pricing does not apply. Returned model is `gpt-6-luna`; no more granular snapshot was exposed in the response or documented as selectable. Jev uses `POST https://api.typesafe.ai/v1/systemone`, pinned `jev-1.13.0`, text only,64k total context/32k state-plus-longest-question; input US$0.042/M, output free. Returned version matches.

The fresh ledger starts at zero independently of older experiments. Before each request, it durably reserves US$0.25 OpenAI or US$0.01 Jev and checks provider cumulative expenditure against US$5. Automatic redirects/retries are disabled. Any failed/uncertain request retains its full reservation and halts that provider. A crash after reservation leaves a pending row and blocks further use. Completed reported input usage must lie within a conservative bound of five copies of the entire serialized UTF8 request (one token/byte), plus4096 tokens per question. The OpenAI bound assumes US$0.22/M for safety (long-context/regional uplift), even though observed short standard usage costs0.10/M. Every body is under30k bytes; the reserve exceeds that bound. Per-call realized cost is rounded upward to whole microusd for budget accounting. Providers were executed sequentially in one process, no concurrent invocations or paid reviewer calls occurred.

10calls each; no retries or unsuccessful paid attempts. Exact raw response bytes, model identifiers, usage, request hashes and request IDs if supplied are preserved. Budget reservations/completions are in [budget-ledger.jsonl](results/budget-ledger.jsonl) and [attempt-events.jsonl](results/attempt-events.jsonl). Tokens are actual provider-reported values, not estimates. Costs are list-rate calculations, not invoice charges; actual invoice is unknown. No billing-admin key, balance top-up, new model/provider or access change was requested. New preparation, harness and report writing require assistant time; ChatGPT/human/editor costs remain unknown. Fixed inherited acquisition/control work is not included in marginal batch charges.

## Reproduction and checks

From repository root:

```bash
python research/2026-10-13/peru-holdout/code/verify.py
python research/2026-10-13/peru-holdout/code/evaluate.py
python -m unittest discover -s code/peru_production_pilot -p 'test_*.py' -v
```

`evaluate.py` reads saved outputs without network. `run.py` without `--live` replays saved provider outputs and regenerates timing fields; preserve the original result file before replay if timing provenance matters. Live replay is denied for previously attempted IDs; no command should bypass the ledger. `prepare.py` requires the external raw cache, manually reviewed locators and lxml; rerunning preparation is development and will alter freeze timestamps. Full originals are intentionally not committed. The17inherited tests pass. Additional offline checks verify frozen hashes, exact denominators, supported returned models, raw request/evidence equality, arithmetic, cumulative budgets and absence of existing credential values from all new committed candidate files. No original baseline output was regenerated or overwritten.
