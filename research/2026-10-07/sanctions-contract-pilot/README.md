# Sanctions/USAspending pilot — access checkpoint

7 October 2026. **Incomplete: no candidate findings or Jev evaluations produced. New Jev spend: US$0.** Alberta remains parked; its separate prior US$0.000507 is excluded.

The existing private repository was clean at starting commit fef7c60. No AGENTS.md or SKILL.md was found in the checkout; workspace .agents and .codex directories were empty. The prior OFAC report and selected JSON evidence exist under evidence/ofac, but the original ZIPs are absent. Counts in that report have not yet been independently recomputed from original evidence.

Library search resolved all three requested originals. The current supported download helper, with exact selection of those three files, stopped at an HTTP 401 during its hosted-app tools lookup. No bytes were materialized. An initial missing companion was installed from the current skill before this authentication failure. No access settings, credentials, or TLS protections were changed. The parent session must restore supported Library transfer or supply the recovered original bytes through an authorized upload route. Do not redownload the full contract archive.

Existing JEV_API_KEY passed authenticated GET /v1/models (HTTP 200). TYPESAFE_API_KEY is absent. No credential value was displayed or saved. Fresh public API/model documentation and the models response are archived with hashes. Version jev-1.13.0 remains US$0.042 per million input tokens, with free outputs and maximum 64,000 input tokens per request.

Budget design: separate new ledger, US$9 internal cap and US$10 authorization ceiling; reserve US$0.003 per request (64,000 × US$0.042 / 1,000,000 = US$0.002688). Every failed or uncertain request retains its reservation; no automatic retries, redirects, or other paid services. This bound is supported by current documentation, but the sanctions-only offline adapter now passes six failure-control tests; live transport and synthetic model calibration remain required before paid calls. Do not execute disabled Alberta scripts or use its old ledger.

The documented Jev interface returns typed decisions (noul, choice, score), not free-form evidence extraction. Continuation must use code-generated, passage-anchored candidate choices with an insufficient-evidence option; Jev selections cannot invent a relationship or serve as verification.

Next: materialize and hash originals; inspect ZIP contents and reproduce subset counts; construct source-linked dossiers; verify historical designations and the NAI calibration from official sources; test the sanctions-only adapter and small controls; run bounded triage; expand only supported identities (maximum three candidates and five validated names each). Both stages remain pending. The user permits an empty credible shortlist. No conclusion about payments, authorization, or sanctions violations is made.

See [technical annex](technical-annex.md) and [source manifest](sources/manifest.json).

## Follow-up checkpoint

The one bounded retry after refreshed exact Library searches again failed with HTTP 401. See recovery-status.json for the exact route and error. Both ZIPs remain inaccessible. The repository report and derived excerpts are readable, inventoried with hashes; they do not replace missing original records. Git object-path history was also searched and recorded.

Six offline tests pass for the Jev-only adapter: provider restriction, retained uncertain costs and retry blocking, cap enforcement, success caching and rounding, invalid usage rejection, and literal passage checking. These tests make no network calls and do not measure model accuracy. Run `python -m unittest discover -s research/2026-10-07/sanctions-contract-pilot/scripts -p 'test_*.py' -v` from repository root.

[NAI partial calibration](NAI-calibration.md) now documents independently refreshed official records, separate from the unavailable immutable baseline. All requested original ZIP contents and full candidate dossiers remain blocked; no claimed 13-candidate dataset was reconstructed from memory.

## NAI calibration result

Current official API history now confirms the zero-obligation vehicle termination and eight child delivery orders dated 13–14 December 2023. Gross positive obligations $36,309.46, negative adjustments −$15,662.32, net $20,647.14; no payments established. All eight child records identify the same NAI recipient/UEI. Dated official-business authorization is a concrete possible explanation; no breach is concluded. See NAI-calibration.md for the full table, coverage limits, and missing instruments. No paid Jev evaluation occurred.
