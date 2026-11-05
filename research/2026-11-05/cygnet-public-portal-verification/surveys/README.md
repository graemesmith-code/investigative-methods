# Private PDF survey interpolation method

This script requires PyMuPDF and a private manifest mapping a well label to its drilling PDF basename, service PDF basename and expected number of planned intervals. It contains no source filenames or operational findings. Keep the manifest, source PDFs and every generated output outside this public repository.

```sh
python interpolate_pdf_surveys.py PRIVATE_PDF_DIRECTORY PRIVATE_OUTPUT_DIRECTORY --manifest PRIVATE_MANIFEST.json
python -m unittest test_interpolate_pdf_surveys -v
```

Optional --assumed-pad-latitude and --assumed-pad-longitude add approximate geographic screening coordinates. The supplied point is not validated as each wellhead origin, and the script does not establish the horizontal datum or north reference. Without these assumptions only reported offsets and TVD are available. It interpolates reported ND/ED/TVD at measured depths, not a new minimum-curvature trajectory. Planned intervals are not evidence of perforation or pumping. Source page numbers and input hashes are retained in private output. Extrapolation beyond the survey is refused. It is a source-layout-specific parser and must be checked against the rendered PDFs before substantive use.
