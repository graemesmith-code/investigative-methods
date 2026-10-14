# RAB-LIDAR-20261014-01 — Washington Lidar Portal

This dated catalog addition describes a reusable public-data source and a proposed reporting recipe. It supplements the [Rabbit catalog](../README.md); it is not a recovered export or a completed investigative experiment. No existing `SYS`, `AP` or `MAP` identifiers are changed.

- **Publisher:** Washington State Department of Natural Resources (DNR), Washington Geological Survey.
- **Official domain / representative URL:** [lidarportal.dnr.wa.gov](https://lidarportal.dnr.wa.gov/).
- **Jurisdiction / record family:** United States — Washington; geospatial, environment and extractives (existing catalog family RF-30).
- **Coverage:** Washington project footprints, including overlapping historical surveys; availability and products vary by project. Do not assume complete statewide coverage or that a project's bounding box contains data everywhere.
- **Access modes:** Public map preview; project or area-of-interest downloads; lidar image services for GIS. The [official help](https://lidarportal.dnr.wa.gov/help.html) explains these routes.
- **Cost / eligibility:** Public portal and metadata queries were accessible without an account or payment. DNR's [program page](https://dnr.wa.gov/washington-geological-survey/publications-and-data/lidar) describes public distribution and links free alternative downloads. No paid service is required for the proposed first check; local storage, bandwidth and reporting time still cost resources. Successful full-file download was not verified here.
- **Refresh cadence / historical dates:** Project-based historical acquisitions, with new and historical collections added over time; no guaranteed revisit interval. Project-name years and catalog update dates are not precise flight dates. Record acquisition start/end dates from the technical report and, where needed, individual tile or flightline metadata before drawing time-specific conclusions.
- **Resolution:** Read each project's raster cell size, point density, horizontal/vertical accuracy, coordinate system, vertical datum and units. No universal resolution or verified Kitsap specification is assigned by this entry; cell size and point density are different quantities.
- **Reuse / licence:** Public access does not establish unrestricted republication rights. Review the downloaded project's use constraints, attribution and contributing-agency terms. DNR's [GIS portal](https://data-wadnr.opendata.arcgis.com/) provides an accuracy and fitness disclaimer; this review establishes no blanket licence for every contributed dataset.

## Access points and checked example

| Local access ID | Route | Useful first action |
|---|---|---|
| RAB-LIDAR-20261014-01-A | [Washington Lidar Portal](https://lidarportal.dnr.wa.gov/) and [help](https://lidarportal.dnr.wa.gov/help.html) | Preview an area; inspect all overlapping projects and explicitly select the desired products |
| RAB-LIDAR-20261014-01-B | [Portal project index](https://lidarportal.dnr.wa.gov/project) | Save the project name, publisher-side project/dataset IDs and product names; this is the portal's implementation endpoint, not a guaranteed supported API |
| RAB-LIDAR-20261014-01-C | Area-of-interest selector and image-service links in the portal | Request only necessary tiles or use a GIS image service before downloading a whole project |

On **14 October 2026**, the live project index returned **Kitsap Refresh23 2024**, publisher-side project ID **336**, with DTM **1807**, DTM Hillshade **1808**, DSM **1809**, DSM Hillshade **1810**, Metadata **1811** and Point Cloud **1812**. These are DNR IDs, not Rabbit IDs; retain the retrieval date and project name in case the service changes. The older **Kitsap County Opsw 2018** also appears. Their presence establishes discovery routes, not a verified comparison of the underlying surveys.

A small inland point-selection query returned available files and byte estimates for both Kitsap projects. The portal's metadata-download route for dataset 1811 returned **HTTP 403** in this check. No raster or point-cloud file was downloaded or inspected. Exact acquisition dates, file formats, density, accuracy and project-specific reuse terms remain to be verified from metadata. The portal HTML, help, project index and query response were checked; rendered GIS layers were not tested.

## Reporting recipe: historical shapes as leads

1. **Start with a dated public-interest question.** For example, did earthworks, a shoreline structure or a development footprint change between two historical surveys? Locate a known civilian feature as a positive control before interpreting an empty result.
2. **Preview cheaply.** Use the portal's area-of-interest tool or GIS image service. Start with a hillshade and metadata; download the smallest relevant tiles only if the preview warrants a closer look. Whole-project selections can be much larger. Free desktop GIS or a point-cloud viewer can support a local check without model calls.
3. **Choose the right product.** DNR distinguishes a DSM, which retains top surfaces such as buildings and trees, from a DTM, which represents bare ground. A ground model may deliberately remove the object of interest. Use the DSM or suitable point-cloud returns for above-ground forms, and the DTM for terrain. Hillshade is a rendering under simulated lighting, not an optical photograph or an identity label.
4. **Join by geometry and provenance.** Preserve project/dataset ID, original tile filename, acquisition interval, footprint, coordinate reference system, datum and units. Transform layers into a common coordinate system and intersect with dated parcel, permit, infrastructure or environmental-record geometries. Carry the official parcel/permit/asset ID into the result, preserving one-to-many matches and positional uncertainty. A nearby name, centroid or apparent silhouette is not an ownership or identity match.
5. **Compare compatible observations.** Align grids and check resolution, classification, ground conditions, vertical reference and survey accuracy before differencing heights. Use an unchanged control area. A publication timestamp cannot date a feature; a multi-day acquisition can combine observations from different times.
6. **Corroborate before reporting.** Treat an unusual shape or change as a lead. Check dated imagery, permits, engineering documents and other independent public records. Keep links, metadata, file hashes, a reproducible extent and notes on alternate interpretations. Automated or AI-assisted triage may suggest candidates, but cannot supply missing dates or verify identity.

This recipe is an editorial proposal based on DNR's product and access documentation. It has not been executed as an object-identification or change-detection trial here. It concerns retrospective public records; it does not establish current locations or operating status.

## Limits and false positives

Tree canopy, roofs and other structures can resemble another object in a DSM. Noise, misclassification, sparse returns, occlusion, water surfaces, interpolation and tile seams can produce misleading forms or apparent absence. Hillshade lighting changes appearance. Different survey dates, datums or processing methods can create false change. Geometry alone cannot identify a particular vessel, operator, owner or activity, and missing returns do not prove an object was absent.

If the DNR route fails, its program page points to the [Puget Sound Lidar Consortium](https://pugetsoundlidar.ess.washington.edu/lidardata/), USGS and NOAA as alternative discovery routes. The [USGS LidarExplorer documentation](https://www.usgs.gov/tools/lidarexplorer) describes preview and download of lidar and derived products. Check that any alternative actually supplies the same acquisition and product; an overlapping regional DEM may use much older surveys. These alternatives are discovery suggestions, not independently tested substitutes for the Kitsap download.

Link checks on 14 October 2026 returned HTTP 200 for the five linked DNR pages/endpoints. Direct checks of the PSLC and USGS documentation links returned HTTP 503 and 403 respectively, although their descriptions were available through indexed official pages. Availability may differ by client or change later.

## Provenance of the suggestion

The source-review request was prompted by [BenjaminDEKR's X post](https://x.com/BenjaminDEKR/status/2109823694428418528). Direct thread access was unavailable in this review. The post is a discovery pointer, not evidence for the project's exact acquisition date or a specific object identification. The catalog claims above rely on the linked official DNR documentation and live portal responses; this entry does not claim a full thread read or reproduce its reported result.

[Catalog guide](../README.md) · [Preserved originals and provenance](../../references/rabbit/README.md)
