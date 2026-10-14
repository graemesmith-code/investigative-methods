# Historical lidar for public-interest reporting

**RAB-LIDAR-20261014-02 · reviewed 14 October 2026 · selective global source guide**

A journalist can use free historical laser surveys to check whether buildings appeared or disappeared, excavation expanded, industrial land grew, or a claimed restoration changed the ground. The best starting places in this review are **England, the Netherlands, Switzerland, Vancouver, Auckland and Spain**. They combine credible public archives, useful surface or point-cloud products, and documented reuse routes. Several have genuinely overlapping historical scans, rather than merely a promise to survey the country again.

Start with one civilian site and two dated surveys. Compare buildings with **point clouds or surface models (DSM)**; compare earthworks with **ground models (DTM)**. A DTM intentionally removes buildings and vegetation, so an apparently empty site can be a processing choice. A national “latest elevation” map can also combine several years and cannot establish when a change happened.

These measurements supply leads and bounded height or shape changes. They do not establish ownership, permits, production, waste composition, operational status or illegality. Pair them with dated imagery, environmental assessments, permits, engineering drawings and corporate or land records. Excavated volume is not automatically mineral production; roof size is not output; a stockpile is not necessarily waste.

**What was actually done:** four regional research workers checked official documentation and terms; anonymous small catalog/API requests and Dutch LAS header range requests tested selected access routes. No full change analysis, giant data download, paid service, account creation or outreach occurred. There is no claim of exhaustive global coverage or legal certainty. Some promising sources remain conditional because their historical footprint, license or anonymous download route needs another check.

## Ranked first choices

Rank reflects a cheap newsroom pilot, not universal data quality. “Repeat” below means the stated evidence, never a claim that every pixel has usable observations in both years. Detailed citations, access routes, terms and limits are in the regional annexes.

| Rank | Archive / pilot | Repeat evidence | Main reason to choose it | First hurdle |
|---|---|---|---|---|
| 1 | England Environment Agency — London Docklands | Official index returns overlapping TQ3580 point-cloud/DSM records for 2017–18 and December 2020 | Anonymous archive, dated products and OGL reuse; strong urban baseline | Tile flight dates, geoid transformation and comparable DSM processing |
| 2 | Netherlands AHN — Rotterdam | Same original C_37HN1 point-cloud tile in AHN3 and AHN4; both LAS headers sampled successfully | Many retained epochs; original point clouds, DSM and DTM; older epochs CC0 | Exact flights still to extract; full original tile is 2.0GB/9.38GB, so use small subsets |
| 3 | Switzerland swissSURFACE3D — Zurich | Official STAC returns the same tiles 2682-1247 and 2683-1247 for 2018 and 2024 | Dense historical classified points, anonymous STAC and broad reuse | LAS ZIP versus COPC formats; derive compatible surfaces and check exact acquisition metadata |
| 4 | Vancouver — civilian redevelopment | Same tile 4830E_54540N verified in 2013 and 2018 catalog; matching 2022 renamed tile also verified | Explicit municipal repeat archive and worldwide open license | Tile naming changes in 2022; coordinate/datum and density must be matched |
| 5 | Auckland — development/earthworks | Official regional collections in 2013 and 2024; small shared footprint verified; pixels/cloud extent still need checking | LINZ DSMs CC BY 4.0; older point archive CC BY 3.0 NZ | NZVD2009 versus NZVD2016: transform before subtracting heights |
| 6 | Spain PNOA — Madrid or a civilian quarry | Official Madrid coverage tables document separate 2010, 2016 and 2024 acquisitions | National cycles, public LAZ, prescribed commercial-reuse attribution | Confirm chosen tile in both surveys; major density/classification differences |

**Next pilots:** first run a two-survey Docklands or Zurich building-footprint comparison on a publicly documented redevelopment; next test Rotterdam excavation or industrial expansion with identically derived surfaces; use Auckland only after a validated vertical conversion. Vancouver is a particularly approachable alternative. Choose a location with an already dated permit as a positive control. These are proposed reporting pilots, not findings of misconduct at those places.

## Global inventory

Evidence grades are deliberately separate. **D** = primary documentation checked; **M** = anonymous catalog/metadata response checked; **H** = a bounded point-cloud header checked; **T** = full data/analysis tested (none here). Repeat **R1** = matching tile or small footprint documented by a live official query; **R2** = official overlapping region/coverage history, exact pilot intersection pending; **R0** = only rolling coverage, planned revisit or unverified history. License **L1** = explicit permissive source terms checked; **L2** = dataset-specific/ambiguous terms; **LX** = access or reuse incompatible with this no-account commercial-newsroom pilot. No grade asserts all files work or constitutes legal advice.

