# Technical protocol: global historical base illumination
Version 0.1, 18 October 2026. Proposed analysis; no global results yet.

This protocol accompanies [the funding proposal](README.md). Items marked **provisional** must be resolved on development data and registered before opening held-out results. Changing them later requires a logged amendment and exploratory labeling.

## 1. Population, units and estimands

**Target population:** publicly documented geographic sites used by U.S. military organizations at some time during 2012–2025, worldwide. This is an ascertainable public-record population, not all actual or classified U.S. military presence.

Include domestic and foreign sites but report them separately. Retain former sites. Record leases, shared host-nation sites, rotational access and contingency facilities as different relationships. Access to a whole airport does not establish exclusive use of its illumination.

Maintain:
- an installation identifier for the administrative entity;
- a site identifier for a geographic place;
- source-specific record IDs and aliases;
- a measurement-footprint identifier where adjacent or overlapping sites cannot be optically separated.

Never sum two overlapping site footprints as independent light sources. A merged optical footprint can retain multiple administrative links. Site mergers, subdivisions and renamed facilities require explicit crosswalks.

Three estimands must remain separate:
1. **Fixed-place change:** radiance over a fixed site footprint at different dates, including before U.S. occupation and after departure.
2. **Documented-presence change:** counts and, where boundaries support it, area of documented U.S.-used sites by date.
3. **Contemporaneous-site illumination:** light measured at places documented as U.S.-used at that date. Its trend changes with both light intensity and membership; it is not a fixed-panel trend.

A fourth, more ambitious estimand—change in light attributable to U.S. activity—is generally unidentified for shared sites. It requires unusually strong local evidence and must not be generalized.

## 2. Historical register and geometry

### Source integration

Start with FY2024 geocoded records, then add older BSRs, the 2015/2021 Vine lists and opening-date material, and corroborating official U.S./host-country sources. [S4–S7] Log source coverage by year and geography. The available BSR archive is not a complete annual panel.

For every occupancy or event claim retain the source, publication date, event date or interval, quotation/page locator, evidence type and researcher decision. Distinguish planned, announced, effective, completed and cancelled changes. Do not date a closure from the first year a row disappears.

Occupancy intervals may be uncertain: store earliest/latest plausible start and end. An uncertain event month is not an exact month. Main event analysis requires dates precise enough for its windows; otherwise use annual case descriptions or sensitivity over the interval. Sites active before 2012 are left-censored; those continuing after 2025 are right-censored.

Two researchers independently review every held-out site's status and geometry. For the full register, double-review all major reported events and a stratified 10% of other entries. Resolve disagreements before publishing; retain the original decisions.

### Location classes

| Tier | Evidence | Use |
|---|---|---|
| A | Verified public boundary, correct geographic identity and sourced occupancy history | Main polygon analysis if optical conditions qualify |
| B | Verified location but approximate footprint or inseparable shared facility | Sensitivity/case analysis; distinguish whole-facility light from U.S. component |
| C | Town/parent pin, conflicting coordinates or unresolved identity | Register only, pending verification |

Tier A geometry does not automatically imply measurable military light. Score optical suitability separately: facility size relative to the sensor footprint, baseline signal above local background, nearby light sources, snow/latitude, coastal pixels and shared uses.

For each eligible site, freeze a reference polygon using documentary and daytime imagery evidence **before examining its nighttime change**. Prefer a fixed maximum documented developed footprint across the study interval for the main within-place comparison; this avoids changing the spatial denominator when a site expands. Keep original and date-specific boundaries as separate objects. Document cases where a maximum footprint includes prior civilian use.

Use boundary erosion/dilation sensitivity at approximately one native DNB footprint, where sensible. Do not automatically exclude small sites with erosion that leaves no area: classify them as unresolved by that test. No smoothing or fractional-pixel weighting creates building-level resolution.

For isolated facilities, an additional, explicitly named “site plus light spill” mask can test overglow. Define it from geometry and development rules, not from the post-event light disappearance. Dense urban sites may never be separable. OSM tags and polygon histories are leads, not proof of U.S. use.

## 3. Satellite product and availability audit

Primary candidate: NASA VNP46A3 Collection 2 monthly composites on a 15-arc-second grid. Use one frozen archive/product specification, not a mixture of Collection 1 and 2. The grid is finer than the effective DNB footprint; it does not resolve individual buildings. [S3, S9]

