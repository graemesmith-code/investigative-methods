# Reproducing this supplement

Use the private repository, including preserved October 6 source files at baseline commit e3986e42a96ab70cbd1ed88e9123fecacbb59fb3. The reading ZIP is an evidence summary, not a complete offline corpus.

Python 3 is used. `review.py` additionally requires PyMuPDF (fitz) and pyproj; this run used PyMuPDF from the existing environment and pyproj from `/tmp/alberta-python`. No paid services are required. From the repository root:

```sh
python research/2026-10-07/three-well-records/scripts/st1_extract.py
python research/2026-10-07/three-well-records/scripts/alias_monthly.py
PYTHONPATH=/tmp/alberta-python python research/2026-10-07/three-well-records/scripts/review.py
python research/2026-10-07/three-well-records/scripts/validate.py
```

`review.py` re-extracts PDFs, reconstructs current all-leg selections, recomputes nine surface distances using the prior GRS80 ellipsoid, checks actual saved IAR zero-count text, and inventories retained source bytes plus nine frozen prior inputs. `validate.py` checks acquired-source hashes, attachment/index byte sizes, aliases, returned NRCan XML fields, full inventory, prior input hashes and coordinate results. The inventory is a post-acquisition audit, not an independent timestamp or proof that unsuccessful responses were complete.

## Exact public queries and pagination

Every `sources/pubdocs-*.request.json` is the saved read-only JSON request for `https://www1.aer.ca/wsPubDocs/search`. The adjacent response is the same basename with `.request` removed. This includes the second pad-location page (offset100), acquired interactively. To reproduce that request, POST the complete saved JSON with `Content-Type: application/json` and normal certificate verification. Do not substitute an unpadded licence: these returned zero while padded identifiers returned events. The published client field selection is retained in `sources/pubdocs-main.js`; `scripts/pubdocs_query.py` regenerates the initial queries. Live indexes can change.

`results/public-document-index.json` contains the 15 download URLs and event/activity attachment metadata. `download_pubdocs.py` only downloads public attachments. `sources/manifest.jsonl` logs ordinary HTTP source acquisition, including corrected NRCan identifiers; its detailed URLs preserve optional query parameters. The initial failed NRCan request returned a schema diagnostic; the corrected requests returned one origin and magnitude, zero picks/arrivals. No completeness inference follows.

`results/pad-event-review.json` is an exploratory metadata summary of the two saved location-query pages, not evidence of exact pad membership or missing consent. The corporate and catalogue PDF text extractions are reading aids; original PDFs are authoritative. Survey drawing OCR was not used to reconstruct a trajectory.

## Failed access and retained limitations

The IAR and Tableau diagnostic scripts are optional acquisition history, not part of offline validation and not invitations to retry access denials. The standard Tableau client stopped at403; the IAR browser stopped at a certificate error. Some intermediate IAR raw responses were overwritten during troubleshooting: their log entries remain but those bytes cannot be reconstructed. Final responses are inventoried; no absence finding depends on failures. Do not disable TLS verification or bypass warnings.

Earlier snapshots remain untouched. The October2025 identifier updates do not date physical geometry changes. The original licence surface points reproduce the earlier proximity screen; current bottomhole points cannot be presented as verified February2025 stage positions. All packets remain indeterminate.
