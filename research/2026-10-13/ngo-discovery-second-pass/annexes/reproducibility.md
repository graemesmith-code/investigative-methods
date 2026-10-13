# Reproducibility, decision rules and limits

This annex specifies a future experiment. It does not record a completed pilot. No agent, model or researcher performance figures are available.

## How selection changed

Read alongside the preserved [original selection protocol](../../ngo-discovery-opportunities/annexes/research-protocol.md). The original report's document-interpretation tests remain auditable, but no longer determine editorial priority. The new selection starts with an accountable consequence after a dated event: restriction, operative permission, sanction, title transfer or receipt of returned money.

The gates are: consequential proposition; identifiable subject and operative obligation; dated original evidence; source path for the next event; realistic public observability; alternatives capable of falsifying a suspected contradiction; bounded baseline; human review and stop rule. An incomplete chain can justify an access test but does not become a finding. Method novelty is unnecessary; a new independently defensible fact matters more than a new interface. No unmeasured AI saving is promoted to a demonstrated feasibility change.

Environmental exceptions and survival of public revenue rights are design extensions requested in the synthesis brief. The cancelled third memo was not available. Their source gates are explicitly unresolved; no omitted findings are reconstructed or attributed to an unseen researcher.

## Evidence schema

For each proposed case preserve these fields, using null or unknown rather than a guess:

| Record | Required fields |
|---|---|
| Subject | Stable ID; names and aliases with dates; project polygon/version where relevant; legal entity distinct from brand/operator/beneficiary |
| Obligation | Exact original source and locator; responsible subject/authority; act covered; effective dates; trigger; scope; exceptions; amendments; evidence of termination |
| Event | Actual versus planned act; event/publication/filing/retrieval dates separately; capacity; location; legal recipient; unit/phase |
| Relationship | Edge type; source passage; dates; independent support; uncertainty; possible innocent explanation |
| Source | Requested and final URL; publisher; retrieval UTC; channel/status/type; byte hash if measured; full PDF versus landing page; relevant section actually read |
| Branch | Fact still missing; why it matters; next source; allowed lookup; stopping budget; competing explanation; search result including failed retrieval |
| Outcome | Cleared comparison; verified new fact; candidate contradiction requiring review; unresolved scope; publicly unobservable; retrieval failure |

Do not conflate independently published sources with independent information. An employer quoting an event programme does not supply independent proof of attendance. Duplicated government announcements do not show repeated transfers.

## Branches and next-source rules

| Trigger | Next source | Resolution sought | Stop if |
|---|---|---|---|
| Former official appears in an event programme | Recording/post-event account → official counterpart's dated role/dossier → amendments/permission record | Actual act, personal capacity, covered topic/contact and period | Attendance, scope or permission history cannot be established publicly |
| Excluded business announces sale/rebranding | Acquirer filing/completion notice → registry history → new recipient/award → sanction/project rules | Business continuity, legal recipient and sanction applicability | Essential award/subcontract/transfer records are non-public or identity stays ambiguous |
| Project enters operation | Current licence → predecessor/amendment/appeal → condition-discharge decision/inspection | Applicable phase, prerequisite and actual authorised activity | Effective permission unavailable; field measurement or disputed modelling essential |
| Project receives an environmental exception | Operative exception → implementing permission → beneficiary/title history → dated inspection/outcome | Who benefited, safeguard altered, conditions retained, subsequent consequence | No project-specific decision or causal evidence; an adverse event alone is insufficient |
| Mine sold after enforcement | Title/cadastre/order → transaction/completion → retained-rights schedule → approving act | Same project, changed rights, lawful reinstatement and surviving obligations | Missing annexes/consents or no stable title bridge |
| A public revenue entitlement may survive sale | Original revenue clause → transfer/novation/amendment → recipient-specific public receipt/audit | Whether right survived and whether a specified attributable payment met it | Tax/royalty receipt confidential or pooling unresolvable; private royalties cannot stand in for public rights |
| Asset-return agreement signed | Acknowledged receipt → implementing accounts → disbursement/segment audit → monitoring reports/amendments | Actual receipt, permitted use, attributable expenditure and triggered deadline | No receipt, no expenditure attribution or undatable reporting trigger |

Agents may revise search plans as evidence changes. They must not revise outcome criteria to keep a lead alive. Source failure cannot be changed to a negative fact about the subject.

## Proposed comparison design

1. Freeze the cohort window, inclusion rule, register snapshot, random seed and attrition rules before searching individuals. Report the denominator and inaccessible fraction. Use NGO-famous cases as controls, not as discovery selection.
2. Pre-register two arms: ordinary retrieval/OCR/joins/alerts plus human reading; the same tools plus an agent choosing follow-up sources and interpreting conditional scope. Give equivalent source-access and research budgets. No paid services under the present authorization.
3. Lock factual outcome labels above. Blind-review every proposed contradiction and a sample of cleared/unresolved cases. A domain/legal specialist decides operative scope; model confidence is not a legal conclusion.
4. Include explicit scope controls: Alexis's non-adverse panel inference, employer-service versus personal-client inference, Manaus phased capacity, independent acquisition, expired/stayed sanction, mixed project funds and planned-versus-actual events. Do not label a partially resolved control fully compliant.
5. Measure source-discovery precision, new independently verified consequential facts, proportion with stable identifiers, publicly resolvable fraction, false-positive reasons, researcher correction/review minutes, model/browser usage, and changes caught on repeat checks. A new document is useful only if it resolves a consequential question.
6. Keep the agent only if it improves defensible information per total reviewer hour without increasing material false allegations. Count time spent on failed branches, permissions, source terms, cleared cases and corrections. Repeat-check benefit requires a longitudinal test; none exists here.

Suggested cohort sizes in the supplied memos (20 approvals; 30–50 sanctions; 15 operating projects; 20 mineral projects; 10 tranches) are alternative bounded designs, not a commitment to run all or a justified sample-size calculation. Their analyst-day estimates were not timed. Power, prevalence, total cost and likely story yield remain unknown.

## Source checking in this revision

`source-access-checks.json` is a bounded nine-URL HTTPS check. Raw PDFs/HTML remain in `/tmp/ngo-second-pass-source-cache`, outside Git. Eight responses returned 200 with measured byte counts/hashes; NRGI returned 403 through local HTTPS. The browser separately read NRGI's substantive page, so that access channel is recorded separately. A response hash proves the retrieved bytes, not correctness, completeness, bulk access or permission for external model processing.

The synthesis read Commission PDF pp.6–7 and 10–11 for restrictions, Manaus RIMA pp.8–9 for units/staging, and the two-page prior licence including condition 9. HTML checks used relevant official guidance/announcement sections. The Commission browser initially returned PDF metadata/text but follow-up navigation failed; verified local download and text extraction supplied the specified reading instead. No claim of full-PDF reading is made.

Rerun access checks only if needed, from the second-pass directory:

```bash
python3 scripts/check_sources.py --cache /tmp/ngo-source-check-rerun --output /tmp/ngo-source-check-rerun.json
```

This intentionally writes a new output rather than silently replacing the dated audit. HTTPS verification remains enabled; no denial bypass, login or alternate credential is used. Dynamic pages and hashes may change. No original PDFs are redistributed in the new directory.

Offline validation:

```bash
python3 scripts/validate.py
```

Validation covers relative links, JSON, listed SHA-256 file hashes, old-audit identity against the original commit, and changed-path confinement. It does not rerun research or verify allegations. Immutable GitHub delivery verifies repository bytes separately from external-source correctness.
