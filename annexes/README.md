# Technical annexes and evidence

Read the [experiment accounts](../experiments/README.md) first if you want the reporting lessons. These annexes preserve detailed methods, source references, historical decisions and instructions for checking the work.

## Detailed accounts

| Readable experiment | Supporting detail |
|---|---|
| [Contracts and sanctions](../experiments/01-ofac-baseline.md) | [Full account](experiments/01-ofac-baseline.md), [original evidence report](../evidence/ofac/original-report.md), [reproduction](reproduction.md#ofac-baseline) |
| [Public-source access](../experiments/02-public-source-pilot.md) | [Source trial](experiments/02-public-source-pilot.md), [sample inventory and selection](../evidence/README.md) |
| [Headline search](../experiments/03-headline-filter.md) | [Prototype references and missing controls](experiments/03-headline-filter.md) |
| [Sixteen news outlets](../experiments/04-newsapi-retrieval.md) | [Outlet list and script behaviour](experiments/04-newsapi-retrieval.md), [reproduction](reproduction.md#the-news-api-retrieval-check) |
| [Paragraph prototype](../experiments/05-paragraph-prototype.md) | [Full account and proposed comparison](experiments/05-paragraph-prototype.md) |
| [Contract top-ten search](../experiments/06-jev-exa.md) | [Evidence gaps and reassessment design](experiments/06-jev-exa.md), [original export](../evidence/exa/overview-1.csv) |
| [Canadian ATI live run](../experiments/07-canadian-ati.md) | [Detailed report](ati-report.md), [evidence index](../research/2026-10-01/ati-live/README.md), [identity correction](../research/2026-10-01/ati-live/correction-identity.md), [code and offline tests](../code/ati/README.md) |
| [Enron](../experiments/08-enron.md) | [Full source chronology and calculations](enron-report.md), [script guide](../research/2026-10-01/enron/README.txt) |
| [Bank lending](../experiments/09-bank-lending.md) | [Full report](crisis-report.txt), [source and script guide](../research/2026-10-01/crisis/README.txt) |
| [Earlier ATI source probe](../experiments/10-ati-source-check.md) | [Queries, three cases and proposed tests](lead-development-report.md) |
| [Mining disclosure pairs](../experiments/11-mining-disclosure-pairs.md) | [Comparability audit](mining-claims-audit.md), [research archive](../research/2026-10-12/mining-claims/README.md), [four-case starter](../code/mining_claims/README.md) |

The [overnight synthesis](overnight-research.md) and its [review checklist](../research/2026-10-01/REVIEW.md) describe the earlier 30 September work. Its “no Jev/Exa calls” and “no releases obtained” statements concern that stage, before the separately documented 1 October ATI run. Vendor prices and service limits in these historical reports are dated observations, not newly checked offers.

## Prompts, accounting and data definitions

The ATI [ranking prompt](../research/2026-10-01/ati-live/ranking-prompt.json), [calibration review](../research/2026-10-01/ati-live/calibration-review.md), [exact costs](../research/2026-10-01/ati-live/cost-summary.json), [sanitized call accounting](../research/2026-10-01/ati-live/ledger-accounting.json) and [source manifest](../research/2026-10-01/ati-live/source-manifest.json) preserve how that run was made. [Reading the ATI files](ati-files.md) explains their roles and the invalid medical-fairness entries.

For other runs, the [evidence inventory](../evidence/README.md) separates included samples from missing inputs. A filename or hash in an old manifest may refer to the original source archive rather than a bundled file. No missing article text or original input has been recreated to fill a gap.

[Technical run record](run-record.md) · [Reproduction instructions](reproduction.md) · [Editorial-restructure verification](restructure-verification.md)

## Why scripts and data stay where they were

Code uses repository-relative paths and pinned file fingerprints. Moving the data with the prose would risk breaking repeatability. We moved long explanations into this annex directory, retained short entry points at former report URLs, and kept canonical scripts, machine-readable evidence, scanned pages and correction records in their original locations. Older manifests remain records of their own publication stage; they are not silently regenerated to describe this edit.

The original ATI database remains excluded because it contains third-party article passages. The accounting export does not replace it or authorize another paid run. Offline checks can be run without it; authenticated continuation is deliberately guarded.

[Home](../README.md) · [Rabbit catalog reference](../catalogs/README.md)

