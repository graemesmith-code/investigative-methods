# Venice and the market for fewer AI refusals

**Status: public-source desk research completed 1 November 2026. No service testing or company interviews.**

Venice markets the removal or avoidance of restrictions as a product feature. Its July 2024 explanation of “uncensored” AI says its models were instructed to disregard censorship policies. Its published model card goes further: a recommended instruction disregards legality and safety concerns. Current hosted-service terms nevertheless prohibit illegal use. These are documented company positions, not proof that any particular user obtained an effective weapon or conducted an attack. [S1–S5]

The institutional finding is a market that can distribute less restricted AI assistance beyond the safeguards chosen by original developers. Its significance does not depend on establishing an individual injury. The unresolved question is how much additional usable capability each service supplies.

## Principal findings

1. **Venice is a distributor and a model publisher.** AskVenice is its public handle and model-publisher identity. It offers a hosted interface and programmable access, while its own model release can be used outside the hosted service. Ending a subscription does not recall downloaded weights. The release reviewed is a particular model, not a description of every current Venice model. [S2, S6]

2. **The competitors are not interchangeable.** NanoGPT explicitly markets uncensored and modified open models alongside mainstream models, while its terms prohibit harmful and illegal activity. FreedomGPT markets uncensored options but warns that moderation varies by model. OpenRouter is a general routing intermediary with its own acceptable-use terms; routing through it does not establish that a model's protections disappear. Featherless removes the infrastructure work involved in hosting supported open models, but its terms also require lawful use and compliance with model terms. [S7–S13]

3. **Privacy and safety need separate assessment.** Venice's privacy-mode page distinguishes ordinary hosted routing, contract-based non-retention, and protected-computing modes. It says some upstream providers may retain prompts. Its general privacy policy, however, describes zero-retention obligations for model providers. Its terms also reserve monitoring powers. These documents need reconciliation, rather than an assumption of either total anonymity or comprehensive surveillance. [S3, S4, S14]

4. **There is evidence that removing safeguards matters, but not a service-specific estimate of dangerous uplift.** Tech Against Terrorism's October 2026 CT-AI summary reports that all 13 fully measured models with removed guardrails failed its test. It explicitly says the benchmark does not measure improvement over web search. UK AISI reports improving cyber and scientific assistance on selected evaluations; it does not rank the services considered here. [S15–S16]

5. **Misuse is broader than the “uncensored” market.** ICCT's October 2026 review identified 12 AI-associated violent incidents and plots in Europe and North America, with ChatGPT the most frequently reported service. Its categories include disputed terrorism classifications and incomplete accounts of AI's contribution. Anthropic reports abuse through reseller infrastructure, but those cases do not implicate the companies in this comparison. An empirical cybercrime study also finds adoption more limited and uneven than some broad claims suggest. [S17–S19]

## What changes for nonproliferation

A hosted service supplies remote computation and operating expertise. For a user with adequate connectivity and access, a large local GPU installation is unnecessary. Local electricity demand and chip imports can therefore miss consequential AI use. Programmable access also allows services to become components in larger workflows. These are architectural inferences, not evidence about the behaviour of any named armed group.

When useful models run locally, service suspensions and provider monitoring become still less reliable. Some dependence on hardware remains, but its discriminatory value falls as ordinary consumer devices suffice. Broad inspection of phones, computers or internet traffic would burden lawful users without reliably identifying dangerous intent.

The strongest near-term concerns concern activities delivered mainly through software and communications: fraud, synthetic media, propaganda production and assistance with cyber operations. Physical harm still depends on people, material access, equipment, testing and reliable execution. Scientific question-answering or refusal rates cannot by themselves establish the ability to produce and deploy a biological weapon.

A defensible response would assess the complete distribution chain: original developers, model modifiers, hosting companies, routers and downstream applications. Candidate measures include independent capability evaluations, clear responsibilities between intermediaries, auditable responses to substantiated abuse reports, and narrow restrictions on verified dangerous functionality. These measures should be tested against migration between services and local substitution.

