"""Resolve and acquire all major matched relationships, including historical FARA.

Legacy Senate identifiers ending -12 are not treated as modern API client IDs.
Reuse existing complete API histories; resolve missing IDs through the registrant
and 2025 filings. Preserve ambiguous mappings for review.
"""
import json,pathlib,collections,concurrent.futures
from extend_reverse import query,P,S,fetch
from match_full_inventory import core
E=P.parent/'lobbying-control-expansion'
def run():
    edges=json.loads((P/'full-inventory-edges.json').read_text());groups=collections.defaultdict(list)
    for e in edges:
        if e['provisional_major']:groups[e['house_relationship_id']].append(e)
    known={}
    for root,patterns in [(E/'sources',['lda-*.json']),(S,['lda-reverse-*.json','lda-followup-*.json'])]:
        for pattern in patterns:
            for f in root.glob(pattern):
                try:d=json.loads(f.read_text())
                except (ValueError,UnicodeDecodeError):continue
                if isinstance(d,dict):
                    for r in d.get('results',[]):
                        if 'filing_uuid' in r:known[r['filing_uuid']]=r
    selection=[{'house_relationship_id':k,'client_names':v[0]['client_names'],'registrant_names':v[0]['registrant_names'],'senate_identifiers':v[0]['senate_identifiers'],'fara_principal_rows':sorted({x['principal_row'] for x in v}),'all_temporal_classes_retained':True} for k,v in groups.items()]
    (P/'major-history-selection.json').write_text(json.dumps(selection,indent=2));out=[]
    for item in selection:
        prefixes={int(s.split('-')[0]) for s in item['senate_identifiers'] if s and s.split('-')[0].isdigit()}
        names={core(s) for s in item['client_names']}
        matches=[r for r in known.values() if r['registrant']['id'] in prefixes and core(r['client']['name']) in names]
        if not matches:
            for reg in sorted(prefixes):
                rows,coverage=query('major-resolve-'+str(reg),{'registrant_id':reg,'filing_year':2025})
                matches += [r for r in rows if core(r['client']['name']) in names]
        ids=sorted({r['client']['id'] for r in matches});item={**item,'resolved_client_ids':ids,'identity_caveat':'ID correspondence uses registrant identifier and normalized client name; underlying legal identity remains subject to original review.'}
        histories=[]
        for id in ids:
            old=E/'sources'/f'lda-history-{id}-summary.json';existing=None
            if old.exists() and json.loads(old.read_text()).get('complete'):
                existing={'client_id':id,'reused_from':str(old.relative_to(P.parent.parent.parent)),'complete':True,'forms':json.loads(old.read_text())['count']}
            if id==59928:
                previous=json.loads((P/'gotion-history-coverage.json').read_text());r=next(x for x in previous if x['params'].get('client_id')==id)
                existing={'client_id':id,'reused_from':'gotion-history-coverage.json','complete':r['complete'],'forms':r['count']}
            if existing:histories.append(existing);continue
            rows,coverage=query('major-history-'+str(id),{'client_id':id})
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:access=list(pool.map(lambda r:fetch('lda-original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None,rows))
            histories.append({'client_id':id,'complete':coverage['complete'],'forms':len(rows),'server_count':coverage['server_count'],'originals_acquired':sum(access)})
        item['histories']=histories;out.append(item);(P/'major-history-coverage.json').write_text(json.dumps(out,indent=2));print(item['house_relationship_id'],item['client_names'],histories,flush=True)
if __name__=='__main__':run()
