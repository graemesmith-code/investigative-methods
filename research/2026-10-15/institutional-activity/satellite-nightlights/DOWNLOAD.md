# Initial NASA science files

The user has completed Earthdata sign-in. Download these two files in your own browser, then upload them to the conversation. Together they are about 67.2 MiB. They test the scientific file format, observation times and quality screening; they are not enough by themselves for a backtest.

- [VNP46A1: VNP46A1.A2025171.h10v05.002.2025172102335.h5](https://data.laadsdaac.earthdatacloud.nasa.gov/prod-lads/VNP46A1/VNP46A1.A2025171.h10v05.002.2025172102335.h5) — 43.3 MiB.
- [VNP46A2: VNP46A2.A2025171.h10v05.002.2025179160943.h5](https://data.laadsdaac.earthdatacloud.nasa.gov/prod-lads/VNP46A2/VNP46A2.A2025171.h10v05.002.2025179160943.h5) — 23.9 MiB.

If NASA asks, use the account you just created/signed into. Do not share passwords or tokens in chat.

The complete nine-date first-stage sample has 18 files (561.4 MiB), listed in `download_manifest.json`. Baseline and positive-control data are additional and have not yet been requested. The bounded local Python downloader defaults to the pair above; `--all` selects the 18 listed files. Its authenticated transfer has not been validated.
