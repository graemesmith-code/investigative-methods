# LightOnOCR-3: possible use for scanned public records

Recorded: 11 November 2026.

**Status: recorded for reference only. No further action authorised.** No OCR comparison has been run, no source documents have been uploaded, and no paid compute has been started for this assessment.

## Potential use

LightOnOCR-3 could help turn awkward scanned records into searchable text. It reads text from page images and tries to preserve the layout, including tables. Possible uses include scanned Pentagon budget books, older records and Alberta well reports that ordinary PDF search handles badly.

The linked Hugging Face page is a launcher for running the model on rented computers rather than a ready-made document-upload tool. The particular processing recipe takes a dataset of page images, rather than a multipage PDF directly, and saves the results to a Hugging Face dataset. A separate version can handle PDFs.

Compute would cost money. The cost of a run on this project's documents has not been established.

## Cautions

- **Privacy:** The linked recipe creates a new output dataset as private by default, but an existing dataset's visibility needs checking. Sensitive source material should not be uploaded without checking the full setup and permissions.
- **Accuracy:** OCR is a discovery aid, not a substitute for the original page. The assessment cited one small independent test on historical books that reported an average character error rate of roughly 8%, with some pages truncated. This does not establish how the model would perform on this project's records, especially numbers and tables. That external result has not been reproduced here.

## Possible comparison, parked

The original suggestion was to compare results on 20–30 public pages that had already caused problems, using the existing OCR as a baseline. The comparison would focus on names, dollar figures, dates and table rows, and whether the model finds material missed by the existing text.

This is retained as an idea only. The instruction when recording this note was to take no further action. No test, upload, purchase or follow-up work is authorised by this note.

## Links

- [Processing recipe and test notes](https://huggingface.co/datasets/uv-scripts/ocr/blob/main/lighton-ocr3-saturate.py)
- [Hugging Face Jobs launcher for lightonai/LightOnOCR-3-0.8B](https://huggingface.co/spaces/uv-scripts/run-on-jobs?model=lightonai%2FLightOnOCR-3-0.8B)

This note preserves the assessment shared on 11 November 2026. No additional model research or validation was undertaken while recording it.
