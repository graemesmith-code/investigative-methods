# What old scandals teach us about finding the next story

Prepared overnight, 30 September–1 October 2026. **Plain-English starting point.**

## The short answer

**Yes, this environment can run useful historical tests now.** It retrieved original Enron filings and banking-survey reports, ran small repeatable calculations and text checks, and tested access to a promising Canadian document catalogue. These were actual, limited tests using free sources. They were not Jev or Exa runs, and they do not establish that AI would have exposed Enron or predicted the financial crisis.

**The best next change to test in the current workflow is to give the model a small packet of connected evidence.** A lone paragraph can be interesting, but the stronger question often appears when it is compared with an earlier record, another document or an entity's stated position.

**Keep the coverage check, but change its purpose slightly.** Ask what is already known and what meaningful question remains. A covered event can contain an unreported consequence; an apparently uncovered event can be too vague or unimportant to pursue.

My first recommendation is a small comparison on the existing Pentagon corpus: paragraph alone versus paragraph plus its parent award and relevant changes. Do that before building a large new system. Canada's completed access-to-information summaries are the most promising additional source found in this research.

## 1. Enron: the useful signal was a relationship

We set a working cutoff of **31 March 2000**, using original filings available by then. The test included Enron's earlier annual and quarterly filings, its March 2000 proxy statement, and one contemporary Duke Energy filing for comparison.

The key connection was already in the public record:

- Enron described a senior officer managing a partnership involved in asset and hedging transactions with the company
- Another document, its proxy statement, named CFO Andrew Fastow and described his role and economic interests in the partnerships
- The proxy also disclosed a $38.5 million loan from an Enron affiliate to one partnership

These support a reporter's question: **Who independently priced these transactions, how independent was the buyer's financing, and what happened to the hedge if Enron's own shares fell?** The filings also described safeguards. A fair investigation would test those safeguards, rather than assume they failed. Importantly, the proxy itself puts the core conflict in one paragraph: the cross-document join adds detail, but was not necessary to spot that core question. This is a reason to test richer context, not evidence that paragraph-only Jev would miss the lead. [Original annual filing](https://www.sec.gov/Archives/edgar/data/1024401/000102440100000002/0001024401-00-000002.txt) · [Original proxy](https://www.sec.gov/Archives/edgar/data/1024401/0000950129-00-001279.txt)

The numerical warnings were less decisive. Enron's 1999 net income rose **27.0%**, while operating cash flow fell **25.1%**. Yet operating cash was still **1.38 times net income**: a simple rule looking for earnings greater than cash would miss it. Other broad warning signs appeared at Duke too. One comparison company is not enough to estimate a false-positive rate or establish who was clean.

The small text scanner also made instructive mistakes. It found the officer/partnership passage, but picked up irrelevant biographies and missed an adjacent passage using Fastow's name instead of his title. That is a concrete reason to test entity linking and neighbouring paragraphs. It is not proof that Jev will fix the problem.

**Important historical limit:** the 2000 financial-year annual filing was not filed until **2 April 2001**, after the March issue of Fortune containing Bethany McLean's article. Using that filing to claim an earlier discovery would give the detector information from the future. Earlier journalism also existed; this research did not establish the first-ever Enron warning. [Filing date](https://www.sec.gov/Archives/edgar/data/1024401/000102440101500010/0001024401-01-500010-index.html) · [Fortune article](https://fortune.com/article/is-enron-overpriced-fortune-2001/)

**What this changes:** screen changes and relationships across documents, not just whether one passage sounds alarming. The completed test demonstrates retrieval, hand-checked numerical inputs, automated arithmetic and simple text scanning. It does not prove fraud detection or measure AI's added value. [Full Enron test and reproduction files](enron/report.md)

## 2. Before 2008: warnings were visible, but warnings were already news

We downloaded original-edition surveys of bank underwriting from 2004, 2005 and 2006. A transparent calculation subtracts the share of relevant-product respondents tightening standards from the share easing them. Product groups contain different numbers of banks. It is a measure of the direction of lending standards, not the share of all banks, loan-dollar exposure or a forecast of losses.

For residential real estate, that difference was **0, 17 and 21 percentage points**. For conventional home-equity lending, it was **3, 16 and 32**. An illustrative ten-point alert rule flagged **0 of 8 categories**, then **4 of 8**, then **4 of 7**. Raising the threshold to twenty points removed every 2005 alert. These rules were chosen retrospectively, and the categories and surveyed institutions are not a fixed population.

The crucial qualification: **the regulator was already publicly warning about easing standards in July 2005**. Summarising that warning faster would not itself have been a scoop. Additional reporting value would come from connecting the warning to named lenders' growth, products, geographic concentrations and assurances about risk. [Contemporary OCC announcement](https://www.occ.gov/news-issuances/news-releases/2005/nr-occ-2005-74.html)

