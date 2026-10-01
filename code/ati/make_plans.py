import json,pathlib,random
p=pathlib.Path(__file__).resolve().parents[2]/'research/2026-10-01/ati-live'
items=[
('leopard','dnd-mdn','A-2023-00105','What was publicly reported about Canada supplying additional Leopard 2 tanks, a recovery vehicle and 155mm ammunition in February 2023?','Canada February 2023 additional Leopard 2 tanks armoured recovery vehicle 155mm ammunition Ukraine'),
('china-permits','dfatd-maecd','A-2025-01773','Is the specific 2025 nuclear-related dual-use export decision identified publicly? Other China permit notes are merged for search triage; no approval or exporter is established.','Canada "00390-2025" nuclear dual use export permit China'),
('ukraine-budget','dnd-mdn','A-2022-01326','What public evidence identifies how the remaining 2022 $500 million Ukraine assistance budget was allocated?','Canada 2022 remainder 500 million military aid Ukraine spending allocation'),
('armoured-vehicles','dnd-mdn','A-2023-01996','Was the recommendation to donate 50 armoured vehicles to Ukraine already publicly reported?','Canada 50 armoured vehicles Ukraine donation December 2023'),
('gac-assignments','dfatd-maecd','A-2025-02439','What explains exclusion of traditional employees from round 3 of 2026 GAC assignments? The summary wording is not a verified finding.','Global Affairs Canada 2026 assignments round 3 traditional employees excluded'),
('israel-maple','dfatd-maecd','A-2023-03335','Recover the article named in the request and distinguish its published claims from still-unseen internal correspondence.','The Maple January 30 2024 Trudeau Government Admits Authorized New Military Exports Israel October 7'),
('nanisivik','dnd-mdn','A-2025-02587','What public record identifies the storage-tank compliance order, its conditions and remedy at Nanisivik?','Nanisivik naval facility environmental protection compliance order storage tank 2025'),
('ukraine-mines','dnd-mdn','A-2022-01530','What is documented about Ukrainian anti-personnel mine use in 2022, and is the separate Canadian-volunteer allegation evidenced?','Ukraine Canadian volunteer fighters anti personnel mines Ottawa Treaty 2022'),
('involuntary-care','dnd-mdn','A-2025-01384','Does public CAF policy already explain consent and involuntary mental-health admission?','Canadian Armed Forces policy involuntary admission mental health psychiatric consent'),
('biometrics','dnd-mdn','A-2025-00181','What public authority and safeguards govern collection of Canadian personnel biometric data during 2025 training?','Canadian Armed Forces 2025 biometric training Canadian citizens standing authority collect data'),
('audit-middle-east','dnd-mdn','A-2025-00661','Is the June 2025 CAF Middle East personnel movement already publicly explained?','Canada Canadian Armed Forces personnel Middle East June 2025 evacuation'),
('audit-petawawa','dnd-mdn','A-2024-00225','Can public sources identify a concrete safety issue at Petawawa Building Q-103 or its golf club?','Petawawa "Q-103" golf club safety'),
('audit-medical-fairness','dnd-mdn','A-2025-02382','Are the requested medical-policy fairness/accommodation standards already public?','Canadian Armed Forces medical policy procedural fairness disability accommodation DMEDPOL')]
def resolve_record(rows, owner_org, request_number):
 matches=[r for r in rows if (r['owner_org'],r['request_number'])==(owner_org,request_number)]
 if len(matches)!=1:
  raise ValueError(f'Expected one record for {owner_org}/{request_number}; found {len(matches)}')
 return matches[0]

def build_plans(rows):
 plans=[]
 for lead,owner,req,question,query in items:
  row=resolve_record(rows,owner,req)
  plans.append({'lead':lead,'request_number':req,'owner_org':owner,'selection':'seeded lower-half audit' if lead.startswith('audit') else 'top editorial cluster','rank_score':row['rank_score'],'question':question,'queries':[query],'source_summary':row['summary_en'],'pages':row['pages'],'disposition':row['disposition']})
 return plans

if __name__=='__main__':
 rows=json.loads((p/'full-ranked.json').read_text())
 (p/'coverage-plans.json').write_text(json.dumps(build_plans(rows),ensure_ascii=False,indent=2)+'\n')

def validate_plan(plan, rows):
 """Fail closed on missing identity or mismatched summary/metadata, before transport."""
 row=resolve_record(rows,plan['owner_org'],plan['request_number'])
 expected={lead:(owner,req) for lead,owner,req,*_ in items}
 expected['c22-control']=('dnd-mdn','A-2025-00945')
 if expected.get(plan['lead'])!=(plan['owner_org'],plan['request_number']):
  raise ValueError('Lead identity disagrees with reviewed composite identity')
 for key,source in [('source_summary','summary_en'),('rank_score','rank_score'),('pages','pages'),('disposition','disposition')]:
  if key in plan and plan[key]!=row[source]:raise ValueError(f'Plan {key} disagrees with source record')
 return row
