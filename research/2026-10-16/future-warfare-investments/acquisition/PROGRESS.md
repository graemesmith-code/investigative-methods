# Committed acquisition checkpoint — 16 October 2026, 21:00 UTC

Actual payloads are downloaded, opened and parsed. Larger DoD contract exports are still generating; their counts below are **query counts, not downloaded rows** until validation profiles exist.

| Completed source | Raw size / records | Validated reusable subset |
|---|---:|---|
| Newer SBA bulk CSV with abstracts | 394,911,278 bytes; 219,649 rows | 25,770 FY2019–FY2026 defense/selected DOE award rows; 15 missing UEIs; 43 repeated composite source IDs |
| Older SBA bulk CSV | 367,551,355 bytes; 207,731 rows | Superseded comparison snapshot; do not combine with newer file |
| USAspending DARPA contracts + subawards ZIP | 2,417,982 bytes | 12,057 prime actions, 4,869 subaward rows; prime dates 2018-10-01–2026-07-16 |
| USAspending selected DoD research grants + subawards ZIP | 15,958,687 bytes | 88,273 prime actions, 14,143 subaward rows; prime dates 2018-10-01–2026-09-25 |
| Grants.gov full XML ZIP | 78,292,394 bytes; 83,576 synopsis/forecast records | 3,283 security-agency/date-bounded opportunity records; funding intent only |
| OMB PB2025/PB2027 budget authority and outlays | Four complete XLSX files | 38,600 FY2019–FY2026 security-account/year/measure/vintage cells, plus complete source tables |
| DARPA PB2025 justification book | 4,253,354 bytes; 252 pages | Full text pages and 256 program-title funding rows; 47 rows lack parsed project IDs |
| GovInfo FY2026 DoD appendix | 2,127,622 bytes; 114 pages | Full page text; no claim of project-to-award crosswalk |
| Microelectronics Commons | Six complete technology-area PDFs | 57 project headers, including one amount with unspecified scale; full page evidence |
| APFIT March 2023 implementation report | 603,542 bytes; 11 pages | Ten FY2022 projects, selected funding and production/delivery narratives |
| NCSES Federal Funds tables | 1,167,352-byte ZIP | All 99 workbooks/sheets parsed, 8,355 positional rows including headers/footnotes |
| FFRDC FY2025 microdata | 29,809-byte ZIP | 862 expenditure rows; source/agency/type breakdowns overlap |
| PSC April 2025 workbook | 462,762 bytes | 6,109 rows in main sheet, including headers, plus 23 category-manager rows |

Further acquisition: complete FY2019–FY2025 DOE LDRD annual financial reports and the full Sandia FY2025 narrative report; validate document text/scan status and financial units. No paid model calls or Exa calls; later pipeline interfaces are designs only.

Pending USAspending exports: a ten-term DoD capability slice (324,990 prime actions reported by count endpoint) and the broader DoD R&D PSC category A slice (342,900 prime actions reported by count endpoint). These overlap DARPA and each other. No summed investment total is calculated.

Access limits: R-1/Army/Navy direct budget routes returned errors; official DARPA/GovInfo alternatives succeeded. SBA API returned 403, published bulk CSV succeeded. SAM API probes returned 404; documentation requires an authorized key. Workspace persistence remains unconfirmed; a Library archive is planned, not yet saved at this checkpoint.

## 21:35 UTC checkpoint

The downloaded payloads now total **1,045,161,207 bytes**; normalized files total **531,589,349 bytes**, including intentionally overlapping/source-preserving views. **223 checks pass**, with **zero integrity errors and three explicit keyword-family count/export coverage warnings**. Current parsed spending extracts contain **474,975 unique transaction keys** after exact-key union; this is a count of actions, not investments or an additive monetary estimate.

The full keyword ZIP is **47,414,894 bytes**, containing **305,768 prime actions** and **31,308 subaward rows**. Its count endpoint reports 324,990 prime actions. Smaller FY2019 and FY2026 exports return precisely the same transaction-key sets as those years in the broad export, while retaining count discrepancies (31,105 vs 24,383; 36,069 vs 35,822). The cause remains unestablished; the files are usable evidence with a qualified coverage claim.

R&D single-year diagnostics have been downloaded and parsed: FY2019 **44,337 prime actions + 19,937 subaward rows**; FY2026 **33,089 prime actions + 3,090 subaward rows**. Prime counts match the independent count endpoint. The broader FY2019–FY2026 R&D job has reported 342,900 prime actions, matching its count response, but its complete ZIP is still generating. It is not yet counted as downloaded.

All seven DOE LDRD reports are parsed, with two scanned Table1s manually transcribed against rendered source pages. The seven-year financial table has **123 rows including seven annual totals**; annual project counts reconcile. The full selected report corpus supplies **701 physical PDF pages**, with OCR flagged. Source/monetary dictionaries, semantic audits, exact duplicate views, candidate identifier joins and the deterministic pipeline dry run are now available. Large-data Library archival remains pending completion of the main R&D export.
