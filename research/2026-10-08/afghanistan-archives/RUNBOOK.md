# Reproduce and continue in the cloud checkout

## Offline reproduction

From repository root, Python 3 stdlib plus Poppler (`pdftotext`/`pdfinfo` 25.03.0 in this run) suffice. No Python package installation is needed.

```sh
python research/2026-10-08/afghanistan-archives/code/validate.py
python research/2026-10-08/afghanistan-archives/code/pilot.py
python research/2026-10-08/afghanistan-archives/code/discovery.py
```

`pilot.py` without `--download` uses cached files and refuses missing cache. It rewrites derived results; its network count then reflects that replay. Preserve the original download log as the retrieval record. `discovery.py` makes candidate contexts and a deliberately assistant-selected reading packet. It is not an automated contradiction or novelty judge.

For a fresh acquisition, review `sources/pub-robots.html`, the current catalogue and terms first, then use `pilot.py --download`. Requests are serial, spaced at least 1.2 seconds, restricted to Publications Canada, maximum 20 acquisition requests per invocation, 12MiB per body and 60MiB downloaded per invocation. It asserts the observed 14+1 selection; a changed catalogue requires review, not automatic expansion. These limits exclude prior/manual source probes and HTTP redirects and are not a global network meter. Do not repeatedly rerun failed downloads. The current run made 18 logged catalogue/body retrievals including the initial archive notice and its explicit continuation; auxiliary HTML/search/robots/JavaScript and news-search checks are separate. All downloads have already completed; no further batch is running.

Optional local quality probe (Tesseract 5.5.0 and `pdftoppm`):

```sh
python research/2026-10-08/afghanistan-archives/code/ocr_lowtext.py
```

This performs OCR on only the 25 flagged low-text pages and preserves the result separately. Eleven OCR outputs exceed 80 characters; review shows cover/title text and two map pages among these. That is not evidence of 11 substantive missing pages. The machine-readable primary page field `ocr_performed=false` describes the primary Poppler extraction; join the separate OCR file on document/PDF page for the supplemental OCR.

`source_check.py` and `lac_probe.py` record the exact source URLs and public search payload used. **Do not replay them blindly:** they can contact live services and do not implement a persistent cross-run denial blocklist. The recorded CJOC 403 and LAC direct-PDF 403 are stop points. Do not retry or route around them. `lac_probe.py` uses only an anonymous UI-issued anti-forgery token in memory, no account, credential creation or authentication. Saved source HTML has anonymous session tokens removed; raw versus sanitized hashes are recorded.

## Model experiment design — not authorized to run on paid APIs

Use the ten-page `results/review-packet.json` first, not the whole archive. Require structured outputs with claim, exact source page, metric definition, geography, time period, projection/observation distinction, competing explanation, receipt evidence, prior-publication match and abstention. No source-page support means abstain. Evaluate against the explicit benchmark-change negative control, the already-covered school/outcome control and the unresolved acreage-definition case. Reviewer must inspect source images before accepting numeric/table claims. Model agreement is not corroboration.

The packet is 41,511 characters: approximately **8,302–13,837 input tokens**, using 3–5 characters/token, before instructions. At an entirely hypothetical $0.10/million input and $0.40/million output, 3,000 output tokens would make a pass about **$0.0020–$0.0026**, excluding instructions/retries. These are arithmetic illustrations, not current vendor prices, a model choice or a spending authorization. The 2,234,861-character full corpus is roughly 447k–745k input tokens. The same hypothetical one-pass input plus 30k output would be about $0.057–$0.086. Refresh actual pricing and tokenize the final payload only after explicit paid-API authorization. No paid calls were made; prior Jev caps do not transfer. This assistant's reading and judgments are platform analysis, not a demonstrated result from a cheap external model.

Local ordinary code already supplies enumeration, hashes, deduplication, page extraction, OCR triage and lexical retrieval without inference fees. Access to relevant bodies, disciplined claim matching and expert review currently matter more than token price. Human/platform/cloud costs were not measured or claimed to be zero.

## Next checkpoint

Start with acquisition queue rank 1: at most three cited evaluation/monitoring bodies, 20MB; compare identical metric definitions before searching for receipt evidence. In parallel conceptually, but without spawning agents or bulk scraping, review a bounded LAC metadata sample only if ordinary accessible bodies can be reached without the denied route. No new paid budget, personal records, outreach, applications or credentials.

Stop after that batch if there is no new source class or same-scope discrepancy beyond known public evaluation findings. Escalation would need a specific acquired document and a concrete missing link, not a large speculative crawl. The saved branch provides continuity when the laptop closes; no background daemon, scheduled job or future notification was installed.
