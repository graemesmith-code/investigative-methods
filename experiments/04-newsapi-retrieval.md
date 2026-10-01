# 04. Can a news provider retrieve sixteen outlets?

**Question:** Does The News API return material from the outlets a reporter wants to check? On 25 September 2026, the user reported 27 requests across 16 outlets with no errors. The script is saved; its response files are missing.

## What the source contains

The service searches its own article index. A returned count describes that index, not an outlet's complete archive. A successful response also does not establish that the articles match the intended domain or month.

## A recipe you can follow

1. Choose the outlets and month explicitly.
2. Ask for a few sample articles from each outlet and read their source and date.
3. If a monthly search is empty, try without the month to see whether the date restriction explains it.
4. Before using the service to rule out prior coverage, check a specific article you already know should be there.

## What happened

The inspected script covers outlets including Reuters, AP, Bloomberg, WSJ, NPR and specialist defence publications. It requests up to three samples at a time, checks domains and month strings, and stops on access or quota restrictions. For example, an empty dated result followed by an undated result would point to the date restriction as a possible issue—not prove that every article outside the month is available.

That example describes how the check works, **not an observed outlet result**. Without the missing saved responses, we cannot allocate the reported 27 requests to particular outcomes or independently verify “no errors.” The annex lists all sixteen outlets and the script's specific limits.

## Cost, limits and the next useful step

The script was designed for a free-plan check. Actual quota use, charges and reviewer time are unknown. No authenticated request was made for this rewrite.

Recover the saved report if possible. For a newly authorized test, save both responses and usage, choose the month explicitly, and include known articles. A domain sample alone cannot establish coverage of an exact event.

[Technical annex: outlet list, code and settings](../annexes/experiments/04-newsapi-retrieval.md) · [All experiments](README.md)
