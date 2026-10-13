# Four public-document pilots worth testing with cheap AI

Prepared for Graeme Smith · 13 October 2026 · selective research/design review

**Start with procurement decisions: check whether the authority's explanation matches the bidder's documents under the actual tender rules.** Original rules, evidence and decisions are publicly downloadable and tied together by exact IDs. The difficult work is understanding conditional requirements, scanned attachments and correction stages. That gives cheap AI a specific, testable job.

Three other modest pilots are worth trying: interpret ownership rights and filing histories; distinguish company equity from project/licence ownership; and compare supplier tables with the narrative in the same sustainability report. Public-source controls support all four. **None has produced an investigative finding or measured AI saving.** Agreements and correctly declined comparisons are useful controls.

The initial review applied an unnecessarily strict selection rule: an established method or an unmeasured AI benefit could prevent a design being retained. This revision asks whether accessible public evidence supports a realistic experiment. It preserves the earlier [audit and counts](annexes/initial-review/REPORT.md), expands contextual reading, and keeps missing-evidence and measurement safeguards.

## What “ready” means

- **Pilot-ready:** the original documents and comparison rules are sufficient for a small interpretation experiment. A contradiction and a previously demonstrated saving are not prerequisites.
- **Conditional:** a specific access, processing, identity, date or measurement blocker prevents the consequential test.
- **Rejected:** the proposed claim depends on missing private evidence or a comparison that cannot support it.

A pilot can reuse an old method and still discover new cases later. Today's cheap-model prices do not prove these problems were impossible before 2026. Let a reproducible data slice choose subjects; use known cases solely as controls.

## 1. Does a procurement decision describe the bidder's evidence accurately?

**Why it matters.** A wrongly described missing qualification could exclude a bidder, while an inaccurately accepted qualification could undermine competition. AntAC's [25 May 2026 analysis](https://antac.org.ua/en/news/cabinet-of-ministers-allows-construction-material-prices-to-be-concealed-in-procurement-for-the-reconstruction-of-war-affected-regions/) identifies the risk of requirements tailored to contractors. The narrower public-record test is whether decisions accurately apply published requirements to submitted evidence.

**Proposed experiment.** Take 20 completed civilian construction tenders from a fixed month, using a published sampling seed. For each, compare two material requirements with the bidder's original evidence and the authority's explanation. If a decision says a required document was absent, a valid matching document submitted at the required stage would nominate a question for review. A keyword miss would not.

