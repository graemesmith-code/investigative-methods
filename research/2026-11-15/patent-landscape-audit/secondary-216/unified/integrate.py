"""Preserve original216 membership; normalize schemas without inflating reading depth."""
import json,csv,re,collections,hashlib,pathlib
P=pathlib.Path('/tmp/deep216'); O=P/'unified'
def load(p):return json.load(open(p))
records=load(P/'records.json'); ledgers=[load(P/'chunk1/review.json'),load(P/'chunk2/notes.json'),load(P/'chunk3/review.json'),load(P/'chunk4/review.json')]
official={x['index']:x for x in load(P/'acquisition.json')}
out=[]
for i,r in enumerate(records):
 c=i//54+1; raw=ledgers[c-1]; pid=r['publication_id']; parts=r['publication'].split('/'); num,kind=parts[-3:-1]; norm='EP'+num+kind
 if isinstance(raw,dict): n=raw.get(pid,raw.get(norm)); assert n is not None,pid
 else:
  matches=[x for x in raw if x.get('publication_id') in [pid,norm] or x.get('normalized_publication_id')==norm];assert len(matches)==1,(pid,matches);n=matches[0]
 row={'record_number':i+1,'original_publication_id':pid,'normalized_publication_id':norm,'epo_publication_uri':r['publication'],'publication_number':num,'kind':kind,'date':r['date'],'title':r['title'],'chunk':c,'original_queue_basis':r['review_basis'],'source_url':n.get('source_url',n.get('source',n.get('url',''))),'review_note':n.get('reading_note',n.get('assessment',n.get('finding',''))),'review_depth':n.get('review_depth',n.get('review_scope',n.get('reading_scope',''))),'review_basis':n.get('basis','see review_note'),'classification_as_authored':n.get('classification',n.get('class','not normalized')),'source_sha256':n.get('html_sha256',n.get('sha256_html','')),'reviewer_ledger':f'chunk{c}/'+('notes.json' if c==2 else 'review.json'),'original_review_record':n}
 # All A3 records remain separate, not silently replaced by companion application.
 if n.get('coverage')=='mapped_WO_selected_claims_only': status='mapped_WO_counterpart_claims_only_exact_EP_unverified'
 elif kind=='A3': status='search_report_publication_no_claims_reviewed'
 elif n.get('availability')=='unavailable' or n.get('status') in ['unavailable','404']:status='unresolved_source_access'
 else:status='targeted_substantive_claims_review'
 row['review_status']=status
 row['effective_reading_depth']=({'search_report_publication_no_claims_reviewed':'No claims reviewed in this A3 record; abstract/metadata where retrieved; no substantive negative inference','unresolved_source_access':'No substantive content review of exact publication; source access unresolved','mapped_WO_counterpart_claims_only_exact_EP_unverified':'Selected claims of mapped WO counterpart only; exact EP claims unverified'}.get(status,row['review_depth']))
 row['official_epo_acquisition_status']=official.get(i,{}).get('status','not logged')
 row['official_epo_xml_url']=official.get(i,{}).get('url','')
 row['actual_counterpart_url']='https://patents.google.com/patent/'+({'EP4795475A1':'WO2025082599A1','EP4795351A1':'WO2025082903A1'}[norm])+'/en' if norm in ['EP4795475A1','EP4795351A1'] else ''
 row['source_caution']='source_url is the reviewer attempted/default URL; official_epo_xml_url identifies official retrieval; mapped WO content is separate. See original_review_record and acquisition logs for actual source read.'
 row['same_ep_number_records']=[x['publication_id'] for x in records if x['publication'].split('/')[-3]==num]
 out.append(row)
assert len(out)==216 and len({x['epo_publication_uri'] for x in out})==216
(O/'unified_216.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
fields=[k for k in out[0] if k!='original_review_record']
with open(O/'unified_216.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in x.items() if k in fields} for x in out)
counts={'records':len(out),'unique_ep_publication_numbers':len({x['publication_number'] for x in out}),'unique_publication_uris':len({x['epo_publication_uri'] for x in out}),'review_status':dict(collections.Counter(x['review_status'] for x in out)),'kind':dict(collections.Counter(x['kind'] for x in out)),'family_count':'not established; EP number is not patent family','unresolved':[x['normalized_publication_id'] for x in out if x['review_status']=='unresolved_source_access'],'exact_EP_claims_unverified_counterpart_only':[x['normalized_publication_id'] for x in out if x['review_status']=='mapped_WO_counterpart_claims_only_exact_EP_unverified'],'A3':[x['normalized_publication_id'] for x in out if x['kind']=='A3']}
(O/'counts.json').write_text(json.dumps(counts,indent=2));print(json.dumps(counts,indent=2))
