# Independent civilian rule reasoning audit feasibility study

Prepared for Graeme Smith | 17 October 2026 | Public evidence cutoff 17 October 2026 UTC

A feasibility study of DeonticBench and DAR, with military assurance claims considered only as accountability context.

Revision 2 | Scientific review structure added on 17 October 2026. No expert review or outreach performed.

## Contents

1. Executive verdict

2. Question and public interest

3. Acquired artifact inventory

4. Access licenses and history

5. Three distinct reproducibility claims

6. Bounded scoring evidence

7. First gate independent answer oracle

8. Scientific review and reviewer roles

9. Discovery and confirmatory design

10. Transformations and valid controls

11. Reproducibility and denominator protocol

12. Statistics and interpretation

13. Automation architecture and provenance

14. Isolation and fail safe cost controls

15. Personnel and achievable tiers

16. Transparent token and financial model

17. Adoption consequence and investment gate

18. Counterarguments fair publication and deliverables

19. Limitations and verification record

## 1 Executive verdict

A small independent audit is feasible now for civilian rule reasoning, using public DeonticBench data and the DAR implementation. It can inspect the scoring system, reconstruct selected released configurations and test carefully validated input changes without institutional cooperation. Exact reproduction of every historical published number is not established: original trial logs, precise service behavior and complete runtime provenance have not been acquired. A new endpoint or a replacement model produces a new experiment, even when its name resembles a published model.

The best first investment is a technical audit and a narrow numerical pilot. Automation can manage acquisition, scheduling, transformations, checking and analysis. It cannot establish the correct interpretation of a rule merely by asking another model. A trusted engineer with limited availability can help build the system, but an independent human must validate a small set of rule-to-answer derivations. If that review is unavailable, publish the access and scoring findings and stop before capability claims.

Actual work for this study comprises public repository and paper acquisition, version/history inspection, ten dataset-file downloads, row counting, schema inspection and a tiny synthetic offline check of reviewed pure scoring functions. No paid model, API, Exa, benchmark inference, generated Prolog or agent experiment was run. No institution was contacted. The proposed experiments and budgets below are options requiring separate authorization.

The public connection to military assurance is real but bounded. Both papers acknowledge DARPA CODORD funding, and the official program page lists them as performer papers. That makes their published claims suitable for independent accountability. It does not show that the civilian benchmark represents a deployed military system. A civilian benchmark failure cannot establish unsafe deployed weapons, battlefield conduct or a legal violation. [S01, S02, S03, S04]

Recommendation: proceed only through the free technical gates, then seek a capped 24-anchor pilot if independent answer validation is practical. Reserve a larger donor proposal for a demonstrated public-interest consequence and a credible human review budget.

## 2 Question and public interest

The question is whether one researcher, supported intermittently by a machine-learning engineer, can independently reproduce published government-funded rule-reasoning results and test sensitivity to minor input changes using materials obtainable on 17 October 2026. The study tests feasibility, not the models' abilities. Its executable scope is civilian taxation, baggage fee rules, immigration administration and housing-law benchmark tasks. The initial recommended confirmatory pilot narrows further to numerical tax and baggage-fee cases.

DeonticBench was submitted on 6 April 2026; DAR on 3 June 2026. Their funding acknowledgements identify DARPA CODORD and Schmidt Sciences. DARPA's CODORD page lists both under RTX BBN performer papers and describes an aspiration toward reliable, explainable rule reasoning. RTX's 28 August 2025 announcement describes DONATELLO development under a DARPA award. These are evidence of funded research and stated ambitions, not evidence that a specific production DONATELLO system equals any model-harness configuration evaluated in DAR. [S01-S04]

The public-interest hypothesis is that claims about dependable rule application deserve an independently checkable account of their evidentiary limits. A scoring defect, inaccessible historical artifacts, or reproducible sensitivity to irrelevant wording may matter even when authors openly acknowledge weaknesses. Novelty and material consequence still need to be shown; simply repeating that large language models sometimes make mistakes is unlikely to justify a major investigation.

Do not construct operational targeting scenarios, optimize weapons or develop military testing procedures. TEELAWS and ASIMOV/REBAR enter only as comparisons of adoption, public access and published claims. No technical transfer from the civilian tests to operational military evaluation is proposed.

The study uses a source cutoff of 17 October 2026, UTC. Program pages and pricing pages are live snapshots, not authenticated histories. Their contents may change after acquisition. Claims about unavailable material mean it was not verified in the named public locations inspected, not that it cannot exist elsewhere.

## 3 Acquired artifact inventory

Two full public Git repositories were cloned and inspected as text and data. DeonticBench is pinned to 3c168f943880fcbd3a3d717a516500312534273b. Harbor DeonticBench is pinned to 2fe3aa40bf856d533a79a6052a28eb3fc1b618f1. The Hugging Face dataset is pinned to 805fb0529d7ae295679c5c1730765ec07d2c20ac. Three arXiv PDFs were acquired as v1: 2604.04443, 2606.05009 and 2605.18423. These are actual local files, not merely advertised links. [S01, S02, S05-S07, S11]

All ten advertised Parquet files at the dataset pin were downloaded and read with a trusted Parquet reader. Whole split row counts are 100 SARA Numeric, 276 SARA Binary, 300 Airline, 5,314 Housing and 242 USCIS-AAO: 6,232 in total. Hard counts are respectively 35, 30, 80, 78 and 28: 251 in total. Hard is advertised as a subset of whole; the totals must not be added together as independent cases. The count check validates file row counts, not correctness, uniqueness or every hard-to-whole membership relation.

