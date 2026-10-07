# Full FARA inventory: feasibility and actual coverage

The official public interface can enumerate the needed datasets. This executor has recovered the complete rendered active and terminated registrant responses, but has **not acquired the complete foreign-principal or document inventories**. No population-wide collision or concealment claim is supported.

## What is acquired

The [active registrant endpoint](https://efile.fara.gov/api/v1/Registrants/json/Active) yielded 538 rows and the [terminated endpoint](https://efile.fara.gov/api/v1/Registrants/json/Terminated) yielded 6,552. Together they contain 7,089 distinct registration numbers. Number 5769 occurs twice in the terminated response with different termination dates; neither row was discarded. Current status is not a determination of status on a historical filing date.

The web reader exposes these responses as 68 and 769 indexed lines. Every line was recovered, overlapping lines agreed, and reconstructed JSON parsed successfully. `scripts/fara_inventory.py` reproduces these checks from saved excerpts. These are rendered text captures with whitespace normalized at line boundaries, **not byte-identical API response archives**. Completeness refers to the two rendered endpoint responses; it has not been independently reconciled to bulk data.

## Official complete-data route and blocker

The [DOJ bulk-data page](https://efile.fara.gov/ords/fara/f?p=API:BULKDATA) documents daily CSV/XML archives covering active and terminated registrants and principals, plus available document URLs. Its verified CSV download links are:

- [All registrants](https://efile.fara.gov/bulk/zip/FARA_All_Registrants.csv.zip)
- [All foreign principals](https://efile.fara.gov/bulk/zip/FARA_All_ForeignPrincipals.csv.zip)
- [All available document URLs](https://efile.fara.gov/bulk/zip/FARA_All_RegistrantDocs.csv.zip)

Each exact URL returned HTTP 403 in the executor on 7 October 2026. The web reader recognized ZIP content but cannot materialize that content type. No ZIP bytes were acquired. Failed requests are in `sources/manifest.jsonl`; a failed download is not an empty dataset. Repeated requests, alternative credentials, security workarounds and third-party paid services were not used.

The [documented API](https://efile.fara.gov/ords/fara/r/fara_ws/api/endpoints) offers registrant lists and per-registration active/terminated principal and document queries, with a five-request/ten-second limit and no authorization requirement. Browser checks of Mercury 6170's principal endpoints in JSON and HTML and its JSON document endpoint failed; Global Point 7518's HTML document list was readable earlier, while its JSON document route failed. Mercury's readable HTML document result was only the first 50 rows. Partial HTML lists are not complete document histories. Broken relative links on the newer friendly documentation route were distinguished from failures of the verified canonical endpoints.

A new-registrants-only query would miss new principals represented by existing registrants and is not an adequate replacement. The full principal inventory remains blocked at the materialization stage. A complete API fallback would require traversing both principal statuses and documents for every registration number and checking every response; it has not been executed or represented as complete. Broad official 2024 reports and selected original filings remain the acquired principal evidence.

## Resumption contract

Obtain the three exact official ZIPs through a functioning authorized public download environment and retain their original bytes. `scripts/validate_fara_bulk.py DIRECTORY` checks CRC, safe uncompressed size, CSV structure, field names, row counts, identifiers and URL counts without silently deduplicating records. Inspect actual schemas before joins. Reconcile active/terminated registration numbers against the saved API snapshot, preserving time differences and duplicate historical rows. Record publication and retrieval dates separately.

Then enumerate every principal relationship and all document types, including amendments and supplemental statements; preserve the official principal and registration identifiers. Join the declared 259 LDA client relationships to that inventory using legal names, addresses and original contracts, not names alone. Retrieve dated originals incrementally, preserving failed-document denominators. For historical obligation analysis, establish ownership/control and relevant activities on the actual filing date. Keep separate denominators for **inventory coverage**, **original-document acquisition**, **source extraction**, and **legal analysis**. Finding a catalogue row is not reading a filing; reading a filing is not resolving disclosure obligations.

This repair/inventory stage incurred no paid calls. The earlier combined Jev estimate remains $0.003035 and the conservative full-call reservation bound remains $0.15 against the authorized $15 ceiling.
