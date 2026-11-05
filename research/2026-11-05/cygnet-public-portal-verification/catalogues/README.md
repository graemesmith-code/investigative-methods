# Public earthquake catalogue audit

Python 3 standard-library only. No private chronology or raw data are included here. The script reads public AGS/AER and NRCan catalogue interfaces, checks AGS count and object-ID completeness, screens radius distances, and exports five audit CSVs. It never uploads or publishes files.

Required arguments: `--out PRIVATE_DIRECTORY --start UTC_START --end UTC_END --bbox SOUTH WEST NORTH EAST --pad LAT LON --toe LAT LON`. Choose a bounding rectangle that contains both search circles. Default radius is 15 km. Start/end define the retrieval envelope, not local calendar dates. Use the appropriate UTC boundary conversions explicitly.

Optional `--input PRIVATE_RAW_DIRECTORY` runs completely offline using the seven saved raw files named by the script. Offline access records indicate copies, not new HTTP responses. The supplied geographic/time parameters must describe the saved query; the script does not independently reconstruct the original query from raw responses. Preserve the original access log with the raw source directory.

Optional `--operations PRIVATE_CSV` reads private chronology, with columns:
- log_number
- start_mst
- end_mst (may be empty)
- interval_semantics (use stage_with_undated_delay for stage bounds that do not timestamp an earthquake)
- source_basis (use nominated_catalogue_origin when the input is a catalogue origin rather than an independent operational observation)

Timestamps use ISO-compatible strings. Their MST basis is explicitly assumed and unverified; UTC conversion is a fixed +7 hours, not automatic Alberta civil-time conversion. Do not feed MDT timestamps under that label. No chronology is hardcoded. Without operations, the operational CSV is header-only and all events are classified as without a close supplied entry.

Outputs include AGS events, NRCan events, tentative cross-catalogue pairs, operational reconciliation, and catalogue events without a close supplied entry. It also writes raw responses, metadata, an access log with URLs/parameters/UTC timestamps/HTTP status/byte counts/SHA256, a count summary and file hash manifest. Raw NRCan text depth is parsed independently from XML depth, preserving any unit inconsistency. The AGS M field means only industry-reported magnitude, not an identified company or known magnitude scale.

Matching is explicitly heuristic: nearest-time cross-catalogue candidates are called probable only within 10 seconds and 5 km. Operational proximity uses a configurable 600-second screen, which is not a scientific association criterion. No provider attribution or causality is inferred. Missing catalogue detections do not prove absence of earthquakes. Missing uncertainty fields do not mean zero uncertainty. AGS object IDs may change and are not permanent earthquake identifiers; EDGE IDs identify incident reports and can be shared by several earthquakes.

Completeness: the query requests at most 1000 features and verifies count and exact ID-set equality, failing rather than silently accepting truncation. For a larger result, split the requested time envelope and reconcile the resulting subsets explicitly. Current exporter requires nonempty AGS and NRCan results; raw responses remain available if that requirement fails. The tool is intended for compact, manually reviewed audits, not unattended global harvesting.

Offline validation on the retained research inputs reproduced 10 AGS records, 3 NRCan records, 3 probable catalogue pairs, 8 supplied chronology rows, and 5 AGS records without a close operational entry. Raw research inputs and chronology remain private and are deliberately absent from this methods directory.
