Historical access-stage snapshot, superseded by README.md after successful user-local downloads and measurement screening.

# Satellite night-light pilot: access and timing result

**15 October 2026. Status: archive/timing checks completed; brightness backtest blocked on scientific-file transfer. Earthdata sign-in succeeded, but the cloud browser rejected the download redirect. No radiance measurements have been downloaded or scored.**

The selected test is feasible as a retrospective measurement experiment, subject to cloud/quality screening. It is **not yet an established advance-warning method**. The archive exists, but the corrected files currently returned for the selected dates were produced after the operations. Historical near-real-time queries returned no matching files.

## What was actually checked

NASA's public Common Metadata Repository was queried for Washington's tile `h10v05`, using Suomi-NPP Collection 2 products `VNP46A1` (at-sensor light and observation time) and `VNP46A2` (corrected light). Each selected UTC observation date has both standard files:

| Case | Selected observation dates (UTC) | Standard A1 / A2 files | Historical NRT A1 / A2 matches | A2 production delay, days* |
|---|---|---:|---:|---:|
| Iran, June 2025 | June 18–20 | 3 / 3 | 0 / 0 | 8.44–8.67 |
| Venezuela, January 2026 | Dec 30–Jan 1 | 3 / 3 | 0 / 0 | 8.64–21.73 |
| Iran, February 2026 | February 25–27 | 3 / 3 | 0 / 0 | 8.54–14.67 |

\* Calculated from each filename's production timestamp minus the start of its UTC observation day. This is **not exact latency from overpass, nor first-publication time**. It describes the current archived versions; earlier versions may have existed. CMR `updated` is recorded separately and is not assumed to be first availability. The 9 A1 files' corresponding delays are 1.36–2.91 days.

Queries deliberately cover boundary days; CMR returns overlapping intervals inclusively. Counts above use strict observation-date filtering, not raw search hit counts. Metadata presence does not establish clear sky or usable pixels.

The initial anonymous request for a scientific HDF5 file returned HTTP 302 to NASA's Earthdata login. The user subsequently completed Earthdata sign-in through the secure browser flow; the signed-in profile was observed. The cloud browser then rejected the scientific-file download redirect under its URL security policy (unsupported protocol). No science file was obtained. That is a browser transfer limitation, not a NASA account failure or proof that the file is unavailable. AWS's registry explicitly identifies these assets as controlled access requiring Earthdata Login. The 247-collection public VEDA inventory contains some disaster night-light examples and monthly composites, but no matching daily Washington series for these windows. One documented VEDA CMR compatibility request returned HTTP 500; that is a service failure, not proof of permanent incompatibility.

## What this means for a newsroom

The free standard archive could answer **“was this broad area unusually bright?”** once quality-screened pixels are available. It cannot, by itself, answer **“could we have issued that lead before the operation?”** NASA documents a near-real-time service, but its general LANCE guidance describes a roughly seven-day rolling archive. Zero historical matches here do not prove no timely files were originally published.

A future live test would need to retain the exact NRT files and first-seen timestamps as they arrive. This run has not scheduled or started ongoing collection. Brightness measures emitted light, not staff numbers: an extra thousand workers may leave exterior illumination unchanged.

## Resume this test

1. Earthdata sign-in is now complete. Because the cloud browser blocked the download redirect, download the science files in your own browser and upload them to the conversation. The exact initial pair is linked in [DOWNLOAD.md](DOWNLOAD.md). Alternatively, the prepared local script uses [NASA's documented download-token procedure](https://nrt3.modaps.eosdis.nasa.gov/help/). Do not put credentials in this repository or chat.
2. Start with the June 20 A1/A2 pair: about **67.2 MiB**. The 18-file event-window manifest totals **561.4 MiB**, before baselines. `code/download_files.py` defaults to that two-file check and accepts `--all` for the listed 18 files. This downloader is prepared, not validated against an authenticated transfer.
3. Inspect the real schema, acquisition times, quality flags and unfilled corrected radiance. Run the frozen broad-area screening in `PROTOCOL.md`. Only then obtain baseline/ordinary-night data and run a brightness comparison.

Successful scientific-file transfer is the immediate dependency. Quality, sensitivity and warning performance remain unresolved scientific questions. None of the three cases has been counted as a hit or miss.

## Files

- `download_manifest.json`: exact file identifiers, URLs, sizes and timestamps.
- `evidence/coverage_summary.json`: dated queries and filtered historical coverage.
- `evidence/download_access_check.json`: initial anonymous login redirect.
- `evidence/browser_transfer_status.json`: successful sign-in followed by the browser policy rejection.
- `evidence/public_alternatives.json`: compact public-service inventory.
- `evidence/titiler_compatibility.json`: recorded service error.
- `config.json`, `PROTOCOL.md`: broad areas and rules fixed before pixel inspection.
- `code/catalog_preflight.py`, `code/summarize_preflight.py`: reproduce the metadata audit.
- `code/download_files.py`: bounded, credential-safe download handoff.

## Primary documentation

- [NASA Black Marble Collection 2 user guide](https://landweb.modaps.eosdis.nasa.gov/data/userguide/BlackMarbleUserGuide_Collection2.0_20241203.pdf), especially filename convention, Tables 5–10 and section 5.4.
- [NASA VIIRS Black Marble products](https://viirsland.gsfc.nasa.gov/Products/NASA/BlackMarble.html).
- [NASA LANCE FAQ: retention, latency and registration](https://forum.earthdata.nasa.gov/viewtopic.php?t=5201).
- [NASA download authentication](https://nrt3.modaps.eosdis.nasa.gov/help/).
- [AWS registry: NASA Suomi-NPP access](https://registry.opendata.aws/nasa-suomi-npp/).
- [VEDA's public statistics service](https://docs.openveda.cloud/user-guide/notebooks/quickstarts/timeseries-stac-api.html).

These sources describe products and access. The counts and delays above are this project's own calculations from the saved NASA metadata manifest.
