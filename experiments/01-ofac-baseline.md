# 01. Do contract recipients share sanctions-list names?

**Question:** Could a simple comparison of US contracting records and sanctions names produce a manageable reading list? The screen ran on 18 September 2026; its report, code and selected outputs are preserved.

## What the sources contain

USAspending records contract actions and amounts. The OFAC list records US Treasury sanctions designations and aliases. A shared name is a reason to check identity. It does not show that a payment occurred or that a transaction broke the law. The September 2026 sanctions snapshot also cannot establish status on every earlier contract date.

## A recipe you can follow

1. Choose dated copies of both lists and write down which period they cover.
2. Compare full names first. Keep looser matches, such as names with “Ltd” removed, in a separate list.
3. Read the actual contract action for each match. Check the address and official identifiers, the date and what the amount means.
4. Ask what record would resolve the question, including an innocent explanation. Keep rejected matches too.

A spreadsheet can illustrate the comparison on a small sample. The annex explains the code used for the full-year screen.

## What happened

The screen read **6,639,176 FY2025 transactions**, covering 101,379 distinct recipient names. It compared them with 23,398 names and aliases for 9,980 sanctions entities. Five candidate pairs matched after case and punctuation changes; eight more appeared after removing company suffixes. Together they involved 153 transactions and 72 award identifiers. **No sanctions violation was established.**

The clearest identity example was **NAI Logistics B.V.**, matched by full name and street address. Its 11 March 2025 record, vehicle SPE60523D9402, modification P00002, says **“TERMINATE FOR CAUSE” and USD0 in new obligations**. A contract vehicle is an arrangement under which orders can be placed. This row records its termination; it does not prove a prohibited payment or that work continued after designation.

## Cost, limits and the next useful step

No paid data or model calls were used. Downloading, computing, storage and review time were not costed. Matching misses spelling variants, ownership relationships and subcontractors, while common names create false alarms.

For NAI, the next useful step is to reconstruct the vehicle and delivery-order history, including FY2024, and check timing and identity. That work has not been completed here.

[Technical annex: counts, sources and reproduction](../annexes/experiments/01-ofac-baseline.md) · [All experiments](README.md) · [Home](../README.md)
