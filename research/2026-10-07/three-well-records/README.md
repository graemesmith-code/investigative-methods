# Three-well records follow-up — October 7, 2026

**Found: original applications and licences, survey attachments, later official UWI amendments, and the corporate amalgamation certificate. Still missing: the actual stage/pumping/stop/restart logs, actual stimulated intervals, contemporaneous operator seismic notifications and any applicable restart consent.** All prior investigative packets remain indeterminate. No violation, withheld data, unauthorized restart or causation is established.

This supplement preserves the reviewed October 6 experiment at commit `e3986e42a96ab70cbd1ed88e9123fecacbb59fb3`. It adds records acquisition only: no Jev calls, purchases, outreach, new accounts or security changes. Prior Jev estimated spending remains US$0.000507.

## The important new finding: the wells changed identifiers after the earthquakes

The official [2024 ST1 archive](https://www.aer.ca/prd/data/well-lic/dwll2024.zip) identifies Vesta Energy Ltd. as the original licensee. The [October 30, 2025 ST1 amendment entries](sources/st1-2025-WELLS1030.TXT), corroborated by three downloaded AER information-update letters, explicitly map the old to current UWIs:

| Licence | Original issue | UWI before the reported amendment | Current UWI | Original application / activity | October 2025 update submission |
|---|---|---|---|---|---|
| 0515889 | October 30, 2024 | 02/16-28-037-28W4/0 | 00/15-28-037-28W4/0 | 33151710 / 33151712 | 33713494 |
| 0516327 | November 18, 2024 | 00/08-33-037-28W4/0 | 00/07-33-037-28W4/0 | 33174496 / 33174506 | 33713522 |
| 0516328 | November 18, 2024 | 03/01-33-037-28W4/0 | 00/02-33-037-28W4/0 | 33174496 / 33174507 | 33713527 |

The original issue lists also use longer raw forms `102/16-28-037-28W4/00`, `100/08-33-037-28W4/00`, and `103/01-33-037-28W4/00`; original licence PDFs display their own UWI formatting. Preserve these source strings, the stable licence numbers and both dated aliases when requesting records. They are **not six independently established wells**. The update letters change UWI, well name and bottomhole location; the publication date does not establish when the physical geometry changed or prove separate drilling legs. Current ST37 has one bottomhole and one production-string record for each licence; it does not supply complete historical leg geometry.

All three original licences specify the same surface pad, **05-31-037-28W4**, and Duvernay target/terminating formation. Their surface coordinates match the later ST37 coordinates used in the original screen. An offline GRS80 recomputation reproduces all nine prior surface distances (2.730–3.329 km) from the original licence coordinates. Thus the new identifiers do not negate the surface-proximity screen; they make the historical bottomhole/trajectory and completion-record lineage more important. **The earlier bottomhole distances (1.041–1.544 km) are later-snapshot screening proxies, not verified February distances.** Historical stage distances and stage-level rule-area membership remain unknown; the original reports are preserved with this explicit qualification. We do not infer trajectory from survey drawing OCR or turn planned bottomhole coordinates into as-drilled coordinates. Planned/licensed Duvernay is still not proof of the actual stimulated interval. See `results/coordinate-history-audit.json`.

The company’s [December 2024 notice and attached certificate](https://parallaxenergy.ca/wp-content/uploads/2024/12/General-Notice-Parallax-Energy-Operating-Inc.-Certificate-of-Amalgamation.pdf) establish the Vesta/Parallax corporate amalgamation effective December 4, 2024. Its [published notice](https://parallaxenergy.ca/vesta-energy/) says its “business administration number” remained unchanged, without specifying an AER BA code. The original application records identify Vesta as business associate **A0L1**, whereas current records use **A97L**; the notice does not establish continuity between those codes. This strengthens corporate identity tracing, but does not replace exact well-level licensee history, transfer effective dates or proof of who controlled the February operations. Current records use BA **A97L**; do not equate the current BA label with independently verified historical operational control.

## Records actually acquired

The official public [OneStop document index](https://www1.aer.ca/PubDocs/) returned two indexed events for each exact, zero-padded licence: its original application and its October 2025 information update. We downloaded **15 public attachments across five unique events**: three application-PDF attachments covering two application numbers, three original licences, three update letters, two survey-plan attachments and four small geographic ZIP attachments. Some supporting documents are duplicated between applications; this count is attachments, not 15 independent findings. The application records are planning/licensing evidence, not February completion logs. A survey's land/pad-location consent is not written earthquake-restart consent.

These real documents were available even though the October 6 IAR searches displayed `Total Applications Found: 0`. Both observations are preserved. Today's expanded IAR application/BA/location/date attempts produced empty-parameter/application errors, and a browser attempt stopped at a certificate warning. They are **failed searches, not zero results**. The earlier explicit zero counts remain valid only for those particular IAR queries, never for the universe of records or permissions.

A location-index query for section 31, township 37, range 28, meridian 4 returned 141 events in two pages; 63 carry Vesta/Parallax labels. One was submitted January–March 2025, for a pipeline, not a target-well restart. Location-index results can involve multi-location projects and are not proof of an exact pad association. No additional restart consent was identified in these retrieved metadata. Index coverage is not established as complete for seismic response correspondence.

The February 2025 Petrinex volume snapshot was rechecked against **all six old/current UWIs** (556,249 rows). Again there were no FromToID matches. No facility history could therefore be linked. The earlier current-UWI-only negative result is supplemented, not turned into evidence of no activity. Monthly volumes and production status cannot establish HF pumping times in any event. Current production-string `PUMPING` is a production status, not evidence that HF pumps ran during an earthquake.

## What the free routes did and did not provide

| Missing evidence | Public route checked | Result |
|---|---|---|
| Stage times, pumping, stop/restart | Disclosure summary; General Well Data catalogue 219 and its public Tableau/search export; tour catalogue and Directive059 FAQ | Public export returned an input-instruction row, not well details. Catalogue describes useful tour-occurrence/perforation/completion fields, but actual target detail rows were not retrieved. No time-resolved operational evidence acquired. |
| Actual stimulated interval / historical geometry | Original applications/licences, survey attachments, update letters; current all-leg ST37 extract | Planned/licensed formation and identity changes verified. Actual stimulated-stage top/base depths and as-drilled trajectory remain missing. |
| Historical operator / transfers | Original Vesta licences; corporate notice/certificate; current BA data; free Well Licence Report catalogue 683 | Stronger corporate chain, but target historical transfer rows not acquired. Initial CSV export contains only an as-at-date row. Standard public client received HTTP403 and was stopped; no bypass. |
| Contemporaneous seismic magnitude/detection | Existing AGS/NRCan snapshots and public waveform supplement; new event-specific NRCan detail queries requesting all origins/magnitudes/arrivals | Same one origin and one ML magnitude per event; zero picks/arrivals. No operator detection/notification record or historical solution sequence provided. |
| Written restart permission / accepted plan | OneStop exact authorization and location queries; IAR follow-up; incident-publication criteria | No such letter identified in retrieved documents. That does not mean it was absent, required, or violated. |

NRCan's query API requires its `YYYYMMDD.HHmm` event identifier, not the `ca…` identifier it returns inside QuakeML. Its validation response exposed that requirement; corrected queries `20250222.1405` and `20250225.0632` matched the expected `ca2025dscb` and `ca2025dwzq` records. February 22 remains ML3.1 in NRCan versus MLy2.09/industry M2.49 in AGS. The returned creation dates are catalogue metadata, not operator notification times. Requesting extra fields does not prove that a server supplied all underlying revisions.

Normal certificate verification remained enabled. Secure HTTP retrieved public HTML/CSV shells and OneStop records; no TLS warning was bypassed. The Tableau client’s 403 and Chromium’s certificate error were honored. Other official endpoints were separate documented public routes, not attempts to retrieve restricted records.

## The precise next records to obtain

[RECORDS-NEEDED.md](RECORDS-NEEDED.md) supplies the identifiers, dates, record types, receiving offices and verified pricing limits. It is a preparation document, **not a sent request or order**.

The narrowest useful package is February **15–28, 2025**, covering both local event times (February 22, 07:05:18 MST; February 24, 23:32:36 MST), with the February 1–March 15 envelope for monitoring plans and response/restart correspondence. Ask for original and amended records under **each licence and both UWI aliases**. Do not order six wells because each has two aliases.

The AER tour catalogue lists **$42 per well**, hence a listed-price subtotal of **$126 for three**, plus applicable taxes. The inspected official pages do not explicitly specify currency. The catalogue does not guarantee that this price includes service-company job reports, treatment/pressure charts or every attachment. Confirm the contents, correct aliases, currency and total before approving payment. A free routine-disclosure/support inquiry should first seek the unavailable free-report extracts and clarify where the seismic response records are held. Neither inquiry nor purchase has been made.

## Reproducibility and evidence limits

`results/public-document-index.json` maps every attachment to its official event/activity and download URL. `sources/manifest.jsonl` records download timestamps, TLS verification, outcomes, sizes and SHA256s. Read-only OneStop GraphQL requests/responses are preserved exactly, using the public application's own endpoint and field schema. `results/st1-target-matches.json`, `alias-monthly.json`, `current-all-leg-mapping.json`, and `nrcan-detail-summary.json` preserve the joins and their limits.

Scripts are under `scripts/`. Acquisition scripts make explicit free public requests; offline extraction and validation are separate. Full corpus remains in the private repository. The small reading deliverable omits large JS/HTML plumbing and unrelated raw tables. Some intermediate IAR diagnostic responses were overwritten during troubleshooting; the log retains their filters/timestamps/outcomes, while final raw responses and browser failure are saved. No completeness claim relies on those unsuccessful attempts. Old snapshots and conclusions were not overwritten.
