Research snapshot: 12 October 2026.

Ten concrete mining-project pairings have accessible evidence on both sides: a Western company filing and a company-attributed statement in a host-country reporting system. All ten pairs were downloaded, opened and matched to the named company or project. The wider access log recorded 88 direct requests, 85 HTTP 200 responses and three failed routes. These are investigative starting points, not ten established contradictions.

Begin with Southern Copper’s Peruvian molybdenum production, Kinross’s Brazilian dam attributes and Endeavour’s Ity royalty payments. They provide identifiable records and consistent specimens for testing extraction. B2Gold’s Fekola dividends provide the strongest numerical follow-up, but their gross-versus-net and shareholder-entitlement definitions remain unresolved.

The decisive Rabbit rule is conditional: IF two authenticated company statements concern the same entity, fact, time, scope and measurement convention, AND their permissible values cannot overlap, THEN the statements cannot both be correct. Rabbit need not choose the correct statement. It must establish comparability first.

Brazil and Peru provide the clearest direct-regulator examples. The other eight use company returns to national, state-led Extractive Industries Transparency Initiative processes, often compiled by independent administrators. They expose company assertions to national reporting systems, but their precise submission obligations and legal consequences require country-specific checking.

## The ten pairings

| Rank | Project and host country | First fact to compare | Tested host evidence |
| --- | --- | --- | --- |
| 1 | Kinross Paracatu, Brazil | Dam construction method and liners | ANM operator CSV |
| 2 | Southern Copper Toquepala and Cuajone, Peru | Annual fine molybdenum production | MINEM XLSX |
| 3 | Endeavour Ity complex, Côte d’Ivoire | Royalties and state-related dividends | EITI company-return XLSX |
| 4 | Endeavour Sabodala-Massawa, Senegal | Royalties and state dividends | EITI company-return XLSX |
| 5 | B2Gold Fekola, Mali | Royalties and dividends | EITI company-return XLSX |
| 6 | Rio Tinto QMM, Madagascar | Mining royalty and local royalty share | EITI company-return PDF |
| 7 | Barrick and AngloGold Ashanti Kibali, DRC | Dated ownership interests | EITI ownership XLSX |
| 8 | IAMGOLD Essakane, Burkina Faso | Dated equity ownership | Company form embedded inside EITI XLSX |
| 9 | Barrick Lumwana, Zambia | Mineral royalty and income tax paid | EITI company-column PDF |
| 10 | Galiano Asanko, Ghana | Mineral royalties | EITI company-column PDF |

## Free access routes that worked

**United States.** The SEC submissions API returned a real company response, and the quarterly bulk index downloaded in full. Use the index to locate 10-K, 40-F, AIF and technical-report exhibits; obtain facts from the original exhibits. Companyfacts does not replace narrative mine tables. The tested first-quarter 2024 index was 4.49 MB and contained 370,321 filing entries. Use a descriptive User-Agent including contact information and a paced downloader.

