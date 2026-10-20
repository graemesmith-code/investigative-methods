# WorldStateMedia and the preparation of public narratives for armed conflict

- **Rabbit addition:** RAB-MEDIA-20261020-01
- **Added:** 20 October 2026
- **Status:** Documentation assessed; research designs proposed. No gated access accepted, bulk corpus downloaded, classification run or predictive result obtained.
- **Record family:** State-media articles, outlet governance classifications and multilingual text.
- **Jurisdiction:** International. Coverage is substantial, not a census of every government, outlet or official narrative.
- **Primary sources:** [WorldStateMedia paper](https://arxiv.org/abs/2610.24990), including Appendix A.3; [English corpus and data card](https://huggingface.co/datasets/manestay/world_state_media_en); [public English URL index](https://huggingface.co/datasets/manestay/world_state_media_urls_en); [FineWeb documentation](https://huggingface.co/datasets/HuggingFaceFW/fineweb).
- **Catalog context:** [Catalog guide](../README.md); [preserved Rabbit reference](../../references/rabbit/README.md). This addition does not renumber or modify the original Rabbit inventory.

## Why this belongs in Rabbit

The interesting question is not whether hostile headlines precede wars. Often they do not, and sometimes they merely describe a war already under way. The stronger question is whether changes in a state's description of another state make particular forms of violence more publicly acceptable, and whether those changes add useful warning beyond existing crisis indicators.

A second, distinct opportunity is to identify technologies that governments are beginning to present as legitimate, necessary or inevitable tools of conflict, then check whether rhetoric precedes procurement, doctrine or deployment.

The proposed product is an evidence-backed early-warning and reporting system, not a machine that predicts wars or determines which territorial claims are true. State-media language can reveal public messaging; it does not establish private intent, popular acceptance or a decision to attack.

## Source and access assessment

The paper, submitted 18 October 2026, describes approximately 118 million records across 136 countries and 114 languages. Cross-crawl deduplication reduces the combined material to approximately 58 million unique-URL articles. Those are not necessarily 58 million independent stories: syndication and rewritten copies require additional treatment. English coverage extends from 2013 to mid-2025; multilingual coverage ends in mid-2024. The paper examines training-corpus representation and source-dependent model answers, not the predictive validity of conflict-warning indicators.

The English data card lists url, id, dump, row_index, base_url, country, typology_2022 through typology_2025, text, date and token_count. Country and governance labels characterize outlets, not each article's target, truth or official endorsement. The source labels come from State Media Monitor. Labels from 2022–2025 must not be silently projected onto 2013 ownership or editorial control.

**Critical timing hazard:** date is a FineWeb crawl date, not an article publication date. The paper's corpus-level consolidation keeps the latest crawl of each URL. Using that version to predict earlier events could leak later text or updates into the apparent past. A valid backtest needs the text actually captured before its forecast cutoff. An old publication date on a later capture is insufficient. Where earlier captures cannot be reconstructed, exclude the item from historical forecasting or use it only for descriptive research.

The English corpus is approximately 101 GB. The public documentation is readable, but access to gated files requires accepting conditions and sharing Hugging Face account information. That step has not been taken. The database is offered under ODC-By v1.0, subject to stated Common Crawl conditions and retained publisher rights; this is not blanket permission to republish article text. Confirm the terms for the exact subset before retrieval or redistribution. No acquisition cost or refresh cadence is assumed; compute, storage and model costs have not been measured.

## Seven experiments worth considering

### 1. The permission to use force index

**Hypothesis:** A shift from naming an adversary to justifying force adds warning beyond generic hostility or coverage volume.

Extract who is speaking, which country is being discussed, what conduct is alleged, which response is defended, and how strongly it is presented as necessary. Distinguish reporting an opponent's threat from endorsing it. Potential signals include force framed as defensive necessity, diplomacy portrayed as exhausted, and progressively broader categories of acceptable coercion.

**Test:** On eligible pre-event snapshots, assess whether within-outlet changes improve forecasts of a separately defined interstate escalation in the next 30 or 90 days. Compare against mention volume, ordinary sentiment and a prior-crisis baseline. Include sustained hostility that never escalated.

**Deliverable:** A dated dyad timeline with original passages and a simple warning rule, followed by an honestly scored holdout test. A finding that rhetoric is loud but uninformative would also be useful.

### 2. The disappearance of off ramps

**Hypothesis:** The narrowing of publicly acceptable alternatives is more informative than an increase in threats.

Track whether negotiations, concessions, intermediaries and limited settlements are presented as feasible, futile or treacherous. Measure the replacement of conditional language by inevitability or claims that no alternative remains. Also track reversals: do de-escalating crises restore legitimate choices?

**Test:** Compare escalating and non-escalating crises involving the same states or outlets. Hold mention volume approximately constant. Ask whether the signal improves on option 1, not merely whether its chart looks persuasive after a war.

**Deliverable:** A paired-case explanatory essay and a reproducible coding guide. This measures public argument, not whether an audience believes it.

### 3. The enemy role switchboard

**Hypothesis:** Changes in the role assigned to a foreign state reveal which relationships are moving toward confrontation.

Build a directed network of attributed roles: partner, rival, aggressor, terrorist sponsor, illegitimate authority or existential threat. Focus on transitions within each outlet rather than absolute comparisons between different languages and media systems. Preserve the distinction between criticism of a government and hostility toward a population.

**Test:** Compare the network's changes with separately dated diplomatic ruptures, coercive measures and military escalation. Keep those outcomes separate: success at anticipating a diplomatic row is not success at forecasting war.

**Deliverable:** An interactive or static narrative map identifying unexpected changes and counterexamples, with an audit trail. Long-standing enemy language may have little marginal predictive value.

### 4. The coordinated permission campaign

**Hypothesis:** A novel justification spreading across distinct state-linked outlets is more informative than one inflammatory editorial.

Track the appearance and uptake of new frames across a fixed panel of outlets, languages and audience types. Remove verbatim syndication before measuring spread; distinguish a shared wire story from multiple editorial choices. Test foreign-facing versus domestic-facing messaging only where audience orientation can be independently established.

**Test:** Compare synchronised reframing with routine coverage of large events and with major campaigns that never culminated in force. Do not label correlation proof of a central directive.

**Deliverable:** A campaign reconstruction showing first observed appearances, independent repetitions and confidence limits. Multilingual coverage ends earlier, so it cannot be treated as a complete 2025 comparison.

### 5. The technology promise to material evidence ladder

**Hypothesis:** A change from vague celebration to concrete doctrine, units, exercises and industrial priorities identifies technologies gaining practical military relevance.

Track the role assigned to a technology: prestige symbol, laboratory experiment, procurement priority, force structure, exercise or claimed deployment. Examples could include autonomy, electronic warfare, quantum sensing or AI-enabled command support. Claims of superiority remain claims, not evidence of capability. A second test should distinguish rhetoric promising cheap, precise, low-risk war from rhetoric claiming an adversary’s technological progress creates a closing window for action. Either may expand the range of violence presented as thinkable, without forecasting what technology actually works.

**Test:** Join dated rhetoric to later public budgets, contracts, procurement notices, doctrine and exercise records. Compare with fashionable technologies that received sustained publicity but little follow-through. Control for global technology hype and require identifiers or corroborated entity matching.

**Deliverable:** Ten claim-to-record dossiers and a small historical test of whether specific language predicts later material commitments. This may be the strongest near-term journalism route even if war forecasting fails.

### 6. Preparing the home audience to bear costs

**Hypothesis:** Enemy construction becomes more informative when paired with explicit preparation for sacrifice.

Track messages legitimising economic hardship, prolonged confrontation, mobilisation or disruption as necessary costs of national security. Keep actual policy announcements separate from rhetorical features, so a model is not credited for “predicting” an event already announced.

**Test:** Ask whether the combination of external justification and domestic cost preparation improves on either alone. Use placebo periods of economic difficulty without armed escalation. Control for censorship changes, source loss and changing publication volume.

**Deliverable:** Matched timelines and an error ledger documenting false alarms. Again, this establishes messaging, not popular consent.

### 7. Testing a precedent abroad before applying it at home

**Hypothesis:** A justification rehearsed in coverage of somebody else's conflict later becomes an argument for the outlet's own state's coercive action.

Track explicit analogies and purported exceptions involving sovereignty, territorial restoration, protection of populations or preventive necessity. Require a textual chain, not an analyst's retrospective resemblance. The first outcome is adoption of the justification in domestic policy discourse; subsequent use of force is a separate outcome.

**Test:** Trace a small prespecified set of claims across time, retaining precedents that never became domestic policy. Hold out later passages and require independent readers to agree on the connection.

**Deliverable:** A sourced argument genealogy: where a permission was tested, how its wording travelled, and when a more authoritative speaker adopted it. Do not infer secret intent from similarities alone.

## Recommended sequence and bounded first pilot

Start with **option 1 paired with option 2** for the conflict-warning hypothesis. Treat **option 5** as a parallel reporting hypothesis with a more concrete external check. Options 3, 4, 6 and 7 are candidate extensions, not features to add until a result appears.

1. **Feasibility gate:** Verify that pre-cutoff captures can be recovered and that source coverage supports stable time series. If not, stop historical predictive claims and design a prospective collection or descriptive study instead.
2. **Small annotation pilot:** Subject to access approval, propose 400 passages across four state dyads, two language tracks and both escalating and non-escalating crisis windows. Include two independent competent readers on a prespecified overlap subset; quote attribution and permissions-for-force categories are the initial coding tasks. The dyads and sampling frame must be chosen before scoring.
3. **Cheap triage:** Begin with metadata, lexical candidate retrieval and deduplication. Consider a small model only after human agreement is acceptable; expensive model review should be reserved for uncertain passages. No paid-model budget or authorised corpus access is assumed.
4. **Temporal evaluation:** Reserve later periods untouched. Fit preprocessing, language thresholds and feature choices on training data only. Check generalisation to held-out countries, not just later months from the same conflict.
5. **Decision output:** A brief go/no-go note, codebook, sample evidence table, coverage/timestamp audit and realistic cost estimate. This is a design proposal, not an experiment already run.

The 400-passage sample is for feasibility and coding, not adequate evidence of predictive accuracy. A performance study needs the full eligible country-dyad/time risk set, including quiet periods. Do not report precision from a deliberately balanced selection of war and peace examples as if it were a real-world warning rate.

## What a credible prediction claim would require

- Define escalation, onset, continuation and technology adoption separately before analysis. [UCDP's event, dyadic and onset resources](https://ucdp.uu.se/downloads/) are candidate outcome sources; specify version and date uncertainty and audit overlap between event reporting and the predictor corpus. [COW MID v5.0](https://correlatesofwar.org/data-sets/mids/) ends in 2014 and is not an adequate default outcome source for a 2013–2025 study.
- Blind annotators to outcomes. Modern language models know famous conflicts: use narrow passage-level coding, not questions asking whether a story foreshadows a known war. Test masking country names and dates; all features must be grounded in the text.
- For a genuine operational replay, account for when an archive became accessible as well as when its crawler captured a page. A historical text-availability test is not automatically a real-time deployability test.
- Use rolling-origin evaluation and report precision, recall, calibration, lead time and false alarms per dyad-year. Rare events make accuracy alone misleading.
- Compare with simple baselines: previous violence, crisis status, seasonality where relevant, mention volume, outlet activity and generic sentiment. A sophisticated language feature must add something beyond these.
- Maintain a stable outlet panel or disclose changes. Deduplicate across URLs and syndication families as well as repeated crawls.
- Audit a stratified sample in the original language. A translated English phrase is not automatically equivalent across languages or political contexts.
- Record a clear abstention state for missing evidence. A quiet scrape is not a quiet government.
- Separate forecasting from causation. Even a useful predictor would not prove that propaganda caused violence or that officials had already decided to attack.
- Do not use Wikipedia's treatment of sovereignty as an independent truth label. The paper's territorial-dispute exercise is an illustration of source effects, not a validated basis for geopolitical adjudication.

## Practical interpretation

The broad ambition is to compare many states, but a credible first result will be narrow. The most valuable outcome may be a repeatable reporting device: identify a changed justification, show when it became prominent, then ask what independently observable action followed. That is more defensible than a global “war probability” map built from undated hostile language.

**Source suggestion provenance:** WorldStateMedia paper and public documentation reviewed on 20 October 2026. The seven experiments and pilot parameters above are proposed research designs, not findings of the paper. No outreach, gated access or data processing has been performed.
