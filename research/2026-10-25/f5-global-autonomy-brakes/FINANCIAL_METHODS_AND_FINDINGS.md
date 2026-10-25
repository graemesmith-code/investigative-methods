# F5 financial hydration: completed new live verification

Cutoff: 25 October 2026. This is a new F5 run, not a republication of F4 raw files. No paid API was used by this workstream. All financial amounts below are net reported obligations, not outlays or the price of effective safeguards.

## The corrected denominator

The source financial index contains **712,186 physical rows and 712,186 distinct transaction keys**. It is a discovery index, not a complete award ledger. All three source archives were checked against the user-supplied SHA256 identities before screening. Primary financial descriptions from the research-context, R&D contracts and capabilities archives were screened for MIL-STD-882E, SSSTRP, WSESRB, FISTRP, system/weapon safety, flight termination/AFTS, safe-and-arm/ESAD, range safety and hazard-tracking terms. Physical description observations include overlapping source collections and are not distinct actions. Coverage is separately counted in `safety-contract-screen-audit.json`: **every one of the 712,186 financial index keys has a primary-description observation**, across **886,629 overlapping physical description observations**.

This produced **102 exact award candidates**, including two mandatory F4 hydration regressions. All 102 received a new USAspending award-detail request, every no-date/no-keyword-filter transaction page, and every exact-identity FPDS Atom lifecycle page to exhaustion. **All 102 reconcile on both views**, with **1,053 distinct actions in each view**, retaining **104 negative FPDS actions**. USAspending and FPDS represent related agency-reported information; their agreement does not constitute independent evidence of performance.

Ten initial cases were promoted for substantive discussion or mandatory regression; 92 remain supporting machine candidates. Financial verification alone does not promote the 92 into autonomy-governance findings. A further independent live lead, Anduril's HR0011269E126, is a native **OtherTransactionAward**, not an IDV. It adds three FPDS actions and one FPDS-only financial reconciliation. Five subsequent targeted FAR leads bring the final financial register to **108 identities**: **107 FAR two-view reconciliations** and **one native FPDS-only OT**, with **1,192 USAspending actions**, **1,195 FPDS actions** and **113 negative FPDS actions**. The native OT is not presented as an additional USAspending reconciliation.

## Mandatory corrections, reproduced in new live data

| Exact generated identity | Archived actions | New USAspending / FPDS actions | Net obligation | Boundary |
| --- | ---: | ---: | ---: | --- |
| `CONT_AWD_N0042123F3004_9700_N0017819D7484_9700` | 3 | 53 / 53 | $27,836,455.94 | DCS air-vehicle test/evaluation support. Two negative actions retained. This is not wholly safeguards spending. |
| `CONT_AWD_N0016422F3007_9700_N0017819D7763_9700` | 6 | 19 / 19 | $24,423,706.49 | Herren unmanned/small-combatant professional support. A 5 July 2026 current PoP end does not prove termination or no continuation. |

Both include Modification 0. DCS's base signature is 31 March 2023; current PoP end is 31 May 2027. Herren's base signature is 6 July 2022; current PoP end is 5 July 2026. Signature dates and PoP dates are separate fields. The exercise fixes the misleading denominator, not merely the arithmetic of a filtered slice.

## Concrete assurance leads

| Exact identity | Scope in primary description | Net obligation / actions | Reporting limit |
| --- | --- | --- | --- |
| `CONT_AWD_FA865824FB015_9700_47QRAA20D006C_4732` | ENSCO independent verification/validation for CFSS autonomous flight-termination unit wrapper software and programmable-logic designs as part of certification | $433,665.20 / 9 | A concrete certification-support description; one negative action retained. Current PoP ended 1 March 2026. Not a demonstrated weapon-law governor or current operating certificate. |
| `CONT_AWD_W911QX23C0029_9700_-NONE-_-NONE-` | Textron completion of flight-termination system and field-test support for quadrotor autonomy | $700,000.00 / 9 | One negative action retained. Current PoP ended 30 September 2025. Does not demonstrate fielded lethal-platform compliance. |
| `CONT_AWD_W58RGZ22F0097_9700_W58RGZ21D0062_9700` | Soldier unmanned-aircraft system safety engineering support, System Dynamics International | $224,504.28 / 3 | Archive had two actions; new history has three, including a negative action. Scope does not identify operational outcomes. |
| `CONT_AWD_W56HZV19C0058_9700_-NONE-_-NONE-` | Autonomous Solutions Intelligent Urgent Stop; proposed safety-certification steps | $149,356.75 / 3 | Research on a vehicle emergency stop, not certification achieved or a legal engagement rule. Historical PoP ended 6 August 2020. |
| `CONT_AWD_FA865126FB024_9700_FA865121D0010_9700` | Cummings universal safe-and-arm module development and munition open-architecture test/evaluation | $206,693.00 / 1 | New 2026 action; functional engineering scope only. Signature 19 May; PoP starts 22 May, ends 22 December 2026. |
| `CONT_AWD_N0001421C2004_9700_-NONE-_-NONE-` | Advanced Acoustic Concepts electronic safe-and-arm fuze/device technologies | $6,897,797.00 / 7 | Does not establish autonomy, completed certification or implemented control on a particular fielded weapon. |
| `CONT_AWD_W900KK21F0075_9700_W900KK18D0010_9700` | Kratos target-system flight termination development | $924,465.41 / 2 | Aerial targets and range protection; not a blanket brake on operational engagements. |
| `CONT_AWD_N6660419P0553_9700_-NONE-_-NONE-` | McLaughlin Tomahawk system-safety hardware/software services | $75,576.09 / 1 | Safety-services description, not proof of any specified AI or legal review result. |