The Git checkout contains those five hard JSON files with the same row counts and five smoke files with five records each. It does not contain current whole splits. Airline concerns baggage FEES, including fee computation; it is not a lost-luggage compensation dataset. DAR excludes housing: 35 + 30 + 80 + 28 = 173 source cases, across four subdomains. The adapter text reads these four hard files. Three task framings do not create 519 independent factual cases. [S05-S07]

The acquired Harbor tree contains direct, zero-shot and few-shot adapters, templates, harness source, command examples and evaluators. Its generated datasets and jobs are not tracked at the inspected paths. They are advertised or generatable outputs, not acquired historical task bundles or raw trial logs. A separate meta-harness evaluator exists and needs its own review before a Kira configuration is used.

The public evidence inventory records URLs, byte counts, SHA-256 checksums and access timestamps. Raw downloads and historical extracts remain locally preserved; only concise metadata, our study and the bounded synthetic check results are published.

## 4 Access licenses and history

The Hugging Face card declares CC BY 4.0 for the dataset. Preserve attribution to the authors and source dataset, cite the pinned revision, identify modifications and retain applicable notices if redistributing derivatives. This card does not independently settle every upstream document right or any personal-data issue. Avoid republishing large immigration narratives unnecessarily. The proposed release should prefer IDs, hashes, transformation specifications and minimal excerpts needed to explain findings. [S07]

The Harbor checkout contains an Apache License 2.0 file. Preserve relevant copyright, attribution and modification notices if redistributing its code; inspect bundled component licenses separately. The DeonticBench root has no standalone LICENSE file in the inspected checkout. Public readability is not a blanket permission to redistribute code. Inspection, citation and publication of our own method remain possible; obtain licensing clarity before packaging substantial repository code or publishing a turnkey fork. The paper PDFs are retained as evidence and linked, not republished.

Version history makes the reference correction independently inspectable. The initial commit c421259e4cc6dbe41f568f94fb4e11017b2ea98b is public. Commit e2516e32ab4f86e63ba4046d8549dd58a7d992a0 on 26 April is titled as a reference correction. Commit c6e3fe749a200fbfe1d78622968d33e4f6cec31d on 26 May updates reference programs and smoke splits. The README acknowledges corrections to flawed reasoning, trivial logic and hardcoded outputs. Historical hard JSONs from all three revisions were actually extracted and checksummed. [S05, S08]

For a May-specific comparison, use e2516e32 as the immediate predecessor and c6e3fe74 as the corrected revision. For paper-era sensitivity, preserve the initial version as an additional branch of analysis. Neither is proven to be the exact artifact used for every April publication result. Recovered Git history does not recover service settings, original model traces or the complete original data generation process.

Freeze benchmark-era statute files and embedded texts with the cases. Do not silently substitute current law or current airline policies. A contemporary-law study would be a separate question with new authoritative sources and labels.

## 5 Three distinct reproducibility claims

Historical verifiability asks whether an outsider can trace a reported table entry to the exact original cases, outputs, model snapshot, settings and scoring. The papers and released source allow useful examination, but no complete original raw jobs bundle was acquired. The inspected ignore rules exclude jobs, trials and result CSV patterns. That is an access limitation, not proof that logs never existed or were deliberately withheld. Exact historical reproduction remains conditional on recovering missing provenance and an accessible matching model service. [S01, S02, S06]

Current implementation reproduction asks whether an auditor can reconstruct and run the released method at a fixed revision today. Public cases, statute texts, adapters and instructions make that plausible. Offline build review, dependency resolution, a verified runtime image and model availability are still gates, not completed work. A released task generator can support reconstruction even when generated datasets are absent. Record the generated task hashes, and compare them to any later-acquired historical task bundles rather than assuming identity.

Independent robustness asks whether a currently tested, precisely identified configuration retains correctness under validated changes to public civilian cases. This does not require original logs. It does require independent answer derivation, a protected holdout, full denominator accounting and explicit model access permission and spending authorization. Its results must be labelled by current model identifier, observation date and released implementation revision.

DAR is a reasoning setup evaluated with general models and agentic harnesses. The inspected release is not evidence of a dedicated trained DAR checkpoint. Likewise a benchmark reference Prolog program is an answer artifact, not a separately validated model. DeonticBench discusses training experiments, but this study has not acquired or verified the full training checkpoints, optimizer state and trajectories needed to reproduce those experiments. [S01, S02]

Publish a claim ledger with one row per target number: paper version, table, domain, metric, configuration, sample denominator, required artifacts, acquired evidence, missing items and attainable claim level. Never label new-model agreement with an old score as historical replication.

## 6 Bounded scoring evidence

At the Harbor pin, collect skips trial directories without result.json. A trial with result.json but missing verifier/test-stdout.txt is retained with expected and got both empty and an error marker. Default _compute_row accuracy counts equality while ignoring that marker. Thus two empty strings can count as correct. The --errors-as-incorrect branch prevents that accuracy path. The same file selects the latest lexicographically named run for a model within a parent jobs directory, so older repeated attempts can disappear from its aggregate. [S09]

For strict macro-F1, an errored trial with a known expected label becomes an error sentinel; an errored trial with no recoverable expected label is dropped from F1. The reported n can therefore differ from the records contributing to F1. Missing token or cost fields default to zero in collection. These observations justify independent denominator and usage reconciliation; strict mode alone is not a complete audit remedy.

