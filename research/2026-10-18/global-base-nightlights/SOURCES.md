# Source register and completed checks
Checked for this proposal on 18 October 2026 unless otherwise stated. This is a source audit, not a global data-quality audit. Cached spreadsheet inspection was completed in the preceding project work; those files remain available.

## S1. World Bank methodological signpost

Oscar Barriga Cabanillas, Walker Kosmidou-Bradley, Silvia Redaelli, Eigo Tateishi and Ivo Teruggi. *Afghanistan’s New Economic Landscape: Using Nighttime Lights to Understand the Civilian Economy after 2021*. Policy Research Working Paper 10969, November 2024.

[Publisher PDF](https://documents1.worldbank.org/curated/en/099256511062426629/pdf/IDU1f7011ce815ecb1494d1a0e61042efed1a409.pdf)

Downloaded PDF, extracted text, read methods and visually checked printed page 10. Key locators: printed pp. 9–11 (data, masking and aggregation), footnote 11 (overglow/urban separation). The reported military-mask pixel counts must not be described as numbers of bases. We have not reproduced its numerical results.

## S2. Authors’ public implementation

[Repository](https://github.com/worldbank/afg_viirs_analysis)
[README at inspected revision](https://github.com/worldbank/afg_viirs_analysis/blob/87e025752a2aee9312717b7ccd0ec60ec3c7f431/README.md)

Inspected repository listing and README. Main revision retrieved: 87e025752a2aee9312717b7ccd0ec60ec3c7f431, dated 15 October 2024. The README describes alternative filtering pipelines and brightness-derived timing/operator classifications, which our independent validation must not reuse as truth labels. Code, notebooks and data directory exist; notebook execution, data completeness and rights have not been audited.

Replication work should first establish which pipeline/masks generated the published figures, whether all required inputs are available, and how results change under NASA Collection 2. A faithful replication and a product-substitution robustness test are different deliverables. Questions for the authors can be prepared; no contact has been made.

## S3. NASA monthly product

[NASA LAADS VNP46A3 product page](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A3/)
[Dataset DOI](https://doi.org/10.5067/VIIRS/VNP46A3.002)

Checked official Collection 2 description, nominal January 2012 start, monthly cadence, band options and approximate 58 MB file size. Collection 2 includes adjustments for SNPP spectral-response degradation. This supports product selection, not a guarantee of comparable radiance at every site throughout the period.

Still required: archive tile/month enumeration, first-year completeness, recent-year completeness, actual usable-pixel coverage and representative runtime benchmarks. No new global science-data download was performed for this proposal.

## S4. FY2024 geocoded inventory

[US Base Project data page](https://usbaseproject.com/data/)
[Original spreadsheet](https://usbaseproject.com/wp-content/uploads/2024/11/BSR-FY24_Lat-Long.xlsx)

Cached file: bsr2024.xlsx, 328,939 bytes. Prior inspection of Sheet1 found:
- 1,626 named rows excluding the header;
- 1,624 numeric coordinate pairs within latitude/longitude ranges;
- 1,546 distinct exact pairs;
- two missing/nonnumeric coordinate pairs.

These are mechanical record counts, not validated base counts. Shared pins may reflect related sites or coarse geocoding; they do not justify deleting records without review. Notes include use of town coordinates. Inventory contains both U.S. and foreign entries, with buildings, acreage, replacement-value and coordinate-source fields.

Still required: source snapshot/hash manifest, row-level quality review, historical identities, polygon matching, current-status verification and reuse terms for the geocoding contribution. Numeric coordinates establish syntactic validity, not correct location.

## S5. Historical Base Structure Reports

[US Base Project BSR archive](https://usbaseproject.com/base-structure-reports/)

Prior page check found reports for FY2012, 2013, 2014, 2015, 2017, 2018, 2019, 2020, 2022, 2023 and 2024. This is an archive listing, not completed extraction or an assertion that absent years cannot be found elsewhere. Reports and definitions require comparison before constructing a panel.

Still required: search official archives for gaps, extract original site IDs, reconcile changed reporting thresholds and treat omitted or unnamed sites explicitly.

## S6. Vine historical lists

[Author’s maps/data page](https://www.basenation.us/maps.html)
[Workbook](https://www.basenation.us/uploads/5/7/1/7/57170837/vine_david_lists_of_us_military_bases_abroad_1776-2021_final_2021_09_01_rev.xlsx)
[Archive DOI](https://doi.org/10.17606/7em4-hb13)

Cached workbook: vine2021.xlsx, 583,006 bytes. Contains historical snapshots including 2015 and 2021 and an opening-date sheet for named sites in 2020.

Prior mechanical inspection of the 2015 sheet found 679 named rows, 649 numeric in-range coordinate pairs and 398 distinct exact pairs. Rows and pins are not independent confirmed active bases. The 2021 sheet has a different schema; do not assume equivalent coordinates. Historical classifications and the inclusion of U.S. territories require normalization.

This helps recover places missing from FY2024. It does not supply a complete annually dated global boundary dataset. Corroborate event/status claims with primary documentation. Access through the author’s workbook succeeded; an archive-page access failure did not prevent inspection.

## S7. Official basing definitions and documentary anchor

[Congressional Research Service, R48123, 10 July 2024](https://www.congress.gov/crs_external_products/R/PDF/R48123/R48123.1.pdf)

Use as a source for the scope and definitions of overseas basing and references to official evidence. Its units and inclusion rules differ from a BSR site register; do not use disagreement in headline counts as evidence of missing facilities without reconciliation.

## S8. Official GIS boundary coverage check

[NTAD Military Bases FeatureServer layer](https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_Military_Bases/FeatureServer/0)

On 18 October 2026 queried /query with:
- where=1=1
- outFields=countryName
- returnDistinctValues=true
- returnGeometry=false
- f=json

Response contained one distinct countryName: **usa**. This is direct evidence about this layer's returned country classification, not a complete geographic validation of every polygon or proof that no overseas dataset exists elsewhere. The service therefore cannot be assumed to provide global overseas polygons. Obtain per-site geometry from additional documented sources.

## S9. NASA Collection 2 quality specification

[Black Marble User Guide, Collection 2.0](https://landweb.modaps.eosdis.nasa.gov/data/userguide/BlackMarbleUserGuide_Collection2.0_20241203.pdf)

October 2024 guide; downloaded and inspected relevant monthly quality documentation. Printed page 23, Table 12 provides monthly/annual quality values. Table 13 provides platform codes. Use the matching variable attributes in actual science files as well.

The proposed site coverage, annual completeness, effect-size and validation gates in our protocol are our research-design choices; they are not recommendations attributed to NASA.

## S10. Internal prior experiment

[Earlier NASA nightlights follow-up](../../2026-10-15/institutional-activity/satellite-nightlights/FOLLOWUP_RESULTS.md)

This small daily Pentagon study motivates transparent missingness, collection-specific quality handling and separation between observing light and validating an activity proxy. It did not establish an anomaly backtest or a global military-activity relationship. Its quality-mask correction should be checked for relevance to a different monthly product rather than copied mechanically.

## What remains unverified before funding expansion

1. Historical universe size after deduplication, former-site recovery and definition reconciliation.
2. Number and regional distribution of eligible, verified overseas boundaries.
3. Monthly archive and site-level usable coverage, including early 2012 and high latitudes.
4. Exact reproduction of a published World Bank result with its original inputs.
5. Held-out performance and false-positive rates for physical changes and departures separately.
6. Rights to redistribute each source-derived geometry/table.
7. Actual cloud/download costs, human verification time and scope achievable within the expansion budget.

No claim of being the first global study is made. A fuller prior-work review belongs in the funded feasibility phase.
