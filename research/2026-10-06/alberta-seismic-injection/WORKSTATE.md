# Resumed checkpoint

The corpus and original analysis were pushed to private main at 36045a11a42e3bd463064602252fc151dda60c9f. The Jev repair was committed separately as 56115b1; the final response records the latest verified remote commit.

`scripts/jev_v2.py` ran 12 new synthetic controls using the SAME cumulative ledger: 14 total successful calls, estimated US$0.000415, zero pending reservations and no other paid calls. Original failed control remains in `jev/C02-monthly-volume-trap.request.json` and `.response.json`; original ledger is archived as `jev/v1-ledger.json`.

See `jev/METHOD-REPAIR.md` and `jev/v2/evaluation.json`. At an illustrative 0.5 cutoff, 34/36 atomic answers matched fixture labels, and 10/12 full fixtures matched. This is not a calibrated performance estimate. Explicit continuous pumping was missed in S03 and S10. Three-way deterministic gates now preserve abstention as null/indeterminate; the original derived gates are archived. No further API calls were needed for that correction. The 12 existing offline checks still pass, with the original cost check now using v1-ledger.json. Add checks for v2 and total accounting during final review.

The extended data result is 2,692 surface-or-bottomhole reporting records across 1,328 UWIs. Two candidate physical events overlap date windows at three wells. Nine catalogue-event-well packets preserve agency differences, not nine discoveries. All remain indeterminate.

Remaining: independent review; optional real evidence-gap ranking only, never accusation or compliance scoring; final report and technical annex; reproducibility and hash inventory; Library bundle; final remote verification. No raw-data change since the detailed checkpoint below. Preserve the live ledger and do not reset or replay paid calls.

---

# Handoff checkpoint — 2026-10-06, approximately 21:33 UTC

Parent explicitly requested this checkpoint turn end so it can observe progress and resume. **Experiment is not finished or pushed.** Environment `/workspace/investigative-methods` is usable, branch `work`, HEAD and origin/main both `a92de4d1f5be5d9cfa0316ee3b8fa5aafe79085f`. No AGENTS.md or local skill instructions were found; `/workspace/.agents` was empty. All changes are new files under this experiment; earlier work untouched. No subagents spawned.

## Acquired and analyzed

- Original SO2, SO2A, SO6, SO7 PDFs, full Directive065 (2026-03-31), Bulletin2024-29 and2024-28, Bulletin2019-07, Manual027, Directive059, INF164, MMR guidance. Rule text/maps inspected; `RULES.md` summarizes operative differences. Historical 2024 Directive065 not retrieved; no backcasting.
- AER complete SummaryChemical-WaterUse: **219,827,680 uncompressed bytes**, saved as 14.8MB gzip. **595,923 ingredient rows**, two non-record footer lines separately identified, no malformed data rows. Source completion timestamp September15 2026. Dedup key licence/UWI/submission/window/coordinates excludes component stage-count differences (retains stage sets). **16,391 in-period reporting records**, not necessarily distinct jobs.
- AER order GIS ZIP64.9MB with actual Subsurface_Orders polygons. Stale labels noted (SO2 not2A; geology fields must not override PDFs). Map visually compared to appendix outlines; current version provenance limited.
- ST37 original ExcelZIP183.9MB; inspected and scanned SH540,379, BH539,681, ProductionString659,315 rows. Retained all in-period HF licences, not only candidate entities. Surface or bottomhole area membership yields **2,692 records /1,328 UWIs**: FoxCreek2062, Brazeau14, RedDeer616. Broad candidates, not legally eligible exposure denominator.
- AGS catalogue **9,669 events2020–2025**, server count independently confirms complete response, no truncation. ML missing9648; MLy missing1. Full typed magnitudes, depth/type/algorithm/EDGEIDs saved; no numerical uncertainty.
- NRCan public React app revealed its genuine same-host FDSN event query; retrieved **651 events** in fixed broad bounding box covering all3areas for2020–2025, both text and QuakeML. **513ML,135MLy,3Mw**. No numerical uncertainties. XML depth values appear numerically km despite generic QuakeML convention; use explicit CSV Depth/km. Current catalogue creation metadata does not prove real-time operator availability.
- Petrinex well licences528,761 rows (9940 period-licence matches), facility operator-history full extract, Jan2025 volume564,687 rows incl11252INJ, Feb2025 volume556,249 rows. Three target UWI mappings have zero February FromToID matches, not proof of no activity. Monthly Hours not timestamps. Petrinex FRAC=fractionation, notHF.
- ActiveDisposalWellList actual XLSX dated2026-09-15,2169sheetrows including3header rows, inspected schema/sample. Separate from HF/disposal historical exposure.
- Incident release86318rows and complaint28186rows scanned. Licence0516327 matches a Feb15release and Feb24noise complaint. Noise CIC0438079 is **NOT** AGS earthquake EDGE438049. SourceInCompliance='No' in noise record must not be turned into seismic finding. These records may have mutable current licensee labels.
- IAR public form searches for each of3licences via normal HTTPS form POST returned0applications. Saved pages and log. Does not prove no consents exist.

