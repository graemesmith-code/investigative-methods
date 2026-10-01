# 08. Could old Enron filings support useful questions?

**Question:** With a cutoff of 31 March 2000, could public company filings support a specific reporting question? The 30 September 2026 exercise retrieved original filings, checked figures by hand, and ran arithmetic and simple text searches. It did not run an AI comparison or demonstrate discovery of the fraud.

## What the sources contain

Annual and quarterly filings describe reported finances and transactions. A proxy statement describes matters for shareholders, including some officers' interests. These can establish what a company disclosed. They cannot reveal all private agreements, prove fair prices or establish intent.

The test used four eligible Enron filings and one Duke Energy annual filing for comparison. A later Enron filing was kept outside the main test. One comparison company cannot tell us how often the method would raise false alarms.

## A recipe you can follow

1. Set a historical cutoff and list only documents available by then. Keep filing dates separate from the financial year described.
2. Compare reported profit with operating cash and read the explanations for large changes.
3. Find transactions involving company officers. Read adjacent passages and other filings to identify the parties and their interests.
4. Preserve the company's stated safeguards, and write a question that could test whether they worked.
5. Check earlier journalism before calling the question new.

## What happened

Enron's 1999 net income rose **27.0%** while operating cash flow fell **25.1%**. Yet operating cash was still **1.38 times net income**. A simple rule looking for profit greater than cash would not flag it. Other broad warning signs appeared at Duke too, so they were not unique indicators of fraud.

The more concrete question concerned partnerships managed by CFO Andrew Fastow that transacted with Enron. The proxy also disclosed a **USD38.5 million loan from an Enron affiliate** to one partnership. A reporter could ask who independently priced those deals and how independent the financing really was. The documents described safeguards; this test did not prove they failed.

The proxy itself puts the central conflict in one paragraph. Connecting documents added detail but was not necessary to spot that question. The simple text search also returned irrelevant biographies and missed a nearby passage that used “Fastow” rather than his officer title. No model was tested to show it would fix those mistakes.

## Cost, limits and the next useful step

No paid data or model API calls were used. Platform inference and human time were not priced. The financial inputs were hand-checked, so this was not fully automatic extraction.

The case and rules were chosen with hindsight. A modern model may know Enron's ending; hiding the name would not reliably remove that knowledge. Earlier reporting existed, and the exercise did not establish the first warning. In particular, the 2000-year annual filing arrived on **2 April 2001**, too late to support a claim of beating the March issue of Fortune.

Use this case to check document reading, dates and arithmetic. A meaningful next comparison would select ordinary companies as well as troubled ones before seeing the outcomes, and give simple rules and model-assisted review the same time allowance.

[Technical annex: original filings, chronology, figures and script](../annexes/enron-report.md) · [All experiments](README.md)
