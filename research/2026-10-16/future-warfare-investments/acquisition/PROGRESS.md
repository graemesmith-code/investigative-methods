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