There was an actual automation failure: ordinary text extraction initially missed six of eight 2005 rows. Checking how many category rows should exist exposed the error. Reading the table by its page coordinates and checking the rendered pages repaired it. Category coverage and percentage row totals were checked; the script did not extract all product-specific respondent counts. This is why a seemingly precise AI summary needs mundane extraction checks underneath it.

A second example, mortgage-pricing data, showed why more data does not automatically mean a better warning. Part of a headline increase reflected interest-rate and reporting mechanics. The Federal Reserve's published adjustment used information missing from the free public loan file. We could read its contemporary conclusion; we could not reproduce the entire adjustment from freely available microdata. [Federal Reserve analysis](https://www.federalreserve.gov/pubs/bulletin/2006/hmda/default.htm)

**What this changes:** track combinations and contradictions, and preserve missing fields, revisions and denominators. Do not confuse a government warning, a lender-specific investigation and a forecast of a system-wide collapse. [Full crisis test, sources and limitations](crisis/report.txt)

## 3. How to use historical tests without fooling ourselves

Enron and 2008 are excellent engineering exercises and poor clean tests of a modern model's foresight. The model may already know the ending. Hiding the company name does not erase familiar figures, wording or transaction structures. We also chose these examples because they became famous.

Use two separate tracks:

1. **Historical development tests:** Can we recover the right document, read its table correctly, join the right entities, identify the change and produce a supported reporting question? Enron is useful here
2. **A forward-looking test:** Freeze a simple method before reviewing new material, preserve every result, and see which questions survive a journalist's check. This gives stronger evidence that the method works beyond remembered scandals

For another historical round, choose a whole group of comparable companies or records before checking outcomes, including ordinary cases. Compare simple rules with semantic ranking under the same review-time allowance. An obscure historical case can reduce obvious recognition, but does not guarantee freedom from training-data contamination.

We do not need to find every possible story. We need an honest measure of **worthwhile, evidence-backed questions per hour of human review**, with cash costs alongside it. A small random check of rejected records is enough to begin noticing systematic blind spots; it is not a demand for exhaustive recall.

### Exa Snapshot does not solve the historical-cutoff problem by itself

