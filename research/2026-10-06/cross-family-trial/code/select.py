import pathlib,json,csv,hashlib,datetime
P=pathlib.Path(__file__).resolve().parents[1];ROOT=P.parents[1]/'2026-10-04'
rows=[json.loads(x) for x in (ROOT/'consequential-expansion-09/cross-batch-ranked-routes.jsonl').read_text().splitlines()]
# New uniform scores: severity, potential reach/materiality, public accountability, specificity of consequential contradiction; each0–4. Access excluded.
spec='''R01 sanctions 4 4 4 4
R02 sanctions 4 3 4 3
R03 sanctions 3 3 3 2
R04 sanctions 3 3 4 3
R05 medical_evidence 4 4 3 3
R06 environment 4 3 3 2
R07 environment 3 3 3 2
R08 environment 3 3 3 2
R09 environment 4 3 3 2
R10 trade 3 4 3 2
R11 aid_finance 3 4 4 2
R12 digital_rights 3 4 4 2
R13 environment 3 4 3 2
R14 energy 3 4 3 3
R15 space 3 3 4 3
R16 markets 3 3 4 3
R17 government_records 3 3 4 3
R18 sanctions 3 3 3 2
N01 aid_finance 3 4 4 2
N02 public_procurement 3 4 4 2
N03 defense 4 4 3 2
N04 legislation 3 4 4 3
N05 government_records 3 3 4 3
N06 government_records 3 3 4 2
N07 environment 4 4 3 2
N08 markets 3 3 3 3
N09 resource_finance 3 3 4 3
P01 medical_evidence 4 4 3 3
P02 transport_safety 4 3 4 3
P03 digital_rights 3 4 4 3
P04 environment 3 4 4 3
P05 markets 4 3 4 3
X02 extractive_revenue 3 4 4 3
X03 environment 4 3 4 4
X04 lobbying 3 3 4 4
X05 political_money 3 3 4 3
X06 lobbying 3 4 4 3
X07 environment 4 3 4 4
X08 environment 4 3 4 3
X09 resource_finance 3 3 4 4
X11 medical_evidence 4 4 3 4
X12 resource_finance 3 3 3 4
X13 corporate_assets 3 3 4 4
X14 markets 3 4 3 4
Z01 public_procurement 3 4 4 4
Z02 displacement 4 3 4 3
Z03 medicines_advertising 4 3 4 3
Z04 intellectual_property 3 4 3 3
Q02 political_money 3 3 4 4
Q03 sovereign_finance 3 4 4 4
V01 portfolio 3 4 3 4
B01 energy 4 3 3 4
B02 aid_finance 3 4 4 4
J01 conflict_evidence 4 3 4 3
J02 intellectual_property 4 4 3 2'''
score={}
for line in spec.splitlines():
 i,f,*n=line.split();score[i]=(f,list(map(int,n)))
assert len(score)==55
ref={'Q01':('R04','Registry/legal-status bucket; original S06 lineage, not identical predicate'),'REF-DISC01':('X04','Explicit declaration versus governing disqualification'),'REF-H01':('R05','Trial reporting obligations; original H01 lineage'),'X01':('R05','Medical-evidence disclosure bucket; original H04 lineage, not outcome switching'),'X10':('P05','Facility findings and documented corporate connection'),'REF-CONS':('X07','Approval before covered action'),'REF-D01':('R12','Infrastructure observation versus operative requirements; original D01 lineage'),'REF-EVID':('X11','Independence of evidence units'),'REF-MEP':('X04','Express interest declaration versus actual interest'),'REF-OUT':('R14','Exact generating unit and output/status'),'REF-REL':('V01','Portfolio issuer/control rules'),'REF-SEARCH':('N05','Records claim versus authenticated custody'),'REF-COMP':('X02','Specific obligation and actual satisfaction; also X07 timing'),'REF-INS':('P05','Precise risk assertion versus established finding'),'REF-AER':('X07','Restart permission before action')}
assert set(score)|set(ref)=={r['test_id'] for r in rows};assert not set(score)&set(ref)
rank=[];by={r['test_id']:r for r in rows}
for i,(f,n) in score.items():
 r=by[i];rank.append(dict(formulation_id=i,family=f,severity=n[0],reach_materiality=n[1],public_accountability=n[2],contradiction_specificity=n[3],consequence_total=sum(n),title=r['title'],source_file=r['source_file'],reason='Conditional consequence of the original card: '+r['title']+'. Scores concern a material established instance, not its probability or access.',access_separate=dict(prior_readiness=r['readiness_tier'],prior_effort=r['effort_tier']),attached_refinements=[j for j,(p,why) in ref.items() if p==i]))
rank.sort(key=lambda r:(-r['consequence_total'],r['formulation_id']))
strong=[];families=set()
for r in rank:
 if r['family'] not in families:strong.append(r['formulation_id']);families.add(r['family'])
 if len(strong)==6:break
seed='graeme-cross-family-2026-10-06-v1'
random_order=sorted((i for i in score if i not in strong),key=lambda i:hashlib.sha256((seed+'|'+i).encode()).hexdigest());random_ids=random_order[:3]
def exp(name,data):
 (P/(name+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in data))
 with (P/(name+'.csv')).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in data)
exp('uniform-consequence-ranking',rank)
exp('refinement-groups',[dict(refinement=i,parent_bucket=p,reason=why,sampling_weight=0,semantic_equivalence_claim=False) for i,(p,why) in ref.items()])
selected=[]
for arm,ids in [('high_consequence',strong),('random_comparison',random_ids)]:
 for i in ids:r=dict(next(r for r in rank if r['formulation_id']==i));r['arm']=arm;r['draw_sha256']=hashlib.sha256((seed+'|'+i).encode()).hexdigest() if arm=='random_comparison' else None;selected.append(r)
exp('frozen-nine',selected)
(P/'selection-provenance.json').write_text(json.dumps(dict(seed=seed,random_algorithm='Sort remaining49 IDs by SHA256 UTF8(seed + | + ID), take first3',source_commit='c29762cac5f31aa5b7886da446f3f6647288ddfb',primary_formulations=55,refinements_zero_extra_weight=15,grouping_note='Attached refinement buckets are operational sampling groups, not claims of exact semantic equivalence. Several original ancestor mechanisms are outside the55 detailed primary cards; original lineage is preserved.',strong_rule='Descending new uniform sum; lexical formulation ID ties; greedily take first6 distinct source families',selected_strong=strong,selected_random=random_ids,no_new_record_inspection_before_selection=True),indent=2)+'\n')
print(strong,random_ids)
