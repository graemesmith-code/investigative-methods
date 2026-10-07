"""Foreign-entity discovery across complete acquired annual forms and original RRs.

Positive entries identify disclosed relationships, never suspicious nondisclosure.
Empty metadata is not an original-form No response.
"""
import json,collections
from acquire import P,S
def enrich(screen,annual_rows,rr_rows):
 annual={r['filing_uuid']:r for r in annual_rows};by=collections.defaultdict(list)
 for r in annual.values():
  if r.get('foreign_entities'):by[r['client']['id']].append(r)
 rr={r['client_id']:r for r in rr_rows};out=[]
 for c in screen:
  c=dict(c);id=c['client_id'];a=by[id];registration=rr.get(id,{})
  c['initial_high_amount_foreign_entities_listed']=c.pop('foreign_additions_present',c.get('initial_high_amount_foreign_entities_listed',False))
  c['any_acquired_2025_foreign_entities_listed']=bool(a)
  c['acquired_2025_foreign_entity_filing_uuids']=sorted(r['filing_uuid'] for r in a)
  c['acquired_original_rr_foreign_entities_listed']=any(registration.get('foreign_entities',[]))
  c['history_expansion_selected']=c['country']=='US' and (bool(a) or c['acquired_original_rr_foreign_entities_listed'])
  c['foreign_field_interpretation']='Positive = entity listed in indicated source scope. False is not an original-form No or evidence of no foreign ownership.'
  out.append(c)
 return out
def run():
 screen=json.loads((P/'client-screen.json').read_text())
 rows=[r for f in S.glob('lda-annual-*.json') for r in json.loads(f.read_text())['results']]
 rr=json.loads((P/'rr-coverage.json').read_text());out=enrich(screen,rows,rr)
 (P/'client-screen.json').write_text(json.dumps(out,indent=2))
 selected=[{'client_id':r['client_id'],'client':r['client_name'],'annual_foreign_filing_uuids':r['acquired_2025_foreign_entity_filing_uuids'],'rr_positive':r['acquired_original_rr_foreign_entities_listed']} for r in out if r['history_expansion_selected']]
 (P/'history-expansion-selection.json').write_text(json.dumps({'base_checkpoint':'f673516593b62e4a96f9c4ba763d7c07244971fd','rule':'All screened US-domiciled client IDs with a foreign entity listed in any acquired 2025 form OR any acquired original RR. Positive disclosure is a chronology lead, not evidence of wrongdoing.','annual_forms':len({r['filing_uuid'] for r in rows}),'selected':selected},indent=2))
 changes=[{'client_id':r['client_id'],'client':r['client_name'],'initial_high_amount_positive':r['initial_high_amount_foreign_entities_listed'],'any_2025_positive':r['any_acquired_2025_foreign_entities_listed'],'source_uuids':r['acquired_2025_foreign_entity_filing_uuids']} for r in out if r['any_acquired_2025_foreign_entities_listed']!=r['initial_high_amount_foreign_entities_listed']]
 (P/'foreign-discovery-correction.json').write_text(json.dumps({'issue':'Prior field name omitted its initial >=$1m source scope; discovery now uses all acquired 2025 forms.','changed_clients':changes,'annual_positive_clients':sum(r['any_acquired_2025_foreign_entities_listed'] for r in out),'us_history_selection':len(selected)},indent=2));print('annual positive',sum(r['any_acquired_2025_foreign_entities_listed'] for r in out),'selected histories',len(selected),'changed',changes)
if __name__=='__main__':run()
