# What to do next

The next useful result is a small, fully documented comparison. Expanding the corpus before preserving evidence would make the method harder to evaluate.

1. **Recover the latest evidence.** Export the ten original contract paragraphs, all 100 lead–article pairs, exact queries, source dates, prompt/model versions, corpus date range, code revision and manual reassessment decisions. Preserve missing fields explicitly if they cannot be recovered.
2. **Resolve the Anduril case.** Recover exact alleged prior-coverage URLs and compare them with the saved Exa results for FA881926DB0011. Decide whether the problem was retrieval, classification, a different event, or remains uncertain.
3. **Create known controls.** Use covered contract events with known article URLs, including the missed WSJ THAAD example once its exact reference is recovered. Test whether the same retrieval settings can find them.
4. **Compare on the same reviewed records.** Freeze a modest corpus and label it manually before viewing model ranks. Include routine actions, zero-dollar modifications, options, known covered events and worthwhile questions. Run simple rules and rules plus Jev on those same records.
5. **Record real costs and human time.** Preserve charges, credits, retry counts and reviewer minutes. Count useful leads using a definition fixed before ranking. Audit random rejected records for important misses.
6. **Keep or stop based on evidence.** Retain a method if it materially improves useful leads or reviewer time while preserving important controls. If it cannot beat a spreadsheet and simple rules, document that result and change the method.

These steps are proposals, not completed experiments. A later public-sharing decision can use this notebook, but the current repository is private and no public release or licence is part of this work.

[Home](../README.md) · [Run template](../templates/run.md)
