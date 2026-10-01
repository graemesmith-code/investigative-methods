# Finding reporting questions in public records

A notebook for journalists who want to try small, affordable experiments with public records, search and AI. Start with a question you understand, keep the original evidence, and judge the result by whether it helps a reporter decide what to read next. You do not need to code to read these accounts or try their basic recipes.

This is a record of experiments, including failures and unfinished work. It has **not** established a reliable scoop-finding service or shown that AI outperforms a reporter using simple rules.

## Choose a starting point

- **See the most complete trial:** [Canadian access-to-information summaries](experiments/07-canadian-ati.md). We ranked 1,234 request summaries, checked ten shortlisted topics and obtained one seven-page release. Two specific files were worth obtaining next; no new allegation was verified.
- **Learn from a simple check:** [Contracts and sanctions names](experiments/01-ofac-baseline.md). Millions of transactions became 13 name matches. The strongest example recorded a contract termination with no new money committed, not a prohibited payment.
- **Understand what search can miss:** [A missed known news story](experiments/03-headline-filter.md) and [the ten-lead Jev/Exa trial](experiments/06-jev-exa.md). An empty result is not evidence that a story is unreported.
- **Try reading connected documents:** [Enron filings](experiments/08-enron.md) and [bank lending before 2008](experiments/09-bank-lending.md). These are exercises in reading and checking historical records, not demonstrations of predicting scandals.
- **Choose a source for your beat:** [Rabbit catalog reference](catalogs/README.md), alongside the [small public-source access trial](experiments/02-public-source-pilot.md). A catalog entry is an invitation to test a source, not a promise that access works or that it contains a story.

[All experiments, dates and evidence status](experiments/README.md) · [A recipe for your own experiment](docs/method.md) · [Blank run record](templates/run.md)

## What has proved useful so far

Keeping the actual record beside the proposed question makes mistakes easier to catch. In the ATI trial, an existing article led to the exact mental-health policy release: the useful decision was to stop pursuing an already-covered claim. Another lead named a ten-page Nanisivik compliance file, but public background did not prove that the order caused the facility's closure. The missing file mattered more than more general searches.

What has **not** been demonstrated is a dependable success rate, the number of important records missed, or savings in reporter time. Several early prototypes lack the original inputs and search logs. The historical tests were chosen with hindsight. The later ATI trial preserved much more evidence, but still has no matched comparison against simpler selection methods.

## Costs and corrections belong beside the results

The ATI run recorded **USD0.061954 in estimated Jev usage across 1,402 calls**, plus **USD0.119 reported by Exa across 17 searches**. Their sum, USD0.180954, excludes unmeasured labour and is not an audited invoice or full project cost. Earlier contract-ranking costs remain unknown. The requested OpenAI comparison was blocked on a missing key **before any API call; USD0 and no comparison result**. [Costs and limits](docs/costs-and-limitations.md).

**ATI correction:** ten model assessments for one lower-ranked medical-fairness check used the wrong department's summary. Those assessments and the previous conclusion are invalid; a corrected rerun is pending. All ten shortlisted topics retain their checked identities. [Correction and preserved history](research/2026-10-01/ati-live/correction-identity.md).

## Read, check, then adapt

Each experiment starts with its question, what the source can tell you, a recipe, results and the next useful step. **Inspected evidence** means a saved file was checked; **reported result** means the full supporting logs are missing; **proposal** means it has not been tested. None of these labels makes a lead a finding ready to publish.

[Technical annexes](annexes/README.md) hold the longer reports, prompts, code, accounting and reproduction instructions. Code and machine-readable evidence stay at their established paths so existing scripts continue to work. The repository remains private; this edit changes neither access nor licensing.

Updated 1 October 2026. Source dates and the limits of each historical run are recorded on its page.
