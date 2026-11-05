# Execution and validation record

Date: 5 November 2026.

Environment: Python 3.12.14; PyMuPDF 1.26.6.

## Actual review execution

- `extract_aer.py` was executed successfully on all twelve supplied PDFs: 669 physical pages. The initial page-text JSON used the same `get_text(sort=True)` extraction method as the preserved rerun.
- `extract_completion_chronology.py` was rerun successfully and reproduced the original 835-row raw index byte-for-byte in the original workspace. This is a count of raw indexed rows, not a count of unique activities or validated time intervals. The script's filesystem-dependent enumeration means cross-machine row ordering is not guaranteed.
- `extract_service_timeline.py` was executed on the three service-company packages, with split files kept separate. It is a limited field/comment selector, not a complete stage table parser.
- `check_split_boundary.py` was executed on both split pairs. Part A page 70 matched part B page 1 in each pair, for extracted text and default-rendered pixels. No source pages were removed.
- Important statements and selected rate/pressure plots were rendered and visually reviewed. This was targeted visual review, not a claim that every page was visually audited.

## Archive verification

The four preserved scripts were compared byte-for-byte with the supplied executed versions before publication. Python syntax compilation and four synthetic smoke tests passed. The smoke tests cover page preservation, unchanged PDF bytes, manifest hashing, keyword-index page references, field/comment retention, raw-clock preservation, the documented page-continuation limitation and positive/negative split-boundary comparisons.

These checks validate specific extraction behavior. They do not validate the underlying records, completeness of the acquisition, chronology, scientific attribution or regulatory conclusions. No source records are included in the tests.
