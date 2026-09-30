# Enron: a useful lead-generation replay, not a fraud-discovery claim

Research date: 30 September 2026. Main historical cutoff: end of 31 March 2000.

## Bottom line

This environment can already reproduce a modest, useful financial-records experiment without a paid data service: retrieve original SEC filings, preserve their dates and hashes, calculate transparent financial changes, and find source-backed relationships that justify reporter questions. The small experiment below actually ran.

The strongest Enron lead is relational: an asset buyer and hedge counterparty was managed by Enron's own CFO, with performance-linked economic interests. The annual filing describes an unnamed senior officer; an already-public proxy supplies Andrew Fastow's name and role. Importantly, the proxy's LJM1 paragraph itself contains the CFO relationship and transaction details, so a paragraph-level semantic classifier could flag the core lead without a cross-document join. Joins add identity reconciliation and further detail; whether they improve ranking is a hypothesis for a comparative test.

This does not demonstrate that AI would have discovered Enron's fraud. Enron is a famous, heavily contaminated test case, the rules here were selected after inspecting it, and one comparison company cannot estimate a false-positive rate. The valid result is narrower: contemporaneous public evidence supported specific questions worth investigating, and today's tools can help retrieve and audit that evidence cheaply.

## What actually ran

A standard-library Python script processed the primary document in five contemporaneous SEC submissions: Enron's 1998 and 1999 annual filings, its second-quarter 1999 quarterly filing, its March 2000 proxy, and Duke Energy's 1999 annual filing. Exhibits were excluded from the text scan. The script also keeps Enron's later 2000 annual filing explicitly outside the main test, for a contradiction check.

Sources were downloaded successfully from SEC in the cloud workspace. Some SEC pages failed in the search/open interface, but direct retrieval of the public original documents succeeded. No user computer, paid API, private financial database, external messaging or separate model API was used. Zero paid data/API calls is not a measurement of the platform's inference cost.

The numerical values were manually transcribed and checked against the original source spans. The arithmetic and Boolean rules are automated. Therefore this is a reproducible calculation and text-retrieval demo, not a demonstrated end-to-end automatic table extractor or model evaluation.

### Numerical results from the original 1999 filings

All money values are USD millions. Comparative values come from the same contemporaneous filing, not a later restatement or a modern fundamentals service.

| Calculation | Enron | Duke Energy |
|---|---:|---:|
| Net income, 1998 → 1999 | 703 → 893 | 1,252 → 1,507 |
| Net income growth | +27.0% | +20.4% |
| Operating cash flow, 1998 → 1999 | 1,640 → 1,228 | 2,331 → 2,684 |
| Operating cash flow growth | -25.1% | +15.1% |
| Operating income growth | -41.8% | -26.2% |
| Operating cash flow / net income | 1.38× | 1.78× |
| Operating plus investing cash flow, 1999 | -2,279 | -1,116 |