Non-retention is a legitimate protection for journalists, researchers and vulnerable users. It can coexist with preventative controls and privacy-preserving evaluation. Safety assurance should not be equated with indiscriminate retention of private conversations.

## Unanswered reporting questions

- Which current Venice models and privacy modes inherit developer safeguards, add service-level safeguards, or deliberately reduce refusals?
- How do the company's differing statements about upstream retention and monitoring powers fit together in practice?
- What independent tests measure task success, cost, time and reliability, rather than willingness to answer?
- How do each service and its suppliers divide responsibility for abuse detection, investigation and account restrictions?
- Can independent evaluators verify enforcement without obtaining private user conversations?
- What happens to actual task completion when a service intervenes: reduction, delay, or migration elsewhere?
- Is there documented use by particular armed groups? This review found no substantiated link between Venice and ISKP. That is an evidence gap, not proof of non-use.

## Technical annex: method, limits and reproduction

**Scope.** Purposive comparison of Venice, two explicitly uncensored consumer alternatives, and two relevant distribution/infrastructure services. This is not a representative market survey or a ranking of the most permissive models. No model outputs were generated, no accounts purchased, and no provider contacted. No bypass instructions or harmful prompts are reproduced here.

**Evidence hierarchy.** Product pages establish advertising claims; contracts establish stated obligations; neither establishes actual implementation. Published evaluations establish results only within their reported tasks and access conditions. Threat reports are attributed to their authors and do not establish prevalence across all AI use.

**Time.** Pages were read on 1 November 2026. The July 2024 Venice post is historical evidence still publicly available, not a complete current system specification. NanoGPT's reviewed terms are dated 31 October 2026. Model catalogues and policies may change. Search/open retrievals can reflect caches, and failed direct retrievals are preserved rather than treated as negative findings.

**Capture.** The evidence archive contains search/open tool outputs, not complete raw HTML or a forensic website capture. It includes source URLs, line references where returned, retrieval batches, failures and contextual discovery results. NanoGPT's product page was accessible through indexed primary-source search results when direct opening failed. Discovery-only third-party results are not treated as technical evidence.

**Reproduction.** Revisit the source URLs below; compare marketing, terms, privacy and technical documentation separately. Record the access date and policy effective date. Preserve errors. Seek independent, benign task-performance studies before drawing conclusions about additional dangerous capability. No harmful-output experiment was conducted in this review.

**Storage.** Underlying retrieval extracts are stored in the existing Drive research hierarchy:
`My Drive/work/journalism/2026-11-01 Venice and uncensored AI services`.
The package is named `2026-11-01-venice-public-source-research.zip`. Access links are intentionally omitted from this public repository. No private source identities or unpublished project information are included here.

**Evidence integrity.** File `evidence/web-extracts.json`, SHA-256:
`bdc72c51a2277490ee4c8bd2b6a954bed3bebfb5095cc4aac59edcbb145eb0c2`.
This identifies the captured tool-output file, not the original websites. A manifest inside the archive records hashes of the other packaged files.

## Source catalogue

All sources accessed 1 November 2026. Sources are public; claims remain attributable to the publisher.

