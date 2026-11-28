# Can autoresearch help an investigative reporter?

**Background paper for Graeme Smith · 28 November 2026**

Yes. The best first use is a job you already do by hand. Give the system two editions of a government budget book and ask it to find the passages where a program’s stated plans or accomplishments changed. Let it try different ways of finding those passages. Judge each attempt by how many genuine changes a reporter can verify in the first ten results and how long that takes.

Your ASIMOV reporting supplies a good example. In June 2025, the Defense Advanced Research Projects Agency asked for money to finish a benchmark and check simulated scenes against field data. In April 2026, it reported developing an *initial* framework. Both passages are accessible. Finding them side by side is a task a machine can learn. Whether the field check happened is a question for the person who accepted the work, or the record of that acceptance. [1] [2] [3]

### What a harness adds

An ordinary research assistant follows an instruction and brings back an answer. An autoresearch harness lets it change **how it does the job**, run the new method on the same material, see which cases it missed and try again. The reporter supplies examples with known answers and decides what counts as an improvement. The useful product is a better search or comparison method that can be used on the next batch of records.

Andrej Karpathy’s original demonstration makes this distinction concrete. An agent could edit one training program, run it for five minutes, score how well the model predicted text, and keep or discard the change. A newsroom can borrow the experiment design using ordinary documents and an existing model. There is no reason to train a new language model for the proposed test. [4]

> I would pay for a machine that puts two revealing pages side by side before breakfast. I would be wary of paying for it to tell me why the second page reads differently. The first job saves an afternoon. The second may be the reason to spend that afternoon on the phone.

<!-- page -->

## What the evidence supports

### A newsroom has already done the underlying job

ProPublica found over 1,000 nonprofits had removed diversity-related wording. Reporters combined keyword searches, artificial intelligence and manual checks across two filing fields. [5] Imagine trying to do the Pentagon equivalent with a word count. If an office drops “independent review” in one paragraph and orders an outside review panel in the next, the counter will flag a disappearance. A reporter needs to see both passages to judge what survived. ProPublica demonstrates that comparing successive records can pay off. Its account leaves open how much an agent that revises the method would add.

### Your existing classifier offers a test of the extra value

TypeSafe, the maker of Jev, published a worked example using 2,000 Wikipedia requests that people had rated for politeness. One model proposed questions about the text, Jev answered them, and a separate program learned which answers predicted the human ratings. The first set of questions scored **0.471** on an error measure where lower is better. Five rounds of experimentation brought it to **0.456** on 800 examples withheld from the loop. That is about a 3% improvement over the first set. It is a vendor’s demonstration on a different task. It gives you a good reason to include one well-written, fixed prompt in any comparison. [6]

### Lower cost and better leads can come apart

Nicholas Hagar tested three ways for an agent to read 38 Chicago police documents. Across five tasks, his FieldGuide system used 27% fewer tokens and took 41% less time than direct file access. Yet the leads generated with direct access received higher average blind ratings. There were only five leads per method, and the raters often disagreed. A separate Northwestern study found that models matched the human panel’s exact newsworthiness score on roughly 14–46% of scorable cases, depending on the model. The panel also disagreed internally. Neither result settles who finds better stories. Both argue for measuring the work a reporter can actually use. [7] [8]

There is a further difficulty peculiar to discovery. A reporter may learn six weeks later that the oddest document in the pile mattered. Keep a separate list of unexpected finds and record which led to a new document, a useful interview or a decision to stop. That gives you a way to see what the formal score overlooked.

<!-- page -->

## Where it fits your reporting

In your “catch” method, one set of records describes an event, a rule predicts what another record should show, and the second source tests that expectation. A harness can try better ways to find the second record or match it to the first. The reporter owns the rule. Test a proposed match against a few deliberately mismatched records. If the same discrepancy appears when dates or entities are swapped, the rule may be detecting ordinary background noise. If an agent can quietly relax the rule whenever too few cases qualify, a productive-looking run may have changed the question.

