# Verified operative rules and limits

Primary PDFs and appendix maps are saved in `sources/`; retrieval hashes are in `sources/manifest.jsonl`. These summaries preserve conditions and are not legal conclusions.

| Order | Effective window relevant to this experiment | Formation and mapped scope | Trigger and response |
|---|---|---|---|
| SO2 | 2015-02-19 through 2024-11-18 | Duvernay zone, Appendix A; affected well surface or bottom hole in mapped zone | During HF, available/recorded event ML ≥2 within 5 km: immediate report and response plan. ML ≥4 within 5 km: immediate report, cease HF, safe state. Written AER consent and acceptable modified plan before restart. |
| SO2A | From 2024-11-19, although made 2024-11-06 | Appendix A; Duvernay through basement, affected well surface or bottom hole | Same inclusive 2/4 ML thresholds and 5 km conditions. Real-time submission and public passive seismic sharing within one year. |
| SO6 | From 2019-05-27 | Zone 1 = surface to top of Duvernay; Zone 2 = Duvernay. HF prohibited in Zone 1/Appendix A and Zone 2/Appendix B. Traffic-light provisions in Zone 1/Appendix C annulus (B minus A). | Yellow ≥1 ML within 5 km during HF, report and mitigate. Clause 5(f): ≥2.5 ML requires immediate suspension and safe state. That red clause does **not** explicitly repeat the 5 km/during-HF wording; our proximity/time screen is bounded, not a replacement legal interpretation. Written consent and acceptable modified plan before restart. |
| SO7 | From 2019-12-09 | Zone 1 = surface to top of Duvernay; Zone 2 = Duvernay through basement. Zone 2 HF prohibited in Appendix A. Traffic lights apply to Zone 1 in A and Zone 2 in B excluding A. | Yellow ≥1 ML within 5 km during HF, report and mitigate. Clause 4(f): ≥3 ML, immediate suspension, safe state and contact AER. It does **not** explicitly repeat 5 km/during-HF. Written consent and acceptable modified plan before restart. |

SO2 predecessor was independently downloaded at the standard official URL; Bulletin 2024-29 confirms amendment effective November 19 and extension below Duvernay. SO7 is not backdated to Bulletin 2019-07's May recommendation. Data before 2020 are not discovery cases.

## Boundaries

The official `AER_Order_System_SHP.zip` includes `Subsurface_Orders` polygons in NAD83 geographic degrees. Its rows are labelled `2`, `6.1`, `6.2`, `7.1`, `7.2`; output GeoJSON retains original properties. Maps were visually inspected from the rule PDFs. The GIS has old labels (including superseded 1B/3A/4/5); do not read it as a versioned current legal register. SO2/SO2A appendix outlines are compared visually; pre/post geography continuity remains a GIS-version limitation. SO6 Appendix C is the outer 6.2 polygon minus inner 6.1; SO7 exclusion is 7.1 inside 7.2. The GIS `Strat_Unit=7280` on multiple areas does NOT override the different operative formations. No town buffers are used as legal boundaries.

The broad scan includes surface or bottom-hole membership, then separately records subarea membership. It retains up to 5.5 km pairs to expose sensitivity around the 5 km screen; distances are ellipsoidal GRS80 horizontal kilometres, not hypocentral distances. Neither surface nor bottom-hole position is assumed to be the definitive legal distance reference for all clauses. Stimulated stage trajectories and event uncertainty are missing. The 0.1-degree event-area buffer in the supplementary output is explicitly a coarse screen, never legal geography.

## Magnitude, timing and versions

AGS columns distinguish ML (local), MLy (Yenier-corrected local), industry M, and Mw. MLy is a local-magnitude estimate, not moment magnitude; its separately labelled sensitivity analysis is scientifically useful. INF164 (August 2026) recommends Yenier magnitude estimation, but cannot establish the historical magnitude available at a 2025 operation. We never substitute Mw or undifferentiated M into an ML threshold. NRCan independently exposes typed ML and MLy and is joined separately. Differences between catalogue versions are retained rather than selecting the most adverse magnitude.

Event timestamps are UTC; date-only reporting windows are compared in America/Edmonton including daylight saving. End dates are inclusive *possible-overlap days*, not midnight stop times or continuous pumping. Licence target/terminating formation is a proxy for geological applicability, not proof of the actual stimulated interval. Current licensee names, facility operators, and historical pumping operators remain distinct identities.

## Disposal: separate rule family, not applied to HF records

Bulletin 2024-28 introduced Directive 065 induced-seismicity provisions in November 2024. Saved Directive 065 is the March 31, 2026 revision, section 4.1.8, printed pages 4-24 to 4-27. It addresses disposal across Directive 051 fluid classes. An approval holder with an MMR plan follows its own inclusive low/high thresholds within 10 km (or larger AER-specified radius); high-level response includes immediate reporting, implementing the plan, returning the well safe, and written consent before resuming affected operations. Thresholds and duties require the dated approval/plan and applicable rule edition. The historical November 2024 text was not verified, so current clauses are not backcast over 2020–2025.

The active disposal inventory is dated September 15, 2026 and is not a historic exposure inventory. Petrinex INJ rows include injection activities beyond wastewater disposal; scheme subtype/product must be checked. FRAC means *fractionation* in Petrinex, not hydraulic fracturing. Monthly Hours are accumulated hours, not a timestamp series. No disposal-compliance claim is made without the appropriate approval, MMR thresholds and time-resolved operation.
