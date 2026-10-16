# Measurement feasibility: all three event archives

Completed 15 October 2026. This report concerns input integrity, native-grid coverage, quality flags and clocks. It does not estimate brightness anomalies or warning accuracy. The original `config.json` and `PROTOCOL.md` are retained unchanged; their access-stage status text is historical.

## Provenance and scope

The user downloaded the fixed 18-file manifest locally and uploaded three archives. All files matched the frozen catalog entries, download-receipt SHA-256 hashes and byte counts. ZIP CRC checks, HDF5 signatures and HDF5 opens passed. These receipts prove consistency with the downloader's records; they are not independent NASA signatures.

| Archive | SHA-256 |
|---|---|
| iran_june_2025.zip | 9724350b5c689588ccbc8ec14ed97adc456acf49ec924a1a4dcf163d8847ed95 |
| iran_feb_2026.zip | 7b05d8dd420dc778fda60bf87baac9529ac70f54c85753f75758cb00e6b5db29 |
| venezuela_jan_2026(1).zip | efe90bfb3073a9809beb869e0ce7fb808a08463190ee9b3a4d8075e28e05c719 |

**Use `evidence/verified_uploads.json` as the authoritative machine-readable provenance.** Science files total 588,680,197 bytes. Receipt transfer intervals sum to 235.21 seconds; this excludes account setup, interruptions and uploading, and is not an end-to-end usability measure.

The earlier Iran-only source/evidence checkpoint was absent from the resumed runtime. The measurement code was reconstructed from the unchanged protocol and config, with the earlier documented coordinate interpretation and diagnostics. All six Iran target fractions reproduced the earlier results to floating-point precision before finalizing Venezuela. This is workflow recovery, not an independent replication or preregistration. The relaxed scenarios were already motivated by the Iran results.

## Exact measurement choices

The four approximately 2 km squares are defined in `config.json`. Denominators include the entire square, including any water and partial boundary cells. No region was shifted or resized after inspection. No employee geofence is claimed.

