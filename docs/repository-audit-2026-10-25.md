# Repository audit — 25 October 2026

**Finding:** This public repository is useful as a record of reporting experiments, but its raw-data footprint and navigation have outgrown its informal storage rules. The immediate concern is large files and ambiguous delivery paths, not the number of repositories or branches. No data should be deleted or Git history rewritten on the strength of this audit alone.

**Editorial conclusion:** Preserve reporting findings, negative results, provenance, small samples, verification scripts, and reproducible manifests in GitHub. Put replaceable bulk inputs and regenerable full-size machine outputs in separately backed-up data storage, linked from GitHub by retrieval instructions and SHA-256 checksums. Before moving anything, verify the external copy can be restored.

## At a glance

As observed on the default branch `main`, 25 October 2026, at commit `4acc0364b1aad56587625873b10bcba30377fd96`:

| Measure | Observed |
| --- | ---: |
| Tracked files in current tree | 4,509 |
| Total bytes of current file contents | 1,155,672,045 bytes (1,102.13 MiB; 1.08 GiB) |
| GitHub repository metadata `size` | 698,948 KiB (about 682.57 MiB; different measure from current files) |
| Maximum single current file | 102,378,238 bytes (97.64 MiB) |
| Branches returned by GitHub's branch listing | 20 |
| Distinct content-identity groups reused at multiple paths | 63 |
| Additional paths with identical Git blob SHA | 112 (39.33 MiB of *logical* duplicate file contents) |
| Maximum tracked path depth | 8 components |
| Tree API pagination/truncation | `truncated: false` |
| Public/private status | **Public** |

The sum of current file contents is **not** on-disk `.git` storage or complete Git history. GitHub repository metadata does not by itself establish the size of a full fresh clone, the age of unreachable objects, or whether Git LFS is billed. Identical Git blobs are already deduplicated at the Git object level; deleting their duplicate paths will not necessarily save that many repository bytes.

## Main space consumers

| Project | Files | Current file contents | Immediate treatment |
| --- | ---: | ---: | --- |
| [Alberta seismic and fracturing](../research/2026-10-06/alberta-seismic-injection/README.md) | 208 | 441.47 MiB | Preserve investigative report, event packets, code, full source manifests; verify external backup of split source archives and regenerable raw records before migrating |
| [F4 autonomy brakes audit](../research/2026-10-25/f4-autonomy-brakes-audit/README.md) | 274 | 307.22 MiB | Most urgent: near-100 MiB JSON and redundant compressed recovery transport; maintain verifiable publication chain before any change |
| [Pentagon contract history](../research/2026-10-16/future-warfare-investments/README.md) | 2,811 | 138.11 MiB | 1,247 gzip HTML captures plus 1,247 parsed JSON page records are valuable paired evidence, not automatically duplicate waste; consider external archive with stable manifest |

Together these three directories contain **about 80.5%** of the current bytes. The remaining material includes 2026-10-04 source-comparison runs with repeated inventories, FARA tables in the top of `research/`, and other small experiments.

By file type: `csv` 302.20 MiB (180 files), `json` 232.80 MiB (2,108), `jsonl` 105.27 MiB (157), `zip` 99.16 MiB (42), `gz` 41.03 MiB (1,253), and `md` only 1.99 MiB (210). Split `.part*` files add additional substantial volume. The Markdown prose is not causing the storage problem.

