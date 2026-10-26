# Post-freeze correction: Skydio government-exception comparison

**26 October 2026, independently checked after the 09:09 editor freeze.** An independent Astra reader identified a real scope problem in the generated comparison field. The editor verified the parser, all eight archived/live source bodies and the three decisive official web pages. This addendum preserves the earlier frozen files rather than silently replacing them.

## Finding and correction

`build_registers.py`, line 101, searches the **whole document** for government-exception phrases. The resulting `version_comparison` field does not isolate the weapons clause or resolve legal priority. January's “government exception present” label is therefore true at document level but unsuitable as a clause-change timeline.

The January–3 February 2026 archive has a government-action exception in **§1.3, Conditions of Use**, while **§6.3, Use Restrictions**, contains no express exception locally. The broader clause cannot be ignored. The exception is visible in the [official January archive](https://www.skydio.com/legal/terms-and-conditions-enterprise/2026-01-01-2026-02-03); its legal interaction with §6.3 is not resolved by string matching.

The earlier memo's observation that the weapons **passage** returns to older wording is supported. Its wording about exceptions disappearing and returning must, however, be narrowed: it does not establish that government permission was legally withdrawn and later restored. The editor's frozen ED-006 and review-log shorthand require the same qualification. The editor's earlier final-record acceptance did not identify this parser-scope limitation.

## Clause-local readback

All locators below refer to extracted source lines preserved in the private working record. Source hashes and clause identifiers appear in the companion JSON. Every inspected weapons passage was also checked against the original HTML, whose hash matches the frozen source register.

| Public archive label | Weapons-passage line | Exception stated locally? | General Conditions of Use exception |
|---|---:|---|---|
| 29 Jun–20 Sep 2022 | 37 | No | No matching exception found in inspected conditions |
| 21 Sep 2023–11 Jun 2025 | 88 | No | No matching exception found in inspected conditions |
| 12 Jun–7 Sep 2025 | 87 | No | No matching exception found in inspected conditions |
| 8 Sep–31 Dec 2025 | 72 | Yes | §1.2, line 9 |
| 1 Jan–3 Feb 2026 | 86 | **No** | **§1.3, line 12: yes** |
| 4 Feb–27 Apr 2026 | 71 | Yes | §1.2, line 9 |
| 28 Apr–16 Jun 2026 | 69 | Yes | §1.2, line 9 |
| Live page at 26 Oct 2026 cutoff | 84 | Yes | §1.2, line 15 |

The [September–December page](https://www.skydio.com/legal/terms-and-conditions-enterprise/2025-09-08-2025-12-31) and [February–April page](https://www.skydio.com/legal/terms-and-conditions-enterprise/2026-02-04-2026-04-27) expressly place government-action language in the weapons list item. The January page does not; it still carries the general exception. Archive labels are not proven customer acceptance dates, and unsupplied date intervals are not filled by inference.

## Required integrated wording

> Skydio's public archives vary in where government exceptions appear. The January–early February 2026 weapons clause lacks the local exception found in the adjacent archived versions, but its general Conditions of Use still contains a government-action exception. The text does not establish a withdrawal and restoration of government permission, nor which terms governed a particular military customer.

For a corrected comparison table, retain separate fields for **document-wide matching phrase**, **exception in the weapons passage**, **general-conditions exception locator**, and **legal interaction/applicability unresolved**. Do not interpret the old one-field output as a legal effect. The original normalized findings LC02–LC04, current-clause observations and broader no-deployed-veto conclusion do not need reversal on this evidence.

## Distribution and status

This addendum is authored analysis and metadata only; original source bodies remain private working material. No publication action was performed. Both original licence and editor whitelist payload sets remain byte-for-byte unchanged, as verified again for this addendum. The coordinator must carry this correction alongside the frozen record and narrow any integrated timeline before release. Cost: $0.
