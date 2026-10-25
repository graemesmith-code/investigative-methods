# Archive screening

The canonical JSONL pass in `screen_archives.py` uses Python's standard library
and makes no network requests. The optional auxiliary pass requires `pyarrow`.
Raw inputs and its SQLite database stay in a private workspace outside the public
research package. The script refuses to reuse a populated database.

Run with the three exact, verified Library downloads:

```bash
python3 code/screen_archives.py \
  --archives /absolute/path/FWI-20261016-normalized-research-context.tar.gz \
             /absolute/path/FWI-20261016-normalized-rd-contracts.tar.gz \
             /absolute/path/FWI-20261016-normalized-capabilities.tar.gz \
  --work-dir /workspace/scratch/f4-data
```

An existing normalized input tree can instead be read with `--extracted-dir`.
That route explicitly reports that archive hashes were not verified. Every
individual file receives a SHA-256 inventory entry. No symlinks or special
archive members are extracted; unsafe paths stop the run. Byte-identical files
are accounted as duplicate appearances without rescanning or adding dollars.
All JSONL streams are read through EOF, checking gzip CRCs. Non-JSONL files are
inventoried, and parse/stream failures retain exact file/row/error details.
The expected 22 research-context files and seven descriptive slices have an
explicit basename/row-count check. Missing or mismatched expected files produce
`completed_with_recorded_gaps`, preserving useful partial output without claiming
the whole requested universe was screened.

The complete lexicon and match rules are recorded in `audit/screen-accounting.json`.
All JSONL rows are examined, including contextual, budget, assistance and subaward
rows. Institutional anchors qualify independently; otherwise a safeguard match
must occur in the same source observation as an AI/autonomy/robotics/targeting or
weapons term. Acronyms use token boundaries. This is broad candidate selection,
not proof that a funded, active program implements a safeguard. Full unique
description strings are retained without a character cap.

Only `financial_actions` amounts enter obligation totals. Each exact transaction
key contributes once. A conflicting duplicate is an explicit error. Money joins
use the complete award key; recipient names and PIID normalization never join
dollars. Negative modifications reduce totals. Missing or invalid amounts stay
null and are counted. Corpus nets include every acquired action in the window,
including actions whose own administrative descriptions lack search terms.
SBIR/grant headline amounts and contract ceilings are not added. Exact-key
financial amounts are **net obligations within the acquired action corpus and
named window**, not complete award funding or spending attributable to
safeguards. Acquisition filters can omit older positive, negative and zero
modifications. These nets are therefore not guaranteed lower bounds. Exact
joins, hashes and financial conservation prove internal consistency; they do
not establish that the acquired history is complete. Live complete-history
figures remain source-distinct and must not overwrite the archive sums.

The register retains all A/B/C/D memberships and an automated A>B>C>D primary
category for nonoverlapping accounting only. These assignments require human
review; a word such as "ethical" may describe training, and "certification" may
describe an unrelated engineering objective. Category C can contribute to lawful
operation without explicitly testing LOAC or civilian harm. Candidate-category
dollar subtotals in the audit are labeled accordingly and must not become
verified program totals in a report.

Fiscal windows use the source `fiscal_year` (FY2019–FY2026 and FY2024–FY2026).
An additional calendar window uses action dates from 2024-01-01 through
2026-10-25. Snapshot dates bound actual coverage. All available end-date fields
are retained with their source field names; missing fields are reported as
missing, never taken as proof that an award has ended. No date field establishes
that technical work continued through that date.

The performer trace retains all named-prime/subawardee recipient matches in
2025–2026 and marks textual relevance rather than dropping missing-code cases.
PSC/NAICS fields remain available for review. A recipient-level hit does not
establish an ASIMOV continuation, nor does the absence of a hit establish the
absence of subcontracts or classified work.

Verification performed on 2026-10-25: a private synthetic fixture exercised exact
duplicate financial transactions, duplicate descriptions, a negative modification,
overlapping A/B/C classifications, token-boundary false-positive avoidance and
independent institutional anchors. Expected $100 minus $20 equaled 8,000 integer
cents; three physical financial rows became two distinct financial actions; all
three description observations remained accounted. This fixture tests arithmetic
and mechanics, not completeness or accuracy of the real archive findings.

The public export omits contact email/phone strings embedded in administrative
award descriptions. It records each original/published description SHA-256 and
redaction count in matching list order; no description has a length cap. Full
originals remain private. Recipient-role fields distinguish a reported subawardee
from a prime recipient. Possible same-PIID source keys are cross-referenced for
agency/parent review, without merging dollars or declaring them distinct awards.

## Auxiliary formats and date reconciliation

The archives also contain parquet tables, OCR JSON and text beyond the requested
canonical JSONL datasets. The optional auxiliary sweep requires `pyarrow`:

```bash
PYTHONPATH=/workspace/scratch/f4-screen-deps python3 code/screen_archives.py \
  --auxiliary-only --extracted-dir /workspace/scratch/f4-data-complete/extracted \
  --work-dir /workspace/scratch/f4-auxiliary
```

