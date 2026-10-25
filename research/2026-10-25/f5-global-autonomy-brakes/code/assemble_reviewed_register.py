#!/usr/bin/env python3
"""Merge authored F5 observations; explicit access and journalistic novelty.
Unknown body depth is not promoted. Raw outputs belong on Drive, not Git.
Standard library only; no network, authentication or publication operations.
"""
import argparse,csv,json,re
from pathlib import Path
from urllib.parse import urldefrag
RANK='''NATIVE-LEGAL-LR45 L-NL2026 A33 A34 A31 A35 N26 N07 US-SAF-01 US-SAF-04 US-SAF-02 L-AR2753 A01 A32 L-NSPM11 USPTO-11946710 USPTO-11768065 USPTO-12282340 NATIVE-NATO-E12 NATIVE-NATO-E06 NATIVE-NATO-F02 NATIVE-SAFETY-S20 NATIVE-SAFETY-S22 NZ-CUAS NATIVE-ALLIED-B10 NATIVE-ALLIED-B12 NATIVE-ALLIED-B11 NATIVE-ALLIED-B13 A02 A25 A28 A30 A17 A18 N01 NATIVE-NATO-N06 NATIVE-NATO-N23 N11 N12 N14 N15 NATIVE-NATO-F03 NATIVE-NATO-E13 NATIVE-NATO-E14 NATIVE-NATO-E10 US-SAF-05 US-SAF-06 US-SAF-16 US-SAF-18 US-SAF-27 US-SAF-17 L-AP136 NATIVE-LEGAL-LR12 NATIVE-LEGAL-LR02 L-231101 NATIVE-LEGAL-LR04 L-UK2016 L-AU2024 L-CA2024 L-MCKEE2025 F01 F02 F03 F04 F12 F16 P-US12175877B2 P-US12087171B2 P-WO2023167712A2 P-US20260022912A1 MERGED-PATENT-WO2025088600A1 NATIVE-LEGAL-LR08 NATIVE-LEGAL-LR35 NATIVE-LEGAL-LR36 NATIVE-LEGAL-LR38'''.split()
FIELDS='source_id aliases workstream title source_date source_url evidence_quality access_state source_basis claim_supported currentness implementation funding journalistic_novelty retrieval_provenance source_actor observation_independence limits promotion_status source_observations'.split()
UNKNOWN='Body-access depth not documented in supplied metadata; bibliographic/discovery use only, no full-text verification claim.'
NOVELTY='Previously public/context source; journalistic novelty not established. New retrieval alone is not a new finding.'
def load(p):return json.loads(Path(p).read_text())
def txt(v):return json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else str(v or '')
def key(u):return urldefrag(u)[0]
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['second-lane','native','integrated','out','reading-pack']:p.add_argument('--'+n,required=True,type=Path)
 a=p.parse_args();rows=[];byurl={};byid={};count=0
 def add(r,sid,lane,work='crosscut'):
  nonlocal count
  u=r.get('url',r.get('source_url',r.get('source')))
  if not isinstance(u,str) or not u.startswith('http'):return
  title=r.get('title',r.get('programme',sid));claim=r.get('claim_supported',r.get('claim',r.get('supports',r.get('status',r.get('functional_summary','')))))
  date=r.get('date',r.get('document_date_or_version',r.get('publication_date','Publication date not separately recorded')))
  quality=r.get('evidence_quality',r.get('quality',r.get('source_class',r.get('record_type',r.get('evidence_type','Authored source observation')))))
  access=r.get('access_state',r.get('access',UNKNOWN));limits=r.get('limits',r.get('limitation',r.get('limitations',r.get('missing',''))))
  obs={'id':sid,'lane':lane,'literal_url':u,'title':title,'date':date,'claim':claim,'quality':quality,'access_as_recorded':access,'limits':limits};count+=1
  if key(u) in byurl:row=byurl[key(u)];row['_obs'].append(obs);row['_ids'].append(sid)
  else:
   row=dict(source_id=sid,aliases=sid,workstream=txt(work),title=txt(title),source_date=txt(date),source_url=key(u),evidence_quality=txt(quality),access_state=txt(access),source_basis='Read depth as recorded by the identified reporting lane; no inferred full-body success.',claim_supported=txt(claim),currentness=txt(r.get('currentness','Document date/version above; retrieval on 2026-10-25 is not current implementation proof.')),implementation=txt(r.get('implementation','Only the source scope stated; no additional deployed-effectiveness claim.')),funding=txt(r.get('funding','No financial amount attributed from this source.')),journalistic_novelty=NOVELTY,retrieval_provenance='F5 source review on 2026-10-25; original IDs/lanes preserved in source_observations.',source_actor=txt(r.get('author_or_office',r.get('source_actor','Publisher/author; not an independent outcome auditor'))),observation_independence='Related mirrors, versions and agency reporting views are not automatically independent.',limits=txt(limits),promotion_status='context_or_discovery',_obs=[obs],_ids=[sid]);rows.append(row);byurl[key(u)]=row
  byid[sid]=row
 for group,file in [('allied','sources.json'),('safety','safety-source-register.json'),('patents-legal','source-register.json'),('financial','financial-sources.json')]:
  for i,r in enumerate(load(a.second_lane/group/file),1):
   sid=r.get('id',r.get('source_id','F%02d'%i));work=1 if sid.startswith('A') else 2 if sid.startswith('N') else 4 if sid.startswith('P-') else 5 if sid.startswith('L-') else 3;add(r,sid,'second/'+group,work)
   if group=='financial':byid[sid].update(access_state='Full award/action bodies read and hashed; official SBIR body read where this row is a technical-scope citation.',source_basis='New live receipts and targeted source audit; exact identities retained.',journalistic_novelty='Lifecycle denominator correction or scoped procurement lead; not deployed safeguard or first-reporting proof.',observation_independence='USAspending/FPDS are related agency views, not independent performance observations.')
 if (a.second_lane/'root-sources.json').exists():
  for i,r in enumerate(load(a.second_lane/'root-sources.json'),1):add(r,r.get('id','V%02d'%i),'coordinator',1)
 n=a.native/'f5-sources'
 for r in load(n/'nato-eu/primary-bibliography.json'):add(r,'NATIVE-NATO-'+r['id'],'native/nato',2)
 for r in load(n/'legal-updates/primary-bibliography.json')['sources']:add(r,'NATIVE-LEGAL-'+r['source_id'],'native/legal',5)
 for r in load(n/'allied/candidate_register.json')['candidates']:add(r,'NATIVE-'+r['id'],'native/allied-candidate',1)
 s=(n/'allied/allied_assurance_memo.md').read_text().split('## Ranked primary bibliography',1)[1]
 for line in s.splitlines():
  m=re.match(r'(\d+)\. \*\*(.*?)\*\*(.*)',line);urls=re.findall(r'\]\((https?://[^)]+)\)',line)
  if m and urls:add({'url':urls[-1],'title':m[2],'claim':re.sub(r'\[Source\]\(.*','',m[3]).strip(' .')},'NATIVE-ALLIED-B'+m[1].zfill(2),'native/allied-bibliography',1)
 for line in (n/'safety-boards/PRIMARY_BIBLIOGRAPHY.md').read_text().splitlines():
  c=[x.strip() for x in line.split('|')]
  if len(c)<6 or not re.fullmatch(r'S\d+',c[1]):continue
  for i,u in enumerate(re.findall(r'\]\((https?://[^)]+)\)',c[3])):
   add({'url':u,'title':c[2].replace('**',''),'claim':re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',c[3]),'access_state':c[4],'limits':c[4]},'NATIVE-SAFETY-'+c[1]+('' if not i else '-'+str(i+1)),'native/safety',3)
 for r in csv.DictReader((a.integrated/'data/patent-safeguards-register.csv').open()):
  for i,u in enumerate(json.loads(r['source_urls'])):add({**r,'url':u,'date':r['publication_date'],'claim':r['functional_summary'],'access_state':r['claim_read_status'],'implementation':r['implementation_evidence'],'limits':r['limitations']},'MERGED-PATENT-'+r['publication_number']+('' if not i else '-'+str(i+1)),'merged/patents',4)
 for r in load(a.second_lane/'patents-legal/official-uspto-verification.json')['records']:
  number=r['official_url'].rsplit('/',1)[1]
  add({'url':r['official_url'],'title':r['publication_number']+' official grant'+(' and correction certificate' if r.get('correction_certificate') else ''),'date':r['patent_date'],'claim':r['functional_verification'],'access_state':'Official image-only PDF downloaded HTTP 200; selected cover/claims visually read'+('; correction certificate read' if r.get('correction_certificate') else ''),'limits':r['limits'],'implementation':'No deployed outcome or current legal-status/ownership audit.'},'USPTO-'+number,'official/patent',4)
 add({'url':'https://www.nzdf.mil.nz/assets/Uploads/DocumentLibrary/EXP-26-MIN-0026_Counter-Uncrewed-Aircraft-Systems_Approval-to-Deliver.pdf','title':'NZ Cabinet minute EXP-26-MIN-0026 and paper','date':'2026-07-21; public release 2026-10','claim':'Acquisition approved alongside legal barriers to full capability use.','access_state':'Public release downloaded; image minute rendered/OCRed and selected governance page visually checked.','limits':'Not an AI-specific refusal or Article36 opinion; withheld supplier/legal detail not inferred.'},'NZ-CUAS','native/allied-late',1)
 applied=set()
 for file in ['allied-nato-access-overrides.json','legal-patent-access-overrides.json']:
  o=load(a.integrated/file)
  for x in o if isinstance(o,list) else o['records']:
   k=key(x['url'])
   if k not in byurl:continue
   for f in ['access_state','source_basis','claim_supported','implementation','funding','journalistic_novelty','source_actor','observation_independence','limits']:
    if x.get(f):byurl[k][f]=txt(x[f])
   applied.add(k)
 for sid in ['US-SAF-09','US-SAF-13']:
  r=next(x for x in load(a.second_lane/'safety/safety-source-register.json') if x['id']==sid);byid[sid].update(access_state=r['access'],claim_supported=r['claim'],evidence_quality=r['quality'],implementation=r['implementation'],promotion_status='excluded_as_substantive_current_body_authority')
 # Exact promoted-document dates and scope; do not confuse a record date with disclosure.
 byid['NATIVE-LEGAL-LR45'].update(title='Dutch SMASH disclosed governance bundle: advice, permission, change control and testing',source_date='Released 2026-10-09; search window 2020-01-01 through 2026-01-12',currentness='Contains dated 2021–25 governance records; does not establish current 2026 permission or field compliance.')
 byid['NATIVE-SAFETY-S20']['source_date']='2025-07-09 release; event 2025-07-03'
 byid['NATIVE-SAFETY-S22']['source_date']='2023-05-30 signed submission; event 2022'
 byid['NATIVE-ALLIED-B13']['source_date']='Applicant-guide filename revision 2025-09 for 2026 sandbox'
 byid['NZ-CUAS']['source_date']='Minute 2026-07-21; public release 2026-10'
 byid['F11'].update(access_state='Full native FPDS OtherTransactionAward feed read; three actions and feed aggregate checked. No verified USAspending award/transaction mapping.',source_basis='Exact native instrument 9700/HR0011269E126; no generated USAspending key invented.',observation_independence='One FPDS source view only; not a two-view reconciliation.')
 selected=[byid[sid] for sid in RANK];assert len(RANK)==75 and len({r['source_url'] for r in selected})==75
 missing=[(r['source_id'],r['title']) for r in selected if r['access_state']==UNKNOWN]
 if missing:raise ValueError('Explicit access required for ranked sources: '+str(missing))
 for r in selected:r['promotion_status']='ranked_source_with_explicit_scope'
 for r in rows:r['aliases']=';'.join(dict.fromkeys(r.pop('_ids')));r['source_observations']=json.dumps(r.pop('_obs'),ensure_ascii=False,separators=(',',':'))
 a.out.mkdir(parents=True,exist_ok=True)
 with (a.out/'global-brakes-master-register.csv').open('w',newline='') as f:w=csv.DictWriter(f,FIELDS);w.writeheader();w.writerows(rows)
 lines=['# F5 ranked reading pack: 75 primary sources','','Ranked for reporting value and evidence specificity. Related mirrors, statutes, patent family members and agency views are not independent proofs. Actual access and claim limits are explicit. Newly retrieving a source is not journalistic novelty. Wider source inventories remain on Drive.','']
 def readable(value):
  try:
   parsed=json.loads(value)
   if isinstance(parsed,list):return '; '.join(map(str,parsed))
  except (ValueError,TypeError):pass
  return value
 for i,r in enumerate(selected,1):lines += [f"{i}. **[{r['title']}]({r['source_url']})** — {r['source_date']}. {readable(r['claim_supported'])} Access: {r['access_state']}. Limit: {readable(r['limits'] or r['implementation'])}",'']
 body='\n'.join(lines)+'\n';assert len(body.encode())<=100000;a.reading_pack.write_text(body)
 audit={'source_observations_preserved':count,'distinct_source_urls':len(rows),'source_specific_overrides_applied':len(applied),'ranked_sources':75,'ranked_undocumented_access':0,'generic_see_memo_access_placeholders':sum('See source-specific' in r['access_state'] for r in rows),'unpromoted_undocumented_body_access':sum(r['access_state']==UNKNOWN for r in rows),'novelty_rule':'Journalistic novelty separate from retrieval provenance; no new-retrieval novelty default.','dedup_rule':'URL fragments consolidated; every literal URL and source observation retained. Distinct URLs do not equal independent evidence.'}
 (a.out/'source-register-assembly-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit))
if __name__=='__main__':main()