**What passed access checks.** A [Prozorro control](https://public.api.openprocurement.org/api/2.5/tenders/bc2b85df808042fa8157d6ddbf79d0c6) exposed 63 records; all 33 non-signature documentary files downloaded. An employment archive contained 32 PDFs. Exact tender, lot, bid, award and document-version IDs connect the authority's and bidder's original claims. They are distinct claimant streams in one system, not independent verification of credentials.

The control illustrates the hard parts. Certification was required only when applicable law demanded it. Subcontractor capacity and corrections were allowed. Some uploads occurred after the award and may belong to the winner-evidence stage. Native text extraction failed to recover Cyrillic from the archive. Free Ukrainian OCR recovered readable-script text on two fixed pages; recognition accuracy and credentials remain unassessed. Suitable-language OCR is the baseline, not an AI advantage. No qualification failure or contradiction was established.

**AI's job.** After proper OCR, propose cited requirement–evidence–decision triples; distinguish mandatory, conditional and optional clauses; classify bid, winner and correction stages; connect role descriptions with evidence types. Code retrieves files, preserves IDs and versions, unzips archives and checks dates. A specialist decides legal applicability and whether evidence satisfies a requirement. AI must never infer absence from a failed extraction.

**Prior work and stop rule.** DOZORRO already used [AI risk screening in 2018](https://dozorro.org/blog/yak-shtuchnij-intelekt-dozorro-monitorit-zakupivli), and [proBI advertises document analysis](https://dozorro.org/tools/pro-bi). These are meaningful comparators; they do not establish that this citation-backed, version-aware pairing is already solved. That narrower hypothesis remains unproved. Stop if fewer than 16 of 20 tenders have the necessary histories, or OCR/conditional legal interpretation defeats the comparison. Keep the AI companion only if it maintains the specified accuracy and reduces total expert review minutes.

**Budget:** estimated cash reserve up to US$50; 6–12 specialist hours, rate unknown. Current acquisition/OCR checks cost US$0; no paid model call occurred. [Original passage, complete bundle, temporal safeguards and nine-gate design](teams/revisit_integrity/findings.md).

## 2. Do publicly filed ownership rights support the dated control declaration?

**Why it matters.** Ownership registers become more useful when journalists can distinguish what a company actually declares from what a graph or name match suggests. Global Witness's [The companies we keep](https://globalwitness.org/documents/466/The_companies_we_keep.pdf) proposed shareholder cross-checks. TJN and Open Ownership's [2025 PSC analysis](https://taxjustice.net/wp-content/uploads/2025/05/oo-tjn-research-paper-uk-psc-register-2025-05.pdf) identifies limitations involving ranges, rights and history. A PSC is a person with specified ownership or control interests; the register is not independent proof of the true owner.

**Proposed experiment.** Select five ordinary companies from a frozen registry/date cohort. Reconstruct the publicly documented share denominator, rights and relevant event history, then compare only same-period declarations. A purported mismatch becomes a lead only after amendments, nominees, exemptions and all relevant dates are checked. A confirmation statement marked “no updates” is not an empty shareholder list.

**What passed.** Two preselected controls supplied four PDFs, 17 pages, including scanned rights/transfer/control forms. An additional data-selected check parsed 604,714 rows in one official company-snapshot partition; 41,395 met the stated cohort rule. Its three seeded controls supplied nine incorporation/confirmation PDFs, 92 pages. In their incorporation documents, 44 of 74 pages had almost no native text. Local OCR recovered sampled image pages. One visually checked clause distinguishes inherited/transmitted rights from the right to vote before membership registration. That conditional meaning cannot be inferred from the phrase “same rights” alone.

**AI's job.** Propose page-cited labels for present versus contingent rights, affected holder roles, superseding clauses and effective dates. Code performs OCR, exact company/document joins, arithmetic and chronology. A legally capable human approves operative rights and completeness. Missing private shareholder agreements remain missing; this pilot tests disclosed rights only.

**Prior work and stop rule.** The shareholder/PSC logic is established. The experiment adds a reusable clause-and-event evidence ledger, with the graph/rules approach as baseline. Use only publicly evidenced relationships and [rules operative at the relevant date](https://www.gov.uk/government/publications/people-with-significant-control-summary-guidance/summary-guidance-for-companies-register-of-people-with-significant-control-pscs). Stop when histories or rights are incomplete. Do not scale unless material fields are accurate, conditional-rights controls produce no false contradictions, and review time improves.

**Budget:** estimated cash reserve US$25; 6–12 review hours, rate unknown. Existing downloads/local OCR cost US$0. [Nine-gate rights design](teams/revisit_ownership/findings.md) · [registry-selected and page-quality controls](teams/revisit_psc_root/findings.md).

## 3. Does “100% owned” mean the same thing in the narrative and equity table?

**Why it matters.** Public project descriptions and audited accounts can refer to different ownership interests. A reporter needs to distinguish a genuine inconsistent disclosure from a licence, subsidiary or project-perimeter difference. The Sentry's [Gaming the System](https://thesentry.org/wp-content/uploads/2022/12/GamingTheSystem-TheSentry-Dec2022.pdf), December 2022, gives a concrete public-disclosure starting point.

**Proposed experiment.** Extract an issuer's entire subsidiary table and associated dated ownership narratives, then label 20 pairs. Ask whether a statement of complete equity ownership is compatible with the same unit's disclosed percentage. Licence ownership, consolidated control and indirect project interests are different units; unresolved mappings require abstention. After the control benchmark, discovery would use a fixed exchange/sector roster, not notorious-company selection.

**What passed.** An original [65-page audited financial report](https://ivanhoemines.com/site/assets/files/5195/ivn_q4_2020_financial_statements_final.pdf) and [original issuer release](https://www.ivanhoemines.com/news-stories/news-release/ivanhoe-mines-engaging-in-strategic-discussions-regarding-its-tier-one-assets-in-africa/) were readable. Three conservative controls produced one percentage agreement and two comparisons that must be declined because scope or dates were not bridged. The NGO's named example is already reported; it is not a new lead. An official subsidiary-to-permit/perimeter bridge is still required before alleging false disclosure.

**AI's job.** Classify what a quantifier describes—entity equity, licence, holding company, project interest or accounting control—and preserve qualifications with page citations. Code extracts tables, percentages and dates. Humans validate the exact unit bridge. The prototype is useful even if it learns to reject apparent discrepancies more reliably.

**Stop rule and budget.** Require no false contradiction on the scope traps, accurate fields and reduced total review time against code-assisted human reading. Stop consequential comparisons without same-unit evidence. Estimated optional model reserve US$25; 10–20 human hours. Present public controls/code cost US$0. [Original passage, controls and nine-gate design](teams/revisit_kleptocracy/findings.md).

## 4. Do scanned supplier tables agree with the same report's narrative?

**Why it matters.** Public Eye/FEMNET's [January 2021 Grüner Knopf study](https://www.publiceye.ch/en/publications/detail/does-the-gruener-knopf-deliver-on-its-promise) manually assessed whether company disclosures made risks and responses verifiable. Public reports can be checked for their own factual coherence without access to secret transactions or factory inspections.

**Proposed experiment.** Sample ten entries from the saved official company directory. In each dated report, compare explicit supplier-country and production-stage statements with its sourcing table. Separately label actions as completed, planned, conditional or lacking an outcome measure. Compare only identical periods, stages and group scopes. This tests disclosure consistency, not actual supplier behaviour or certification compliance.

**What passed.** The [official directory](https://gruener-knopf.de/gk-unternehmen) supplied 50 company entries. Its first entry supplied two original company reports totalling 22 pages; all were image-only. Appropriate free German OCR plus ordinary table-grid segmentation recovered all five country cells and 14 of 15 normalized cells in the sampled table. Supplier-country sets agreed within the German report. The older English report concerned a different period; its absence of a later supplier country was correctly not flagged.

**AI's job.** Add multilingual labels for office versus supplier locations, production stage, reporting cutoff, and planned versus completed action; reconstruct difficult table meaning with cited regions. Native extraction, suitable language OCR, grid/table code and manual correction are the baseline. Ordinary code already did much of the clean-table task; semantic AI must earn its place.

**Stop rule and budget.** Double-review 50 fields, include role/period traps, and measure row completeness, material accuracy and human correction minutes. Stop if period equivalence or permitted document use fails. Estimated local-compute cash scenario US$0–50 if suitable hardware exists; 6–12 review hours plus setup, hardware cost unknown. Certification-compliance claims remain conditional: current certificate dates and applicable obligations were not verified, and the restricted normative guide is excluded from AI inputs and redistribution. [Original bottleneck, controls, stronger baseline and nine-gate design](teams/revisit_publiceye/findings.md).

## Conditional opportunities with specific blockers

| Test | What prevents the consequential test now |
|---|---|
| C4ADS server/GPU configuration interpretation | Original Chinese procurement/contract sample remains inaccessible; exact configured variant bridge missing. The proper baseline already includes **371,442 text-searchable documents and GPU/specification keywords**, not announcement-only search. AI must recover residual configuration meaning beyond that. [Evidence](teams/revisit_kleptocracy/findings.md). |
| PPLAAF-derived environmental-assessment site claims | Public assessment and gazetteer controls downloaded, but original Banana assessment, phase/coordinate equivalence and processing terms remain unresolved. A reachable control PDF bears “OFFICIAL USE ONLY”; it was not transmitted to external AI. Citations/comparators must be separated from site assertions. [Evidence](teams/revisit_integrity/findings.md). |
| NRGI/Sherpa payment-to-recipient comparison | Detailed reconciliation annex absent; entity/project, payment category, recipient, currency and recognition definitions unbridged. The sampled residual was already published. No promotion to fill the shortlist. [Audit](annexes/audit/audit.md). |
| Open Ownership land-register exemptions | Current RCI search denied access and legal-title universe is not freely established; exact legal role and date matter. [Evidence](teams/revisit_ownership/findings.md). |
| Multilingual contract carve-outs and amendments | Original paired contracts/complete amendments were not acquired; quotation in an NGO paper cannot replace them. [Evidence](teams/revisit_ownership/findings.md). |

Aggregate trade gaps attributed to firms, sanctions names treated as payments, unavailable bank records and guessed accounting conversions remain rejected. Additional OCCRP reading sharpened plausible public-document tasks but did not supply fresh original counterpart records. [Full rejection/hold ledger](REJECTIONS.md).

## Scale, costs and limits

The [coverage matrix](COVERAGE.md) gives all fifteen organizations' acquisition and reading counts. The targeted pass added 19 unique contextual readings and 10 deeper relevant-section assessments, including a measured low-keyword-hit Public Eye control. Where no local index existed, method-diversity sampling is labelled rather than called low-hit sampling. The corpus and reading remain uneven and English-led; absence of a selected opportunity is not a negative conclusion about an organization's entire decade.

**Actual incremental cash spend: US$0.** No paid model/service calls, outreach, email or allegation investigation. Proposed budgets are estimates; human review and hardware/source costs are separate. [Official dated pricing and assumptions](annexes/why-now-and-costs.md) show that small text-extraction bills can be modest. They do not establish accurate outputs or lower total reporting cost.

The defensible 2026 claim is economic plausibility: affordable semantic processing may reduce the work of interpreting public material already accessible to a reporter. The pilots can falsify that claim. An old method, an agreement control or an unsuccessful AI arm can still produce a useful reusable recipe.

[Coverage](COVERAGE.md) · [source inventory](source-inventory.jsonl) · [opportunity manifest](opportunity-manifest.json) · [technical/revision log](TECHNICAL-LOG.md) · [reproduce](README.md).
