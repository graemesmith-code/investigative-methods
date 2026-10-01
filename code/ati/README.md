# Canadian ATI live runner

This is the independently tested lean runner used for the [completed experiment](../../research/2026-10-01/ati-live/report.md). It is not the predecessor's incomplete fixture-only build. Eleven safeguards tests passed before paid calls; all 1,234 corpus records were scored, followed by 140 coverage screens, 28 branch screens and 17 Exa searches.

The exact executed API-stage source is in [executed-v1/](executed-v1/), with [hash provenance](../../research/2026-10-01/ati-live/executed-code-provenance.json). Current top-level code adds a post-run archive safeguard: all live stages refuse to proceed without the original private ledger and its recorded call history. `make_plans.py` also uses a repository-relative path. Two new tests exercise the guard. No new API calls were made to archive these results.

## Verify offline

From the repository root:

```
python -m unittest discover -s code/ati -v
python code/ati/validate_archive.py
```

Tests use temporary fixture ledgers and make no network requests. They check caps before transport, caching, persistent budgets, uncertain failures, invalid usage, numeric response validation, bounded prices, redirects and safe continuation. The source collector and literal search-aid extractor are in [ati-cloud-preflight](../../research/2026-10-01/ati-cloud-preflight/).

## Preserve the cumulative budget

The one live ledger is `research/2026-10-01/ati-live/ledger.sqlite`. It remains in the original private execution workspace, **not this repository**, because it contains third-party article passages. The published [accounting export](../../research/2026-10-01/ati-live/ledger-accounting.json) preserves per-attempt usage, charges and request/response hashes without that text. It is not a substitute runnable cache or a fresh spending authorization.

Do not run `executed-v1/` as an alternative to the continuation guard. Do not create a new ledger or reset previous costs. Authorized continuation requires restoration and reconciliation of the original live ledger, current pricing verification, and whatever further research scope the user authorizes. The archived report is complete without another paid call.

Runtime credentials are read only through existing environment variables, sent only to exact respective API endpoints, never logged, and never included in the repository. Authenticated redirects are refused. Reservations precede transport. Failures retain full reservations; uncertain attempts block that provider. There are no automatic retries. Each provider's cap is USD10 of accounted usage and reservations; taxes/invoice fees are not verified by the API responses.

## Files

- `pipeline.py`: bounded transport, cumulative ledger, cache, seeded calibration and full ranking.
- `coverage.py`, `make_plans.py`: preserved reviewed queries and bounded Exa execution.
- `match_coverage.py`: Jev screening of coverage; outputs are not final editorial findings.
- `public_sources.py`, `ocr_release.py`, `filter_branches.py`: public retrieval, scanned-policy extraction and bounded passage screening.
- `test_pipeline.py`, `validate_archive.py`: offline safeguards and archive checks.

Only the top-level live runner should be used for future work. No scheduler, deployment, public sharing or outreach is included. No third paid model API was used.
