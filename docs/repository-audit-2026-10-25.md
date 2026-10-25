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


---

## Storage architecture decision note — 25 October 2026

### Recommendation: keep the four jobs distinct, but start with only two services

**Phase 1 (simple, now):** Continue to use public GitHub for publishable methods, the Rabbit catalog, code, reports, plain-English case indexes, and small verification samples. Keep unfinished or sensitive reporter notes in a **separate private workspace** (a local Obsidian vault or private GitHub repository, not this public repository). Use private Google Drive folders for working copies of source documents, evidence bundles and moderate-sized datasets. Maintain an independent offline or separately backed-up copy of irreplaceable originals. **Do not yet move or delete existing Git files.**

**Phase 2 (when bulk data exceeds roughly 50–100 GB, or many automated jobs produce large archives):** Use a private Backblaze B2 bucket for large machine-readable datasets and verified evidence snapshots. Keep Drive for normal document access and GitHub for methods and manifests. Backblaze is an object store: files are identified by stable object keys and can be uploaded or downloaded by a script, but it is not a document editor or convenient full-text notebook. Optionally use Cloudflare R2 instead when public distribution/download volume is the decisive factor.

**Phase 3 (publication):** Continue publishing readable material through GitHub, optionally with GitHub Pages as the website. Deposit *final, cleared-for-publication* data releases in Zenodo for a stable archival citation, or distribute large public downloads from R2. Do not deposit confidential sources, unreviewed third-party material, or restricted records in public repositories.

**Principle:** One investigation, one canonical metadata manifest, multiple fit-for-purpose storage locations. An agent or reporter starts with the investigation README in GitHub; the README points to the authoritative source objects, their verification hashes, caveats and availability, without copying all the raw data into Git.

### Service comparison: published rates checked 25 October 2026

| Service | Role | Representative price | Main limitation |
| --- | --- | --- | --- |
| Google Drive / Google One | Casefiles and source documents, initial small-to-moderate bulk | 15 GB free shared with Gmail and Photos; Italian offers: 100 GB around €1.99/month, 200 GB around €2.99/month; 2 TB offers around €9.99/month depending on plan | Sync is not independent backup; less convenient for automated millions-of-record pipelines and reproducible immutable archival evidence |
| Backblaze B2 | Private large data lake and independent archive | First 10 GB free; approximately US$6.95/TB/month thereafter; free downloads to 3× average monthly stored data | More technical; file contents are not automatically indexed like a notebook; extra charges may apply to large download volume |
| Cloudflare R2 Standard | Public dataset distribution or bulk access | 10 GB storage free per month, then US$0.015/GB-month; request charges beyond allowances; no internet egress fee | Technical setup and careful public/private bucket access management |
| Zenodo | Citable finished public releases | Free; 50 GB default quota per record | Not for continuously changing live corpora or undisclosed sensitive source material |
| Obsidian (local) | Private reporting notebook | Application free; optional Sync Standard from US$4/month billed annually (1 GB sync storage, 5 MB per-file maximum) | Note-taking and linking, not a bulk data archive |
| GitHub | Publication, code, small datasets, machine-readable manifests | Free tier currently adequate for published method and documents | Regular Git file warning >50 MiB, hard block >100 MiB; GitHub suggests repositories ideally <1 GB |

