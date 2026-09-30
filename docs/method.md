# How the method works

The method is a series of small tests. First collect public records faithfully. Then reduce the queue using clear rules. Use a model only for narrow judgments about text. Search the surviving leads for earlier coverage, and have a journalist inspect the evidence.

## Collect before interpreting

Keep the source URL, exact query, retrieval time, date range and raw-file hash. A hash is a fingerprint that lets another person check whether they have the same file. Keep action date and publication or first-observed date separate. A late record is not necessarily a new event.

## Use code for exact work

Code handles names, identifiers, duplicates, arithmetic and dates. The OFAC baseline shows why the weaker suffix-removal pass needs a separate label. An identifier match can be useful, but identity and context still need checking.

## Use a model for a bounded question

Jev's proposed role is to classify compact passages or candidate pairs. Examples: does this paragraph explicitly state a changed scope; does this passage describe the same event; is the described work a study or routine support? Save the exact question and model version. Ranking helps choose what to read; it does not prove a fact.

This architecture is adapted from the inspected 17 September Jev journalism design. It is a proposal for evaluation. The design's catalogue counts, vendor performance claims and historical price examples are not carried into this notebook as tested newsroom results.

## Search, then classify

Exa and other search providers retrieve possible coverage. First ask whether known articles can be recovered. Then ask whether a retrieved article concerns the precise event. A broad company mention is not enough. Separate official announcements, copied releases and independent reporting.

Use limited language: “No obvious exact-event match in the saved search” is acceptable when the search and results are preserved. “Never reported” is not supported by an incomplete index or short result list.

## Give the reporter a small queue

Each card needs the original record, a proposed reporting question, coverage status, a plausible ordinary explanation, uncertainty and one next document check. A starting proposal is at most ten cards per week. That limit has not been validated as the optimal newsroom workload.

Measure the number of useful cards, the important records missed, review time and actual cost. Compare rules alone with rules plus a model on the same input set. Retain rejected examples so evaluation includes the mistakes that never reached the top ten.

[Home](../README.md) · [Next steps](next-steps.md)
