# Rules fixed before inspecting radiance

Prepared 15 October 2026. This is a staged exploratory protocol, not a claim of preregistration or completed validation. Only the access stage has run.

## Scope and regions

Use Suomi-NPP Collection 2 A1/A2 only. Do not pool satellites or switch products after viewing results. `config.json` fixes four approximately 2 km by 2 km squares: a broad Pentagon area and comparison districts at Rosslyn, Reston Town Center and Tysons. These are analyst-defined regions, not property boundaries. They include surrounding lights and cannot identify employees, visitors or individual movements. Langley is not added to this first test.

The comparison districts are imperfect: different land use and lighting schedules, and possible defense-related activity, may confound or reduce differences. Normalize each region to its own earlier observations; do not compare raw brightness levels as if regions were interchangeable. Nominal 500 m cells are not independent observations and cannot be converted to headcounts.

## Access and measurement gates

First download one A1/A2 pair and inspect actual metadata/schema before implementing extraction. The download script does not perform extraction. Then inspect the nine selected dates using the same rules, reporting every exclusion.

Read A2 `DNB_BRDF-Corrected_NTL`; never substitute `Gap_Filled_DNB_BRDF-Corrected_NTL`. Collection 2 uses floating-point corrected radiance, unlike some older scaled-integer examples. Respect attributes in the actual files; mask fill values before scaling. Pair A1 `UTC_Time`, sensor angle and quality with the same tile/date. Retain file hashes and retrieval timestamps.

The strict primary screen is: finite non-negative observed radiance; A2 Mandatory_Quality_Flag = 0; Snow_Flag = 0; cloud bit 0 = night, bits 4–5 = high confidence, bits 6–7 = confidently clear; no shadow, cirrus, snow, aurora or lunar-eclipse flags; A1 QF_DNB = 0; sensor zenith at most 60 degrees; valid acquisition time. Reject missing/unknown flags. Source: Collection 2 guide Tables 5–10. Inspect flag-1 exclusions separately because the product's outlier screen could suppress a real unusual light change. Do not count unscreened A1 spikes as detections.

Require at least 75% valid area in the target and at least two controls, using fixed native-grid cell footprints/area weights. Missingness remains missing, never zero or interpolated evidence. Review masks before interpreting brightness.

## Timing

The manifest contains UTC observation dates, not local work-shift labels. Convert each actual A1 pixel time to America/New_York, accounting for daylight saving. Label after-midnight observations as the preceding evening's work night where appropriate, and retain both labels.

Initial conservative acquisition cutoffs are June 21, 2025 00:00 EDT; January 2, 2026 00:00 EST; and February 28, 2026 00:00 EST. They are deliberately conservative boundaries, not claims about exact operation start times. The selected dates precede them; verify actual pixel timestamps nevertheless. Any expanded event window must be documented before examining its radiance. A same-date early-morning image may follow an operation and cannot be called a warning.

For retrospective physical response, only acquisition must precede cutoff. For an operational warning claim, the exact version also must have been publicly available before cutoff. Production time is a lower bound on that version's availability; CMR updated time is not a first-release log. The current A2 versions fail the pre-operation production condition. Do not present retrospective standard-data findings as a replay of historical NRT alerts.

## Baseline and comparison stage — not yet acquired

After the measurement gate, obtain all calendar days from January 1, 2024 through March 31, 2026 for the same tile/products, processing sequentially and retaining small regional extracts. If transfer or storage costs are prohibitive, document a smaller design before looking at brightness results; do not select only clear or exciting nights. Download volume is a practical cost even when data fees are zero.

For each target date, use same-weekday observations from the preceding 84 days, requiring at least six valid baseline observations per cell. Calculate per-cell relative deviations from earlier medians, aggregate with fixed area weights, and subtract the median region-normalized deviation of eligible controls. Freeze any exact score formula and holiday handling before scoring, after inspecting schema only. Maintain the valid-area gate to prevent changing cloud masks from impersonating changes in light. Calendar confounders must be dated from independent sources before scoring: holidays/holiday eves (especially New Year), shutdowns, outages, snow and lighting/infrastructure changes.

Calibrate an alert threshold using 2024 only; evaluate on all eligible 2025–March 2026 dates, then report event-window scores, missingness, ordinary-date alert burden, consecutive alert episodes and sensitivity to controls. Do not tune thresholds on the three famous cases or label all other dates proven false alarms. A complete event register is needed for precision/recall claims.

## Positive control and stop rules

Before any military-event inference, check the same radiance/QA workflow on a well-documented broad electricity-loss example, initially the Houston February 2021 freeze (February 10 and 16 are NASA VEDA's published example dates). Use native science data and a fixed urban region with sufficient clear observations, not resampled color-image brightness. This positive control has not been acquired or run; freeze its exact geometry and baseline before inspecting its values. A major blackout establishes responsiveness to a large light change, not sensitivity to extra office workers or to brightening.

Stop without scoring a case if fewer than two pre-cutoff dates survive quality/baseline/calendar rules. Record it as unscorable, not negative. If the positive control cannot be measured, resolve the measurement problem before interpreting target results. If the archive cannot support an operational replay, report only the retrospective physical-response result. A null result in three cases cannot refute all possible institutional-activity indicators.
