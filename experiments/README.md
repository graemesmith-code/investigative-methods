# Experiments: what happened and what you can try

Start with any question below. Each account can be read without running code. “Completed” describes the limited test, not a verified story or a validated system.

| Question | Date | Evidence and outcome |
|---|---|---|
| [01. Do contract recipients share sanctions-list names?](01-ofac-baseline.md) | 18 Sep 2026 | Completed screen; saved report and outputs. Thirteen candidate pairs, no violation established. |
| [02. Which public feeds can a newsroom use?](02-public-source-pilot.md) | 19 Sep | Source archive inspected; nine usable source families in that test, plus access failures. |
| [03. Can a headline filter find a known news story?](03-headline-filter.md) | 22–24 Sep | Prototype publication verified historically; missed control reported, detailed logs missing. |
| [04. Can a news provider retrieve sixteen outlets?](04-newsapi-retrieval.md) | 25 Sep | Script inspected; 27 requests and no errors reported, response files missing. |
| [05. Does the full contract paragraph help?](05-paragraph-prototype.md) | 27 Sep | Prototype published historically; ranking performance unmeasured. |
| [06. What did the top-ten Jev/Exa search show?](06-jev-exa.md) | 29 Sep | Ten-row export inspected; later check verifies original-award trade coverage for Anduril, but the exported event and search remain unresolved. |
| [07. Which Canadian ATI releases should a reporter read next?](07-canadian-ati.md) | 1 Oct | Completed ranking and bounded searches; one release read, two acquisition priorities, one invalid lower-ranked check pending rerun. |
| [08. Could old Enron filings support useful questions?](08-enron.md) | 30 Sep | Original filings checked; arithmetic and simple text search completed. No AI comparison or discovery claim. |
| [09. What did bank surveys show before 2008?](09-bank-lending.md) | 30 Sep | Three survey editions extracted and checked; warnings were already public. |
| [10. Is Canada's ATI index a useful place to start?](10-ati-source-check.md) | 30 Sep | Earlier source probe: twenty summaries inspected, three selected examples, no releases obtained at that stage. |

Jev is the model service used to rank or assess text in some trials. Exa is the search service used to retrieve possible earlier coverage. Their roles and costs are distinct. The requested OpenAI comparison is **blocked before its first API call**, with USD0 spent and no result to compare.

For a new trial, use [the method](../docs/method.md) and [run record](../templates/run.md). For source ideas, use [the Rabbit reference](../catalogs/README.md). For exact historical settings and saved files, use [the annexes](../annexes/README.md).

[Home](../README.md)
