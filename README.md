# Finding reporting questions in public records

Public records can offer more leads than a journalist has time to read. This notebook explores small, affordable ways to choose what deserves a closer look—with spreadsheets, search and sometimes AI. You do not need to code to follow the accounts or try their basic recipes.

The most complete trial ranked 1,234 Canadian access-to-information request summaries, checked ten shortlisted topics and obtained one seven-page release. It identified two specific files worth reading next, **not a verified scoop**. Estimated model usage and reported search costs totalled **about 18 US cents, excluding setup and reporting time**. The useful result was a clearer next reporting step, including knowing when to stop.

## Choose a recipe for your beat

- **Find the next document to read.** The [Canadian ATI experiment](experiments/07-canadian-ati.md) turns short request summaries into choices: obtain a named file, sharpen a question, or recognize that the story is already covered. Try it when an index is much larger than your reading time.
- **Check names without jumping to conclusions.** The [contracts-and-sanctions experiment](experiments/01-ofac-baseline.md) reduced millions of transactions to thirteen candidate pairs. Its strongest example shows why the action behind a match matters as much as the name. The [NAI follow-up](research/2026-10-14/nai-contract-history/README.md) reconstructs orders, modifications and the original termination notice; the lead was parked for editorial prioritization on 14 October 2026.
- **Separate foreign-agent overlaps from disclosure violations.** The [FARA / federal-awards pilot](research/2026-10-14/fara-award-pilot/README.md) screened the complete FY2025 prime-contract archive for $0. Canadian Commercial Corporation dominates the corroborated action count; no disclosure violation was established, and grants/Canadian procurement remain incomplete.
- **Trace an AI capability from funding to a physical test.** The [F2 tactical-AI investigation](research/2026-10-24/f2-tactical-ai/README.md) screened 712,186 selected financial transactions and developed three conditional reporting dossiers. It separates vendor claims, exact awards and test evidence, preserving unresolved funding links, prior coverage and reproducible screening code.
- **Test whether your search works.** The [missed known news story](experiments/03-headline-filter.md) offers a simple recipe: check an article you already know exists before trusting an empty search. No result does not mean no earlier reporting.
- **Give a promising paragraph more context.** The [Enron filings](experiments/08-enron.md) and [bank-lending surveys](experiments/09-bank-lending.md) show how connected records and careful arithmetic can produce better questions—and catch misleading ones.
- **Stop when a company network does not produce a story.** The [Tuscany company-records review](research/2026-10-22/tuscany-corporate-records/README.md) extracted ownership and lending facts from eleven filings but established no consequential new finding. Parked on 22 October 2026; it records an editorial stopping rule and the limits of the extraction result.
- **Explore a new source.** Browse the [Rabbit catalog reference](catalogs/README.md), then use the [public-source trial](experiments/02-public-source-pilot.md) to check a few records before investing in a bigger collection.

Some trials use **Jev**, a model service that ranks or assesses text, and **Exa**, a search service for finding possible earlier coverage. Their [ten-lead contract trial](experiments/06-jev-exa.md) shows why the original records and search results must accompany a dashboard.

- **Check whether an activity indicator survives a backtest.** The [institutional-activity pilot](research/2026-10-15/institutional-activity/README.md) tested free Pentagon-area Metro counts against Iran and Venezuela operations. Neither scored Iran window flagged; Venezuela was unscorable. It preserves the negative result, code, data and lessons about publication delay, controls and misleading ratios.

## Try something small, and keep what you learn

Start with [the reporting recipe](docs/method.md) and [blank run record](templates/run.md), or browse [all ten experiments](experiments/README.md). Each account explains the question, source, steps, results, costs and next useful move.

The emerging [DATA1 + RULE + DATA2 method](docs/rule-based-source-comparisons.md) offers five small options for discovering rule-grounded connections from existing source descriptions. It proposes a bounded pilot; no full Rabbit parsing or new experiment has started.

**What we still need to learn:** whether these methods save reporter time or find better questions than simple rules. Early trials have missing evidence, and historical examples benefit from hindsight. Read the [costs and limits](docs/costs-and-limitations.md), [correction history](research/2026-10-01/ati-live/correction-identity.md) and [unfinished work](docs/next-steps.md) alongside the results.

[Technical annexes](annexes/README.md) preserve the detailed reports, prompts, code and evidence for anyone who wants to check or adapt the work.

Notebook updated 1 October 2026; NAI follow-up and FARA/federal-awards pilot added 14 October 2026; institutional-activity pilot added 15 October 2026; Tuscany company-records review added 22 October 2026.

