# Can satellite night lights provide a cheap newsroom lead?

**16 October follow-up: the same downloads now support a two-night brightness comparison, but no staffing inference or anomaly backtest.** Relaxing the extra upstream stray-light veto recovers the June 19–20 pair. The central 500 m square rises **5.3%**, compared with **6.6%** in disjoint nearby surroundings and **6.9%** in the original 2 km square. The increase is not strongest in the smallest building-centred area. January and February still have only one usable night each. [Full follow-up, spatial test and synthetic dilution test](FOLLOWUP_RESULTS.md).

The next priority is independent evidence linking aggregate overnight occupancy to visible light at the satellite overpass hour. More event images alone will not establish that relationship. No alert or completed anomaly backtest is claimed. The original screening result below is retained for comparison.

**15 October 2026: all three uploaded archives have been processed. The original quality rules leave every case unscorable. This is a completed measurement-feasibility test, not a completed brightness backtest. No warning signal has been established.**

The recommendation is to **pause further bulk downloads and keep night lights as a research option**. Access is solved. The remaining problems are usable observations, quality flags, holiday comparisons, sensitivity to office activity, and proof of timely delivery.

We verified all **18 NASA files**, covering nine dates and four broad areas: **588.7 MB / 561.4 MiB**, with no data fee. We checked a roughly 2 km square around the Pentagon against similarly sized areas at Rosslyn, Reston Town Center and Tysons. These squares include surrounding roads and buildings. They measure neither employees nor occupancy.

## The three-case result

A usable date requires at least **75% valid area in the target and two comparison areas**. A case needs at least **two usable dates**, followed by baseline and calendar checks. The latter checks have not been reached.

| Historical case | Dates examined | Usable dates, original rules | Usable dates, exploratory quality changes* | Conclusion |
|---|---|---:|---:|---|
| Iran, June 2025 | June 18–20 | 0 of 3 | 2 of 3 | Original test unscorable; revised method warrants review |
| Venezuela, January 2026 | Dec 30–Jan 1 | 0 of 3 | 1 of 3 | Still below the two-date minimum |
| Iran, February 2026 | February 25–27 | 0 of 3 | 1 of 3 | Still below the two-date minimum |

\* These are **post hoc coverage diagnostics**, not detections or validated substitute rules. They retain the same areas, dates, 75% threshold, observed-data requirement and two-control requirement. They allow only the A1 stray-light-only flag and/or medium-quality cloud classification. They never admit cloudy pixels, snow warnings, other A1 flags, or poor-quality corrected-light retrievals. [All four scenarios](MEASUREMENT_TECHNICAL.md) remain separately reported.

In the initial 15 October measurement screen, no brightness means, changes, anomaly scores, hits or misses were calculated. The radiance array was read solely to check whether an observed value exists and is valid. The [16 October follow-up](FOLLOWUP_RESULTS.md) subsequently calculated descriptive brightness levels and changes; it still supplies no anomaly scores, hits or misses. Missing observations were not filled with earlier nights.

## What prevented a fair test?

**June: our initial filter may be too restrictive.** Two dates have over 95% usable target area under the corrected product's other requirements, but most of that area also carries an upstream stray-light flag. Our original rule vetoes it. NASA describes Black Marble's correction for stray light, so applying that extra veto deserves review; correction alone does not establish that residual error is small enough for an office-activity signal. With the veto relaxed, both dates have sufficient comparison coverage. We have not changed the primary finding.

**February: clouds remove two dates.** The remaining date rises from 18.4% to 93.8% valid target area if medium cloud-mask quality is accepted while still requiring confidently clear sky. One date is insufficient under the chosen case rule.

**Venezuela: weather flags and the New Year limit the test.** December 30 has partial cloud/missing coverage and a cloud-mask snow/ice flag across the target. Its separate Snow_Flag says no snow: that disagreement is recorded, not resolved by selecting the favorable field. December 31 has no observed corrected-light retrieval across the target and is classified cloudy. January 1 rises from 60.0% to 86.2% valid target area under the medium-quality diagnostic, with sufficient controls. It is still only one date, observed at about 02:35 local time after New Year's Eve.