| Reporting job | What the system can improve | What the reporter must settle |
|---|---|---|
| **Pentagon budget comparisons** | Match the same program across years, follow a transfer to a new account and return both passages with page numbers. | Was a task dropped, renamed, moved or completed elsewhere? Which office has the deliverable? [1] [2] [3] |
| **Contract and sanctions matches** | Test ways to catch spelling variants while rejecting namesakes. Reward correct identity, date and action type. | A transaction recorded after sanctions can implement a termination. Read what the action actually did before treating the match as new business. [9] |
| **Canadian access requests** | Rank summaries by whether they identify a specific, obtainable record that answers a defined question. Check a sample of low-ranked rows. | Your trial ranked 1,234 summaries, checked ten topics and obtained one release. Two further files were worth seeking. Their contents were still unknown. [10] |
| **Prior news coverage** | Test which queries recover known articles about the exact event, including cases where the headline used different words. | An empty result leaves coverage unresolved. Your reported miss of a known missile-defence story lacks the original query and article reference, so it needs reconstruction before it can be a scored test. [11] |

### What an overnight discovery run should hand back

An exploratory run can still range widely across the archive. Ask for a concrete discrepancy, the strongest ordinary explanation, the source that could distinguish them, and a reason to pursue or park the lead. Allow it to return zero. Review a few discarded cases. A quota of three surprising leads rewards a system for calling the third-best item a surprise, however weak the day’s records were.

<!-- page -->

## The first pilot

**Question.** Given the same budget documents and ten slots on your reading list, does an agent that revises its search method surface more verified changes than either a simple text comparison or a single careful prompt? The following numbers are proposed limits. This paper reports no new pilot results.

### Assemble the material

Start with 60 manageable program comparisons from consecutive budget editions. Use 30 for development, including known changes, and reserve 30 from different program families for the final test. Draw that second group from a defined list before seeing the outcomes. Keep transfers, reorganizations and passages with bad text extraction in scope. Give all three methods the same complete editions so they have a fair chance to find a relocated passage. The ASIMOV example belongs in development because its answer is already public. [1] [2] [3]

Read and label the pairs independently of the machine’s suggestions. Count a change when the documents show an addition, removal or material revision to a named task, test, deliverable or explicitly stated responsibility. Record transfers and rewordings that preserve the substance. Mark a pair unresolved if the record is incomplete. For each judgment, save the pages and a sentence saying what decided it. Add examples that defeat a literal word search to the development set. Keep the final draw intact, even if it contains fewer interesting cases than expected.

### Compare three methods on equal terms

| Method | What it gets to do |
|---|---|
| **A · Text comparison** | Match program titles and identifiers, then highlight changed sentences and rank the pairs by changes involving task or responsibility terms. |
| **B · One careful prompt** | Use the same documents and model as C. A reporter writes the instructions once, including how to handle transfers, and freezes them. |
| **C · Iterative method** | Start with B. See errors on the development cases, change one instruction or search rule per round, and record which change helped. Freeze the winner before the final test. |

Use the same output form for every method. Each card needs the program, two page references, the relevant wording in context and a narrow description of the change. Where a passage appears to vanish, record the successor section checked and the scope of the search. Set aside claims about motive or what happened outside the documents.

<!-- page -->

## Technical annex

### Score it against a reporter’s reading time

**Primary measure.** Count distinct, correctly documented changes in each method’s first ten cards on the 30 unseen pairs. Shuffle the cards and hide the method names during review. A hit needs the right program, the right passages and a supported description. Duplicates, unsupported claims and unfilled slots earn zero. Inspect the original page images. A printed page number and a file page number can differ.

**Check the misses.** Because the reporter labeled all 30 test pairs, also report how many confirmed changes each method found out of all confirmed changes, how many false alarms it produced and how many pairs remained unresolved. List any important case the simpler method found and the winner missed. A test with too few genuine changes to distinguish the methods is inconclusive. Still record what happened.

**Decision.** As a practical hurdle, advance C only if it yields at least two more verified changes in the first ten than the better of A and B, without increasing the time needed to verify ten cards. Record review time per method in a separate timed pass, balancing order or using a fresh reader to reduce familiarity effects. Treat a first win as permission to repeat the comparison on a fresh batch. A small trial cannot establish a general accuracy rate.

### Keep the experiment honest and affordable

**Freeze the test.** Give the agent access to the development answers only. Keep the final labels, the scoring procedure and the choice of test cases outside its editable workspace. Hold related program names, near-duplicate text and editions of the same project in one group. Repeatedly trying methods against the same supposed final test teaches the system its quirks. [12]

**Log each attempt.** Save the source file versions, page locations, model version, prompt or rule change, output, score, elapsed time and charges. Save failures and rejected changes too. On restart, resume from the last completed attempt. First confirm the reader can retrieve a known passage in the middle of a file. In your November document-hunting trial, a software error returned document openings even when the model requested later passages. [13]

