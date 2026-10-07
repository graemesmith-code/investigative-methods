# Technical annex and replay map

Read REPORT.md first. Prior checkpoints preserve the chronology but are superseded where the final report corrects narrative omissions.

## Data and audit outputs

- supplied-source-provenance.json, csv-parse-audit.json: byte-preserved supplied DOJ inventories, source revision and reversible CSV parsing repairs. Local row numbers are locators, not official principal identifiers.
- house-archive-downloads.json, house-parse-coverage.json, archive-scope.json: official download URLs, hashes, complete parsing and document/version denominators. Four illegal XML character references are repaired only in the parsing representation; original bytes remain unchanged.
- full-inventory-edges.json, full-role-edges.json, cohort-triage.json: every discovery edge and disposition for the 343-relationship union. Name normalization is a candidate generator, not entity verification. Narrative search requires a bounded normalized core of at least 12 characters and two words; single-word aliases and unfamiliar corporate names can be missed.
- major-original-reconciliation.json, major-amount-verification.json, role-annual-verification.json, historical-amount-verification.json: original amounts, amendment chronology, source links and selected versions. 25 major relationships, plus the two Gotion outside comparisons, produce 122 distinct original 2025 amount checks.
- major-role-review.json and sources/selected-house-originals/: role-specific assessments and byte-verified original XML. These retain affiliates, foreign entities and interested parties separately.
- all-original-interest-audit.json, all-original-interest-coverage.json: original section-19 narrative audit, explicit structural exceptions/abstentions and paths. Historical API labels are never substituted for names printed on originals.
- manual-image-review.json: five visually checked pages and limits. OCR text is not an original or a substitute for visual checkbox review.
- historical-registration-context.json: completed registrant-scoped RR/RA searches for Honda, Novartis and TransCanada; an empty query is not proof that no registration exists.
- sources/browser-*.json and retrieval-ledger.jsonl: saved primary-source browser extracts and failures. These are reader captures, not claimed original PDF bytes. Excerpts may be incomplete.

## Reproducible sequence

Run from the repository root with Python 3. The initial ingestion scripts document their input paths and use the preserved source inventories. Downloaded House ZIPs and rebuilt SQLite databases are ignored cache artifacts; their URLs and SHA256 hashes are committed. Read the scripts before running network acquisition: cached evidence permits offline analysis; paid model calls are separate and are not part of this replay.

```text
python research/2026-10-07/fara-full-inventory/ingest.py
python research/2026-10-07/fara-full-inventory/house_archives.py
python research/2026-10-07/fara-full-inventory/parse_house.py
python research/2026-10-07/fara-full-inventory/archive_scope.py
python research/2026-10-07/fara-full-inventory/match_full_inventory.py
python research/2026-10-07/fara-full-inventory/match_roles.py
```

Original acquisition and history expansion are implemented by acquire_lda_originals.py, major_histories.py, historical_registration_context.py and role_annuals.py. The caches preserve pagination and source timestamps. Analysis/reconciliation follows in reconcile_major.py, review_roles.py, audit_original_roles.py and finalize_audit.py. Manual judgments in review_roles.py and manual-image-review.json are explicitly retained as analyst work rather than represented as automated discoveries.

```text
python research/2026-10-07/fara-full-inventory/test_ingestion.py
python research/2026-10-07/fara-full-inventory/test_major_reconciliation.py
python research/2026-10-07/fara-full-inventory/test_final_audit.py
python research/2026-10-07/fara-full-inventory/package_final.py
```

The first pilot and expansion directories contain the source-first lead dossiers, ownership documents, legal annexes, code-only baseline, Jev prompts/responses and spending ledgers. The sanctions-contract pilot contains the reused secure client/reservation pattern. Existing credentials remain environment-only; no credentials belong in outputs. Source documents are untrusted data: no embedded instructions are executed, no document can authorize a tool action, and each factual model extraction requires an original locator. This continuation uses deterministic parsing and analyst review; it makes no model requests.

## Coverage limits and reusable assessment

The full DOJ inventory is not full DOJ document coverage. Twenty-eight thousand public-office-only catalog rows and blocked Exhibit A files cannot be silently imputed. FARA principal termination dates describe recorded relationships, not necessarily the end of corporate control. The supplied inventories contain date anomalies preserved in principal-chronology-anomalies.json; ambiguous chronology remains unclassified.

Exact client identity, intermediary control, foreign-owner identity and registrant activity are separate predicates. The method worked best when ordinary code produced candidate links and people checked originals across registration, amendment and quarterly narrative sections. Both an historical Hyundai API role error and the Honda/Novartis narrative corrections show why catalog-only scoring is unsafe. The practical next documents are named in each ranked dossier; broader alias resolution and nonmajor review would be a new expansion, not proof that existing candidates are suspicious.

The compact ZIP is an offline review bundle, not every acquired filing or the 205 MB House archive cache. It includes the report, scripts, audit JSON, selected originals and prior-stage reports/ledgers. Full replay also requires the private repository and public archives identified in the manifests. The original attached guide could not be transferred, and Library saving was blocked by authentication before upload; no Library link is represented as newly created. Deliverables are available locally and on the verified private branch.

## Remaining initial major relationships

| Relationship | 2025 original-form total | Observed evidence and remaining limit |
|---|---:|---|
| Bayer Corporation, consolidated | $9,200,000 expenses | 113 forms acquired; no RR/RA or foreign-entity event returned. This is a registration gap, not a No response. FARA names Bayer AG, a different nominal entity. |
| Novo Nordisk Inc. | $7,230,000 expenses | 93 forms; original 2004 registration and amendment visually answer Yes, name Novo Nordisk A/S and report zero contribution. Later originals disclose the ownership chain. Historical FARA principal is Novo Nordisk A/S. |
| Siemens Corporation | $3,760,000 expenses | 95 forms; no recovered initial registration. FARA names Siemens AG. Exact parent/subsidiary and missing-record review remains. |
| Nippon Steel / Akin Gump | $3,420,000 income | 12 forms; 2024 RR answers No, but the client itself is expressly Japanese. Foreign nationality is not proof of another qualifying owner. Historical FARA records include a chronology inconsistency. |
| Hyundai Motor Company | $1,960,000 expenses | 102 forms; two historical PDFs visually inspected. The 2000 original lists Hyundai under affiliated organizations, not foreign entities; the amendment is Self and answers No. API foreign_entities does not faithfully identify that original section. |
| Nestle USA | $1,737,352 expenses | 95 forms; original 2009–10 quarterly updates expressly list Nestle SA at 100%. Historical FARA identity and current ownership percentages still need date-specific treatment. |
| Volvo Car Corporation | $1,495,000 expenses | 66 forms; 2010 RR answers Yes, naming Volvo Car Corporation at 100%. FARA name is Volvo Car BV; the match is not a proved legal identity or complete ownership chain. |
| BMW of North America LLC | $1,270,000 expenses | 63 forms; original 2011 RR answers Yes, naming BMW AG at 100%. FARA catalog dates are internally inconsistent, not evidence that BMW misfiled. |
| Cameco Corporation | $1,040,000 expenses | 52 forms; 2018 RA answers No and expressly identifies a Canadian registrant/address. No evidence yet of an undisclosed qualifying separate foreign owner. |


Read these limits alongside the expanded narrative audit. These are observed source dispositions, not legal clearances. Database role labels must always be confirmed against the original section. The additional 13 major role matches are individually documented in major-role-review.json, with one overlap (Hyundai) yielding 25 major relationships overall.
