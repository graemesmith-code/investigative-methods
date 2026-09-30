# 04. Check retrieval from sixteen news outlets

**What we tried:** use The News API to retrieve small article samples from sixteen selected outlets, with a monthly query and an undated follow-up when the monthly search returned zero.

**Why:** a newsroom needs to know whether its chosen sources are represented before treating a news search as a coverage check.

**What happened:** on 25 September the user reported 27 requests across 16 outlets with no errors. The [supporting script](../code/newsapi/check_newsapi_sources.py) is present and inspected. Saved result JSON and the generated report were not supplied here, so request counts and the no-error outcome remain reported results rather than independently verified logs.

**What it cost:** the script was designed for a free-plan check. Actual quota use, bill and human review time are missing. Historical free-plan assumptions should be verified before another run. This notebook did not execute paid or authenticated requests.

**What remains uncertain:** provider counts are counts within the provider's index, not proof of complete outlet coverage. A success response can still contain domain or date mismatches. Zero under one alias does not prove an outlet is absent under all aliases.

**Why it matters:** the check helps identify access and query problems. It cannot decide that a particular contract event was never reported.

## What the code actually does

The script lists Reuters, AP, Bloomberg, WSJ, New York Times, Washington Post, Politico, CNN, NBC, NPR, Defense News, Breaking Defense, Defense One, Air & Space Forces Magazine, USNI News and The War Zone. Domain aliases are test inputs, not verified coverage guarantees.

It requests up to three article samples per query, keeps provider counts and response records, checks returned domains and month strings, and stops on connection, authentication, plan or quota restrictions. An undated follow-up checks whether the date filter may explain an empty monthly result. Counts cover all indexed subjects, not only contracting. The War Zone's older thedrive.com/the-war-zone archive is not tested.

The historical 27-request total cannot be decomposed into particular outlet outcomes without the missing saved logs. The code can attempt between 16 and 32 queries if all outlets are reached, but that possible range is not evidence of which requests actually occurred.

## Repeating it

See [technical reproduction](../docs/reproduction.md) for the command. Supply an existing authorised token through the environment or hidden prompt; never commit it. Choose and record the month explicitly because the script's default is June 2026. Preserve outputs and quota evidence outside any credential files, then inspect them before sharing.

Add an exact-event known-article control for every outlet that will be used to exclude coverage. A source-domain sample and a successful HTTP response cannot substitute for that control.

[Experiment index](README.md) · [Home](../README.md)
