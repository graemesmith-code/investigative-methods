# NAI calibration — partial independently refreshed record

The official 11 December 2023 OFAC notice independently confirms NAI Logistics B.V., Dutch registration 60346515, VAT NL853868670B01, Amsterdam Kingsfordweg address, and GLOMAG designation linked to Ajmal Rahmani. NAI Logistics Limited of Cyprus is listed separately. Sources are archived under sources/ofac-20231211.html and sources/treasury-jy1973.html; hashes and retrieval dates are in sources/manifest.json. This was already a public designation case, not a novel discovery.

The fresh official USAspending vehicle response sources/nai-current-award.json identifies CONT_IDV_SPE60523D9402_9700, recipient NAI LOGISTICS B.V., UEI SLVJF3DR8MN5, and KINGSFORDWEG 151, AMSTERDAM 1043 GR. Name and street/postal address strongly support identity; the procurement response does not independently supply the Dutch company registration number. Its signing date is 2022-11-08, before designation. Last modified date is 2025-03-12. The current vehicle has total_obligation 0, base_and_all_options 6851344.57, total_outlay null, and total_account_outlay 0. The option-inclusive value is not payments or new obligations; these vehicle-level fields do not establish child-order or payment history. Performance end date 2027-10-31 is not proof of continued activity.

The derived repository excerpt reports action date 2025-03-11, P00002, TERMINATE FOR CAUSE, and zero federal action obligation. The subsequently retrieved official transaction endpoint independently confirms this row; see the completed bounded history below. The September original matching rows remain unavailable. Do not equate the action date with the last-modified date.

The downloaded 2022 and 2024 Federal Register regulations independently contain official-US-government-business authorizations at 583.509 and 583.510 respectively. They cover the relevant part's prohibited transactions for official government business by employees, grantees, or contractors. This is a concrete potential lawful explanation requiring transaction-specific assessment; it does not establish that NAI activity qualified or override other sanctions programs. Parent supplied effective-date analysis; full historical rule application remains pending.

Initial checkpoint category (superseded by the bounded history below): strong identity lead; reported post-designation administrative termination. Next records: complete vehicle transactions and child orders, original termination instrument, deliveries/payment records if relevant, and authorization basis. No Jev judgment has been requested. No expansion names have been selected.

## Completed bounded current-API history

The official vehicle transaction endpoint returns three rows, with hasNext=false: original action 2022-11-08; P00001 OTHER ADMINISTRATIVE ACTION 2023-07-10; P00002 TERMINATE FOR CAUSE 2025-03-11. Each has zero additional obligations. Thus termination is independently confirmed; the vehicle's update date remains 2025-03-12.

The child-count endpoint reports 27 child awards, no child IDVs, and no grandchild awards. The explicit child_awards listing returns all 27 on one page. All 27 transaction histories were read within a frozen bound of 30 awards and 100 transactions per award; every response has hasNext=false. This gives 32 child transactions dated 2023-01-25 through 2023-12-14. Nineteen pre-designation transactions total $127,775.30 obligations. Thirteen post-designation transactions across eight orders total $36,309.46 positive obligations and −$15,662.32 adjustments, net $20,647.14. The complete $148,422.44 net matches the child aggregate endpoint. This is a current snapshot, not a reconstruction of what records showed at designation.

All eight post-designation child award-detail responses independently name NAI LOGISTICS B.V. and UEI SLVJF3DR8MN5. Seven have signing/action dates 13 December 2023; one has 14 December. Each original row is modification 0, delivery order, with a null action-type description. Five P00001 rows are labelled OTHER ADMINISTRATIVE ACTION with negative obligations; four fully offset their original positive row and one reduces it by $25.93. These are negative adjustments, not independently documented cancellations. Updates in 2025 or 2026 mean the same recorded action date cannot prove the adjustments were entered contemporaneously.

| Child order | Action date | Positive obligations | Negative adjustments | Net obligations | Current last modified |
|---|---|---:|---:|---:|---|
| SPE60524FWF4N | 2023-12-13 | 13,531.51 | 0.00 | 13,531.51 | 2023-12-13 |
| SPE60524FWF4Q | 2023-12-13 | 10,750.03 | -10,750.03 | 0.00 | 2025-12-05 |
| SPE60524FWF4R | 2023-12-13 | 902.10 | -902.10 | 0.00 | 2025-12-05 |
| SPE60524FWF4S | 2023-12-13 | 1,879.37 | -1,879.37 | 0.00 | 2025-12-05 |
| SPE60524FWF4V | 2023-12-13 | 2,104.89 | -2,104.89 | 0.00 | 2026-07-28 |
| SPE60524FWF5C | 2023-12-13 | 751.75 | -25.93 | 725.82 | 2023-12-18 |
| SPE60524FWF6Y | 2023-12-13 | 2,631.06 | 0.00 | 2,631.06 | 2025-08-22 |
| SPE60524FWG0C | 2023-12-14 | 3,758.75 | 0.00 | 3,758.75 | 2023-12-14 |

**Classification:** credible identity match; confirmed post-designation vehicle administration; possible new post-designation child-order business, with substantial administrative offsets. The two- to three-day interval is not grounds for dismissal. Conversely the dates alone do not prove fresh operational purchasing decisions, deliveries, payments, sanctions-screening failure, or unlawfulness. The official-business general license is a concrete potential authorization, not merely a generic caveat. Neither the old vehicle date nor that license automatically settles applicability.

All eight child-detail total_outlay fields are null. No payment total is established. Recorded performance windows end in December 2023, but they do not establish delivery. The vehicle's 2027 potential duration and $6,851,344.57 option-inclusive value are not the duration or amount of this post-designation finding. Public significance is a narrowly answerable procurement/authorization question involving $20,647.14 net recorded obligations, not evidence of continued multi-year payments.

Strongest innocent explanations: authorized official US government business under then-effective 583.509; record-entry timing/corrections or completion of previously arranged supply. The records do not establish which explanation applies. Obtain the eight signed order instruments, administrative modification documents and audit timestamps, supply acceptance/invoices if relevant, and the agency's transaction-specific authorization basis. This work involved no outreach.

**Coverage limits:** only this vehicle and its API-linked children, not all NAI awards, other vehicles, subsidiaries, ownership relationships, or the 13 original candidates. API pagination completeness is not assurance of underlying agency-reporting completeness. Baseline ZIP reconciliation, payment/acceptance documents, and original procurement instruments remain missing. The known public designation is preserved as prior-publicized status; novelty of these order rows has not been researched or claimed.

Raw requests and responses are in sources; SHA-256 and retrieval timestamps are in sources/manifest.json. nai-child-history.json links each child's exact transaction source. scripts/nai_history.py reproduces the bounded child-history acquisition with local cache reuse and no automatic retries. Initial malformed child sort returned HTTP 400 and is retained in the manifest; the documented corrected request succeeded. No rate/access failures occurred.
