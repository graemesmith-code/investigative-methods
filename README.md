# Investigative methods notebook

## Canadian ATI experiment — completed live run

[Read the findings and human handoffs](research/2026-10-01/ati-live/report.md): 1,234 request summaries scored, 17 targeted Exa searches, five follow-up branches, and one seven-page release obtained. Two document-acquisition priorities survived; no new allegation was verified. Combined recorded usage was USD0.180954, not an audited tax-inclusive bill. [Results and evidence index](research/2026-10-01/ati-live/README.md) · [Live-tested code and tests](code/ati/README.md). This archive excludes credentials and full third-party news text.


We are testing cheap ways for journalists to find public records worth reporting. The goal is a method another reporter can copy, measure and improve. A promising lead is a question to investigate, not a finding to publish.

**What we tried:** compare contracting records with sanctions names; test public defence feeds; filter contract headlines; check news-provider retrieval; rank original contract paragraphs; search the highest-ranked leads for earlier coverage.

**Why:** public records are abundant, but newsroom time is scarce. A useful method should save review time while keeping important records visible.

**What happened:** the sanctions baseline produced 13 name-based candidate pairs and established no violation. The public-feed pilot preserved usable samples from nine source families. Two prototypes were published historically. The latest Exa export records ten leads, nine possible coverage matches and one with no clear match in its results; it does not preserve the articles needed to verify those labels.

**What it cost:** the sanctions run used no paid data or model calls. Actual total costs, including human time, were not recorded. Actual per-run Jev and Exa bills are missing. We cannot yet claim a measured cost per useful lead.

**What remains uncertain:** whether model ranking improves on simple rules, whether searches recover known coverage reliably, and whether these prototypes consistently produce worthwhile assignments. Several runs are documented only through reported results.

**Why it matters:** a reproducible failed test can be valuable. Missing a known article teaches us to repair retrieval before interpreting silence as novelty. A zero-dollar contract termination teaches us to read the action before treating a name match as wrongdoing.

## Overnight research

[What old scandals teach us about finding the next story](research/2026-10-01/README.md) — a plain-English report on the Enron and pre-2008 tests, choosing data sources, and a sharper Jev → coverage → evidence loop. Includes completed small tests, reproduction files and clearly marked next experiments.

## Start here

- [Experiments and evidence status](experiments/README.md): six readable accounts of what we know.
- [How the method works](docs/method.md): collection, screening, search and editorial review in ordinary language.
- [Run template](templates/run.md): record a new experiment without losing its evidence.
- [Evidence inventory](evidence/README.md): what is included, how it was selected, and what is missing.
- [Costs and limitations](docs/costs-and-limitations.md): distinguish actual spending from estimates.
- [Next steps](docs/next-steps.md): repair evidence capture, then compare methods on the same records.
- [Technical reproduction](docs/reproduction.md): supporting code and prerequisites.

## How to read claims

**Inspected evidence** means a file in the supplied evidence was opened and checked when this notebook was prepared. **Reported result** means the run or outcome was described but its full logs are absent. **Proposal** means work still to do. **Missing evidence** means a conclusion cannot presently be verified. Publication of a prototype is not proof that it works today.

This notebook was prepared on 30 September 2026 from selected September research. It covers professional journalism methods. No story allegation, outreach or new paid run is authorised by a notebook entry. Technical details follow the English explanation on each experiment page, so no programming knowledge is needed to read the results.
