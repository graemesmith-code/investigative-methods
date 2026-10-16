# Follow-up fixed before brightness inspection — 16 October 2026

This is an explicitly exploratory follow-up requested after the first quality screen. Existing quality coverage and the three case identities are known. No regional brightness values have yet been inspected. Use only the same 18 uploaded science files; no new observation dates, satellites or tiles. Preserve the original result.

## Questions and limits

1. Do the original extra quality vetoes materially alter availability or the brightness of the spatial sample retained?
2. Does a building-centred area have a distinct light measurement from the wider neighbourhood, and are changes localized there?
3. How much would a hypothetical localized change be diluted by broad-area aggregation?

There is no independently labelled occupied/unoccupied night, no ordinary-night baseline and no direct window-light measurement in this batch. These tests cannot establish that working overnight makes a building brighter, estimate worker numbers, assign causation, or validate a military warning detector.

## A. Quality and spatial selection

Reproduce the original four quality scenarios. For follow-up brightness diagnostics, use the combined relaxed screen already reported: observed finite non-negative A2 corrected light, mandatory quality 0, both snow checks, night, confidently clear, medium-or-high cloud-mask quality, no shadow/cirrus/aurora/eclipse, A1 flag exactly 0 or 16, sensor zenith <=60 degrees and pre-cutoff valid acquisition time. Call this the exploratory mask; do not claim it is a newly validated recommended rule.

For every region/date, report area coverage and mean observed corrected radiance under each screen if coverage is at least 75%. Also report diagnostic means on smaller retained subsets with their exact coverage, labelled unsuitable for an event score. Compare retained A1-flag-0 and recovered flag-16 subsets within June scenes to expose spatial selection; their difference is not a correction error estimate because the locations differ.

## B. Apertures and common pixels

Retain all four original 2 km squares. At the fixed target centre implied by the original box, construct nested 500 m and 1 km squares using the same latitude/longitude scaling as the original config. These are analyst-defined building-centred apertures, not measured building boundaries.

Also define a disjoint surrounding region: retain original target-square pixel weights only for native grid cells that do not intersect the 500 m aperture. This prevents the core and its comparison ring from sharing raster values. Report the number and union footprint of core-intersecting cells, not just the small nominal aperture area. Geometric partial-cell weighting does not provide subpixel localization.

Use area-weighted means of observed A2 corrected radiance in native units. No gap-filled data and no raw A1 spike interpretation. Report level ratios of core to disjoint surroundings only when both have >=75% coverage. A bright core does not demonstrate that its windows or staff caused the light.

For within-event temporal comparisons, examine every chronological pair of dates in each case, using the intersection of valid native cells between dates. Require >=75% common support in the target and >=2 of the original 3 controls; apply the same support rule separately to smaller apertures. Compute 100*(later/earlier-1) for the area-weighted mean on identical pixels. Subtract the median percentage change of qualifying control regions, and show each control's result. Do not call this an anomaly score: both dates may already be affected, and no normal baseline exists.

For the expected June 19–20 pair, additionally report unchanged-primary-mask common support and all four mask results, without dropping the common-support rule after seeing values. If smaller apertures fail their gate, report the missing comparison rather than loosen it.

## C. Synthetic sensitivity in light units only

On the first chronological scene where the core and broad target both meet exploratory coverage, add hypothetical +10%, +25%, +50%, and +100% to observed light in all grid cells intersecting the 500 m aperture. Recompute broad-area means with unchanged masks. This deliberately optimistic raster perturbation affects entire mixed cells, not an identified building; it quantifies arithmetic dilution only. It cannot estimate detection power, false alarms, people, or real radiometric uncertainty.

Report a comparison with the observed pair variation where available, but do not turn that variation from two nights into a noise distribution. Do not estimate statistical significance from spatial pixels as if independent.

## Reporting

Retain all nine dates, including failures, and write exact native-grid values, flags, area weights and results. Produce readable tables and a fixed-scale spatial plot for qualifying June scenes, with fill/exclusions distinct from darkness. A change in sign or magnitude across apertures/controls weakens an institutional interpretation. Save code, this protocol, its pre-analysis hash, outputs, limitations and next decisive occupancy-validation design to the existing GitHub project.
