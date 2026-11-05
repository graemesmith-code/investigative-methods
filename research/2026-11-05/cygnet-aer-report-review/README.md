# Cygnet AER report-review methods

Preserved on 5 November 2026. This is a **code and methodology archive**, not a publication of source records or investigative findings. It follows the earlier [Alberta seismic/fracturing screen](../../2026-10-06/alberta-seismic-injection/README.md).

The scripts support a local, page-cited review of twelve supplied PDFs. They extract embedded PDF text, create navigation aids and check split-file boundaries. They do not establish causation, regulatory compliance, operator knowledge or restart authorization.

## Contents

- [Method and interpretation limits](METHODS.md)
- [PDF extraction and keyword index](code/extract_aer.py)
- [Raw daily-completion row index](code/extract_completion_chronology.py)
- [Service-report field and comment index](code/extract_service_timeline.py)
- [Split-boundary comparison](code/check_split_boundary.py)
- [Synthetic smoke tests](tests/test_methods.py)
- [Execution and validation record](VALIDATION.md)

The four analysis scripts are preserved as executed. The synthetic tests were added for this archive and do not contain actual source records. The scripts are small, dataset-specific review aids, not production parsers.

## Reproduce locally

Use Python 3.12 and PyMuPDF 1.26.6, the versions used in the archived run. Install dependencies in an isolated environment:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Keep source PDFs and generated outputs **outside this public repository**. With `ARCHIVE` set to the absolute path of this directory, and `SOURCE` and `WORK` set to private local directories:

```sh
python "$ARCHIVE/code/extract_aer.py" "$SOURCE" "$WORK/aer-reports"
```

The extractor writes one JSON and text file per PDF, plus a hash/size/page manifest and keyword index. It uses the embedded text layer and performs no OCR. A keyword miss is not evidence of absence. All outputs can contain unredacted source text; no automated privacy filtering occurs.

The raw completion-index script expects the original filename pattern and an `aer-reports` directory relative to its working directory. It does not sort the input files or output chronology. It must be run from `WORK`:

```sh
cd "$WORK"
python "$ARCHIVE/code/extract_completion_chronology.py"
```

Review the script's limitations before interpreting its output. It retains uncorrected times, durations, page references and row text. It overwrites `aer-reports/completion_chronology_raw.json` on rerun. File enumeration can change row ordering on another filesystem.

For each service-report JSON, run:

```sh
python "$ARCHIVE/code/extract_service_timeline.py" \
  "$WORK/aer-reports/<original-pdf-stem>.json" "$WORK/service-index.txt"
```

This is a limited line selector, not a complete table parser. On pages containing `Start Frac`, it selects matching field lines and the text from `Frac Comments` onward. Other pages retain their extracted text. An end time is retained only if it appears on a selected line or in retained text. Verify important values against the PDF, including rendered charts.

For a split package:

```sh
python "$ARCHIVE/code/check_split_boundary.py" \
  "$SOURCE/<part-a>.pdf" "$SOURCE/<part-b>.pdf"
```

The boundary checker compares the last page of part A with the first page of part B using text and default-rendered pixels separately. It does not delete or merge pages. Continue citing physical page numbers in the original split files.

## What is deliberately absent

Original PDFs, invoice data, extracted text/JSON, detailed findings, private storage links and rendered source pages are not part of this archive. The directory-level `.gitignore` reduces accidental inclusion, but it is not a privacy control: inspect staged files before every publication. Reproduction of the real review requires separately authorized access to the original records.
