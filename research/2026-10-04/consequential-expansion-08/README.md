# What the three new routes actually cost to check

**55 reviewed formulations remain; this pass adds none.** The consolidated ranking contains 70 cards, including 15 refinements. Three bounded access checks retrieved one public source-reference record, one well-identity record and one historical trial version. None supplies an end-to-end investigation, a violation or a patent-invalidity finding.

## Practical decision

| Route | Verified free evidence | Unresolved bottleneck | Decision |
|---|---|---|---|
| J01 media chronology | Public Airwars incident links to source ID, original URL and captured/post dates | Archive entry is text without original media; independent payload retrieval failed | Small pilot only; next-check effort rises from 2 to 3 |
| REF-AER stop/restart | Entering one preselected licence in the public form returned its UWI and identity | Operation/cessation timestamps and original restart consent not acquired | Defer bulk matching; effort remains 4 |
| J02 trial/patent | One historical registry version rendered in a free browser | Public availability of the relied-on wording, granted claim and complete priority chain | Defer scaling; specialist work dominates, effort remains 4 |

All three remain readiness tier 3 because the decisive evidence is unresolved. A newly obtained component does not automatically make the next decisive check cheap. No consequence score or incomparable raw scale was used to reorder the cross-batch ranking. Ties remain deterministic by test ID. The ranking measures readiness for a next check, not total cost or probability of a publishable finding.

## What the samples establish

**Airwars:** Public incident USMAR260909a exposes a source-reference route. Source 296803 has an original post URL, post identifier and capture metadata, but no original image/video payload in the retrieved record. Its internal review link was not followed. The incident's substantive assertions were not evaluated. An unrelated, preselected NASA-media URL diagnostic returned an empty archive availability result and a CDX timeout; the URL was not independently verified live. This establishes neither archive-wide absence nor a working media-response route. J01 still needs exact payload identity, capture provenance and an explicit contemporaneous-event caption.

**AER:** Licence 0466075 was selected from an existing regulator document before querying the dashboard, solely as an interface specimen. It is not selected as a suspected seismicity case. A guessed URL filter first returned an unpopulated dashboard; actual visible textarea entry then returned UWI 03/04-08-063-21W5/0 and identifying fields. The dashboard's displayed aggregate count remained zero despite the identity row, so it is not an absence count. Selecting the row timed out in bounded browser automation. No operation dates, injection stages or consents were obtained. This is an environment-specific interaction limit, not proof that a normal user cannot open details. Current licensee identity does not establish the historical operator.

AER documents a general route through public data, inquiries and then formal information requests where needed. General-record ATI has a $25 initial fee; disclosure of a particular consent is not guaranteed. No consent-specific free public index was confirmed in the bounded search. No inquiry, request, payment or mass dataset download was made. Stage-level timing and operative historical orders remain necessary even if a completion summary is obtained. Historical well context does not justify applying the 2024 order retrospectively.

**ClinicalTrials:** The normal browser rendered NCT00000415 version 1, with submission date 2005-06-23 and estimated version-update posting 2005-06-24. Its first-posted field is 1999-11-04 estimated; the history lists three versions. The 1999 field does not prove that every word in the retained 2005 version was public in 1999. No original protocol attachment was obtained. A guessed legacy official PDF route for an unrelated preselected patent number returned 404; this is endpoint failure, not evidence that the patent or official documents are unavailable. No technical trial/patent pair or priority chain was acquired.

J02 also now makes explicit that missing literal wording need not mean a missing claim limitation. Specialist-reviewed inherency and explanatory evidence may apply; the test must not assemble absent claim elements from separate references. The patent remains a lead requiring expert assessment.

## Provenance repair

Batch 07 inherited D07/D08 from batch 06 without a filename. Those IDs collide with different documents in 07. Corrected current 07 and 08 use explicit `applicable_evidence_refs` objects containing evidence-file path, document ID and supporting Rabbit source IDs. B01 resolves specifically to 06's EIA schema; B02 to 06's World Bank audit anatomy. N01 retains no such support. Each 07 card also has qualified documentation references. Historical ZIPs and receipts remain intact; the new corrected 07 ZIP replaces its Library version while preserving Library identity.

## Verification and audit

Thirteen checks pass: nine provenance/count/ranking checks and four sample-evidence checks. An initial test selected an earlier, incomplete browser-log row; it was repaired to select the actual returned record. The failed and passing outputs are retained. Corrected 07's fourteen checks also pass.

`route-checks.csv` and JSONL record decisions and next checks. `cross-batch-ranked-routes.csv` and JSONL contain all 70 cards. `evidence/documentation` gives exact URLs and restrained observations; HTTP/browser logs record failures and bounded successes. Retrieved identifying fields and dates are preserved rather than full page copies. Hashes of inspected excerpts identify the observations but do not authenticate a site's historical claims.

The requests-library dependency was absent, so the probe uses Python's standard library. Installed Chromium resolved the missing bundled-browser executable. Browser CA validation failed locally; for the public, read-only browser probes it was explicitly disabled and logged. Earlier direct HTTP reads used normal TLS verification. No credentials or restricted services were used.

Run `python code/build.py`, `python code/validate.py`, and `python code/package.py` to rebuild exports, checks and ZIP from saved evidence. Network probes are separate opt-in scripts and are not required for local reproduction. The ZIP contains the canonical baseline and expansions 01–08, excluding older ZIPs. Each batch's historical receipts describe that batch's delivered version, not necessarily later corrected source files.

Weekly ChatGPT telemetry is unavailable; the last user report remains 88% at 18:50 UTC. No percentage is attributed to this pass. Paid API calls, payments and outreach: **zero**.
