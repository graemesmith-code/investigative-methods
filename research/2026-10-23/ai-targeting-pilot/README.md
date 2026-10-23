# AI targeting: a 90-example coding pilot

**23 October 2026. Status: initial inspection set delivered; not a completed comparative news-corpus study.**

## The question

Should machines be allowed to select targets or use force, and on what conditions? Compare attributable US, Chinese and Russian official statements, separating **formal safeguards** from **how officials justify or sell the policy**. Both are substantive objects of research. A change in rhetorical emphasis is not automatically a change in policy.

## What was actually done

A purposive public-web search assembled 90 review examples, 30 associated with each country. A row is a distinct policy proposition or provision, not necessarily an article, speech or independent observation. Source passages were read and the coding received a second AI review. There has been **no independent human-coder validation**.

This was **not an INFINI-NEWS corpus extraction**, random sample, exhaustive retrieval, or longitudinal experiment. The 30-per-country number is an inspection quota. It does not demonstrate equivalent coverage or comparable denominators.

| Evidence origin | US | China | Russia | Total |
|---|---:|---:|---:|---:|
| News-reported claim | 6 | 14 | 3 | 23 |
| Primary-document benchmark | 24 | 6 | 27 | 57 |
| Original document reached through news | 0 | 3 | 0 | 3 |
| Official document republished by news | 0 | 7 | 0 | 7 |
| All review examples | 30 | 30 | 30 | 90 |

There are **15 event/document clusters**: four US, seven Chinese and four Russian. One Russian working paper supplies 23 rows. Of all 90 examples, 67 directly concern targeting, weapons use or control; 21 are broader military-AI context; two are generic-AI inferences excluded from the targeting core. Only **11 news-reported claims** meet the strict targeting/control definition: five US, five Chinese and one Russian. These are yield counts in this selected set, not national prevalence estimates.

The intended observation window was January 2023 through March 2026. Actual coverage is uneven: US examples are from 2023–2024; the Russian examples cover 2023–2025; Chinese examples extend into March 2026. Absence of a selected recent example does not establish absence of relevant statements.

## Findings that survive inspection

1. **“Human control” is not a single measurable position.** Human responsibility, human judgment, decision support, emergency intervention and approval of each individual strike are different claims. The codebook can preserve these differences rather than force them into a yes/no score.
2. **Scope matters as much as apparent stance.** Human-only nuclear-use decisions must not be reported as a blanket ban on autonomous conventional targeting. Chinese and US nuclear statements illustrate this trap.
3. **Detailed conditions are easier to find in policy documents than in this news sample.** Treating document clauses as if they were independent media observations would manufacture a balanced-looking comparison.
4. **Official attribution is a real filter, not an outlet label.** A prominent Chinese news article attributed some human-control advice to an academic, not the official quoted elsewhere in the article. The academic statement was not retained as the government's position.
5. **Opposition to new rules is not opposition to all safeguards.** Russian material can reject a particular human-control term or a new instrument while invoking existing law and other controls. Attribute those positions; do not endorse legal assertions or infer battlefield compliance.
6. **Policy and persuasion need linked, separate coding.** The current pilot codes safeguards. It does not yet quantify arguments about necessity, competition, precision, civilian protection, sovereignty or reassurance. Those are proposed next-stage variables, not completed findings.

These are methodological and source-level findings. They do **not** establish which country is more permissive, national trends, actual operational safeguards, or military capability.

## Inspect the work

- [Methods, codebook and quality review](METHODS.md)
- [90-row data in CSV](claims.csv), with source links, locators, provenance, eligibility and review caveats
- [Same data plus summary in JSON](claims.json)
- [Proposed next steps, not executed](NEXT-STEPS.md)
- [Count and structure verification](verify_counts.py)

The public export contains analytical paraphrases and source references, not full article text or copied source excerpts. Original web pages can change; this export does not provide immutable source snapshots. The delivered review workbook contains the inspection material, but is not required to inspect these structured findings.

No new paid service was purchased for this pilot. Complete model-usage and researcher-time accounting was not captured, so total economic cost is unknown, not zero. The new proposed work is not authorized by the act of saving this record.

[Repository home](../../../README.md)
