"""Temporal screen and explicitly recorded review; no liability scores."""
import json,datetime,pathlib,collections
P=pathlib.Path(__file__).resolve().parent
def date(x):return datetime.datetime.strptime(x,'%m/%d/%Y').date() if x else None
def run():
    edges=json.loads((P/'cohort-principal-edges.json').read_text());out=[];counts=collections.Counter()
    for e in edges:
        start=date(e['principal_registration_date']);end=date(e['principal_termination_date'])
        if end and end<start:status='inconsistent_catalog_chronology_no_temporal_inference'
        elif start>datetime.date(2025,12,31):status='principal_relationship_begins_after_2025'
        elif end and end<datetime.date(2025,1,1):status='principal_relationship_terminated_before_2025'
        else:status='catalog_dates_overlap_2025'
        counts[status]+=1;e={**e,'temporal_screen':status}
        if status=='catalog_dates_overlap_2025':
            if e['client_id']==200358:
                e.update(review='Corporate-group bridge retained; different named legal client and registrant. Original Zeno Exhibit A explicitly names Alibaba Group; no concealment conclusion.',review_source='https://efile.fara.gov/docs/6652-Exhibit-AB-20240201-14.pdf')
            else:e.update(review='Rejected as an identity match: shared generic/name token identifies different named legal entities or individuals. This is not a clearance of the LDA client.',review_source='Supplied ForeignPrincipals CSV row '+str(e['fara_principal_row']))
        out.append(e)
    (P/'reviewed-cohort-edges.json').write_text(json.dumps(out,indent=2))
    result={'generated_edges':len(edges),'client_ids_with_edges':len({e['client_id'] for e in edges}),'temporal_counts':dict(counts),'current_overlap_name_false_positives':sum(e['temporal_screen']=='catalog_dates_overlap_2025' and e['client_id']!=200358 for e in out),'retained_group_bridges_not_exact_legal_client_matches':sum(e['temporal_screen']=='catalog_dates_overlap_2025' and e['client_id']==200358 for e in out),'known_positive_recall_limitation':'PPD/Mercury, previously verified using original contract/address, is missed by this name-only baseline (LDA spelling DRUTVO vs FARA DRUSTVO and group suffix). Prior dossier remains in review; failure to generate an edge is not evidence of no relationship.','liability_scores_validated':False,'new_paid_calls':0}
    (P/'edge-evaluation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':run()
