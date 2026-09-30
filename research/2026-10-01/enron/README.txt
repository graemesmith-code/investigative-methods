Enron original-filing retrospective mechanics demo

Start with report.md. Run python run_test.py using Python 3.9+ and network access. Missing original SEC documents are downloaded into sources/. Outputs go to output/.

The included manifest.json pins the originally checked source hashes. The script enforces these hashes before numerical computation and stops on mismatch; output/manifest.json records the verified run. No paid API key or non-standard library is required. Source hashes are byte-specific. A missing/invalid manifest or changed source stops the script; inspect the change rather than silently replacing the benchmark. Source retrieval can fail or be throttled; respect SEC access policy.

Numeric extraction was manual and verified; arithmetic and text rules are automated. This is not a blind model evaluation. The portable packet omits full source documents and full quotation caches. Original sources can be obtained by the script or verified URLs. Source line numbers are one-based original raw-file lines, not browser-rendered lines.

The fixed historical cutoff is end of March 31, 2000. The 2000-year Enron 10-K is explicitly excluded and used only for a later contradiction check. No privacy-sensitive user information is included.