**Largest file:** `research/2026-10-25/f4-autonomy-brakes-audit/evidence/brakes-candidate-register.json`, **97.64 MiB**. Its CSV counterpart is 80.55 MiB; an auxiliary JSON Lines candidate list is 46.46 MiB, and ASIMOV continuation CSV is 44.85 MiB. GitHub warns about ordinary Git files above 50 MiB and blocks files above 100 MiB. A routine expansion could break the next push. [GitHub guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

**Highest-cost archival structure:** Alberta holds 40 MiB pieces of `ST37-excel.zip` and `order-shapes.zip`, plus source tables. These are existing recovery artifacts, not necessarily useless duplicates. The source and its checksum/retrieval record must survive any migration.

## Problems observed

### P0 — prevent imminent avoidable failures

1. **Stop committing growing bulk machine registers into ordinary Git.** The F4 JSON file is already 97.64 MiB. Do not increment it in place. Keep human-review selections, code, sample records and manifests in Git. Give the full register an independently verified data location and checksum before migrating it.
2. **Resolve F4 package link ambiguity.** [F4 README](../research/2026-10-25/f4-autonomy-brakes-audit/README.md) links to `F4-COMPLETE-RESEARCH-PACKAGE.txt.gz`, which was **not present** in the current tracked tree. [Recovery transport](../research/2026-10-25/f4-autonomy-brakes-audit/audit/recovery-transport/README.md) does contain validated split/gzip backups for four already-published consumer registers, but explicitly does not claim to be the promised complete package. Update delivery documentation after verifying the full package's actual location. Do not infer loss merely from its absence in Git.
3. **Check access and publication risk.** The repository is **public**. [docs/next-steps.md](next-steps.md) still calls it private; this is stale. A filename scan found no obviously named credential files, and root `.gitignore` excludes `.env`, `*.pem` and `*.key`, but **no full content/history or personal-data scan** was performed. Public procurement records, article text, leaked data and third-party source exports require separate publication-rights reviews.

### P1 — restore an understandable front door

4. **Refresh the [top-level README](../README.md).** It omits prominent current work, including Alberta and F4. Put a short *Current reporting / Parked trials / Methods and source catalog / Technical archive* index near the top. Each entry needs one plain-English outcome, date, unresolved question and destination.
5. **Distinguish experiments from snapshots.** The 2026-10-04 source-pair review directories share exact `candidate-inventory` files and other repeated outputs. There are 63 repeated-Git-blob groups/112 extra identical file paths across the current tree. Git already deduplicates identical blobs: this is mainly an information-architecture/review burden, not a guaranteed 39 MiB disk saving. Prefer one canonical inventory plus run manifests/pointers for future iterations.
6. **Make status and provenance mandatory.** Each project README should specify research question, *finding / no finding / parked*, study window, source owner/link, retrieval date, original and output hashes, commands, version, spend, coverage gaps, reporting next step and who/what may publish. Keep an appendix for machine instructions.
7. **Reduce ambiguity from flat files.** Top-level `research/FARA_All_RegistrantDocs.csv` and neighboring FARA exports should be documented as a named dataset with origin/retention and permissions; do not move blindly because existing scripts may use those paths.
8. **Assess branches before pruning.** GitHub lists 20 branches, including named work, recovery and archives. The number is not a capacity problem; determine whether each contains unique commits and whether its output reached `main` before closing it.

### P2 — a sustainable default

9. **Introduce a data retention policy:** keep small sources and checked samples in Git; above **10 MiB**, ask whether the artifact is source evidence, derived output, or a regenerable cache. Above **25 MiB**, require an explicit written retention reason. Above **50 MiB**, default to separately backed-up object storage and a manifest; exceptions need a rationale. Never use Git as the only backup for irreplaceable evidence.
10. **Record one canonical destination per dataset.** Manifest fields: original URL/terms; acquisition date; original filename; full bytes; SHA-256; licensing/publication status; local and off-Git storage URI; schema; retrieval or regeneration command; coverage caveat; permitted sharing; and verification date. No external storage has been set up in this audit.
11. **Make reproducibility fail visibly.** A cheap automated check can flag files above 10/25/50 MiB, missing relative Markdown targets, missing dataset manifest fields, accidentally tracked secrets and changed machine outputs without provenance. Do not auto-delete evidence on test failure.
12. **Only consider history surgery later.** Removing a file in a new commit does not remove it from earlier commits. A real space reduction may require `git filter-repo` or another history rewrite, and coordinated backup, verification and branch/clone handling first. No rewrite was performed.

## Proposed information architecture

```text
README.md                     Plain-language front door; active and parked indexes
catalogs/                     Rabbit source catalog and updates
experiments/                  Reusable reporter-readable recipes and verdicts
research/YYYY-MM-DD/slug/     One canonical folder per investigation and run status
code/                         Only shared/reused tooling; project-specific code stays with case
docs/                         Method, governance, audits, data-storage policy
annexes/                      Long technical methodology when not project-local
# Bulk archives: outside ordinary Git, with manifests + verified restore tests
```

Avoid a wholesale directory move now. Links and citations in earlier research may be permanent evidence references. Migrate in small, reversible batches; update and test links; preserve old source IDs and hashes.

## Proposed cleanup sequence (nothing deleted during audit)

1. **Today:** Freeze new ordinary-Git commits above 50 MiB; make a tested backup of the F4 registers and the promised complete F4 package, or accurately explain where it lives.
2. **Next:** Rewrite the root index to make the current high-value work discoverable; fix stale public/private language.
3. **Then:** Create dataset manifests and verified off-Git copies for the 441 MiB Alberta group and large F4 data; only afterward decide which ordinary-Git raw copies to retire.
4. **Afterwards:** Consolidate the 2026-10-04 duplicate run inventories logically; inspect branch divergence; run a more exhaustive credentials, sensitive-source, publication-rights and broken-links audit.
5. **Finally:** Evaluate actual pack/history size on a fresh clone with `git count-objects -vH` and `git-sizer` before deciding whether a disruptive history rewrite is justified.

## Method and limits — technical annex

- Read GitHub repository metadata, the untruncated recursive default-branch Git tree, the list of 20 branch names, the 50 most recent commits, root `.gitignore`, root README, selected research READMEs, F4 package-validation and transport files, and selected supporting documentation on **2026-10-25**.
- File count and current bytes: `tree.filter(type === "blob")`, summing `size`. Project grouping uses the first three path components for `research/YYYY-MM-DD/name`.
- Duplicate identification uses exact Git blob SHA, not similar names or textual near-duplicate matching. Distinct filenames with the same SHA are exact byte-identical contents; future revisions and retained history were not audited.
- Sampled relative Markdown links in root README, `docs/next-steps.md` and F4 README against the tracked tree; one unresolved F4 complete-package link found. This is **not** a complete repository-wide link scan.
- The current-tree histogram is not a full repository-size, packfile, billing, Git LFS, branch-specific, remote-backup, license, secret, or historical-content audit. No malware claims, corruption claims, permission guarantees or absence-of-secret claims follow from these checks.
- Reference GitHub policies: [large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) and [repository structure and operational limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).

**Audit status:** Evidence reviewed; cleanup plan proposed; no existing dataset, branch or research record deleted, moved, or rewritten.
