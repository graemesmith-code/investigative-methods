# Offline news-salience pilot

Status: preparation complete; genuine human labels absent; performance unmeasured.
No inference calls, credentials, model downloads or paid services are needed. Python 3.10+,
standard library only. Work from the repository root:

```sh
python research/2026-10-08/news-salience/benchmark.py prepare
python -m unittest discover -s research/2026-10-08/news-salience -p 'test_*.py' -v
python research/2026-10-08/news-salience/benchmark.py evaluate --labels /path/to/completed-labels.csv --out /path/to/report.json
```

Preparation reads the existing `research/2026-10-01/ati-live/calibration-ranked.json`,
`calibration-ids.json` and `ranking-prompt.json`. It validates exact membership of 100
records and the original department counts (36 Global Affairs Canada, 64 National Defence).
The original files remain unchanged. Source hashes and inspected GitHub blob identifiers
are recorded in `packet/coordinator/manifest.json` and `inspection-provenance.json`.

## What this tests

Can the existing cheap Jev ranking help an editor select worthwhile follow-up questions
from access-to-information request summaries, beyond transparent text and metadata rules?
It does not test whether allegations are true or whether a trained prominence model works.
Do not treat the topic named in a request as an event that occurred. `NE` means no records
exist; it does not establish the allegation or proposed policy. `DA` is disclosed in full,
`DP` disclosed in part, `EX` all exempted, `EC` all excluded. Positive page counts do not
mean this benchmark has obtained the disclosed documents.

| Construct | Meaning here | Existing information |
| --- | --- | --- |
| Follow-up priority | Human decision to invest reporting effort | Blank human labels; Jev composite is a candidate ranking |
| Public significance | Potential consequence if the question warrants investigation | Jev consequence is a proxy, not verified impact |
| Novelty | Newness relative to a documented prior public account | No valid novelty labels; do not use specificity or missing coverage as a substitute |
| Evidence strength | What the material actually supports | Request summaries only; Jev evidence score measures next-comparison potential |
| Editorial prominence | Observed position of a linked published article | No placement or linked-article dataset in this sample |

The saved Jev composite weights consequence 0.4 and specificity, evidence-comparison
potential and reporting question 0.2 each. All components remain separately evaluable.
They are not trained prominence predictions or calibrated probabilities. Confidence is
not evidence of accuracy.

## Blinded labeling procedure

1. A coordinator freezes this version before any labeling. Give reviewers only this rubric
   and `packet/reviewer/records.csv` plus a fresh copy of `labels.csv`. Do not share the
   coordinator folder, original ranked files, scripts, prior calibration review or this
   repository browsing session. The coordinator should not serve as the independent rater.
2. Review all 100 records in their shuffled order. Identifiers are reassigned independently
   of scores; summaries in both languages and ordinary source metadata remain visible.
   Use a Canadian national investigative desk as the common audience. Assume a short
   initial desk check is feasible; document any specialist knowledge that changes a label.
3. Enter your reviewer ID and a short rationale for every record. Score each dimension
   separately. Leave unknowable novelty and observed prominence blank or `unknown`.
   These missing values are not zeros. No external searches are needed for initial
   follow-up/significance labels. Do not fabricate a novelty assessment from memory.
4. Prefer two independent editors. Compare their labels and reasons while still blinded;
   preserve both original files. Create a separate adjudicated file with a single consensus
   reviewer ID after resolving disagreements. The evaluator processes one complete rater
   or consensus file at a time; it does not silently average raters or calculate agreement.
5. Only after labels are frozen should the coordinator evaluate and inspect low-ranked
   positives. Evaluate independent raters too to see whether the result depends on one
   editor. Keep labels private unless their publication has been agreed.

| Label | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| followup | No useful follow-up apparent | Park; broad or costly question | Worth a bounded desk check | Priority check; concrete consequential question |
| significance | Trivial or private interest | Limited institutional interest | Material policy, money, service or safety stakes | Potential serious harm, rights or major public expenditure |
| evidence_strength | Request wording alone, no substantive support | Specific document described but unseen | Obtained material supports a bounded fact | Independent corroboration supports that fact |
| novelty | Already established in cited prior account | Minor increment | Material new detail | Changes the prior public account |
| prominence | Linked article in low prominence position | Section or ordinary placement | Front page or prominent homepage position | Lead position |

