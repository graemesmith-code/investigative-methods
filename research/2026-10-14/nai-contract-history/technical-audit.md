# NAI Logistics B.V.: public award-history findings

Retrieved October 14, 2026, in the cloud workspace. The collection was read-only. Public publication was subsequently authorized; no account creation, paid services, outreach or record requests. Repository recovery snapshot: `8557d0d9c6b8c1effe2d53e8b95d2425cb6d0e5f`. This folder publishes the relevant evidence and reproducible queries. The larger cloud audit remains local.

## Main finding

The final zero-obligation termination row is not the complete picture. Official USAspending records show eight new delivery orders with positive obligations dated December 13–14, 2023, after the December 11 designation. Gross positive obligations were **$36,309.46**. Five P00001 modifications reduced obligations by **$15,662.32**, leaving **$20,647.14 net** for those eight orders. Four were completely deobligated; one was reduced by $25.93. The modification action dates are December 13; their initial reporting dates are December 18. These records establish reported new orders and obligations after designation. They do not establish physical delivery, acceptance, cash payment, or a sanctions violation.

The original DLA termination document and its embedded signed notice provide additional evidence beyond the database. P00002 terminated the contract **in its entirety**, under FAR 52.212-4(m), effective and signed March 11, 2025. The notice expressly attributes the action to OFAC designation and says OFAC/DFAS restricted transactions because no applicable general license or exemption existed for this engagement. That is the contracting officer's dated statement, not an independent legal conclusion by this investigation. The parallel legal review identified a pre-existing official-government-business authorization; applicability and the basis for the agency's position remain unresolved.

The latest positive obligation in the accessible recipient-wide records is December 14, 2023. There are no later positive procurement obligations or new orders in those retrieved records. The only later procurement action is the March 11, 2025 vehicle termination. The 15-month interval therefore does not demonstrate 15 months of continuing orders, performance or payments.

## Original records and exact termination reason

Primary sources recovered directly from the DLA public package, using ordinary notice-and-consent forms and valid TLS:

