# Second-pass NGO discovery review

Prepared 13 October 2026 for Graeme Smith. Read [the newsroom report](REPORT.md) first.

This separate directory supersedes the editorial recommendations of [the first report](../ngo-discovery-opportunities/REPORT.md), preserved at commit `22ed3314d612f880f16608ed1349fe79cd278238`. It leaves that audit, source corpus and prior code unchanged. This is a focused synthesis of two supplied research memos and selected official-source checks. No third memo, new allegation, paid call, outreach, email or live pilot is included.

- [Technical log](TECHNICAL-LOG.md): authorization, environment, repository preservation, actual checks and delivery procedure.
- [Reproducibility annex](annexes/reproducibility.md): selection change, evidence schema, next-source rules and proposed evaluation.
- [Reading audit](annexes/reading-audit.md): original researcher depth versus independent synthesis checks.
- [TI memo](annexes/ti-monitoring-gaps.md) and [enforcement memo](annexes/enforcement-blind-spots.md): supplied research, with original caveats and section audits.
- [Local HTTPS check results](annexes/source-access-checks.json), [legislation contents access](annexes/commencement-access-check.json) and [browser checks](annexes/browser-checks.json): channel-specific source access, including failures.
- [Deduplicated URL references](annexes/source-reference-index.json): references only, never a count of reports read.
- [File manifest](file-manifest.json): SHA-256 of deliverable bytes; its own bytes and later delivery receipts are excluded to avoid self-reference.

Run `python3 scripts/validate.py` for offline checks. `scripts/check_sources.py` reruns only the fixed bounded access list, writing to a disposable cache and a new output path as described in the annex. It calls no model service. Cached original PDFs/HTML are outside Git.

The branch is `research/ngo-discovery-2026-10-13` in the private repository `graemesmith-code/investigative-methods`. The parent reviews and sends any requested email.
