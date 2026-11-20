# SID-2 as a document-hunting assistant: a practical trial

20 November 2026. Exploratory methods note, not a controlled benchmark.

## The short version

**Promising as a tireless research assistant; not yet a substitute for a reporter's judgment.** SID-2 helped generate searches, navigate public technical material and shortlist documents. The surrounding workflow produced useful passages and counterevidence. It did not demonstrate that SID reliably identifies the most newsworthy finding, discovers original stories or outperforms another model.

The estimated SID model charge was **about US$0.28**, including two preliminary tests. That excludes the other assistant, web search, extraction, setup and reporting time. It is not the cost of an investigation.

The practical use is to give SID a well-organised collection, let it pursue bounded document trails, then make a human check the original passages, context and novelty.

## What we tried

The question was whether SID-2 could help find public documents relevant to Pentagon AI testing and accountability. This was deliberately open-ended exploration, not a test of whether it could reconstruct an existing story from a fixed document collection.

SID was used as a **search controller**: it chose searches, requested passages and returned ranked document identifiers. It was not a self-contained browser. Our client supplied the tools that actually searched and read sources.

Responsibilities were split:

- **SID:** choose local text searches; request web discovery; select passages to read; rank source IDs.
- **Surrounding assistant/client:** select the initial sources; run web searches; choose URLs to fetch; download and extract source text; execute tool calls.
- **Verification stage:** revisit original documents, distinguish findings from proposals, check qualifications and decide what was useful.

Consequently, neither the discoveries nor the errors can all be attributed to SID alone.

The expanded run began with 30 downloaded sources, approximately 2.58 million extracted characters. The final inventory contained 75 source records. An inventory entry is not proof that its full text was available or that SID read it. Local search was lexical, so source selection and wording shaped what could be found.

## What happened

### Small tests

The first live trial used three paid calls, four model-generated searches and 14 public source records. SID returned eight ranked sources but made no explicit read requests. A useful report was present in the material supplied and absent from its final shortlist; subsequent inspection by the supervising assistant found relevant passages.

A second, more focused trial used six calls, nine searches and four reads. It reached the call limit without returning a final ranking. Its read responses were assistant summaries, not full original-document text. That limits what the test tells us about direct document analysis.

### Expanded exploration and a necessary repair

The larger experiment used raw extracted passages, local search and paged reads, with assistant-mediated web discovery. Four of eight broad episodes stopped at a conservative context-size guard without final rankings. Large chunks were consuming the available working space.

A subsequent four-request pass exposed a defect in **our bridge**. SID supplied range boundaries as separate start/end fields; the original reader expected the range inside the document identifier. The handler ignored those fields and returned document openings instead of the intended passages.

We stopped that pass, preserved the defective calls and repaired the schema/handler to accept both representations. Six subsequent focused episodes completed. The failed reads are not successful page retrievals, and this integration defect is not evidence of a model comprehension failure.

The logs for the expanded experiment record:

| Item | Count |
|---|---:|
| Paid SID requests | 66 |
| Local text-search calls | 114 |
| Web-search requests | 39 |
| Explicit read calls | 24 |
| Final ranking calls | 10 |

These counts include interrupted, denied or defective calls. They are not counts of unique successful searches or entire documents read. Web requests beyond the 20-handoff allowance were denied rather than executed. Search results themselves also supplied passages, so explicit read calls are not a complete measure of text received.

## What was useful, and what still needed a reporter

