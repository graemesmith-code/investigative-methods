# 02. Which public feeds can a newsroom use?

**Question:** Before building a reporting tool, can we retrieve records that a journalist can understand and check? The 19 September 2026 source archive was unpacked and inspected for this notebook; access was not retested during this rewrite.

## What the sources contain

The trial covered public spending, announcements, regulations, research, oversight reports and corporate identifiers. These answer different questions. A spending record can describe a commitment rather than cash paid; a research description can reveal what an agency wants studied without proving the study was completed.

## A recipe you can follow

1. Pick two sources connected to a beat you know.
2. Retrieve a few records, including a known example, and save the original response and date.
3. Trace each row back to its official record. Read the description and check what the date and amount mean.
4. Record blocked access, empty results and missing documents separately. Add another source only once these two are useful.

## What happened

The inspected archive contained 20 capture entries and 14 extracted tables. **Nine source families** supplied usable data in that test: USAspending, official contract-announcement RSS, Federal Register, Regulations.gov, ClinicalTrials.gov, OpenAlex, GAO, Oversight.gov and GLEIF. Several tables came from the same family.

A Greenland keyword example exposed a basic trap: a company with “Greenland” in its name need not be doing work in Greenland. The combined Greenland-and-special-studies search found no qualifying record in that test, which is not proof that no such study exists.

Access also failed in useful ways. SAM.gov required a personal key; SBIR returned forbidden responses; Grants.gov returned a maintenance page. The announcement feed worked, while a linked contract article was blocked. These are dated observations, not permanent verdicts on the services.

## Cost, limits and the next useful step

Several routes needed no key; Regulations.gov used a public demonstration key. Actual charges and staff time were not preserved in a cost ledger. Small saved samples establish access at the time, not comprehensive coverage or a working ongoing service.

Repeat the two-source recipe with a clear reporting question and a record of time spent. The four small example tables in the annex show the kinds of fields to inspect.

[Technical annex: source samples and failed access](../annexes/experiments/02-public-source-pilot.md) · [Rabbit reference](../catalogs/README.md) · [All experiments](README.md)