Official sources or provider references: [Google One Italy](https://one.google.com/intl/it_it/about/), [Google One Italian App Store offers](https://apps.apple.com/it/app/google-one/id1451784328), [Google Drive sync behaviour](https://support.google.com/drive/answer/13401938?hl=en), [Google Drive deleted-file recovery](https://support.google.com/drive/answer/1716222?hl=en), [Backblaze B2 prices](https://help.backblaze.com/hc/en-us/articles/217667478-Understanding-B2-Pricing-Structure), [Backblaze Object Lock](https://help.backblaze.com/hc/en-us/articles/360052973274-Object-Lock-FAQs), [Cloudflare R2 prices](https://developers.cloudflare.com/r2/pricing/), [Zenodo quota](https://help.zenodo.org/docs/deposit/manage-quota/), [Obsidian Sync plans](https://obsidian.md/help/sync/plans), [GitHub large-file guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). Prices and availability vary by date, location and account; verify before purchase.

### Why Google Drive alone is not enough

- Drive for desktop can **stream** files (mostly cloud-only) or **mirror** them (full Mac copy), but changes and accidental deletions propagate. Google Drive trash generally retains deleted files for 30 days; older non-Google file versions can expire after 30 days or 100 newer revisions unless preserved. This is **synchronization**, not independent archival backup.
- Drive is good for ordinary papers and PDFs, easy Mac Finder access, and connected document assistants. Bulk data should be retrieved by automated scripts when it grows beyond modest files or record counts. An AI connector does **not** turn a 100-GB data corpus into automatically understood, searchable research.
- A Drive folder accessible to the owner is not automatically safe for anonymous sources. If source confidentiality matters, encrypt content *before* cloud upload, restrict access, separate the encryption key, and consider whether transmitting it to any AI service is appropriate. Do not commit the decrypted plaintext, credentials or source identities to public GitHub.
- Google Drive's broad convenience does not provide the same retention controls as dedicated object stores. Backblaze B2 supports optional immutable Object Lock, but it must be configured deliberately (and retention mistakes can be difficult to undo).

### Proposed directories and ownership

```text
PRIVATE NOTEBOOK (Mac / Obsidian / optional private GitHub)
  /ideas /active /parked /contacts-private

GOOGLE DRIVE (private; access controlled)
  /Investigations/00-inbox/                    Unprocessed transfers; short-lived
  /Investigations/10-active/<case-id>/          Working copies and correspondence
  /Investigations/20-original-evidence/<case-id>/  Read-only by convention; originals plus acquisition records
  /Investigations/30-processed/<case-id>/       Smaller interim data and reviewed outputs
  /Investigations/90-closed/<case-id>/          Final archived case packets

BACKBLAZE B2 (later; private bucket by default)
  /<case-id>/sources/                           Raw large datasets, snapshot identifiers
  /<case-id>/derived/                           Regenerable large outputs
  /<case-id>/manifests/                         Byte counts and cryptographic checksums

GITHUB (existing public investigative-methods repo)
  /research/<YYYY-MM-DD>/<case-id>/README.md    Reporter-readable result, status and reporting next steps
  /research/<YYYY-MM-DD>/<case-id>/DATA-MANIFEST.md  Where data lives and how to verify/restore
  /research/<YYYY-MM-DD>/<case-id>/code/        Reproduction scripts
  /docs/                                        Reusable governance and procedure
  /catalogs/                                    Rabbit entries
```

Use stable case identifiers and distinct *public/private* markers in manifests. For any private object, GitHub should contain a neutral description and cryptographic checksum, **not** the confidential object's access URL or identifiable source details.

### Minimum metadata for every externally stored file

- Investigation ID and data role: `original-source`, `derived-output`, `reporter-note`, `publication`.
- Safe public description; specific source and rights/terms in the appropriate private register.
- Original acquisition timestamp, source URL if safe, reported coverage dates, file byte length, SHA-256 digest.
- Canonical storage provider and object path, private/public classification, external backup location where safe to disclose.
- Script/command or manual instructions to retrieve and verify; derivation script version and input hashes for derived files.
- Retention decision and review date, full-publication permission status, and restore-test result.

Do **not** make GitHub a universal index of source identities. For a sensitive investigation, the manifest in GitHub must not expose identities, unpublished allegations or private archive access parameters.

### Reversible pilot and acceptance checks

1. **Pilot one public, low-risk archived project**, e.g. a small dated procurement archive, not confidential or leaked material.
2. Copy originals, a small machine output and manifest into a new private Drive folder. Check file counts and SHA-256 checksums; download a representative sample and compare bytes.
3. Write its case's public README and safe manifest, with distinct labels for original source, derived outputs and editorial verdict. Confirm a fresh user/agent can navigate it without seeing secret links.
4. For a **second pilot**, upload a 1–5 GB replaceable public bulk archive to B2, with correct billing limits, private bucket settings, versioning and a scripted restore. Confirm read-back and hash before further migration.
5. Only after two successful restore exercises, plan staged removal of verified, regenerable current-branch data, with explicit decision on historic Git objects. Nothing here authorizes deletion, force pushes or an automatic repository history rewrite.

### Immediate priority for the already audited repository

A. Preserve and test a canonical backup of the F4 `brakes-candidate-register.json` (97.64 MiB), companion CSV, ancillary candidate outputs, and recovery manifests. Resolve the documented **missing F4 complete-package link** before changing references.

B. Record original source/derived-output status for Alberta's 441.47 MiB case and its multipart compressed files; verify whole-file reconstruction from parts before migration.

C. Treat the Pentagon contract archive's HTML and JSON pairs as source/evidence plus structured extraction, not assumed duplicate waste. Create a complete inventory before relocating 2,494 historical source-and-parse records.

D. Keep the Rabbit catalog, short experiments, code, investigative findings and publication-ready reports in GitHub. Their size is negligible compared with raw machine data.

**Decision status:** Architecture proposed; vendor accounts, Drive folders, B2 buckets, backup automation, and migrations have **not** been set up. No existing file moved or deleted.
