# Finding reporting questions in public records

Public records can offer more leads than a journalist has time to read. This notebook explores small, affordable ways to choose what deserves a closer look—with spreadsheets, search and sometimes AI. You do not need to code to follow the accounts or try their basic recipes.

The most complete trial ranked 1,234 Canadian access-to-information request summaries, checked ten shortlisted topics and obtained one seven-page release. It identified two specific files worth reading next, **not a verified scoop**. Estimated model usage and reported search costs totalled **about 18 US cents, excluding setup and reporting time**. The useful result was a clearer next reporting step, including knowing when to stop.

## Choose a recipe for your beat

- **Find the next document to read.** The [Canadian ATI experiment](experiments/07-canadian-ati.md) turns short request summaries into choices: obtain a named file, sharpen a question, or recognize that the story is already covered. Try it when an index is much larger than your reading time.
- **Check names without jumping to conclusions.** The [contracts-and-sanctions experiment](experiments/01-ofac-baseline.md) reduced millions of transactions to thirteen candidate pairs. Its strongest example shows why the action behind a match matters as much as the name.
- **Test whether your search works.** The [missed known news story](experiments/03-headline-filter.md) offers a simple recipe: check an article you already know exists before trusting an empty search. No result does not mean no earlier reporting.
- **Give a promising paragraph more context.** The [Enron filings](experiments/08-enron.md) and [bank-lending surveys](experiments/09-bank-lending.md) show how connected records and careful arithmetic can produce better questions—and catch misleading ones.
- **Explore a new source.** Browse the [Rabbit catalog reference](catalogs/README.md), then use the [public-source trial](experiments/02-public-source-pilot.md) to check a few records before investing in a bigger collection.

Some trials use **Jev**, a model service that ranks or assesses text, and **Exa**, a search service for finding possible earlier coverage. Their [ten-lead contract trial](experiments/06-jev-exa.md) shows why the original records and search results must accompany a dashboard.

## Try something small, and keep what you learn

The [mining disclosure study](research/2026-10-12/mining-cross-government-disclosures/README.md) preserves ten cross-government company-statement pairs, the full comparison methodology and an unresolved Fekola dividend lead. Access tests and consistent controls are kept separate from proven contradictions; none has yet been established to publication standard.

Start with [the reporting recipe](docs/method.md) and [blank run record](templates/run.md), or browse [all ten experiments](experiments/README.md). Each account explains the question, source, steps, results, costs and next useful move.

**What we still need to learn:** whether these methods save reporter time or find better questions than simple rules. Early trials have missing evidence, and historical examples benefit from hindsight. Read the [costs and limits](docs/costs-and-limitations.md), [correction history](research/2026-10-01/ati-live/correction-identity.md) and [unfinished work](docs/next-steps.md) alongside the results.

[Technical annexes](annexes/README.md) preserve the detailed reports, prompts, code and evidence for anyone who wants to check or adapt the work.

Updated 1 October 2026. This repository remains private; access and licensing are unchanged.
