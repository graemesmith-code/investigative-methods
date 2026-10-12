# Implementation handoff

## What runs now

From the repository root, run:

```bash
python code/peru_production_pilot/screen.py
python -m unittest discover -s code/peru_production_pilot -p 'test_*.py' -v
```

The runner uses only the Python standard library and the committed reviewed `comparison-input.json`. It regenerates all 100 results and summary counts. The elapsed-time field varies by run. Thirteen controls passed; see `control-test-log.txt`. This is a reproducible arithmetic/evidence-gate prototype, not an unattended document-understanding system.

`fetch_sources.py` retrieves specifically selected manifest entries, saves their bytes and checks the pilot fingerprint. Supply a genuine research contact in your user-agent, for example:

```bash
python code/peru_production_pilot/fetch_sources.py \
  --id minem-production-2023.7z \
  --output /tmp/peru-production-sources \
  --user-agent 'YOUR_PROJECT YOUR_REAL_CONTACT'
```

No contact is invented by the program. A changed hash or failed request produces a nonzero exit; changed bytes are preserved under a different name. Dynamic customs pages may change even for an identical query, so revalidation is necessary. The helper supports the saved SUNAT POST fields. It was syntax-checked; the original acquisition log records the live requests performed during this pilot, rather than claiming that every request was rerun through the packaged helper.

## Replaying government extraction

The pilot used Python `openpyxl` for XLSX and `lxml` for HTML tables, and Poppler `pdftotext -layout` for PDFs. Archive extraction used system libarchive; a normal 7-Zip-compatible extractor is also sufficient. These are optional for cached comparison. No dependency installation or network access is needed for `screen.py`.

Download the four production archives and unpack relevant workbooks into `research/pilot-raw/minem-2019-bulk/` through `minem-2023-bulk/`. The 2001–2020 archive contains both 2019 and 2020. Use the original workbook names shown in `host-detailed-rows.json`: 2019 has separate `COBRE.xlsx`, `ORO.xlsx`, `PLATA.xlsx`, `ZINC.xlsx`, `MOLIBDENO.xlsx`; subsequent years have a single production workbook. Then run:

```bash
python code/peru_production_pilot/extract_minem.py
```

This helper reproduces `host-detailed-rows.json` and `host-version-audit.json` from the unpacked inputs plus the saved annual-summary observations in `host-records.json`. It is tailored to these specific layouts. It does not update reviewed comparison gates or Western observations. The extraction ignores smelting/refining when forming concentration-stage totals to avoid double counting, strips the 2019 percent prefix from metal labels, and retains legal company/plant/process labels and monthly locators. Blank monthly cells contribute zero under the pilot convention; this must be reviewed before applying the parser to other periods. Empty source populations are missing, not zero.

SEC HTML table numbers in the inputs are document-order indices from the pilot's lxml extraction. Annual columns and footnotes still require review. Some Western values were manually transcribed from PDF text; their extraction has not been automated in the packaged code. `comparison-input.json` is the canonical reviewed input, including the unresolved Julcani 2022 dash.

## Next build tasks and acceptance conditions

1. **Source registry and versioning.** Record source class (government filing, investor report, ministry compilation or original return), retrieval time, hash and supersession relations. Preserve changed versions. Successful HTTP access alone never validates a claim.
2. **Entity and measurement contracts.** Give each operator/metal series a reviewed mine/plant population, ownership basis, calendar period, product streams, processing stage and assay/cutoff definition. Freeze these contracts before new-year comparisons. Keep unresolved fields explicit; never let an AI guess them from similar numbers.
3. **Extraction with evidence.** Return the original Spanish/English label, value, unit, period, page/table/cell and source hash. Translation must preserve uncertainty. Reject gold-equivalent, payable/sales measures, partial acquisition years and a dash treated as zero. Route uncertainty to a parked case without changing the denominator.
4. **Blind reuse and measured cost.** Apply completed contracts unchanged to new years. Measure acquisition success, extractor corrections, manual minutes, stable contract coverage, and independently reviewed alert quality. Review every alert and a random agreement sample. The 80/100 target remains unmet in this pilot; do not report cached arithmetic speed as full-system throughput.
5. **Contradiction evidence package.** Require an explicit same-assertion determination plus original submission/correction provenance before using “both cannot be true.” Keep investor inconsistencies distinguishable from two-government contradictions. Neither numerical mismatch nor equality alone establishes legal liability or truthfulness.

For the next reporting pass, prioritize La Arena and Shahuindo gold plus Antamina and Cerro Lindo concentrate coverage. Search public technical reports and environmental-file appendices for existing original-return exhibits. If those cannot close the specific gate, retain the lead as unresolved and move on. Do not turn an unresolved case into an instruction to consult a regulator.

For trade, retain the working SUNAT query as a separate acquisition capability. Do not build production-to-export or mirror-import contradiction rules until company/shipment and metal-content identity is established. Canada/UK/China routes tested here did not supply the necessary counterpart.

## Follow-up implementation additions

Two new standard-library helpers are available: `fetch_nexa_registry.py` for the observed free Nexa endpoints, and `replay_language_controls.py` for reviewed comparison controls. `fetch_sources.py --manifest` now accepts the follow-up manifest and JSON-encoded POST bodies. See [FREE_API.md](FREE_API.md) for exact commands and live-test evidence.

The follow-up adds original regulator-hosted Spanish annual-report controls for Nexa, 45 registry document entries, and source/version fingerprints. It does not close the ministry product/assay gates for the four leads. Those cases are parked. The next implementable scope is clean SEC–SMV production comparisons plus acquisition/versioning; a separate original ESTAMIN-return connector has not been established.