**Stop rule and cost.** Cap the first comparison at €20 in model and search charges across all three methods, including the final comparison. Stop tuning after eight variants or three consecutive attempts without a gain, whichever comes first. That is 4% of your €500 ceiling for a story. Reserve the cost of the final comparison before tuning. Record human time separately. If labeling and setup take six hours and the tool later saves twenty minutes per batch, it takes eighteen batches to recover those six hours. For a one-off question, reading the files yourself may be cheaper.

<!-- page -->

## Sources and reading notes

**The worked example.** [1] [Defense Advanced Research Projects Agency, fiscal 2026 budget, printed p. 273][1]. Plans for completing and checking the benchmark. [2] [Fiscal 2027 budget, printed p. 310][2]. The agency’s later account of the initial framework. [3] [ASIMOV contract and budget check, 27 November 2026][3]. Your published reconciliation identifies the account transfer and the question the public records leave open.

**The original harness.** [4] [Andrej Karpathy, autoresearch experiment instructions][4]. See the sections on editable code, fixed evaluation, run length and retaining changes.

**The newsroom precedent.** [5] [Ellis Simani, “Deleting DEI,” ProPublica, December 2025][5]. See the reporting methodology below the story.

**The closest implementation to your workflow.** [6] [TypeSafe, “Autoresearch feature discovery”][6]. The published comparison includes direct scoring, the first proposed questions and the final result. The worked example is about politeness.

**Independent journalism studies.** [7] [Nicholas Hagar, “FieldGuide”][7], especially tables 1–2 and the limits of the blind lead ratings. [8] [Nick Hagar, Ethan Silver, Clare Spencer and Nicholas Diakopoulos, “LLM-Assisted News Discovery in High-Volume Information Streams”][8], table 2. One study compares document access methods. The other compares model judgments with human ratings on one beat.

**Your earlier trials.** [9] [Contract history behind a sanctions match][9]. [10] [Canadian access-to-information experiment][10]. [11] [Headline filter and missing reference][11]. These are trial accounts, with their original evidentiary limits.

**Evaluation and reproducibility.** [12] [Cynthia Dwork and colleagues, “The reusable holdout,” Science, 2015][12]. Explains how adapting decisions to repeated test results can undermine their validity. [13] [Document-hunting trial, 20 November 2026][13]. Records the failed passage reads, repair and limits on the cost estimate.

[1]: https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2026/budget_justification/pdfs/03_RDT_and_E/RDTE_Vol1_DARPA_MasterJustificationBook_PB_2026.pdf#page=296
[2]: https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2027/budget_justification/pdfs/03_RDT_and_E/RDTE_Vol1_DARPA_MasterJustificationBook_PB_2027.pdf#page=334
[3]: https://github.com/graemesmith-code/investigative-methods/blob/9de93ceee3cea4b2170a953fe73ef93b50963966/research/2026-11-27/asimov-contract-and-budget-check.md
[4]: https://github.com/karpathy/autoresearch/blob/master/program.md
[5]: https://www.propublica.org/article/deleting-dei-language-nonprofits-irs-forms
[6]: https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery
[7]: https://bpb-us-e1.wpmucdn.com/sites.northwestern.edu/dist/4/9200/files/2026/09/9288-Nicholas-Hagar.pdf
[8]: https://cplusj2025.com/wp-content/uploads/2025/12/LLM-Assisted-News-Discovery-in-High-Volume-Information-Streams.pdf
[9]: https://github.com/graemesmith-code/investigative-methods/blob/9de93ceee3cea4b2170a953fe73ef93b50963966/research/2026-10-14/nai-contract-history/README.md
[10]: https://github.com/graemesmith-code/investigative-methods/blob/9de93ceee3cea4b2170a953fe73ef93b50963966/experiments/07-canadian-ati.md
[11]: https://github.com/graemesmith-code/investigative-methods/blob/9de93ceee3cea4b2170a953fe73ef93b50963966/experiments/03-headline-filter.md
[12]: https://pubmed.ncbi.nlm.nih.gov/26250683/
[13]: https://github.com/graemesmith-code/investigative-methods/blob/9de93ceee3cea4b2170a953fe73ef93b50963966/research/2026-11-20/sid-2-document-hunting.md
