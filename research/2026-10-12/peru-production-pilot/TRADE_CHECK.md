# Company-level export/import feasibility check

**Result:** a free Peru company-level customs route works. No true destination-country company/shipment counterpart was established from the free sources tested. Mirror-trade comparison is parked. No aggregated national difference is used as company evidence.

## Peru: live successful query

The ministry's 2024 company directory identifies La Arena S.A. as RUC **20205467603** and Shahuindo S.A.C. as **20505792042**. Do not confuse the latter with Shahuindo Exploraciones. Personal contact details from the directory are not reproduced here.

Form: <https://ww3.sunat.gob.pe/servlet/HRGDecExp?codr=50&opcion=detalleexp>

POST endpoint: <https://ww3.sunat.gob.pe/servlet/SgDetalleEk?codr=50>

```json
{"orden":"export","FecInicial":"01/12/2023","FecFinal":"31/12/2023","codigo":"20205467603","codr":"50"}
```

The HTTP 200 response returned three declarations dated 22 December 2023 under HS 7108120000. Transcribed response fields:

| Declaration | Destination | Net kg | FOB value shown |
|---|---|---:|---:|
| 235-2023-077945 | United Kingdom | 241.17 | 13,870,490.70 |
| 235-2023-077946 | Canada | 131.51 | 92,769.05 |
| 235-2023-077947 | United Kingdom | 4.55 | 259,623.55 |

Descriptions identify doré bars and display gold/silver percentages (53.58% Au, 31.28% Ag). The repeated assay description, weight and value allocation have not been reconciled. Do **not** multiply these weights by the displayed percentages and label the result fine-gold production. No corresponding named foreign consignee or linked import declaration was present in the retrieved response.

A separate exporter-summary route also worked after correcting the document type to `tipodoc=4` (RUC): POST `https://ww3.sunat.gob.pe/servlet/SgDetExportacion?codr=50`, with `fechselec=embar`, December dates, `codexportacion=20205467603`, `orden=fob`, `Select=paisdesti`, `Codigo=''`, `criterio=exportador`, `codr=50`. It returned a Canada summary with three occurrences, 584.05 net kg and FOB 22,111,776.573. **Do not compare this directly with the declaration-date table:** the selected date basis is shipment date rather than declaration numbering date. The initial `tipodoc=6` probe gave no registration match; that was a query error, not evidence of no exports.

## Destination countries: availability tested

| Source | Actual access result | Why it does not make a matched pair |
|---|---|---|
| Canada, 2023 major importers by HS6 and country | Downloaded 23.27 MB XLSX, HTTP 200; approximately 517,000 data rows | Company, product and origin-country fields; no shipment quantities, values, Peru exporter counterpart or declaration identifier. |
| UK Trade Info, traders for 710812 | Page downloaded, HTTP 200 | Trader/product/month information, not matching shipment-level metal quantities and counterparty. |
| China customs public statistics index/query | Both tested URLs returned HTTP 502 in this environment | No usable company-level paired record obtained. Public indexed statistics descriptions did not establish named-company shipment matching. This does not prove such data are unavailable everywhere. |

Canada: <https://ised-isde.canada.ca/site/ised/sites/default/files/documents/cid-bdic-majorimportersbyhs6bycountry2023_0.xlsx>

UK: <https://www.uktradeinfo.com/search/traders/?commodities=710812>

China tested: <https://stats.customs.gov.cn/indexEn> and <https://stats.customs.gov.cn/queryDataForEN/queryDataByWhereEn>.

Before revisiting mirror trade, require named exporter/importer linkage, shipment/declaration identity, compatible dates, same goods and assay basis, and treatment of re-exports, refining and valuation. A true shipment match still does not establish production identity: inventory movements and bought-in metal can separate mine output from exports. This run did not buy data, contact anyone or infer a company mismatch from country aggregates.
