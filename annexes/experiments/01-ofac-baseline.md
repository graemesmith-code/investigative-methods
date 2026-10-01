# 01. Compare contract recipients with sanctions names

**What we tried:** take a full year of federal contracting transactions and look for recipient names that also occur on an OFAC sanctions list. OFAC is the US Treasury office that maintains the list used here.

**Why:** this is a simple, repeatable baseline for deciding whether a large public dataset can yield a manageable set of records for a reporter to inspect.

**What happened:** the completed 18 September screen read 6,639,176 FY2025 transactions with 101,379 distinct recipient names. It compared them with 23,398 names and official aliases belonging to 9,980 OFAC entities. It found five candidate pairs after normalising case and punctuation and eight more after removing terminal company suffixes. Those 13 pairs involved 153 transactions and 72 award identifiers. These are screening alerts. No sanctions violation or failed screening was established.

**What it cost:** no fuzzy matching, Jev calls, paid data or outreach were used. Computing, download, storage and review time were not costed. This demonstrates a baseline without paid model calls, not a measured zero-cost reporting service.

**What remains uncertain:** most pairs are weak name collisions. The current sanctions snapshot cannot by itself tell us a company's status on every historical action date. Corporate identity, action history and applicable authorisations require separate checks.

**Why it matters:** a deterministic screen can dramatically reduce the volume for review, but the reporter must interpret the record correctly. The strongest identity lead illustrates why an alert is not an accusation.

## The NAI example in ordinary language

NAI Logistics B.V. matched by full name and street address. The observed record is contract vehicle **SPE60523D9402**, modification **P00002**, dated **11 March 2025**, with action **TERMINATE FOR CAUSE** and **$0.00 federal action obligation**. The [OFAC designation announcement](https://ofac.treasury.gov/recent-actions/20231211) dates from 11 December 2023; the [USAspending vehicle record](https://www.usaspending.gov/award/CONT_IDV_SPE60523D9402_9700/) identifies the vehicle.

A contract vehicle is an arrangement under which orders may be placed. This row records its termination. It does not establish a prohibited payment, a new award after designation, or a failed sanctions check. The time between designation and termination does not establish that work continued. The next reporting question is what the vehicle and delivery-order histories show, including FY2024. That history has not been reconstructed here.

## Evidence and reproduction

The [original report](../../evidence/ofac/original-report.md) and [compact screen summary](../../evidence/ofac/screen-summary.json) support the counts. The [NAI excerpt](../../evidence/ofac/nai-transaction-excerpt.json) preserves selected fields from the saved matching row. It is a derived excerpt, not the complete original row.

The source is the [official FY2025 contract archive](https://files.usaspending.gov/award_data_archive/FY2025_All_Contracts_Full_20260906.zip), a September 2026 snapshot of actions from 1 October 2024 through 30 September 2025. Ordinary contract actions and blank-type vehicle rows were included. The OFAC list was published 17 September 2026; only Entity entries were retained, with strong and weak aliases distinguished. Individuals, vessels and aircraft were excluded from matching.

Scripts and exact input hashes are described in [technical reproduction](../reproduction.md). Full data is deliberately omitted from this small notebook. The completed historical run was not rerun against the 1.9 GB contract archive during notebook preparation.

## A method another reporter can copy

1. Preserve the dated source files and hashes before screening.
2. Use conservative matching first and label weaker matching separately.
3. Keep the original matching transaction, not only a company-name summary.
4. Compare identity using addresses and official identifiers.
5. Establish sanctions timing and interpret the action and amount before considering a legal conclusion.

The method should be evaluated on known matches and known collisions. It is limited to direct recipients and does not cover beneficial ownership, subcontractors, all sanctions lists or spelling variants.

[Experiment index](../../experiments/README.md) · [Home](../../README.md)
