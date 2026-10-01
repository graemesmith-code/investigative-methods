# 02. Find public feeds a small newsroom can actually use

**What we tried:** test public defence-related feeds and keep their responses and small tabular extracts, rather than assume that a source catalogue means usable access.

**Why:** a cheap monitor needs dependable inputs. Each record must also answer a reporting question: what money changed hands or what work was commissioned?

**What happened:** the 19 September archive was unpacked for this notebook. It contains a README, manifest, 14 normalised CSV extracts and raw JSON, XML and captured status responses. The audit identifies nine source families with usable data: USAspending, official contract-announcement RSS, Federal Register, Regulations.gov, ClinicalTrials.gov, OpenAlex, GAO, Oversight.gov and GLEIF. Multiple extracts can come from one family; 14 files does not mean 14 independent sources.

**What it cost:** several routes required no key; Regulations.gov used a public demonstration key. Actual request charges and staff time were not preserved as a cost ledger. Access without a key is not a complete accounting of running costs.

**What remains uncertain:** access and schemas can change, feed coverage is partial, and database descriptions can be stale or administrative. These are test samples, not discoveries. Current API functionality was not retested for this notebook.

**Why it matters:** testing sources first helps keep the system small. The same pipeline can look for significant money changes and interesting research commissions without applying one dollar threshold to both.

## Two questions, two ledgers

The **money ledger** asks what an award or modification changed. An obligation is a commitment, a ceiling is a maximum, and a payment is money actually paid. Those amounts must not be substituted for each other.

The **intent ledger** asks what problem an agency is commissioning someone to examine. A small study can be important even if its amount is modest. A transaction describing an amendment may not be a new commission, so the original award history still matters.

The source pack's Greenland keyword test also shows why word matches need review: a company name containing Greenland is not proof that work concerns Greenland. The combined Greenland-plus-special-studies query returned no qualifying record in that test; it does not establish that no such study exists.

## What failed and what was preserved

SAM.gov required a personal API key; no record sample was fabricated. SBIR endpoints returned forbidden responses amid maintenance or authorisation problems. Grants.gov returned a maintenance page. The official announcement RSS worked, but the linked contract article was blocked in the test environment. Those are historical access observations, not permanent source verdicts.

## Evidence and a bounded repeat

The [inspected original manifest](../../evidence/api-samples/manifest.csv) records 20 captures, including failed access checks. [Four small CSV selections](../../evidence/README.md) show transaction fields, study descriptions, legal-entity identifiers and announcement links. Selection sizes and hashes are recorded there. The full raw pack is retained as a source reference, not uploaded wholesale.

For a repeat, choose two source families, save exact queries and raw responses, record the retrieval time, and check that a human can trace every extracted row back to a source record. Count failed and empty responses separately. Only then add another source. This repeat is a proposal, not a new run.

[Experiment index](../../experiments/README.md) · [Home](../../README.md)
