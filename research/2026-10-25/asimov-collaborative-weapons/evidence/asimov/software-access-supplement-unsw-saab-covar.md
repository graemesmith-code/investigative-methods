# ASIMOV public software/data/demo access supplement

**Cutoff and inspection date: 24 October 2026.** Scope: UNSW/ASU, Saab/MIT, and CoVar/Duality. Public pages, repository metadata, README/license text, paper acknowledgments, and demo explanatory text only. No repository clone, software installation, executable download, code execution, simulation, login, terms acceptance, paid service, or outreach was performed.

## Bottom line

No publicly accessible **full ASIMOV benchmark software or dataset** was verified for these three teams in this bounded pass. This does not establish that no release exists or that a contractual obligation was breached. A significant related MIT/Saab lead, **SEED-SET**, has an accessible paper, project website, and public website/demo assets. Its specific attribution to ASIMOV remains **unconfirmed**. A linked Colab's contents and executability could not be verified without proceeding beyond the public sign-in rendering.

## 1. Saab/MIT: RESPECT and the related SEED-SET lead

### Confirmed program identity

Saab's **6 January 2025** announcement identifies its ASIMOV work as RESPECT and names Devesh Upadhyay, Christopher Vo, Chuchu Fan, and Nicholas Roy. Its **18 December 2025** year-end account still describes the collaboration and development. Neither examined page supplies a RESPECT repository, dataset, or executable demo.

- https://www.saab.com/markets/united-states/us-newsroom/stories/2025/darpa
- https://www.saab.com/markets/united-states/us-newsroom/stories/saabs-2025-wrapped-building-capability-driving-innovation-and-expanding-u.s.-manufacturing

### SEED-SET paper: related research, not yet contract-attributable

*SEED-SET: Scalable Evolving Experimental Design for System-level Ethical Testing* is an ICLR 2026 paper by Anjali Parashar, Yingke Li, Eric Yang Yu, Fei Chen, James Neidhoefer, Devesh Upadhyay, and Chuchu Fan. ArXiv records first submission **2 March 2026**, revision **11 March 2026**, under **CC BY 4.0**. The public paper acknowledges DARPA funding and public-release approval but does **not name ASIMOV or an award number**. Shared Saab/MIT investigators and ethical-testing subject matter make it a relevant lead, not a proven RESPECT deliverable. MIT's **2 April 2026** institutional account also says DARPA funded the work, without specifying ASIMOV. The paper's Appendix C.0.2 states: “Code for the simulation will be released upon request.” No request was sent.

- https://arxiv.org/abs/2603.01630
- https://arxiv.org/html/2603.01630v2
- https://news.mit.edu/2026/evaluating-autonomous-systems-ethics-0402
- https://proceedings.iclr.cc/paper_files/paper/2026/hash/94ab02a30b0e4a692a42ccd0b4c55399-Abstract-Conference.html

### What can actually be accessed

1. **Public project website:** https://anjaliparashar.github.io/seed-site/ . Readable research summary, figures and links. It advertises a blog walkthrough and Colab. Those advertisements alone do not establish a runnable software release.
2. **Public website repository:** https://github.com/MIT-REALM/seed-set-website . Repository description identifies SEED-SET; its README describes a research-website template and labels the **website** CC BY-SA 4.0. That license must not be silently applied to an unverified full research implementation. The repository contains `demo_lite.html` and static site assets. GitHub metadata shows latest commit **53dc895317ec4aa6872e6509b20560fcfe0d0632**, dated **21 April 2026 03:25:04 UTC**, message “Added blogpost and code”; the releases API returned **zero published releases**. A commit message is not proof of complete benchmark delivery.
3. **Public explanatory demo asset:** https://github.com/MIT-REALM/seed-set-website/blob/53dc895317ec4aa6872e6509b20560fcfe0d0632/demo_lite.html . Its explanatory text presents an illustrative power-grid ethics walkthrough, including surrogate-model widgets rather than a full trained-model run. Only text was inspected; interactive behavior was not tested. This supports **public demo/website assets**, not a verified executable benchmark. The deployed paths https://mit-realm.github.io/seed-set-website/demo_lite.html and https://anjaliparashar.github.io/seed-site/demo_lite.html both returned HTTP 404 during direct read-only checks.
4. **Different deployment:** https://mit-realm.github.io/seed-set-website/ returned HTTP 200 and retains the code-section wording **“To be released soon!”** It also retains some text and links from a different CoRL 2025 project. It should not be treated as a clean final-release manifest.
5. **Linked Colab:** https://colab.research.google.com/drive/1eNi_Ogxze1mkHXmp94bY0QWhxA3H7bT2?usp=sharing . Public web rendering exposed only sign-in text. Notebook contents, license, runtime requirements, and whether anyone without permission can open or execute it remain **unverified**. No authentication or runtime was initiated.
6. **Misleading code-link target:** the author project's footer links “Code” to https://github.com/MIT-REALM/contextual_failure . Its README identifies **Cost-aware Discovery of Contextual Failures using Bayesian Active Learning, CoRL 2025**, and GitHub identifies an MIT license. This is a different project, not verified SEED-SET or ASIMOV source code. The link may be a template remnant, but its cause is unknown.
7. **Blog links:** the author's top blog link resolves to the 404 `demo_lite.html` path above; another resources/footer blog link points to https://anjaliparashar.github.io/seed-site/blogpost.html , which the web-reading tool could not access. Do not count that failed read as a verified working demo or conclude that every access route is broken.

