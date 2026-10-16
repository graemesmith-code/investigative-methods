# Bounded acquisition and validation

Started 16 October 2026, 20:39 UTC. **Work in progress: early committed checkpoint.**

This pass acquires actual public payloads for investigating US national-security investment across quantum, autonomy/drones, sensors, cyber, space, electronic warfare and logistics. It preserves the original announcement corpus, historical collection and source registers.

## Initial bounds and decisions

- **USAspending:** FY2019–FY2026 action dates (1 October 2018–30 September 2026); DARPA contracts first, then a documented capability-text slice of DoD actions. Retain base awards and modifications, including negative obligations. Generated transaction downloads have a 500,000-row ceiling; validate each slice against the ceiling and split where necessary. Public DoD data carry a 90-day delay.
- **SBIR/STTR:** official public bulk CSVs with abstracts; normalize FY2019–FY2026 defense awards and capability-relevant DOE candidates. Bulk files contain other agencies/older awards; do not treat those as eligible or add them to security spending. API maintenance/403 does not block the published file route. Compare the two different official bulk links and report their vintages.
- **Budgets:** prioritize defense RDT&E/program exhibits and finite project documents, FY2019–FY2026 where available. Budget requests and prior-year column values retain their own measures/vintages; no inferred project-to-award crosswalk.
- **Opportunities:** one full Grants.gov daily XML snapshot, then bounded security-agency/date filtering. Funding estimates are intent, not awards.
- **Capability collections:** finite Microelectronics Commons/APFIT project documents and useful institutional research context. No whole scholarly graphs, unrelated NIH corpus, paid access, credential creation or paid model execution.

Downloaded payloads, exact HTTP URLs, retrieval timestamps, bytes and SHA-256 hashes are recorded in [the HTTP manifest](validation/http_manifest.jsonl). Validation profiles and representative records are added as parsing completes. HTTP 200 alone is not validation: inspect file signatures, open archives and parse records.

## Storage and reproduction

Initial filesystem: 32 GB overlay, approximately 30 GB free. Raw and normalized data live at `/workspace/task-data/future-warfare-investments/`, outside Git. Limit downloads to 15 GB and preserve at least 6 GB free disk. **Durability has not been established:** this is task workspace storage, with no confirmed independent archival retention. GitHub preserves scripts, manifests, checksums, samples and reporting; it does not preserve the large raw payloads. Generated USAspending links can expire; request JSON is retained so files can be regenerated, although a later snapshot may have a different checksum.

Create a Python virtual environment and install `code/requirements.txt`; run `code/acquire.py {sbir,darpa,grants}` and `code/normalize.py SOURCE` as documented by the final annex. Downloaded content is not committed. No email is sent by this worker; the parent handles the requested morning email.
