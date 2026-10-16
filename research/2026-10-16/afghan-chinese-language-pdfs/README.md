# Chinese-language Afghan government PDFs: one verified publication

## Finding

A complete scan of the eight Chinese-language categories in the saved FinePDFs inventory found **one verified Afghan government publication**: the Chinese version of the **Chairman's Statement of the Sixth Regional Economic Cooperation Conference on Afghanistan**, held in Kabul on **3–4 September 2015**.

The recovered original is a three-page PDF. Its cover bears the name and emblem of the **Islamic Republic of Afghanistan, Ministry of Foreign Affairs**. All three pages were visually inspected. This is a Republic-era publication.

The relevant passages are:

- **Paragraph 9, PDF page 2:** China's Belt and Road Initiative and its potential regional benefits.
- **Paragraph 11, PDF page 2:** the proposed railway linking China, Kyrgyzstan, Tajikistan, Afghanistan and Iran.
- **Paragraph 14, PDF page 3:** possible financing from sovereign wealth funds, the BRICS New Development Bank and the Asian Infrastructure Investment Bank.
- Other sections cover the Lapis Lazuli route, Chabahar, energy connections, regional information networks and investment promotion.

The statement is public diplomatic material. It demonstrates Chinese-language publication by an Afghan government conference platform, but does not establish who translated it, who paid for translation, or a previously undisclosed agreement.

## Why the earlier search missed it

The archived address was **recca.af**, outside **gov.af**. It was also in the **Mandarin Chinese category**, outside the previously screened unknown-language category. Both selection rules would have missed it.

A historical list of official domains is therefore necessary. The ministry's current [conference page](https://recca.mfa.gov.af/main-forum/) identifies the 2015 event and links the old recca.af domain to the Ministry of Foreign Affairs. Its [contact page](https://recca.mfa.gov.af/contact/) gives the ministry's Kabul address and a recca.af email. The [2017 annual review, PDF page 2](https://recca.mfa.gov.af/wp-content/uploads/2022/11/RECCA-Annual-Review-2017-FINAL-VERSION.pdf) carries ministry copyright and advertises the Chinese statement among its publications.

## Download and date information

The conversation supplies the unchanged recovered PDF as `2015-RECCA-VI-Chairmans-Statement-Chinese.pdf`.

- Historical source: http://recca.af/wp-content/uploads/2015/12/cn.pdf
- Conference dates printed in the document: 3–4 September 2015.
- PDF creation metadata: 28 December 2015. This is an editable metadata field, not independent proof of publication.
- Archived server Last-Modified header: 30 December 2015.
- Common Crawl capture: 22 November 2017.
- Recovery and verification: 16 October 2026.

**Copy quality:** All three pages render without repair; the PDF has an end marker and its final paragraph is present. The archive nevertheless flags the response as truncated. That flag is preserved in the audit, so this is described as a usable recovered original, without an unqualified guarantee of byte-for-byte completeness. The original site could not supply a fresh comparison copy.

## Search result and limits

All **4,982,532 records**, in **30 files** across **eight Chinese-language categories**, were checked. There were no unresolved scan errors.

There were **zero gov.af-domain matches** in those categories. A broader candidate rule—any .af domain or any hostname containing “afghan”—found 45 records:

| Host | Records | Assessment |
|---|---:|---|
| recca.af | 1 | Retain: verified Afghan ministry publication |
| faceafghan.com | 41 | Exclude: Chinese corporate filings and related professional documents |
| afghanpeper.com | 2 | Exclude: electronic-component data sheets |
| afghanboxcamera.com | 1 | Exclude: camera-building manual |

No post-2021 government publication was established in this scan.

This is complete coverage of the selected Chinese-language categories, **not a census of every Chinese passage published by an Afghan government**. Chinese sections in documents labelled English, Persian, Pashto or another language may be missed. Official domains outside .af whose names do not contain “afghan” may also be missed. The processed archive is not a complete historical web archive. The separate Russian, Arabic and other language searches remain unfinished.

## Technical annex

- `summary.json`: counts and elapsed scan time.
- `scan-audit.json`: all 30 source files, every completed row group and coverage checks.
- `candidate-decisions.jsonl`: all 45 candidates, source metadata and decisions.
- `retained-source-record.json`: the retained record, recovery details, document hash and verification notes.
- `archive-response-headers.txt`: original archive and server headers, including the truncation flag.
- `scan_chinese.py` and `work/source-parquet-inventory.json`: reproducible URL-column scan.
- `download_pdfs.py` and `manifest.jsonl`: recover the retained original from its archive pointer.

The selection reads URL columns; full record text is retrieved only for address matches. Chinese-language category codes include Mandarin, Hakka, Classical Chinese, Southern Min, Wu and Cantonese, with separate writing systems where the saved inventory provides them. All categories matching those language families in the inventory were included.

The URL scan took **312 seconds** in this run, including retrieval of matching records. This excludes dependency setup, source-PDF recovery, visual review, reporting and saving. No paid model service was called by the scan script. The surrounding assistant session was not separately cost-metered.

To repeat from this folder:

    python3 -m pip install -r requirements.txt
    python3 scan_chinese.py
    python3 download_pdfs.py

The scanner checkpoints completed row groups under `work/states/`. To measure a fresh full run, use a fresh folder. Public archive and dataset availability can change.