| ID | Source | Use and limit |
|---|---|---|
| S1 | [Venice: What does uncensored mean?](https://venice.ai/blog/what-does-uncensored-really-mean-in-venice) | Historical company explanation, dated 18 July 2024. |
| S2 | [AskVenice model card](https://huggingface.co/AskVenice/venice-uncensored) | Publisher identity, collaboration and stated model design; not a capability evaluation. |
| S3 | [Venice terms](https://venice.ai/legal/tos) | Illegal-use prohibition, monitoring powers and downstream API responsibilities. |
| S4 | [Venice privacy policy](https://venice.ai/legal/privacy-policy) | Metadata and retention statements; effective 2 June 2026. |
| S5 | [Venice's 2026 alternatives comparison](https://venice.ai/blog/best-chatgpt-alternatives-without-filters) | Current company qualification that hosted services still prohibit illegal content. Competitor rankings not adopted. |
| S6 | [Venice API overview](https://docs.venice.ai/overview/about-venice) | Hosted programmable access and integrations; implementation not audited. |
| S7 | [NanoGPT uncensored product page](https://nano-gpt.com/use-cases/uncensored-ai) | Marketing, through indexed primary-source extracts; direct opening failed. |
| S8 | [NanoGPT terms](https://nano-gpt.com/legal/terms-of-service) | Harmful-use prohibitions and downstream obligations; dated 31 October 2026. |
| S9 | [FreedomGPT FAQ](https://www.freedomgpt.com/faq) | Product scope and model-dependent moderation. |
| S10 | [FreedomGPT terms](https://www.freedomgpt.com/terms-of-service) | Lawful-use requirement and privacy qualification. |
| S11 | [OpenRouter FAQ](https://openrouter.ai/docs/faq) | Routing, metadata and prompt-logging distinctions. |
| S12 | [OpenRouter terms](https://openrouter.ai/terms) | Published restrictions; not an implementation audit. |
| S13 | [Featherless terms](https://featherless.ai/terms) and [product page](https://featherless.ai/) | Hosted inference infrastructure and contractual restrictions. |
| S14 | [Venice privacy modes](https://venice.ai/privacy) | Mode-dependent provider access and retention; claims not independently verified. |
| S15 | [CT-AI Benchmark, October 2026](https://www.ct-ai.org/) | Public summary and methodological qualification; restricted full report not obtained. |
| S16 | [UK AISI Frontier AI Trends Report](https://www.aisi.gov.uk/frontier-ai-trends-report) | Government evaluations; report covers models released through October 2025. |
| S17 | [ICCT operational-use review](https://icct.nl/publication/tell-me-how-make-bomb-terrorist-use-conversational-ai-evidence-and-prospects) | Researchers' 28 October 2026 analysis; underlying cases not separately re-investigated. |
| S18 | [Anthropic September 2026 threat report](https://www.anthropic.com/threat-intelligence-report-september-2026) | Provider-reported abuse and reseller infrastructure; not attribution to reviewed services. |
| S19 | [Hughes, Collier and Thomas: Stand-Alone Complex or Vibercrime?](https://arxiv.org/abs/2603.29545) | Empirical research preprint, revised August 2026; counterweight to sweeping adoption claims. |
| S20 | [Venice About](https://venice.ai/about) | Starting point and current company claims; user counts not independently verified. |

## Follow-up: what experts have actually discussed

**Reviewed 1 November 2026.** Public scrutiny of the distribution model is substantially more developed than assessments of individual commercial services.

**Venice specifically.** Policy Horizons Canada's 2025 foresight report names Venice as an example of AI offered with few safeguards, within a wider discussion of small models and oversight. This is government foresight, not a service audit or necessarily government policy. [S21] Certo Software published hands-on Venice demonstrations in May 2025, reporting phishing and malicious-code generation. Its promotional article does not establish comparative attack success; general expert quotations within it should not be mistaken for Venice-specific assessments by those quoted. [S22]

**NanoGPT specifically.** Targeted public searches did not locate a comparable service-specific assessment by a recognised AI-safety or nonproliferation institution. This is a bounded search finding, not evidence that no evaluation or private discussion exists. Results about Andrej Karpathy's nanoGPT code are unrelated to the commercial nano-gpt.com service. References to AI-safety meetings in the city of Venice are likewise unrelated to the company.

**The biosecurity argument.** RAND's September 2026 study found that reducing refusals could improve models' assistance on its biological-misuse evaluations, without reliable enhancement of underlying capability. It recommends testing modified models and safeguards at third-party inference platforms. Neither Venice nor NanoGPT is named in the report's searchable text. These are model/task evaluations, not demonstrations of completed biological attacks. [S23]

**An explicit counterterrorism disagreement.** In May 2026, Andrew Glazzard, David McIlhatton and Paul Martin argued that efficiency gains were clearer than a fundamental transformation of terrorist capability. [S24] Adam Hadley's July response argues that cheap, accessible models with removed safeguards fit terrorists' established technology preferences. He calls for safety responsibilities to extend to hosting and inference providers. His assessment is an argument about the wider ecosystem, not an audit of these services. [S25]

**Distribution as a policy target.** An October 2026 Belfer Center paper led by Stephen Casper recommends proactive moderation of dangerous modified variants, alongside independent studies of what users can accomplish with AI assistance. It treats distribution platforms as a remaining intervention point. The paper is a scenario-based analysis, not evidence that its imagined event occurred. [S26]

**The counterweight.** Sayash Kapoor, Rishi Bommasani, Arvind Narayanan and colleagues' 2024 framework asks what additional risk open models create relative to existing alternatives. It also recognises openness's benefits. Its historical assessment of limited evidence should not be presented as a current verdict on 2026 models. [S27]

The reporting question is whether commercial distribution makes dangerous assistance sufficiently easier, cheaper or more reliable to alter outcomes, and whether proportionate interventions reduce that assistance rather than merely shifting it elsewhere. No source above establishes use of these services by ISKP.

### Supplemental source catalogue and method

All URLs accessed 1 November 2026. Company-specific exact-name/domain searches were combined with targeted searches of safety, biosecurity and counterterrorism institutions. The search is not exhaustive. No interviews, purchases or harmful-output tests were conducted. Search-result snippets were treated as discovery evidence unless they reproduced the relevant primary publication. Full technical evaluations, policies and claims require separate assessment.

| ID | Primary source | Date and evidentiary role |
|---|---|---|
| S21 | [Policy Horizons Canada, Foresight on AI: Policy considerations](https://horizons.service.canada.ca/en/2025/02/10/ai-policy-consideration/index.shtml) | 2025; Insight 6 explicitly names Venice. |
| S22 | [Certo Software, Unleashed AI](https://www.certosoftware.com/insights/unleashed-ai-hackers-embrace-unrestricted-chatbot-venice-ai/) | 20 May 2025; vendor-led demonstration, authored by Sophia Taylor. |
| S23 | [RAND, Open-Weight AI Models May Increase Biological Misuse Risks](https://www.rand.org/pubs/research_reports/RRA5112-1.html) | 14 September 2026; Sunishchal Dev, Casey O. Barkan and colleagues; technical study. |
| S24 | [Glazzard, McIlhatton and Martin, Will Generative AI Fundamentally Change Terrorist Threats?](https://ctc.westpoint.edu/?p=58094) | May 2026; counterterrorism analysis, CTC Sentinel. |
| S25 | [Hadley, Guardrails Under Test](https://ctc.westpoint.edu/feature-commentary-guardrails-under-test-terrorist-misuse-of-ai-models-and-the-open-weight-abliteration-problem/) | July 2026; benchmark commentary and policy argument. |
| S26 | [Casper and colleagues, A Pre-mortem on the First Major AI-Enabled Terrorism Event](https://www.belfercenter.org/research-analysis/pre-mortem-first-major-ai-enabled-terrorism-event-and-choices-could-enable-it) | 15 October 2026; scenario analysis and governance recommendations. |
| S27 | [Kapoor and colleagues, On the Societal Impact of Open Foundation Models](https://arxiv.org/abs/2403.07918) | February 2024; marginal-risk framework and openness benefits. |

**Measurement caution.** Hadley's July article describes a pilot comparison with web search, whereas the October CT-AI website's FAQ explicitly says its current benchmark is not a measure of uplift over web search. These are not interchangeable measurements; this note does not combine their figures.

**Supplemental archive.** Retrieval extracts, this expanded README and a hash manifest are preserved as `2026-11-01-expert-discussion-supplement.zip` in the same Drive investigation folder named above. The archive contains search/open outputs rather than complete original websites. It preserves discovery results, including rejected and irrelevant hits, for auditability; those hits are not endorsed sources. No private project details are included in this public note.
