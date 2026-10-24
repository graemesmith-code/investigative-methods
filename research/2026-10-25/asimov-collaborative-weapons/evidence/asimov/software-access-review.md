# ASIMOV public tool access review

**Public sources inspected 24 October 2026.** This bounded follow-through asks what a member of the public can actually obtain, not whether a search engine can prove universal absence. It distinguishes papers, project descriptions, website assets, executable tools and complete benchmark datasets. No code was cloned, installed or executed; no account, trial, terms acceptance, paid access or outreach was attempted.

## Result

**No complete, publicly accessible software or dataset release attributable to one of the seven ASIMOV contracts was verified in the inspected sources.** This is not a finding that none exists or that contractual delivery failed. Three contract/programme-linked research outputs are now verified: Kitware's REBAR preprint, RTX's MAGNET paper, and a newly located Lockheed Martin team workshop manuscript. The latter corrects the earlier bounded finding that no Lockheed-specific publication had been located.

MIT/Saab's **SEED-SET** is a substantial related lead with a public paper and website/demo assets, but its ASIMOV attribution is not established. Its published access paths do not yet establish a complete runnable benchmark release. See the [detailed three-team access supplement](software-access-supplement-unsw-saab-covar.md).

## Seven performer access map

| Performer and identified work | Public material actually verified | Software or data access result |
|---|---|---|
| Kitware, CB001, REBAR | Full [18 May 2026 preprint](https://arxiv.org/abs/2605.18423), [HTML](https://arxiv.org/html/2605.18423v1), project announcements | No REBAR repository, dataset or runnable demo linked in the inspected paper or author/project pages. Paper license is CC BY 4.0, not a verified software license. |
| RTX, CB002, MAGNET; CALVIN subaward title | [5 July 2026 publisher abstract, affiliations and contract acknowledgment](https://link.springer.com/chapter/10.1007/978-3-032-30836-8_46) | Full chapter is subscription/paid content and was not accessed. No public MAGNET/CALVIN software, dataset or demo established. |
| STR, CB003 | DARPA performer announcement and primary award identity; contract description “Lethal Intelligent Autonomy” | No attributable release located through the bounded institutional, project-title, award-ID and GitHub searches. |
| CoVar, CB004, GEARS | CoVar and Duality announcements | No GEARS release linked. Generic commercial Falcon access is not evidence of a GEARS release. |
| UNSW, CB006, Adversarial Generative Ethics | UNSW/ASU announcements, lab pages and investigator records | No project-specific software or dataset release established in the inspected sources. |
| Saab, CB007, RESPECT | Saab announcements; related MIT/Saab SEED-SET paper and website | No RESPECT release verified. SEED-SET has public website/demo assets, but programme attribution and full runnable implementation remain unverified. |
| Lockheed Martin, CB018, Architecture Ethical Framework | Full [workshop manuscript](https://sites.cc.gatech.edu/ai/robot-lab/online-publications/CASEWorkshopFinal.pdf), explicitly acknowledging CB018 | No accompanying repository, dataset or executable-demo link in the inspected manuscript. Public-release permission on a paper is not a software license. |

## Kitware REBAR

The paper names Prose2JSON and REBAR-Orchestrator packages but does not supply a project-specific code or dataset link. Its GitHub links concern arXiv rendering support or cited work, not REBAR source. Its Falcon reference is a generic simulation-platform link.

The following were inspected: [Kitware's award announcement](https://www.kitware.com/kitware-awarded-3-9m-darpa-contract-to-develop-standards-for-evaluating-ethics-in-ai-driven-military-technologies/), [Duality's REBAR announcement](https://www.duality.ai/news/duality-kitware-asimov), [Basharat's institutional profile](https://www.kitware.com/arslan-basharat/), [Kitware's open-source catalogue](https://www.kitware.com/open-source/), [software-release listing](https://www.kitware.com/software-releases/), and corresponding author Jonathan Diller's [research](https://jond07.github.io/research.html) and [publication](https://jond07.github.io/publications.html) pages. No project-specific release link was established. The current release listing is not a comprehensive historical catalogue.

Duality's [1 June 2026 news item](https://www.duality.ai/news/rebar-robot-ethics) says the paper was presented at ICRA 2026. This is a dated team account of presentation, stronger than the preprint's prospective wording, but not proof of government acceptance or software release. Diller's current research page lists the manuscript as submitted to Springer Proceedings in Advanced Robotics, not as an accepted final report.

GitHub repository and indexed-file searches covered REBAR, its expanded title, Prose2JSON, REBAR-Orchestrator, ASIMOV and CB001 with/without hyphens. Kitware-scoped REBAR searches returned no match; its ASIMOV results were unrelated CMake test-version strings. The public [Kitware GitLab project search](https://gitlab.kitware.com/api/v4/projects?search=rebar&simple=true&per_page=100) returned an empty list.

One name collision warrants caution: [s0cks/prose2json](https://github.com/s0cks/prose2json) is a public Go/Ollama text-to-JSON utility created 15 October 2026. Its inspected README credits no ASIMOV, REBAR or performer. Its name alone does not establish identity with the package described in May's REBAR paper. It was not counted as a programme release.

## RTX MAGNET and CALVIN

The publisher makes the MAGNET abstract, authors and exact CB002 acknowledgment public. Its page has no project-code or supplementary-dataset link; it labels the chapter subscription content and offers paid access. The author's [public account of the HCI presentation](https://www.linkedin.com/posts/contactpeggywu_what-could-possibly-go-wrong-a-hazard-centric-activity-7502430688642740224-RMB9) links back to that chapter, not software.

Live [USAspending subaward records](https://api.usaspending.gov/api/v2/subawards/) verify a useful search alias: **Criteria for AI with Legally Informed Values and Nonmaleficence (CALVIN)**. CB002 reports Virginia Tech, $17,850 dated 5 December 2024, and SIFT, $60,000 dated 29 October 2024. The exact read request and response fields are in `rtx-calvin-subawards.json`. These are reported subawards within the prime, not additional programme spending to add to the prime total. CALVIN's relationship to MAGNET beyond their common contract is not explained by these records.

Exact-title/alias searches, SIFT/RTX/Virginia Tech domain searches and GitHub indexed-file/repository searches found no attributable release. SIFT's guessed on-site search URLs failed in the public text reader; that failure is not a negative search result for its entire site. No paywall or authentication restriction was bypassed.

## New Lockheed Martin output

*Towards Reliably Ethical Autonomous Weapon Systems* is a five-page publicly posted manuscript by **Ronald C. Arkin, Alan R. Wagner, Leete Skinner and Mark Hoffman**. Page 1 explicitly identifies DARPA **FA865125CB018** and gives Skinner and Hoffman's affiliation as **Lockheed Martin ATL, Cherry Hill**. Arkin is affiliated with Georgia Tech and Wagner with Penn State in the paper. These are publication-time affiliations, not proof of current employment or formal PI status.

[Arkin's university-hosted CV](https://sites.cc.gatech.edu/aimosaic/faculty/arkin/vita.html) dates the manuscript to the August 2025 IEEE CASE workshop on ethical considerations in robotics and automation. It also lists a May 2025 GETS presentation and an April 2026 APPE contribution, *Quantifying Ethical Difficulty: A Framework for Benchmarking the Decision-Making of Lethal Autonomous Weapons Systems*, by the same four authors. The latter two are presentation/publication records, not verified code releases; their complete texts were not established here.

The manuscript discusses assessment of legal and normative ethical readiness. This review records its existence, attribution and access, not detailed military implementation. The paper contains no public repository or dataset URL. Exact award identifiers, title/alias searches and Lockheed-scoped GitHub searches did not establish a software release.

## Bounds and remaining questions

The search included the programme name and expanded title, the four established project names, MAGNET/CALVIN, exact prime IDs, hyphenated ID variants, relevant university/company pages, public GitHub repository/indexed-file results and Kitware GitLab project metadata. Search-index coverage, default-branch indexing, capped result sets and unlinked institutional storage limit any negative conclusion. No private repositories or authenticated notebook contents were inspected. The queried GitHub organization strings are search scopes, not independent proof that every account is an official institutional account.

The immediate accountability questions are: Which accepted outputs can an outside researcher obtain today? Where are their licenses, reproducibility instructions and data? Are some deliverables available only on request or to government users? Which restrictions remain, and were the public-access intentions narrowed? None of those questions is answered merely by the completion banner or by the absence of an indexed download.

The new source hashes, GitHub query log and three-team supplement preserve reproducibility. Source-paper full text, executable code and personal administrative fields are not redistributed in this review.
