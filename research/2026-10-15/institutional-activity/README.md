# Can aggregate activity produce newsroom leads before military operations?

**Selected follow-up completed through measurement screening:** [Satellite night-light pilot](satellite-nightlights/README.md) — all 18 uploaded NASA files verified; all three historical cases are unscorable under the original quality rules. Exploratory mask changes recover two June dates but only one date in each winter case. No brightness anomaly or warning accuracy is claimed. [Bounded next step](satellite-nightlights/NEXT_STEP.md).

**15 October 2026 — exploratory test completed; no validated warning signal.**

We tested a cheap version of the “Pentagon Pizza” idea using public Metro passenger counts. The hypothesis was that unusually late departures near the Pentagon might supply a reporting lead before a major operation. We used station totals only: no phone identifiers, individual trips, employee identities or movement histories.

The first rule did not flag either Iran pre-operation window. The Venezuela window was unscorable under the chosen holiday and traffic-volume rules. This is a negative finding for one rail-departure measure, not a refutation of every possible aggregate activity signal.

## What happened

| Case | Window result | Preceding Friday evening station entries | Earlier comparable-Friday median |
|---|---|---:|---:|
| Iran, June 2025 | No flag; two eligible evenings | 245 | 297.5 |
| Venezuela, January 2026 | Unscorable; holiday and low volume | 133 | 250 |
| Iran, February 2026 | No flag; three eligible evenings | 314 | 250 |

The rule examined the share of Pentagon-station entries occurring from 19:00 to midnight relative to 15:00 to midnight. Entering a station means boarding the rail system, so this is a possible departure-from-area proxy. It is **not building occupancy or a count of workers**. We compared earlier same weekdays and the changes at Pentagon City, Rosslyn and Crystal City.

We set the threshold using 2024, then applied it unchanged from January 2025 through March 2026. It flagged **23 of 259 eligible dates**, grouped into 18 alert episodes. The interval contained 455 calendar dates; 196 were excluded or lacked a valid score. Other military actions and causes were not exhaustively labeled, so the 23 flags are **background alerts**, not 23 proven false predictions.

The public source also has a **seven-day publication delay**. Regardless of statistical performance, it cannot itself supply same-night leads.

## Lessons worth keeping

1. **Check price, archive and publication latency before building.** A free, downloadable archive is not necessarily a timely signal. The Metro archive is useful for a retrospective benchmark but fails the immediate newsroom use case.
2. **Name the thing actually measured.** Passenger passages, cars, brightness and mobile-device indices are different measurements. None automatically means “an extra thousand people at work.” Drivers, people staying all night and people using other exits can be invisible to a particular proxy.
3. **A rising fraction can hide a falling count.** Before the June 2025 case, Friday's late-departure share rose while the number of evening entries fell. Inspect the numerator and denominator, not only the anomaly score.
4. **Keep three clocks separate.** Record observation time, publication time and operation/first-public-report time. Metro's service day includes the early hours of the following calendar day. A Friday daily total can contain Saturday observations. “June 22 in Iran” was June 21 in Washington.
5. **Count the quiet dates.** A few famous events can make almost any indicator look impressive. Apply a fixed rule across the whole eligible interval and count the reporting workload it creates. An incomplete event registry cannot establish precision.
6. **Controls can be disrupted too.** Construction closed Crystal City on the February 2026 operation date. Holidays, weather, shutdowns and changes in service can create or erase apparent signals.
7. **Do not turn the brief into an arbitrary exclusion.** We imposed a minimum of 1,000 afternoon-plus-evening passages to focus on broad traffic. That was our analysis choice, not a source privacy requirement or a count of distinct people. It made Venezuela unscorable. Future thresholds need a measurement/sensitivity rationale; do not describe an excluded case as a miss or a null result.
8. **Preserve negative findings without tuning them away.** The cases were already known when the hypothesis was chosen. Fixing the threshold before inspecting case scores helps, but is not independent preregistration or prospective validation. Do not keep changing windows and controls until these three cases “work.”
9. **Test sensitivity without inventing people.** Synthetic extra rail passages can check whether the statistic responds to large changes. They do not show that a staffing increase would produce those passages.

## What is and is not established

- **Established:** a public, zero-data-fee archive; reproducible acquisition; complete date rows in the selected exports; an executable exploratory test; no qualifying flag in either scored Iran window.
- **Not established:** a useful military predictor, a complete event/disruption calendar, reliable false-positive or detection rates, a conversion to employee numbers, or a cheap feed satisfying the required timeliness.
- **Decision:** do not deploy this Metro measure as a standalone warning system. Preserve it as a benchmark and choose a genuinely different measurement or a bounded supplier-feasibility test.

## Reproduce or inspect

- [Technical specification and limitations](TECHNICAL.md)
- [Original three next-test options](NEXT_TESTS.md) — **satellite test selected; measurement screening completed; road counters and supplier feasibility not launched**
- [Exact first-pass results](exploratory_results.json)
- [Two-page results report](institutional-activity-pilot-results.pdf)
- [Complete pilot kit: original exports, cleaned CSV, code and provenance](institutional-activity-pilot-kit.zip)

The kit contains 14,688 station/date/time-selection rows, covering four stations, three selections and 1,224 dates from January 1, 2023 through May 8, 2026. The end date is the exported view's selection, not an assertion that the underlying archive ends there. The fee was **$0**, excluding analyst/setup time.

After unzipping, from the kit directory:

```sh
python3 code/clean_and_check.py
python3 code/exploratory_backtest.py
```

Both scripts use Python's standard library. No paid API calls are needed to reproduce the included historical results.

## Main sources

- [WMATA ridership portal](https://www.wmata.com/about/open-data-hub/ridership-data.html)
- [WMATA data definitions, publication lag and service-day convention](https://www.wmata.com/content/dam/wmata-com/migrated-assets/initiatives/ridership-portal/upload/rdp-metadata.pdf)
- [February 2026 ridership snapshot: construction and weather](https://www.wmata.com/content/dam/wmata-com/migrated-assets/initiatives/ridership-portal/upload/February%202026%20Ridership%20Snapshot.pdf)
- [November 2025 snapshot: federal shutdown dates](https://www.wmata.com/initiatives/ridership-portal/upload/November-2025-Ridership-Snapshot.pdf)

The kit's `SOURCES.txt` and `event_registry.csv` preserve the remaining official references and event-date caveats.
