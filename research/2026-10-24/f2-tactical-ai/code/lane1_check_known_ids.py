import sqlite3,json
from pathlib import Path
B=Path(__import__('os').environ.get('F2_ROOT', str(Path(__file__).resolve().parents[1])));C=sqlite3.connect(B/'data/financial_actions.sqlite');C.row_factory=sqlite3.Row
ids=['HR0011269E197','M678542690040','HQ08452390066','HR001123C0150','FA228025C0002','H92405259E002','H92405239P004','HR00112490372','HR00112490430','HR00112590028'];o={}
for x in ids:o[x]=[dict(r) for r in C.execute('SELECT award_key,entity_name,COUNT(*) AS transactions,SUM(obligation_cents)/100.0 AS net_usd,MIN(action_date) AS first_action,MAX(action_date) AS last_action FROM transactions WHERE award_id=? GROUP BY award_key,entity_name',(x,))]
(B/'lane1/known_id_checks_after_validation.json').write_text(json.dumps(o,indent=2));print(json.dumps(o,indent=2))
