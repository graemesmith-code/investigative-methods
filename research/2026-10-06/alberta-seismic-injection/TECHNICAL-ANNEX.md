# Technical annex and reproduction

## Selection and bounded estimand

The frozen [protocol](PROTOCOL.md) selects 2020-01-01 through 2025-12-31 in America/Edmonton and all three named hydraulic-fracturing order areas from rule/data coverage. Entity names and known incidents were not discovery seeds. Subsequent incident, February volume and public-application lookups are explicitly post-discovery corroboration attempts. Their results did not change the discovery scope. Synthetic controls are segregated under `jev/`.

The implemented question is: which public HF reporting groups have a surface or bottomhole coordinate in a selected order-area polygon, a possible local-date overlap with a catalogue event, and a horizontal separation at or below 5 km (with 5–5.5 km sensitivity), where the event's specified magnitude meets that area's inclusive red threshold? ML is primary; MLy is separately labelled sensitivity; Mw/industry M never silently pass an ML gate. This generates candidates requiring evidence; it does not establish legal applicability or operation at event time.

SO6/SO7 red clauses do not expressly repeat the yellow clause's distance/time language. Consequently a 5.5 km cutoff is a **study bound**, not a claim that more distant events cannot matter. Yellow duties are not tested. Prohibited-zone HF is not tested because actual stimulated-zone evidence is missing; location alone cannot resolve the prohibition. There are 6 bottomhole reporting groups in Brazeau's outer polygon and 614 in Red Deer's outer polygon, zero in either inner polygon; the extended surface-or-bottomhole totals are 14 and 616. These membership counts are not findings about prohibited operations. Disposal has a different approval/plan-specific regime, and production is a different activity.

## Data and schemas actually inspected

| Source | Coverage acquired / actual fields | Valid use and limitation |
|---|---|---|
| AER SummaryChemical-WaterUse | Full 219,827,680-byte table; 595,923 ingredient rows plus two footers. Licence, UWI, Last_Submission_Date, Licensee, BH coordinates, stage count, water total, Start_Date/End_Date, ingredient/component fields. | Reporting-window screen and identifiers. No clock-time pump/stop sequence. Summary date-field derivation unresolved. |
| AER WaterSourceData | Full approximately 13.9 MB table; diversion/source dates and volumes. | Water sourcing, not injection timing. |
| AGS earthquake FeatureServer | Padded UTC query: 9,679 records; exact local-period filter: 9,668. UTC/Mountain time, lat/lon, Depth_km/Depth_type, event type, MLy, ML, M, Mw, EDGE_Id, Algorithm. | Mutable catalogue snapshot. 9,647 lack ML; numerical location uncertainties absent. Not a monitoring-completeness guarantee. |
| NRCan FDSN | Fixed bbox 51.5–54.9 N, −118.3–−112.9 longitude, padded UTC dates; 651 text and QuakeML records, all within local period. Time, lat/lon, Depth/km, magnitude type/value, event/origin IDs, metadata. | Independent typed magnitudes. XML numerical depths match text kilometres rather than assumed generic QuakeML metres: use explicit CSV km. Metadata creation time is not operator detection/notification time and may precede an origin. |
| ST37 | Complete 183,921,877-byte Excel archive. Surface 540,379 rows, bottomhole 539,681, production strings 659,315 scanned; retain all period licences before collisions. | Current infrastructure positions and identifiers; not historical operating control. |
| Petrinex Well Licence | 528,761 rows; 9,940 matching period licence records. ProjectedFormation, TerminatingFormation, licence/BA identifiers and dates. | Current formation proxies, not fracture-stage formation. |
| Petrinex monthly volumetrics | January 2025: 564,687 rows / 11,252 INJ; February: 556,249 rows. ProductionMonth, ActivityID, ProductID, FromToID, facility/BA IDs, Volume, Energy, Hours and other fields. | Monthly totals, not daily/hourly timelines. INJ includes steam and other activities beyond disposal. FRAC denotes fractionation, not HF. Activity/product units must be interpreted through the saved layout; no conversion into HF timing is attempted. |
| Facility Operator History | Actual full ZIP and schema retained. February target IDs have zero matches, hence zero linked facilities examined. | Historical operator remains unresolved; do not claim a successful historical identity join. |
| Active disposal inventory | September 15, 2026 workbook, 2,169 sheet rows including three headers. | Current inventory only. Not a historical 2020–2025 disposal exposure set. |
| Incident release / complaint tables | 86,318 release rows; 28,186 complaint rows. Exact licence and incident-ID matches checked. | A noise complaint `SourceInCompliance=No` is not a seismic violation; CIC0438079 differs from EDGE438049. |
| IAR public application search | HTTPS form requests for each of the three licences; saved returned pages and query logs, zero applications. | No inference that written consent did not exist. |

