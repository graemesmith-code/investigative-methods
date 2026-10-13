# Reproducible NGO opportunity review

Start with [the plain-English report](REPORT.md). The revised report ranks four pilot-ready document-interpretation opportunities and separates specifically blocked designs from rejected inferences. No investigative finding or measured AI saving is claimed. The initial zero-finalist audit is preserved in `annexes/initial-review` and Git history.

- [Coverage and gaps](COVERAGE.md): all fifteen organizations and distinct stage counts.
- [Rejections](REJECTIONS.md): concrete reasons, linked to original source passages in team ledgers.
- [Technical log](TECHNICAL-LOG.md): methods, access failures, corrections and limits.
- [Complete source inventory](source-inventory.jsonl), [machine index](machine-screen-inventory.jsonl), [counts](coverage-counts.csv) and [totals](totals.json).
- [Selection manifest](opportunity-manifest.json): four pilot-ready methods, six selected blocked designs/extensions, nine-gate evidence and later reporting safeguards.
- [Cost/why-now annex](annexes/why-now-and-costs.md), [protocol](annexes/research-protocol.md) and [independent audit](annexes/audit/audit.md).

## Targeted revision

Read the new ledgers for [procurement/ESIA](teams/revisit_integrity/findings.md), [rights/history](teams/revisit_ownership/findings.md), [registry-nominated controls](teams/revisit_psc_root/findings.md), [issuer scope/GPU](teams/revisit_kleptocracy/findings.md), [supplier disclosure and low-hit sample](teams/revisit_publiceye/findings.md) and [additional OCCRP methods](teams/revisit_occrp/findings.md). Source versions append their reading flags; repeated reads do not inflate unique counts. [Revision deltas](revision-deltas.json) preserve initial/current stages and changed judgments. Corporate/procurement test documents remain outside NGO corpus totals.

## Validate the saved result

With Python 3.12+ (standard library), run from this directory:

```sh
python scripts/consolidate.py
python scripts/build_coverage.py
python scripts/validate.py
```

`validate.py` checks schemas, counts, exact original-line pointers, machine-index joins, reading-stage integrity, JSON parseability, local Markdown links and file hashes. It makes no network or paid calls. `file-manifest.json` records committed research-file hashes; generated validation outputs and the manifest itself are excluded from self-hashing. Re-running acquisitions will change metadata and therefore invalidate old file hashes until a deliberate new run is recorded.

## Reacquire sources or bounded data controls

Read each team's README/findings and scripts first. Downloaded copyrighted reports and complete original tender records were stored under `/tmp`, not committed. They may disappear with this environment. Hashes and original public URLs identify what was obtained; they cannot replace the source bytes or promise perpetual retrieval.

- [Global Witness / GFI / Public Eye](teams/global_trade/findings.md): `census_publiceye.py`, `check_public_data.py`, `machine-screen.py`; browser catalog IDs/URLs are discovery provenance, not persistent executable content references.
- [OCCRP / Sentry / C 4 ADS](teams/kleptocracy/README.md): browser-assisted metadata plan and `build_inventory.py`; batch-body mismatches explicitly downgraded. Do not treat a cached header as attributed source text.
- [TJN / Open Ownership / NRGI](teams/secrecy_ownership/README.md): sitemap/census, selected acquisition, bounded DRC sources and machine index.
- [Spotlight / Sherpa / Basel](teams/legal_enforcement/findings.md): `census.py`, `acquire.py`, `machine-screen.py`; publication attachment selection excludes recurring site-navigation PDF links.
- [TI / PPLAAF / AntAC](teams/integrity_whistleblowers/findings.md): TI catalogs, custom PPLAAF endpoints, bounded `prozorro_pilot.py` and `prozorro_compare.py`. Fresh public attachment URLs are regenerated from stable tender/document IDs; transient signatures are not committed.
- [Independent UK/DRC controls](annexes/audit/audit.md): `reproduce_audit.py`, byte hashes, minimal workbook cell locations and missing-annex evidence.

Local text extraction uses `pdftotext`; DOCX/XLSX parsing uses standard ZIP/XML tools. Some scripts may require the available `lxml`/`pypdf` packages; their imports and execution paths remain visible. Cache names differ by team and are documented in their code. No script is intended to perform a live allegation investigation, use paid models, contact anyone or evade denied access. The [future extraction prompt](annexes/extraction-prompt.txt) is a design artifact, not an inference call.

`check_pricing.py` reads current official model documentation only; it does not call an inference endpoint. Estimates use dated official observations, explicit token assumptions and separately unpriced human/source costs. Actual incremental cash spend in this run was US$0.

## Scope and provenance

13 October 2016–13 October 2026, or founding through review day. English-led official-source census with identified translation deduplication, substantial known gaps and purposive deep reading. TI national chapter checks were purposive, not exhaustive. AntAC is the Ukrainian Anti-Corruption Action Centre. This is source discovery and methods design; no email, outreach, paid test or wrongdoing finding was performed. Repository privacy and unrelated work were preserved on a separate branch.
