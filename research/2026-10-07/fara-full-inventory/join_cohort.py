"""Discovery edges, not legal-entity equivalence or findings of concealment."""
import pathlib,json,sqlite3,re,unicodedata,collections
P=pathlib.Path(__file__).resolve().parent;E=P.parent/'lobbying-control-expansion'
SUFFIX={'inc','incorporated','corp','corporation','llc','ltd','limited','plc','llp','lp','co','company','the'}
GENERIC=SUFFIX|{'of','and','for','group','international','america','american','united','states','us','usa','association','council','national','institute','global','holdings','holding','services','systems','north','government','on','behalf','through','ministry','development','public','relations','communications'}
def tokens(name):return re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower())
def norm(name):return ' '.join(tokens(name))
def core(name):return ' '.join(x for x in tokens(name) if x not in SUFFIX)
def run():
    db=sqlite3.connect(P/'inventory.sqlite');fps=[json.loads(x[0]) for x in db.execute('SELECT payload FROM ForeignPrincipals')]
    clients=json.loads((E/'client-screen.json').read_text());annual={x['client_id']:x for x in json.loads((E/'annual-reconciled.json').read_text())}
    edges=[]
    for c in clients:
        name=c['client_name'];variants=[name]
        # Literal parenthetical aliases are retained as source text; no invented aliases.
        variants.append(re.split(r'\s*\(',name)[0].strip())
        distinctive={x for x in tokens(variants[-1]) if x not in GENERIC and len(x)>=4}
        for f in fps:
            target=f['Foreign Principal'];ft=set(tokens(target));reason=None
            if any(norm(v)==norm(target) for v in variants):reason='normalized_exact_name'
            elif any(core(v)==core(target) for v in variants):reason='corporate_suffix_only_difference'
            elif distinctive and distinctive<=ft:reason='all_distinctive_client_tokens_in_principal'
            if reason:
                a=annual[c['client_id']]
                edges.append({'client_id':c['client_id'],'lda_client':name,'income_lower_bound':a['income_known'],'expenses_lower_bound':a['expenses_known'],'major_after_amendments':a['major_reported_lower_bound'],'match_rule':reason,'fara_principal_row':f['row'],'fara_registration_number':f['Registration Number'],'fara_principal':target,'fara_registrant':f['Registrant Name'],'principal_registration_date':f['Foreign Principal Registration Date'],'principal_termination_date':f['Foreign Principal Termination Date'],'principal_source_lines':[f['line_start'],f['line_end']],'country':f['Country/Location Represented'],'identity_verified':False,'legal_inconsistency_established':False})
    edges.sort(key=lambda x:(not x['major_after_amendments'],x['client_id'],x['fara_principal_row']))
    (P/'cohort-principal-edges.json').write_text(json.dumps(edges,indent=2));print('edges',len(edges),'clients',len({x['client_id'] for x in edges}),'rules',dict(collections.Counter(x['match_rule'] for x in edges)))
    for id in sorted({x['client_id'] for x in edges}):
        e=[x for x in edges if x['client_id']==id];print(id,e[0]['lda_client'],'major',e[0]['major_after_amendments'],'edges',len(e),'principals',list(dict.fromkeys(x['fara_principal'] for x in e))[:8])
if __name__=='__main__':run()