`results/actual-schemas.json`, `petrinex-vol-schema-sample.json`, `petrinex-licence-schema.json`, `st37-extraction.json`, and `candidate-ingredient-rows.json` preserve actual fields and samples. Full public datasets, not catalogue descriptions alone, underpin these limits. January monthly data was chosen to inspect structure; February was acquired after the candidate cluster emerged. Downloading every month would not add missing within-day timestamps, so no six-year monthly injection completeness claim is made.

## Deduplication, joins and missingness

The disclosure grouping key is licence, UWI, submission date, start date, end date and BH coordinates. Distinct windows/submissions remain distinct. Component stage counts and water values are collected as sets, not summed. Of 16,391 period groups, 4,573 have multiple stage values and 9,279 multiple water values. Fields retained from the first ingredient row are checked for conflict: zero conflicting groups. Each group has original uncompressed physical line references; 57 unique ingredient rows underpin the real packets. These units cannot be assumed to be unique jobs.

The full table has 42,025 groups, no malformed data rows, no invalid date windows and no invalid coordinates among period groups. The source's row-count and completion-time footers are explicitly excluded. The original 2,674 BH-scoped groups / 1,312 UWIs expand to 2,692 groups / 1,328 UWIs when surface membership is included, adding 18 surface-only groups.

All 16,391 period groups match current surface and licence records. Projected formation is missing for 169 and terminating formation for 57; among 2,692 scoped groups those counts are five and two. Even nonmissing formations leave formal geological applicability unknown. The three surfaced wells have current DUVERNAY FM proxies, but every evidence packet carries `formal_geological_applicability: null`, unknown pumping, and unresolved historical identity.

UWI-to-Petrinex mapping preserves well-event characters and produces a 20-character ABWI identifier; its syntax and negative lookup are tested. Zero February FromToID matches do not mean zero activity; reporting aggregation, identity mapping and confidentiality remain possible limitations. Facility histories are not a substitute for historical HF operator/licensee confirmation.

## Time, maps, magnitudes and event identity

The official NAD83 order GIS is retained and plotted against the PDF appendix maps. Its stale labels are not an authoritative versioned rule register. SO2/SO2A geography continuity is a visual comparison; dates and formations come from operative text. Every packet carries the dated rule: Fox Creek SO2 before November 19, 2024 and SO2A thereafter; SO6/SO7 effective May 27 / December 9, 2019. Actual surfaced packets are SO7. No current 2026 disposal directive is backcast onto prior operations.

The earlier 0.1-degree polygon-buffer event prefilter has been removed. All acquired events passing each typed magnitude threshold are evaluated against scoped wells. `threshold_events_catalogue_wide_before_well_distance` counts threshold events across each acquired catalogue before distance filtering; these are not events in that order area. GRS80 ellipsoidal horizontal distances are measured separately to surface and bottomhole; neither is presumed the definitive legal reference for every clause. Stage trajectories, possible datum differences and numerical location uncertainty are unavailable. The 5–5.5 km sensitivity is not an uncertainty distribution.

UTC timestamps are converted using the IANA America/Edmonton timezone, including DST. Both catalogue queries are padded outside the target years, followed by exact local-date filtering. The effective interval is 2020-01-01 07:00 UTC inclusive to 2026-01-01 07:00 UTC exclusive. Independent review found the first download incorrectly used UTC calendar years. The correction removes one AGS event that was December 31, 2019 locally, adds no in-period events, and leaves NRCan and the candidate cluster unchanged. Original snapshots remain in `sources/pre-audit/`; the exact difference is in `results/time-boundary-audit.json`.

Date-window ends are inclusive possible-overlap days. A February 24 local event at 23:32 cannot be compared as February 25 against local reporting dates. Neither same-day overlap nor later reporting activity proves pumping after the event. Manual 027's `perfDate`/Treatment Date is a fracture date; its separate general operation dates concern rig/site presence. Neither independently documents how this summary aggregates Start_Date/End_Date. Sub-day logs are still required.

AGS ML/MLy/M/Mw and NRCan MagType are retained. No scaling law or ML=Mw assumption is used. Candidate cross-catalogue matches require both ≤10 seconds and ≤10 km, retaining every qualifying counterpart; uniqueness within that tolerance is not identity proof. February 22's NRCan ML3.1 versus AGS MLy2.09/M2.49 is a material disagreement, prominently retained. INF164's 2026 magnitude guidance does not prove the magnitude available to an operator in 2025.

## Access routes and unresolved records

