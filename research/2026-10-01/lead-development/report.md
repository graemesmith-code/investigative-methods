# Improving cheap journalism lead discovery

Research date: 30 September 2026

The best next version is to find consequential changes, check what is already known, then get the next useful piece of evidence. Keep the Jev → search → re-Jev sequence, but do not make “no coverage” the sole route to a lead.

## What the small live test established

This was a free, web-based feasibility walkthrough, not a Jev or Exa benchmark. No paid API calls, document requests, outreach or repository edits were performed.

Canada’s completed ATI request summaries are a promising additional haystack. Direct JSON requests returned:

- Global Affairs Canada, completion-year 2026: 441 entries; 324 marked fully or partly disclosed
- National Defence, completion-year 2026: 793 entries; 602 marked fully or partly disclosed
- Combined: 926 potentially obtainable releases among 1,234 entries, before relevance, duplication or redaction checks

These counts were observed on 30 September 2026 at approximately 21:18 UTC. They are the API's reported totals and facet counts. Only the ten first-page records per department were returned and inspected, and three examples were selected. The 926 figure counts matching summaries marked partly or fully disclosed; it does not count underlying document packets downloaded, read or independently verified. No such packets were obtained.

GAC’s returned months stopped at July; DND’s stopped at August. They cannot be treated as a complete September activity feed. The first-page examples were convenience samples, not representative samples. Disposition is a useful access proxy, not a guarantee of useful content or successful delivery. Requesting an existing release may still involve delay, redactions, incomplete files and substantial reading time.

