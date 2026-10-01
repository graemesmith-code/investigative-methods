# 03. Filter contract headlines, then test a known article

**What we tried:** build a headline-based prototype for narrowing Pentagon contracting leads and check news retrieval against a known Wall Street Journal article about THAAD.

**Why:** headlines provide a cheap starting point for triage and checking whether a subject has already attracted coverage. But a search tool needs to recover known examples before its empty results are useful.

**What happened:** the headline prototype was published on 22–24 September. Historical publication was verified. The reported GDELT check failed to recover the known WSJ THAAD control. The full control query, article URL, response log and date settings are not present in the approved evidence supplied for this notebook.

**What it cost:** actual prototype, hosting, model and search costs were not recovered. A provider's apparent availability or an estimate cannot substitute for the bill and reviewer time.

**What remains uncertain:** the failure could arise from indexing, query formulation, date limits or another retrieval issue. Without the saved query and response, its cause cannot be assigned. Present live functionality of the published application is untested.

**Why it matters:** zero search results cannot mean “unreported.” A failed known control means the search is not reliable enough to exclude coverage in that case. Repair this before using search silence to prioritise a supposed scoop.

## Prototype references

- [Replit project](https://replit.com/@smithg5/Pentagon-Headline-Filter)
- [Published application](https://pentagon-headline-filter.replit.app)

These are historical project and publication references. They are not pinned code snapshots and do not establish current behaviour.

## How to make the next test useful

Before searching unknown leads, select a small set of articles already known to cover exact contract events. Save their identifiers, URLs and publication dates. Include difficult cases: acronym changes, a modification rather than an initial award, and a specialist publication.

Run fixed queries and record whether each known item is retrieved. Keep the search response, query, date restrictions, returned domains and failure state. If a control is missing, label the outcome **retrieval incomplete**. Only after retrieval succeeds should a second step decide whether a returned article covers the exact action or merely the wider programme.

This procedure is proposed validation; no recovery rate is claimed. A headline mentioning the same company is not an exact-event match. Agency and contractor announcements should be distinguished from independent reporting.

## Missing reproduction evidence

A repeatable historical comparison needs the original code revision, input headlines, query construction, controls, provider settings and result logs. None are reconstructed by visiting the public prototype alone. The future [run template](../../templates/run.md) captures these fields.

[Experiment index](../../experiments/README.md) · [Home](../../README.md)
