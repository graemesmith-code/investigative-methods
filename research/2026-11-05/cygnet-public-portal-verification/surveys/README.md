# Private PDF survey interpolation method

**6 November 2026 correction:** This original parser reproduces summary fields without checking whether top exceeds bottom or reconciling conflicting source fields. Do not treat unreviewed outputs as validated geometry. See the [source-supported reconciliation and impact audit](../../../2026-11-06/cygnet-discrepancy-reconciliation/README.md). The original code and historical outputs remain preserved.

This script requires PyMuPDF and a private manifest mapping a well label to its drilling PDF basename, service PDF basename and expected number of planned intervals. It contains no source filenames or operational findings. Keep the manifest, source PDFs and every generated output outside this public repository.

```sh
python interpolate_pdf_surveys.py PRIVATE_PDF_DIRECTORY PRIVATE_OUTPUT_DIRECTORY --manifest PRIVATE_MANIFEST.json
python -m unittest test_interpolate_pdf_surveys -v
```

Optional --assumed-pad-latitude and --assumed-pad-longitude add approximate geographic screening coordinates. The supplied point is not validated as each wellhead origin, and the script does not establish the horizontal datum or north reference. Without these assumptions only reported offsets and TVD are available. It interpolates reported ND/ED/TVD at measured depths, not a new minimum-curvature trajectory. Planned intervals are not evidence of perforation or pumping. Source page numbers and input hashes are retained in private output. Extrapolation beyond the survey is refused. It is a source-layout-specific parser and must be checked against the rendered PDFs before substantive use.
