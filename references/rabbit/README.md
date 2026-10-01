# Rabbit originals and version history

For a readable introduction and examples by reporting beat, start with the [catalog guide](../../catalogs/README.md). This directory preserves the original text exports separately from the journalism narratives. Their source descriptions, scores, access claims and cautions have not been silently updated.

## Files to use

| Part | Latest recovered version | Earlier distinct version | System records |
|---|---|---|---:|
| Reader guide | [Rabbit1.txt](originals/Rabbit1.txt) | No distinct later content recovered | 0 |
| Volume 1 | [Rabbit2(1).txt](originals/Rabbit2%281%29.txt), modified 23 September 2026 | [Rabbit2.txt](originals/Rabbit2.txt), original August export | 267 in either version |
| Volume 2 | [Rabbit3.txt](originals/Rabbit3.txt) | Later copy is byte-identical | 298 |
| Volume 3 | [Rabbit4.txt](originals/Rabbit4.txt) | Later copy is byte-identical | 361 |
| Volume 4 | [Rabbit5.txt](originals/Rabbit5.txt) | Later copy is byte-identical | 359 |
| Volume 5 | [Rabbit6.txt](originals/Rabbit6.txt) | Later copy is byte-identical | 270 |

Use the latest recovered version of each part for reading. Retain the original Rabbit2 when comparing what changed. Do not concatenate both volume-1 versions and count their repeated systems twice.

The texts contain Markdown-style headings and stable `SYS` and `AP` identifiers, although their original extension is `.txt`. They can be searched as plain text or parsed by those headings. The original workbook is identified in the provenance; it is not bundled here. We have not reconstructed a missing workbook or substituted newly generated entries.

## Dates, duplicate copies and changes

The six original Rabbit files are byte-identical to exports generated on 19 August 2026 and uploaded under the Rabbit names on 21 August. Six `(1)` copies were uploaded on 17 September. Five are identical to the originals and are represented by their names, dates, sizes and hashes in [provenance.json](provenance.json).

Rabbit2(1) is the distinct copy, modified on 23 September. A comparison with Rabbit2 finds a 223-line inserted GSA/SAM documentation review and one changed description. Its thirty `RAB-GSA-20260923-01` through `-30` identifiers are local review entries. Its 267 global `SYS` identifiers and 745 `AP` identifiers are unchanged.

Upload dates are not source-verification dates. The guide contains notes from several development stages, including earlier counts; do not treat every historical methods paragraph as a description of the final 1,555-record set. The separate 158 → 263 → 345 workbook history is documented in provenance, not represented here as additional unique Rabbit systems.

## Integrity and limits

[Provenance](provenance.json) supplies exact byte sizes, SHA-256 and Git blob fingerprints, original upload/modification timestamps, earlier-export matches and duplicate-copy history. [Local verification](verification.json) records checks performed after transfer into this repository: all seven original files matched; the five original volumes contain 1,555 unique, uninterrupted `SYS` identifiers and 2,516 unique `AP` identifiers.

The transfer archive was decoded and checked outside the repository. Only the seven originals and their provenance were imported; temporary base64 chunks and the compressed archive are not part of `main`.

The originals include partial, unverified and discovery-only sources. We did not retest their endpoints or update their prices, quotas, terms or coverage claims. Targeted credential and privacy checks found placeholders rather than live credentials or private contact details; the files describe record systems, not the underlying personal datasets. The provenance retains the limits of that review.

No separate human byline or compilation-wide license was found. Recovery does not confer rights in third-party records or extend a code license to them. The repository remains private, with its access and licensing unchanged.

[Catalog guide](../../catalogs/README.md) · [Technical annexes](../../annexes/README.md) · [Home](../../README.md)
