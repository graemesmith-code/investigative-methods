# Validation record

5 November 2026. Read-only public queries and private-source calculations only.

- Five synthetic tests passed: two EarthScope response-path/hash/distance tests and three survey interpolation/extrapolation tests.
- The catalogue script's offline replay reproduced the saved row counts and all five output tables. Raw inputs and private chronology are not published.
- AGS feature count and object-ID equality were checked against separate queries, rather than relying only on a page-size assumption.
- The corrected EarthScope run preserved 61 unique response paths, with byte lengths and SHA256 matching every logged body. Both Station endpoints agree on the returned channels. Eight sampled waveform bodies were checked by miniSEED v2 record headers; station/network, rates, sample counts and requested endpoints match. A second review also checked record-boundary continuity. This does not validate amplitudes or detect events.
- The optional survey parser reproduces the private geometry CSV byte-for-byte. Three repeated survey-depth records have DLS variants but matching geometry; out-of-range coordinates remain unavailable rather than being extrapolated.
- Any count is completeness under the stated query and detection/publication limits, not a complete physical earthquake count or evidence of compliance.

Only the explicit code/documentation allowlist was prepared for publication. Private originals, private input manifests, operational tables, source quotations, findings, rendered pages, raw HTML/JSON responses and response headers remain outside the public commit.