Every parquet row is parsed. Where a same-basename JSONL exists, rows are compared
for exact semantic equality in source order. Equal rows inherit the canonical
content screen and are counted as duplicate representations. All unequal or
additional rows and all parquet tables without JSONL mirrors are independently
screened. Every OCR page, JSON array record and text line is also screened. The
auxiliary audit reports row counts, mirror equivalence, hashes and failures.
Auxiliary monetary fields never enter the canonical financial sums.

Public auxiliary leads contain source/row/hash identifiers, category terms,
matching field names, corporate performer matches and dates, avoiding raw page
bodies and unnecessary personal details. Full selected rows remain private in
the auxiliary work directory. Raw USAspending source tables expose performance
end dates omitted from normalized JSONL. After both sweeps finish, reconcile
these dates into the main registers with:

```bash
python3 code/screen_archives.py \
  --enrich-end-dates /workspace/scratch/f4-auxiliary/auxiliary-dates.sqlite
```

This joins complete award keys only and leaves money unchanged. All underlying
date observations remain visible, including conflicting same-date values. A
latest end date does not prove active technical work or option exercise.

After the initial full sweep, a fresh editor challenge added CODORD, DONATELLO,
deontic/ethical-constructs and ARMOR2025 aliases. The supplemental pass rechecks
every stored full description for those terms, preserves all previous matches,
and records the initial lexicon gap with revised counts:

```bash
python3 code/screen_archives.py \
  --editor-supplement /workspace/scratch/f4-data-complete/screen.sqlite
```

Run this before final end-date enrichment, since it regenerates the registers.

The initial lexicon recorded in `audit/screen-accounting.json` can be replayed
with `--lexicon-config audit/screen-accounting.json`; the default code includes
the later editor aliases. A second fresh challenge exposed the source office
abbreviation `DEFENSE TEST RESOURCE MGMT CENTER`. Check those raw office fields
and the assistance funding-goals field denominator before the editor pass:

```bash
PYTHONPATH=/workspace/scratch/f4-screen-deps python3 code/screen_archives.py \
  --institution-supplement \
  --extracted-dir /workspace/scratch/f4-data-complete/extracted
```

The editor pass imports the resulting exact-key institutional evidence without
adding financial actions. It separately reports recovered keys and overlaps.
Institutional office affiliation is a candidate lead, not verified safeguards
spending. The raw assistance field `funding_opportunity_goals_text`, omitted by
normalized records, receives an explicit populated/unique-value denominator
check; its content is included in the complete auxiliary field screen.

Auxiliary work can be partitioned by the three extracted archive directories.
Use a different `--package` and `--work-dir` for each partition. Merge completed,
disjoint partitions with repeated `--merge-auxiliary-part PACKAGE WORKSPACE`
arguments and a fresh merged `--work-dir`. The merge checks file disjointness,
candidate-line conservation and date-observation conservation before final
end-date enrichment. Arrow date and decimal columns are losslessly converted to
ISO dates and exact decimal strings for semantic JSONL comparisons; raw money
does not enter the accounting totals.

After merging auxiliary partitions, unify safeguard matches having actual award
keys into the main register, then run end-date enrichment:

```bash
python3 code/screen_archives.py \
  --import-auxiliary-award-hits /workspace/scratch/f4-data-complete/screen.sqlite
```

This records exact-key auxiliary provenance and category overlaps without
importing auxiliary dollars. Full canonical award descriptions remain in the
main register; complete auxiliary match metadata remains in
`evidence/auxiliary-candidates.jsonl`, referenced by source/hash/row from the
main register to avoid duplicating the same metadata. Funding-goals matches
receive a specific warning: a program-level funding purpose does not establish
what an individual award actually tests. Context-only records without actual
award keys and performer-only matches remain auxiliary leads; no award is
invented from a keyword hit.

Validate the final file union and cross-format hashes with
`python3 code/screen_archives.py --validate-complete-coverage`. The completed run
accounts for 100 input files: 36 JSONL streams and 64 parquet/JSON/text files.
The initial count of 37 streams in an interim progress update double-counted
the assistance subaward stream; the final denominator is derived from the
actual inventory. Row counts were unchanged by that correction.

For exact auxiliary lexicon replay, use
`--lexicon-config audit/screen-auxiliary-run-lexicon.json`. The later office
aliases remain an explicitly separate follow-up. Full CSV fields can exceed
128 KiB; the script raises Python's CSV parser field-size limit and does not
truncate those descriptions. The execution-notes register records resolved
format errors and superseded partial attempts.

Run final financial/CSV/hash conservation checks with
`python3 code/screen_archives.py --validate-final-register PATH/TO/screen.sqlite`.
The actual canonical action-date range is **2018-10-01 through 2026-09-30**,
covering FY2019–FY2026. It contains no October 2026 financial actions, despite
the October 16 archive creation date. October continuation checks therefore
depend on live sources. Fiscal and calendar dollar windows are explicitly
separate; future performance dates do not establish funded current activity.

Reconcile every descriptive monetary observation against the canonical ledger:

```bash
python3 code/screen_archives.py \
  --validate-financial-joins /workspace/scratch/f4-data-complete/screen.sqlite \
  --extracted-dir /workspace/scratch/f4-data-complete/extracted
```

This separately verifies exact transaction/award keys, integer-cent action
obligations, action dates and fiscal years. Duplicate descriptive observations
are compared without adding them to money. Subaward rows lacking prime-action
transaction keys are explicitly counted and excluded from prime sums.