Evidence labels must reflect what the reviewer has actually seen: all summaries may
reasonably receive 0 or 1. Record obtained-document references in `evidence_basis` for 2/3.
Novelty requires `novelty_basis` describing dated prior coverage and the added fact.
Prominence requires `prominence_basis` with outlet, publication/capture date, article link,
record-to-article link evidence and exact page/position. The coarse bins above are optional
ordinal analysis conventions, not equivalence between a homepage and print A1/A16. Keep
print and homepage samples separate in any later prominence experiment. A record with no
known article is `unknown`, not low prominence.

The optional 30-record starter packet mixes 10 top records, 10 randomly chosen ranks
11–80 and 10 randomly chosen bottom-quintile records. Its order and fields conceal bands.
Use it to check rubric clarity or spread the work across sessions, then complete the other
70. It oversamples the extremes and cannot estimate overall recall. Starter provenance
is available only to the coordinator. Do not use it to tune the frozen baseline; a later
rules version needs a new untouched evaluation sample.

## Baselines and evaluation

`rules_text` counts four predeclared bilingual pattern groups once each across both
summary fields: harm/rights (2), accountability (2), money/decisions (1), and a specific
date/document identifier (1). Accent folding supports the French field. Regex and weights
are in code and the manifest. This is a modest, imperfect ordinary-rules comparator.
It can overreward emotive requests and miss synonyms; no claimed optimal baseline.

`rules_availability` gives one point for DA/DP with positive pages plus a capped log-page
term (at most 0.5). `rules_combined` adds text and availability. The latter two are
acquisition heuristics, not evidence truth or public significance. All three are compared
with the saved composite and four saved components. Score ties use source ID ascending;
the many rule ties can influence top-k selection. Review sensitivity before drawing a
strong conclusion; this scaffold does not estimate statistical uncertainty.

Default target is `followup`. `--axis significance` etc. evaluates other constructs
separately; never combine human axes into one supposed ground truth. Every record must
have a valid 0–3 label for the requested target, reviewer ID and rationale. Unknown or
partial labels fail clearly, so neither blanks nor the starter become negatives.
Novelty/prominence labels require their external basis. The evaluator reports:

- Precision and recall at 10 and 20, with positive defined in advance as human label >=2.
- Normalized discounted cumulative gain at 10 and 20, using ordinal gain `2^label - 1`.
- Separate within-department rankings with their own denominators.
- All human-positive records in Jev's bottom 20, for potential false-negative review.

Use `--k 5 10 20` for other predeclared desk budgets. Undefined recall (no positives) or
normalized gain (all zeros) returns null, not a success score. Metrics describe this
100-record pilot, not the full 1,234-record corpus. There is no statistical superiority
test, no accuracy of factual claims and no inference about future datasets. Inspect
disagreements and near ties as well as aggregate numbers. A useful signal would find more
worthwhile questions at the same review budget with acceptable missed leads, consistently
across raters. Record human time and any subsequent acquisition costs outside these metrics.

## Completed versus blocked comparisons

| Comparison | Current state | Additional requirement |
| --- | --- | --- |
| Input membership, department strata, saved score completeness | Completed on existing files | None |
| Frozen rules ranking versus saved Jev ranking | Both rankings available for inspection | Editorial labels for usefulness judgment |
| Jev/rules top-k yield, recall, ordinal ranking quality | Runnable; no results claimed | Complete genuine labels for one target |
| False negatives in bottom Jev quintile | All 20 queued in full packet; 10 in starter | Independent follow-up/significance labels |
| Inter-editor consistency | Procedure supplied; no agreement results | Two independent completed files and comparison/adjudication |
| Actual novelty or substantive evidence | Not established by this sample | Dated coverage review and obtained release material |
| Print A1-versus-A16 or homepage placement learning | Not runnable from available data | Linked article/record examples, dated layout/page evidence, labels and held-out split |
| Generalisation or trained cheap-model advantage | Not measured | New independently sampled holdout; training material if fine-tuning |

See `spangher-code-review.md` for what can be reused from the research code and what is
missing. `packet/status.json` deliberately contains no performance metrics. Fixture tests
use synthetic labels only; their successful execution is software validation, not a
benchmark result.
