# Technical reproduction

The included code supports repeating parts of the research. It does not recreate the missing headline, paragraph-ranking or Exa logs.

## OFAC baseline

Use Python 3.11 or later and the standard library. The original scripts are in `code/ofac/`. They expect `sdn.xml`, `entities.json` and `names.json` beside them. Those full files are excluded from this repository. The source archives inspected for this notebook contain them; a newly downloaded OFAC list may differ from the historical snapshot.

1. Obtain the exact saved SDN XML where permitted and verify SHA-256 `ab7951b5b70c22068903f1e571362f4358b90f2b983a966f322c82dffeca8170`.
2. Place it at `code/ofac/sdn.xml` and run `python3 code/ofac/prepare.py`. This makes the entity/name files and a local ZIP in `code/`; keep generated data out of Git.
3. Obtain the [exact FY2025 archive](https://files.usaspending.gov/award_data_archive/FY2025_All_Contracts_Full_20260906.zip). The saved metadata gives 1,914,255,016 bytes and SHA-256 `792f6b3ee67afd4d4e9eb7f3463a083f80efaf13279a7a1bfaba6fecfd6443da`.
4. Run `python3 code/ofac/check_screen.py` for the provided synthetic direct-match, suffix-match, unrelated-name and duplicate check.
5. Run `python3 code/ofac/screen_contracts.py /path/to/fy2025-full.zip /path/to/run-results`.

The code has fixed FY2025 date bounds. Updating a snapshot or date range creates a different run and requires a new run record. The original `prepare.py` embeds the historical retrieval date in its summary; update that field for a new retrieval and record the code change rather than reusing a misleading date.

The complete archived input is needed for an exact historical repeat. The compact NAI excerpt and summary cannot regenerate all candidates. Notebook preparation checked saved evidence and ran the original synthetic fixture with saved entity/name files; it did not repeat the full 6.6-million-row screen.

## The News API retrieval check

Use the inspected script with an existing authorised token, supplied via `THENEWSAPI_TOKEN` or the hidden interactive prompt. No token is included. Verify current account terms and quota before a new run.

```bash
python3 code/newsapi/check_newsapi_sources.py --month YYYY-MM --output /path/to/run-results
```

Replace `YYYY-MM` explicitly. The script defaults to June 2026 if omitted. It writes `newsapi_source_results.json` and `newsapi_source_report.txt`. Preserve the raw responses and actual usage alongside a run record. Review outputs for secrets and unrelated personal information before sharing. The code's generation attribution was removed from the introductory comment for this curated copy; executable logic is unchanged from the inspected source.

## Other experiments

For the completed Canadian ATI run, use the [ATI code and offline-test instructions](../code/ati/README.md) and [guide to ATI files and fields](ati-files.md). Code and evidence retain their original repository paths.

The API sample manifest documents source captures, not a complete collector implementation. The Replit references establish historical prototype publication without pinning code. The Exa CSV cannot reproduce Jev ranking or search without original inputs, prompts, code version, queries and article outputs. Missing material is listed in the [evidence inventory](../evidence/README.md).

[Home](../README.md)