Saved primary PDFs, bulletins, maps, public API payloads and actual table extracts were obtained with normal certificate verification. The Tableau HTML shell was accessible through an ordinary verified request, but system Chromium stopped on `ERR_CERT_AUTHORITY_INVALID`; no warning was bypassed. The saved error is `sources/tableau-browser-error.json`. Petrinex Well Infrastructure showed Refreshing and its API returned 404; ST37 and Well Licence provided usable alternatives. The NRCan FDSN endpoint was discovered in the official site's app bundle; failed guessed/root routes were not treated as data.

The initial 150 MB disclosure limit was too small and was raised for the known official full dataset. One large-download attempt without the existing descriptive User-Agent returned 403; restoring that same descriptive User-Agent succeeded. No authentication or security policy changed. Normal-sized rule PDFs were never rejected under a tiny artificial cap. Acquisition errors and successes remain in the manifest.

Free disclosure, Manual027/Directive059 guidance, official Tableau route, ST37, well licence data, AGS and NRCan event APIs, incident records and IAR application search did not provide the required time-resolved stage logs, actual stimulated interval, contemporaneous monitoring history or restart consent. The source catalogue advertised paid well records ($42/well) and disposal progress reports ($10/request); none were purchased and no outreach was made. This is a documented bounded search through reasonable free official routes, not proof that no public or obtainable record exists elsewhere.

Required next evidence is listed in README. Permissions matter only where a qualifying shutdown/restart is established. No public match is never proof of no permission. Current labels, release complaints and monthly hours must not be repurposed into those missing facts.

## Offline reproduction and provenance

Use a checkout of the private repository. Python 3.11+ is recommended; the environment's dependency versions are pinned in `requirements.txt`. Install into an isolated environment if needed:

```bash
python -m venv /tmp/alberta-repro
/tmp/alberta-repro/bin/pip install -r research/2026-10-06/alberta-seismic-injection/requirements.txt
cd research/2026-10-06/alberta-seismic-injection
/tmp/alberta-repro/bin/python scripts/reproduce.py --full
/tmp/alberta-repro/bin/python scripts/verify_sources.py
```

`--full` reconstructs the original order/ST37 ZIPs from lossless ≤40 MiB pieces, checks their SHA256s, parses the disclosure, rescans all ST37 sheets and licence data, reruns the extended join/cross-catalogue checks, computes audit summaries and runs tests. It makes **no network or paid calls**. Without `--full`, saved all-period infrastructure extracts are reused. `results/reproduction-log.json` records commands, output and return codes. The existing private repo `code/ati/pipeline.py` provides the unchanged cost ledger used in offline cost tests.

`get_initial.py`, `refresh_catalogue_bounds.py`, `get_large.py`, `iar_search.py` and `tableau_probe.py` are explicit live public-data acquisition routes; do not run them as part of an immutable snapshot reproduction. Some initial discovery probes were interactive; their exact successful URLs, bytes and hashes are retained in `sources/manifest.jsonl`, with IAR POST logs separately in `results/iar-search-log.jsonl`. Sources are snapshots retrieved October 6, 2026, not contemporaneous 2025 observations. The complete disclosure is stored losslessly as `.csv.gz`; the original CSV can be regenerated by gzip decompression. Multipart reconstruction metadata and hashes are in `sources/multipart/manifest.json`.

Jev scripts are separate from reproduction. The original pilot's live route and the completed real gap route are disabled; V2 requires the existing cumulative ledger and current pricing verification. No default script performs paid calls. Exact requests/responses, archived failed pilot and gate outputs, superseded unsent drafts, final token estimate and guarded real gap output are retained. Any Jev input whose current analysis file changed after audit has an immutable matching snapshot under `jev/gap-only/input-snapshots/`.

The compact Library review bundle omits large infrastructure, volume and incident archives and their multipart pieces; it is a review deliverable, not a substitute for the full private checkout. The private repo contains the complete acquired corpus needed for full offline reproduction. See `BUNDLE-MANIFEST.json` in the ZIP for inclusions, hashes and repository reference.

## Final validation

The full offline run completed all eight steps successfully, including bulk infrastructure rescans and 17 tests. Tests cover local-year edges/DST, magnitude types/inclusive thresholds, rule-version transition, real-packet unknowns, deduplication/source rows, spatial and catalogue associations, false incident conflation, missing monthly matches, Jev abstention/cost, reservation failure retention and lossless source restoration. All 53 successful acquisition records match original/current or preserved pre-audit bytes. The configured Jev secret value was absent from scripts, response artifacts and derived results. Source downloads retain their exact original bytes; the raw ArcGIS count response's CRLF is intentional and not normalized for a whitespace check.