The two recoverable June observations are at about 03:07 on June 19 and 02:48 on June 20, corresponding to work nights June 18 and 19. [OPM lists June 19, 2025 as a federal holiday and January 1, 2026 as New Year's Day](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/). Holiday-eve and holiday behavior therefore need handling before an ordinary-weekday comparison could be trusted. This is a calendar confound, not proof of a particular lighting change.

## Does it meet the original brief?

| Requirement | What this test establishes |
|---|---|
| Extremely cheap | NASA data fee is zero; this batch was 561.4 MiB. Analyst time and repeated transfers remain costs. |
| Broad aggregation | Yes: fixed areas of about 4 km²; no phone data, identifiers, trajectories or small cohorts. |
| Timely | Not established. Every downloaded corrected-file version was produced after its conservative event cutoff. |
| Backtestable | Historical files exist, but these windows fail the original measurement gate. No ordinary-night baseline was acquired. |
| Detects an extra 1,000–2,000 workers | Unknown. More people can leave exterior lighting unchanged; brightness cannot be converted to headcounts here. |

The target observations occur between roughly **01:27 and 03:25 Washington time**. A timely satellite feed would still supply an overnight snapshot, not continuous evening monitoring. NASA documents a separate near-real-time service; the [LANCE FAQ](https://forum.earthdata.nasa.gov/viewtopic.php?t=5201) describes a roughly three-hour delivery goal and a roughly seven-day archive. Our historical queries found no matching NRT versions. That does **not** prove none existed: we cannot reconstruct historical warning delivery from this batch. Current versions' production dates are not first-publication logs.

## The useful next step

The next investment should be **a small method-validation exercise, not another large event download**. The [16 October follow-up](FOLLOWUP_RESULTS.md#what-would-answer-the-overnight-work-question) specifies a two-link validation: overnight work to light, then light to satellite. Its smaller-aperture and synthetic tests have been run on the existing batch; independent staffing validation and a baseline backtest have not. The earlier [NEXT_STEP.md](NEXT_STEP.md) preserves the original bounded proposal, flag questions, costs and stop rules. Real-time availability remains a separate untested requirement.

Before claiming a reporting lead, we need a defensible quality rule, an independent positive control, ordinary-night variability, an unchanged scoring rule and a count of alerts on other dates. A known blackout can test a large loss of light; it cannot establish sensitivity to extra office workers.

## Lessons to carry forward

1. **Obtain a small sample before transferring a long archive.** Catalog coverage is not usable coverage.
2. **Inspect actual product versions.** Collection 2 quality codes differ from older examples; an old tutorial can silently admit poor data.
3. **Separate failed observations from negative results.** None of these cases establishes that the area stayed normally bright.
4. **Audit the filters themselves.** Extra caution can discard corrected observations. Relaxations must remain visible and cannot become successes after seeing the cases.
5. **Preserve three clocks and the local work night.** Acquisition, availability and the event are different times.
6. **Validate the link to activity.** A technically excellent light measurement may still be a poor staffing proxy.

## Inspect or reproduce

- [16 October follow-up results and recommended validation](FOLLOWUP_RESULTS.md)
- [Follow-up protocol frozen before brightness inspection](FOLLOWUP_PROTOCOL.md), [machine-readable results](evidence/followup_results.json), and [independent checks](evidence/followup_verification.json)
- [Technical report, date-by-date coverage and timing](MEASUREMENT_TECHNICAL.md)
- [Bounded next step and stop rules](NEXT_STEP.md)
- [Original protocol](PROTOCOL.md) and [fixed regions and primary rules](config.json), unchanged
- [Machine-readable results](evidence/measurement_results.json)
- [Verified input hashes and download receipts](evidence/verified_uploads.json)
- [Independent verification result](evidence/independent_verification.json)
- [Preserved earlier access-stage audit](ACCESS_AUDIT.md)

Code and small quality extracts accompany this report. The 18 large science files are reproducible from the exact download manifest and are not committed to GitHub. The independent check reproduced **1,170 pixel decisions and 36 regional summaries across all four scenarios**, within numerical tolerance. The original six Iran results were also reproduced before finalizing Venezuela.

Primary product references: [NASA Collection 2 guide](https://landweb.modaps.eosdis.nasa.gov/data/userguide/BlackMarbleUserGuide_Collection2.0_20241203.pdf), [NASA Black Marble description](https://viirsland.gsfc.nasa.gov/Products/NASA/BlackMarble.html), and [NASA's quality-code changes](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A2/). Numerical results are this project's calculations from the uploads.