Native arrays are 2,400 × 2,400, spaced at 1/240 degree. We use the supplied latitude and longitude values as cell centers, following [NASA LAADS User Services' specific clarification](https://forum.earthdata.nasa.gov/viewtopic.php?p=26597&t=8169). For this tile the first centers are latitude 40 and longitude −80; we do not add another half-cell offset. Cell footprints extend half a grid step around each center. Spherical intersection areas use radius 6,371.0088 km and are checked against each square's analytic area. The target intersects 30 cells; these are not independent observational replicates.

Every A1/A2 pair matches the date, tile and actual LocalGranuleID. A2's InputPointer includes the exact A1 filename. ProductionTime attributes match the catalog. Coordinate vectors match between paired files. Attributes and dataset shapes/types are recorded in `evidence/science_schema.json`.

Only the unfilled A2 `DNB_BRDF-Corrected_NTL` is accessed, and only to produce a valid-observation boolean. Its Collection 2 floating-point scale is 1 and offset 0; the actual fill value is masked. No gap-filled radiance, raw A1 brightness, brightness means, event scores or rankings are read into the analysis outputs. A1 supplies quality, angle and acquisition time.

The fixed primary mask requires:

- finite, non-negative, non-fill observed corrected radiance;
- Mandatory_Quality_Flag = 0 and Snow_Flag = 0;
- non-fill cloud mask; bit 0 = night; bits 4–5 = 3 (high quality); bits 6–7 = 0 (confidently clear);
- cloud-mask bits 8, 9, 10, 12 and 13 unset (shadow, cirrus, snow/ice, aurora, eclipse);
- A1 QF_DNB = 0; valid sensor zenith at most 60 degrees;
- valid UTC_Time in [0,24] decimal hours and acquisition before the fixed cutoff.

These are this project's deliberately strict combined rules, informed by the [Collection 2 guide, Tables 5–10](https://landweb.modaps.eosdis.nasa.gov/data/userguide/BlackMarbleUserGuide_Collection2.0_20241203.pdf). They are not represented as NASA's sole recommended mask. Exclusion reasons overlap and cannot be added as independent percentages.

A date passes at 75% valid area in the target and at least two of three controls. A case requires at least two dates before later baseline/calendar gates. Invalid or absent observations remain missing, never zero evidence of activity.

## Results for every date

Percentages below are the target's area surviving the indicated mask, not brightness. A date-level pass also requires controls. The corresponding control checks produce the same passing-date counts shown below.

| UTC date | Primary | Allow A1 flag 16 only | Allow medium cloud quality | Both changes | Primary date passes? |
|---|---:|---:|---:|---:|---|
| 2025-06-18 | 0.00% | 0.00% | 0.00% | 0.00% | No |
| 2025-06-19 | 19.64% | 96.18% | 19.64% | 96.18% | No |
| 2025-06-20 | 25.04% | 95.82% | 25.04% | 95.82% | No |
| 2025-12-30 | 0.00% | 0.00% | 0.00% | 0.00% | No |
| 2025-12-31 | 0.00% | 0.00% | 0.00% | 0.00% | No |
| 2026-01-01 | 59.97% | 59.97% | 86.18% | 86.18% | No |
| 2026-02-25 | 0.00% | 0.00% | 0.00% | 0.00% | No |
| 2026-02-26 | 0.00% | 0.00% | 0.00% | 0.00% | No |
| 2026-02-27 | 18.45% | 18.45% | 93.76% | 93.76% | No |

All three primary cases are **unscorable**, not negative. At no point is a relaxed scenario substituted for the primary finding.

The first diagnostic permits QF_DNB exactly 0 or 16, preserving all other A1 vetoes. The second permits cloud-mask quality 2 or 3 while still demanding confidently clear sky. The combined scenario applies both changes. All retain mandatory quality 0, both snow requirements, angle, timing and control-area gates.

June 19 and 20 have A1 flag 16 over 80.36% and 74.96% of the target, respectively. The [NASA algorithm description](https://viirsland.gsfc.nasa.gov/Products/NASA/BlackMarble.html) includes stray-light correction. Whether an additional A1 veto is appropriate for small-change detection remains unresolved; this diagnostic does not validate a revised mask. June 18 has no observed corrected retrieval.

February 25 and 26 have no observed corrected retrieval and confidently cloudy classifications throughout the target. On February 27, medium cloud-mask quality covers 78.27% of the target, despite confidently clear classification throughout. Mandatory quality 0 covers 93.76%; flag 1 covers 6.24%.

December 30 has 39.84% missing observed radiance, and 60.16% classified confidently clear with mandatory quality 0. Cloud-mask bit 10 is nevertheless set across the target while Snow_Flag is 0. Even removing that snow veto alone could not reach 75% from the 60.16% available high-quality area. December 31 has no observed corrected retrieval and is confidently cloudy throughout, with the same disagreement between the two snow indicators. These flags are algorithm outputs, not independent ground observations of snow.

On January 1 all target pixels have observed radiance and confidently clear classification, but mandatory quality excludes 13.82% (flag 1: 10.92%; flag 5/glint: 2.90%). Cloud-mask quality is medium over 26.21%. The medium-quality diagnostic leaves 86.18% target coverage and qualifying controls. It still leaves Venezuela with only one date.

Some earlier libraries/tutorials describe flag 1 as good ephemeral light. That is **not Collection 2's coding**: [NASA explicitly defines 0 as high quality and 1–5 as poor quality](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A2/). The [World Bank blackmarbler tutorial inspected in this review](https://worldbank.github.io/blackmarbler/articles/assess-quality.html) contains the older meanings and defaults to gap-filled radiance in one example. We did not adopt those defaults. A genuine unusual light can potentially be affected by an outlier screen; flag-1 exclusions are reported rather than silently restored.

## The clocks

UTC_Time is converted with America/New_York, including daylight saving. Times below show the earliest target pixel timestamp rounded to seconds; full min/max and work-night labels are saved in JSON. These timestamps describe acquisition, including pixels later rejected for radiance quality.

| UTC observation date | Local acquisition, approximately | Preceding work night | Current A2 production, UTC |
|---|---|---|---|
| 2025-06-18 | June 18, 03:25:22 EDT | June 17 | June 26, 15:40:10 |
| 2025-06-19 | June 19, 03:06:34 EDT | June 18 | June 27, 10:39:56 |
| 2025-06-20 | June 20, 02:47:44 EDT | June 19 | June 28, 16:09:43 |
| 2025-12-30 | Dec 30, 01:32:25 EST | Dec 29 | Jan 7, 15:21:34 |
| 2025-12-31 | Dec 31, 02:53:57 EST | Dec 30 | Jan 21, 17:28:41 |
| 2026-01-01 | Jan 1, 02:35:16 EST | Dec 31 | Jan 21, 18:33:56 |
| 2026-02-25 | Feb 25, 02:04:54 EST | Feb 24 | March 5, 12:57:19 |
| 2026-02-26 | Feb 26, 01:46:03 EST | Feb 25 | March 6, 14:14:48 |
| 2026-02-27 | Feb 27, 01:27:09 EST | Feb 26 | March 13, 16:05:06 |

All regional acquisition times precede their fixed conservative local-midnight cutoffs: June 21, January 2 and February 28 respectively. These are not exact operation onset claims. All nine current A2 production times follow those cutoffs. Production is a lower bound on availability for that version; it neither establishes first release nor rules out earlier versions. A retrospective physical-response analysis cannot be called an operational replay.

The [OPM calendar](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/) establishes June 19, 2025 and January 1, 2026 as federal holidays. The recovered June candidate dates correspond to a holiday eve and holiday work night; the January candidate is the New Year's Eve work night. Holiday handling is not yet frozen or fitted. No calendar adjustment has been invented from these files.

## Verification and remaining limits

The extraction uses NumPy 2.3.5 and h5py 3.16.0 with Python 3.12.14. `verify_measurement.py` independently decodes stored integer flags using Python's standard library, reconstructs time cutoffs and area-weighted fractions with math.fsum, and checks the two-control rule. It reproduces 1,170 primary pixel decisions and 36 regional fractions under each of four scenarios within 1e-12 absolute tolerance. Geometry, array alignment and input provenance have separate assertions in extraction. This does not validate the scientific proxy or substitute for independent geospatial review.

Nine selected dates are not a random sample of all weather or operating conditions; no general availability rate is inferred. Spatial cells are correlated. Changing valid-area composition can still bias future brightness averages even at 75% coverage. A score should use fixed cell-level baselines and examine common support rather than compare changing raw regional means.

No ordinary-date baseline, positive-control data, event score, threshold, alert-burden series, or contemporaneous NRT receipt log exists for this stage. Neither a detection rate nor a false-alarm rate can be estimated. No staffing sensitivity has been demonstrated.

## Reproduce

Install Python 3.12, NumPy 2.3.5 and h5py 3.16.0, then run from this directory with the three archive paths:

```sh
python3 code/inspect_uploads.py /path/iran_june_2025.zip /path/iran_feb_2026.zip '/path/venezuela_jan_2026(1).zip'
python3 code/check_measurement.py
python3 code/verify_measurement.py
```

Only continue after each command succeeds. The archive filename suffix is irrelevant: event identity comes from the verified embedded manifest. Always pass all three archives for the complete assessment. Scripts write small JSON evidence and extract the large HDF5 files into ignored `raw/`. `MEASUREMENT_SHA256SUMS.txt` records the released implementation and evidence. No credentials are needed to analyze existing uploads.
