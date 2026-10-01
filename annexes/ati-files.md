# Reading the ATI evidence files

This is the supporting-file guide for the [plain-English ATI experiment](../experiments/07-canadian-ati.md). Paths below are relative to the linked directories. Existing data bytes and paths are retained.

## Source and ranking

The [frozen corpus](../research/2026-10-01/ati-cloud-preflight/corpus/) contains the six original response pages, combined `records.json` and `records.csv`, and a manifest and validation record. It has 441 GAC and 793 DND entries, 1,234 total. Pair `owner_org` with `request_number`: request numbers alone are not unique across departments. `_id` is the source record identifier.

`year` and `month` describe request closure, not necessarily the event or first online publication. `pages` means pages released, not pages independently read. Disclosure codes include DA (fully disclosed), DP (partly disclosed), NE (no records), EX (exempted) and EC (excluded); preserve the original source wording when interpreting other fields. Six DA/DP records list zero pages, while one exempted record lists 31 pages. Those source inconsistencies were not silently repaired.

In the [live-run directory](../research/2026-10-01/ati-live/), `full-ranked.json` and `full-ranked.csv` preserve all summaries and model scores. `ranking-prompt.json` defines the questions and weights. `calibration-*` files preserve the seeded 100-record check whose responses were reused in the full ranking. Scores help order reading; neither scores nor model confidence are verified probabilities of a story.

## Searches and decisions

`shortlist-decisions.csv` is the compact record of selected topics and next steps. `editorial-decisions.json` and `branches.csv` preserve decisions after source review. The coverage, control and expansion plan/result files preserve exact searches, order, URLs and metadata. The saved result files omit full third-party article text. `coverage-screen.json` and `branch-evidence-screen.json` contain model assessments, which must be distinguished from final editorial decisions.

**Read the [identity correction](../research/2026-10-01/ati-live/correction-identity.md) before using medical-fairness entries.** Ten historical coverage assessments used the wrong departmental summary. They and the prior conclusion are invalid. `coverage-plans-original.json` preserves the error; corrected metadata elsewhere is not a rerun. `identity-review.json` records the checked associations. Current code rejects the malformed historical plans rather than silently relabeling their assessments.

## Actual documents and costs

`public-sources/` contains selected public government records with source URLs and hashes. `release-ocr/` contains the seven scanned mental-health policy pages, extracted text and page metadata. Automated text reading of an image is called OCR; check it against the image before quoting. `docs/manifest.json` identifies the release retrieval. The publisher's association with the request number is preserved as such; no independent official response letter was obtained.

`cost-summary.json` and `ledger-accounting.json` distinguish estimated Jev charges from Exa-reported usage. The ledger export contains 1,402 Jev calls and 17 Exa searches, with sanitized request/response hashes rather than their full bodies. It is not the private live database and cannot safely restart the run on its own.

`executed-code-provenance.json` fingerprints the API-stage code under [executed-v1](../code/ati/executed-v1/). Top-level [ATI code](../code/ati/README.md) adds continuation and identity safeguards. `archive-file-manifest.json` is a historical archive manifest, including documentation fingerprints from before this editorial restructuring; use [the new verification note](restructure-verification.md) for this change.

[Annex index](README.md) · [ATI narrative](../experiments/07-canadian-ati.md)

## Continuation and the unrun comparison

The corrected medical-fairness screening needs a separately authorized rerun with the original live spending ledger restored and reconciled, not a new empty ledger. The [runner instructions](../code/ati/README.md) explain its continuation guards. The requested OpenAI comparison was blocked on a missing key before any API call; USD0 was spent and there is no comparison result. Neither the archive nor this editorial update supplies credentials or authorizes new calls.
