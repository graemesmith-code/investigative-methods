"""Whole-inventory, role-preserving joins against original 2025 House XML.

Named foreign entities and affiliated organizations are distinct roles. Narrative
mentions are separately labeled, not assumed owners. This is discovery evidence.
"""
import json,pathlib,sqlite3,collections,difflib,re
from match_full_inventory import norm,core,temporal
P=pathlib.Path(__file__).resolve().parent

def run():
 h=sqlite3.connect(P/'house-filings.sqlite');h.row_factory=sqlite3.Row;f=sqlite3.connect(P/'inventory.sqlite')
 principals=[json.loads(x[0]) for x in f.execute('select payload from ForeignPrincipals')]
 bynorm=collections.defaultdict(list);bycore=collections.defaultdict(list);tokens=collections.defaultdict(set)
 for p in principals:
  bynorm[norm(p['Foreign Principal'])].append(p);k=core(p['Foreign Principal']);bycore[k].append(p)
  if len(k)>=12 and len(k.split())>=2:tokens[k.split()[0]].add(k)
 annual={x['house_relationship_id']:x for x in json.loads((P/'house-annual-provisional.json').read_text())};edges={};counts=collections.Counter();names=collections.defaultdict(set)
 def add(row,role,name,principals,rule):
  for p in principals:
   key=(row['house_id'],role,name,p['row']);item=edges.setdefault(key,{'house_relationship_id':row['house_id'],'lda_client':row['client'],'registrant':row['registrant'],'role':role,'printed_name_or_narrative':name,'principal_row':p['row'],'fara_principal':p['Foreign Principal'],'fara_registration_number':p['Registration Number'],'fara_registrant':p['Registrant Name'],'temporal_status':temporal(p),'rule':rule,'docids':[],'identity_verified':False,'provisional_major':annual.get(row['house_id'],{}).get('provisional_major',False)})
   item['docids'].append(row['docid'])
 for row in h.execute('select * from filings'):
  data=json.loads(row['payload'])
  for role,entities,field in [('foreign_entity',data['foreign_entities'],'name'),('affiliated_organization',data['affiliated_organizations'],'affiliatedOrgName')]:
   for ent in entities:
    name=ent.get(field,'').strip()
    if not name:continue
    counts[role+'_occurrences']+=1;names[role].add(name)
    exact=bynorm.get(norm(name),[]);add(row,role,name,exact,'normalized_exact')
    previous={x['row'] for x in exact};variant=[x for x in bycore.get(core(name),[]) if x['row'] not in previous];add(row,role,name,variant,'suffix_or_parenthetical_variant')
  for narrative in set(data['foreign_interest_narratives']):
   counts['foreign_interest_narratives']+=1;names['foreign_interest_narrative'].add(narrative);n=' '+norm(narrative)+' '
   keys=set().union(*(tokens.get(t,set()) for t in n.split()))
   for key in keys:
    if ' '+key+' ' in n:add(row,'foreign_interest_mention',narrative,bycore[key],'bounded_normalized_core_mention_min12_two_words')
 for e in edges.values():e['docids']=sorted(set(e['docids']));e['original_locator']='Named XML section for role; docid maps to archive/member/SHA256 in house-filings.sqlite. Interest mention does not prove ownership.'
 out=list(edges.values());(P/'full-role-edges.json').write_text(json.dumps(out,indent=2))
 summary={'xml_records_screened':109389,'fara_principal_rows_screened':len(principals),'role_occurrences':dict(counts),'distinct_role_name_or_text_strings':{k:len(v) for k,v in names.items()},'discovery_edges':len(out),'relationships_with_role_edges':len({x['house_relationship_id'] for x in out}),'role_edge_counts':dict(collections.Counter(x['role'] for x in out)),'major_relationships_with_role_edges':len({x['house_relationship_id'] for x in out if x['provisional_major']}),'scope':'All original archive versions, not only latest. Role occurrences and edges count repeated/versioned disclosures. XML paths preserve roles; API historical entity arrays are not promoted to original-field facts. No claim of exhaustive aliases, indirect chains, or legal identity.'}
 (P/'full-role-coverage.json').write_text(json.dumps(summary,indent=2));print(summary)
 for id in sorted({x['house_relationship_id'] for x in out if x['provisional_major']}):
  a=annual[id];ee=[x for x in out if x['house_relationship_id']==id];print(id,a['client_names'],a['provisional_expense_sum'],a['provisional_income_sum'],sorted({x['role'] for x in ee}),sorted({x['fara_principal'] for x in ee})[:5])
if __name__=='__main__':run()
