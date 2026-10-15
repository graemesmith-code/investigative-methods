# Three next tests — awaiting the editor's selection

**Checked October 15, 2026. None of these tests has been launched.** They are not three verified live feeds. The first is a documented satellite measurement with a historical archive; the others have explicit access/coverage gates. No purchase, account creation or supplier contact is authorized by this shortlist alone.

## 1. Nighttime light from large institutional areas — recommended first

**Question:** do broad campus areas become detectably brighter on pre-operation nights, relative to their own earlier observations and comparable civilian office areas?

**Source and cost:** NASA VIIRS Black Marble. The daily standard product has a global archive from January 2012 and nominal 500 m / 15-arc-second cells. NASA also documents a near-real-time stream, with approximately three-hour processing latency. Data fees are $0; downloading scientific files normally uses a free Earthdata account/token. Actual granule access has not yet been tested in this project.

**Proposed test:** first establish whether usable, quality-screened observations exist before the same Iran and Venezuela events; then compare broad areas with fixed controls and ordinary nights. Use a positive control with a known large lighting change to test whether the measurement is responsive. Use measured radiance and quality flags, not brightness inferred from a colored web-map screenshot.

**Backtest fit:** the product archive spans all three cases, but cloud-free coverage for the specific pre-event windows is unverified. Distinguish standard reprocessed data from what the near-real-time feed actually published. Three-hour processing is after observation, not a new observation every three hours. Check acquisition and release timestamps against the cutoff.

**Main failure risk:** security lights may remain on regardless of staff; clouds, moonlight, snow, viewing angle and surrounding development can dominate a few pixels. An image after a strike cannot be counted as an advance signal. Brightness is not a headcount. Stop if there are too few usable pre-event observations or the measurement cannot detect the positive control.

Sources:
- https://www.earthdata.nasa.gov/data/catalog/laads-vnp46a1-2
- https://www.earthdata.nasa.gov/data/catalog/lancemodis-vnp46a1-nrt-2
- https://www.earthdata.nasa.gov/data/projects/black-marble
- https://landweb.modaps.eosdis.nasa.gov/data/userguide/BlackMarbleUserGuide_Collection2.0_20241203.pdf

## 2. Broad overnight road traffic — best direct movement alternative

**Question:** is there a large abnormal overnight vehicle flow across broad road corridors serving institutional districts, after regional traffic, weekday and closure controls?

**Source and cost:** FHWA publishes free continuous-counter archives with 24 hourly volume columns per day and a station-location file. Virginia's SmarterRoads advertises free accounts and datasets ranging from real-time sensor streams to annual files. This does not establish that any suitable local counter has both a timely feed and the required archive.

**Proposed test:** first locate a small set of appropriate public counters and verify station history, direction, units, clock, missingness and publication time. Then use fixed broad corridor totals and comparison corridors. No number plates, images, individual vehicles or travel histories are needed.

**Backtest fit:** the checked FHWA download page lists data through 2025, so it can support a June 2025 attempt if local counters exist. It does not presently establish coverage for January/February 2026. Those cases require a verified state archive. Stop before analysis if suitable location/time coverage cannot be obtained. Monthly reporting of hourly data does not provide a live newsroom feed.

**Main failure risk:** unrelated traffic overwhelms the institutional component; construction changes routing; nearby sensors may not cover relevant journeys. Public traffic cameras do not solve historical availability: VDOT explicitly says it does not record footage and past footage is unavailable.

Sources:
- https://www.fhwa.dot.gov/policyinformation/tables/tmasdata/
- https://smarterroads.vdot.virginia.gov/
- https://511.vdot.virginia.gov/cameras

## 3. Aggregate phone-presence data — supplier-feasibility test first

**Question:** can a supplier provide broad, pre-aggregated hourly presence totals for large institutional areas, with enough history, low enough cost and short enough delay to test the original idea?

**This is an access/economics test, not a ready-to-run backtest.** Require only aggregate counts or indices: no device IDs, inferred employee lists, origins/destinations or trajectories. Do not bypass sensitive-location exclusions. A rounded population estimate is not a count of independent sampled devices; ask for effective sample size, coverage stability and suppression rules.

**Pass conditions before purchase or analysis:** archive covering all three event windows plus ordinary comparison periods; meaningful hourly observations; documented release latency of at most a few hours; actual coverage of the proposed broad sites; lawful permitted newsroom use; and an acceptable fixed price. A proposed screening cap is US$100 for a small sample, not a vendor quote or authorization to spend. Seek an existing free research/journalism sample first.

**Why this remains uncertain:** Placer offers aggregated exports, but its feed documentation states a two-day default lag, while API documentation states a three-to-five-day processing lag. Daily delivery is not same-day measurement. BestTime offers live relative busyness for some venues but says it does not supply a dedicated historical export. These specific products therefore do not currently clear the same-night-plus-backtest requirement. Their pricing and data descriptions must not be treated as proof that a different supplier can do so cheaply.

**Proposed test:** inspect current supplier documentation and sample contracts/data for those pass conditions. Prepare a precise sample request if necessary; do not purchase or contact a supplier until that action is authorized. If no eligible low-cost feed exists, record a feasibility failure promptly. If one exists, freeze the sample and protocol before running the event test.

**Main failure risk:** high fees, late reporting, sensitive-site exclusions, unstable panel coverage, and hourly-looking modelled forecasts mistaken for historical observations. Population aggregation alone does not guarantee anonymity or adequate statistical power.

Sources:
- https://www.placer.ai/products/api
- https://docs.placer.ai/docs/faqs
- https://docs.placer.ai/reference/faqs-1
- https://docs.placer.ai/docs/premium-export
- https://besttime.app/

## Recommendation

Choose **1** for the strongest currently documented combination of free data, an archive spanning the cases and a near-real-time product. Choose **2** if direct movement matters more and you accept a coverage/access audit first. Choose **3** to resolve whether the original phone-data idea is affordable and timely at all. None is a demonstrated military-warning method, and no test should be judged by these three famous events alone.
