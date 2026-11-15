"""Rebuild the Site's read-only catalog from pinned, byte-checked Rabbit sources."""
import json, re, pathlib, hashlib, collections
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-root',required=True,type=pathlib.Path,help='Checked-out investigative-methods repository at the pinned revision')
parser.add_argument('--output-root',required=True,type=pathlib.Path,help='Destination for rebuilt Site data')
args=parser.parse_args()
BASE=args.source_root.resolve()
ROOT=args.output_root.resolve()
(ROOT/'data').mkdir(parents=True,exist_ok=True)
OUT=ROOT/'public/data'; (OUT/'records').mkdir(parents=True,exist_ok=True)
COMMIT='88ebd891e75d6448ecf7420ac2df3e6c1f0565a5'
REPO='https://github.com/graemesmith-code/investigative-methods'
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,separators=(',',':')))
def fields(s): return dict(re.findall(r'^- \*\*(.+?):\*\* (.*)$',s,re.M))
def val(d,k):
 v=d.get(k,'')
 return '' if v=='[not recorded]' else v
def provenance(path,line=1): return {'path':path,'line':line,'commit':COMMIT,'url':REPO+'/blob/'+COMMIT+'/'+path+'#L'+str(line)}
checks=[]; systems=[]; aps=[]; mappings=[]; details=[]
expected=json.loads((BASE/'references/rabbit/verification.json').read_text())['files']
for filename in ['Rabbit2(1).txt','Rabbit3.txt','Rabbit4.txt','Rabbit5.txt','Rabbit6.txt']:
 path='references/rabbit/originals/'+filename; b=(BASE/path).read_bytes(); sha=hashlib.sha256(b).hexdigest()
 assert sha==next(x['sha256'] for x in expected if x['path']=='originals/'+filename),filename
 checks.append({'path':path,'bytes':len(b),'sha256':sha}); text=b.decode(); heads=list(re.finditer(r'^## (SYS-\d+) — (.+)$',text,re.M))
 for i,h in enumerate(heads):
  raw=text[h.start():heads[i+1].start() if i+1<len(heads) else len(text)]; ident,name=h.groups(); line=text[:h.start()].count('\n')+1
  top=fields(raw.split('### Access points')[0]); p=provenance(path,line)
  system={'id':ident,'name':name,'organization':val(top,'Publisher') or val(top,'Official domain') or 'Not recorded','publisher':val(top,'Publisher'),'domain':val(top,'Official domain'),'country':val(top,'Normalized jurisdiction') or 'Not recorded','topic':val(top,'Coarse record family') or 'Not recorded','coverage':val(top,'Geographic coverage'),'access':sorted(set(x.strip() for x in val(top,'Access modes').split(';') if x.strip())),'url':val(top,'Representative URL'),'verification':val(top,'Verification status') or 'NOT_RECORDED','verifiedAt':val(top,'Verification date'),'historicalActive':val(top,'Final active'),'confidence':val(top,'Source-system confidence'),'provenance':p,'apIds':[]}
  ver=raw.split('### Verification and access controls',1)[-1] if '### Verification and access controls' in raw else ''
  access=raw.split('### Access points',1)[1].split('### Coverage mappings')[0]
  ah=list(re.finditer(r'^#### (AP-\d+) — (.+)$',access,re.M)); fullaps=[]
  for j,a in enumerate(ah):
   ar=access[a.start():ah[j+1].start() if j+1<len(ah) else len(access)]; aid,aname=a.groups(); f=fields(ar)
   sections=re.split(r'(?m)^#### ',ver); relevant=[v for v in sections if aid in v.split('\n')[0]]; vf=fields('\n'.join(relevant))
   ap={'id':aid,'systemId':ident,'name':aname,'organization':system['organization'],'country':val(f,'Normalized jurisdiction') or system['country'],'topic':val(f,'Normalized record family') or system['topic'],'access':sorted(set(x.strip() for x in val(f,'Access-point type').split(';') if x.strip())),'url':val(f,'Representative access URL'),'documentation':val(f,'Documentation URL'),'layer':val(f,'Layer'),'verification': ' / '.join(v.split('\n')[0].split(' / ')[-1] for v in relevant) or 'NOT_RECORDED','systemVerification':system['verification'],'verifiedAt':val(vf,'Verification date'),'provenance':provenance(path,line+raw[:raw.find(a.group(0))].count('\n')),'cost':val(f,'Cost or eligibility'),'joinFields':val(f,'Useful join fields'),'weakness':val(f,'Main weakness'),'summary':val(f,'Investigative relevance or methodology')}
   aps.append(ap);system['apIds'].append(aid); fullaps.append({**ap,'fields':f,'verificationFields':vf,'verificationText':'\n\n'.join(relevant),'raw':ar})
  maps=[]
  for m in re.finditer(r'^- \*\*(MAP-\d+) — (.*) — (.*?):\*\* (.*)$',raw,re.M):
   mid,country,topic,body=m.groups(); mf={'id':mid,'systemId':ident,'country':country,'topic':topic,'detail':body,'provenance':provenance(path,line+raw[:m.start()].count('\n'))};maps.append(mf);mappings.append(mf)
  detail={**system,'fields':top,'accessPoints':fullaps,'mappings':maps,'verificationText':ver,'raw':raw}
  write(OUT/'records'/f'{ident}.json',detail);details.append(detail);systems.append(system)