The current standard pay-as-you-go service accepts only a rolling **five-month window** and rejects older cutoffs. Its much larger archive claim does not establish ordinary access to a 1999–2000 or 2008 backtest. Snapshot can return stored page content at or before a cutoff, but candidate discovery uses **current retrieval signals**, so it does not reconstruct historical search rankings or remove knowledge already learned by a model. These are current service limits, not a test we ran. [Official documentation](https://exa.ai/docs/search/snapshot) · [Launch announcement](https://exa.ai/blog/exa-snapshot)

## 4. Size the opportunity, not just the database

The biggest pile of records is not necessarily the best place to spend money. First ask:

- Does this source describe consequential actions in a subject you understand?
- Are there identifiers, dates and previous versions that let us connect records?
- Can we obtain the next useful document without a long or expensive process?
- How much is repeated, stale, unreadable or already covered?
- After a short test, how many questions genuinely deserve follow-up?

Start with a cheap **source card**: reported record count, update frequency, date range, typical text length, accessible fields, stable identifiers, duplicates and whether the actual documents are available. Then inspect a small random sample and a separately labelled targeted sample. This can rule out an awkward source before sending its entire contents through any model. It cannot establish the frequency of very rare stories from a tiny sample.

A real access probe found that the Canadian completed-ATI search API **reported 1,234 completion-year 2026 entries** for Global Affairs Canada and National Defence combined. Its summary counts marked **926** fully or partly disclosed. We saved and inspected the first ten entries for each department, not all 1,234 records and not the underlying releases. The returned months stopped at July and August respectively, so this is not a complete current-month feed.

The attraction is practical: summaries give an institution, request number, page count and a route to request previously released documents at no cost. Redactions, missing attachments, delays and duplication still matter. We requested no documents. [Government search and access explanation](https://search.open.canada.ca/ati/)

Three convenience-sample checks illustrate different next moves:

| Candidate | What the coverage check established | Cheapest useful next step |
|---|---|---|
| 12 pages on Ottawa Treaty withdrawals | The withdrawals and Canada's dilemma were already reported | Compare internal recommendations and their dates with the public account |
| 153 pages on C22 pistol incidents | An existing CBC investigation was corroborated through attributed follow-on coverage and a Senate intervention | Use it as a known-covered control; check whether the release adds any distinct incident or warning |
| Five-page brokering-permit note | The summary lacks the broker, destination, item and decision; no exact match was established | Obtain the note to identify the event before paying for more generic searches |

These are acquisition candidates, not newly verified stories. The coverage checks describe what was discoverable by September 2026, not what a January reader would have known. “No result” in the third case mostly tells us the input is underspecified. Unlike a directly downloadable full-text corpus, this index still needs a document-acquisition step before most substantive analysis. [Detailed walkthrough, links and sampling limits](lead-development/report.md)

## 5. A better Jev → search → Jev loop

### First pass: identify a worthwhile change or question

For a contract modification, supply the original paragraph, parent award, previous relevant action, changed amount/scope/time/place and identifiers. Keep different money concepts separate: a ceiling, obligation, payment and amendment are not interchangeable.

Ask: **What changed, why might it matter, and which missing fact would decide whether this deserves reporting?** Keep a paragraph-only version as the comparison.

### Search: establish what people already know

Start with an identifier or distinctive phrase, then use entity + action + programme and relevant aliases. Articles often omit contract IDs, so an ID-only search is insufficient.

Keep two labels: whether the result is the exact event, another modification, related context or unrelated; and whether it is original reporting, a follow-on, an official release, company material or inaccessible. Ten copies of one wire story are not ten independent investigations.

### Second pass: decide the next reporting move

Give Jev the source packet and actual retrieved coverage, ideally without the first score to reduce anchoring. Ask:

- What specific claim is already established?
- What consequential question remains?
- What one document or factual check would most change the decision?
- What ordinary explanation could account for the apparent anomaly?

Possible answers include pursue, already sufficiently covered, get the defining document, or defer because evidence is inadequate. Do not force a new angle for every record.

Use code for exact joins and arithmetic. Use the model for bounded interpretation. Expand only when a specific missing fact justifies it; stop when another search merely produces more background.

### Re-Jev the nearby evidence, not automatically the whole haystack again

Your proposed second use of Jev is worth testing directly. Once there is a promising question, cheaply collect a bounded set of related records using award IDs, company identifiers, programme names, places and dates. For each candidate passage, ask whether it **supports the question, contradicts it, supplies necessary context or merely repeats something known**. Select a few distinct pieces of evidence and reassess the question with those passages attached.

For example, a modification about “additional scope” could pull in the parent award, earlier modifications and programme documents. The second pass might reveal what the new scope actually is, or show that it was an ordinary option already announced. Both outcomes save reporting time.

A practical first limit is one expansion round with at most thirty candidate passages, followed by a stop/pursue decision. This is an experimental budget rule, not an optimal number. Comparing that version with the same lead without expansion would test your idea more directly than repeatedly asking whether the original paragraph is newsworthy.

## 6. The next experiment I would actually run

**Start with 24 existing contract events**, deliberately including ordinary-looking modifications as well as big awards. This is a method comparison, not an estimate of the entire corpus's story yield.

- Version A: current paragraph-only ranking
- Version B: same event plus parent award and relevant changes
- Hold the human review allowance fixed and hide which version produced each question where feasible
- Preserve sources, prompts, scores, outputs, exact searches, URLs, decisions, failures, elapsed review time and charged costs from the start
- Count distinct questions a reporter would pursue after a short factual check; reject attractive wording without supporting evidence

Separately, use **12 known-covered events** and confusing near-matches to test retrieval and event matching. This diagnoses coverage checks without claiming to measure all-news recall. Then compare a second pass that drops covered events with one that asks what remains genuinely unresolved.

Only after that small comparison, give existing contracts, completed ATI summaries and one other source equal review-time budgets. Keep a random sample separate from deliberately enriched candidates. The winner is useful reporting opportunity per review hour, not the highest model score or largest queue.

Current Exa list pricing observed during this research is $7 per 1,000 ordinary searches with up to ten results: 60 candidates receiving three searches each would be **$1.26 in base search charges**, before other services, optional additions and human time. This is a planning estimate, not a reconstruction of previous bills. Requesting fewer results mainly saves downstream reading; it does not reduce that base search charge. [Exa pricing](https://exa.ai/pricing)

## What was and was not accomplished overnight

**Completed:** original public-document retrieval; an Enron calculation/text/relationship demonstration; a banking-survey extraction and control test; Canadian API access and summary-count checks; three bounded free-web coverage walkthroughs; an independent critical review; reusable scripts and source manifests.

**Not completed:** new Jev or Exa API runs; a model-versus-baseline performance comparison; a claim of earlier journalistic discovery; a complete historical news archive; underlying Canadian release requests; or proof that the proposed second pass improves yield. A USAspending enrichment lookup returned HTTP 503, so that live parent-award join was not demonstrated here.

No paid API purchases or calls, outreach, new credentials or public publication were made. Platform inference and human time were not priced. The next decision is whether the 24-event comparison is worth running, not whether to build a large autonomous newsroom.

### Reproduction files

- [Enron report and portable source pointers](enron/report.md) · [script](enron/run_test.py) · [manifest](enron/manifest.json)
- [Crisis report](crisis/report.txt) · [download script](crisis/download_sources.py) · [analysis](crisis/analyze_occ.py) · [source manifest](crisis/source_manifest.json)
- [Lead-development report and live-probe evidence](lead-development/report.md)

The report date is the intended morning reading date. Source downloads and live checks occurred on 30 September 2026. Downloaded hashes establish which bytes this research used; they do not independently establish the first historical online availability of those bytes.