**Provisional primary band:** all-angle, snow-free composite to preserve observations. Near-nadir snow-free is a required sensitivity analysis; geometry effects could justify promoting it to primary during development. Record the final choice and coverage cost before validation. Do not choose the band with the most appealing event response.

For every granule preserve collection, platform, tile, acquisition interval, processing timestamp/PGE version, source URL, bytes and checksum. Inspect actual platform flags; reject unexplained platform changes. An alternative sensor series requires overlap calibration and a separate sensitivity result. No automatic stitching.

Before analysis:
1. Enumerate unique tiles intersecting site and control polygons.
2. Query the archive for all intended months; record absent, duplicate and revised products.
3. Inspect representative files from early, middle and recent years.
4. Check calendar coverage, sensor gaps, valid fields, scale/offset, fill values, platform and quality rules.
5. Publish the difference between a product file existing and useful observations existing within a site.

The intended period is 168 months, January 2012–December 2025. An illustrative 1,624-site table has 272,832 site-month rows, but the historical union and exclusions will change this count. Do not advertise “continuous” time series before this audit.

### Data volume and processing

NASA lists approximately 58 MB per monthly tile. [S3] Illustratively, 100 unique tiles × 168 months × 58 MB is about 974 GB decimal before working copies; 50 tiles is about 487 GB. These are scenarios, not an audited tile count or storage quote. Four copies of a 100-tile scenario approach 3.9 TB.

Cache each tile once for all sites; process month by month and write small site summaries. Avoid loading a continental multiyear raster cube into RAM. Benchmark a few tiles before bulk retrieval. Record download bytes, wall time, peak memory and cost. If permitted cloud subsetting can reduce transfer, validate its output against a local reference extraction. No paid service or commercial imagery is required for the initial design.

## 4. Quality and missingness

The Collection 2 guide's monthly Table 12 defines quality 0 as more than three observations, 1 as three or fewer, 2 as historical gap filling and 255 as fill. [S9] Use product-specific attributes in the actual files and test parsing.

**Provisional main cell eligibility:** finite, in-range snow-free radiance, matching quality flag 0 and observation count at least four. Exclude fill/gap-filled values from change inference. Carry the observation count and temporal standard deviation; neither is a substitute for a formal error model.

Do not copy the previous daily A1 stray-light veto onto corrected monthly A3 values. Do not turn cloud, snow, missing granules or gap-filled cells into zero radiance. Do not silently clip valid small negative radiances: follow the product's documented valid range, and record any handling needed for a chosen product.

**Provisional site-month eligibility:** at least 80% of the fixed footprint area has eligible observations. Run 70% and 90% area gates as sensitivity analyses. Changing the fraction changes coverage, not the underlying observed light.

**Comparisons:** recompute before/after values on their common valid spatial support, requiring at least 80% of the fixed footprint under the main rule. Where a constant long-window intersection becomes too small, shorten the comparison or mark it unavailable; do not scale a partially observed sum to the whole site without a justified model.

**Annual summaries:** initially require at least nine eligible months, with at least two in each calendar quarter. Compare the same calendar months between years. If seasonal darkness/snow makes this impossible, publish a separately labeled fixed-season series; do not compare a winter-heavy estimate with a summer-heavy one or include these in a homogeneous annual global total.

These coverage cutoffs are proposed working rules, not NASA prescriptions. Report failure rates by region and site type, sensitivity to rules, and why exclusions occurred. Freeze changes using development data only. Missingness can be systematically associated with location and time; it is not random merely because a quality flag removed it.

## 5. Measurements and normalization

Let r(p,t) be eligible radiance in cell p at month t. Let a(i,p) be the geodesic area in square kilometres of cell p intersecting fixed footprint i.

On a stated common support C:
- mean radiance R(i,t) = sum[a(i,p) × r(p,t)] / sum[a(i,p)];
- area-integrated radiance L(i,t) = sum[a(i,p) × r(p,t)].

R has units nW cm^-2 sr^-1. L has those units multiplied by km². L is a comparative integrated-radiance measure, **not watts, electricity use or total physical luminous flux**. Apply latitude-dependent cell area; counting equal-grid cells as equal area biases global comparisons.

Publish the observed area alongside every value. Never compare totals on different amounts of observed land as if only brightness changed. Aggregate overlapping polygons through a dissolved geographic union, not by double-counting component sums.

