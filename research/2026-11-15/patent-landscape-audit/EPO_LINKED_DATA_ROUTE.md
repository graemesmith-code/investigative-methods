# Supplemental patent access tests, 15 November 2026

## Successful independent EPO route
The EPO Linked Open EP Data service is accessible in this environment, independently of the previously blocked OPS route. Its official documentation describes occasional reference/API/SPARQL use; heavier collection should use bulk datasets. It contains EP bibliographic/family/classification records, with limited non-EP identification data; it is not a worldwide full-text corpus.

Actual tests:
- GET https://data.epo.org/linked-data/data/publication/EP/3608622.json returned A1 (2020-02-12), B1 (2023-06-07).
- GET https://data.epo.org/linked-data/query using `query` URL parameter and Accept application/sparql-results+json returned valid JSON.
- Exact bounded query in test.sparql returned 32 publications from 2021-11-15 through 2026-11-15 in exact inventive CPC F41H7/005. Limit500 was not reached. No descendants, non-inventive codes, additional classes, or full-text keyword search included. This is a viable discovery route, not completeness evidence.
- Application-specific and publication-specific SPARQL responses retained. Publication response linked to representations.
- GET https://data.epo.org/linked-data/representation/publication/EP/3608622/NWB1.xml succeeded: 55,302 bytes, valid official EP XML, one description, three claims sections and 27 claim elements across languages. It is NOT 27 distinct claims. Full text now acquired for this example, not all 32 results.

Reproduce:
```
curl -G https://data.epo.org/linked-data/query --data-urlencode query@test.sparql -H 'Accept: application/sparql-results+json'
```
Use exact publication representation URLs returned by EPO records rather than inventing paths. For additional research, query selected adjacent classes and retrieve pertinent linked representations within fair-use policy; obtain bulk for sustained comprehensive collection. EPO-native results can independently check Google-indexed findings. EP publications alone exclude national-only filings and EPO does not republish all Euro-PCT A documents, so WO and national lanes remain necessary.

## USPTO export correction
Official FAQ explains 500 records is an auto-loaded batch, NOT a hard export ceiling. Scroll to the last record to load the next 500, repeat until complete; CSV max10,000 documents and result buffer max20,000. Expand '+ number' in individual family rows to include other US family documents in exported CSV. Thus original annual sharding remains a valid cautious method, but original exports must not be described as complete family inventories unless all members were expanded and count-reconciled.
Suggested method correction: 'Annual sharding avoided un-loaded 500-row batches. USPTO supports up to10,000 exported documents; only expanded/displayed family members are included. Earlier exports are candidate metadata rather than exhaustive family-document inventories.'

## Other documented routes, not acquired
EPO national full-text bulk includes FR/ES/CH/GB, ST36 XML, but official page describes ordering, subscription, credentials, and country-varying coverage. No order placed. The sample download UI returned only a JS shell to web tool; no sample retrieved.
Google Patents CSV documented top1,000 results, not all results: date/jurisdiction shards and count reconciliation required. Google BigQuery public patent dataset is worldwide bibliographic plus US full text according to Google's repository; should not be represented as worldwide fulltext.

## Sources
https://www.epo.org/en/searching-for-patents/data/linked-open-data
https://link.epo.org/web/linked_open_ep_data_user_guide_en.pdf
https://link.epo.org/web/SampleQueries_v1.2.pdf
https://www.uspto.gov/patents/search/patent-public-search/faqs
https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/national-full-text-data
https://support.google.com/faqs/answer/7049588?hl=en
https://github.com/google/patents-public-data/blob/master/tables/dataset_Google%20Patents%20Public%20Datasets.md

## Preserved official evidence
- Official EP3608622B1 XML: https://drive.google.com/file/d/1VHoiUBLmCy5CDF_eFxmjdS-4xtbvmD6Y/view
- Exact CPC query results: https://drive.google.com/file/d/17lQ-NztDdCEFHoDc0VWvITUKpnLp99uJ/view
- Publication record: https://drive.google.com/file/d/1P7bFJrBXAFL5dew_-er7hGlZJb0kwbSV/view
- Application query response: https://drive.google.com/file/d/1qNuW1W2AStihKFTrN54KpdzmIEwfpuP3/view
- Publication query response: https://drive.google.com/file/d/1Qagz0pCiyeOUuUXQkV8-UOCP-Mb7p_Xj/view
