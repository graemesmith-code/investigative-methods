# Supplement: public station metadata and waveform availability

**Public waveform records covering both candidate event times were downloaded and decoded successfully.** This October 6, 2026 follow-through adds a concrete seismic source for expert review; it does not change the main report's indeterminate classifications or establish an operator's monitoring/data-release compliance.

SO7 clause 4(i) requires the applicable passive seismic monitoring information/data to be submitted to AER in real time and passive seismic data to be publicly shared through IRIS within a year of collection. Both February 2025 times are more than a year before this check. The relevant [order](https://www.aer.ca/documents/orders/subsurface-orders/SO7.pdf) is already archived. Establishing a release breach would additionally require identifying the licensee's relevant collected data and its collection/release history; this availability check does not supply that evidence.

## Networks and selection

The [FDSN I0 registry](https://www.fdsn.org/networks/detail/I0/) says the Scientific Induced Seismicity Monitoring Network was migrating from 2K to I0, with records fragmented across both codes. We therefore checked both, plus the regional RV network, using the published [EarthScope station service](https://service.earthscope.org/fdsnws/station/1/). The first query used the fixed event-cluster centre 52.215 N, −113.957 longitude, a one-degree radius, and metadata epochs overlapping February 22–25, 2025. Public-only channel queries returned no matching 2K or I0 records and returned RV metadata.

A second public metadata-only query included metadata describing restricted/partly restricted stations across each entire 2K and I0 network. It returned five 2K stations (nearest approximately 466 km) and 67 I0 stations (nearest approximately 200 km), none near this cluster. This does not mean no relevant industry station existed, no data were submitted, or data were withheld. Metadata may be incomplete, relocated between codes, or differently registered. No restricted waveform access, credentials, embargo bypass or outreach was attempted. The HTTP 404 responses from the initial queries are retained in the acquisition log as query outcomes, not characterized as access denials or regulatory failures.

RV returned five stations with HH seismic channels within the radius. Ranked solely by distance to the fixed cluster centre, **RV.REDDA** was nearest at **5.406 km**, followed by ROCKA 61.314 km, BASHA 74.563 km, BSLNA 101.086 km and HACKA 104.683 km. REDDA's metadata position is 52.179264, −113.903442, elevation 892 m, sensor Trillium Compact 120. This station was selected by proximity, not company affiliation. Its data cannot be assumed to be the candidate wells' licensee-owned monitoring data.

## Small waveform download and validation

The public [dataselect service](https://service.earthscope.org/fdsnws/dataselect/1/) returned the following unauthenticated HTTPS downloads for `RV.REDDA..HH?`, each with a matching StationXML instrument-response query:

| Catalogue event | Requested UTC interval | MiniSEED bytes | Decoded records |
|---|---|---:|---|
| ca2025dscb, February 22 at 14:05:18 | 14:04:18–14:07:18 | 83,968 | HHE, HHN, HHZ; 18,001 samples each, 100 Hz |
| ca2025dwzq, February 25 at 06:32:36 | 06:31:36–06:34:36 | 86,528 | HHE, HHN, HHZ; 18,001 samples each, 100 Hz |

All six traces cover the stated catalogue origin time, decode as STEIM1/int32, have no detected gaps in their downloaded windows, and match instrument response metadata at the relevant time. The raw values remain digital counts; response metadata's M/S input units do not mean the downloaded samples have already been converted to velocity. Parsing uses ObsPy's documented MiniSEED reader, with no filtering, response removal, phase picking or magnitude estimation.

This validates **current public availability and readable time coverage**, not waveform signal attribution to either earthquake, sensor timing accuracy, original release date, operational detection/notification, or the magnitude actually available to an operator. One station alone and this limited check cannot resolve the February 22 ML/MLy disagreement. The records could support qualified subsequent review with appropriate calibration, magnitude method and additional stations. They cannot provide pumping times, historical operator identity or restart consent.

## Reproduction and preservation

Exact requests, retrieval timestamps, HTTP outcomes, sizes and SHA256s are in `sources/manifest.jsonl`; raw metadata and both MiniSEED files are under `sources/waveforms/`. The deterministic result is `results/waveforms/availability-summary.json`. `scripts/waveform_availability.py` is explicit live free acquisition; `scripts/inspect_waveforms.py` is offline parsing and coverage validation. To reproduce only the supplement:

```bash
python -m pip install -r requirements.txt -r requirements-waveforms.txt
python scripts/inspect_waveforms.py
python scripts/verify_sources.py
```

The original main report and prior bundle remain preserved through Git and Library version history. The supplement and its small raw downloads are included in the updated version of the same Library ZIP. No additional Jev or other paid call was made. Independent Jev audit confirmed the 15-call/11,858-token/US$0.000507 estimate and the limited interpretation; completed V2 live replay is now disabled, while offline reevaluation remains available.
