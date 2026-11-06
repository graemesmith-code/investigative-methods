# Cygnet discrepancy review and geometry reconciliation

6 November 2026. This is a source-quality review, not an allegation, a compliance finding, an independent earthquake relocation, or a certified as-built well survey. It supplements the [5 November public-record methods](../../2026-11-05/cygnet-public-portal-verification/README.md). The original reports and previous dataset are preserved without modification. Selected findings and reproducible methods are published here at the researcher's express request; source PDFs, private correspondence, personal invoice details, full operational tables, and private storage links are not published.

## Assessment of the inconsistencies

The observed pattern is more consistent with routine transcription, template reuse, copied passages and inconsistent reporting conventions than with demonstrated concealment. This is a qualitative assessment, not a statistical estimate of intent. Three different wells' stage-8 detail fields repeat exactly the same interval, while their own summary tables and daily shot lists distinguish the wells. A stage-9 summary contains an inverted interval; a wrong-well stage-19 report was inserted into another package; several timestamps, units and totals fail elementary internal checks. These mechanisms can explain errors without assuming intent.

This does not establish that every error is innocent. Inconsistencies that affect injection timing, seismic responses, stage identity, treatment volumes or restart decisions require original logs and an audit trail. These supplied PDFs alone cannot establish a notification chain, a formal regulator restriction, who authorized restart, a regulatory breach or deliberate alteration. Retention of explicit seismic remarks in the reports also argues against treating the mere presence of errors as proof that seismicity was systematically hidden. The record needed to test intent is different from the record needed to correct a numerical field.

## Geometry decisions

A = licence 0516327; B = 0516328; C = 0515889. All depths below are measured depth in metres, with daily perforation lists labelled mKB. They are distances along the borehole, not vertical depth. All PDF page references are physical, 1-based; split files retain their own numbering.

| Well / stage | Conflicting source fields | Best supported interval | Basis and decision |
|---|---|---|---|
| A / 8 | Service summary p3: 5715.4–5771.4. Detail p27: 5749.4–5805.4. | **5715.4–5771.4**, midpoint 5743.4 | A daily p33 lists all eight depths from 5771.4 down to 5715.4 and plug 5775.4. Retain the summary; flag detail. |
| B / 9 | Summary split file1a p3: top 5805.4, bottom 5741.4. Detail p30: 5685.4–5741.4. | **5685.4–5741.4**, midpoint 5713.4 | B daily p26 lists all eight depths and plug 5745.4. Correct summary-derived top by −120 m and naive midpoint by −60 m. Do not merely sort the inverted endpoints. |
| C / 8 | Summary split file2a p3: 5753–5809. Detail p27: 5749.4–5805.4. | **5753–5809**, midpoint 5781 | C daily p30 lists all eight depths and plug 5813. Retain the summary; flag detail. |
| C / 19 | Summary split file2a p3: 5049–5105. Detail p60: 5045.4–5101.4, explicitly identifying B and 53 stages. | **5049–5105**, midpoint 5077 | C daily p23 supports summary and plug 5109. Reject the wrong-well inserted detail for C. |

The repeated 5749.4–5805.4 interval on A8 and C8 is B8's own interval, independently recorded in B daily p29, with plug 5809.4. A copied field or template is a strong explanation, but these PDFs do not prove which software or person introduced it. Selection is supported by enumerated shot depths and plug positions, not merely the regular 64 m stage sequence. These are high-confidence source reconciliations, still short of a certified wireline/perforation record.

## Impact on the prior geometry

The complete prior dataset was reproduced from the original service summaries and drilling surveys before any correction. It contains 156 interval rows represented by three points each, or 468 location rows, interpolated from 978 unique survey stations (A: 325; B: 326; C: 327).

Only **two prior location rows change numerically**: B9 top and midpoint. B9 bottom is unchanged. A8, C8 and C19 already used the better-supported summary values. The previous code calculated an inverted interval's midpoint because it checked stage count/order and survey range, but did not reject top greater than bottom. Successful code tests and reproducibility did not establish that its source values were valid.

B9 midpoint, in the source survey's reported local frame:

