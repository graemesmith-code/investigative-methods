#!/usr/bin/env python3
"""Exact duplicate views and provenance index. Cross-source PIIDs remain candidate links."""
import collections,json,re
import pandas as pd
from acquire import ROOT,DATA,save_json
policies={};path=DATA/'normalized/sbir_current.parquet';sbir=pd.read_parquet(path);dedup=sbir.drop_duplicates('document_id',keep='first');dedup.to_parquet(DATA/'normalized/sbir_current_exact_deduplicated.parquet',index=False)
policies['sbir_current']={'input_rows':len(sbir),'exact_content_document_duplicates_removed':len(sbir)-len(dedup),'deduplicated_rows':len(dedup),'different_content_same_source_key_groups':int((dedup.groupby('source_record_id').size()>1).sum()),'policy':'Drop only exact identity/content duplicates. Different content with same composite source ID remains a separate version; no amount summation.'}
precedence=sorted(p.stem for p in (DATA/'normalized').glob('usaspending_dod_rd_fy*.parquet') if re.fullmatch(r'usaspending_dod_rd_fy\d{4}',p.stem))+['usaspending_dod_rd_contracts']+sorted(p.stem for p in (DATA/'normalized').glob('usaspending_dod_capabilities_fy*.parquet') if re.fullmatch(r'usaspending_dod_capabilities_fy\d{4}',p.stem))+['usaspending_dod_capabilities','usaspending_darpa','usaspending_dod_research_grants'];index={};piids=collections.defaultdict(set);source_rows={}
for source in precedence:
 p=DATA/'normalized'/f'{source}.parquet'
 if not p.exists():continue
 d=pd.read_parquet(p,columns=['transaction_key','document_id','award_key','record_sha256','identifiers_json']);source_rows[source]=len(d)
 for r in d.to_dict('records'):
  key=r['transaction_key'];entry=index.setdefault(key,{'transaction_key':key,'preferred_source':source,'preferred_document_id':r['document_id'],'award_key':r['award_key'],'representations':[],'row_hashes':set()});entry['representations'].append({'source':source,'document_id':r['document_id']});entry['row_hashes'].add(r['record_sha256']);ids=json.loads(r.get('identifiers_json') or '{}');piid=(ids.get('award_id_piid') or ids.get('award_id_fain') or '').upper().strip()
  if piid:piids[piid].add(r['award_key'])
rows=[]
for entry in index.values():
 entry['different_content_representations']=len(entry.pop('row_hashes'));entry['representation_count']=len(entry['representations']);entry['representations_json']=json.dumps(entry.pop('representations'));rows.append(entry)
d=pd.DataFrame(rows);d.to_parquet(DATA/'normalized/usaspending_unique_transaction_index.parquet',index=False)
links=[]
for r in dedup.to_dict('records'):
 contract=(json.loads(r.get('identifiers_json') or '{}').get('Contract') or '').upper().strip()
 if len(contract)<6:continue
 for award in piids.get(contract,[]):links.append({'sbir_document_id':r['document_id'],'contract_string':contract,'usaspending_award_key':award,'relation_type':'same_award_candidate','basis':'exact uppercased contract/PIID-or-FAIN string; agency/parent context still requires review','review_status':'unreviewed','financial_aggregation_permitted':False})
if links:pd.DataFrame(links).to_parquet(DATA/'normalized/sbir_usaspending_candidate_links.parquet',index=False)
policies['usaspending']={'source_rows':source_rows,'input_rows':sum(source_rows.values()),'unique_transaction_keys':len(d),'overlapping_representation_rows':sum(source_rows.values())-len(d),'keys_with_differing_content':int((d.different_content_representations>1).sum()),'precedence':precedence,'policy':'Index unique transaction keys; retain all alternate evidence references. Different row content requires vintage comparison. No spend totals computed.'};policies['candidate_cross_source_links']={'links':len(links),'distinct_sbir_documents':len(set(x['sbir_document_id'] for x in links)),'policy':'Candidate relationships only, never automatic capability/award merge or additional funding.'}
save_json(ROOT/'validation/deduplication.json',policies)
if links:pd.DataFrame(links).head(12).to_csv(ROOT/'samples/sbir_usaspending_candidate_links.csv',index=False)
print(json.dumps(policies))
