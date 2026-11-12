# Spangher public-code inspection — 8 October 2026

Primary source: [newsworthiness-public](https://github.com/alex2awesome/newsworthiness-public).
Inspected file blob identifiers are in `inspection-provenance.json`. No research code
was executed or copied into this scaffold. README scale/coverage figures are the project's
own descriptions, not results reproduced here. The README describes both historical data
releases and an October 2026 code-only export; the latter determines current availability.
Fetching `data-to-submit/full-meeting-row-df.csv` through GitHub returned 404.

| Inspected element | Useful design element | Limitation and adaptation |
| --- | --- | --- |
| [process-homepage-data.py](https://github.com/alex2awesome/newsworthiness-public/blob/main/modeling/data-processing-scripts/process-homepage-data.py) | Join article URLs to captured layout; preserve homepage key, normalized x/y and area; deduplicate article/capture pairs | Requires captured HTML, articles, bounding boxes and language tooling. URL normalization drops some information; audit collisions before adopting. No such input exists in this ATI pilot. |
| [train_models.sh](https://github.com/alex2awesome/newsworthiness-public/blob/main/modeling/basic-homepage-model/train_models.sh) | Explicit placement dataset and evaluation configuration | References missing `data/basic-homepage-placement-labeling.jsonl` and a downloadable BigBird model. Not an offline executable precedent with this export. |
| [trainer.py](https://github.com/alex2awesome/newsworthiness-public/blob/main/modeling/basic-homepage-model/trainer.py) | Input split field, per-category evaluation, trivial all-positive comparator | Missing split falls back to unseeded random assignment. Classification accuracy/F1 are not top-k discovery value. Here we freeze source membership, seed blinding and report ranking yield by department. A future trained model needs grouped/time-aware held-out article, policy and capture splits. |
| [sentence_model.py](https://github.com/alex2awesome/newsworthiness-public/blob/main/modeling/basic-homepage-model/sentence_model.py) | Document records with sentence arrays and labels; tokenization separated from model | Depends on Torch/Transformers, pretrained weights and labels. Token-length filters silently drop records outside 5..max tokens; future reuse must account for dropped examples. No model port or training claimed. |

Placement is observed editorial allocation of space and attention. Coverage is whether a
public document links to a published article. Neither is identical to public significance,
novelty, evidence quality, or the value of an unpublished lead. A homepage position is not
a print-page A1/A16 label. Future prominence learning should retain outlet, date, exact
position, record/article match confidence, repeated captures and provenance, and control
for outlet agenda, geography, topic and repeated stories. Article text after publication
must not leak into a record-only discovery evaluation.

The reusable contribution here is the research decomposition: preserve the source-to-story
relationship, distinguish placement from coverage, evaluate against people and simple
comparators, and inspect subgroup results. This scaffold supplies new standard-library
code implementing a narrower evaluation. Its human-label exercise is not a replication
of Spangher's model or research findings. Obtaining data, clarifying reuse rights and
auditing a new train/test split are prerequisites for an actual transfer experiment.