| Quantity | Previous | Reconciled | Difference |
|---|---:|---:|---:|
| Measured depth (m) | 5773.4 | 5713.4 | −60.0 |
| North offset (m) | −392.330378 | −389.793004 | +2.537374 |
| East offset (m) | 3541.350735 | 3481.437080 | −59.913655 |
| TVD (m) | 2575.134477 | 2576.858188 | +1.723711 |

The calculated horizontal displacement is **59.967361 m**, mostly west. B9 top shifts **119.953282 m** horizontally. The decimals make the arithmetic checkable; they are not claims of survey accuracy. Linear interpolation of rounded station coordinates can introduce small geometric inconsistencies, so these are not sub-centimetre measurements.

The corrected B9 midpoint is bracketed by MD 5707.25 and 5726.29 on B drilling p39. Their reported TVD/ND/ED values are respectively (2577.01, −389.47, 3475.30) and (2576.54, −390.47, 3494.30) m. Interpolation weight is (5713.4−5707.25)/(5726.29−5707.25). The same common-pad projection as the old dataset gives conditional latitude 52.219005922 and longitude −113.950451865. Unknown wellhead-specific origin, geodetic datum and north reference still prevent treating that as a surveyed absolute position.

All seven previously supplied selected stage coordinates are numerically unchanged: A27, A32, A43, B28, C29, C35 and C40. The additional midpoints B44 and C45 quoted in the prior memo also remain unchanged. This correction therefore does not change the highlighted seismic-stage positions. It does not establish any event-to-well causal link, and it does not cure the original positional or operational-clock uncertainty.

Had the erroneous detail rather than the summary been used, A8's midpoint would move about 33.997 m horizontally on correction, and C8's about 3.600 m. These are **alternative-field sensitivities**, not additional changes in the old dataset.

C1's bottom perforation at MD 6257 remains 10.22 m beyond the last extracted survey station at 6246.78. Its derived position remains unavailable; no extrapolation was introduced. Coil-tubing lengths (mCT) are still not interchangeable with survey/perforation MD or mKB.

## Extent of the cross-check

The audit traversed 11 supplied operational PDFs, 667 physical pages including two repeated split-boundary pages. The invoice was excluded. Every service summary interval and every detected detailed service report was compared; critical discrepant fields and B's affected survey brackets were rendered and inspected visually. This is not a claim that every pixel of every page was inspected.

- 156 summary intervals: A: 52; B: 53; C: 51.
- 137 detailed service reports: A: 45; B: 45; C: 47. The C count includes the wrong-well B19 insert; it is not 47 independently valid C detail reports.
- Four summary/detail mismatch records: A8, B9, C8, and wrong-well C19. All other extracted top/bottom detail fields agree with their summary.
- 139 unique daily perforation envelopes after explicit handling of page continuations, a rerun and a zero-like placeholder: A: 46; B: 46; C: 47. Only B9 disagrees with its original summary envelope.
- Seventeen summary intervals have no corresponding daily perforation envelope in this audit: A28–30, A33–34, A44; B29–34, B45; C41–44. These remain planned/summary geometry and must not be represented as proved perforation or treatment.

Two additional source/parser traps were checked:

1. A19 daily p27 has multiple perforating runs. The first row lists four depths and describes loss of communication; a later row lists three further depths. Together they support the 5011.4–5067.4 envelope. A separate sentence says five guns had fired. MD 5035.4 is not explicitly listed in either shot list. Do not invent the eighth cluster or treat the first run's bounds as the whole stage. A11 and A15 also cross physical page boundaries (pp30–31 and pp28–29 respectively).
2. B53 daily p10 literally appends “0mKB” after seven plausible depths. Preserve that raw entry as an anomaly, but do not use it as a surface-to-stage endpoint. Service summary split file1a p3 and detail split file1b p71 support 2877.4–2925.4, a 48 m envelope and plug 2929.4. The seven nonzero daily depths support the same bounds. It is not justified to force every stage to a 56 m span or to invent another shot.

## Other important discrepancy classes

The prior page-audited review recorded the following distinctions. They are carried forward here as source-quality findings, not new accusations:

