# Nine-case feasibility and selector pilot: no surviving leads

All nine frozen cases received a bounded first pass. **Seven are indeterminate and two blocked. No complete investigative test produced a null, falsified lead or surviving lead.** Two limited subchecks were negative: no indexed 2023 contract transaction for the queried recipient identifiers (R01), and a signing press release's spending-limit assertion matched the law (N04). These are not completed sanctions-compliance or personal-statement tests.

This is a feasibility and selector pilot, **not an efficiency comparison**. It does not establish that the six editorially high-ranked formulations outperform the three random formulations. All nine cases were chosen by the model within those formulations, with familiar examples and prior work disclosed. Formulation selection is reproducible; case discovery was not an unbiased automated sample.

| Case | Arm | What happened |
|---|---|---|
| R01 — sanctioned supplier / US contracts | High | Indexed 2023 query empty; historical positive control worked. Full sanctions question indeterminate. |
| B02 — duplicate aid reimbursement | High | Audit OCR accessible, but aggregate amounts cannot establish duplicate costs. Audit-selection deviation. |
| Q03 — sovereign guarantee disclosure | High | Report PDF exceeded our artificial 1.5 MiB body cap; no guarantee selected. Blocked. |
| X03 — waste recipient authority | High | Facility and reporting forms accessible; recipient schema unresolved. Indeterminate. |
| X11 — participant overlap in medical review | High | Title selector picked a correction notice; article route also returned CAPTCHA. Indeterminate. |
| Z01 — changed quantities and bid ranking | High | Project inspection OCR lacked rival rates and quantities; document-selection ambiguity. Indeterminate. |
| N04 — enacted law versus statement | Random | Institutional signing press release matched section 101 on spending limits; personal-statement eligibility unresolved. Indeterminate. |
| N06 — intelligence release differences | Random | CIA routes returned homepage; archive PDF exceeded artificial cap. Blocked. |
| R04 — sanctioned person's PSC record | Random | First five official search results supplied no qualifying company/PSC record. Indeterminate. |

**49 charged search/retrieval attempts, $0 new paid external spend.** The recorded per-case spans range from about one to thirteen minutes, but overlap, include waits, and sometimes begin at return-time logging. They must not be summed or described as measured active effort. Allowing a conservative extra minute before each first log still leaves each under the 15-minute wall bound. There was no active-time telemetry. Setup, reasoning, code, review and packaging are additional work. The last user-reported weekly balance was **76% at 13:38 UTC October 6**; no weekly meter or attributable task-drain measurement is available.

## What this pilot actually taught us

Retrieving a document is not enough: the required invoice, recipient, historical authority, cohort or rival-rate detail may be absent. HTTP 200 can mean a challenge, homepage redirect, or an API response that ignored an attempted join. These failures are preserved in `evidence/content-validation.json`.

Several preselection rules were too ambiguous or weak to produce an eligible starting record. B02 is explicitly a selection deviation: the initial API returned zero documents, then two searches produced an audit without preserving the complete candidate frame needed to prove the frozen lexicographic rule. Z01's inspection report may fit a broad implementation interpretation, but the eligible-document ordering was not established. X11's title rule admitted a correction. R04's generic register search was not a usable historical PSC candidate frame. N04's institutional press release is not demonstrated to be the personal presidential statement named in the protocol. None was quietly replaced.

The 1.5 MiB limit was imposed by this experiment. It is **not evidence that ordinary reporters cannot cheaply obtain these PDFs**. Q03 and the archive half of N06 may become accessible simply by permitting larger individual files in a separately registered pass. B02 and Z01 publisher OCR was available within the cap. For truncated responses only a lower bound of 1,572,865 bytes is measured; full sizes were not acquired. CIA's 29.32 MB figure is catalog-reported, not measured here.

The ranking scores are editorial judgments about conditional consequence. Their short rationales mostly restate card titles; they do not establish empirically calibrated differences. X03 and X07 tied at 15 in the same editorial `environment` family; lexicographic ID order selected X03. A different defensible family taxonomy or tiebreak would change the six. The 15 refinement attachments are loose operational sampling buckets, not proof that 55 primary cards semantically cover all 70 detailed cards. They had zero extra lottery weight.

## Audit and deviations

The freeze was committed before retrieval at [c615758](https://github.com/graemesmith-code/investigative-methods/commit/c6157582afeab0c7927af086eda39ffaa0dd6de8). The immutable protocol, nine-file hash manifest, 55-row scores, seeded 49-candidate random draw and 15 refinement exclusions remain unchanged. Independent parent review reproduced the selection and confirmed freeze-before-retrieval.

The acquisition log retains failures and provisional closes. X03 initially stopped at five attempts, then resumed the same case within its original wall window after review; the final count is 11, not an exhausted 12. Its attempted joined endpoint returned exactly the same bytes as the reporting-form endpoint. Remaining cases sometimes overlapped in batched acquisition, departing from the protocol's sequential-block wording. Because each case stayed within its original wall window, this did not expand its allowance; it prevents treating the spans as independently measured active costs. One administrative `resume` entry was corrected from one charged retrieval to zero, with the correction recorded. No shared original was actually used to decide two test outcomes; R04 stopped before needing R01's OFAC page.

Some web-tool searches and original-page views are preserved as timestamped URL/query observations rather than raw snapshots. Not all candidate lists are recoverable from the repository; this is an evidence limitation, particularly B02. Saved original HTTP bodies have hashes; their semantic verification is separate from successful transport. No security settings were weakened. The five quarantined October 4 browser observations were not used. No new paid API, credentials, outreach or bulk execution was used.

## Download and reproduce

Download `checkpoints/cross-family-trial-first-pass.zip` from this private repository (GitHub sign-in required). It contains the readable report, CSV/JSONL outcomes, frozen selection, original small responses, code and audit logs. `results.jsonl`/`results.csv` include each case's observation, ordinary explanations, gaps, stop reason, attempts and next cheapest check. `progress-ledger.json` gives the honest counts.

Run `python code/validate.py` from any directory to validate freeze hashes, draw, outcomes, cost accounting and saved-response hashes. `code/build_results.py` rebuilds the result tables from the frozen rows, attempt log and explicit editorial outcome definitions; it makes no network calls. `code/fetch.py` is the bounded acquisition helper, not permission to rerun this closed pilot.

No first-pass case remains open. A second pass could repair selectors, validate the EPA schema and allow larger same-case PDFs, but should be declared separately and retain these failed first-pass results. It has not been run or folded into these outcomes.