Each entry provides a request number, institution, summary, disposition and page count. The government says copies of previously released records can be requested at no cost; these informal requests do not have the same statutory requirements as formal ATI requests. That makes this a particularly good “which document should I get next?” corpus. [Search and access explanation](https://search.open.canada.ca/ati/)

## Three concrete walkthroughs

All coverage checks below were made on 30 September 2026. They assess what this bounded search could establish then, including articles published after the January 2026 completion month. They are not retrospective claims about what a search in January would have found. Underlying event dates, completed-request month, article publication date and the date of this coverage check are distinct.

### Ottawa Treaty

The [GAC entry A-2025-00627](https://search.open.canada.ca/ati/record/dfatd-maecd,2026,1,A-2025-00627) identifies 12 partly disclosed pages of briefing notes prepared between 1 March and 30 June 2025 about treaty withdrawals. The completed-request month is January 2026. The entry does not establish when the summary was first posted.

Coverage is readily detectable after expanding beyond the ATI identifier:

- Reuters covered the initial withdrawal plans in March 2025
- Canadian Affairs reported the implications for Canada’s Ukraine training mission on 23 September 2025, with comments from DND, GAC and advocates
- GAC’s October 2025 committee briefing already described bilateral efforts to discourage withdrawal
- AP covered Poland’s withdrawal on 20 February 2026

Sources: [Reuters on the initial plans](https://www.investing.com/news/commodities-news/poland-and-baltic-nations-plan-to-withdraw-from-landmine-convention-3934608), [Canadian Affairs reporting](https://www.canadianaffairs.news/2025/09/23/ukraine-exit-from-ottawa-treaty-complicates-mission/), [GAC committee briefing](https://international.canada.ca/en/global-affairs/corporate/transparency/briefing-documents/parliamentary-committee/2025-10-30-faae), [AP’s Poland report](https://apnews.com/article/1d2d9a1daccf2a55265dd0b2db5ebdb5).

Precise next question: Do the 12 pages identify dated Canadian recommendations or diplomatic interventions that materially add to the public October account?

Next document: the already-completed 12-page release, then compare its recommendations and dates against those existing sources.

Disposition: worth a small document check; no demonstrated fresh claim yet. “Countries are withdrawing” and “this complicates Canada’s position” are already covered. A later advocacy discussion surfaced too; it was not counted as additional independent reporting. The search did not establish the most recent coverage anywhere.

### C22 pistol

The [DND entry A-2025-00945](https://search.open.canada.ca/ati/record/dnd-mdn,2026,1,A-2025-00945) identifies 153 partly disclosed pages concerning unintentional discharges or injuries involving the C22 during 1 January 2020–30 July 2025. Completed-request month: January 2026.

Searching C22/C-22, SIG Sauer and P320 recovered CBC’s 16 April 2026 report about a soldier’s lawsuit over an April 2024 incident. The original CBC page was inaccessible to the web tool. Coverage was corroborated through its syndicated listing, an April 20 follow-on report explicitly attributing CBC, and a contemporaneous Senate intervention. These are not three independent investigations. [Follow-on report](https://thedefensepost.com/2026/04/20/canada-lawsuit-pistol-accident/), [Senate intervention](https://sencanada.ca/en/senators/macdonald-michael-l/interventions/691183/18), [original CBC URL linked by the follow-on](https://www.cbc.ca/news/politics/pistol-soldier-canada-wounded-p320-9.7165101).

The newest relevant editorial item found in this bounded search was the April 20 follow-on, not a verified “latest article anywhere.”

Precise next question: Does the 153-page release contain incidents, dated warnings or investigative records beyond those already used in the CBC investigation?

Next document: the release’s index and incident chronology, checked against CBC’s reported facts before reading all 153 pages closely.

Disposition: use as a known-covered control; only retain as a reporting lead if the documents add something. The summary is not proof of either a defect or undisclosed incidents. No finding about the underlying incident or litigation was independently verified in this exercise.

### Brokering permits

The [GAC entry A-2023-02654](https://search.open.canada.ca/ati/record/dfatd-maecd,2026,1,A-2023-02654) identifies five partly disclosed pages of briefing note 02697-2023 concerning a decision on Group 2 brokering-permit applications. Completed-request month: January 2026. The identifier contains 2023, but the exact underlying decision date is not supplied.

Exact-ID, note-number, title, English contextual and French contextual searches did not establish an exact-event editorial match. They mainly retrieved unrelated numerical matches or general reporting and official information. This is weak searchability, not demonstrated novelty: the summary names no broker, destination, item or decision outcome.

Precise next question: Which applications, countries and goods does the note concern, and what decision or conditions were recommended?

Next document: the five-page release. Extract that event identity before spending more search calls.

The [2023 official military-export report](https://international.canada.ca/en/global-affairs/corporate/reports/export-import-controls/military-goods-2023) supplies a useful comparison table, but explicitly warns that permit values can be duplicated across rows and authorization need not mean a transfer occurred that year.

Disposition: inexpensive evidence-acquisition candidate, not yet an actionable story. No particular country, broker or alleged misconduct can be inferred from this summary.

All three looked interesting as summaries, but they demand different next actions. A binary covered/uncovered label would lose that distinction.

## Change the unit from paragraph to reporting question

A paragraph is a convenient input, but an event or change should be the unit of work.

For a contract modification, give Jev:

- The original paragraph
- The parent award’s purpose
- The previous relevant action
- The changed amount, scope, duration or location, clearly separated
- The source dates and identifiers

Then ask: “What changed, why might it matter, and which fact would determine whether this deserves reporting?”

This tackles a weakness visible in the existing samples: an administrative-looking modification may concern an interesting programme, while a dramatic dollar figure may be a ceiling, an exercised option or an already-announced purchase.

USAspending supports transaction-level fields including action date, modification number, description and amount, so this is a concrete, bounded join rather than a general research agent. Its API is documented as unauthenticated. A live parent-award lookup attempted during this research returned HTTP 503, so that particular enrichment was not demonstrated in this exercise. [API documentation](https://api.usaspending.gov/docs/endpoints)

## Make the second Jev pass coverage aware

After retrieval, ask three separate questions:

- Does this article concern the same event or modification?
- What does it actually establish about the proposed reporting question?
- What consequential question remains, and what specific evidence could answer it?

Use two classification axes.

Event relationship:

- Exact event/action
- Parent award or earlier/later modification
- Related context
- Unrelated
- Cannot determine

Source provenance:

- Original editorial reporting
- Editorial follow-on or syndication
- Official publication
- Company or advocacy release
- Database/aggregator
- Inaccessible or insufficient text

A government announcement matching an award establishes disclosure; it does not establish editorial coverage. Ten syndicated versions of one story are one reporting lineage. A well-reported award can still contain an uncovered modification, local consequence, implementation failure or emerging pattern.

Keep the matcher blind to the first Jev score where possible. “This is a high-priority scoop” is anchoring material, not matching evidence. Require a supporting passage and event fields for a positive match. A search-provider category such as “news” is not a substitute for checking provenance.

## Search in stages with a stop condition

Start with an event fingerprint:

- Stable identifier
- Recipient and meaningful aliases
- Specific action or programme
- Action date and an appropriate date window
- Amount with its meaning: obligation, ceiling, amendment or payment

Proposed three-step search:

1. Exact identifier or distinctive quoted phrase
2. Entity + action + programme, using common names and rounded amounts when useful
3. A targeted alternative for unresolved, worthwhile cases: local language, original outlet, parent award or older context

Do not insist every query contains every field. Articles frequently omit contract identifiers. Conversely, broad company searches find articles that have nothing to do with the action.

Stop when the remaining editorial decision is clear:

- An exact article fully covers the proposed claim: record it and assess a different angle only if there is a concrete basis
- The event identity is too vague: obtain the defining document
- A promising unresolved case survives the ordinary search: allow one targeted expansion
- The next search is merely generic background: defer it

The walkthrough used 18 queries across three candidates. Seven were spent on the underspecified brokering case with little improvement. That supports an earlier “get the five-page note first” stop rule. This is an observation about this small walkthrough, not a measured general search-efficiency effect.

## Pick haystacks through small trials

The recommended order for the next experiments is:

1. **Existing defence contracts enriched with parent/change history.** Lowest switching cost; tests whether the missing ingredient is context rather than a new source.
2. **GAC and DND completed ATI releases.** Concrete document-access path and strong subject fit; freshness and redactions remain constraints.
3. **Canadian aid-project changes.** GAC publishes IATI activity files every business day, including partners, project status, results and financial fields. Test changes in projects rather than rediscovering whole projects. These files may contain information absent from the Project Browser. [GAC IATI documentation](https://www.international.gc.ca/world-monde/issues_development-enjeux_developpement/priorities-priorites/initiative.aspx?lang=eng)
4. **Canadian procurement amendments.** Useful for joins, but reporting conventions require care: amendments may be aggregated, options may be reported differently, and non-financial amendments need not always appear. [Publication guide](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32763)
5. **OFAC changes linked to activity histories.** Prefer newly changed entities plus dated transactions over rerunning an undifferentiated name cross-match. OFAC provides list downloads and archived deltas. Identity, historical status, transaction meaning and applicable permissions remain separate verification questions. [OFAC Sanctions List Service](https://ofac.treasury.gov/sanctions-list-service)

Briefing-note titles are particularly useful as a bridge into completed ATI releases through note identifiers. On their own they are often document pointers, not story evidence. Cabinet-confidence titles are excluded and other titles can be redacted, so absence is not evidence that a subject was ignored. [Briefing-note search](https://search.open.canada.ca/briefing_titles/)

For a first comparison, take 20 randomly sampled entries plus 10 deliberately enriched candidates per corpus. Keep those groups separate and avoid duplicates between them. Use the random group to learn about the ordinary material and the enriched group to test a discovery strategy. Neither a top-ten list nor the convenience sample above estimates the whole corpus’s yield. Small samples are for deciding what to test next, not producing precise rankings of rare-story rates.

## Cheapest falsifiable experiments

### Parent context test

First priority: take 24 contract events spanning large awards, modest modifications and administrative-looking actions. Compare paragraph-only Jev with paragraph-plus-parent-and-change Jev. Have a reporter review anonymized outputs.

Success: more distinct worthwhile questions, or equal usefulness with less review time.

Failure: only longer summaries, recurring amount errors or no improvement over simple rules.

### Retrieval controls

Use 12 events with known editorial URLs plus hard negatives involving the same supplier or award but a different action. Compare one broad query with the staged query recipe.

Measure known-article recovery, false exact-event matches and unique reporting lineages. This tests the search/matching step without pretending to measure discovery recall across all news.

### Coverage aware second pass

Take a mixture of clearly covered, unresolved and source-only cases. Compare “discard covered” against “identify the remaining evidence-backed question.”

Success: additional human-approved questions that survive a short check.

Failure: plausible-sounding angles unsupported by new evidence.

### Small haystack comparison

Give the three leading sources the same reporter-time allowance and record every stage. Advance the source that produces the best questions per review hour, not the largest raw queue. Track acquisition delay separately from reading time so a cheap-to-request but slow-to-arrive file is not mistaken for an immediately actionable lead.

### Pattern test

After the above, group a narrow class of actions by supplier, programme, location or time before ranking. Look for meaningful changes relative to comparable records. Use arithmetic for the pattern and Jev for the explanation. Require a plausible ordinary explanation alongside every anomaly. Do not interpret a missing record as an anomaly before checking reporting scope, identifiers, delay and access failure.

These are proposed tests and decision criteria, not validated performance thresholds. Choose the human-review allowance before seeing the outputs; do not tune both the method and its evaluation on the same handful of examples.

## What to measure and preserve

The headline outcome should be human-approved, evidence-backed questions worth pursuing per reviewer hour, alongside cash cost per such question.

Record separately:

- Records available, retrieved, usable and deduplicated
- Unique events considered
- Candidates searched
- Cases with exact editorial coverage
- Cases with only official/PR/context results
- Evidence-expansion attempts
- Questions accepted, deferred and rejected
- Cash charged, credits consumed and human minutes

“Verified lead” should mean the factual hook was checked and a reporter accepted the next step. It must not imply the eventual allegation is established or that nobody has reported it.

Audit a small random sample of rejected records. Exhaustive recall is not necessary for this project, but it is useful to know whether the filter systematically loses the kind of story the reporter values. Compare with simple dollar/change/keyword rules and a random baseline on the same frozen records. Count duplicated story clusters once.

Preserve the source passage, event identity, exact query, returned URLs, relevant passages, provenance labels, decision and reason. Keep failed requests, unreadable articles and missing fields visible. Log action date, completion date, publication date and first-observed date separately; do not silently substitute one for another.

Current Exa pricing is $7 per 1,000 ordinary searches with up to ten results. Sixty candidates receiving three searches each would therefore have a $1.26 base search estimate, before other services, optional additions and human time. Requesting three results rather than ten does not reduce that base charge; selective reading mainly saves model tokens and editorial effort. These are planning figures, not measured costs of the earlier runs. [Exa pricing](https://exa.ai/pricing), [search response and request fields](https://exa.ai/docs/reference/search)

Do not wait for a perfect architecture or reconstruct every old run before experimenting again. Run one small, fully preserved comparison. The most promising improvement is supplying the right adjacent evidence at the right moment, then asking a sharper editorial question.

## Reproducibility and limits of this package

The accompanying `reproduce_counts.py` makes two unauthenticated GET requests to the official ATI JSON search route and writes aggregate counts without retaining the unrelated first-page records. Run it with Python 3:

```sh
python reproduce_counts.py --year 2026 --output count-probe-rerun.json
```

The exact original endpoints were:

- https://search.open.canada.ca/ati/?owner_org=dfatd-maecd&year=2026&search_format=json
- https://search.open.canada.ca/ati/?owner_org=dnd-mdn&year=2026&search_format=json

`corpus-counts.json` preserves the original observed aggregates. `selected-records.json` preserves only the three relevant public source records. `source-manifest.json` identifies original captures, transformations and file hashes. `web-query-ledger.json` records all 18 query strings and bounded case-level conclusions. It is a compact research ledger, not an export of every returned page. `count-probe-validation.json` records a successful live rerun of the reproduction script later on the same date; both requests returned HTTP 200 and the same aggregate counts.

The sources were accessed through the public web. No Exa or Jev execution occurred, and no search-recall, novelty or cost-per-lead result can be inferred from this package. Full third-party article text and unrelated convenience-response records are deliberately excluded. The original CBC article could not be opened; the report explicitly labels the derivative and official evidence used to establish the existence of coverage.
