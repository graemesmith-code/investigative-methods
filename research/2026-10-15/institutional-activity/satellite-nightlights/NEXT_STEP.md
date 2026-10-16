# A bounded next step for the night-light method

**Decision: do not acquire the original multi-year baseline yet.** The present primary test is unscorable in all three cases. More event-adjacent images alone cannot establish a useful lead detector. The following is a proposed follow-up design, not work already run or a scheduled collection.

## 1. Resolve the mask before inspecting brightness

Review these concrete questions against the exact Collection 2 datasets and quality extracts:

1. When A2 mandatory quality is 0 and its observed corrected radiance is present, should upstream A1 QF_DNB = 16 still veto the pixel? What residual stray-light uncertainty remains, and how does it compare with small changes in city lighting?
2. When cloud confidence is confidently clear but cloud-mask quality is medium, what validation supports retaining a pixel for small day-to-day differences?
3. How should a disagreement between A2 Snow_Flag and cloud-mask snow/ice bit 10 be handled? December 30–31 are concrete examples. Do not select whichever field retains more data.
4. Can mandatory flag 1's outlier component erase real brightening, and how should that limitation be quantified without admitting contaminated values?

The published documentation establishes flag meanings and correction steps, but does not settle every small-signal acceptance decision above. A qualified remote-sensing review or a written clarification from the product team would be useful. No external inquiry has been sent. Preserve the original primary result and version any replacement rule before reading event brightness.

## 2. If a defensible mask emerges, test coverage on independent dates

Use the same satellite, collection, tile, four regions and 75%/two-control gate. Proposed fixed sample: **June 1–14, 2024; December 15–28, 2024; February 1–14, 2025** (42 dates, 84 A1/A2 files). Select all dates in those blocks, including weekends, holidays and cloudy days. These dates are independent of the three case windows, not certified negative military-event examples.

At this batch's average size, transfer would be roughly **2.56 GiB**. That is an estimate, not a catalog quote or authorization to expand it. A prospective 28-day two-product collection at the same average would be roughly 1.71 GiB. By comparison, the original January 2024–March 2026 daily plan contains 821 dates / 1,642 files, roughly 50 GiB at this average, before another tile or positive control.

Record quality availability, missingness runs, processing time and byte costs before producing brightness scores. A proposed practical gate is at least 7 qualifying dates in each 14-day block and no more than four consecutive unavailable days in a block. These are newsroom usability choices, not scientifically validated universal thresholds. Fix them before acquiring the follow-up; failure would deprioritize this feed as a dependable sole source. Passing would only justify a larger feasibility study. Three short seasonal blocks cannot establish annual reliability.

## 3. Validate a physical measurement before an event detector

Freeze the geometry and baseline of the planned documented power-outage positive control before acquiring its native science files. Test that the pipeline recovers a large independently established light change, without gap-filled observations. A blackout tests dimming; a separately documented broad increase in exterior lighting would better address brightening. Neither demonstrates sensitivity to additional office occupancy.

On independent ordinary dates, quantify variability from view angle, illumination, snow and changing valid cells. Define the exact cell-level normalization, baseline requirements and control subtraction before any event scoring. Use synthetic radiance perturbations only to measure computational sensitivity in radiance units, never to invent a conversion to people.

## 4. Separate retrospective and live questions

For a retrospective study, keep the original cases visibly unscorable under their original rule. Any later re-analysis is exploratory and must include independently selected events and calendar rules. The surviving June dates are holiday-linked; the original same-weekday baseline proposal does not by itself solve that. Do not keep expanding windows until two favorable dates appear.

For timeliness, a later bounded NRT collection must preserve exact bytes/version, observation timestamp, successful first-retrieval time, preceding unsuccessful checks and delivery time to an editor. Polling gives an interval for availability, not exact publication time. Standard and NRT outputs must be compared separately; a standard-data model is not automatically valid on NRT. Retain the feed before its rolling archive expires. No continuous or scheduled scientific-data collection has been started here.

## Editorial stop rule

Until these gates pass, describe the result as **a free broad-area satellite source with unresolved coverage, sensitivity and live-delivery feasibility**. Do not issue military-activity alerts from it. If method review cannot justify a stable mask cheaply, move the next pilot to a different measurement, such as the previously proposed aggregate road counters, while preserving this result. This exercise does not show that every aggregate-activity signal fails.