- [DLA award package](https://www.dibbs.bsm.dla.mil/Awards/AwdRec.aspx?contract=SPE60523D9402&dlv=&cnt=).
- [Original contract](https://dibbs2.bsm.dla.mil/Downloads/Awards/22NOV22/SPE60523D9402.PDF), saved as `evidence/documents/SPE60523D9402.pdf` (11 pages).
- [P00001](https://dibbs2.bsm.dla.mil/Downloads/Awards/22NOV22/SPE60523D9402_P00001.PDF), saved with embedded contractor-signed copy.
- [P00002](https://dibbs2.bsm.dla.mil/Downloads/Awards/22NOV22/SPE60523D9402_P00002.PDF), saved with embedded `Termination Notice NAI T4C Signed.pdf` (2 pages). The attachment was extracted with `pdfdetach`; it is part of the official retrieved PDF, not a separately sourced document.

P00002, continuation page 2, states:

> The United States Department of the Treasury – Office of Foreign Assets Control (OFAC) placed NAI LOGISTICS B.V. on the OFAC sanctions list. The purpose of this modification is to terminate for cause contract number SPE60523D9402 in its entirety in accordance with FAR 52.212-4(m).

It incorporates the March 11, 2025 notice. The notice states on pages 1–2:

> The Government shall pay Supplier for any accepted Deliverables provided prior to the effective date of termination unless such payment is prohibited by law or subject to any applicable set-off right. The Government has been restricted by OFAC\ DFAS for transactions because there is no applicable general license or exemption for the Government’s engagement with NAI. FAR 25.701 (a).

It also says designation stops further performance. The notice was digitally signed by John Parson March 11, 2025 at 08:59:40 -04:00. The recorded digital-signature text has been preserved; cryptographic signature validation was not performed. The notice does **not** say when the restrictions began, identify invoices or payments, quantify accepted deliveries, discuss the Part 583 general authorization, or explain the timing of the March 2025 decision. Its payment clause is conditional language, not evidence any particular deliverable was accepted or paid.

The exact USAspending action reason code is X, **TERMINATE FOR CAUSE**, with $0.00 action obligation. The detailed original reason is designation, with complete termination; the database label alone omitted this explanation.

## Identity and original baseline

Recovered `experiments/01-ofac-baseline.md`, `annexes/experiments/01-ofac-baseline.md`, `evidence/ofac/original-report.md`, original screen source metadata, selected NAI excerpt and sanctions archive. The historical baseline and report remain unchanged in the repository; a dated follow-up link has been added. The prior screen deliberately covered FY2025 action dates (October 1, 2024–September 30, 2025) and found one NAI row in that period. It explicitly said vehicle and FY2024 delivery-order reconstruction had not been completed. This explains why the baseline stopped at the termination row; it did not provide evidence that the FY2024 order history was empty.

Identity in current official procurement rows: NAI LOGISTICS B.V., UEI **SLVJF3DR8MN5**, CAGE **H2G78**, Kingsfordweg 151, Amsterdam, Netherlands, 1043 GR. Historical direct-recipient DUNS **491319143** appears in 158 award details / 328 transaction rows; older rows use Schiphol Boulevard 231, Luchthaven Schiphol. The parent fields also contain UEI **H9J3LCB6URU8** and DUNS **561470928**, with the same recorded parent name. These parent identifiers were searched as additional retrieval keys; they are not treated as independently established corporate identity or ownership findings.

The preserved OFAC snapshot identifies entity **44257**, Dutch registration **60346515**, VAT **NL853868670B01**, and no aliases. [Original December 11 announcement](https://ofac.treasury.gov/recent-actions/20231211) and [Federal Register notice](https://www.govinfo.gov/content/pkg/FR-2023-12-18/pdf/2023-27725.pdf) provide the historical designation, rather than inferring it from a current list. Federal Register PDF and extracted text are saved in `evidence/documents/`. The parallel legal reviewer verified E.O. 13818 / GLOMAG and distinguished Cyprus NAI Logistics Limited (44252).

## Vehicle chronology and date distinctions

| Event | Procurement database action date | Original document dates and meaning | Action obligation |
|---|---|---|---:|
| Base award, modification 0 | 2022-11-08 | SF1449 block 3 award/effective date is November 8; contracting officer signature block 31c is November 22. DIBBS award/post date is November 22. | $0.00 |
| P00001 | 2023-07-10 | Original SF30 effective date points to block 16c, July 9. Embedded copy has contractor date July 5 and officer July 9. Incorporates FAR 52.204-27, the ByteDance/TikTok prohibition; it is not a sanctions action. | $0.00 |
| OFAC designation | Not a procurement action | December 11, 2023, original Treasury/Federal Register evidence. | — |
| Eight new orders and five reducing modifications | 2023-12-13 / 14 | Order SF1449/SF30 documents were not available through the explored public DIBBS searches. Action dates below are database dates; actual signature/effective dates are unverified. | +$36,309.46 / -$15,662.32 |
| P00002 | 2025-03-11 | Original SF30 block 3 refers to block 16c, March 11. Complete termination; designation is the stated cause. | $0.00 |

USAspending `date_signed` for the vehicle is November 8, but the original officer signature is November 22. Do not collapse these into one date. Original ordering period is January 1, 2023–September 30, 2027. Original delivery period is “48 Hours after 1 February 2023 through 31 October 2027.” Current database ordering end is October 31, 2027; it changes in the P00001 data row, but the retrieved P00001 narrative concerns a clause update, so this investigation does not claim the original modification substantively extended the ordering period. The later end-date field does not override complete termination.

The vehicle's **$6,851,344.57** original total award / potential value is a requirements-contract estimate/value, not an obligation or payment. USAspending reports $0 vehicle obligations, with spending recorded on the child orders. Current net obligations across all 27 children are **$148,422.44**: FY2023 $24,489.25 and FY2024 $123,933.19.

## Every FY2024 delivery order under SPE60523D9402

FY2024 means October 1, 2023–September 30, 2024. There are 19 orders / 24 action rows in the retrieved official data; all have this parent reference. Dates under performance are reported contractual periods, not proof of executed delivery. “Gross” is the base action obligation; “reductions” is the sum of modifications. All amounts USD.

| PIID | Base action date | Gross | Reductions | Net | Reported performance period |
|---|---|---:|---:|---:|---|
| [SPE60524FVX9U](https://www.usaspending.gov/award/CONT_AWD_SPE60524FVX9U_9700_SPE60523D9402_9700/) | 2023-11-20 | 14350.57 | 0.00 | 14350.57 | 2023-11-23–2023-11-23 |
| [SPE60524FVX9V](https://www.usaspending.gov/award/CONT_AWD_SPE60524FVX9V_9700_SPE60523D9402_9700/) | 2023-11-20 | 4783.52 | 0.00 | 4783.52 | 2023-11-27–2023-11-27 |
| [SPE60524FVY0B](https://www.usaspending.gov/award/CONT_AWD_SPE60524FVY0B_9700_SPE60523D9402_9700/) | 2023-11-20 | 14350.57 | 0.00 | 14350.57 | 2023-11-30–2023-11-30 |
| [SPE60524FVY0C](https://www.usaspending.gov/award/CONT_AWD_SPE60524FVY0C_9700_SPE60523D9402_9700/) | 2023-11-20 | 14350.57 | 0.00 | 14350.57 | 2023-11-29–2023-11-29 |
| [SPE60524FVZ1R](https://www.usaspending.gov/award/CONT_AWD_SPE60524FVZ1R_9700_SPE60523D9402_9700/) | 2023-11-24 | 5580.78 | 0.00 | 5580.78 | 2023-11-29–2023-11-29 |
| [SPE60524FVZ1S](https://www.usaspending.gov/award/CONT_AWD_SPE60524FVZ1S_9700_SPE60523D9402_9700/) | 2023-11-24 | 14350.57 | 0.00 | 14350.57 | 2023-11-29–2023-11-29 |
| [SPE60524FVZ1T](https://www.usaspending.gov/award/CONT_AWD_SPE60524FVZ1T_9700_SPE60523D9402_9700/) | 2023-11-24 | 2391.76 | 0.00 | 2391.76 | 2023-11-29–2023-11-29 |
| [SPE60524FWD9U](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWD9U_9700_SPE60523D9402_9700/) | 2023-12-08 | 14224.21 | 0.00 | 14224.21 | 2023-12-13–2023-12-13 |
| [SPE60524FWD9V](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWD9V_9700_SPE60523D9402_9700/) | 2023-12-08 | 14224.21 | 0.00 | 14224.21 | 2023-12-14–2023-12-14 |
| [SPE60524FWE0D](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWE0D_9700_SPE60523D9402_9700/) | 2023-12-08 | 2562.85 | 0.00 | 2562.85 | 2023-12-12–2023-12-12 |
| [SPE60524FWE0R](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWE0R_9700_SPE60523D9402_9700/) | 2023-12-08 | 2116.44 | 0.00 | 2116.44 | 2023-12-13–2023-12-13 |
| [SPE60524FWF4N](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWF4N_9700_SPE60523D9402_9700/) | 2023-12-13 | 13531.51 | 0.00 | 13531.51 | 2023-12-13–2023-12-18 |
| [SPE60524FWF4Q](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWF4Q_9700_SPE60523D9402_9700/) | 2023-12-13 | 10750.03 | -10750.03 | 0.00 | 2023-12-13–2023-12-21 |
| [SPE60524FWF4R](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWF4R_9700_SPE60523D9402_9700/) | 2023-12-13 | 902.10 | -902.10 | 0.00 | 2023-12-13–2023-12-21 |
| [SPE60524FWF4S](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWF4S_9700_SPE60523D9402_9700/) | 2023-12-13 | 1879.37 | -1879.37 | 0.00 | 2023-12-13–2023-12-21 |
| [SPE60524FWF4V](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWF4V_9700_SPE60523D9402_9700/) | 2023-12-13 | 2104.89 | -2104.89 | 0.00 | 2023-12-13–2023-12-20 |
| [SPE60524FWF5C](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWF5C_9700_SPE60523D9402_9700/) | 2023-12-13 | 751.75 | -25.93 | 725.82 | 2023-12-13–2023-12-20 |
| [SPE60524FWF6Y](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWF6Y_9700_SPE60523D9402_9700/) | 2023-12-13 | 2631.06 | 0.00 | 2631.06 | 2023-12-21–2023-12-21 |
| [SPE60524FWG0C](https://www.usaspending.gov/award/CONT_AWD_SPE60524FWG0C_9700_SPE60523D9402_9700/) | 2023-12-14 | 3758.75 | 0.00 | 3758.75 | 2023-12-14–2023-12-21 |

All five reductions are P00001, action date December 13, 2023, code M **OTHER ADMINISTRATIVE ACTION**. Four orders (FWF4Q, FWF4R, FWF4S, FWF4V) are fully deobligated. FWF5C is reduced by $25.93 to $725.82. The code is not **LEGAL CONTRACT CANCELLATION** or **TERMINATE FOR CAUSE**; without their original modifications, the precise operational reason for the reductions is unverified. This memo describes the financial result, not a proven cancellation rationale.

Four December 8 orders were placed before designation but have reported performance dates December 12–14. Eight December 13–14 orders have post-designation performance periods. None of those scheduled periods alone proves delivery. No later performance evidence was recovered.

## Eight FY2023 delivery orders / pre-designation baseline

| PIID | Base action date | Net obligation | Reported performance period |
|---|---|---:|---|
| [SPE60523FSC9V](https://www.usaspending.gov/award/CONT_AWD_SPE60523FSC9V_9700_SPE60523D9402_9700/) | 2023-01-25 | 2672.01 | 2023-01-30–2023-01-30 |
| [SPE60523FSC9W](https://www.usaspending.gov/award/CONT_AWD_SPE60523FSC9W_9700_SPE60523D9402_9700/) | 2023-01-25 | 2672.01 | 2023-01-30–2023-01-30 |
| [SPE60523FSE9R](https://www.usaspending.gov/award/CONT_AWD_SPE60523FSE9R_9700_SPE60523D9402_9700/) | 2023-01-31 | 1791.75 | 2023-02-03–2023-02-03 |
| [SPE60523FTB2Z](https://www.usaspending.gov/award/CONT_AWD_SPE60523FTB2Z_9700_SPE60523D9402_9700/) | 2023-04-03 | 2202.85 | 2023-04-11–2023-04-11 |
| [SPE60523FTB3A](https://www.usaspending.gov/award/CONT_AWD_SPE60523FTB3A_9700_SPE60523D9402_9700/) | 2023-04-03 | 4405.71 | 2023-04-11–2023-04-11 |
| [SPE60523FTC7W](https://www.usaspending.gov/award/CONT_AWD_SPE60523FTC7W_9700_SPE60523D9402_9700/) | 2023-04-06 | 5140.00 | 2023-04-14–2023-04-14 |
| [SPE60523FUZ7X](https://www.usaspending.gov/award/CONT_AWD_SPE60523FUZ7X_9700_SPE60523D9402_9700/) | 2023-09-01 | 2155.73 | 2023-09-28–2023-09-28 |
| [SPE60523FUZ8N](https://www.usaspending.gov/award/CONT_AWD_SPE60523FUZ8N_9700_SPE60523D9402_9700/) | 2023-09-01 | 3449.19 | 2023-09-14–2023-09-14 |

Before designation there were 19 orders (eight FY2023 and eleven FY2024) totaling $127,775.30 net obligations. Subsequent positive obligations were confined to December 13–14, 2023 in the retrieved history.

## Reporting and corrections

The original vehicle base action has initial report date December 13, 2023, despite the 2022 effective/signing dates; P00001 also has initial report date December 13, 2023. P00002 was initially reported March 11, 2025, last modified March 12, 2025. The eight post-designation base orders were initially reported on their action dates except **SPE60524FWF6Y**, action December 13, 2023, initially reported **August 22, 2025**. That particular order is retrospective database evidence rather than an independently recovered contemporaneous order document.

The five reductions were initially reported December 18, 2023, although all carry December 13 action dates. Three have last-modified timestamps in December 2025, and FWF4V in July 2026. Reporting / correction dates do not establish new obligations or ongoing work on those later dates. Same-day base and modification ordering cannot be inferred from the API sort order. Full row timestamps are in `fy2024-order-transactions.csv`.

## Payments, outlays and missing records

There are seven File C federal-account funding records linked to this vehicle's children, reporting FY2024 fiscal month 3 (December 2023), account **097-4930**, Defense Working Capital Fund, Defense, object class 26.0, program activity 0801, DEFC Q. All seven `gross_outlay_amount` values are **null**. Their reported account obligations sum to $34,070.57, differing from the procurement-row net obligations. They include positive funding amounts for four fully deobligated procurement orders and omit late-reported FWF6Y. These are separate data series; they must not be added to procurement obligations, treated as cash payments, or silently reconciled by assumption.

The vehicle amounts endpoint shows zero aggregate outlays; individual award details show `total_outlay:null` and `total_account_outlay:0`. Null underlying outlay records and absent funding rows make “no payment occurred” unsupportable. No post-designation payment date, disbursement voucher, invoice settlement, bank transfer, supplier receipt, acceptance certificate, delivery ticket or blocked-payment record was recovered. The termination notice supplies a restriction claim, but no dated blocking ledger or start date.

Recipient-wide funding retrieval covers every one of the 251 awards/vehicles and yields 77 direct award funding rows plus 35 IDV child rollup rows (the rollups repeat child records and must not be double-counted). Two positive historical outlay entries exist, both before designation: $24,540.15 on SPE60520P2725, FY2022 fiscal month 6 (March 2022); and $15,489.53 on SPE60521P8692, FY2021 fiscal month 9 (June 2021). These are reporting-period account outlays, not dated supplier-payment vouchers. No reporting period later than December 2023 is present in the retrieved account-funding rows. Historical outlay evidence demonstrates why obligations and payments must be queried separately.

## Recipient-wide award history and reproducible coverage

The unrestricted UEI search returned **244 contracts and seven vehicles**, with **450 unique transaction rows**, action dates December 30, 2014–March 11, 2025. Net procurement obligations across these records are $3,278,422.34, not payment totals. All FY2024 procurement actions found are under SPE60523D9402. The seven vehicles are SPE60015D9502, SPE60015D9516, SPE60017D9502, SPE60017D9503, SPE60017D9505, SPE60518D9402 and SPE60523D9402. Their complete transactions and every associated award's transaction history are preserved.

`all-recipient-awards.csv` and `all-recipient-transactions.csv` contain the entire recovered official rows, including modifications, administrative actions, closeouts, historic terminations, positive and negative obligations, recipient identifiers and parent references. These records include 31 termination-for-convenience rows and one termination-for-cause row. This investigation did not independently authenticate every old contract document or establish why historical recipient/parent fields changed.

Queries and counts (no action-date restriction unless explicitly indicated):

| Query / route | Retrieved result count | Pagination |
|---|---:|---|
| `recipient_search_text:[SLVJF3DR8MN5]`, contracts A/B/C/D | 244 awards | 100 + 100 + 44, final hasNext false |
| Same UEI, IDV types | 7 vehicles | 1 page, final hasNext false |
| Recipient-name text `NAI LOGISTICS` | Same 244 / 7 | Fully paginated, same ID sets |
| Historical direct DUNS 491319143 | 158 contracts / 0 IDVs | 100 + 58; none additional |
| Parent UEI H9J3LCB6URU8 | 103 contracts / 1 IDV | 100 + 3; none additional |
| Parent DUNS 561470928 | 27 contracts / 0 IDVs | 1 page; none additional |
| Vehicle `idvs/awards`, `child_awards` | 27 orders | 1 page, final hasNext false |
| Vehicle `child_idvs` / `grandchild_awards` | 0 / 0 | Each final hasNext false |
| Vehicle `transactions` and count | 3 | Count independently agrees |
| Each recipient award `transactions` | 450 total | Every endpoint traversed to final hasNext false |
| Recipient transaction search, contracts | 436 | 100 + 100 + 100 + 100 + 36 |
| Recipient transaction search, IDVs | 14 | 1 page |
| Official recipient download | 251 award rows + 450 transaction rows | 701 total, independently agrees with paginated API |
| Official vehicle download | 27 order summaries + 3 vehicle actions + 7 funding rows | 37 total |
| Vehicle funding and each of 27 child funding endpoints | 7 funding rows / 20 children with none | Every endpoint fully paginated |
| Every recipient award/vehicle funding endpoint | 77 direct rows / 35 rollup rows | Every endpoint fully paginated |

Direct `award_ids:SPE60523D9402` finds the vehicle but does not find its differently numbered children in ordinary contract search. A hyphenated vehicle search returned zero; stripping formatting and following the relationship endpoint is essential. Child keys are `CONT_AWD_<child PIID>_9700_SPE60523D9402_9700`; the vehicle is `CONT_IDV_SPE60523D9402_9700`. Official agency values are DoD top-tier 097, DLA subtier 97AS, historical/submitting/parent identifier 9700, and offices SPE605 / SPE600. Searches were not artificially restricted to one office, country or period.

Address and CAGE keyword searches in USAspending returned zero; these are not reliable identity filters for absent records. A quoted recipient-name search also returned zero, while ordinary name and UEI searches agreed. Persisted failed and empty query attempts are preserved; initial exploratory retries may have been superseded under the same file labels. OFAC lists no aliases for 44257; raw procurement names are consistently NAI LOGISTICS B.V. with no DBA field. No additional alias was invented.

Saved reproducibility: [reproduce.py](reproduce.py), [query manifest](evidence/query-manifest.json), [reconciliation checks](evidence/reconciliation.json), and [official API snapshot ZIP](evidence/official-api-snapshot.zip). The ZIP contains original public API responses and official exports, with exact request bodies, UTC retrieval timestamps, status, byte counts and response SHA-256 values. HTTP response headers, cookies, browser form state and unrelated evidence are excluded. The readable evidence files alongside the ZIP preserve full recipient rows and order summaries. The reproduction script can retrieve a later snapshot; corrections may change historical rows. Public source documents are in [evidence/documents](evidence/documents/).

All eight base-order records were separately reviewed against fresh official award-specific downloads before publication: action dates, initial-report dates, obligations and performance periods agree with the recipient export. [Eight-record check](evidence/eight-base-order-review.json). These are original database/export rows, **not recovered signed delivery-order documents**. Actual signed/effective dates of those orders and reducing modifications remain unverified. The base rows for FWF4Q, FWF4R, FWF4S, FWF4V and FWF5C initially report a December 19 performance end; later modification/latest-award fields report December 20 or 21. The order-summary table uses latest reported periods, while the eight-base-row review preserves the base periods. Neither establishes actual delivery.

## Official access limits and bounded searches

[GSA's FPDS transition page](https://sam.gov/fpds) says ezSearch was decommissioned February 24, 2026 and searching public awards in SAM.gov requires sign-in; the [successor API documentation](https://open.gsa.gov/api/contract-awards/) requires a personal/public API key. Ordinary legacy ATOM requests returned a page-not-found / HTTP 400 response; the unauthenticated successor request returned HTTP 404. No account was created and no auth was bypassed. Deleted-contract history and independent current SAM/FPDS verification of each child were therefore unavailable. USAspending is the accessible official alternative; its procurement data are sourced from the federal contract reporting system, so two USAspending routes are consistency checks, not wholly independent sources.

DIBBS public search by vehicle and CAGE H2G78 returned one vehicle package and the three original documents. Searching FWF6Y as a delivery order and award number, and all 19 FY2024 PIIDs as delivery orders, yielded no awards on file for those criteria. These empty document searches do not negate the USAspending order records. Conventional guessed PDF paths initially returned 404; later package-derived URLs succeeded. Public original order/modification documents, actual delivery/acceptance evidence and invoices remain unavailable from the explored routes. DIBBS access required ordinary consent forms on both public hosts; it did not require an account, TLS exception or access-control bypass. There is no unresolved browser-only DIBBS obstacle.

Bounded official-domain searches for exact vehicle, hyphenated vehicle, solicitation SPE60522R0214 and hyphenated form, NAI and termination, and NAI in DLA/Defense contract announcements did not recover a separate contemporaneous sanctions notice, order document or payment record. Web search result absence is not evidence no such records exist. The search-ledger JSON records these queries. The original vehicle package ultimately provided the relevant termination notice directly.

## What the delay establishes and what remains open

December 11, 2023 to March 11, 2025 is 456 elapsed days. Original records establish a later complete termination explicitly based on designation, and eight reported orders in the first three days after designation. They do not establish continuing business throughout the interval. Last positive obligation December 14, null public outlays, several complete deobligations, and the notice's OFAC/DFAS restriction statement are material counterevidence to an assertion of 15 months of uninterrupted purchasing/payment.

The strongest unresolved questions are: why were the December 13–14 orders placed; what prompted their reductions; did any fuel actually arrive or get accepted; when did OFAC/DFAS restrictions begin; what payments, blocked funds, set-offs or unsettled invoices existed; and why did the agency determine no authorization applied despite the pre-existing Part 583 official-government-business provision? No sanctions violation, failed screening, actual payment after designation, or applicable transaction authorization is established here.

Parallel legal review supplied historical [2022 rule](https://ofac.treasury.gov/media/930146/download), 31 CFR 583.509 effective December 21, 2022, and [2024 rule](https://ofac.treasury.gov/system/files/2024-03/20240311_global_magnitsky_sanctions_regulations.pdf), renumbering the provision to 583.510 effective March 12, 2024. That review is separate; this memo preserves the agency's original statement without assuming the scope, reliance or applicability of the general authorization. A provision's existence is not proof that it authorized release/payment from blocked property or displaced procurement restrictions.

The records most likely to resolve the remaining questions would be contemporaneous DLA sanctions determinations, original order/SF30 files, fuel delivery and acceptance records, DFAS payment/blocking ledgers and the underlying termination analysis. They were not requested; no outreach is authorized.


## Historical legal-text qualification

The original 2023 CFR is also preserved in [legal-2023-cfr.pdf](evidence/documents/legal-2023-cfr.pdf). At the time of the December 2023 orders, §583.502 was **reserved**. The 2024 paragraph 583.502(e) must not be applied retrospectively as a rule governing those orders. The 2023 provisions §583.503 (OFAC exclusions from licenses) and §583.404 (incidental transactions) raise possible questions, but no evidence establishes that they explain this particular DLA decision. The official-business provision's existence does not resolve its applicability or prove DLA relied on it. This report does not categorically exclude DLA from the provision based solely on its employees/grantees/contractors wording.