Report absolute changes and relative changes only when the baseline is reliably above the development-set detection floor. A barely lit site can yield a spectacular meaningless percentage. Estimate a local noise/detection floor from stable comparison areas and pre-event variation; freeze the floor rule before holdout. No universal percentage-to-personnel conversion.

For an atlas, index each site's adequately observed reference period to 100 and show the original radiance too. Do not use a post-opening baseline to imply that a site existed earlier. Sites without a defensible common baseline should display absolute radiance or a clearly identified site-specific baseline, not participate in a common-base global index.

## 6. Civilian references and confounding

Select comparison areas using pre-event evidence only, preferably multiple nonmilitary areas in the same broad climate/grid setting with similar baseline brightness and urban context. Preserve raw site series as the primary observed outcome.

A nearby annulus is a diagnostic, not a perfect control. It can contain military spill light, base-dependent businesses or the economic consequences of closure. Exclude obvious airports, flares, industrial developments and other military sites; map exclusions. Where no credible control exists, show an unadjusted case with that limitation.

A reference-adjusted change can be the site's matched-month change minus the weighted change in preselected comparisons. Freeze weights from pre-event data. Interpret this as adjustment for shared variation, not automatic causal identification.

Log plausible alternative explanations:
- general electricity outages, war damage and grid expansion;
- LED replacements, shielding, lighting schedules and environmental policies;
- civilian airport operations, urban development and land-use conversion;
- snow, vegetation, fires, flares and residual atmospheric contamination;
- view angle, platform calibration and processing revisions.

LED changes can alter the sensor-observed spectrum without proportional changes in visible illumination or activity. Seek maintenance/energy records in prominent cases. A stable result across two processing products is helpful but not fully independent when both use the same sensor.

## 7. Validation design and provisional decisions

Use the 48-site, four-class design in the proposal. Randomize development/holdout assignment within feasible strata with a recorded seed after independent histories and geometry are ready. Group linked sites where possible. Keep the holdout event labels from the extraction analyst until settings and output files are frozen. These are safeguards against tuning, not proof of independence.

For events with adequate data, compare the 12 months before with the 12 months after the transition, omitting the event month and matching calendar months. With multi-month construction or uncertain dates, predefine transition exclusions and test wider windows. Require at least nine matched eligible months under the initial annual rule. Confirm persistence in the following year where available; late-2025 events cannot pass a two-year persistence check in this dataset.

**Provisional sustained-change rule:** a matched-year radiance difference of at least 20% from an adequately bright baseline, exceeding the 95th percentile of absolute matched-year changes in development-set continuing controls, with the same direction in a majority of matched months. Report 10%, 20% and 30% thresholds as sensitivity, without selecting the best on holdout. If the baseline is near the detection floor, use absolute radiance evidence and report separately.

The 20% threshold is an initial practical effect-size choice, not established sensor performance. Its freeze requires the remote-sensing scientist and statistician to examine development noise. If changed, document why before validation.

Report:
- counts of sampled, documented, measurable and classified sites, by class;
- direction, magnitude, seasonal persistence and sensitivity for every case;
- physical-event detection rate and continuing-site false-positive rate;
- separate departure/transfer outcomes, including unchanged or brighter sites;
- binomial uncertainty intervals, with a warning that episode dependence and purposive sampling limit their interpretation.

In the planned holdout there are only 12 physical-change sites and six continuing sites. Even 10/12 successful detections has a roughly 55–95% Wilson 95% interval; zero false positives among six is compatible with an upper rate around 39%. Therefore this phase is a feasibility gate, not a precise performance certification.

**Provisional expansion signal gate:** at least 9/12 held-out physical transformations show the expected sustained direction, no more than 1/6 continuing sites triggers, and conclusions survive the main sensitivity analyses. Count unevaluable physical cases against this operational gate, while also reporting conditional accuracy among measurable cases. With fewer documented cases, report the smaller denominator and revise the claim, not the threshold after seeing results.

The pilot may show that the departure question is not recoverable even when physical transformation is. Do not redefine a transferred, illuminated base as a successful closure detection.

Assess reporter usefulness through a small blinded review: two journalists first receive records-only case files, then satellite findings, and document whether the latter adds a specific, checkable question. A proposed practical gate is at least three materially new leads among eight mixed-outcome cases, independently corroborated before publication. This is an editorial value assessment, not a statistical accuracy estimate.

## 8. Statistical analysis and global summaries

The primary release is descriptive. For individual events use matched-season differences and reference comparisons; report observational associations.

