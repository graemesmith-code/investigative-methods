# Checkpoint 08 — corrected evidence status

**55 reviewed formulations, 15 refinements, 70 cards. No end-to-end feasible case or finding.** Independent review identified an unauthorized certificate-validation bypass in the AER and ClinicalTrials browser probes. All five affected observations are quarantined. They do not establish verified well identities, historical trial versions, or dates.

The browser probes supplied only public well/study identifiers, no credentials, logins or sensitive user data. All sessions ended. Process inspection found no live Chromium process, only exited zombies. Reusable and temporary scripts now require normal certificate validation; no system trust settings were changed. The original failure and bypass logs remain in `evidence/browser-probes.jsonl`, annotated with quarantine status. Exact scope and remediation are in `evidence/certificate-incident.json`.

## What remains usable

The Airwars public-source reference was retrieved over normally validated HTTPS. It exposes a post URL/ID and capture metadata, but no original media payload. No restricted review link or source library was accessed. The hypothetical NASA URL returned no archive snapshot, but was not verified live: it is not evidence of an archive-access barrier. An unrelated guessed patent URL returned404: that is an endpoint failure, not evidence that patent records are inaccessible. Checkpoint09 attempts proper positive controls through observed/documented URLs.

AER official catalogue and access-request documentation remain usable. They specify a public search and a general route for obtaining unavailable records. General-record ATI has an initial $25 fee and does not guarantee a particular consent. No inquiry, request or payment was made. The browser-rendered licence/UWI row and operational interface observations remain provisional; direct HTTPS HTML shells do not authenticate those fields.

The ClinicalTrials browser-rendered version/date fields are provisional. Do not reuse the previously reported 2005/1999 dates as verified observations from this run. The general methodological distinction remains: study-first-posted and submission dates do not by themselves establish public availability of particular historical wording. No granted-claim/priority pair was obtained.

## Decisions and corrections

J01 stays a conditional small pilot, with effort tier3 because an original payload is still required. AER and J02 remain effort4; no bulk execution is justified. These judgments do not treat a guessed URL failure as a general access barrier. All three remain readiness3 because decisive evidence is unresolved.

Inherited evidence IDs now use qualified file paths and supporting source IDs. B01 resolves to batch06 EIA schema, B02 to its World Bank audit; N01 retains no such support. All original ZIPs and Git history remain preserved. The corrected ZIP supersedes the original08 bundle for current use.

Thirteen checks pass after quarantine-aware updates, including qualified evidence resolution and protection against counting quarantined observations. Earlier failed/passing outputs remain in Git and the initial test log. Corrected07's fourteen checks passed separately.

Use `route-checks.csv`, the complete `cross-batch-ranked-routes.csv`, `counts.json`, and the evidence logs. Local build/validate/package scripts make no network calls. Separate probe scripts require normal HTTPS; stop on a certificate warning. No full investigation, paid calls, payment or outreach occurred.

Weekly ChatGPT telemetry is unavailable; the last user report remains88% at18:50UTC. That does not measure this task's consumption.
