# 05. Rank the original contract paragraphs

**What we tried:** move from headline-level triage to the original paragraphs in Pentagon contract announcements through the Paragraph Lead Test prototype.

**Why:** the paragraph can distinguish an initial award, option, modification, amount, location or scope. A short headline often loses the feature that makes a change worth examining.

**What happened:** the Paragraph Lead Test was published on 27 September. Historical publication was verified. The next reported large run, on 29 September, used 10,000 original contract paragraphs and is documented separately in [experiment 06](06-jev-exa.md). This page records the prototype milestone; publication alone supplies no performance result.

**What it cost:** actual build, hosting and per-run model costs were not recovered. Reviewer time was not recorded. No cost-effectiveness claim follows from the prototype's existence.

**What remains uncertain:** the supplied evidence lacks a pinned code revision, exact ranking prompt, corpus date range and saved paragraph-level outputs. Current live functionality has not been tested for this notebook.

**Why it matters:** a reviewer should see the sentence that caused a record to be ranked highly, with its source and date. Preserving that evidence makes it possible to decide whether a model has selected meaningful changes or merely familiar, prominent companies.

## Prototype references

- [Replit project](https://replit.com/@smithg5/Pentagon-Jev-Lead-Test)
- [Published application](https://pentagon-jev-lead-test.replit.app)

## The reusable unit should be an evidence card

For each paragraph, keep an immutable ID, original text, source URL, publication date and any action date stated in it. Add a clear explanation of the proposed news value. Keep the model's score and exact prompt/version beside the record, not in place of the original text.

For a contract, distinguish ceiling, obligation, payment and potential value. Do arithmetic and date comparisons in code. Ask a model a narrow question about stated content, such as whether a paragraph explicitly describes changed scope. Do not ask it to determine whether wrongdoing occurred.

A reviewer should be able to reject an apparently interesting card because it is an already-described option, routine support or a company-name coincidence. Keep those rejections: they are useful examples for evaluating the next version.

## Proposed comparison

Use the same manually reviewed set for simple rules and model ranking. Compare worthwhile records retained, top-ten usefulness and reviewer minutes. Audit a random sample of rejected records for missed important items. The winner is the method that makes review better at a measured cost. No such controlled comparison has yet been demonstrated by the supplied prototype evidence.

[Experiment index](../../experiments/README.md) · [Home](../../README.md)
