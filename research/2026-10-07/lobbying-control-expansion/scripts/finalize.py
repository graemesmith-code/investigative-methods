"""Build offline coverage, source index and reviewable evidence inventory."""
import json,hashlib,csv,collections
from acquire import P,S
rr=json.loads((P/'rr-coverage.json').read_text());annual=json.loads((P/'annual-coverage.json').read_text());amount=json.loads((P/'original-amount-verification.json').read_text())
rows={}
for f in S.glob('lda-*.json'):
 try:d=json.loads(f.read_text())
 except (ValueError,UnicodeDecodeError):continue
 if isinstance(d,dict):
  for r in d.get('results',[]):
   if isinstance(r,dict) and 'filing_uuid' in r:rows[r['filing_uuid']]=r
index=[]
for id,r in sorted(rows.items()):
 f=S/('original-'+id+'.html');b=f.read_bytes() if f.exists() else b''
 if b.startswith(b'%PDF'):
  # Retain immutable retrieval cache, add correctly suffixed offline viewing copy.
  f=S/('original-'+id+'.pdf')
  if not f.exists():f.write_bytes(b)
 index.append({'uuid':id,'client_id':r['client']['id'],'client':r['client']['name'],'registrant_id':r['registrant']['id'],'registrant':r['registrant']['name'],'year':r['filing_year'],'period':r['filing_period'],'type':r['filing_type'],'posted':r['dt_posted'],'original_url':r['filing_document_url'],'local_original':str(f.relative_to(P)) if b else '', 'sha256':hashlib.sha256(b).hexdigest() if b else ''})
with (P/'filing-index.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(index[0]));w.writeheader();w.writerows(index)
counts={'screen_filings':780,'screen_client_ids':259,'annual_queries_complete':sum(x['complete'] for x in annual),'annual_forms':sum(x['count'] for x in annual),'annual_ld2_amounts_checked':len(amount),'annual_ld2_amount_pairs_matching':sum(x['matches_api'] for x in amount),'rr_queries_complete':sum(x['complete'] for x in rr),'rr_queries_target':259,'rr_forms_recovered':sum(x['rr_count'] for x in rr),'rr_zero_result_queries':sum(x['rr_count']==0 for x in rr),'unique_catalogued_lda_filings_across_all_expansion_queries':len(index),'unique_original_lda_forms_across_expansion':sum(bool(x['local_original']) for x in index),'fara_report_entries':1598,'fara_report_normalized_strings_not_entities':859,'strict_name_edges':2,'loose_name_edges':131,'major_relationships_after_amendments':255,'new_jev_actual_calls':8,'jev_test_items':16,'jev_distinct_payloads':8,'combined_pilot_cost_estimate_usd':.003035,'combined_full_reservation_bound_usd':.15}
ra=json.loads((P/'missing-rr-ra-coverage.json').read_text())
timeline=json.loads((P/'ownership-timeline-coverage.json').read_text())
fara=json.loads((P/'fara-inventory-coverage.json').read_text())
counts.update({'complete_all_years_client_histories':timeline['relationships_with_complete_all_years_query'],'missing_rr_ra_queries_complete':sum(r['complete'] for r in ra),'missing_rr_ra_queries_target':len(ra),'missing_rr_ra_forms':sum(r['ra_count'] for r in ra),'missing_rr_ra_originals':sum(r['originals'] for r in ra),'missing_rr_queries_with_ra_recovery':sum(r['ra_count']>0 for r in ra),'historical_image_pdf_records_without_structured_field_parse':timeline['original_image_pdf_records_not_field_parsed'],'fara_active_rendered_inventory_rows':fara['active_rows'],'fara_terminated_rendered_inventory_rows':fara['terminated_rows'],'fara_unique_registration_numbers':fara['unique_registration_numbers'],'full_fara_principal_inventory_acquired':False,'full_fara_document_inventory_acquired':False})
(P/'final-coverage.json').write_text(json.dumps(counts,indent=2))
(P/'COVERAGE.md').write_text('# Coverage at this checkpoint\n\n'+'\n'.join('- '+k.replace('_',' ')+': **'+str(v)+'**' for k,v in counts.items())+'\n\nRR zero results are retrieval gaps, not evidence of missing registrations. Metadata and original acquisition are counted separately; acquisition does not mean every field was manually read. See REPORT.md and TECHNICAL-ANNEX.md for scope and exclusions.\n')
cases=[{'editorial_order':1,'client_id':64409,'client':'Prvo plinarsko drustvo d.o.o.','registry_ids':{'Croatia_MBS':'030070559','Croatia_OIB':'58292277611'},'lda_registrant_id':70175,'fara_registrant_number':6170,'major_in_acquired_relationship':False,'status':'Ownership disclosure question; exact filing-date chain and full FARA amendments missing','innocent':'Form interpretation or filing error; documented later service-scope change','missing':'Certified dated ownership extract and complete principal-specific amendment history'}, {'editorial_order':2,'client_id':68910,'client':'Arm Limited','registry_ids':{'UK_company':'02557590','UK_parent':'11299879'},'lda_registrant_id':86196,'fara_registrant_number':None,'major_in_acquired_relationship':False,'status':'UK ownership record vs particular LDA No; no FARA pair acquired','innocent':'Filing mistake or parent/client confusion; prior Carmen registration already discloses SoftBank','missing':'Filing-date share chain and explanation or correction of FGS response'}, {'editorial_order':3,'client_id':64167,'client':'KuCoin (unresolved legal entity)','registry_ids':{},'lda_registrant_id':401105040,'fara_registrant_number':None,'major_in_acquired_relationship':True,'status':'Abstain on disclosure inconsistency; brand/entity and date bridge missing','innocent':'Different legal entities and intervening governance change','missing':'Engagement agreement identifying exact client and contemporaneous share register'}]
for c in cases:c.update(jev_suspicion_score=None,source_dossier='REPORT.md',liability_or_intent_finding=False)
(P/'ranked-cases.json').write_text(json.dumps(cases,indent=2))
hashes={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(S.iterdir()) if f.is_file()}
(P/'source-hashes.json').write_text(json.dumps(hashes,indent=2));print(json.dumps(counts))
