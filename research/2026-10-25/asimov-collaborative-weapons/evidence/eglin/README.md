# Public source audit of selected FA8651 awards

Research cutoff: 24 October 2026. Prepared for journalism research. No outreach or publication was performed.

## Start here

- `portfolio-findings.md`: conclusions, six exact-award case histories, procurement and location distinctions, novelty hypotheses and contrary evidence.
- `fa8651-cohort-audit.csv`: all 22 FA8651-prefixed entries from the fixed register, not a handpicked set of 14. Contains six named-case flags, reported-period status, financial values, agencies/offices, principal performance locations, parents, scope notes and source URLs.
- `fa8651-contract-actions.csv`: all 124 published FPDS actions across the 20 contracts. Values are action changes, not cumulative totals. The two grants have no FPDS contract-action histories.
- `timeline.md`: the six awards' major procurement changes and separately labelled historical programme evidence.
- `people-and-source-map.md`: dated public professional roles, interview questions, public institutional routes, conflicts and uncertainty about departures.
- `source-index.md`: verified-source URL index for the above material.
- The package-level `manifest.json` and `SHA256SUMS` provide hashes after finalization; this subdirectory has no separate manifest.

## What is verified

The current USAspending records for all 22 were retrieved, and the complete paginated FPDS histories for all 20 contracts were checked. Obligation, base-and-exercised and base-and-all-options changes reconcile exactly to current totals for every contract. Six recorded current completion dates extend past the cutoff. This is not a real-time count of active programmes, legal closures, fielded weapons or successful technical outputs.

Of the six named cases, TALON and GTRI's supersonic order have reported current completion dates beyond the cutoff. TALON's original October 2026 end is stale; the record now says September 2027. EpiSci's original October 2026 end was shortened to October 2025 and value reduced. All six named awards together have $12,256,665.44 in net obligations, not total programme spending.

## Definitions and cautions

- Net obligation means funds legally committed, not necessarily paid out.
- Current/base-and-exercised value is distinct from obligations and from potential/base-and-all-options value.
- A current completion date does not mean the entire period is fully funded.
- A potential end date or unexercised option is not a demonstrated extension.
- Awarding office, funding agency, reported principal performance location, recipient headquarters and actual test location are different fields/facts.
- FA8651 is an Eglin-linked contracting identifier; it is not evidence that all work occurs there.
- Research classifications, proposal abstracts and contract titles do not establish operational effectiveness or production.
- USAspending and FPDS share underlying reporting. Their reconciliation is a consistency check, not independent proof that work occurred as reported.
- DoD reporting lag means late actions may not yet be visible.
- No technical construction, implementation or operational employment guidance is included.

## Fixed register provenance

Repository: `graemesmith-code/investigative-methods`.
Commit: `e931fcbc6dc52c00b0565e853637a64fa95773b3`.
Published path: `research/2026-10-24/f2-tactical-ai/audit/lane1-tactical-candidates-384.csv`.
Immutable source: https://github.com/graemesmith-code/investigative-methods/blob/e931fcbc6dc52c00b0565e853637a64fa95773b3/research/2026-10-24/f2-tactical-ai/audit/lane1-tactical-candidates-384.csv

The original frozen source is reported as 508,667 bytes with SHA-256 `cfe921e6d629c71e1a916802f7d2395c4c6de8d453426293eba081bf202186b0`. The local audit input was retrieved through a text connector and has normalized line endings: 508,283 bytes. No byte-identity claim is made for that text copy. The 22 exact identifiers and all financial evidence were separately checked against the official primary records. Original source bodies are not reproduced in this public-safe deliverable package.

The selected register includes one ASIMOV overlap, Saab RESPECT FA865125CB007, and two grants. Those are labelled explicitly. It is neither the complete FA8651 portfolio nor a uniformly eligible collection of collaborative weapons.