## Actual bounded result

`results/evidence-packets.json`: **9 catalogue-event-well packets**, representing **two candidate physical events × three wells**, not9discoveries. AGS/NRCan crossmatch retained separately, tolerance predeclared ±10s and≤10km, unique match for each:

| Local day | NRCan | AGS matched estimate | Key implication |
|---|---|---|---|
|2025-02-22|ca2025dscb,ML3.1,14:05:18UTC|object9289785,MLy2.09,industryM2.49,14:05:17UTC,1.373km origin difference|Threshold classification differs by catalogue/type. NRCan origin creation metadata2025-04-02; cannot assume available at operation.|
|2025-02-24|ca2025dwzq,ML3.76,2025-02-25 06:32:36UTC|object9289976,MLy3.12,industryM3.25,1second/.169km difference,EDGE438049|Both typed local estimates above RedDeer3, but pumping/detection/response still unresolved.|

Wells0515889 (00/15-28-037-28W4/0),0516327 (00/07-33-037-28W4/0),0516328 (00/02-33-037-28W4/0). Current source labels Parallax Energy Operating Inc., BA A97L. Both projected and terminating licence formations DUVERNAY FM, not actual stimulated-interval proof. All are within SO7 AppendixB outsideA; BHdistance~1.04–1.54km, surfacedistance~2.73–3.33km. Date windows includeFeb15–28 and narrower windows; date-only endpoints are possible-overlap days, not continuous pumping. Seven AGS and16NRCan window pairs, nine grouped packets. Thirty-three near-but-nonoverlap records saved as controls.

All real packets **indeterminate**, no established noncompliance/causation. Needed: actual stage formation/trajectory, pumping/stop timing, contemporaneous magnitude and detection, historic identity and any written restart consent. Missing public consent is not proof of none. No real compliance-testable packet.

## Jev

Existing supported `JEV_API_KEY` environment credential configured; value never exposed. Current primary pricing/endpoints downloaded from docs.typesafe.ai/models and /api; pinnedjev-1.13.0,$0.042/Minput,freeoutput. New authorized budget separate; internal9USDcap, reserve0.003/call, no automatic retries. Uses existing budget implementation without modifying old file.

**Two synthetic calls completed, estimated cost71microusd=US$0.000071 based on reported input tokens. Zero unresolved reservations, zero other paid calls.** Pilot intended3cases but stopped aftercase2 failed: model correctly said monthly totals do not establish pumping, yet answered0.82 to unresolved-restart authorization despite no evidenced restart. Raw exact responses, prompts, ledger export and private live sqlite saved. `jev_controls.py` now blocks nonpilot expansion unless all3pilotcasespassed. Do not rerun live or reset ledger.10syntheticpayloads prepared, only2sent.3early AGSreal prompts unsent; should regenerate final9NRCan/AGS packet requests as UNSENT, add cost bounds, do not submit real evidence under this failed pilot. Pilot verdict not generalized model-performance estimate.