A tiny offline check used only two reviewed, pure scoring functions extracted with Python's syntax parser. No repository module, dependency setup, generated program, harness or model was run. A synthetic accuracy fixture with one ordinary correct record and one error record with two empty strings scored 2/2 by default and 1/2 in strict mode. A three-record strict-F1 fixture retained n=3 while its calculation used two known-label records, yielding macro-F1 1/3. These are synthetic demonstrations of current code behavior, not reconstructed publication results. The public offline-checks.json records the inputs and scope; synthetic-scoring-check.py repeats the bounded check against a supplied pinned scorer.

The feasibility finding is limited: independent scoring is necessary and achievable. Whether any published table is affected is unknown without original relevant records and scoring provenance. Do not infer misconduct, publication-wide inflation or the frequency of this path from its existence. A different historical evaluator or an error-free original job could produce unaffected results. Review Kira's separate evaluator independently before applying this observation to it.

## 7 First gate independent answer oracle

Before inference, establish a small answer set that does not depend on either the tested model or the authors' reference program. For each anchor, a researcher writes a rule-to-fact derivation identifying the exact frozen provision, relevant facts, applicable thresholds, exceptions, precedence and final label or amount. A second human checks the derivation without seeing model answers. A language model can help locate passages but cannot be the sole judge or supply unquestioned labels.

For numerical cases, implement a separate, small deterministic checker from the reviewed derivation using exact integer or decimal arithmetic. Test bracket boundaries, inclusivity, rounding, aggregation and exception priority. Do not translate the authors' Prolog line by line and call agreement independent verification. Compare the independent result with the source label and Prolog only after the human derivation is locked. Disagreement creates an oracle-dispute record; resolve it openly before the confirmatory manifest is frozen or exclude it with a reason recorded before model execution.

The reviewer may be an appropriately skilled rule analyst rather than retained counsel for every record. Obtain limited domain-expert advice on genuinely ambiguous provisions, exception conflicts and the validity of transformation families. The expert validates rule semantics, not the complete investigation or an AI-generated corpus. The scientific-review stages below require separate methodological and contextual expertise where appropriate. Do not present this as professional legal advice or an adjudication of anyone's real case.

Recommended gate: 24 numerical anchors, with rule provenance and answer derivations accepted by both reviewers, plus two invariant variants and one changed-answer control per anchor. If 24 cannot be validated within the time cap, narrow the claim and case set; do not compensate with thousands of unreviewed outputs. Immigration and housing may need more interpretive work and enter only after a separate semantic feasibility check.

Every final scheduled test must have a trusted label in an external grading manifest before it runs. Agents must not be able to read that manifest, source labels, reference answers or verifier credentials. Oracle ambiguity discovered later triggers transparent sensitivity analysis and correction, never silent relabelling toward a preferred conclusion.

## 8 Scientific review and reviewer roles

Journalistic publication should meet a scientific standard: specify the question, preserve falsifiable predictions, freeze the confirmatory protocol and retain negative or null results. Graeme expects possible access to former JAGs, ethicists and ICRC specialists for methodology, results review and commentary. Availability is a user expectation, not confirmed access. No reviewer, collaboration, institutional endorsement or ICRC participation has been secured. No contact has been made.

Before preregistration is frozen, an independent methodological and statistical reviewer should challenge sampling, controls, cluster units, multiplicity, power, denominators, retry rules and inference limits. Resolve material objections in a dated decision log; retain unresolved dissent. Before inference, suitable civilian-domain reviewers validate the selected rule-to-fact derivations, numeric checker assumptions and transformation families. Former JAG or ICRC experience does not by itself establish tax or baggage-policy expertise. These roles may differ.

After outputs are collected, disputed answers should be adjudicated against the frozen rubric by a reviewer blinded, where practical, to model identity, configuration and investigators' preferred conclusion. Record what was masked and any unavoidable unblinding. Keep original labels, outputs, reviewer decisions and disagreements. A new interpretation after inference must not silently rewrite the confirmatory oracle: report the original analysis and a clearly labelled amended sensitivity analysis.

After analysis, IHL and ethics specialists can assess the wording, public-interest relevance and limits of military-assurance interpretations. Expertise cannot validate out-of-scope claims or turn civilian results into evidence of battlefield harm. Offer authors a fair opportunity to respond to the exact findings and proposed wording; reviewer commentary and author response remain distinct from the statistical results.

Review packet checklist: question and claim ledger; pinned protocol and analysis plan; sampling frame and oracle derivations; transformations and controls; schedule and denominators; blinded dispute bundle; analysis code and statistical plan; exclusions, negative results and amendments; proposed claims and expertise limits. Retain a versioned packet index and written reviewer disposition.

Separate investigator, engineer, rule reviewer, statistical reviewer and contextual commentator responsibilities. Disclose funding, authorship, prior involvement and relevant institutional ties; record recusals or independent adjudication where conflicts matter. The engineer maintains execution and isolation, not automatic authority over legal labels or interpretation. Do not assume extensive unpaid expert work. Agree bounded tasks, hours, compensation if any and availability before committing to a tier; narrow or pause confirmatory work if essential review is unavailable.

Preserve exploratory and confirmatory distinctions, all exclusions with timing and reasons, and every dated protocol amendment with its rationale and whether outputs had been seen. Publish negative and null findings under the same standards as positive findings. Review is scrutiny, not certification or endorsement.

