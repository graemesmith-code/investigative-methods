# Rabbit review — 23 November 2026

Three proposals await a decision: one new source and two corrections. Recommendations: **ACCEPT 1, MERGE 2, HOLD 0, DECLINE 0**. No new access-route proposals are pending. These are recommendations only; no Rabbit proposal, catalog record or enablement setting was changed.

The useful addition is a source showing how free carbon allowances compare with reported emissions across European industries. The two Australian corrections have already been implemented in the catalog, although their proposals still say pending. The next job there is to reconcile the queue with the work already done.

## New source — ACCEPT for catalog inclusion

**Track which European industries receive free carbon permits**
Proposal: PROP-9d1dbeb7-9e4b-4bae-9910-9a8aaf9a58d5.

Official European Environment Agency documentation supports a distinct collection of emissions, free allowances and surrendered units aggregated by country, activity and year. Its September 2026 release advertises 2005–2025 coverage and CSV/TXT/SQL files; metadata states public access and Creative Commons Attribution 4.0 terms. This complements the Industrial Emissions Portal (SYS-0219; AP-0220, AP-0407), which concerns facility releases and transfers. No matching emissions-trading collection was found in the reviewed source, access-method and candidate searches.

Remaining limits: documentation was checked, not data rows or the complete archive. The submitter's reported ZIP-signature test was not independently reproduced. No working data API or operator-level join is certified. The viewer page still labels its temporal coverage 2005–2024, whereas the release metadata specifies 2005–2025. Coverage extends beyond EU members; distinguish the release from the viewer and use an appropriate geographic label. Changing system scope affects comparisons. Exceeding free allocation alone is not evidence of a breach.

Next human action: accept a documentation-backed listing with those limits; label bulk access as advertised rather than newly verified, preserve the earlier probe only as an attributed submission claim, and check a small sample before building an automated collector.

Evidence:
- [Release and advertised downloads](https://www.eea.europa.eu/en/datahub/datahubitem-view/98f04097-26de-4fca-86c4-63834818c0c0/download)
- [Dated metadata and stated licence](https://sdi.eea.europa.eu/catalogue/datahub/api/records/9eee3fc9-3060-4e3f-bc8d-e22e7c3f6bda?language=eng)
- [Viewer scope and field descriptions](https://www.eea.europa.eu/en/analysis/maps-and-charts/emissions-trading-viewer-1-dashboards)
- [Commission reporting and verification explanation](https://climate.ec.europa.eu/areas-action/carbon-markets/eu-emissions-trading-system-eu-ets/monitoring-reporting-and-verification_en)

## Corrections — MERGE with the existing correction release

**New South Wales property sales**
Proposal: PROP-b902ebaa-76e1-490c-9473-02496014f6a7.
Records: SYS-1416, AP-2368, MAP-01573, MAP-01574.

The live records already show Australia — New South Wales and JUR-AU-NSW through release nsw-jurisdictions-20261120. The original United Kingdom import remains preserved under baseline; historical PARTIAL verification is unchanged. Official NSW documentation confirms the jurisdiction and describes bulk sales since 1990. It states non-commercial reuse restrictions; that is not a legal clearance for any particular use. No sales payload was downloaded.

Next human action: reconcile this pending proposal with the existing release and record it as already incorporated, without applying the same field change again. Remaining uncertainty is queue reconciliation, not jurisdiction or a demonstrated need for another source.

Evidence: [NSW property-sales documentation](https://www.nsw.gov.au/housing-and-construction/land-values-nsw/how-to-find-property-sales-information).

**New South Wales custody statistics**
Proposal: PROP-b3c8c34f-d8f4-4d9a-8e60-d11b2db028ba.
Records: SYS-1299, AP-2247, MAP-01434.

The same correction release already assigns Australia — New South Wales and JUR-AU-NSW while preserving the baseline and PARTIAL status. The publisher explicitly identifies all of NSW as its geographic coverage and describes monthly custody population, reception and discharge data. Workbook contents were not tested.

Next human action: reconcile the proposal with the existing release rather than repeating the correction. No change in access verification is warranted.

Evidence: [NSW custody dataset documentation](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets/custody-data.html).

## Technical annex

The installed Rabbit connection returned can_review=true. A page requested with limit=50, offset=0 contained all 44 visible proposals and next_offset=null: three pending, zero needs_info. The other 41 have decisions. Automatic first checks suggested considering acceptance for all three, with no duplicate matches; custody included a source-is-evidence warning. These checks explicitly did not fetch contents. Current record inspection revealed both corrections already applied, which the automatic name/URL check had not identified.

Searches covered sources, access methods and imported candidates, using emissions, trading, allowances, carbon, Union Registry and NSW where relevant. All returned complete result pages. Exact record reads inspected source-to-access and coverage relationships. A shared publisher was not treated as proof of duplication.

Primary pages were retrieved on 23 November 2026. No large datasets were fetched, access purchased, or proposal actions performed. No source usage history or private investigation notes are included in this report.