The workflow helped move from broad claims about AI evaluation to concrete test methods. For example, the public [AIRC report on AI/ML test and evaluation](https://acqirc.org/wp-content/uploads/2025/01/WRT-1071-OY1-v1.1.pdf) describes experiments that withhold categories of training data and test what happens to performance. Its discussion of a notional autonomous-aircraft assessment is a different kind of evidence: a proposed analysis is not a completed operational test.

The related public [CODEX repository](https://github.com/vtnsi/codex) provides an inspectable implementation of coverage and inclusion/exclusion methods. This is not OpenAI Codex. Available code is useful evidence of a deliverable, but does not establish that an operational system had to pass it.

These are examples of the distinction the verification stage had to make, not claims that SID alone discovered the sources. Other results were already known. We did not complete a systematic prior-media-coverage check, so none should be advertised as an original scoop on this basis.

Useful habits that emerged:

- Read conclusions and limitations, not just abstracts.
- Separate a proposed method, a prototype demonstration, an operational test and a mandatory acceptance gate.
- Search for counterevidence, not only material supporting the initial hypothesis.
- Match full project names, award numbers and dates. The same acronym can refer to different projects.
- Treat repeated text in related reports as repeated evidence, not independent corroboration.
- Do not turn failed downloads, paywalls or empty searches into claims that records do not exist.

## Cost accounting

The expanded run's API-reported usage was:

- Input: 2,053,030 tokens, including 1,109,184 cached tokens.
- Output: 11,591 tokens.
- Estimated model charge: US$0.2752821.
- Earlier two tests: US$0.00314935.
- Combined estimate: **US$0.27843145**.

The calculation used the [SID model pricing](https://www.sid.ai/models) recorded for the experiment: US$0.25 per million uncached input tokens, US$0.025 per million cached input tokens and US$1 per million output tokens.

```text
cost = ((input - cached_input) * 0.25
        + cached_input * 0.025
        + output * 1.00) / 1,000,000
```

Cached input is a subset of input. Reported reasoning tokens are already part of output and must not be added again. These are usage-based estimates, not an independently verified invoice or account balance. Prices may change.

The experiment does not establish cost per publishable lead or time saved. Those would require defined outcomes and a comparison.

## A reusable workflow

1. **Define a bounded question.** Ask for documents that could establish or contradict a proposition, not an essay confirming it.
2. **Build a source manifest.** Keep stable IDs, original URLs, dates, retrieval status, document version, extraction method and hashes. Distinguish unavailable full text from available abstracts.
3. **Supply real search and read tools.** A function name in an API request does not execute a search. The client must run it and return the result.
4. **Test the bridge before interpreting the model.** Request a known middle and final passage. Check that returned text and range labels match. Reject malformed ranges instead of silently returning the opening.
5. **Use short, focused episodes.** Set call, spending and context limits. Remind the model of remaining turns and reserve capacity for a final ranked list.
6. **Return originals, not just summaries.** Attach page or line references and inspectable source links. Keep reported PDF-page numbers distinct from printed page labels.
7. **Record each failure honestly.** Log denied calls, extraction gaps, incomplete episodes and repairs separately from successes.
8. **Verify the shortlist independently.** Check every material claim against the source, record counterevidence and check prior coverage before treating a lead as novel.
9. **Keep credentials and confidential reporting out of logs.** This trial used public materials, not private drafts. This public note omits credentials, private communications and unpublished reporting files.

### API integration lessons

An initial request failed with HTTP 400 because it omitted the task body required around the tool definitions. Supplying the task through the instructions field resolved that class of error. The terminal setup also illustrated why a small request file is safer than a long, manually pasted shell command with nested quotes.

Use the current official documentation rather than assuming an OpenAI-compatible endpoint supports every field or tool convention unchanged:

- [SID-2 making a request](https://platform.sid.ai/docs/research-preview/sid-2/making-a-request)
- [SID-2 tools](https://platform.sid.ai/docs/research-preview/sid-2/tools)
- [SID-2 reference implementation](https://platform.sid.ai/docs/research-preview/sid-2/reference-implementation)

Preserve the required final reporting-tool contract, and test the round trip from requested search to client result to ranked IDs. Unit tests and mocked turns validate plumbing, not journalistic usefulness.

## Verdict and evidence boundary

Keep SID-2 in the toolkit for inexpensive, bounded document hunting. Make it return passages and links that a reporter can inspect. Do not mistake a long search log for comprehensive coverage, or a ranked list for a verified finding.

This note summarises the completed 20 November 2026 run report and its recorded usage and failure accounting. It is not a standalone reproducibility package: the full runtime logs and reporting corpus are not published here. There was no fixed benchmark, baseline model, blind relevance assessment or measurement of recall. We therefore cannot infer a model-performance advantage or a reliable rate of original discoveries.

**Good value as a search component. Editorial judgment remains the scarce part.**