## 9 Discovery and confirmatory design

Use a small discovery set, such as 8-12 anchors outside the confirmatory set, to debug formats, identify interpretation pitfalls and choose deterministic transformation families. Those sizes are planning choices, not completed sampling. Record all exploration. Do not reuse discovery failures as if they were a held-out confirmation. Freeze a separate confirmatory list, seed, transformation specification, primary endpoints, exclusions, retries, budgets and decision thresholds before viewing confirmatory model outputs.

The proposed 24-anchor numerical pilot should be sampled across tax and airline rules, difficulty and available exception patterns, subject to the independent-review gate. The final sample frame and selection probabilities must be documented. If practical constraints produce a purposive set, say so and limit conclusions to that set. Keep source-family and rule-family identifiers so cases using the same provision are not mistaken for unrelated evidence.

Compare two configurations with the model snapshot, case text, labels, exemplars and evaluation method fixed. A direct-answer configuration and one reviewed agentic configuration can answer a practical question, but differences combine navigation, tools, prompts and resource use. To attribute a gain to a harness feature requires ablations that change only that feature. Do not infer causation from two practical bundles.

Report controlled-budget comparisons with matched token or spending limits separately from practical-configuration comparisons using each method's documented settings. Record differences in tool calls, context construction, repair turns, timeouts, sampling temperature and output limits. Do not use a stronger new model as the control for an older weaker model and attribute the difference to the harness.

For each condition, collect three planned stochastic draws per input if authorized. Retain all draws. Randomize and interleave configurations and variants in small blocks to reduce confounding by endpoint drift and time of day. Record provider response model identifiers, dates and routing information where available. A provider seed is useful metadata but not a guarantee of determinism. A changed or unavailable endpoint creates a new cohort, not an invisible continuation.

## 10 Transformations and valid controls

Meaning-preserving changes should leave the oracle answer unchanged under the frozen rule text. Candidate families include consistent renaming of non-operative identifiers, reordering independent fact sentences, and equivalent display of quantities with units preserved. A family is admissible only after a reviewer checks references, negation scope, entity roles, temporal order, exceptions and cross-references. If reordering changes what a pronoun refers to, it is not a valid invariant. Avoid replacing legally operative terms with casual synonyms merely because they sound similar.

Meaning-changing controls intentionally alter one legally relevant fact and require an independently derived new answer. For a civilian fee rule, a change that crosses a reviewed baggage-weight or count boundary can be a control only when the fee, inclusivity and any applicable exception are known from the actual pinned rule. For tax, use reviewed statutory boundaries and exact rounding. These are design categories, not claims that any particular benchmark case has already passed validation.

Threshold tests should include points just below, at and above the operative threshold where the rule supports them. Add paired exception-present and exception-absent cases and precedence tests only after confirming the rule hierarchy. These are changed-meaning tests; report them separately from sensitivity to irrelevant wording. A model that always returns the original answer might look stable under invariants but fail every valid answer-changing control.

Missing or conflicting facts belong in a separately labelled extended test. An absent premise does not automatically make a negative label correct. Specify whether the task permits an indeterminate result, assumes a closed world or requires an explicit request for clarification. For conflicting rules or facts, define the applicable priority or mark the oracle disputed. Do not mix these cases into published benchmark accuracy denominators without a declared new task definition.

Use deterministic transformation code with unit and property checks, a reversible change log and field-level diffs. Property tests can ensure entity-renaming bijections and unchanged quantities, but cannot prove legal equivalence. Preserve a human-reviewed sample per family and review every exceptional case. Cosmetic invariance supports only a narrow robustness claim; it does not establish broad semantic or legal competence.

## 11 Reproducibility and denominator protocol

Create a pre-run manifest containing every scheduled anchor, variant, condition and draw, including trusted expected labels outside the agent environment. Assign stable IDs and hashes before execution. Reconcile the full Cartesian schedule against output records even when a job produces no result file. All scheduled cases remain in the primary denominator; report successful completions as a secondary conditional metric only.

For each attempt distinguish correct, substantive wrong answer, malformed output or parser failure, tool failure, timeout, infrastructure failure and intentional abstention. An abstention must be recognizable under a predeclared response convention; a crash is not responsible uncertainty. Record reasons where observable without pretending to know model intent. Missing usage is unknown, not zero. Reconcile provider billing or usage exports when available, with unresolved usage visibly bounded.

Pre-register retry rules. For example, allow one infrastructure retry after an authenticated transport failure, retain both records and designate the original scheduled attempt as primary with a separate recovered-service analysis. Never retry only wrong answers. Do not use best-of-N or latest-only selection to summarize independent draws. Model-requested repair within a fixed harness budget is part of the declared configuration and its tokens count toward cost.

Report strict answer normalization and a separate normalization sensitivity analysis. Define permissible whitespace, currency symbols, integer/decimal equivalence and categorical aliases in advance. Do not broaden normalization after seeing errors. Published-style scoring, corrected all-scheduled scoring and semantic-error classification should be reported as different analyses; the difference can reveal measurement artifacts without redefining model performance after the fact.

For F1, derive the class universe and true labels from the schedule, not successful verifier text. Missing predictions must contribute failures for their known true class; unknown scheduled truth is a failed oracle gate. Report confusion matrices, class support, coverage and error categories alongside macro-F1. Keep numerical exact accuracy separate; a pooled cross-domain score must disclose weighting and should not conceal small-domain failures.

