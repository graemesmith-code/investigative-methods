# F6 corporate legal brakes — checkpoint 02

**Research incomplete. Source-team intake and independent release review pending.**

The approved directive has been materialized in this consumer environment and verified: 26,565 bytes, SHA256 `a59cf56bd82414b9c3e2079d4d7dfd8353bb3ffb0d37f4a09b0991e27032199a`. Its Library current version is 1; its filename labels the approved directive v2. Those are different version systems.

[Start with the Drive reading guide](https://drive.google.com/file/d/1Hqui7OgSYem6nocwWKlWWX7vG5ca83HW/view?usp=drivesdk). The [claim-to-evidence index](https://drive.google.com/file/d/1Qja-aEYTaTqZ6xiAlF5CZXfrk60DYZXL/view?usp=drivesdk) and principal occurrence/candidate/coverage/source registers are individually accessible. [Detailed F6 data folder](https://drive.google.com/drive/folders/1LAErE1EpubQKKdLW7aU0A0B44ey_Nd2q). The child folder's parent and owner were read back. Its inherited anyone-reader permission was observed; no permissions were changed. Only authored, cleared material belongs there.

This initial checkpoint contains the screening/validation code, premise-audit framework and publication/intake state. **One primary compilation has received a machine text pass over 130/130 extracted pages; 41 occurrences are retained, all provisionally classified, with zero promoted findings.** Full semantic/image completeness remains pending. Native source-team dossiers are not yet received. These counts are not a count of corporate controls or IHL commitments.

The 30-company panel produces 360 company/lane cells. Every cell is explicitly awaiting native-team review; panel labels are not yet resolved legal entities. Four existing native teams cover all twelve lanes. Their reviewed dossiers, source records and actual editorial histories will be integrated through Library. The coordinator does not duplicate their research or claim their work as received.

## Read

- [Report and current gaps](report.md)
- [Premise audit](LEGAL_PREMISE_AUDIT.md)
- [Reading pack and source priorities](READING_PACK.md)
- [Screening and intake contract](SCREENING_METHODS.md)
- [Drive object manifest](DRIVE_DATA_MANIFEST.json)
- [Machine-readable publication scope](manifest.json)

## Reproduce the screen

```sh
python3 code/screen_references.py /absolute/path/sources.jsonl /absolute/path/data
python3 code/screen_references.py /absolute/path/sources.jsonl /absolute/path/data --reviews /absolute/path/reviews.jsonl
python3 -m unittest discover -s code -p 'test_*.py' -v
python3 code/validate_release.py . /absolute/path/data
```

The code makes no network calls and cannot spend money. Private full-text snapshots and detailed output belong outside Git. All new Git files must be under 100,000 bytes. The full source lexicon and exact execution hashes accompany the Drive registers. The eight tests are synthetic checks of pipeline behavior, not research evidence or measured real-world recall.

Final release requires the completed source dispositions, three genuine editorial rounds and the parent's independent release decision. Local validation cannot supply that decision.
