# Provenance and recovery limits

The authoritative recovered text is the full saved research page [Rabbit mining claims and ten cross government comparisons](https://chatgpt.com/space/page_8e9a9f5ed4048191b3efe7395d6e15d0). The connected Pages tool returned the full page on 12 October 2026: 132 blocks, sequence 0, created 10:27:53.070752 UTC and updated 10:27:55.928921 UTC. `FINDINGS.md` preserves its complete Markdown; `sources/saved-page.json` preserves the returned structured content and metadata. The archive manifest hashes these recovered files, not the unavailable original downloads.

The delegation identifies original research thread `01a12f6e-7e1f-7282-af80-7d483680c05f` and latest completed turn `01a12f6e-879a-73c7-8a3c-f388553e2e28`. Those identifiers are provenance supplied by the delegation, not a transcript independently recovered here. The original execution environment reportedly went offline during PDF/ZIP packaging. No callable general research-thread reader was exposed; Personal Context returned “Personal context is unavailable for this conversation.” The saved page was recovered directly and read in full.

## Missing artifact manifest

| Artifact | Recovery status and implication |
| --- | --- |
| Original 88-request access ledger | Not recovered. Only aggregate 88/85/3 counts and three described failed routes are preserved; exact timestamps and failed-route URLs cannot be reconstructed. |
| Original discovery query/tool history | Not recovered. Recorded source routes and direct URLs survive in the page; full discovery chronology does not. |
| Raw downloaded HTML, PDF, XLSX, CSV, JSON and bulk indexes | Not recovered. Page-reported byte sizes, counts and locators survive; original bytes and file hashes cannot be independently checked. |
| Essakane embedded original form and workbook relationships | Not recovered as files. Exact embedded path, relationship and cells survive in the profile. |
| Original extraction/comparison code and synthetic control | Not recovered. The page records comparison rules and says a synthetic disjoint-value example exercised code; no original script or output is bundled. |
| Original normalized claims, translations and intermediate tables | Not recovered beyond the saved narrative and specimen values. |
| Original model roles, prompts, token ledger and costs | Not recorded in the recovered page and not recovered elsewhere. No model names, role allocations or spending totals are inferred. |
| PDF/ZIP reading package | Not recovered; completion is not asserted. This Markdown/JSON archive is a new archival deliverable. |
| Full original conversation transcript | Not recovered. The saved page is the source for findings and method. |

The page states no company or regulator was contacted. It documents free access routes, but does not provide a full cost ledger. That is not proof of a particular original model-cost total. This archival task used no paid service calls or third-party outreach.

## Boundaries of verification

Statements such as “downloaded,” “verified” and “HTTP 200” in `FINDINGS.md` are preserved reports of the original research. New scripts under `scripts/` were written only to validate this archive's integrity, simple specimen arithmetic and current source-link availability. They are not original research execution code. Current HEAD responses do not reproduce the original GET/download/parser tests, authenticate document contents, or establish comparability.

The repository was confirmed private before writing. The working checkout matched remote main at `8557d0d9c6b8c1effe2d53e8b95d2425cb6d0e5f`. Existing files were preserved; only index links were added outside this dated directory. No AGENTS.md or applicable local skill files were found in the checkout or selected workspace instruction directories.