## 12 Statistics and interpretation

The unit of independence is not a response. All variants and repeated draws derived from one anchor share a base-case ID; cases can also share statutes or rule-source families. Treat each anchor's outputs as a bundle. For a finite public benchmark, report descriptive scores for exactly that fixed set and avoid suggesting that a confidence interval makes it representative of all legal reasoning tasks.

For stochastic uncertainty of a fixed endpoint, summarize repeated draws and paired configuration differences while preserving anchor bundles. For broader case-sampling uncertainty, use a cluster bootstrap that resamples anchors, or source families when dependence warrants it, carrying every variant, configuration and draw together. A hierarchical or multiway approach may be needed if rule families cross anchors. With few independent families, state that intervals are unstable and prefer descriptive reporting over false precision.

Primary endpoints can be baseline strict accuracy, paired accuracy loss under two invariant families, and changed-answer-control accuracy. Also report conditional flip rates among correctly answered baselines, distinguishing a flip to correct from a flip to wrong. Define each denominator explicitly. Three repeats estimate limited stochastic variation; they do not create three independent cases or adequately map every possible model trajectory.

Prespecify the confirmatory family of comparisons and use Holm adjustment or an appropriate familywise procedure across its hypothesis tests. Exploratory domains, alternate normalizations, subgroup analyses and discovered failure types should be labelled exploratory. Report effect sizes and cluster intervals even when adjusted tests are inconclusive. Choose a practically meaningful difference and minimum validated sample in advance; a power calculation must use plausible cluster variability, not the raw count of responses.

Public benchmark contamination is unavoidable as a possibility. Training exposure cannot be reliably inferred from a high score or disproved by simple renaming. Held-out transformations reduce direct string memorization but do not eliminate structural familiarity. Record publication dates, provider training disclosures where available, model changes and exemplar overlap. Private new civilian cases could improve novelty later, but require new oracle work and a separately scoped study.

A stable wrong answer is not robustness. A new failure should survive independent semantic review, repeated draws and a valid changed-answer control before becoming a headline example.

## 13 Automation architecture and provenance

Use a narrow pipeline: acquire and hash public inputs; validate schemas and oracle records; freeze a schedule; construct agent-safe inputs; execute authorized tasks; collect immutable outputs; independently score; analyze paired bundles; produce a claim ledger and report. Separate stages so a scorer update never silently changes the input schedule. Every derivative points to parent hashes and a transformation version.

Minimum case schema: study_id, source_revision, source_case_id, anchor_id, source_family_id, rule_family_id, split, input_hash, statute_hash, oracle_version, reviewer_decision, transformation_family and variant_id. Minimum run schema adds schedule_id, condition_id, model_request_name, returned_model_id, provider, harness_revision, image_digest, prompt_hash, exemplar_hashes, temperature, limits, seed if available, draw_id, attempt_id, timestamps and status.

Minimum outcome schema includes raw_output_hash, parsed_answer, normalized_answer, trusted_expected_label_reference, correctness, failure_category, abstention_flag, parser_version, scorer_version, token fields with unknown explicitly represented, monetary estimate and actual cost when known. Preserve tool traces and stderr when permitted; strip credentials and personal identifiers from public logs. Do not publish private system credentials, signed URLs or unnecessary case narrative.

Store raw records append-only. A journal records state transitions, retries and operator interventions. Validate counts by schedule ID at every stage; duplicate or missing IDs fail analysis. Keep original outputs separate from normalized answers and reviewer commentary. Publish concise machine-readable metadata and a reproducible analysis script, with dependency versions, while retaining sensitive or restricted raw material privately.

The engineer's valuable intervention is reviewing isolation, state transitions, denominator recovery and a small independent numeric checker. Automation can generate draft prose and summaries, but a human signs off on semantic labels, claims and publication. Use fixed templates to reduce operator load rather than allowing an autonomous agent to invent and revise the study design during execution.

Rebuilds should use a locked dependency environment and content-addressed container images. The inspected template uses a dated base image, unpinned apt packages and a remote install script piped to a shell; it was read but not executed. A historical build may be difficult to recreate exactly. A secure replacement build must be labelled as a changed implementation. [S10]

## 14 Isolation and fail safe cost controls

Do not run repository setup commands or model-generated programs on the researcher's normal workstation. First review the relevant scripts and dependency chain. Build a disposable environment with no personal credentials, home-directory mounts or access to the evidence archive. Give the model only the frozen civilian task inputs and permitted tools. Keep gold labels, reference programs and the evaluator in a separate process or environment inaccessible to the agent.

Generated Prolog and shell commands are untrusted code. Use a nonprivileged sandbox with CPU, memory, file, process and wall-clock limits; read-only rule inputs; a small output directory; and network disabled. The proposed offline checker should not load arbitrary predicates or files from generated programs. Review the sandbox before a paid pilot. This study did not execute those components.

Model network access, when later authorized, should be mediated by a separate gateway with credentials unavailable to the task sandbox. Permit only named provider endpoints and validated requests. Disable arbitrary web browsing, package downloads, outbound tools and remote command execution unless separately justified. A civilian rule task does not need an unrestricted network.