Sources: [Enron original 1999 10-K](https://www.sec.gov/Archives/edgar/data/1024401/000102440100000002/0001024401-00-000002.txt), income statement and cash-flow statement; [Duke original 1999 10-K](https://www.sec.gov/Archives/edgar/data/30371/0000950109-00-001035.txt), printed pp. 40–41. Exact raw-file line spans are in numeric_inputs.json.

Enron triggers a divergence rule: rising net income alongside falling operating cash flow. But the very common earnings-exceed-cash rule does not flag either company. Enron's reported cash flow was still 1.38 times income. Falling operating income with rising net income and a funding gap after investing flag both companies. Such observations can be useful without being evidence of fraud.

Duke is one contemporaneous comparison, not a certified clean control. Its filing reports a large extraordinary gain and an $800m injury/damages accrual that help explain its mixed headline results. Enron also reports a $441m MTBE impairment. Therefore the raw operating-income declines are not clean measures of recurring-business deterioration. We did not audit every Duke disclosure, scan an industry cohort or establish Duke's later outcomes. The comparison shows non-specificity; it supplies no empirical false-positive rate.

Enron's cash-flow statement includes $2,217m in merchant-asset sale proceeds. Subtracting those proceeds from $1,228m gives -$989m, but this is only a sensitivity illustration: it does not reverse associated costs or establish that sales were improperly classified. It must not be called corrected operating cash flow. A reporter should ask how repeatable the cash generation was.

### Text and relationship results

A deliberately simple rule looks for an officer near a managing-member/general-partner phrase within a whitespace-delimited block. It finds the relevant LJM paragraph in the August 1999 quarterly filing and the 1999 annual filing. It finds no such block in the prior Enron annual filing or Duke's annual filing. That is a string-rule result, not an exhaustive finding that those documents contain no conflicts.

The proxy is a useful failure test: the same rule returns three blocks, including two biographical passages unrelated to the specific LJM transaction. It also misses the subsequent LJM2 paragraph because that paragraph says Fastow rather than repeating his officer title. Section filtering, entity linking and adjacent-paragraph context are needed. We did not run a model to show that it solves those errors.

Human-verified links available by the cutoff:

- Enron's 1999 second-quarter filing, Note 8, says an Enron senior officer manages LJM's general partner and describes Enron shares, a note receivable and a put option in the same transaction. [Original 10-Q](https://www.sec.gov/Archives/edgar/data/1024401/0001024401-99-000020.txt)
- The March 2000 proxy identifies Fastow as CFO and managing member of the general partners of LJM1 and LJM2, and describes a profit share beyond the general partner's proportional capital contribution. It also discloses an outstanding $38.5m Enron-affiliate loan to LJM2. [Original proxy, Certain Transactions, printed pp. 26–27](https://www.sec.gov/Archives/edgar/data/1024401/0000950129-00-001279.txt)
- The annual filing adds year-end asset transactions. Join it to the proxy by the entities and transaction descriptions, not by assuming that every unnamed officer is the CFO. Source pointers and paraphrased relationships are included in the package.

Preserve the company's stated safeguards too: the proxy says other senior officers negotiated transactions at arm's length, and specifies restrictions on Fastow's interest in and voting of the transferred shares. The risk question is whether these safeguards worked, not an unsupported assertion that none existed.

## Chronology and the cutoff trap

| Date | What was public or published | Backtest treatment |
|---|---|---|
| 31 March 1999 | Enron 1998 annual filing | Eligible original baseline |
| 16 August 1999 | Enron Q2 filing, including the officer/LJM relationship | Earliest relevant filing directly inspected here, not a claim of earliest journalism |
| 21 March 2000 | SEC filed-as-of date of Enron proxy | Eligible; document/mail date is 28 March, meeting date 2 May |
| 21 March 2000 | Duke 1999 annual filing | Eligible illustrative comparison |
| 30 March 2000 | Enron 1999 annual filing | Eligible |
| 20 September 2000 | Jonathan Weil's WSJ Texas Journal article on noncash energy-trading gains | Earliest accounting-warning story verified in this search, not proven absolute first |
| 5 March 2001 issue | Bethany McLean, Fortune, “Is Enron overpriced?” | Issue date is established; original first on-sale/online availability is unresolved |
| 2 April 2001 | Enron 2000 annual filing | Too late for a pre-McLean test |
| 9 May 2001 | Peter Eavis, TheStreet, questioned related-party dealings while covering Off Wall Street research | Explicit public partnership warning before October |
| 28 August 2001 | WSJ discussed Fastow's partnership relationship | Also before October |
| 16 October 2001 | Company announced major charges; conference call disclosed equity reduction | Raw facts already public before some subsequent articles |
| 17–19 October 2001 | WSJ investigated partnership losses, equity consequences and benefits to insiders | Major revelations, not first public red flags |
| 8 November 2001 | Enron announced intended restatements | Later outcome evidence, prohibited as earlier input |

Original filing dates: [1998 SEC index](https://www.sec.gov/Archives/edgar/data/1024401/000102440199000007/0001024401-99-000007-index.htm), [1999 SEC index](https://www.sec.gov/Archives/edgar/data/1024401/0001024401-00-000002-index.html), [2000 SEC index](https://www.sec.gov/Archives/edgar/data/1024401/000102440101500010/0001024401-01-500010-index.html). Other dates were verified in original SEC submission headers.

Coverage sources: [Senate report, printed pp. 35, 60–61](https://www.govinfo.gov/content/pkg/CPRT-107SPRT82147/html/CPRT-107SPRT82147.htm); [Fortune archive](https://fortune.com/article/is-enron-overpriced-fortune-2001/); [then-WSJ editor Paul Steiger's account](https://niemanreports.org/not-every-journalist-missed-the-enron-story/); [original October 17/19 articles in the UCLA Loeb submission](https://www.anderson.ucla.edu/documents/areas/adm/loeb/02a14enron.pdf); [SEC chief accountant's December 2001 testimony and chronology](https://www.sec.gov/newsroom/speeches-statements/121201tsrkh-testimony-recent-events-relating-enron-corporation).

TheStreet's original link did not resolve; its title, date and subject are independently documented in the Senate report. An analyst report dated May 6 should not be assumed freely public then. Likewise a magazine issue date is not necessarily the actual first date readers saw it. Later archive timestamps are not evidence of original availability.

The March 31 cutoff precedes the verified Weil story by 173 days. This is potential lead time in a reconstructed record, not evidence that an automated system produced a novel scoop then. Historical news-archive completeness remains unestablished.

## What the public record cannot prove

The source packet can establish disclosed roles, transactions, amounts and accounting descriptions. It cannot establish the undisclosed economics, side agreements, true risk transfer, actual fair values, personal compensation or intent required to prove the fraud.

For example, the SEC's later Fastow complaint describes an undisclosed Cuiaba repurchase/profit guarantee. That later allegation helps identify what evidence a reporter would need, but it cannot be smuggled into a March 2000 detector. [SEC complaint, Cuiaba section](https://www.sec.gov/litigation/complaints/comp17762.htm)

Nor is mark-to-market accounting itself fraud. A system should request assumptions, cash realization and sensitivity, rather than treating an accounting label as a conviction. As an explicitly future-only check, Enron's original 2000 filing reports $4,779m operating cash flow against $979m net income: the cash-below-earnings rule would still fail to flag it. That document is excluded from the main replay.

## The reporter questions worth producing

1. Who independently set and checked prices in transactions with the CFO-managed buyer, and what comparables or competitive bids support those prices?
2. How much independent loss-absorbing capital supports the hedge? What happens if both the investment and Enron's own shares fall?
3. How much of the buyer's purchase money originated with Enron or its affiliates? What recourse, guarantees, repayment and repurchase commitments remain?
4. How much of reported profit and cash generation depends on asset sales, valuation movements and year-end transactions? How does that compare with peers using similar accounting?
5. Why do different public documents use different entity labels, and can every material financial amount be reconciled without double counting?

These are transferable investigation prompts. None requires the model to recognize a famous scandal.

## Changes recommended for the search design

Keep the semantic triage → prior-coverage search → exact-event reassessment chain, and test enriching promising paragraphs into claims supported by small packets of related records. This replay does not demonstrate that paragraph-only semantic ranking misses the core LJM1 lead or that joins outperform it.

- First extract dated facts and relationships, with units, fiscal periods, document IDs, source spans and explicit uncertainty. Do arithmetic in code.
- Add a year-over-year disclosure diff and a relationship join across annual reports, quarterly filings and proxies. Preserve entities and transaction type; maintain coreference rather than assuming same-name/same-party matches.
- Use semantic review to rank bounded reporter questions and identify benign explanations and missing evidence. Require each factual clause to point to an eligible source.
- Search prior reporting for the exact relationship or economic claim, aliases, transaction terms and dates. A story about Enron generally is not necessarily coverage of the same claim; no retrieved match is not proof of no coverage.
- Measure retrieval and novelty judgment separately. Seed known pre-cutoff stories as positive retrieval controls. If the control cannot be found, mark novelty unknown.
- Deduplicate repeats of an unchanged footnote so a long-running monitor alerts on new relationships or material changes, rather than repeatedly rediscovering the same lead.

## A defensible next experiment

1. Freeze the cutoff, source membership, hashes, rules, prompts and reporting budget before looking at holdout outcomes. Split source availability from reporting-period end, and from later discovery of an old private document.
2. Use Enron only for debugging extraction and provenance. Add a pre-specified historical cohort of comparable company-years, including controls, obscure failures and firms that never produced the target story during a defined follow-up period. Match business model and accounting regime where possible.
3. Compare deterministic rules, generic semantic triage, and combined extraction/relationships/diffs. Hold review effort fixed; record time and cost per source-supported, journalist-accepted lead.
4. Have reviewers judge evidence and actionability with outcomes withheld. Separately measure extraction precision, unsupported-claim rate, known-story retrieval recall, exact-event novelty errors, lead diversity and review burden. Do not reduce all of this to a single fraud score.
5. Audit low-ranked and randomly sampled records so misses can be observed. Non-enforcement is not proof that a company was clean; label the outcome and observation window narrowly.
6. Guard against training contamination. Removing company names alone is insufficient: numbers, dates, entities, phrasing and famous footnotes can identify Enron. Use paraphrased/synthetic counterfactual packets for mechanics tests, hidden outcome labels and truly prospective shadow monitoring for the strongest evaluation. Do not claim masking proves the model lacked prior knowledge.
7. End with a reporter-ready evidence packet and next verification action. Stop at a lead when interviews, nonpublic contracts or new authority are required.

A prospective monitor of a narrow public source stream, alongside this historical development set, would answer the practical question better than repeatedly asking a modern model whether it can spot Enron.

## Reproduction and limitations

Run `python run_test.py` in the package directory. It downloads missing SEC sources, checks every source against the supplied reference manifest before numerical computation, writes outputs, and performs no model calls. A missing/invalid reference manifest or mismatched source hash stops the run with an explanatory error; changed download bytes do not replace a validated cache. Cached source copies and full text-candidate outputs remain local; the portable package contains source pointers instead of copied filings. Run `python run_test.py --download` only to deliberately refetch.

This is a small audit with hand-checked numerical extraction, simple paragraph segmentation and post-hoc rules. It proves neither predictive performance, first discovery, causal attribution nor general financial-reporting accuracy. In particular, crude whitespace blocks sometimes contain tables or page artifacts. The hash guard prevents calculations against changed bytes; it does not independently validate the manually transcribed values or make the test blind.

Enron-era filings predate the SEC's mandatory XBRL phase-in, which began for the first group with periods ending on/after June 15, 2009. Expect text/table normalization work rather than assuming current structured-data APIs supply point-in-time 1999 values. [SEC phase-in guidance](https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/interactive-data-financial-reporting)
