# Evidence files and validation

Snapshot date: 16 October 2026.

## Contents

The [evidence directory](evidence/) contains **42 USAspending API response snapshots** and one [retrieval manifest](evidence/retrieval_manifest.json), making 43 JSON files:

- 14 award-detail responses
- 9 transaction-history responses for CETLAWS, TEELAWS and the seven ASIMOV awards
- 9 reported-subaward responses for the same awards, including empty responses
- 10 bounded search responses, including searches that returned no records

The two CSV ledgers are normalized views of the relevant award and subaward records. The [full contract report](CONTRACT_BREADCRUMBS.md) describes the search terms, period, source boundaries and unresolved joins. Primary award endpoints are linked in [ihl_prime_awards.csv](ihl_prime_awards.csv).

## Provenance and checks

The JSON responses were preserved with whitespace normalized. Manifest timestamps record retrieval-completion file timestamps; they are not the awards' action dates. Each manifest entry identifies a response file and its SHA-256 checksum.

Before publication:

- All 42 response files parsed as JSON and matched their manifest checksum.
- The award ledger contained 14 unique PIIDs; the reported-subaward ledger contained 16 rows.
- The nine saved transaction series reported no next page and reconciled to their award-level obligations.
- The seven ASIMOV award rows summed to $20,495,054 in obligations and $39,475,202 in base-plus-all-options values.
- Response content was checked for accidentally included credentials. No account keys or credentials are included.

The records are public government procurement data. No private contact directories, personal-life dossiers or copyrighted research-paper corpus are included. These files do not alter the original Pentagon-announcement backup.

## Interpretation limits

An empty search or subaward response is evidence of that query's result, not proof that the activity or collaborator does not exist. DoD procurement reporting has a 90-day public delay. Agency funding offices can differ from awarding offices. Modifications, obligations, potential values, subawards and programme budget figures are different units. Current and potential performance dates are not proof of present activity.

The records establish procurement facts. Legal validity, independent effectiveness, production deployment and successor ownership require other evidence. The reports distinguish directly retrieved API records from indexed documents, secondary reporting and unresolved leads.