Do not fit a generic two-way fixed-effects event study and label its coefficient “the effect of U.S. withdrawal.” Withdrawals can coincide with regime change, war, power-system disruption and changes in civilian economic activity. The statistician must separately justify any causal design, treatment timing, anticipation assumptions and comparison group. Causal inference is outside the guaranteed deliverable.

Spatial cells and adjacent months are not independent experimental subjects. Do not obtain tiny p-values by treating every pixel as a replicate. Use site/episode-level summaries, and, when uncertainty resampling is justified, temporal blocks and geographic/episode clusters. Publish sensitivity ranges separately from statistical confidence intervals.

For global or regional summaries:
1. Show a fixed eligible-site panel and its geographic coverage.
2. Show documented entries/exits separately, with date uncertainty.
3. Show the dynamic contemporaneous-use panel, labeling composition changes.
4. Report equal-site and area-integrated summaries; explain why they differ.
5. Repeat excluding Afghanistan, Iraq, the largest light-contributing sites, and urban/shared facilities.
6. Show unavailable site counts/area by year; never infer that the measured subset represents all sites.
7. Avoid national or global expansion factors without a justified sampling frame.

A regional rise in lights and a different region's decline does not demonstrate transfer of assets. Linkage requires procurement, construction, personnel or other documentary evidence.

## 9. Data structure and reproducibility

Minimum relational tables:

| Table | Required fields |
|---|---|
| sites | site_id, installation_id, aliases, country/territory, geography_class, facility_type, relationship_type, inclusion_basis |
| source_records | source_id, URL, publisher, publication_date, retrieval_date, checksum, original_record_id, page/locator, rights |
| occupancy | site_id, operator/use, start_earliest/latest, end_earliest/latest, evidence_ids, confidence, reviewer |
| events | event_id, site_id, event_type, announced/effective dates or bounds, independent_evidence, physical_outcome, episode_id |
| geometries | geometry_id, site_id, CRS, geometry, source, validity_interval, reference_or_dated, verification_tier, review_date |
| observations | geometry_id, month, product/granule IDs, platform, band, R, L, eligible_area_fraction, observation_count_summary, quality_counts, missing_reason |
| comparisons | comparison_id, target/control IDs, selection_basis, fixed_weights, preperiod, diagnostics |
| decisions | exclusion/amendment ID, reason, author, timestamp, pre/post-holdout status |
| outputs | analysis_version, code_commit, input_manifest_hash, configuration_hash, generated_timestamp |

Use WGS84 for exchange geometry with geodesic/equal-area calculations as appropriate. Preserve original geometries and repairs. Validate coordinate order, units, antimeridian crossings, invalid polygons and tile boundaries.

Pipeline stages: ingest sources → resolve identities → verify histories/geometry → freeze sample → inventory granules → extract/QC → create common-support comparisons → validate → aggregate → publish.

Test substantive failure risks: fill values mistaken for zero; quality flags from the wrong collection; coordinate swaps; incorrect scale factors; double-counted overlapping sites; latitude-biased areas; date shifts; and a missing month falsely creating a closure. Maintain small synthetic fixtures for these implementation risks, plus a manually checked real site-month.

AI may suggest aliases, extract document passages and flag conflicts. Human reviewers must verify identities, dates, boundaries and causal language. Store evidence pointers; model-generated assertions cannot become primary sources. Pin software versions and configuration; keep credentials out of repository and notebooks.

## 10. Publication and review

Atlas styling must separate status from illumination—for example, a status outline and a radiance-change color. Show missing observations as missing, not dark. Provide monthly/annual choices only where supported and disable interpolated “continuous” animation across gaps. Tooltips show geometry tier, usable coverage, measurement units, event evidence and whether attribution is shared.

Release historical evidence, methods and exclusions with the findings. Check each source's reuse terms: publicly accessible spreadsheets and OSM contributions are not automatically unrestricted or public domain. Government records, author-created geocoding and imagery have distinct rights. No individual movement or ad-tech data is involved.

Before expansion, commission a remote-sensing/statistical methods review independent of production. Before publication, review the historical classification and regional coverage. A reviewer can endorse reproducibility while rejecting a withdrawal interpretation; report those judgments separately.

The deliverable remains worthwhile if its strongest result is a sharply bounded one: “large isolated facilities often show physical transformation; many shared or urban sites do not provide a usable measure of U.S. presence.”