- Some B stage38 charts are dated 2023/02/25 while the detailed report gives 23 February 2025. Chart-date headers cannot alone time the operation.
- B daily stage39/40 rows have end times earlier than start times; A March CTU rows also contain inverted endpoints or internal entries outside the enclosing row. Reported daily totals can therefore be inflated.
- A27's 951.51 m³ and 95.51 m³ fields conflict; several rates repeat pressures or differ between L/min and m³/min. These fields should not be silently repaired or treated as real high rates.
- C35 has a 66-tonne narrative/daily figure against 70,000 kg in structured service fields. That conflict remains explicit.
- A43/B44 combined summary volumes reconcile arithmetically as 52.4 + 6 + 35.2 = 93.6 and 53.1 + 6 + 35.2 = 94.3 m³. These appear to aggregate pumpdown, acid and later displacement. Counting the full summary as one day's injection and adding the displacement again would double-count; the contractor's field definition remains unconfirmed.
- C45's 3,570 minutes of recorded third-party delay is 59 h 30 m, while the preceding C40 end to C45 start spans 59 h 54 m. The 24-minute difference means the NPT field cannot be assigned those exact endpoints.
- C's 27 February injection-test narrative is also copied under 25 February alongside “No Activity.” This unresolved date conflict is more consequential than a cosmetic typo.
- C19 contains a wrong-well three-page insertion; later A charts also have conflicting outer headers and inner titles. An alleged C40 inner-title mismatch was not reproduced after enlarged visual inspection and should not be repeated as a verified error.
- Several earlier review citations confused cover pages with summary tables or shifted physical page references. Those are analysis/citation errors, separate from source errors.

The strongest next records for disputed geometry are native wireline/perforation gun logs, plug-setting records, contractor revision history, and a certified directional survey with wellhead coordinates, datum and north-reference metadata. For seismic-response questions, the critical missing evidence is synchronized pump/flow and monitoring logs, the reporting/notification chain and actual regulator correspondence. No outreach was performed as part of this reconciliation.

## Reproduction and validation

The script is deliberately source-layout-specific and offline. It reads the original PDFs and the previously supplied research bundle, emits a raw comparison before adjudication, recovers the documented continuation/rerun cases, and writes a separate annotated revised CSV. It never replaces the originals. Raw values, raw source citations and resolution basis are retained.

Required packages: Python 3 and PyMuPDF. Use a private directory outside the public repository for PDFs, the unpacked prior bundle and all outputs:

```sh
python audit_geometry.py --pdf-dir PRIVATE_PDF_DIRECTORY --prior-dir PRIVATE_UNPACKED_BUNDLE --out PRIVATE_OUTPUT_DIRECTORY
python -m unittest discover -s PRIVATE_UNPACKED_BUNDLE/methods/surveys -v
```

The prior bundle directory must contain methods/surveys/interpolate_pdf_surveys.py; private_source_audit/survey_input_manifest_private.json and stage_locations_private.csv; and deliverables/Cygnet_selected_stage_coordinates.csv. The imported interpolator corresponds to prior commit f6d7a43336be506cc9d44fe56a140c73ef59ddd5. It linearly interpolates reported TVD/ND/ED by MD, not minimum-curvature reconstruction. Its original synthetic tests are exact-point, midpoint and extrapolation refusal. All three passed again.

Executed dataset assertions passed: 156 summaries; 137 details; 139 reviewed envelopes; 978 stations; 468 output rows; exactly two numerical coordinate changes; seven selected coordinates unchanged; C1 unavailable bottom still blank. The script's first raw-parser difference list intentionally includes incomplete A19 and zero-like B53; the later REVIEWED_DAILY results account for them explicitly. A raw parser warning is not by itself a source error.

The checks establish reproduction and stated consistency, not true as-built geometry. A reusable pipeline should additionally fail or quarantine reversed intervals; verify well identity before comparing fields; cross-check shot/plug and summary evidence; preserve contradictions; disallow extrapolation; and distinguish planned from recorded operations. Do not silently repair either the source or the previous dataset.
