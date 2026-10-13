# What changed, what did not, and how to price a pilot

Prepared 13 October 2026. These are design estimates, not tested model bills. Actual incremental cash spend in this research: **US$0**. No paid inference, search, data, or service calls were made. Existing platform access and human/agent time are not priced; zero cash is not zero resource cost. The separate Peru experiment and budget are outside this work.

## The defensible claim

Lower-cost models can make repeated semantic extraction from inconsistent narrative documents more economical: qualifications, exceptions, relationships, product specifications, and the scope of an accounting claim. They do not reveal hidden beneficial owners, payment transactions, protected filings, private invoices, or inaccessible procurement attachments. They do not make aggregate trade statistics evidence against a particular firm.

None of these functions is inherently new in 2026. [OpenAI's 18 July 2024 release](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/) already described text/image inputs, a 128,000-token context window and prices of $0.15 input/$0.60 output per million tokens. Ordinary OCR, rules, document parsing, entity joins and human reading are older still. Avoid retrospective impossibility claims.

There is specific 2026 evidence for a price/capability change: [OpenAI's 30 July announcement](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) reduced Luna prices by 80% relative to its launch prices; [Anthropic's 7 October Haiku 5.5 announcement](https://www.anthropic.com/claude-haiku-5-5) reports lower prices relative to Haiku 4.5. These are vendor announcements and general evaluations, **not evidence of accurate journalism extraction on this corpus**. Cross-document reasoning becoming reliable enough at a low price is a falsifiable hypothesis for a pilot, not a result of this review.

## Current official price observations

Documentation checked 13 October 2026; free page requests and byte hashes are recorded in [pricing-access.jsonl](pricing-access.jsonl). Dynamic page hashes establish fetched bytes, not permanent price guarantees.

| Model / source | Input per million tokens | Output per million tokens | Conditions used here |
|---|---:|---:|---|
| [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna) | $0.20 | $1.20 | Uncached text; each request under 272,000 input tokens. Larger prompts cost more. |
| [Claude Haiku 5.5](https://www.anthropic.com/claude/haiku) | $0.10 | $0.50 | Each request up to 100,000 tokens. Above that: $0.50/$2.50. |
| GPT-4o mini historical launch | $0.15 | $0.60 | 18 July 2024 launch price; context above. |

The root report and proposed budgets use short text chunks, no batch/cache discounts, and no hosted search/OCR/tool surcharges. Output budgets must include any billable reasoning tokens. Tables/image pages may consume more tokens than text; separately measure them before scaling. Do not interpret vendor benchmark claims as a comparison of extraction accuracy.

For an illustrative 1,000-document run, **assume** 8,000 input tokens/document including instructions and 800 output tokens/document, one pass:

- Luna: 8M × $0.20 + 0.8M × $1.20 = **$2.56**.
- Haiku 5.5: 8M × $0.10 + 0.8M × $0.50 = **$1.20**.
- Three full passes plus 20% retry allowance: **$9.22** Luna or **$4.32** Haiku, rounded, before any tools, image input, storage or labor.

This arithmetic measures token exposure, not feasibility. At 10 minutes of human review per document, 1,000 documents mean about **167 hours**, before reporting or translation. Hosting, compute, source licensing and human rates are unspecified; affordable model tokens do not bound the entire project cost. A proposed cash cap of $200 requires an explicit source-access bill, token cap, and human-time allocation.

## Evaluation before spending

1. Define the unit: a tender/award version, company-period-payment type, ownership statement effective date, or exact procurement lot/product. Preserve IDs and provenance.
2. Pick a bounded, reproducible source slice before reading names. Include ordinary controls, missing records and amended documents. Do not begin with famous suspects.
3. Have a human annotate at least 30–50 representative records, including ambiguous translations and ten hard negatives. Keep 20% blind to prompt development.
4. Compare ordinary code (regex/table parser/OCR plus deterministic joins) with semantic extraction. AI must return exact short supporting spans, page/paragraph references, field values, units, dates and an abstention reason.
5. Human-check all proposed contradictions. Record field-level accuracy, abstention, retrieval success, comparable-pair rate, review minutes and dollars. Suggested provisional gate: ≥95% precision for necessary fields on the blind set; zero untraceable assertion accepted; at least 20% reduction in review time at comparable recall. Small samples do not establish production accuracy; report intervals and failures.
6. Stop if underlying records cannot be retrieved permissibly, identifiers cannot be bridged, measurement definitions differ without a documented conversion, or code does the job as cheaply. Stop a supposed scoop if an amendment, timing difference, consolidated scope or another innocent explanation resolves it.

No model test is authorized by this report. The script and prompt in this directory operate locally or describe a future approved experiment; they must not cause paid calls implicitly.