| Place / archive | Products relevant to structures | Repeat / evidence / terms | Decision |
|---|---|---|---|
| England EA | LAZ; dated first/last-return DSM and DTM | R1 / M / L1 OGL | First pilot |
| Netherlands AHN | Classified/split LAZ; DSM and DTM | R1 / H / L1 CC0 old, CC BY newer | First pilot; preserve epoch and processing |
| Switzerland | Classified LAS ZIP, newer COPC; surface raster separate | R1 / H / L1 official federal reuse conditions | First pilot |
| Spain PNOA | LAZ; derived terrain/surface products vary | R2 / D / L1 CNIG terms | Strong after tile/date check |
| Italy, Trento | Historical raw LAZ and newer STEM clouds | R1 / H / L2 legacy/new license mismatch; partial correction overlap | Regional pilot; don't extrapolate to all Italy |
| Finland NLS | Open decimated 0.5 points/m² cloud; denser restricted products | R0 / D / L1 open product; LX restricted | Large changes only; history and coverage needed |
| Norway Høydedata | Project clouds and terrain models | R0 / D / L2 per-project | Promising project lookup |
| Sweden Lantmäteriet | Current forest COPC/LAZ; historic NH | R0 / D / L2/LX access permission/history | Defer anonymous pilot |
| Denmark DHM | 2007/2015/current point clouds | R2 / D / LX current API key/account | Real archive, blocked by task constraints |
| France IGN LiDAR HD | Classified LAZ; MNS/MNT/MNH | R0 / D / L1 Licence Ouverte | Strong baseline; national repeat unproved |
| Germany NRW | Current LAS and surface/terrain products | R0 / D / L1 state open terms | Find retained historic tiles first |
| Wales | Historic and 2020–23 DSM/DTM | R2 / D / L1 mapped OGL; tile terms check | Useful raster lead; clouds not verified |
| Scotland | Project LAS/LAZ, DSM/DTM | R0 / D / L2: phase 2 raw NC exception | Choose OGL project; don't treat all raw clouds as open |
| US NOAA/USGS | LAS/LAZ; derived DEM varies | R2 / M / L2 project constraints; federal public-domain guidance | NYC 2013–14→2017 strong conditional pilot |
| US Washington DNR | Point clouds, DSM, DTM | R2 / M / L2 metadata download blocked | Preserve [prior review](../washington-lidar.md); terms unresolved |
| Canada Vancouver | 2013/2018/2022 LAS | R1 / M / L1 city open license | Strong pilot |
| Canada CanElevation | Actual project LAZ/COPC; separate HRDEM rasters | R0 / D / L1 federal open license | Project clouds; repeats not established |
| Brazil São Paulo | 2017 LAZ ground/surface clouds | R0 / D / L2 GPLv3/CC-BY-SA terms ambiguity | Baseline; resolve data terms |
| Colombia Bogotá | Lidar-derived DSM/DTM | R0 / D / LX BY-NC-SA | Commercial redistribution hold |
| Canada Québec | LAZ and terrain | R0 / D / L1 CC BY 4.0 | Find second acquisition |
| New Zealand LINZ | Regional point clouds and DSM/DEM | R1 / M / L1 named collections CC BY | Auckland pair; datum conversion required |
| Australia ELVIS/NSW | Project lidar, DSM/DEM; metadata dependent | R0 / D / L2 dataset terms | Use project provenance; avoid blended national DEM for structures |
| Australia Victoria | Selected elevation/lidar products | R0 / D / LX fees/NC exceptions | Exclude default commercial pilot |
| Japan Shizuoka | Historical point-cloud releases | R0 / D / L1 named prefectural terms | Promising regional pair; footprint/flight detail pending |
| Hong Kong GEO | 2010–11 and 2019–20 airborne clouds | R2 / D+M / L2 special conditions | Archive real; legal review before derivatives/redistribution |
| Uruguay IDE Minas | 2025 classified LAS route; platform unverified | R0 / M / L1 Uruguay open-data terms | One-epoch lead, no verified repeat |
| Mexico INEGI | Lidar-derived terrain/surface models; sensor must be checked | R0 / D / L1 identified products, raw points unresolved | Discovery only |
| South Africa Cape Town | Public contours from successive lidar surveys | R2 / D / L2 raw/DSM access unresolved | No serious repeat recommendation from this review |

See [western Europe](western-europe.md), [other Europe](other-europe.md), [Americas](americas.md), [Asia, Pacific and Africa](asia-pacific.md), and [additional UK notes](uk-additional.md). Those records give exact official access/license links and qualify costs, foreign access and restrictions. A public map is not a license, and a globally viewable endpoint does not guarantee every foreign user can download every product.

## Go / no-go before analysis

Proceed only when both acquisitions cover the same actual analysis polygon, provide the needed returns or product, and have publication-compatible terms. Save dated terms and use required attribution. Confirm actual flight intervals, CRS, vertical datum, units, classifications, nominal density, accuracy, gridding method and gaps. Restrict the question to change larger than the measured uncertainty and spatial resolution.

Stop or narrow the question when only bare earth is available for a building story, when one year is photogrammetry or satellite elevation, when license terms are unclear, when transformation/control residuals approach the purported change, or when a mosaic cannot date the site. Archive searches failing here are not proof that the data never existed.

