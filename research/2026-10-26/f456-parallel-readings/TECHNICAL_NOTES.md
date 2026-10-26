# F456 parallel readings technical notes

These notes document the completed F456-scan, F456-jane and F456-jody deliverables and their public audit archive. Full reader outputs are in Drive; this technical record is intended for `research/2026-10-26/f456-parallel-readings/TECHNICAL_NOTES.md`. Research cutoff: 26 October 2026. This storage pass added documentation and verification, not new research.

## Deliverables

- [Drive folder](https://drive.google.com/drive/folders/19SNnoFLsqrCih8LJUm4tg2pF2gz5nboh) under the existing work/journalism folder.
- [Reading guide](https://drive.google.com/file/d/1A7MMsqHZNzGQrJ7SRrprpO5w_77Itr1v/view?usp=drivesdk).
- [Rights-safe public audit ZIP](https://drive.google.com/file/d/1Z2v45vvFwE16SA-v-9BQ7p-qnvCdTAaH/view?usp=drivesdk).

| Reader file | Bytes | SHA256 |
| --- | ---: | --- |
| [F456-scan.txt](https://drive.google.com/file/d/1dyMKss-qHEZpg6xzbiWlTEAlqVV6r8lN/view?usp=drivesdk) | 21383 | `4c41a6fc571e9d505895ed3219b6e6ae6fbf6739076e4837a60e23a0775aab26` |
| [F456-jane.txt](https://drive.google.com/file/d/1LU-DIufLnHMXXHB_hLU49CMK-npoh9R8/view?usp=drivesdk) | 13025 | `36ddd9e1acb36263d7e4afcfd5fe7273d9f582820be4dbda6e89becdeba941d9` |
| [F456-jody.txt](https://drive.google.com/file/d/1Hv_YfMCr0MF6C9_AILTX9vJjo2zQwRJ7/view?usp=drivesdk) | 12382 | `7f9aac08f2165c7c33cc12f4cecc3e49d8cff0f70dcf8472b57a67612ac7b5e7` |

The three reader files were not edited or reuploaded during this archive pass. Each existing Drive object was downloaded through authenticated raw-file access and compared byte-for-byte with the local final file; all three SHA256 values matched. Metadata also confirmed filename, MIME type, size, parent folder and owner. Verification date: 26 October 2026.

The audit ZIP is **53141 bytes**, SHA256 `be3ba07c43e6bffbf9cc18a980506b93ab3c717cf482affe3ce1357dd2e49260`. Its Drive download was verified byte-for-byte and by SHA256 against the local ZIP. The top-level reading guide is **4206 bytes**, SHA256 `0428f39c31f5e5c577ffdf873059a1b8d45ac6b56e7eb8d125ce1d35b48ba00f`; its Drive download was likewise compared byte-for-byte and by SHA256. The Drive metadata adapter did not expose provider-native checksums even when requested: these are hashes of actual downloaded bytes, not claims that Drive supplied SHA256 metadata.

The folder and file metadata showed the existing owner and inherited anyone-with-link reader access. No permissions, audience, ownership or unrelated file organization were changed. No anonymous-access test was performed; verification used the connected account. No private/signed download URL is published.

## Method and source snapshots

**Scan.** A multilingual, geographically bounded press-coverage check compared exact findings from pinned F4/F5 and reviewed F6 source-domain memos with mainstream, specialist and primary publicity. Search/read receipts were retained privately; the public archive publishes exact query strings, authored evidence summaries, access-depth qualifications, overlap/deduplication notes and editorial classifications. It does not republish raw news bodies.

F4 commit: `fa55e8d3d7c69bfc1051279185c7c88df8e92cb6`; report Git blob `f2cb7d94368958a583ee9f064cc62b490791b4f4`.

F5 commit: `9d0165f4fb56f8e16518c87b15f5b4c98b6614a1`; report Git blob `87bd12f2ca9b3dab950882ea5cf1b6a876b43f34`.

The scan's six baseline/memo SHA256 values are preserved in `scan/source-snapshot-sha256.txt`. Portable source-relative labels replace executor-local paths; the source hashes themselves are unchanged. Those underlying baselines and source memos are identified, not bundled in this audit ZIP.

**Jane and Jody.** Original hypothetical interpretive readings, not new source sweeps or audits of every raw financial/occurrence row. They are not actual views of Jane Mayer or Jody Williams and do not imitate either person's writing. Full reports and thematic memos were considered alongside supporting audits, counterexamples and selected original-source checks. Their complete inventories distinguish the synthesis reader's work from team coverage, full reads from selective register fields, historical comparisons from rereads, and inherited findings from fresh checks. There is no claim that one reader personally read every raw source.

Their F6 input was `F6-reviewed-native-dossiers-2026-10-26.zip`, 1,788,824 bytes, SHA256 `f9fb60b07eeeffadf3ef197ac7f686e2666cf482dbec42b515710a86f6a6d725`. The supplied inventories record verification of all 125 ZIP members, including 121 payloads totaling 26,071,407 bytes. Those historical source-bundle checks are reported from the reader receipts, not freshly replayed in this storage pass. All F6 inputs were the reviewed source snapshot, **not the final integrated F6 report**. The earlier publication checkpoint `c0a96ff6bcd9cb586e91140506f01b113019a6a8` was not treated as that final report.

## Models and reasoning settings

- The native scan lead was explicitly launched with **xhigh** reasoning and no model override. It inherited model selection; exact model identity was not independently queried and is not inferred here.
- Jane and Jody cloud jobs were explicitly requested as **gpt-6-astra**, **ultra** thinking/reasoning. Admission accepted those requests, and workers confirmed no fallback. The requested three parallel readers were likewise reported as Astra/ultra requests accepted without fallback.
- These are task-configuration and worker-confirmation claims, not an independent model identity attestation. They do not claim that the coordinating parent's model changed.

## Search counts and exact spend

The exact native query log contains **227 queries**: 73 main-lane queries (65 general and eight ASIMOV follow-ups), 76 Europe queries, ten focused Europe policy-gap checks and 68 Nordic/capital queries. **Eight additional preliminary searches** are disclosed separately: four Europe and four capital; their exact strings were not fully preserved, with capital topics reconstructed. This is at least 235 query attempts, not an entirely exact 235-query log. All promoted evidence was reverified in saved searches/reads; no absence conclusion relies solely on the unpreserved preliminaries.

The coverage register has **53 records, not 53 independent stories**. The editorial register has 28 themes; the UK/Canada coverage selection contains 33 targeted queries. Adjacent context and discarded leads remain distinguished, and wire/interview redistribution is not counted as independent reporting.

**Exa: 0 paid requests; US$0 actual API charges; US$0 reserved or uncertain cost.** The separately approved **US$20** ceiling was unused because working Exa access was not available. Archived Exa outputs were not treated as working API access. Native public-web research continued. No credentials were transferred, accounts created, permissions changed or paid access purchased. No external Exa invoice was independently verified; the zero follows from no paid Exa call being made. This budget is separate from F6. The statement is about separately metered Exa activity, not a general assertion about platform subscription or model service costs.

## Evidence and interpretation limits

A scan finding of no exact mainstream match means only no match found within the recorded search. It does not prove worldwide absence, priority, novelty or a scoop. Robots, paywalls, sparse indexing and qualified extracts limit coverage conclusions. No paywall bypass occurred; legitimate syndication is identified. Primary documents and vendor publicity are not mainstream news coverage. Announcements do not establish implementation, company shutoff assertions are not technical audits, and contract-specific permissions/remedies do not establish a universal military rule.

The readings do not certify current executed licence stacks, unresolved successor/master terms, operational compliance, later litigation posture, implementation or harm outcomes. They preserve the difference between institutional capacity and statutory duties; the strongest institutional-decline finding is bounded to the United States. Missing public evidence is not proof of absent controls. The full inventories preserve more detailed source-specific gaps and access qualifications.

## Later Skydio clarification

F6 QA clarified that the January to early-February 2026 Skydio terms retain a general government-action exception elsewhere even when the weapons-use clause lacks a local exception. A broad “government exception present” register label needs clause-level interpretation; wording variation is not proof that government permission was withdrawn and later restored. The frozen scan describes wording changes and rejects permanent-rollback inference, so no material correction was required. The delivered scan bytes remain unchanged. Jane/Jody do not rely on the detailed chronology. The archive's `CLARIFICATION_LOG.md` records this clarification separately from the original inventories' cautions.

## Exact archive inventory

The ZIP has **14 payloads plus two controls**, 16 members total. `MANIFEST.json` records exact path, size, SHA256, original-source filename/size/hash where relevant, and each presentation cleanup. `SHA256SUMS.txt` covers all payloads and the manifest, excluding itself to avoid circularity. The ZIP hash above covers every member, including both controls. All member names, CRCs, byte counts and SHA256 hashes were checked after construction and the remote ZIP matched the complete local bytes.

| Payload path | Bytes | SHA256 |
| --- | ---: | --- |
| `ARCHIVE_README.md` | 3316 | `2777f3def5a6ed0fadef9c03cf23048c545643a9ffcb71cc736bfc45f13cae8a` |
| `CLARIFICATION_LOG.md` | 1412 | `8b1e3861eabcacad2ff2eac0cad544c42a6d22b067077020e5de53223fd61654` |
| `DELIVERY_FILES.json` | 2204 | `86459042280d32d93a8b31ff942deb6076105f00ba66c73472db46e08920593a` |
| `readings/F456-jane-reading-and-source-inventory-2026-10-26.txt` | 11639 | `53b44699ceed83d5a2400b790eb6c67381e9f6037555aa45c7b953516d523bd6` |
| `readings/F456-jody-reading-inventory-2026-10-26.txt` | 18974 | `a26cdaf523eb6473ee7f79f645e3fdd9c30c1c5559ad4745ae2b57776a6b0a11` |
| `scan/audit-summary.txt` | 3857 | `3e207a1822314b9bc77b43caf29bd3c7e37ae1f5e18da684a69ffc136bab977f` |
| `scan/coverage-evidence-log.json` | 52959 | `fb920c540655349c742fd3402c90dca9a1fee7095b27c5976d27493f855d9b96` |
| `scan/editorial-classification-register.json` | 18790 | `01cd16c3c4d5ffe1b7b46558e53ee624be675aab4399bac0ce72dc32da144548` |
| `scan/exa-cost-audit.json` | 607 | `c5c14a71f917607caf72a852cb65d2ccf0b60fd6aae939329d0feff286aea085` |
| `scan/qa-report.json` | 1428 | `f9c1394ae2836a43e94478b0487afc0641a843be68ceca24c50d9bc65eb5989c` |
| `scan/search-query-cost-log.json` | 58205 | `e568814ec304a30c81ff00b9b40975bad44b0af945826ae6ba92c7270f49d6b5` |
| `scan/source-snapshot-sha256.txt` | 664 | `8fd1143f3371b86c337dad954022bede49253e8c1b7b51f502ea1be554cc2136` |
| `scan/source-snapshot.json` | 894 | `e0636bc41ef26343ee051f429dfa1c6fde8a60b3d342403919e3b93a67fb9a4d` |
| `scan/uk-canada-search-coverage.json` | 9746 | `d8dd23d5d0a3b9d04d6e19dfd2fef4c9ac1c3b77b1d9e689f61a6530ad3a4c82` |

## Rights and presentation handling

The archive is whitelist-only. It excludes `private-search-results/`, `europe/` and `capital/` raw receipts, full news bodies, screenshots, primary-source originals, signatures, drafts and secrets. Relative private-receipt names still present inside query logs are historical provenance references to excluded files, not public links. Public source URLs, titles and brief authored descriptions are retained. Content was reviewed for excessive third-party quotation, private/signed URLs and credential-like material before upload.

Cleaned inventories retain the complete substantive source/reading-scope information. Removed material is limited to private Library references, executor-local paths, irrelevant transfer/authentication mechanics and obsolete delivery-blocker text. Scan audit publication flags were explicitly tied to their historical pre-delivery freeze rather than misrepresented as current state. These are **presentation cleanups, not changes to findings**. The original source hashes and exact cleaned payload hashes are both retained in the manifest; exact original reflection receipt hashes are in DELIVERY_FILES.json. The three main reader outputs are unchanged.
