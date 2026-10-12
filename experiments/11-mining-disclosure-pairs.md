# Can a mining company give two governments incompatible facts?

Four of ten proposed mining-project comparisons survived a check of whether they describe the same fact. **All four inspected samples agree within their permitted interpretations. No contradiction was established.** The useful result is a small, defensible starting set for a wider search.

The reporting opportunity is straightforward: if two company statements concern the same project, period and measurement, and cannot both be true after allowing for their stated precision, at least one representation is wrong. A reporter need not establish which one before investigating the inconsistency. That reasoning does not establish intent, fraud, or which filing should be corrected.

| Comparison retained | What can be checked | Why a future mismatch could matter |
|---|---|---|
| [Southern Copper, Peru](../code/mining_claims/cases/peru-2023.json) | Fine molybdenum production in 2023 from Toquepala and Cuajone combined | Incompatible output statements could undermine both investor disclosures and the production statistics used to oversee mining. Production alone does not establish unpaid tax. |
| [Endeavour, Ity, Côte d’Ivoire](../code/mining_claims/cases/ity-2024.json) | 2024 royalties from three project companies and both royalty components | An incompatible total could raise questions about a major mine's claimed public contribution. Currency conversion and the full company population must be checked first. |
| [Barrick, Kibali, DRC](../code/mining_claims/cases/kibali-2023.json) | Barrick group's 45% economic interest in 2023 | Conflicting economic ownership statements would matter to investors and scrutiny of control over the mine. Group ownership is different from direct registered shareholding. |
| [IAMGOLD, Essakane, Burkina Faso](../code/mining_claims/cases/essakane-2023-2024.json) | Historical 90% company / 10% state interest | A conflict about the state's economic share could be consequential. The form has two possible dates; a contradiction must survive both interpretations. |

The host-country material is not uniformly a tax return. Eight of the original ten candidates use national Extractive Industries Transparency Initiative reporting, a government-linked process involving companies and civil society. The surviving cases use company-attributed statements rather than assuming a government receipt figure is a company declaration.

Six cases were parked: Paracatu in Brazil, Sabodala-Massawa in Senegal, Fekola in Mali, QMM in Madagascar, Lumwana in Zambia and Asanko in Ghana. Their unresolved questions concern dates, company scope, payment categories, currency methods or who adopted a reconciled figure. A large numerical difference did not rescue a case whose meaning remained uncertain.

## What is ready

The [implementation starter](../code/mining_claims/README.md) replays the four inspected samples and can re-extract the host workbook cells and Peru's Western production table from the exact downloaded versions. It includes a separate specification for each case, saved evidence locations, a downloader, and tests designed to prevent false alerts. It makes no paid model calls.

The next work is to automate the remaining Western extractions, collect adjacent reporting years, and approve each new period and source version. Translation can help locate corresponding claims in different languages; it should preserve the original sentence and its qualifications. The numerical comparison itself does not need a language model.

Read the [full audit and rejected cases](../annexes/mining-claims-audit.md) for the evidence and reasoning. The [research archive](../research/2026-10-12/mining-claims/README.md) preserves the original ten-candidate discovery, download checks and calculations. Its earlier recommendations are superseded by the audit.

Research and implementation groundwork saved 12 October 2026.