## Annex: a low-cost, reproducible workflow

1. Define a civilian polygon and a public-record question. Find a dated permit or known construction event to test the method; select nearby stable roofs/ground as controls. Download metadata before points.
2. Intersect the two epoch footprints. Record publisher IDs, original filenames, acquisition intervals, download URLs, license versions and hashes. Catalog modification times, LAS creation dates and API `datetime` fields can describe processing/publication rather than flight time; read the field definition.
3. Preview DSM/DTM with QGIS WMS/COG, or point clouds with QGIS/CloudCompare. Select a tiny area first. PDAL can crop supported COPC by bounds; original LAZ may require an entire tile unless the publisher has a subset service. Range support alone does not make ordinary compressed LAZ randomly crop-able. Never upload restricted points to another service.
4. Put both years in one horizontal and vertical reference using official transformations and grids. Document the transformation path, grid/version and units. Verify residuals on stable features before comparing. Never fit alignment on the excavation itself.
5. For structures derive the same DSM statistic from equivalent eligible classes/returns, at a common conservative grid size; for earthworks derive ground surfaces after inspecting classification. Use identical origin, extent and no-data rules. Reprocessing may create apparent changes even when acquisition is unchanged.
6. Mask water, vegetation, occlusion, edges, sparse cells and moving objects. Map height difference with an uncertainty threshold established from controls and survey specs. Distinguish missing data from unchanged/absent features. A rendering is not a measurement.
7. Report defensible area/height changes with uncertainty. For any volume estimate specify boundary, reference surface, sampling and registration errors; seek survey expertise before interpreting tonnes or production. Check imagery, land/permit documents and alternative explanations. Keep reproducible settings and a small publishable derivative rather than redistributing giant raw archives unnecessarily.

**Uncertainty:** a first approximation for independent height errors is `sqrt(sigma_old² + sigma_new² + sigma_alignment²)`. It does not account fully for correlated errors, systematic datum shifts, surface/vegetation changes or interpolated cells. Empirical stable-control residuals and the official error definitions matter more than an automatic threshold. Point density is not raster resolution and neither alone is accuracy.

**Historical public military-site coverage:** these archives can sometimes contain old public survey footprints that include former military land. A concrete documentary starting point is former RAF Upper Heyford: [Cherwell’s historical plan](https://modgov.cherwell.gov.uk/CeConvert2PDF.aspx?A=1&F=CHAPTER+++2+THE+FORMER+RAF+UPPER+HEYFORD.doc&MID=423&R=0) records military use ending in 1994 and discusses environmental improvement/reuse; the council also publishes a [conservation-plan archive](https://www.cherwell.gov.uk/downloads/download/178/raf-upper-heyford-conservation-plan). Query the England archive against the documented civilian redevelopment boundary and test demolition/earthwork or restoration claims. **No matching lidar pair was checked at Upper Heyford**, so this is a proposed historical land-conversion lead, not a verified scan example or a finding about current operations. No present movements or vulnerability analysis was produced. Validate dates, applicable withholding and reuse terms; public visibility alone supplies none of those answers.

## Annex: checks, cost and publication provenance

[AHN checker](check_ahn_headers.py) uses only Python's standard library, caps catalog responses at 3MB and requires HTTP 206 before reading a 4KB range. [Observed results](evidence/ahn-paired-header-check.json) show both original C_37HN1 tiles have the same horizontal rectangle and valid LAS headers (1.2/1.4), while listed full files are approximately 2.0GB and 9.38GB. Only 8KB of Dutch point-cloud files were read; no points were decoded. Header creation dates are **not** claimed as flight dates. Publisher full-file SHA256 values were recorded, not independently validated. A matched tile rectangle does not establish valid observations throughout it.

[Western Europe checker](check_western_europe.py) and [results](evidence/western-europe-checks-results.json) reproduce the Docklands/Zurich overlap and Swiss 4KB header check. [Auckland checker](check_auckland_repeat.py) and [results](evidence/auckland-repeat-check.json) reproduce the small shared-footprint test. [Trento paired headers](evidence/trento-paired-headers.json) show why matching filenames are insufficient: the newer file is only a narrow correction/completion strip inside the older tile, not a complete independent resurvey.

Regional annexes document other successful catalog checks and failures, including migrated endpoints, blocked routes, unavailable metadata and account/permission requirements. They distinguish retrieval from analysis. No legal or scientific conclusion should rest on an untested download.

**Cost ledger:** paid external calls **0**; purchases **0**; paid services **0**; ChatGPT token usage/cost attribution **unknown, not measured**. Free network traffic and cloud compute were used; labor, storage and bandwidth are not claimed costless. No subscriptions, accounts or outreach were initiated.

This addition is separate from preserved Rabbit exports. Existing SYS/AP/MAP records and RAB-LIDAR-20261014-01 remain unchanged. Only this guide, its reviewed regional annexes/check evidence and the catalog index are intended for publication. Draganfly and unrelated research are outside scope.
