"""Offline final reporting/packaging; preserves the early immutable checkpoint."""
import json,csv,pathlib,hashlib,zipfile,collections
from normalize import OUT
from build import csvwrite,dump

def main():
 rows=[json.loads(x) for x in (OUT/'tests.jsonl').read_text().splitlines()];counts=json.loads((OUT/'counts.json').read_text());progress=json.loads((OUT/'progress.json').read_text());byid={r['test_id']:r for r in rows}
 progress['phase']='bounded_344_source_design_sweep_and_design_validation_complete'
 progress['remaining']='No bulk tests executed. Verify actual schema, lawful access, record coverage, historical dates and join identity for a selected recipe before promoting it to feasible. Deferred sources and unadmitted pairs remain open to future substantive mechanisms; no exhaustive hypothesis-space claim.'
 progress['rejected_nonduplicate']=counts['rejected_or_deduplicated']-counts['deduplicated'];progress['deduplicated']=counts['deduplicated'];progress['conditional_designs']=len(rows)
 progress['methodological_completion']='All 344 titles, fields, source roles and catalog limitations considered; policy enumerated every ordered pair; not every ordered pair individually reasoned through.'
 dump('progress.json',progress)
 # Refresh live join labels without falsely claiming the review was selected after all later rank changes.
 p=OUT/'review-sample.csv';reviews=list(csv.DictReader(p.open()))
 for r in reviews:
  assert r['test_id'] in byid;r['join']=byid[r['test_id']]['join_status']
 csvwrite(p,reviews)
 dump('review-selection-provenance.json',{'early_selection':79,'first_full_selection':1949,'final_selection':1738,'delivered_designs':len(rows),'final_selection_seed':20261004,'later_changes':'Removed six redundant ownership/licence routes and two registry-only vessel activity routes; no selected final-review IDs removed. Availability probes changed ranking; final sample is frozen from its selection snapshot, not falsely relabeled as post-probe top eight.','review_type':'same-session model defect-finding; no independent human review or field execution'})
 # Diverse reading queue; not a hidden change to numeric rank.
 examples=['T-S01-0024-0054','T-S04-0024-0074','T-S02-0024-0004','T-E01-0030-0060','T-E03-0053-0004','T-E04-0054-0116','T-I05-0117-0126','T-C01-0217-0214','T-C04-0302-0106','T-C08-0225-0183','T-W01-0091-0210','T-W06-0057-0091','T-H02-0248-0250','T-H04-0247-0248','T-F02-0069-0070','T-D04-0341-0336']
 chosen=[byid[i] for i in examples];csvwrite(OUT/'reading-queue.csv',chosen)
 intro=f'''# A menu of investigative tests

**{len(rows):,} conditional source-pair recipes, organized under {counts['mechanism_rules']} investigative mechanisms.** These are reporting questions, not findings about any person or organization. None is yet confirmed executable. Some will fail at the first record check.

Start with [the reading queue](reading-queue.csv): sixteen varied examples selected for consequence and teachability. Or sort [all recipes](tests.csv) by the separate public-interest, testability, join-confidence and cost columns. The numeric ranking is an editorial heuristic, not a probability of misconduct. Different source implementations of one mechanism are alternatives, not independent discoveries.

The sweep considered all **344 Rabbit descriptions with explicit Useful join fields**. {progress['source_participation']} sources enter the longlist; {progress['sources_support_or_deferred']} remain support, context, access-constrained or insufficiently specified sources. We deliberately stopped below 5,000: reaching that number would require weaker combinations or padded variants. The remaining sources are accounted for in the inventory, with their catalog-specific limitations.

| Count | Meaning |
|---|---|
| {counts['expanded_candidates']:,} | Role-compatible candidate expansions |
| {progress['rejected_nonduplicate']:,} | Rejected by substantive/coverage gates |
| {counts['deduplicated']} | Collapsed as duplicate evidence paths or mirrored access |
| {len(rows):,} | Retained conditional source-pair designs; all pass schema/provenance checks |
| 0 | Record-level tests executed |
| 0 | Confirmed feasible/executable investigative tests |

[Download the complete checkpoint](checkpoints/source-test-discovery-checkpoint.zip). The [early 79-design checkpoint](checkpoints/early-checkpoint.zip) is preserved as published; later corrections supersede it. [Journalists’ guide](journalists-guide.md) explains the sixteen starting recipes. [Quality review](quality-review.md), [ranking rubric](ranking-rubric.md) and [reproduction instructions](reproduce.md) explain how to assess the list.

The most important methodological result: **identity, activity and applicable rule are separate questions**. A shared name is provisional. A registered asset may be frozen, a contract action may be a termination, and an ownership label may describe control rather than shares. Every retained recipe lists ordinary explanations and a cheap next check.

Three small free access probes produced two single-record responses (GLEIF and ClinicalTrials.gov) and one HTTP 403 failure (CISA schema). These are availability checks, not investigative matches. Selected official documentation was also read; all other availability remains unverified. No paid model/search API calls and no bulk investigative execution occurred.

Technical annexes: sources.jsonl and source-manifest.json preserve SYS/AP IDs and byte/line hashes; source-coverage.csv and source-capabilities.jsonl account for every source; join-field-dictionary.csv classifies the labeled fields; pair-universe.csv.gz records all 117,992 ordered source pairs. That pair file is a deterministic policy ledger, **not 117,992 individually reviewed hypotheses**. Rejected candidates, literal model-authored mechanisms, code, sampled defect reviews, evidence logs and progress.json support continuation.

The repository stays private. No source licensing, repository access or visibility was changed. Weekly ChatGPT allowance and token telemetry are unavailable; the user's last reported 99% remaining is historical and cannot quantify this run. New paid API calls: zero.
'''
 (OUT/'README.md').write_text(intro)
 guide='''# How to try one question cheaply

Pick a concrete public-interest event, entity, project or claim. Read the two source descriptions and their weaknesses. Verify the schema and one permissible record before collecting more. Save the raw record, source URL, retrieval date and effective period. Check the proposed identity or location independently. Read the disqualifiers before interpreting any result.

A failed access request belongs in the log. A failed join belongs in the rejected list. A missing search result is not absence evidence. Use agency records, legal text, full filings or a suitable measurement model to resolve the remaining question; offer affected parties the underlying evidence and seek their explanation before publication.

These sixteen examples are a varied reading queue, not an override of the full numeric ranking. Time estimates cover a first documentation check only; historical documents, data cleaning and expert interpretation may be expensive. None is a ready-to-run accusation or a validated executable test.

'''
 for n,r in enumerate(chosen,1):
  guide+=f"## {n}. {r['source_a_name']} → {r['source_b_name']}\n\n**{r['test_id']} · {r['family']}**\n\n{r['initial_observation']} {r['expected_observation']}\n\nWhy it matters: {r['basis']}\n\nInteresting result: {r['interesting_outcome']}\n\nTry first: {r['next_cheapest_check']}\n\nJoin: {r['join_recipe']}\n\nOrdinary explanations: {r['ordinary_explanations']}\n\nStop or qualify: {r['disqualifiers']}\n\nEvidence needed: {r['required_evidence']}\n\n"
 (OUT/'journalists-guide.md').write_text(guide)
 # A complete manifest excluding its own digest, the bundle and post-packaging delivery receipt.
 files=[p for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name not in ['artifact-checksums.json','delivery-receipt.json'] and p.suffix!='.zip']
 dump('artifact-checksums.json',{str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)})
 bundle=OUT/'checkpoints/source-test-discovery-checkpoint.zip'
 with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(files+[OUT/'artifact-checksums.json']):
   info=zipfile.ZipInfo(str(p.relative_to(OUT)),date_time=(2026,10,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
 with zipfile.ZipFile(bundle) as z:assert z.testzip() is None
 print(json.dumps({'bundle':str(bundle),'bytes':bundle.stat().st_size,'sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),'included_files':len(files)+1,'designs':len(rows)}))
if __name__=='__main__':main()
