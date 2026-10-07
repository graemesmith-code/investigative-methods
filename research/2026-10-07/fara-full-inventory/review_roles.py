"""Editorial adjudication of every major role match; preserve original XML context."""
import json,pathlib,sqlite3,zipfile,hashlib,collections
P=pathlib.Path(__file__).resolve().parent
NOTES={
'304790000':('explicit foreign-interest disclosure','Hyundai Seoul interest is expressly described; self/affiliate/owner must remain distinct. Historical API section-label counterexample retained.'),
'307150000':('corporate-group identity unresolved','Original says Zurich Insurance Group is parent; FARA name says Zurich Insurance Company. Do not merge them. Foreign parent interest is explicitly disclosed.'),
'308840000':('explicit foreign-ownership disclosure','Original describes Toyota Motor Corporation and 100% ownership of US subsidiaries. No concealment trigger from this role match.'),
'314340000':('explicit foreign-interest disclosure','Original names Nissan Motor Co., Ltd. and its US commercial interests. Narrative does not independently prove a complete current ownership chain.'),
'322070000':('explicit parent disclosure; FARA branch mismatch','Original names British American Tobacco plc as ultimate parent and refers to LD-1. Matched FARA record specifies a South America branch; that is not a verified identical principal.'),
'322480000':('membership/affiliate role, not assumed owner','Canadian railways and their US operations are explicitly described as association members. Their names do not establish ownership/control of the association.'),
'352130000':('explicit shareholder disclosure; percentages not current-certified','Original names Deutsche Telekom and SoftBank as shareholders. This is what the filer reports, not independent validation that historical percentages remain current.'),
'358040000':('explicit owner update','Original quarter-three update names Nippon Steel at 100%. A later acquisition and update do not by themselves establish earlier nondisclosure.'),
'413770000':('foreign-interest mention, not ownership','Northern Ireland Bureau / Embassy of Ireland appears as an interest narrative. It does not establish either body owns or controls Northeastern University. No ownership allegation follows.'),
'417350000':('explicit principal interest; substring false match','Original names Royal Bank of Canada. Bank of Canada is a nested-name false match and is rejected. Legal identity cannot be resolved by phrase containment.'),
'423740000':('explicit wholly owned subsidiary disclosure','Original says Samsung Electronics America is wholly owned by Samsung Electronics Co., Ltd. Malformed FARA quote rendering is not proof of a second entity.'),
'432110001':('explicit parent disclosure','Original calls Bank of Montreal the foreign parent and identifies its interest. No hidden-parent inference follows.'),
'442220001':('explicit foreign-entity chain narrative','Original names Nutrien Ltd., 10706957 Canada Inc., Agrium and Potash Corporation. Corporate reorganizations and exact current roles require dated records; names are already disclosed.')}
def run():
 edges=json.loads((P/'full-role-edges.json').read_text());groups=collections.defaultdict(list)
 for e in edges:
  if e['provisional_major']:groups[e['house_relationship_id']].append(e)
 assert set(groups)==set(NOTES),'Major role population changed; adjudicate new cases before proceeding'
 db=sqlite3.connect(P/'house-filings.sqlite');db.row_factory=sqlite3.Row;dest=P/'sources'/'selected-house-originals';dest.mkdir(exist_ok=True);out=[]
 for id,ee in sorted(groups.items()):
  originals=[]
  for docid in sorted({d for e in ee for d in e['docids']}):
   r=db.execute('select * from filings where docid=?',(docid,)).fetchone()
   with zipfile.ZipFile(P/'sources'/r['archive']) as z:raw=z.read(r['member'])
   assert hashlib.sha256(raw).hexdigest()==r['sha256'];path=dest/(docid+'.xml');path.write_bytes(raw)
   originals.append({'docid':docid,'archive':r['archive'],'member':r['member'],'sha256':r['sha256'],'file':str(path.relative_to(P)),'signed':r['signed'],'report_type':r['report_type']})
  out.append({'house_relationship_id':id,'client':ee[0]['lda_client'],'disposition':NOTES[id][0],'assessment':NOTES[id][1],'narratives_or_named_entries_reviewed':sorted({e['printed_name_or_narrative'] for e in ee}),'originals':originals,'not_a_compliance_clearance':True})
 (P/'major-role-review.json').write_text(json.dumps(out,indent=2));print('reviewed relationships',len(out),'selected original XML',sum(len(x['originals']) for x in out))
if __name__=='__main__':run()
