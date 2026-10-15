# Technical record: first aggregate-activity test

**Status:** exploratory retrospective screen. The source data were downloaded and the calculation executed on October 15, 2026. This is not a live system or a validated predictor.

## Acquisition and checks

Public WMATA Tableau guest exports were obtained for Pentagon, Pentagon City, Rosslyn and Crystal City. Each station has three selections: all periods, PM peak (15:00–19:00), and evening (19:00–midnight), in Washington local time. These are separately exported totals, not hourly observations. Raw exports are UTF-16 tab-separated files.

The panel contains 14,688 rows and 29,376 entry/exit count cells across 1,224 dates. All 12 exports had complete date rows, no duplicate dates, no blank count cells and nonnegative integer counts. Six recorded zero cells were retained. Afternoon plus evening counts never exceeded the respective all-period counts. Checksums, filters and retrieval timestamps are in the kit. These checks establish internal consistency, not accuracy of the underlying faregate system.

No individual trip, device, identity or employer fields were collected. The 1,000-passage scoring floor is not a privacy guarantee and does not establish a 1,000-person cohort.

## Fixed first-pass rule

1. At each station, calculate `evening entries / (PM entries + evening entries)`.
2. Exclude declared holidays, special federal closures, the October 1–November 12, 2025 shutdown, selected documented severe-weather dates and affected February 2026 construction controls. This is a partial disruption calendar.
3. Require at least 1,000 PM-plus-evening passages at a scored station-day.
4. Compare with the median of the previous 12 valid matching weekdays, searching back no more than 16 weeks; require eight baseline observations. No future observations enter this baseline.
5. Subtract the median same-day deviation at available comparison stations from the Pentagon deviation. Require two comparison stations.
6. Use 2024 to set a positive threshold permitting at most `floor(N/15)` flags among its eligible dates, with strict greater-than comparison. It was **2.365528599 percentage points**, with 16 flags in 245 scored calibration dates.
7. Apply the fixed threshold to January 1, 2025–March 31, 2026. Primary event window: the previous three calendar evenings, requiring at least two valid scores. Do not substitute earlier evenings for a holiday or missing score. Window score is the maximum valid daily score.

The implementation clarifications and original protocol were written before the first anomaly-score run. The protocol document in the kit intentionally retains its pre-execution status wording; `RESULTS.txt` and the JSON record describe completed work. The event choices were already known, so this is not an independently registered experiment.

## Findings

- June 2025 Iran: largest adjusted pre-window deviation **+0.493675245 percentage points**; no flag; two valid evenings.
- January 2026 Venezuela: no valid primary-window evenings under the traffic/holiday rules. A stricter midnight-January-2 cutoff had only one. Both are unscorable.
- February 2026 Iran: largest adjusted deviation **+2.051434222 percentage points**; no flag; three valid evenings.
- Evaluation interval: 23 flagged dates out of 259 scored, across 455 calendar dates. Nearby flags were combined into 18 episodes using at most one intervening calendar date.

The background windows matched by Saturday endpoint and valid-evening count were very limited for June 2025: only five. Do not treat the resulting ranks as reliable significance estimates. No p-value, general sensitivity or precision is claimed.

## Clocks and interpretation

Metro's service date runs 04:00 to 03:59 the next calendar day. All-period Friday totals must not enter a Friday-midnight prediction. The primary rule uses only afternoon/evening blocks. Candidate event cutoffs were midnight Washington time on June 21, 2025; January 3, 2026; and February 28, 2026. These are pre-impact analysis conventions, not independently established mission-launch or first-public-report times. Venezuela's overnight January 2–3 sequence needs further verification before any warning claim.

The public archive has a seven-day publication lag. Today's downloadable historical figures may contain revisions. The analysis tests for a retrospective pattern, not what a newsroom could have known from this source at the time.

The numerator is rail entries, not staff, and changes in route, mode, visitors, transfers and operating hours can alter it. Employees staying through the entire night may produce no observed late departure at all. A null result therefore applies to this measurement and rule.

## Synthetic sensitivity

On 237 eligible dates outside a seven-day buffer around the three cases, add hypothetical evening target passages while holding the historical baseline and control values fixed. Adding 250 caused 216 dates to flag (195 newly flagged); adding 500 or 1,000 caused all 237 to flag (216 newly flagged). Twenty-one dates already flagged. This is a deterministic sensor-statistic sensitivity check, not observed activity, a longitudinal simulation or a conversion from workers to trips.

## Remaining risks

The military-event universe and disruption calendar are incomplete; comparison stations need further review; many low-volume/weekend dates are excluded; case cutoffs and holiday-season comparability remain imperfect. A full methods review should address these before inferring significance. Since this public feed already fails the required timeliness, further refinement is a research choice rather than a necessary step toward deploying it.
