# A living Rabbit catalog

People and assistants can now propose a source, another access method, or a correction note. The home page links to a short form and a sourced change log. Nothing is automatically approved. Accepted new systems extend the source total; new access methods and correction notes do not. Acceptance into the directory is separate from checking and enabling a data route.

The historical graph is flat for a reason: the preserved August export already contains 1,555 systems. September's extra GSA/SAM reviews add no global system identifiers. October preserves the archive; November imports it into the Site. Separate supplements have not been deduplicated into a larger system total. Earlier workbook totals belong to a different catalog. Every approved new source from now on has an actual approval date; the system does not backdate it to a research date.

Five research handoffs are included for human review: EPO Linked Open EP Data as a proposed new service; USPTO export limits; the scope of a CIPO weekly XML part; DPMA official-status checks; and separate INPI national/European records. The last two derive from the recovered 16 November briefing and explicitly flag its missing original acquisition archive. Existing systems stay linked; none is automatically counted as new or enabled.

An assistant can submit evidence quickly. The human still has to decide whether it is useful, distinct and accurately described. Otherwise automation would make a bigger catalog without making a better one.

## Technical annex

- D1 tables `catalog_proposals` and `catalog_changes`, with append-only accepted change payloads. Three schema-only additive migrations. No production data seeded by migration; research handoffs are immutable source-backed proposal fixtures. A fixture is materialized into the proposal table when reviewed.
- Identity is supplied by Sites. Proposals are visible to their submitter and the curator; curated imported handoffs are visible to Site readers. Reviewer authority requires the verified owner email on the server. The client cannot set that flag. Existing private workspace reviews remain private. Sharing permissions are unchanged.
- Submission through MCP `rabbit_submit_proposal` or authenticated POST `/api/contributions` uses the same validation. A unique (user, request key) constraint provides safe retries; changed content with the same key is rejected. Per-caller 100/day limit. No arbitrary SQL or publisher fetches. URLs must be http/https without embedded credentials. Foreign notes are treated as data.
- The approval mutation is intentionally absent from MCP. The curator's form requires an evidence/duplicate review acknowledgement, explanation and matching proposal version. An atomic D1 batch changes the proposal and appends a publication event. Terminal decisions cannot be replayed. Unique publication keys prevent duplicate source-URL or parent/access-URL acceptance across concurrent proposals.
- `/api/catalog` combines the preserved baseline with approved additions and correction notes. New SYS-ADD and AP-ADD identifiers cannot collide with originals. Methods retain parent IDs. Corrections preserve a baseline and append current evidence. They do not rewrite original raw text or silently replace catalog field values. Corrections to specific fields can be proposed as notes for review; field replacement is not implemented.
- Website source search, counts, record drawers, exports and the existing MCP reads use the live layer. `/data/catalog.json` and `/data/full-catalog.json` remain immutable historical exports. The complete UI export includes both originals and `acceptedCatalog` plus the private workspace.
- `rabbit_my_proposals` and `rabbit_changelog` are paginated. `/api/changes` supplies the shared change log, sourced baseline milestones and current total. Request keys and submitter identities are excluded from published records.
- Cross-client fallback: JSON example and schema, plus form import. External clients must support the Site OAuth flow to use its authenticated endpoint directly. Claude and Gemini connectivity is not claimed or tested.

## Validation

Fourteen workflow checks use actual SQLite with the production migrations and a D1 adapter. They cover pending/accepted separation, idempotency, caller isolation, reviewer permission, human acknowledgement, atomic publication, stale decisions, duplicate URLs, original-field preservation, source/method counts, declined/needs-info handling, seed materialization, input validation, historical evidence and exclusion of private request keys. Twenty-one existing catalog/protocol checks also passed with the updated nine-tool schema. Type checking passed.

Desktop browser QA submitted a synthetic local proposal, observed it pending without increasing counts, approved it in the local curator form, observed the change log and count increase to 1,556, and opened the new source drawer with one linked access method. Synthetic test rows were removed from the local preview and are never included in publication. The clean desktop homepage had no horizontal overflow and showed 1,555 again. A physical-phone or effective narrow-viewport test was not completed in this session.

The existing native MCP connection was successfully called before this update. Post-publication evidence is recorded in the repository workflow note. No real candidate is approved by the agent during development.