Require a maximum request count, per-request input/output limits, maximum agent turns, concurrency limit, wall-clock timeout and a total dollar cap enforced before dispatch. Reserve each request's worst-case cost atomically; reject dispatch if it would exceed the cap. Deduct measured charges afterward and keep reservations for unknown usage until reconciled. Provider budget dashboards are a second barrier, not the sole control.

Stop on missing gold labels, schema mismatch, endpoint changes, leaked grading files, unexpected outbound requests, unbounded token use or repeated infrastructure faults. A killed request may still be billed, so maintain contingency within the authorized cap. Do not auto-escalate to a more expensive model or retry indefinitely. Produce a machine-readable stop report and resume only after the specific fault has been reviewed.

No paid run or funding commitment is authorized by this feasibility study. A donor plan must be an explicit future proposal with the maximum spend and human review requirement visible before execution.

## 15 Personnel and achievable tiers

Tier 0 is a free technical feasibility package: preserve public artifacts, pin versions, inspect licenses, map paper claims to implementation, check scoring on synthetic inputs and document missing dependencies. It supports a bounded access and measurement story, not model capability conclusions. This study has completed those acquisition and code-inspection elements; container execution, model availability tests and broad scorer certification remain unperformed. A follow-on engineering review is estimated at 6-12 hours and researcher verification at 6-12 hours, depending on environment familiarity.

Tier 1 is the recommended 24-anchor numerical pilot. With a baseline, two validated invariant variants and one independently answer-changing control, there are four inputs per anchor. Two configurations and three draws yield 24 x 4 x 2 x 3 = 576 scheduled responses. There are only 24 anchor clusters, possibly fewer independent rule families. A second model doubles responses and cost, not the number of anchors.

Planning estimates for Tier 1: base-case derivations 6-12 hours; review of 72 variants 6-12 hours; independent second review of all 96 instances 8-16 hours; engineering 12-20 hours; analysis and reporting 8-16 hours. Total 40-76 hours, reasonably budgeted as 40-80 hours before difficult disputes or additional development. Add an estimated 6-12 hours for independent methodological/statistical review and 4-8 hours for post-analysis contextual review: roughly 50-100 hours overall, with disputed-output adjudication potentially requiring more. The existing independent case-review allocation covers the civilian semantic role; it must not be counted twice. These additional reviewer allocations are planning allowances, not confirmed access or unpaid commitments. These are estimates, not measured productivity. Role overlap must not erase the independent second review. The engineer need not perform all semantic work, but 12-20 engineering hours may already exceed a friend's availability.

Tier 2 extends to DAR's 173 anchors. The same design yields 173 x 4 x 2 x 3 = 4,152 responses per model, or 8,304 for two models. It may require 200-400 or more human hours because immigration interpretation, family validation and error adjudication scale unevenly. This exceeds the minor-intervention premise. Budget more conservatively if all five DeonticBench configurations or housing are added.

The low-personnel fallback is therefore honest: do a strong technical audit, then a smaller semantically defensible pilot. More tokens cannot replace answer validation. A donor-funded team is an option only after the access, oracle and consequence gates pass.

## 16 Transparent token and financial model

No fixed experiment quote is defensible before token measurement and an exact endpoint choice. For each condition, compute cost as (uncached_input_tokens x input_rate + output_tokens x output_rate + cache_write_tokens x write_rate + cache_read_tokens x read_rate) / 1,000,000, plus applicable tools, hosting, storage, tax and other charges. Count every agent turn, repair, failed billable attempt and repeated context. Define token categories so cached input is not charged again as uncached input in the estimate.

The official Anthropic pricing page was acquired on 17 October 2026. Its model table lists Claude Sonnet 4.5 base input at USD 3 per million tokens and output at USD 15 per million; the page also marks this model deprecated in a regional-pricing note. This is a price reference, not proof of callable availability or a commitment to use that historical endpoint. Cache writes, cache reads, long-context, residency and partner routes can have different charges. Recheck the exact route before authorization. The acquired OpenAI pricing URL redirected to a broader business pricing page; no numerical rate from it is used here. [S12, S13]

For illustration only, at USD 3 input and USD 15 output per million, an assumed average 10,000 uncached input tokens and 2,000 output tokens costs USD 0.06 per response. The 576-response pilot would be USD 34.56 in model tokens; 4,152 responses USD 249.12; 8,304 responses USD 498.24. These assumptions are not measured workloads. Agentic repeated context can multiply input cost dramatically, and output reasoning tokens may be separately reported or included in billed output.

A stress illustration at 50,000 input and 8,000 output tokens is USD 0.27 per response: USD 155.52, USD 1,121.04 and USD 2,242.08 for the same respective schedules. Neither illustration includes contingency, tools, hosting or people. Use the pilot's measured token distribution to update later tiers, with median, upper quantiles and maximum costs by condition.

If paid human rates are h_i and hours H_i, personnel cost is sum(h_i x H_i). Add that explicitly to a donor budget. An inexpensive API bill does not make a 200-hour study a low-cost solo project. No purchases, model credits or runs have been approved.

## 17 Adoption consequence and investment gate

TEELAWS has the strongest inspected evidence of actual use among the comparison targets: an Army article dated 23 April 2026 reports testing in West Point's PY201 course. The official SBIR award record lists Perceptronics Solutions, a Phase II award of USD 1,899,999 and an end date of 29 October 2026. The same record describes educational development. The classroom report establishes bounded adoption at that time; the scheduled award end is not evidence of renewal, continued use after that date or operational deployment. No executable TEELAWS package was verified. [S14, S15]

