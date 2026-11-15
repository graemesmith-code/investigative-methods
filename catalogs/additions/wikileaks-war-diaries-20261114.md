# WikiLeaks war diaries: public access and the limits of “full”

Checked 14 November 2026. Rabbit addition: RAB-WARLOGS-20261114.

## Finding for journalists

**The published Afghan and Iraqi war logs can be searched and read publicly. That is not the same as obtaining the entire original, unredacted leak.** No account or proof of journalistic status was needed for the pages checked.

The [official War Diaries explorer](https://wardiaries.wikileaks.org/) reports 76,910 Afghan records and 391,831 Iraqi records. A linked Afghan report opened with its narrative text. These are observed index totals, not independently counted downloads.

The [Afghan release statement](https://wikileaks.org/wiki/Afghan_War_Diary,_2004-2010) says approximately 15,000 reports were withheld for harm minimization. It advertises spreadsheet-compatible and database exports of the public release. This check did not establish that the withheld material was subsequently released or that a complete original corpus is available to journalists on request.

The [Iraq release statement](https://warlogs.wikileaks.org/media/press.html) describes 391,832 reports covering 2004–2009, with May 2004 and March 2009 absent, and explains that information was redacted. Its count is one higher than the current explorer. The reason is unresolved.

**Reporting significance:** these are substantial searchable collections of military reporting. They can support fresh investigations when matched to a specific question and independent evidence. Availability alone establishes neither novelty nor the accuracy of an allegation.

**Plain judgment:** there is enough material here to investigate. The mistake would be to call it a complete picture of either war, or to let an artificial-intelligence system turn a military report into an established fact. Start with a question that matters, preserve the words of the report, and check the people and events behind it.

## Access routes

| Route | What was established | Limit |
|---|---|---|
| [Official explorer](https://wardiaries.wikileaks.org/) | Public collection filters and counts retrieved | No exhaustive crawl or independent count |
| [Afghan search](https://wardiaries.wikileaks.org/search/?release=Afghanistan&sort=date) | Search-results page retrieved | Public release only |
| [Afghan bulk-release page](https://wikileaks.org/wiki/Afghan_War_Diary,_2004-2010) | Advertises compressed comma-separated values, database, web-page and mapping files | Binary download not verified |
| [Iraq release page](https://warlogs.wikileaks.org/media/press.html) | Scope and redaction statement retrieved | No validated full-text bulk file acquired |
| [Explorer source code](https://github.com/yourcelf/afgexplorer) | Maintainer explicitly distinguishes application code from separately obtained records | Cloning the code does not obtain the corpus |
| [University of Pisa teaching dataset](https://didawiki.di.unipi.it/doku.php/dm/warlogs) | Provider describes a filtered, simplified subset; listed fields omit report narrative | Do not treat as complete war logs |
| Original Afghan reporting partners | Contemporary coverage identifies The Guardian, The New York Times and Der Spiegel as recipients of advance material | Asking their archive/investigations desks is a proposed route; present possession and willingness to share were not checked |

Partner context: [contemporary account of advance access](https://www.pcworld.com/article/508139/afghan_war_diary_faq.html). No newsroom was contacted.

## Technical annex: verification and next acquisition

### Checks performed

Public pages were retrieved through web search/open tools. A linked [Afghan record](https://wardiaries.wikileaks.org/id/1026228/) returned structured fields and narrative in its script-free view. No mass extraction, classification, authentication request or legal assessment was performed.

Both official Afghan export links redirected from leakmirror.wikileaks.org to file.wikileaks.org. The retrieval tool could not open those binary targets. This is a tool-access limitation, not proof that the files are unavailable to an ordinary browser.

Advertised targets:

- https://leakmirror.wikileaks.org/file/straw-glass-and-bottle/afg-war-diary.csv.7z
- https://leakmirror.wikileaks.org/file/straw-glass-and-bottle/afg-war-diary.sql.7z

### Minimum useful next experiment

1. Obtain one public-release export, retaining its source URL, retrieval time, original compressed bytes and a modern file hash.
2. Count records and distinct report identifiers; compare against the explorer, and explain differences rather than deleting them automatically.
3. Check that narrative text survives. A casualty table or location extract cannot substitute for the reports.
4. Compare a small sample of downloaded narratives and identifiers against the official pages. Preserve redaction markers, original timestamps and later updates.
5. Test a known incident before treating an empty search as meaningful. Separate “not found in this release” from “did not happen.”
6. Link candidate reports to independent reporting, inquiries or other records; review sensitive names before republishing excerpts.

The public archive, the original leak, and all military records of the wars are three different universes. The Afghan publisher also describes gaps in special-forces, top-secret and allied-force coverage. Even a complete copy of the leak would not remove those limits.

### Machine-readable status

```json
{
  "catalog_id": "RAB-WARLOGS-20261114",
  "checked_date": "2026-11-14",
  "provider": "WikiLeaks",
  "public_explorer": "https://wardiaries.wikileaks.org/",
  "index_counts_observed": {"Afghanistan": 76910, "Iraq": 391831},
  "iraq_release_announcement_count": 391832,
  "count_discrepancy_resolved": false,
  "sample_narrative_retrieved": true,
  "bulk_download_verified": false,
  "original_unredacted_collection_access_verified": false,
  "journalist_only_access_scheme_verified": false,
  "experiment_status": "access_review_only",
  "historical_rabbit_totals_changed": false
}
```

### Catalog placement

This dated review is separate from preserved Rabbit originals and their historical totals. Repository search surfaced the existing WikiLeaks Public Library of US Diplomacy entry, SYS-0050; that is a different collection and does not establish war-diary access. No claim of an exhaustive catalog deduplication is made.

## Follow-up: does OCCRP Aleph hold the withheld Afghan reports?

Checked 15 November 2026. **Unconfirmed. This review did not establish whether OCCRP holds any Afghan War Diary collection, or whether its restricted holdings include the approximately 15,000 reports withheld from the original public release.** Absence from public search results is not evidence of absence from Aleph.

[OCCRP's Aleph landing page](https://aleph.occrp.org/) describes broader access to leaked evidence for accredited journalists. Its [frequently asked questions](https://aleph.occrp.org/pages/faq) say staff can work with journalists and media organizations on bulk exports of specific datasets. Neither retrieved description identifies an Afghan collection or certifies its completeness.

### Useful next step

Ask OCCRP's Aleph team to confirm whether its Afghan War Diary holdings include the original withheld reports, the number of distinct report identifiers, the source/version of the collection, its redaction status, and journalist access/export options. A collection labeled “full” or “91,000 documents” would be a lead, not sufficient proof of completeness.

### Verification limits

Two public search engines were queried for combinations of Aleph, OCCRP, Afghan War Diary, war logs and withheld material. No collection-level record establishing the requested holdings was found. Direct web retrieval of the landing/FAQ pages yielded no readable lines, while search-indexed official text supplied the general access policies. An attempted public collection query at https://aleph.occrp.org/api/2/collections?q=Afghan was inaccessible through the retrieval tool. No authenticated Aleph collection was inspected; no staff member was contacted.

Plain judgment: Aleph is a sensible place to ask, but its large archive is not evidence that it has these particular missing records. Get a direct answer about the version they hold before building a project around it.
