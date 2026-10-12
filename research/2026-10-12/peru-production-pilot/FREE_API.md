# Tested free Nexa Peru document registry

Observed on Nexa Peru's [results centre](https://riperu.nexaresources.com/es/informacion-financiera/centro-de-resultados/) and [annual-report page](https://riperu.nexaresources.com/es/informacion-financiera/memorias-anuales/). Endpoint definitions were read from the site's [public JavaScript](https://riperu.nexaresources.com/wp-content/themes/mziq_nexa-resources_ri/js/file-manager/mziq.cmsint.js?v13). No authentication or paid subscription was used.

## Exact requests

POST, `Content-Type: application/json`:

```text
https://api.mziq.com/mzfilemanager/company/fa653160-ea78-4cd6-897a-335d2c6c4b9f/categoryInternalName/document/language/years
```

```json
{"categoryInternalNames":["annual_reports","results_center_informes_de_governanca"],"language_code":"es_ES"}
```

Observed HTTP 200, returning available bucket years 2014–2026.

POST, same headers:

```text
https://api.mziq.com/mzfilemanager/company/fa653160-ea78-4cd6-897a-335d2c6c4b9f/filter/categories/year/meta
```

```json
{"year":2023,"categories":["annual_reports","results_center_informes_de_governanca"],"language":"es_ES","published":true}
```

Observed HTTP 200; `data.document_metas` contains public document IDs, title, download URL, language and dates. Six bucket probes returned:

| Bucket | Document entries |
|---|---:|
| 2019 | 6 |
| 2020 | 8 |
| 2021 | 8 |
| 2022 | 8 |
| 2023 | 8 |
| 2024 | 7 |
| Total | 45 |

All 45 IDs and download URLs were distinct across these responses. These are documents, not 45 comparable production records. Copies are in [followup-registry](followup-registry/).

## Reuse now

From the repository root:

```bash
python code/peru_production_pilot/fetch_nexa_registry.py \
  --year 2023 --year 2024 --output /tmp/nexa-registry \
  --user-agent 'YOUR_PROJECT YOUR_REAL_CONTACT'
```

The client performs sequential public requests, preserves changed responses as separate versions and records bodies, hashes, access results and latency. The packaged client was actually live-tested with the years endpoint and the 2023 bucket: HTTP 200 for both, eight documents in the latter, 1.1146 and 0.8833 seconds on that run. This small sample does not measure extraction throughput or AI cost.

Retrieve a specifically reviewed source from the follow-up manifest:

```bash
python code/peru_production_pilot/fetch_sources.py \
  --manifest research/2026-10-12/peru-production-pilot/followup-source-manifest.json \
  --id nexa-peru-smv-annual2021.pdf --output /tmp/peru-originals \
  --user-agent 'YOUR_PROJECT YOUR_REAL_CONTACT'
```

The source fetcher supports JSON POST for these registry entries and URL-encoded POST for the original SUNAT entries. It retains changed bytes and returns a nonzero exit if the saved evidence hash no longer matches.

## Required content checks

- `file_year` is a registry bucket, not a reliable production period. The 2023 annual report appears under 2024; fourth-quarter 2023 results appear under 2023 despite a February 2024 publication date.
- `language_code=es_ES` does not certify Spanish content. The downloaded 2023 main-indicators document is in English.
- Titles can refer to Atacocha rather than Nexa Peru/Cerro Lindo. Never use the same registry company ID as proof of the same mining operation.
- A publication date can be a placeholder. Use the document itself for the assertion period and retain the retrieval/version date separately.
- A URL on the company's registry is a company publication. It is not proof of submission to SMV or MINEM. Our SEC–SMV controls separately use original SMV-hosted reports; both retrieved Spanish reports are preliminary versions pending shareholder approval.

The API supplies a reusable acquisition route. The reviewed production assertion contract remains separate.
