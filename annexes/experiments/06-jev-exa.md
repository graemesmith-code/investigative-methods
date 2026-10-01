# 06. Rank with Jev, then search the top ten with Exa

> Historical account retained below. A [dated follow-up](#follow-up-source-check-1-october-2026) now verifies original-award trade coverage, while the exact exported event and original search remain unresolved.

**What we tried:** the user reported ranking 10,000 original contract paragraphs with Jev, searching the top ten leads with Exa, and retrieving ten results per lead. Manual reassessment of exact-event coverage and source type was subsequently added to the process.

**Why:** ranking may reduce the reading queue, while search may identify earlier coverage. The two jobs need separate evidence so a search failure is not mistaken for an editorial discovery.

**What happened:** the actual [Overview 1.csv](../../evidence/exa/overview-1.csv) has ten leads. Nine say “Possible match” and one says “No clear match in results.” Each row reports ten Exa results. Priorities run from 0.660 to 0.710. The no-clear-match row identifies Anduril **FA881926DB0011**, at 0.680. These labels are summary fields; they are not verified assessments of the articles.

**What it cost:** actual per-run Jev and Exa charges, retries and reviewer minutes are missing. Ten results per lead is not an invoice, and token-price estimates are not actual costs.

**What remains uncertain:** the file lacks the original paragraphs, exact queries, article URLs and text, and manual reassessment decisions. Several lead descriptions are abbreviated. The 10,000-record corpus, its date range, prompts and code revision are not present. The CSV's ten rows cannot independently prove the upstream run or the contents of 100 returned article pairs.

**Why it matters:** a compact dashboard is useful for navigation but insufficient for auditing coverage. The next experiment should preserve the article pairs and the reason each was accepted or rejected.

## The Anduril diagnostic remains unresolved

An earlier account claimed prior coverage of this Anduril event, but exact links and their membership in the saved Exa result set were not recovered. Therefore this notebook does not classify the event as either covered or unreported.

The distinction can be resolved only with the original evidence:

- If the relevant exact-event article was absent from the saved search results, the problem was retrieval.
- If it was present but rejected incorrectly, the problem was classification.
- If it covered another award, a broader programme or only an official release, the original coverage claim may itself have been too broad.

These are diagnostic possibilities, not findings about what happened. The row's “No clear match” wording describes a limited result set and must not be converted into “never reported.”

## What a trustworthy reassessment requires

For each of the ten leads, preserve all ten returned results with stable lead ID, rank, URL, date, source type and the retrieved passage where retention is permitted. Mark whether it covers the **same action**, **same programme but different action**, **official announcement**, **copied release**, **independent reporting**, or **uncertain**. Record the deciding sentence and a human rationale.

The reported addition of manual reassessment is a process improvement. Without saved decisions it supplies no numerical revised outcome. Nine possible matches is not nine independently covered events; one no-clear-match is not one scoop. A priority of 0.700 is not a 70% probability of newsworthiness or wrongdoing.

## Next test

Recover the original ten paragraphs and 100 lead–article pairs before repeating at larger scale. Put known covered events through the same search. Compare Jev ranking with simple rules on a fixed reviewed set. Save the actual bill and reviewer time. This is proposed work; it was not performed while writing the notebook.

[Experiment index](../../experiments/README.md) · [Home](../../README.md)

## Follow-up source check: 1 October 2026

The following URLs were independently opened for this update. This is a later public-web check, not a rerun of the original Exa search. No full article text was added to the repository, and `evidence/exa/overview-1.csv` is unchanged.

| Source | What was inspected | What it supports |
|---|---|---|
| [ClearanceJobs, 8 April 2026](https://news.clearancejobs.com/2026/04/08/anduril-lockheed-northrop-among-14-winners-on-1-84b-andromeda-contract/) | Readable contract digest: exact identifier FA881926DB0011 beside Anduril, fourteen recipients, USD1.843 billion ceiling, award dated 7 April | Identifier-level association with the original Andromeda award; a contract digest, not evidence of an independent investigation |
| [Inside Defense, 8 April 2026](https://insidedefense.com/insider/space-force-awards-14-companies-18b-andromeda-gssap-replacement) | Readable bylined trade report naming Anduril among fourteen winners | Editorial trade coverage of the original award; no claim of major-outlet coverage |
| [Washington Technology](https://www.washingtontechnology.com/contracts/2026/04/space-force-picks-14-18b-object-tracking-contract/412754/) | Two open attempts timed out | Supplied candidate link only; its contents were not independently verified in this check |
| [EnvZone, record dated 16 April 2026](https://envzone.com/award-record/air-force-corrects-andromeda-1-84b-idiq-characterization-across-14-awardees/) | Readable secondary correction with the same Anduril identifier | Later distinction between the Andromeda contract vehicle and a programme; not the original award event |
| [Official 8 April contract notice linked by Inside Defense](https://www.war.gov/News/Contracts/Contract/Article/4453890/contracts-for-april-8-2026/) | Open attempt returned HTTP 403 | Original notice not independently read in this follow-up |

The digest gives 7 April as the award date; the correction refers to 8 April. Preserve this source-date distinction rather than silently choosing one date for every event. The identifier occurs in both award and correction contexts. The truncated export cannot resolve which full paragraph was ranked.

**Revised conclusion:** original-award trade coverage is verified. The exact exported event, historical query/date window, returned-result membership and reason for the “No clear match” label remain unknown. No demonstrated retrieval failure, classification failure, app bug or revised success rate follows. Recover the original paragraph and saved search before diagnosing the run.
