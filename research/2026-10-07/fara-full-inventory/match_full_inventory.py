"""Deterministic whole-inventory joins, including inactive and anomalous history.

Exact normalized names, documented punctuation/suffix variants and high-similarity
spelling candidates are separate rules. No rule asserts legal-entity identity.
"""
import sqlite3,json,pathlib,re,unicodedata,collections,difflib,datetime,decimal
P=pathlib.Path(__file__).resolve().parent
SUFFIX={'inc','incorporated','corp','corporation','llc','ltd','limited','plc','llp','lp','co','company','ag','sa','sas','bv','nv','gmbh','ab','as','doo','pvt','pty'}
def norm(name):
    name=re.sub(r'\b(?:[a-zA-Z]\.){2,}',lambda m:m.group().replace('.',''),name)
    name=unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower()
    return ' '.join(re.findall(r'[a-z0-9]+',name))
def core(name):
    words=norm(re.split(r'\(',name)[0]).split()
    while words and words[-1] in SUFFIX:words.pop()
    if words and words[0]=='the':words.pop(0)
    return ' '.join(words)
def temporal(r):
    def d(v):return datetime.datetime.strptime(v,'%m/%d/%Y').date() if v else None
    start=d(r['Foreign Principal Registration Date']);end=d(r['Foreign Principal Termination Date'])
    if end and end<start:return 'catalog_chronology_inconsistent'
    if start>datetime.date(2025,12,31):return 'starts_after_2025'
    if end and end<datetime.date(2025,1,1):return 'ended_before_2025'
    return 'overlaps_2025'
def amount(v):
    try:return decimal.Decimal(v.replace(',','').replace('$','')) if v else decimal.Decimal(0)
    except decimal.InvalidOperation:return decimal.Decimal(0)
def run():
    fdb=sqlite3.connect(P/'inventory.sqlite');hdb=sqlite3.connect(P/'house-filings.sqlite');hdb.row_factory=sqlite3.Row
    principals=[json.loads(x[0]) for x in fdb.execute('SELECT payload FROM ForeignPrincipals')]
    names=[x[0] for x in hdb.execute('SELECT DISTINCT client FROM filings')];by_norm=collections.defaultdict(set);by_core=collections.defaultdict(set);inverted=collections.defaultdict(set)
    for name in names:
        by_norm[norm(name)].add(name);key=core(name);by_core[key].add(name)
        for token in set(key.split()):
            if len(token)>=4:inverted[token].add(key)
    name_edges=[]
    for p in principals:
        raw=p['Foreign Principal'];key=core(raw);matched={n:'normalized_exact' for n in by_norm.get(norm(raw),set())}
        for n in by_core.get(key,set()):matched.setdefault(n,'punctuation_suffix_or_parenthetical_variant')
        if len(key)>=12:
            possible=set().union(*(inverted.get(t,set()) for t in key.split() if len(t)>=4 and len(inverted.get(t,set()))<=200))
            for other in possible:
                if other==key or len(other)<12 or min(len(key),len(other))/max(len(key),len(other))<.90:continue
                ratio=difflib.SequenceMatcher(None,key,other).ratio()
                if ratio>=.94:
                    for n in by_core[other]:matched.setdefault(n,'spelling_similarity_ge_0.94')
        for client,rule in matched.items():name_edges.append({'principal_row':p['row'],'principal':raw,'registration_number':p['Registration Number'],'fara_registrant':p['Registrant Name'],'principal_start':p['Foreign Principal Registration Date'],'principal_end':p['Foreign Principal Termination Date'],'temporal_status':temporal(p),'lda_client_name':client,'match_rule':rule,'identity_verified':False})
    relationships=collections.defaultdict(list)
    for row in hdb.execute('SELECT * FROM filings'):
        r=dict(row);key=r['house_id'] or r['senate_id']+'|'+r['registrant']+'|'+r['client'];relationships[key].append(r)
    by_client=collections.defaultdict(list);annual=[]
    for key,rows in relationships.items():
        quarters={}
        for r in rows:
            if r['quarter']=='registration':continue
            old=quarters.get(r['quarter'])
            if old is None or (r['signed'] or '',int(r['docid']))>(old['signed'] or '',int(old['docid'])):quarters[r['quarter']]=r
        income=sum((amount(r['income']) for r in quarters.values()),decimal.Decimal(0));expenses=sum((amount(r['expenses']) for r in quarters.values()),decimal.Decimal(0))
        record={'house_relationship_id':key,'client_names':sorted({r['client'] for r in rows}),'registrant_names':sorted({r['registrant'] for r in rows}),'senate_identifiers':sorted({r['senate_id'] for r in rows}),'form_count':len(rows),'quarter_count':len(quarters),'provisional_income_sum':str(income),'provisional_expense_sum':str(expenses),'provisional_major':max(income,expenses)>=1000000,'selected_quarter_docids':{q:r['docid'] for q,r in quarters.items()},'version_caveat':'Latest signed timestamp then numeric House document ID; verify against unified API posted-date chronology and originals before materiality claims.'}
        annual.append(record)
        for name in record['client_names']:by_client[name].append(record)
    edges=[]
    for e in name_edges:
        for rel in by_client[e['lda_client_name']]:edges.append({**e,**rel})
    # One edge can recur through different literal aliases. Keep evidence links;
    # de-duplicate only identical principal-row / relationship / name / rule tuples.
    edges=list({(e['principal_row'],e['house_relationship_id'],e['lda_client_name'],e['match_rule']):e for e in edges}.values())
    summary={'principal_rows_screened':len(principals),'distinct_principal_name_strings':len({p['Foreign Principal'] for p in principals}),'lda_client_name_strings_screened':len(names),'lda_house_relationships':len(annual),'name_edges':len(name_edges),'relationship_edges':len(edges),'principal_rows_with_edges':len({e['principal_row'] for e in edges}),'temporal_edge_counts':dict(collections.Counter(e['temporal_status'] for e in edges)),'rules':dict(collections.Counter(e['match_rule'] for e in edges)),'overlapping_major_candidate_relationships':len({e['house_relationship_id'] for e in edges if e['temporal_status']=='overlaps_2025' and e['provisional_major']}),'scope':'Every usable principal row, all five 2025 House archives. Historical/chronologically inconsistent matches retained separately. Name matches are discovery, never legal-entity proof.'}
    for file,data in [('full-inventory-edges.json',edges),('house-annual-provisional.json',annual),('full-match-coverage.json',summary)]:
        (P/file).write_text(json.dumps(data,indent=2))
    print(json.dumps(summary));print('OVERLAPPING MAJOR CANDIDATES')
    shown=set()
    for e in edges:
        if e['temporal_status']=='overlaps_2025' and e['provisional_major'] and (e['house_relationship_id'],e['principal_row']) not in shown:
            shown.add((e['house_relationship_id'],e['principal_row']));print(e['house_relationship_id'],e['lda_client_name'],e['registrant_names'],e['provisional_income_sum'],e['provisional_expense_sum'],'FARA',e['registration_number'],e['principal'],e['match_rule'])
if __name__=='__main__':run()
