# Rabbit: a browsable source catalog and review workspace

**Published 14 November 2026.** [Open the private Rabbit Site](https://rabbit-source-catalog.automatic-de-6954.chatgpt.site) (owner's ChatGPT sign-in required).

The Site makes the preserved Rabbit catalog usable without code: 1,555 historical source systems, 2,516 access methods and 1,739 coverage mappings. It also opens a separate queue of 53 dated review entries: 15 job-posting routes, 12 patent entries and 26 military-technology entries. These supplements are not counted as additional unique historical source systems.

Search and filter by topic, country or jurisdiction, organization, access type and verification. Open a source to follow its original access-method relationships and evidence. Save candidates, review decisions and dated notes; browse coverage gaps and publisher ecosystems; export filtered spreadsheets or the complete catalog and review history.

The catalog is a map to potential evidence. A long list of old access links is useful only if the reporter can see what each link promises, what was actually checked and what still fails.

## Start with the job-posting queue

Open **Review queue**, choose **Job postings**, and inspect an entry. Documentation claims, costs, access restrictions and unresolved checks remain visible. ClearanceJobs remains a permission-dependent candidate; building this interface did not perform collection, obtain permission or establish a working bulk route.

New candidates keep separate identifiers. Link them to an existing source system only when that relationship is established. Record a decision in **Review & notes**. The Site saves it online and retains the prior decision.

## What “enabled” means

No historical record was automatically enabled. Original “Final active” flags are preserved as historical statements. An individual access method or candidate route can be enabled only after the user records a payload check, check date, evidence link, decision and a review of access/reuse conditions. A system is enabled when at least one of its original methods is enabled.

Enabled routes remain separate from the candidate queue. Parked and rejected candidates remain available for inspection. Enabling a route does not run a collector or call the source.

## Limits and ongoing maintenance

- This is a **14 November 2026 snapshot plus a persistent review workspace**. The Site does not automatically synchronize with GitHub or refresh external source records.
- No source endpoints were retested while building it. Historical verification dates are not upload or import dates.
- Coverage views count catalog records. They do not measure the completeness of real-world data or news coverage.
- Publisher groupings use the recorded publisher, with an official-domain fallback where missing. They are catalog relationships, not proof of organizational control.
- Reviews and notes are scoped to the signed-in user. Current access is owner-only.
- Full JSON exports retain original record text, source/access links, coverage mappings, provenance and current review state. Spreadsheet exports are available for simpler use.
- Publication succeeded and the live sign-in gate was checked. Functional tests ran in the development preview; a signed-in production browser test was not completed because the test browser had no ChatGPT session. Preview test data was not published.

## Technical annex

### Sources and reproducibility

Imported repository revision: `88ebd891e75d6448ecf7420ac2df3e6c1f0565a5`.

The importer uses `references/rabbit/originals/Rabbit2(1).txt` and `Rabbit3.txt` through `Rabbit6.txt`. The earlier Rabbit2 is excluded to avoid double-counting volume 1. Original SYS, AP and MAP identifiers stay unchanged. Supplemental RAB identifiers are retained, with explicit related-system links where present.

Each parsed record has a commit-pinned source-file URL and original line number. The complete original system text is retained. All five volume fingerprints match the existing verification manifest.

Files alongside this note:
- [Standalone importer](import_rabbit.py): rebuilds the read-only catalog from a checked-out copy of the source repository.
- [Import audit](import-audit.json): counts, SHA256 fingerprints and import rules.
- [Validation record](validation.json): automated integrity checks, browser checks and verification limits.

Rebuild without fetching any source endpoints:

```sh
python import_rabbit.py --source-root /path/to/investigative-methods --output-root /path/to/rabbit-export
```

This produces read-only catalog JSON, individual source records, full export data, target identifiers and review seed metadata. It does not alter the source checkout or enable routes.

### Site implementation

The Site uses a server-rendered React application with static catalog assets and a durable database for three tables: `reviews`, `candidates`, `review_events`. Source records are immutable; reviews are an overlay. Schema migrations contain no seed dataset. Database changes preserve history.

Production requests require the Site's authenticated identity for workspace operations. Updates are scoped to that identity and reject stale review versions. Source URLs permit only http/https, source text is rendered as text, and spreadsheet formula prefixes are neutralized in exports.

Source revision published by Sites: `960f6db4814e7388fb8e7dbb9f23b6dd4c36349b`. The application source is versioned in the Site's backing Git repository. No credentials, private contact lists, paid source calls or collection jobs were added.

### Validation

Twelve data checks passed: requested counts, unique IDs, bidirectional SYS–AP links, mapping parents, complete detail exports, exact original heading locations, retained original text, SHA256 fingerprints, supplemental IDs and relationships, supplement totals, and no automatic enablement.

Type checking and the production build passed. Browser tests observed search, combined filters, SYS-to-AP navigation, rejected unverified enablement, review persistence after reload, candidate creation, dated notes, filtered CSV download, full JSON download, coverage tables and publisher-to-source-to-method navigation.

Future imports must preserve stable identifiers and the separate review database. A changed catalog is a new version of the evidence map, not a reason to erase earlier decisions.