DARPA's ASIMOV page states that the program is complete and that the page is no longer maintained. Completion does not establish abandonment. The REBAR v1 paper, submitted 18 May 2026, describes a published demonstration and already reports weak protection of bystanders in the evaluated setup. Those weaknesses are the authors' own disclosed findings. Repeating them would not be a new discovery. No public executable REBAR release was verified through the paper and official page inspected; no claim of an exhaustive global repository search is made. [S11, S16]

For CODORD, official linkage and funding are established, while a public chain from benchmark scores to a specific consequential adoption decision is not established by this study. Seek public procurement deliverables, evaluation standards, training assessments, citations in acceptance documents or official claims tying particular metrics to an actual decision. These are document-research targets; institutional replies are not prerequisites for the civilian audit.

A large investment requires two separate go decisions. Scientific go: independently validated answers, viable isolated implementation, accessible exact endpoint, complete denominator and an authorized cap. Public-interest go: a concrete consequential claim that the tests actually address, plus plausible novelty beyond authors' published limitations. If only scientific go passes, frame the work as a reproducibility note or methods contribution and keep investment modest.

The audit cannot certify compliance with international humanitarian law, diagnose battlefield safety or establish unlawful conduct. Civilian rule tasks offer evidence about narrow rule-following and evaluation reliability. Military relevance should be expressed as a question about the evidentiary basis of assurance claims, with the missing validation bridge made explicit.

## 18 Counterarguments fair publication and deliverables

A fair objection is that the authors already describe low scores, nonuniform harness gains and limitations. The audit should acknowledge that prominently. Another is that corrected references may improve present artifacts without changing old outputs; the study must compare exact versions before drawing a connection. A third is that a harness artifact or formatting mismatch may explain a failure. Report the original behavior, strict scoring and normalization sensitivity separately, with minimal reproducing examples and all failed attempts retained.

Negative findings are valuable when they narrow a claim reliably: a corrected score may agree with publication; invariant variants may be stable; a missing artifact may be reconstructable; or a current model may improve. Pre-register these outcomes as publishable. Avoid framing access gaps as obstruction or assuming that every government-funded research artifact must have a particular public license.

Before eventual investigative publication, prepare a fair right-of-reply packet naming exact papers, versions, code paths, examples, denominators, uncertainty and proposed wording. Give authors and relevant institutions a reasonable response window, for example ten working days as an editorial proposal, and preserve corrections. Their participation is optional and silence is not confirmation. No outreach was performed for this feasibility study.

The feasibility deliverables are this matching Markdown and PDF, concise acquisition metadata and checksums, source counts, exact version pins, bounded synthetic scoring evidence and a reusable staged protocol. A future pilot should additionally release its preregistration, oracle decisions, transformation specifications, schedule, allowed public traces, failure ledger, independent scorer, analysis code and reproducibility instructions subject to licensing and privacy review.

Reusable newsworthiness criteria: a specific public claim; evidence of consequence; new independently verified findings; a meaningful effect size; valid controls; a link between the tested artifact and the claimed use; and fair treatment of counterevidence. All should be evaluated separately. A code path alone is a lead. A repeatable civilian failure is a result about that tested system. A claim about real-world harm requires additional evidence this design does not supply.

Decision today: publish this feasibility study, preserve the public evidence and seek only a narrow, capped pilot if independent semantic review can be staffed. No full audit, donor commitment, purchase, model run or outreach follows automatically.

## 19 Limitations and verification record

Verified in this work: two repository heads and their relevant contents; ten downloaded Parquet files and row counts; hard and smoke JSON counts; public pre- and post-correction hard files; three versioned paper PDFs; public program, award and classroom-use pages; the specific current scorer branches; and the bounded synthetic outputs. Raw source acquisition comprises 21 successful URL snapshots, plus ten pinned Parquet downloads. Repository clones and historical extracts are additional evidence objects and are counted separately. The reference list below has 16 primary-source entries; some entries aggregate metadata endpoints and pinned code files from one source family.

Not verified: historical raw trial logs, dedicated DAR checkpoints, complete original training artifacts, exact original runtime images or service snapshots, endpoint availability through an authenticated inference request, effects of scoring behavior on published tables, independent correctness of the benchmark corpus, a military deployment chain, TEELAWS renewal or a public executable package for TEELAWS/REBAR. No experiment supports a model-performance estimate in this feasibility report.

Absence statements are scoped to the named repository trees, paper references and official pages inspected on 17 October 2026. The repository's generated datasets are untracked but public adapters make current reconstruction plausible. A later artifact release can change feasibility. Current pricing and status pages can change independently of the code and paper versions.

The synthetic check is deliberately tiny and cannot certify all evaluator paths. It excludes Kira's evaluator, parser fuzzing and publication-log reconstruction. Parquet reading and JSON counting establish acquisition and structure; they do not establish semantic validity or safe execution of included Prolog. No imported benchmark code was executed wholesale.

This revised edition adds a prospective scientific-review structure; no expert review has yet occurred. The source cutoff and acquisition findings are unchanged. PDF quality assurance covers full-page rendering, visual page review, text extraction, hyperlink annotations, page boundaries and content parity against the Markdown authoring source. Publication verification covers the exact remote commit and file links. Those mechanical checks cannot independently validate the proposed legal interpretations, which remain an explicit gate for any later experiment.