## Blockers and access handling

- Browser Chromium with TLS verification raisedERR_CERT_AUTHORITY_INVALID forwww2.aer.caTableau. Stopped; no ignoreHTTPS or security changes. That prevents finer frac report/incidentdashboard/licence-history review through that browser. Initial ordinary verified-HTTPS HTML shells retained; no later workaround around warning.
- Petrinex WellInfrastructure public page explicitlyRefreshing and API404; ST37/licence alternatives acquired.
- First large HFfetch stopped at150MB (logged). Ad-hoc replacement omitted established descriptiveUser-Agent and got403; restoring original standard collector configuration returned200 and full219.8MB. No auth/security changes. Preserve this audit trail, do not claim there were no403responses.
- Tour reports listed42dollars/well and disposal annual progress reports10dollars/request; **none purchased**, no outreach. These do not prove all free equivalents absent.
- Search queries on licence numbers/Parallax restart/seismic yielded no precise indexed restart evidence. Need finalize search/probe log from saved evidence, not claim exhaustive absence.

## Tests and remaining work

**12offline tests passed** via `PYTHONPATH=/tmp/alberta-python python research/2026-10-06/alberta-seismic-injection/scripts/test_study.py`. Checks counts/sourcefooters,UTC/DST,typedmagnitudes,inclusiveboundaries,polygon/geologyproxy,ellipsoidal distances,duplicate grouping,catalogue disagreement,noiseincident mismatch,monthlymissingness,cost,reservation failure retention,lossless archival parts.

Dependencies installed free under/tmp/alberta-python:shapely,pyproj,pyshp,pyogrio,openpyxl. Existing matplotlib,numpy,pandas,playwright. `plot_bounds.py` produced visually inspected rule-boundary-review.png; cosmetic tick overlapBrazeau can be fixed. No pip/system credential/security changes.

Remaining required:
1. Finish plain-EnglishREADME (currently older checkpoint) with final2events/3wells, magnitude disagreement, missing evidence, Jev failure/cost. Technical annex/dataavailability/searchlog/reprocommands. Consolidate a few inline probes (incidentlookup,monthlyschemainspection) into scripts if desired.
2. Refresh real UNSENTpayloads fromfinal evidencepackets, exactcostestimates, retain oldpilotrequests/responses. Ensure report has no allegation promoted by irrelevant noise record.
3. Make code portable/self-contained: `st37_extract.py` now unzips totemporarydirectory; dependencies/requirements andruninstructions needed. `analyze.py`,extended_analysis.py,corroborate.py produce mainresults. Budget runner imports repo code/ati/pipeline.py atunchangedbasecommit. Avoidpaidreplay.
4. Inspect sources/manifest, add finalhashinventory and verificationevidence. `archive_sources.py` has already split ST37andorderZIP losslessly into7×≤40MiB parts in sources/multipart; originals ignored byexperiment.gitignore. `restore_sources.py` joinsandhashchecks. Thus fullsources can be committed belowGitHub100MB/filelimit. Private repo footprint~428MBlogical beforeduplicateparts.
5. Commit/push newexperiment toprivate repo, checkoriginmainunchanged/rebaseifnecessary; noforcepush. Existing branchwork. Remote main wasverifiedsamea92de4d1. No commit orpush yet.
6. Preparecompactdownloadbundle (reports/scripts/results/essentialraw, linkfullprivate-reposources rather than including250MBarchiveparts) and saveLibrary. Library skillc0/libraryread; library_create_library_file available acceptsfileabsolute path. Helpercontents read butnotwritten; fetchcurrentlibrary_file_transfer.py into/tmpprivateand applyreturnedxattrsinsameexecaftercreate. Fullbundle>50MB requirespreparedhelper; compactreviewbundle~25MBshouldfitdirectroute. NoLibraryfilecreatedyet.
7. Finalremotecommit/artifactverificationandanswer.

No continued background processes are required. Resume autonomously; authorization remains the original experiment scope and US$10Jev maximum. UserlastreportedChatGPTusage72%,notataskcost.