systems.sort(key=lambda x:x['id']);aps.sort(key=lambda x:x['id'])
assert len(systems)==len({x['id'] for x in systems})==1555
assert len(aps)==len({x['id'] for x in aps})==2516
assert [x['id'] for x in systems]==[f'SYS-{i:04}' for i in range(1,1556)]
assert all(a['systemId'] in {s['id'] for s in systems} for a in aps)
assert len(mappings)==len({x['id'] for x in mappings})==1739
candidates=[]
for folder,topic in [('job-postings-20261109','Job postings'),('patents-20261109','Patents'),('ai-weapons-research-20261109','Military technology')]:
 path='catalogs/additions/'+folder+'/sources.json';d=json.loads((BASE/path).read_text())
 for e in d['entries']:
  refs=e.get('original_rabbit_systems',[]);refs=[s for s in refs if s in {x['id'] for x in systems}]
  routes=e.get('endpoints') or e.get('official_urls') or e.get('sources') or []
  candidates.append({'id':e['id'],'name':e['name'],'organization':e.get('provider','Not recorded'),'country':e.get('jurisdiction','Not specified'),'topic':topic,'access':[e.get('route_type',e.get('source_class','Review access route')).replace('_',' ')],'url':next((u for u in routes if u.startswith('http')),''),'verification':'DOCUMENTATION_REVIEW','verificationNote':e.get('verification',''),'verifiedAt':e.get('reviewed_at',''),'relatedSystems':refs,'provenance':provenance(path),'original':e,'priority':e.get('priority','review'),'status':'candidate'})
manifest={'snapshotDate':'2026-11-14','commit':COMMIT,'repository':REPO,'systems':len(systems),'accessMethods':len(aps),'mappings':len(mappings),'candidates':len(candidates),'files':checks,'endpointRetests':0,'rules':['Historical active flags do not enable current collection.','Supplement IDs remain distinct from SYS and AP identifiers.','A current enabled route requires an explicit payload check and reuse review.','No endpoint collection or automatic refresh is configured.']}
write(OUT/'catalog.json',{'manifest':manifest,'systems':systems,'accessPoints':aps,'candidates':candidates,'mappings':mappings})
write(OUT/'full-catalog.json',{'manifest':manifest,'systems':details,'candidates':candidates})
write(ROOT/'data/targets.json',{x['id']:('system' if x['id'].startswith('SYS-') else 'access') for x in systems+aps})
write(ROOT/'data/review-seeds.json',candidates)
write(OUT/'manifest.json',manifest)
write(ROOT/'data/import-report.json',{**manifest,'uniqueIdentifiers':True,'unbrokenSystemRange':True,'allAccessMethodsHaveParents':True,'allSourceFingerprintsMatch':True,'verificationCounts':dict(collections.Counter(x['verification'] for x in systems))})
print(json.dumps(manifest,indent=2))
