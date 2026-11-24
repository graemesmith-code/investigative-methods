# Getting a ChatGPT dot through a long document review

24 November 2026

A reporter assigning several hours of work can give the dot one list of records, spell out what follows the first pass, and have it save evidence as it reads. The best firsthand example was a review of more than 7,600 pages. The operator found a follow-on job could sit idle even after space became available. Adding it to the assignment already running worked for them. One run later fell silent and the operator could recover only the last saved work. [Document-review account and follow-up comments](https://www.reddit.com/r/OpenAI/comments/1wuznlr/i_spent_a_day_poking_dots_with_sticks_heres_what/)

A second operator described a night in enough detail to judge the claim. An eight-hour assignment produced a draft plan and diagrams. The writer saw repeated work and review in the logs from 12:45 a.m. to around 6 a.m. They checked twice and gave one additional instruction. Their dot worked alongside another assistant on a connected work computer. They had told it to try another method when stuck, defer decisions that needed them, and carry on with the rest. [Japanese original](https://note.com/renkon40/n/n9a2676f7504e) · [English translation](https://note.com/renkon40/n/n9a2676f7504e?hl=en)

One researcher reported that their dot sometimes ignored the external notes they had prepared and repeated earlier research. Another user, working on local software, received assurances of progress before the dot acknowledged that nothing was running. For a reporting assignment, ask for the last saved record, the evidence behind it and the next unread record. OpenAI documents where to inspect delegated work in Activity. [Researcher's account](https://community.openai.com/t/feedback-on-dots-core-reliability-workflow-design-computer-control-and-user-experience/1415064) · [Local-task account](https://community.openai.com/t/dot-repeatedly-reports-progress-but-fails-to-complete-tasks-or-clearly-disclose-that-work-has-stopped/1402528) · [OpenAI guide](https://learn.chatgpt.com/docs/dots)

## A brief a reporter can reuse

> Use your cloud computer to review [list of records] for [reporting question]. Start now. This is one assignment. First examine the records, then check the most promising apparent matches against the primary documents and look for facts that would rule them out. Finish when both stages are complete or three hours have passed.
>
> Open [working file] before you begin. For each record, save its identifier, source link and page or passage, what you found, and whether you could actually read it. Save every ten records, or sooner if a single record takes a long time. Record the next unread item. Continue straight into the next batch.
>
> If one source is inaccessible, try another public route, record the gap if it persists, and move on. Leave decisions that need me in the file and keep working on independent items. If you resume after a pause, reopen the file, verify the last completed row, and continue from there.
>
> At the end send the file link, counts for records checked, inaccessible and still unread, and the strongest finding that survived verification. A result of zero is worth reporting.

**Optional check for silent stops.** Ask the dot to schedule one check an hour after launch. Have it reopen the working file and inspect the existing task. If work is active, leave it alone. If it has stopped with records outstanding and time remains, continue from the last saved item. If the dot delegates a task, its activity is visible under its desktop profile. Scheduled checks can be inspected under Scheduled. This is a proposed recovery measure. A second launch while work is still running can duplicate results. [OpenAI scheduling guide](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot)

The hour, ten-record batches and three-hour ceiling are proposed settings for a first trial. None of the accounts establishes an optimal interval. The practical test is whether one can open the file, verify the last record checked and give another researcher the next piece of work without reconstructing the conversation.

## Technical annex

**Evidence and limits.** This was a public-source review. Search terms combined ChatGPT dots with overnight work, hours, research, checkpoints, queues and resumption. We followed leads to the original Reddit discussion, an operator's Japanese write-up, developer-community reports and current OpenAI documentation. We did not run a new overnight trial. There is no basis here for a completion rate, a guaranteed runtime or a claim that the 7,600-page extraction was finished accurately. The Reddit post and its later comments are one operator's account.

**Execution conditions.** Cloud work can continue with the user's computer off. Work requiring files or apps on a connected computer requires that computer online with the ChatGPT app open. OpenAI advises restating essential requirements and linking the current working document. [Cloud and local execution](https://learn.chatgpt.com/docs/dots) · [OpenAI training guidance](https://developers.openai.com/training/walkthroughs/personalize-your-dot)

**Evidence manifest.** The dated source descriptions, URLs, acquisition date and limits are recorded in `dots-research-sources-2026-11-24.txt` in the reporting evidence folder. Its SHA-256 file checksum is `8e3d9fccbc70828ae59ce4207be9867faf9c6a46221ef5eb77e467e72370da7e`. The checksum identifies our saved source notes.