Local raw evidence is retained outside the publication repository under /workspace/ihl-evidence, with checksums and acquisition metadata. The published evidence manifest omits local machine paths. The repository publication is confined to research/2026-10-17/ihl-audit-feasibility/ and preserves unrelated work.

## Primary sources

All sources accessed 17 October 2026 UTC. Pinned paper versions and repository revisions are specified below. Live institutional pages are archived locally by checksum; see evidence-manifest.json.

- **S01** DeonticBench paper v1. 6 April 2026. [https://arxiv.org/abs/2604.04443v1](https://arxiv.org/abs/2604.04443v1) | [https://arxiv.org/pdf/2604.04443v1](https://arxiv.org/pdf/2604.04443v1)

- **S02** DAR paper v1. 3 June 2026. [https://arxiv.org/abs/2606.05009v1](https://arxiv.org/abs/2606.05009v1) | [https://arxiv.org/pdf/2606.05009v1](https://arxiv.org/pdf/2606.05009v1)

- **S03** DARPA CODORD official page. Live page acquired 17 October 2026. [https://www.darpa.mil/research/programs/codord](https://www.darpa.mil/research/programs/codord)

- **S04** RTX DONATELLO award announcement. 28 August 2025. [https://www.rtx.com/news/news-center/2025/08/28/rtx-bbn-technologies-to-empower-ai-to-understand-and-apply-regulatory-legalese](https://www.rtx.com/news/news-center/2025/08/28/rtx-bbn-technologies-to-empower-ai-to-understand-and-apply-regulatory-legalese)

- **S05** DeonticBench pinned repository. Head dated 4 June 2026. [https://github.com/guangyaodou/DeonticBench/tree/3c168f943880fcbd3a3d717a516500312534273b](https://github.com/guangyaodou/DeonticBench/tree/3c168f943880fcbd3a3d717a516500312534273b)

- **S06** Harbor DeonticBench pinned repository. Head dated 5 June 2026 UTC+08. [https://github.com/guangyaodou/harbor-deonticbench/tree/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1](https://github.com/guangyaodou/harbor-deonticbench/tree/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1)

- **S07** Hugging Face pinned dataset and card. Revision acquired 17 October 2026. [https://huggingface.co/datasets/gydou/DeonticBench/tree/805fb0529d7ae295679c5c1730765ec07d2c20ac](https://huggingface.co/datasets/gydou/DeonticBench/tree/805fb0529d7ae295679c5c1730765ec07d2c20ac) | [https://huggingface.co/datasets/gydou/DeonticBench](https://huggingface.co/datasets/gydou/DeonticBench)

- **S08** May reference correction and predecessor. 26 May and 26 April 2026. [https://github.com/guangyaodou/DeonticBench/commit/c6e3fe749a200fbfe1d78622968d33e4f6cec31d](https://github.com/guangyaodou/DeonticBench/commit/c6e3fe749a200fbfe1d78622968d33e4f6cec31d) | [https://github.com/guangyaodou/DeonticBench/commit/e2516e32ab4f86e63ba4046d8549dd58a7d992a0](https://github.com/guangyaodou/DeonticBench/commit/e2516e32ab4f86e63ba4046d8549dd58a7d992a0)

- **S09** Pinned root scorer. Current code acquired 17 October 2026. [https://github.com/guangyaodou/harbor-deonticbench/blob/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1/evaluate_deonticbench.py](https://github.com/guangyaodou/harbor-deonticbench/blob/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1/evaluate_deonticbench.py)

- **S10** Pinned direct adapter build template. Current code acquired 17 October 2026. [https://github.com/guangyaodou/harbor-deonticbench/blob/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1/adapters/deonticbench_direct/template/environment/Dockerfile](https://github.com/guangyaodou/harbor-deonticbench/blob/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1/adapters/deonticbench_direct/template/environment/Dockerfile) | [https://github.com/guangyaodou/harbor-deonticbench/blob/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1/adapters/deonticbench_direct/adapter.py](https://github.com/guangyaodou/harbor-deonticbench/blob/2fe3aa40bf856d533a79a6052a28eb3fc1b618f1/adapters/deonticbench_direct/adapter.py)

- **S11** REBAR paper v1. 18 May 2026. [https://arxiv.org/abs/2605.18423v1](https://arxiv.org/abs/2605.18423v1) | [https://arxiv.org/pdf/2605.18423v1](https://arxiv.org/pdf/2605.18423v1)

- **S12** Official Anthropic model pricing. Live page acquired 17 October 2026. [https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)

- **S13** Official OpenAI API pricing route. Live page acquired 17 October 2026; redirected. [https://openai.com/api/pricing/](https://openai.com/api/pricing/) | [https://openai.com/business/pricing/#api](https://openai.com/business/pricing/#api)

- **S14** Army report of TEELAWS PY201 testing. 23 April 2026. [https://www.army.mil/article/291926/cadets_work_with_software_using_lethal_autonomous_weapons_systems_that_analyzes_tactical_decisions_provides_ethical_score](https://www.army.mil/article/291926/cadets_work_with_software_using_lethal_autonomous_weapons_systems_that_analyzes_tactical_decisions_provides_ethical_score)

- **S15** Official TEELAWS award 215327. 2025 award; scheduled through 29 October 2026. [https://www.sbir.gov/awards/215327](https://www.sbir.gov/awards/215327)

- **S16** DARPA ASIMOV official status page. Live page acquired 17 October 2026. [https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values](https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values)