- [SEC submissions API sample for Freeport-McMoRan](https://data.sec.gov/submissions/CIK0000831259.json)

- [SEC submissions API sample for Rio Tinto](https://data.sec.gov/submissions/CIK0000863064.json)

- [SEC bulk filing index for Q1 2024](https://www.sec.gov/Archives/edgar/full-index/2024/QTR1/master.gz)

**Canada.** Statistics Canada’s full ESTMA CSV downloaded: 53,258,265 bytes and 114,594 records. The observed reporting-year labels span 2021–2026; this is not a completeness claim for every company. Preserve the actual period start and end fields. Its monetary data are converted to CAD, and parent and subsidiary rows can duplicate the same payments. Follow WEB_LINK to the original ESTMA return before comparing amounts.

- [Canadian ESTMA bulk CSV](https://www150.statcan.gc.ca/n1/pub/71-607-x/2022008/STC_DF_ESTMA-eng.csv)

**United Kingdom.** The unauthenticated Companies House extractives API worked. Its all-company 2024 endpoint returned 52 reports. Rio Tinto’s company endpoint returned reporting years 2015–2025 and retained multiple historical versions. The direct 2023 report includes QMM’s project royalty. Inspect reportEndDate, amendments and versions rather than assuming a URL year settles the reporting period.

- [All-company 2024 extractives JSON](https://extractives.companieshouse.gov.uk/api/year/2024/json)

- [Rio Tinto all years and versions](https://extractives.companieshouse.gov.uk/api/company/00719885/json)

- [Rio Tinto 2023 JSON](https://extractives.companieshouse.gov.uk/api/company/00719885/year/2023/json)

- [API endpoint documentation](https://extractives.companieshouse.gov.uk/developer/endpoints)

**Host countries.** Prefer the national annexes linked in the profiles. Brazil offers a complete operator-level dam CSV; Peru offers company-production Excel; Côte d’Ivoire, Senegal, Mali, DRC and Burkina Faso offer downloadable Excel annexes. Madagascar, Zambia and Ghana have downloadable PDFs containing company declarations. These are bulk document downloads, not necessarily query APIs.

The EITI API returned country metadata and revenue examples, but a field labelled “company” can mean government revenue disaggregated by company. The inspected DRC summary template explicitly calls for government values. Such records cannot automatically serve as the company’s second statement.

## 1 Kinross Paracatu in Brazil

**First comparison:** construction method, liner status and stored material at individual tailings facilities. A surviving contradiction would concern tailings engineering, downstream communities, regulatory oversight and investor disclosure.

**Western statement:** [SEC-filed Kinross technical report](https://www.sec.gov/Archives/edgar/data/701818/000110465926035270/tm269365d1_ex99-1.htm), effective 31 December 2025 and dated 26 March 2026. Downloaded HTML: 2,552,896 bytes. Section 18.4, printed pages 158–159, describes Specific Tailings Tank XII as having downstream raises and a geomembrane liner.

**Host statement:** [ANM SIGBM complete dam CSV](https://dadosabertos.anm.gov.br/SIGBM/Barragens.csv). Downloaded CSV: 3,384,198 bytes, 906 dam rows, six belonging to the selected Kinross operator. It uses CP1252 encoding and a comma delimiter. Match Kinross Brasil Mineração S/A by CNPJ **20346524000146**. Dam IDs include Tank XII **8438**, Eustaquio **8431** and Santo Antonio **8433**. For Tank XII, the construction-method field is “Alteamento a jusante” and the liner field is “Sim”. These agree with the SEC specimen.

**If/then:** IF the declarations describe the same dam, construction stage and effective time, AND assert mutually exclusive construction methods or liner states, THEN they cannot both be correct.

**Immediate work:** extract the three named dams, then all six Kinross structures; approve a Portuguese-English construction dictionary; retain dated snapshots. Match historical design attributes first and confirm no intervening modification. The ANM download is current while the SEC report is historical. Modified centreline is a subtype of centreline, not an automatic contradiction. Current height and maximum design height are different facts. A construction label alone is not a safety verdict.

**Readiness:** both sources and the operator/dam match verified; historical-stage alignment remains necessary before automated flags.

## 2 Southern Copper in Peru

**First comparison:** annual fine molybdenum production from Toquepala plus Cuajone, calendar 2024. This is a strong production pilot with consequences for resource reporting and, after checking the applicable metal definitions, the royalty base.

**Western statement:** [Southern Copper 2024 SEC 10-K](https://www.sec.gov/Archives/edgar/data/1001838/000155837025002017/scco-20241231x10k.htm), downloaded HTML 10.32 MB. Printed page 37 reports Toquepala **19,771** and Cuajone **9,740**, each in **thousand pounds** of molybdenum.

**Host statement:** [MINEM December 2024 bulletin annexes XLSX](https://cdn.www.gob.pe/uploads/document/file/7632703/6471629-bem-diciembre-2024-excel-de-anexos.xlsx?v=1739544984), downloaded and opened, approximately 0.34 MB. In sheet **2. PRODUCCIÓN EMPRESAS**, row 72 identifies Southern Peru Copper Corporation, Sucursal Peru. Cell **F72 = 13,386.3420761 fine metric tonnes**. MINEM’s [ESTAMIN description](https://mineria.minem.gob.pe/obligaciones_mineras/estamin/) establishes the mandatory monthly reporting route.

The host row aggregates the company’s Peruvian operations, so sum both mines on the SEC side. **29,511,000 lb = 13,385.96443107 tonnes**. The combined rounding interval for two independently rounded thousand-pound rows is **±0.45359237 tonnes**. The MINEM value lies inside it. This is a consistent control, not an apparent discrepancy to publish.

**If/then:** IF both values are final annual fine-metal output for the same two mines at 100% scope, AND their converted precision intervals do not overlap after revisions and measurement conventions are aligned, THEN the production statements conflict.

**Immediate work:** implement molybdenum first, using 2023–2024 data already present in the ministry table and corresponding SEC history. Extend to copper only after documenting its reporting basis. Separate output from sales, concentrate from contained fine metal, and mine output from smelted or refined metal. The 10-K cash-cost denominator is separately defined net of metallurgical losses and must not substitute for the production field.

**Readiness:** both sources and a numerical control verified; production-definition and revision checks remain mandatory.

## 3 Endeavour Ity complex in Côte d’Ivoire

**First comparison:** 2024 royalties, followed by state-related dividends. The Western return reports approximately **USD 265.6 million** in total Ity project payments, making an irreconcilable material claim consequential for public revenue.

**Western statement:** [Endeavour 2024 Canadian ESTMA return](https://edv-14806-s3.s3.eu-west-2.amazonaws.com/files/4717/4886/2253/Endeavour_Mining_ESTMA_2024.pdf), downloaded PDF approximately 0.82 MB. Ity royalties are **USD 45,145,203**.

**Host statements:** [2024 national EITI report](https://eiti.org/document/26393), 12.31 MB, and [annexes XLSX](https://eiti.org/document/26394), 5.04 MB. Match the Ity complex to Société des Mines d’Ity (SMI), Société des Mines de Daapleu (SMD), and Société des Mines de Floleu (SMF). SMI’s tax identifier is **8500064P**. Sheets **34.1, 34.5 and 34.8**, company-final **column G**, rows **27 and 42**, contain the 85% and 15% royalty components. The six cells sum to **XOF 27,368,514,903**.

Using the Western report’s disclosed payment-date FX range, **595.72–631.40 XOF per USD**, that sum corresponds to **USD 43.346–45.942 million**. The Western royalty lies inside the interval.

**If/then:** IF the approved legal-entity set and complete royalty basket cover the same 2024 payments, AND the Western amount lies outside the host amount’s valid FX-and-rounding interval, THEN the payment declarations conflict.

**Immediate work:** approve the SMI/SMD/SMF-to-complex mapping and use the six royalty cells as the first control. Treat state dividends and SODEMI dividends separately before aggregation; establish gross/net withholding treatment. Do not compare SMI alone with the entire Ity complex. Sheet 45.1 can contain government-origin records such as FD_DGI despite a company-related title.

**Readiness:** downloads and company-column attribution verified; project-basket approval is the main activation requirement.

## 4 Endeavour Sabodala Massawa in Senegal

**First comparison:** 2024 royalties and cash dividends to the state. The Western project reports approximately **USD 207.6 million** in total payments.

**Western statement:** [Endeavour 2024 ESTMA return](https://edv-14806-s3.s3.eu-west-2.amazonaws.com/files/4717/4886/2253/Endeavour_Mining_ESTMA_2024.pdf). The project label is Sabodala Mining Company SARL. Royalties are **USD 21,399,746** and dividends **USD 14,538,193**.

**Host statements:** [Senegal 2024 EITI report](https://eiti.org/document/25525), downloaded PDF 13.58 MB, and [Excel annexes](https://eiti.org/document/25614), downloaded XLSX 18.45 MB. Sheet **11**, cell **I33**, gives Sabodala Gold Operations company-final royalties of **XOF 12,982,245,458**; **I38** gives state dividends of **XOF 8,550,085,532**. Use column **I** for the company, not **L** for government.

The royalty converts to approximately **USD 20.561–21.793 million** across the disclosed FX range, containing the Western amount. Sabodala Gold Operations (SGO) and Sabodala Mining Company (SMC) are different legal entities, so their project relationship must be approved before asserting comparability.

**If/then:** IF the SGO/SMC project bridge is established and both returns describe the same recipient, payment category and cash year, AND the permissible monetary intervals are disjoint, THEN the declarations conflict.

**Immediate work:** preserve the original, adjusted and final company columns G/H/I and government columns J/K/L. Activate royalties first; check dividend gross/net treatment separately. The initial government royalty figure of approximately XOF 16.602 billion was adjusted in the domestic reconciliation. That known reconciliation is not a new Rabbit discovery.

**Readiness:** both files and precise company cells verified; legal-entity/project mapping remains necessary.

## 5 B2Gold Fekola in Mali

**First comparison:** 2023 dividends and royalties, retaining amendments. This is the strongest numerical follow-up in the ten, but it is not yet a demonstrated contradiction.

**Western statement:** [B2Gold amended 2023 ESTMA return, version 2](https://s204.q4cdn.com/324791784/files/doc_downloads/estma/2023-ESTMA-B2Gold-Report-Amended.pdf), downloaded PDF 505,006 bytes. The Fekola project reports royalties **USD 75.69 million**, dividends **USD 59.06 million**, and total payments **USD 336.31 million**.

**Host statements:** [Mali 2023 national EITI report](https://eiti.org/document/23795), 3.75 MB, and [2023 final annexes XLSX](https://itie.ml/wp-content/uploads/2024/06/Annexes-ITIE-2023-_-Version-Definitive.xlsx), 758,969 bytes. Match Fekola SA, NIF **087800848K**, not the separate Fekola Regional exploration/development project. Sheet **Annexe 10 - (2)** uses **column I** for company declarations after adjustments. **I6** is taxe ad valorem, **XOF 22,844,482,528**; **I13** is ISCP, **XOF 22,873,818,742**; **I7** is dividends, **XOF 32,135,608,890**.

The dividend converts to **USD 51.211–55.071 million** across the Western report’s disclosed CFA-to-USD rate bounds, **0.0015936–0.0017137**. That interval is below USD 59.06 million. The arithmetic does not overlap, but gross/net withholding, free-carried versus ordinary equity entitlement, and the precise cash scope could explain the difference.

**If/then:** IF the same dividend basket is asserted for 2023 with identical shareholder entitlement and gross/net treatment, AND even the valid full FX-and-rounding interval cannot reconcile it, THEN at least one underlying amount is incorrect.

**Immediate work:** resolve those dividend definitions using the already retrieved documents and retain the amended Western version and its amendment note. Do not compare total ESTMA royalties with only the ad-valorem line; establish whether ISCP belongs in that royalty basket. The 2024 host annex was also downloaded, but a matching Western 2024 return was not verified for this candidate.

**Readiness:** both declarations and exact cells verified. A bounded numerical lead exists; semantic approval is still required before a contradiction verdict.

## 6 Rio Tinto QMM in Madagascar

**First comparison:** 2023 royalties including the local royalty share, linking public revenue from a coastal mineral-sands project to a UK filing.

**Western statement:** [Rio Tinto 2023 Companies House JSON](https://extractives.companieshouse.gov.uk/api/company/00719885/year/2023/json), downloaded approximately 32 KB, corroborated by an [FCA-hosted filing](https://data.fca.org.uk/artefacts/NSM/RNS/5196185.html), 224,119 bytes. In projectPayments/projectPayment, project **MDG01** reports royalties **USD 3,527,727** and taxes **USD 950,386**.

**Host statements:** [Madagascar 2023 report](https://eiti.org/document/25571), downloaded PDF 9.74 MB, and [2023 annexes PDF](https://eitimadagascar.mg/wp-content/uploads/2025/12/Annexes-Rapport-2023.pdf), 56.37 MB. The annex identifies QIT Madagascar Minerals by tax ID **4000164665** and RCS **1998B00480** on PDF page 15. Main-report PDF page **264**, table **109**, attributes figures to companies’ reporting templates: QMM mining royalty **MGA 4,747,768,340.47** plus “ristourne minière” **MGA 11,078,126,125.81**, the local royalty share for the Fort-Dauphin treasury.

**If/then:** IF these two Malagasy components exhaust MDG01’s declared royalty basket, AND legitimate payment-date currency conversion, timing and refund treatment cannot reconcile their sum with the UK amount, THEN the declarations conflict.

**Immediate work:** establish the royalty basket and defensible payment-date FX bounds, then expand across years through the UK company endpoint. Translate “ristourne minière” in context as a local royalty share, not automatically as a refund. Page 259’s theoretical government allocation is not the company statement. Page 214’s project commitments include conditional wording; do not recast them as paid cash. One annual average FX rate cannot prove a contradiction.

**Readiness:** government JSON API and host company statement verified; royalty-basket and FX validation remain open.

## 7 Barrick and AngloGold Ashanti Kibali in DRC

**First comparison:** ownership percentages, shareholder identities and effective dates. This avoids foreign-exchange ambiguity and can affect profit entitlement, state participation and attribution of responsibility.

**Western statement:** [Barrick’s 2023 Annual Information Form filed with the SEC](https://www.sec.gov/Archives/edgar/data/756894/000119312524068583/d643214dex991.htm), downloaded HTML approximately 1.92 MB, reporting Barrick’s **45%** interest.

**Host statements:** [DRC 2023 EITI annexes XLSX](https://eiti.org/document/25572), downloaded 7.32 MB, and [national report PDF](https://eiti.org/document/25573), 4.23 MB. In sheet **Annexe 11** (with a trailing space in the actual name), row **29** is Kibali Goldmines SA. **C29 = Oui** marks the capital declaration as supplied by the company; **F29** identifies NIF **A0702049L**. **H29/I29** identify SOKIMO at **10%**; **L29/N29** identify Barrick at **45%**; the following row continues AngloGold Ashanti at **45%**. Annexe 13 also records the company’s statement about the two 45% controlling interests.

**If/then:** IF both company statements describe the same share class or economic interest at the same corporate level and date, AND a named holder’s percentages are mutually incompatible, THEN both cannot be correct.

**Immediate work:** use the 45/45/10 split as a control and expand to other operators marked as having supplied their declaration. An [AngloGold Ashanti 2023 SEC filing](https://www.sec.gov/Archives/edgar/data/1973832/000162828024017820/au-20231231.htm) was located as a potential third statement, but its download was not included in this candidate’s verified pair.

Do not equate a direct holding company’s share with a parent’s effective economic interest. Track acquisitions and share classes. Missing beneficial-owner information is not an incompatible affirmative assertion. Kamoa was excluded from this ownership pilot because its host-table company-submission marker is “Non”.

**Readiness:** host company authorship and Western interest verified; same-date and same-level ownership checks remain mandatory.

## 8 IAMGOLD Essakane in Burkina Faso

**First comparison:** company-declared equity ownership; production is a later extension. Ownership determines state profit participation.

**Western statements:** [IAMGOLD 2023 AIF filed with the SEC](https://www.sec.gov/Archives/edgar/data/1203464/000106299324006457/exhibit99-1.htm), downloaded HTML approximately 1.05 MB, and [2024 SEC-filed MD&A](https://www.sec.gov/Archives/edgar/data/1203464/000162828025006844/q42024managementdiscussion.htm), 2.03 MB. The ownership split is IAMGOLD **90%**, state **10%**.

**Host statements:** [Burkina Faso 2024 EITI annexes XLSX](https://eiti.org/document/25565), downloaded 17.36 MB, and [report PDF](https://eiti.org/document/25566), 2.30 MB. Match IAMGOLD Essakane SA, tax ID **00016079H**. Annexe 10, row **9**, marks the company as having supplied legal-ownership data.

The original form is embedded inside the XLSX ZIP at **xl/embeddings/Microsoft_Excel_Worksheet3.xlsx**. The outer workbook relationship **sheet11.xml.rels, rId10**, with anchor at zero-based row **8**, associates it with Essakane row 9. In the embedded sheet **17.Structure de Capital** (trailing space), **D13 = 0.10** for the state and **C15/D15 = IAMGOLD/0.90**. The form includes a management-attestation section. Its capital-date label says **31/12/2023**, even though its reporting-period header says 2024.

**If/then:** IF that date label is resolved and two declarations assert different ownership fractions for the same interest at the same time, THEN both cannot be correct.

**Immediate work:** preserve the embedded form and the workbook relationship proving which company supplied it. Do not silently change the capital date to 2024. Use the 90/10 split as the control, then extract other embedded capital forms.

For a production follow-up, host Annexe 6 **E18** reports company gold volume **14,603.158 kg**, while the SEC 2024 table reports **454,000 oz** at 100% scope. Doré/fine gold, inventory and production definitions remain unresolved; that raw difference is not an established contradiction.

**Readiness:** original embedded form, parent filing and company provenance verified; explicit date ambiguity remains gated.

## 9 Barrick Lumwana in Zambia

**First comparison:** cash-paid mineral royalties and corporate income tax for 2023. The royalty alone is approximately USD 66 million.

**Western statement:** [Barrick 2023 Canadian ESTMA report](https://www.barrick.com/files/doc_downloads/estma/Barrick_2023_ESTMA_Report.pdf), downloaded PDF 259,256 bytes. Lumwana royalties are **USD 66,410,000** and income taxes **USD 7,620,000**.

**Host statement:** [Zambia EITI 2023–2024 report](https://eiti.org/document/25291), downloaded PDF 3.41 MB. Use the **2023 reconciliation**, not the combined report title as the payment period. Physical PDF page **119**, printed page **117**, records Lumwana’s company-declared mineral royalty **ZMW 1,295,435,702.84** and income tax **ZMW 157,681,355.48**.

The report separately records government royalty **ZMW 1,338,626,264.60** and a final reconciliation position **ZMW 1,317,031,032.60**, with notes about a duplicate government record and earlier-year amounts paid in 2023. Keep the original company claim and any adopted corrections separately.

**If/then:** IF the declarations cover the same cash-paid royalty or income tax, AND validated FX, refunds, offsets and amendments cannot reconcile them, THEN both cannot accurately describe the same payments.

**Immediate work:** extract the two company-column fields and establish transaction-date FX bounds. A payment year is different from a tax-liability year. An annual average such as 20.22 ZMW/USD is contextual, not sufficient proof. Separate cash from VAT offsets.

Kansanshi is an expansion candidate only after separating statutory royalties from its distinct ZCCM arrangement. The domestic differences already explained in the host report are not a fresh cross-government finding.

**Readiness:** both sources and exact company column verified; reconciliation, cash-basis and currency checks remain unresolved.

## 10 Galiano Asanko in Ghana

**First comparison:** 2023 mineral royalties declared through two reporting systems. The approximately USD 15 million claim offers an English-language baseline for the financial rules.

**Western statement:** [Galiano 2023 Canadian ESTMA report](https://s203.q4cdn.com/835664992/files/doc_downloads/estma/galiano-gold-inc-2023-estma-report-final.pdf), downloaded PDF 435,496 bytes. Asanko royalties are **USD 14,802,000**, reported on a cash basis and rounded to the nearest USD 1,000.

**Host statement:** [Ghana 2023 mining reconciliation report](https://eiti.org/sites/default/files/2023%20gheiti%20mining%20sector%20reconciliation%20report.pdf), downloaded PDF 5.20 MB. Match Asanko Gold Mines Ltd, TIN **C0004524764**. Appendix **3D** begins on physical PDF page **250**; page **251**, printed page **236**, gives company-final royalties **GHS 142,780,548**. The separate government adjustment is **GHS 11,606,054**.

**If/then:** IF the project scope, included recipients and cash year are identical, AND legitimate conversion and rounding intervals do not overlap, THEN the royalty declarations conflict.

**Immediate work:** anchor extraction to the TIN and Appendix 3D, preserve the company-final and original amounts separately, and read category-specific currency notes. Some payments may already be in USD. The return’s exchange-rate notes cannot be indiscriminately applied to every payment line.

Do not scale project-wide payments by Galiano’s historical ownership percentage. Its corporate withholding-tax line is not automatically part of the same project payment. Exclude the already published domestic government adjustment from any claim of a newly discovered cross-government mismatch.

**Readiness:** both source files and company attribution verified; payment-currency and project-scope documentation are required before a verdict.

## How Rabbit should decide that both claims cannot be true

Approve eight conditions before producing an incompatibility verdict:

1. Both underlying statements are attributable to the company, rather than a compiler, government-receipt column or translator.

2. The project and legal entities match, with explicit subsidiary-to-parent and project-component mappings.

3. The effective dates or reporting periods match.

4. The economic and physical definitions match: fine metal versus concentrate, direct versus effective ownership, paid versus owed, or gross versus net.

5. The scope matches: 100% versus attributable amounts, recipients, included facilities and payment categories.

6. Revisions and amendments have been reconciled, retaining the original versions.

7. Rounding, units and legitimate currency-conversion uncertainty are represented.

8. Both are affirmative, sufficiently complete claims; blank, non-response, below-threshold and omitted fields remain unknown rather than zero.

For two numerical claims, represent each as a permissible interval. Only disjoint intervals establish numerical incompatibility. For positive local-currency payments totalling L, with every valid payment-date exchange rate between r_min and r_max local units per USD, the USD sum must lie in **[L/r_max, L/r_min]**. Add documented rounding uncertainty. With mixed currencies, negative refunds or offsets, derive bounds by component. An annual-average FX rate is not an adequate substitute.

For categorical claims, use reviewed mutually exclusive categories. “Downstream” and “upstream” may be incompatible for the same construction stage; “modified centreline” and “centreline” need not be.

Return **COMPATIBLE WITH PRECISION**, **REVIEW REQUIRED**, or **INCOMPATIBLE CLAIMS**. Only the last means the verified assertions cannot both be correct. It does not independently establish intent or which government received the incorrect statement.

Actual controls from this research: the Peru molybdenum intervals overlap; Ity and Senegal royalties are compatible across the disclosed FX range. Fekola’s dividend intervals are disjoint before definition adjustments, so that case remains REVIEW REQUIRED. A separate, explicitly synthetic disjoint-value example exercised the incompatibility branch of the comparison code.

## Use AI translation without losing the evidentiary statement

Keep the original-language passage or spreadsheet cell beside its translation, with document URL, reporting period, source version, exact page or cell and the company-attribution evidence. Store the literal number and unit before converting either. Use translation to extract candidate claims; use deterministic arithmetic and reviewed definitions for the final comparison.

Useful distinctions include Portuguese **alteamento a jusante** as downstream raising, **alteamento a montante** as upstream raising, and **linha de centro modificada** as modified centreline; French **ristourne minière** can mean the local royalty share; **déclaration société** is a company statement, while **déclaration administration** is a government statement. Preserve the company/government distinction through every intermediate table.

Do not let a model silently repair ambiguous dates, change a negative sign, equate paid with payable, or infer zero from an empty cell. Have a human approve each new term-to-fact mapping, then reuse that approved mapping across the corpus. The machine should show the two original assertions, their translations and the reason the intervals or categories cannot overlap.

A minimal claim record should retain source URL and hash, page or cell, company and project IDs, speaker, recipient system, effective date, submission/version date, original text, translated text, fact type, original value and unit, normalized interval or category, amendments and the eight approval conditions.

## Immediate pilot and expansion

**Production pilot:** Southern Copper molybdenum is the clearest numerical control. Implement the two-mine aggregation, pound-to-tonne conversion and published rounding interval; then extend across the national MINEM workbook to other companies with verified SEC filings.

**Physical-fact pilot:** extract all six Kinross dams from the ANM CSV and pair them with technical-report sections. Begin with historical design attributes that can be aligned to a construction stage. Freeze the host CSV by retrieval date and seek dated history for changing fields.

**Payment pilot:** implement Ity’s six royalty cells and explicit SMI/SMD/SMF mapping. Expand only after the royalty basket and currency treatment pass review. The same extraction pattern applies to Senegal and other projects in the Côte d’Ivoire workbook.

**Targeted investigative lead:** settle Fekola’s gross/net and shareholder-entitlement definitions before describing the non-overlapping dividend figures as an inconsistency. The documents and exact cells needed to start that review are linked above.

**Ownership pilot:** use Kibali and Essakane as controls. The Burkina Faso embedded forms are particularly valuable because ordinary spreadsheet parsers can miss the company-original evidence.

Keep amounts and facility characteristics connected to why a discrepancy matters: public revenue, state profit participation, production reporting and tailings oversight. Materiality should guide prioritization after comparability is established.

## Rejected routes and limits on the underlying hypothesis

A Philippine MGB bulletin request returned HTTP 403; one EITI Senegal company-revenue API route returned 403; the Mongolia live reporting portal returned 502. These were not counted as usable endpoints. Mongolia and Guinea PDFs were accessible, but no equally strong, fully matched company-attributed pair was established for the final ten. Kamoa’s company capital declaration was marked as not supplied, so it was excluded from that ownership pilot.

Cross-jurisdiction checking should be treated as a coverage hypothesis, not as an established absence of previous work. The [Mauritania 2024 report](https://eiti.org/document/25353), physical PDF page 60, expressly compares Tasiast’s local declaration with Kinross ESTMA and says those company amounts agree. It distinguishes that match from differences with government figures. The defensible opportunity is broader coverage, reproducibility, multilingual extraction and stricter factual predicates.

This extends the earlier Rabbit ESTMA mechanism, including source SYS-0295, by insisting that both compared claims are the company’s own representations. Ordinary EITI reconciliation often compares company payments with government receipts; that is a different logical relationship.

All ten candidate pairs returned HTTP 200 and were parsed far enough to identify the stated company or project. A page title or search snippet alone was not accepted as an access test. Access on the research date does not establish uptime, completeness for every year, unrestricted redistribution, or publication-ready proof of wrongdoing. No company or regulator was contacted, and no material cross-government contradiction has yet been established to publication standard.