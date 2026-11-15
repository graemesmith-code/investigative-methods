# Rabbit: a provisional map of possibilities

**Published 14 November 2026; visual redesign published 15 November 2026.** [Open the private Rabbit Site](https://rabbit-source-catalog.automatic-de-6954.chatgpt.site) (owner's ChatGPT sign-in required).

The Site opens as an early draft: “A rough map of new possibilities.” It maps public-record sources for journalism in the age of artificial intelligence without presupposing the questions or a sequence of investigative steps. The opening states the project's working premise: as models improve, journalists may work very differently six months from now. This is a reason to keep the map revisable, not a prediction proved by the catalog.

The owner's rabbit drawings provide the logo and illustrations. Four quiet views offer ways into the collection; detailed controls remain in the notebook.

The preserved catalog remains usable without code: 1,555 historical source systems, 2,516 access methods and 1,739 coverage mappings. It also opens a separate queue of 53 dated review entries: 15 job-posting routes, 12 patent entries and 26 military-technology entries. These supplements are not counted as additional unique historical source systems.

Search and filter by topic, country or jurisdiction, organization, access type and verification. Open a source to follow its original access-method relationships and evidence. Save candidates, review decisions and dated notes; browse coverage gaps and publisher ecosystems; export filtered spreadsheets or the complete catalog and review history.

The catalog is a map to potential evidence. A long list of old access links is useful only if the reporter can see what each link promises, what was actually checked and what still fails.

## Four ways to get your bearings

- **By subject:** interactive counted circles for the ten largest detailed record families, with all 36 observed families available. Clicking Company records opens exactly 167 source systems; Public contracts & spending opens 180. A source may belong to several families.
- **By place:** source counts by the original jurisdiction labels, including provinces and global collections. There are 241 distinct labels, not 241 countries. Search for Italy, for example, to open its 14 systems.
- **By access:** routes for website search, file downloads, data services and update feeds. These groups match words in the imported labels; they overlap and are not new access tests.
- **By certainty:** the distribution of historical checking, kept separate from current decisions to enable a route.

The main illustration suggests a close look at one collection, connections across many, some combination, or uses not yet imagined. The numbered question-first walkthrough has been removed. Counting methods remain optional. The “What’s the catch?” drawing is visible in the main page beside a short explanation of a testable connection. The repeated subject-circle sketch has been removed from the page because the interactive circles already serve that purpose. The notebook retains search, filters, coverage gaps, publisher ecosystems, review work and exports. Detailed imported fields are collapsed by default; provenance is still one tab away.

The design lesson is simple: an interface can quietly impose a method. Rabbit should give people room to discover questions through the records and emerging tools, rather than require them to arrive with a settled question.

The design is deliberately handmade and free in intent. The Site is still owner-only at this stage: the redesign did not change sharing permissions. Individual listed sources may have their own fees or access conditions.

## What makes a connection worth testing

A shared person, company, place or time can provide a reliable trail between datasets. The reporting purpose comes from a separate relationship: a law, regulation or physical constraint that lets us ask, “If A is true here, what must—or must not—be true there?” This is one possible use of the catalog, not a required investigative sequence.

A matched name alone does not establish the same entity; an apparent mismatch does not establish wrongdoing. Check the identity, time and place, and whether the rule actually applies. Then an inconsistency may be a reporting lead worth pursuing. The aim is a useful test of the records, not a connection made for its own sake.

## The job-posting review queue

Open **The notebook → Review queue**, choose **Job postings**, and inspect an entry. Documentation claims, costs, access restrictions and unresolved checks remain visible. ClearanceJobs remains a permission-dependent candidate; building this interface did not perform collection, obtain permission or establish a working bulk route.

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

Source revision published by Sites: `8f030b20b5c52d09b770992c27f3ce4527e0a3d4`. The application source is versioned in the Site's backing Git repository. No credentials, private contact lists, paid source calls or collection jobs were added.

### Mapping correction and visual calculations

Coverage headings contain em dashes between identifiers, jurisdictions and record families. Some jurisdictions also contain an em dash, such as Canada — Ontario. The importer now uses the final separator to identify the family; the previous parser could mistake a province name for part of a topic. MAP-00327 is the regression fixture. Original bytes, identifiers, mapping totals and provenance remain unchanged.

The subject view counts distinct system identifiers per detailed mapping family: 36 families and 1,735 distinct system/family memberships from 1,739 mapping records. All 1,555 systems have at least one family. Circle area represents count, with a small hand-drawn contour; placement and the original sketch's intersections do not encode measured overlap. Small screens use a counted list.

Access group matching uses search/web portal/browse (1,133 methods), bulk/download (1,235), API/web service (1,409), and feed/stream (73). Historical verification counts remain partial 609, carried forward 479, not recorded 369, discovery only 98. Country and province labels are not silently combined.

### Validation

Fifteen data checks passed, including the corrected jurisdiction parser, all ten sketch counts and complete subject membership. The original checks cover: requested counts, unique IDs, bidirectional SYS–AP links, mapping parents, complete detail exports, exact original heading locations, retained original text, SHA256 fingerprints, supplemental IDs and relationships, supplement totals, and no automatic enablement.

Type checking and the production build passed. Browser tests observed search, combined filters, SYS-to-AP navigation, rejected unverified enablement, review persistence after reload, candidate creation, dated notes, filtered CSV download, full JSON download, coverage tables and publisher-to-source-to-method navigation.

The 15 November redesign checks also observed chart-to-record navigation, preservation of a chart selection after reload, homepage search, 26 linked routes for USAspending, collapsed technical fields and filtered spreadsheet export. The home page was checked at desktop width and a 340 CSS-pixel width using browser zoom, with no page-level horizontal overflow. This was a responsive-layout check, not a physical-phone test. Deployment succeeded; the live sign-in gate was observed. Signed-in production browsing remains untested in the test browser.

A subsequent copy-and-layout revision on 15 November removed prescriptive onboarding and reduced the page's visible controls and prose. Browser checks observed all four views, the company chart opening 167 records, Italy search returning 14 records, optional notes opening and closing, and no page-level horizontal overflow at 340 CSS pixels. The access grouping patterns, catalog data, review backend and permissions were unchanged. Type checking and the production build passed before publication; historical data and persistence tests were not repeated for this presentation-only revision.

A further illustration revision on 15 November moved the catch drawing out of collapsed notes, removed the duplicated subject sketch, and explained the distinction between a shared identifier and a testable rule. Desktop preview checks confirmed that the catch image loads once outside the notes, the original subject sketch is absent from the page, and notes still open and close. Type checking and the production build passed. This presentation-only change did not alter the catalog, review database or access permissions.

Future imports must preserve stable identifiers and the separate review database. A changed catalog is a new version of the evidence map, not a reason to erase earlier decisions.
