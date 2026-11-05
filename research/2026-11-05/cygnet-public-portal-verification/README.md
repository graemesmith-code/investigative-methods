# Cygnet public record verification methods

Preserved on 5 November 2026 as a continuation of the [AER report review](../cygnet-aer-report-review/README.md). This archive contains code and methodology only. It does not publish the private source PDFs, their text, the detailed findings memo, or private operational tables. Public query responses and privately derived tables are stored separately in the research working directory.

## The reporting question

Use public records to test three possibilities: a supportable rule violation, a weakness in the rules or their implementation that exposes the public to harm, or unusual conduct with substantial public interest. Stop short of allegations that the available records cannot establish. The method should narrow the next record request, not attempt to infer private intentions or explain every operational detail.

## Procedure and limits

1. Query the official AGS/AER earthquake feature layer and NRCan FDSN event service with an inclusive date window and a rectangle enclosing 15-km circles around the pad and lateral toes. Preserve all magnitude scales, original depths, missing uncertainty fields, origin times, source classification and incident references. Verify count and ID completeness independently. Compare catalogue rows before counting distinct events. Public incident references and industry magnitude fields do not themselves identify an operator or well.
2. Query EarthScope Station metadata across all networks within 25 km, both including and excluding restricted channels, using both legacy IRIS and current endpoints. Check temporary 2K and successor I0 as well as regional networks. Metadata, restriction annotations and data access are separate propositions. Test anonymous waveform downloads and validate the returned miniSEED IDs and time windows. Use waveform-derived MUSTANG availability metrics if the availability service is retired. A failed service is not a zero-data result.
3. Test AER public OneStop, compliance and vent-flow exports. Save failure bodies with their actual type, HTTP status and time. Do not infer no filing from an inaccessible or undownloaded dataset. Public dashboard publication thresholds are not the same as reporting thresholds. Administrative application searches do not inventory well files or restart correspondence.
4. Reconcile operational text against source-page images before assigning event times or stages. Preserve inconsistent fields rather than silently repairing them. An NPT delay can be associated with a stage without identifying a distinct earthquake. A broad operational interval can contain an earthquake time without proving continuous flow at that second. Supplied catalogue origins are not independent operational timestamps.
5. Interpolate a planned stage only between bracketing survey measured depths. Retain depth reference, survey pages, wellhead origin, horizontal datum and north-reference assumptions. Do not extrapolate missing toe surveys or equate coil-tubing measured length with survey measured depth. Treat approximate stage coordinates as screening information, not earthquake relocation.

## Reproduce the public queries

Python 3 standard library is sufficient for the public-query scripts. The optional private-PDF survey parser additionally requires PyMuPDF (1.26.6 was used). Keep an absolute PRIVATE_DIRECTORY outside this repository. For EarthScope, supply a separately stored CSV with columns label,start,end containing UTC two-minute test windows:

```sh
python earthscope/query_earthscope.py --out "$PRIVATE_DIRECTORY/earthscope" --windows-csv "$PRIVATE_DIRECTORY/waveform_windows.csv"
python earthscope/query_earthscope_supplement.py --out "$PRIVATE_DIRECTORY/earthscope"
python earthscope/summarize_earthscope.py --out "$PRIVATE_DIRECTORY/earthscope"
```

The published EarthScope query uses the study's public pad coordinate, radial search and February–March 2025 window. A rerun can return revised data. Exact URLs, query parameters, access timestamps, response bodies, HTTP status, sizes and hashes must accompany any conclusion. The miniSEED check validates record headers, IDs, sample counts and endpoints; it does not decompress amplitudes or independently detect earthquakes.

See the catalogue script's --help for its output directory and optional separately supplied operational-input table. No script signs in, contacts a person, requests restricted access, or changes an external record.

## Validation and privacy

The research run independently checked AGS row counts and IDs, metadata endpoint agreement, representative miniSEED headers, waveform-derived availability rows and response SHA256 hashes. An initial response-path suffix collision was corrected and the complete EarthScope acquisition was rerun; the superseded attempt remains only in private working storage. Successful query completeness is not complete earthquake detection or regulatory-compliance evidence.

Only an explicit allowlist of code, this README, methodology and tests should be committed. A .gitignore is a guardrail, not a privacy review. Raw pages can contain personal names, contact details and cookies; source-derived findings and queries can also disclose investigative material. Inspect every proposed file before publication.

## Primary public interfaces

- https://services2.arcgis.com/jQV6VMr2Loovu7GU/arcgis/rest/services/Alberta_Earthquakes_view/FeatureServer/0
- https://www.earthquakescanada.nrcan.gc.ca/fdsnws/event/1/query
- https://service.earthscope.org/fdsnws/station/1/
- https://service.earthscope.org/fdsnws/dataselect/1/
- https://service.earthscope.org/mustang/measurements/1/
- https://www.fdsn.org/networks/detail/I0/
- https://www.fdsn.org/networks/detail/2K_2014/
- https://www.aer.ca/data-and-performance-reports/compliance-dashboard/incidents
- https://www.aer.ca/data-and-performance-reports/activity-and-data/lists-and-activities/general-well-data
