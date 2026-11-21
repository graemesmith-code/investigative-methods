# Editorial-placement data and model access audit

Checked 8 October 2026. Scope: public data, trained weights and stated reuse terms for
Spangher's front-page and later homepage work. No paid calls, inference, training or
contact with the authors. Machine-readable observations and download checksums are in
`data-access-audit.json`. This audit establishes access, not a benchmark result.

## Result

There is a working public source of raw homepage text and screen coordinates. There is
no verified ready-to-run Spangher newsworthiness checkpoint or ready-made placement
training set in the inspected public sources. The original print corpus is unavailable
through its official distributor. A reconstruction path is technically plausible but
requires filtering and validation; data reuse terms remain unresolved.

| Resource | Access verified | What it provides | Remaining gap |
| --- | --- | --- | --- |
| [2021 front-page paper](https://arxiv.org/pdf/2104.09653) | Paper readable | Names the New York Times Annotated Corpus and page-based training target | Paper access is not data/model access |
| [Original corpus distributor](https://catalog.ldc.upenn.edu/LDC2008T19) | Live catalog read | Explicitly states the corpus is no longer available | No authorized dataset download established; no price/purchase path asserted |
| [newspaper-pages](https://github.com/alex2awesome/newspaper-pages) | Complete recursive tree and release endpoint checked | Older classifier code and analysis notebooks consistent with the front-page work | No fine-tuned checkpoint or placement corpus found; release list empty |
| [newsworthiness-public](https://github.com/alex2awesome/newsworthiness-public) | Complete recursive tree and release endpoint checked | Code-only export for public-document coverage/placement work | No data/model artifacts found; release list empty; prior advertised CSV returned 404 |
| [Homepage research repository](https://github.com/alex2awesome/homepage-newsworthiness-with-internet-archive) | Complete recursive tree and release endpoint checked | Parsing/ranking code and notebooks | Derived pairs and weights absent; release list empty |
| [Author's Hugging Face models](https://huggingface.co/alex2awesome/models) | Public API listed 35 models | Quote, discourse, stance and summary models | No identifiable editorial-placement/newsworthiness checkpoint found |
| [Author's Hugging Face datasets](https://huggingface.co/alex2awesome/datasets) | Public API listed two datasets | City-council silver-standard summaries and docket-bench | Neither is an identified placement training corpus |
| [News Homepages extracts](https://palewi.re/docs/news-homepages/extracts.html) | Downloaded outlet roster and item index | 5,816 annual outlet/item index rows at inspection; capture-file references | These rows are archive containers, not labeled examples or unique outlets |
| [Guardian 2026 archive item](https://archive.org/details/guardian-2026) | Downloaded matching link data, accessibility tree and screenshot | Text, URL and top/left/bottom/right coordinates | Raw links include navigation, duplicates and non-story links; no validated preference labels yet |

Repository file trees were not truncated. Checks covered the current trees, release lists
and the author's public model/dataset catalogues; they do not establish that private,
unlisted or third-party-hosted artifacts do not exist. The Hugging Face `all-models` tree
contains configs/results/prediction outputs, not loadable weight files; its salience-named
outputs are not sufficient evidence of an editorial-placement model.

## Actual download test

Source item: `guardian-2026`. Capture time: `2026-01-01T01:11:02.011154+00:00`.

- Hyperlink file: 91,988 bytes, 418 entries. All 418 have finite numeric top, left, bottom
  and right coordinates. Those are link rectangles, not necessarily whole article cards.
- Accessibility tree: 103,677 bytes, with role/name/children structure.
- Matching viewport screenshot: 282,781 bytes. Visually inspected; it shows the Guardian
  UK homepage with story cards, navigation and promotional modules.
- All three downloads returned HTTP 200 and matched the archive's advertised MD5 checksums.

Exact URLs and SHA-256 checksums are in the manifest. Only access evidence is added to the
repository; copyrighted capture contents are not republished there. The screenshot is a
viewport capture, so it cannot visually validate every below-fold link. This sample proves
that actual assets can be retrieved; it does not prove all outlets/dates have usable data.
No HTML asset was downloaded or checked in this sample.

Importantly, this capture's hyperlink data already contains coordinates. We may be able
to build a headline-level placement experiment without downloading full articles or
re-running the original HTML parser. That is an inference to test in a subsequent
extraction pilot. It is not a claim that ordinal DOM order equals editorial preference:
promotional modules above the news lead, hidden links and different story-card sizes need
explicit handling.

## Reuse terms

The [palewire archiver](https://github.com/palewire/news-homepages) has a GNU General Public
License version 3. That is its software license. No license/rights/usage field was found
in the checked archive collection or Guardian item metadata; it is not a verified license
for training on or redistributing publisher material. The three Spangher research trees
have no repository-wide license file identified; embedded third-party license files in
the older repository do not establish a license for the whole research project.
Public download access, software reuse, publisher-content reuse and redistribution must
remain separate statuses. No permissive data/model license is inferred from availability.

## Concrete next action

Ask Spangher for (1) a fine-tuned front-page or homepage-preference checkpoint and its
inference instructions; (2) derived placement/pairwise data and original split/group IDs;
(3) any previously collected expert public-record judgments; (4) explicit data/model/code
reuse conditions for this journalism experiment and sharing reproducible outputs.

In parallel, the next technical experiment would examine a bounded set of archived
captures from several outlets, extract candidate article links, validate position/card
signals against screenshots and record the extraction failure rate. Existing raw
coordinates make that worth testing. Do not run paid scoring or claim trained-model
availability until actual model artifacts and usable labeled examples are secured.