Every FAR case above has a primary source at `https://api.usaspending.gov/api/v2/awards/{exact_generated_identity}/`; the register retains the actual completed request URL, retrieval time and raw-response hash. FPDS receipts retain all actual page URLs.

## Anduril high-assurance OT: new live source, narrower claim

The official [FPDS Atom history](https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&VERSION=1.5.3&q=PIID%3A%22HR0011269E126%22&s=FPDSNG.COM&indexName=awardfull&start=0) identifies **`FPDS_OTHER_TRANSACTION_AWARD:9700:HR0011269E126`**, recipient Anduril Industries, UEI **KC3CH2MSK7Q3**, description **AIS and ADS-B high-assurance software**. The schema is `OtherTransactionAward/OtherTransactionAwardID/OtherTransactionAwardContractID`, with amounts and dates under `contractDetail`.

The complete visible history comprises Modification 0, signed 27 April 2026, $2,375,000; P00001, signed 19 May, $0; and P00002, signed 25 June, $326,162.33. Their net **$2,701,162.33** matches the feed aggregate. The all-options value is **$2,927,010**, a different financial field. Current and potential completion are 31 October 2027. No pagination next link remains. The original FPDS response SHA256 is `0e937ed6f4d1c8dec88abaac8c653e88e1ac5f7694ba5280734c2f8b92b5e615`.

An official USAspending PIID discovery search within A–D contract types returned no results. This limited search does not establish global absence from USAspending. No generated key was guessed, and no unrelated award's money was assigned. The USAspending mapping remains **unverified**, so cross-system reconciliation is unavailable. The native FPDS action/aggregate agreement is one source view. High assurance for AIS/ADS-B does not establish an engagement legal governor, safety-board approval, successful certification or implementation on a weapon.

## Controls and validation

`hydrate_full_award_lifecycle.py` separates exact identity from search discovery. It preserves agency, PIID, parent PIID/agency and record schema. FAR awards, FAR IDVs, native OT IDVs and native OT awards are distinct. Assistance uses USAspending transaction history rather than a contract-only FPDS denominator. Unavailable histories remain unavailable; no agency 9700 fallback is used to assign money.

The transaction request body contains only `award_id`, `page`, and `limit`. FPDS search selects only the exact PIID and known parent; returned identities are checked even if the index search is imprecise. Pages follow actual next links. Cycles, absent pagination metadata, missing IDs, null amounts, conflicting duplicate actions, unparsed schema entries and nonzero deltas prevent a clean reconciliation claim. Negative actions are never discarded. Source-defined recipient UEIs are not compared with nine-digit legacy DUNS identifiers; this workstream makes no SBIR-company-to-award money assignment.

The public retrieval journal records started/finished requests and body hashes. Current code fsyncs journal writes and writes aggregate outputs by atomic replacement. Initial retrievals used a flushed journal; do not call the earlier process crash-proof. `--resume` reuses completed records; incomplete records emit warnings and require the explicit read-only `--retry-incomplete` option to replace them. It does not silently treat a retained failed request as complete.

Four no-network regression tests pass: exact-parent and exact-agency exclusion with an older base and negative modification across pages; unfiltered transaction pagination; missing metadata does not imply exhaustion; and native OT-IDV/OT-award schema separation. The OT-IDV path is fixture-tested, not claimed live-exhaustively validated in F5. The added OtherTransactionAward path is validated against the new live Anduril history.