## 2. UNSW/ASU: announcements and investigator records, no verified release

The **24 January 2025** UNSW announcement for Adversarial Generative Ethics describes the research team and plans but does not link a released tool or dataset. The ASU Autonomous Collective Systems lab and its publications listing were inspected, alongside the investigator CVs already documented in the main people/output note. No project-specific release link was established. Older Pheeno robotics resources linked from the ASU lab are not evidence of an ASIMOV release.

- https://www.unsw.edu.au/news/2025/01/unsw-awarded-contract-to-develop-framework-for-measuring-ethical
- https://faculty.engineering.asu.edu/acs/
- https://faculty.engineering.asu.edu/acs/publications/
- https://search.asu.edu/profile/1943720/cv
- https://search.asu.edu/profile/559491/cv

Two additional current institutional profiles establish participation, not software access: **Mindika Premachandra**, UNSW senior research associate, describes prior work designing an ASIMOV ethics measurement system; **Jenna Allen**, now a UNSW World in Transition research associate, describes previous participation in UNSW's ASIMOV team. Neither page dates the transition precisely or supplies a release link. Do not infer termination or its cause from this wording.

- https://www.unsw.edu.au/staff/mindika-premachandra
- https://www.unsw.edu.au/canberra/our-research/world-in-transition

## 3. CoVar/Duality: GEARS announcements, generic platform access is not release evidence

CoVar's **20 December 2024** issuer announcement and Duality's **19 May 2025** announcement establish GEARS and the partnership. The inspected pages do not provide a public GEARS repository, dataset, executable, or benchmark download. Duality's generic resource library and FAQ do not establish GEARS release access. Its “Launch Falcon” link points to a commercial platform; the public text reader returned no substantive page contents. No account, trial, paid access, form submission, or platform execution was attempted. Generic Falcon availability cannot substitute for evidence that GEARS deliverables are publicly available.

- https://www.prnewswire.com/news-releases/covar-awarded-darpa-contract-to-define-ethical-standards-for-future-autonomous-systems-302337393.html
- https://www.duality.ai/news/duality-covar-asimov
- https://www.duality.ai/resource-library
- https://www.duality.ai/faq
- https://falcon.duality.ai/
- https://covar.com/products/

## 4. Bounded negative-search scope and false matches

This pass searched indexed public institutional/project pages and GitHub repository metadata/README text for ASIMOV with these teams, GEARS/its expanded name, RESPECT/its expanded name, Adversarial Generative Ethics, and relevant award identifiers. It also inspected the public MIT-REALM organization repository listing. GitHub README-search queries for the phrase “Responsible Ethical Standards” and identifiers FA865125CB006, FA865125CB007, and FA865125CB004 returned zero repositories. A “Gauging Ethical” query returned **Amir-Mann/LifePrioritizationSurvey**, whose README describes a separate KAIST-network survey, not CoVar/DARPA GEARS. No private repository, authenticated code search, comprehensive code corpus, or non-indexed institutional storage was searched.

- False match: https://github.com/Amir-Mann/LifePrioritizationSurvey
- Public organization metadata: https://api.github.com/orgs/MIT-REALM/repos?per_page=100&type=public
- Website commit metadata: https://api.github.com/repos/MIT-REALM/seed-set-website/commits?per_page=1
- Website release metadata: https://api.github.com/repos/MIT-REALM/seed-set-website/releases

## 5. Reproducibility and access records

Sanitized metadata records accompany this note: `software-query-metadata.json`, `mit-realm-repository-metadata.json`, `seed-set-access-metadata.json`, and `seed-set-demo-text-metadata.json`. They record exact URLs, UTC observation timestamps where collected, response hashes, and bounded results. They contain no downloaded executable, full paper, or retained source-code file. A response hash verifies the observed bytes if independently obtained; it does not establish historic availability before the observation date.

Selected response SHA-256 values:

- MIT-REALM SEED-SET deployed home page: `b1fe24e06f47ece2a060422057ad12781e77462a6683445bc2ec26707534ba23`.
- Pinned public `demo_lite.html` asset, text-only inspection: `784fcba2a0e49026eae5e257243748f4ecf3e7a35ce7fe6c1014e5020550653a`.
- Latest-commit API response: `40f1ad6b35a077d7fe687f3ebf9fb8368e8bc73470b5b928f78693ddfd13d2c8`.
- Empty releases API response: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