`validate_hydration.py` independently rereads cached raw JSON/XML bodies and recomputes exact-identity counts, net sums and hashes. Final 108-record validation passes with 412 used source-body hashes checked, 1,192 USAspending actions, 1,195 FPDS actions, 113 negative FPDS actions and no discrepancies. The raw cache additionally retains a bounded USAspending discovery response and duplicate request receipts. These validation checks concern source accounting, not proof that all real-world recent actions are public. Reporting lags, including delayed release of DoD contract information, restrict negative conclusions.

Two early exploratory USAspending generated-key probes used unverified parent guesses and returned HTTP 404. They were abandoned as discovery failures, not used as financial identity fallbacks or evidence of absence; exact identities were then obtained from the archived exact-key index. This note preserves the limitation rather than presenting those probes as valid award retrievals.

## Delivery boundaries

Heavy CSV/JSON/XML and request journals are indexed on Drive. Scripts and authored methods are suitable for lightweight GitHub delivery. No source archive, credential, signed URL, copied restricted standard or private correspondence belongs in the public dataset. No source was contacted. No purchase or permission change was performed.

## Targeted board-support and digital-safety followups

Five additional exact identities were first observed in official FPDS, then hydrated without guessing the agency or parent. All five fully reconcile on both related agency views. They supplement the 102 archive keyword candidates; they do not change the archive-screen denominator.

| Exact identity | Current net obligation / actions | Source-supported scope and limitation |
| --- | --- | --- |
| `CONT_AWD_N0017821F3008_9700_N0017819D7230_9700` | $48,049,439.87 / 131 | Basic Commerce & Industries weapon-system safety studies, investigations, audits and management support. Signed 12 May 2021; PoP starts 1 June 2021, current end 30 November 2026. This entire support award is not a board-only or autonomy-safeguards budget. |
| `CONT_AWD_W31P4Q20F0094_9700_W31P4Q18D0016_9700` | $27,999.63 / 1 | Torch software-safety missile-laboratory support, signed 16 January 2020; current PoP ended 31 May 2020. Not evidence of current operation. |
| `CONT_AWD_N6833523C0430_9700_-NONE-_-NONE-` | $146,468.00 / 1 | INSPIRD Phase I digital model-centric safety proposal. [Primary SBIR page](https://www.sbir.gov/awards/205574) and live recipient UEI D859W8HNHD86 match exactly. Safety-information tooling, dashboards and evidence search are proposed; certification success is unverified. |
| `CONT_AWD_N6833523C0444_9700_-NONE-_-NONE-` | $239,358.00 / 2 | Penta Phase I MBSE model of the Navy munition/missile safety process. [Primary SBIR page](https://www.sbir.gov/awards/205575), UEI TXQSGD76CNC4, identifies safety-panel and MIL-STD-882 artifacts as proposed model inputs. A process model is not an engagement legal governor. |
| `CONT_AWD_N0002424CS166_9700_-NONE-_-NONE-` | $1,177,083.00 / 4 | Separate Penta Phase II instrument. [Primary SBIR page](https://www.sbir.gov/awards/211829), same verified UEI, proposes AI/ML assistance with extracting safety requirements and organizing test evidence. Its money remains attached to this exact instrument. Implementation, effectiveness and board acceptance are unverified. |

The archived financial index contains zero BCI actions under the exact key, one Torch action, one INSPIRD action, two Penta Phase I actions and four Penta Phase II actions. Zero BCI observations mean absence from this index, not zero funding: live hydration finds 131 actions. The targeted source audit retains exact identifier/hash provenance while keeping legacy nine-digit DUNS values separate from current 12-character UEIs.

Schedules differ between portals. INSPIRD's SBIR page ends 26 December 2023, while the live award's current PoP ends 11 December 2023 and potential end is 10 June 2024. Penta Phase II's SBIR schedule ends 19 August 2025; the current award record ends 19 August 2027. These are explicitly unreconciled schedule presentations, not forced to match and not proof of operational activity. Financial action sums still reconcile.

The supplied [Navy FY26 Q2 forecast](https://www.navsea.navy.mil/Portals/103/Documents/NSWC_Dahlgren/Small_Business/NSWCDD_LRAE_FY26_Q2.pdf) returned HTTP 403 to this worker. No access workaround was attempted. The exact award's weapon-system safety scope is independently verified in FPDS/USAspending; a more specific B70/board association requires separate forecast-body verification. This read limitation does not block the financial reconciliation.

Full SBIR abstracts and public contact details are not republished. The public audit retains citations, exact identities, hashes and authored summaries. Full page bodies are excluded from the Drive payload because permission to rehost contractor-authored abstracts was not established; the financial API bodies remain public-source data. This is an explicit copyright boundary, not a missing upload claim.
