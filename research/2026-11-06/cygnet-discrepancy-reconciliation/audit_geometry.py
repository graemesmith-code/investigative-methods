#!/usr/bin/env python3
"""Offline Cygnet provenance-preserving geometry comparison; never rewrites inputs."""
import argparse,csv,hashlib,importlib.util,json,math,pathlib,re
import fitz
ROOT=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--pdf-dir',type=pathlib.Path,required=True);p.add_argument('--prior-dir',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('prior',a.prior_dir/'methods/surveys/interpolate_pdf_surveys.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
manifest=json.loads((a.prior_dir/'private_source_audit/survey_input_manifest_private.json').read_text())
SERVICES={'A':['TR,33458569,0516327,00_07-33-037-28W4_0,z2.pdf'],'B':['split file1a.pdf','split file1b.pdf'],'C':['split file2a.pdf','split file2b.pdf']}
LIC={'A':'0516327','B':'0516328','C':'0515889'}
DETAIL=re.compile(r'Stage (\d+) of (\d+) on the (.+?) is now complete\.')
def number(s,label):
 q=re.search(re.escape(label)+r'\s+([\d,]+(?:\.\d+)?)\s+m(?:\s|$)',s);return float(q[1].replace(',','')) if q else None
surveys={};summaries={};details=[];comparison=[];hashes=[]
for w,(drill,service,n) in manifest.items():
 surveys[w]=m.get_surveys(a.pdf_dir/drill)
 d=fitz.open(a.pdf_dir/service);rows=[(int(x[1]),float(x[2]),float(x[3])) for x in m.STAGE_RE.finditer(d[2].get_text())];assert len(rows)==n
 summaries[w]={stage:(top,bottom) for stage,top,bottom in rows}
 for f in SERVICES[w]:
  doc=fitz.open(a.pdf_dir/f)
  for page,pdfpage in enumerate(doc,1):
   s=pdfpage.get_text();mch=DETAIL.search(s)
   if not mch:continue
   stage=int(mch[1]);top=number(s,'Top Perforation Depth');bottom=number(s,'Bottom Perforation Depth');plug=number(s,'Plug Set Depth')
   detail=dict(well=w,licence=LIC[w],stage=stage,service_file=f,service_page=page,detail_identity=mch[3],detail_top=top,detail_bottom=bottom,detail_plug=plug,expected_stage_count=n,detail_stage_count=int(mch[2]))
   details.append(detail);st,sb=summaries[w][stage]
   comparison.append(dict(detail,summary_file=service,summary_page=3,summary_top=st,summary_bottom=sb,top_diff_m=None if top is None else top-st,bottom_diff_m=None if bottom is None else bottom-sb,summary_reversed=st>sb,identity_consistent=int(mch[2])==n))
 for f in [drill,*SERVICES[w]]:
  fpath=a.pdf_dir/f;hashes.append(dict(file=f,sha256=hashlib.sha256(fpath.read_bytes()).hexdigest(),physical_pages=len(fitz.open(fpath))))
def write(name,rows):
 with (a.out/name).open('w',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
write('all_service_details.csv',details);write('summary_detail_comparison.csv',comparison)
(a.out/'input_hashes.json').write_text(json.dumps(hashes,indent=2))
bad=[r for r in comparison if r['top_diff_m'] or r['bottom_diff_m'] or r['summary_reversed'] or not r['identity_consistent']]
print('COUNTS',len(details),{w:sum(x['well']==w for x in details) for w in LIC});print('DIFFERENCES',json.dumps(bad,indent=2))
# Compare prior geometry to fresh parse; report precisely if its CSV carries any changed values.
prior=list(csv.DictReader((a.prior_dir/'private_source_audit/stage_locations_private.csv').open()))
issues=[]
for r in prior:
 w=r['well'];stage=int(r['stage']);st,sb=summaries[w][stage];md={'top_perforation':st,'bottom_perforation':sb,'midpoint':(st+sb)/2}[r['position']]
 assert math.isclose(md,float(r['measured_depth_m']),abs_tol=1e-9)
 if min(surveys[w])<=md<=max(surveys[w]):
  v=m.interpolate(surveys[w],md)
  for k in ('tvd_m','north_offset_m','east_offset_m'):
   assert math.isclose(v[k],float(r[k]),abs_tol=1e-9),(w,stage,k)
print('All 468 prior geometry rows reproduce from source summaries and surveys.')
print('SURVEY_COUNTS', {w:len(v) for w,v in surveys.items()})
DAILY={'A':'TR,33458531,0516327,00_07-33-037-28W4_0,z3.pdf','B':'TR,33458537,0516328,00_02-33-037-28W4_0,z2.pdf','C':'TR,33458526,0515889,00_15-28-037-28W4_0,z2.pdf'}
rx=re.compile(r'Plug and Perforate Stage\s+(\d+)\s*-\s*Set YJ Composite Plug at\s*([\d.]+)\s*mKB,\s*Perforate\s*-\s*([\d.,\s]+?)\s*mKB',re.I)
narrative=[];unparsed=[]
for w,f in DAILY.items():
 for page,pdfpage in enumerate(fitz.open(a.pdf_dir/f),1):
  text=pdfpage.get_text(sort=True)
  for mt in rx.finditer(text):
   stage=int(mt[1]);plug=float(mt[2]);shots=[float(x.strip()) for x in mt[3].split(',')];st,sb=summaries[w][stage]
   narrative.append(dict(well=w,licence=LIC[w],stage=stage,daily_file=f,daily_page=page,plug_m=plug,shots_m=';'.join(map(str,shots)),shot_count=len(shots),top_m=min(shots),bottom_m=max(shots),summary_top=st,summary_bottom=sb,top_diff_m=min(shots)-st,bottom_diff_m=max(shots)-sb))
  for mt in re.finditer(r'Plug and Perforate Stage',text,re.I):
   if not rx.match(text,mt.start()):unparsed.append(dict(well=w,file=f,page=page,snippet=text[mt.start():mt.start()+400]))
write('daily_perforation_comparison.csv',narrative)
(a.out/'daily_unparsed.json').write_text(json.dumps(unparsed,indent=2))
print('NARRATIVE',len(narrative),{w:len({x['stage'] for x in narrative if x['well']==w}) for w in LIC},'UNPARSED',len(unparsed))
print('NARRATIVE_DIFFERENCES',json.dumps([r for r in narrative if r['top_diff_m'] or r['bottom_diff_m']],indent=2))
print('MISSING_NARRATIVE_STAGES',{w:sorted(set(summaries[w])-set(x['stage'] for x in narrative if x['well']==w)) for w in LIC})
# Source-supported alternatives. Values remain explicit decisions; never overwrite raw summary input.
RESOLUTIONS=[('A',8,(5749.4,5805.4),(5715.4,5771.4),'daily p33 + service summary p3; detail p27 contradicted'),('B',9,(5805.4,5741.4),(5685.4,5741.4),'daily p26 + service detail p30; summary p3 contradicted'),('C',8,(5749.4,5805.4),(5753.0,5809.0),'daily p30 + service summary p3; detail p27 contradicted'),('C',19,(5045.4,5101.4),(5049.0,5105.0),'daily p23 + service summary p3; detail p60 identifies B, reject for C')]
impacts=[]
for w,stage,old,new,basis in RESOLUTIONS:
 for position,omd,nmd in [('top_perforation',old[0],new[0]),('midpoint',sum(old)/2,sum(new)/2),('bottom_perforation',old[1],new[1])]:
  ov=m.interpolate(surveys[w],omd);nv=m.interpolate(surveys[w],nmd);delta={k:nv[k]-ov[k] for k in ['tvd_m','north_offset_m','east_offset_m']}
  impacts.append(dict(well=w,licence=LIC[w],stage=stage,position=position,old_md=omd,recommended_md=nmd,delta_md=nmd-omd,old_tvd=ov['tvd_m'],recommended_tvd=nv['tvd_m'],old_north=ov['north_offset_m'],recommended_north=nv['north_offset_m'],old_east=ov['east_offset_m'],recommended_east=nv['east_offset_m'],delta_tvd=delta['tvd_m'],delta_north=delta['north_offset_m'],delta_east=delta['east_offset_m'],horizontal_shift=math.hypot(delta['north_offset_m'],delta['east_offset_m']),recommended_survey_lower=nv['survey_lower_md_m'],recommended_survey_upper=nv['survey_upper_md_m'],recommended_survey_lower_pages=nv['survey_lower_pages'],recommended_survey_upper_pages=nv['survey_upper_pages'],basis=basis))
write('candidate_geometry_impact.csv',impacts)
print('CANDIDATE_MIDPOINT_IMPACTS',json.dumps([r for r in impacts if r['position']=='midpoint'],indent=2))
corrected=[];changed=[]
for r in prior:
 r=dict(r);r.update(raw_measured_depth_m=r['measured_depth_m'],resolution_status='unchanged summary geometry; see discrepancy audit',resolution_basis='')
 if r['well']=='B' and r['stage']=='9':
  md={'top_perforation':5685.4,'midpoint':5713.4,'bottom_perforation':5741.4}[r['position']]
  r['measured_depth_m']=md;r.update(m.interpolate(surveys['B'],md));r['resolution_status']='source-supported correction; original summary preserved';r['resolution_basis']='B daily physical p26 and service split file1a physical p30'
  phi=math.radians(52.222509);ell=math.sqrt(1-.0066943799901413165*math.sin(phi)**2)
  r['approximate_latitude']=52.222509+math.degrees(r['north_offset_m']/(6378137.0*(1-.0066943799901413165)/ell**3))
  r['approximate_longitude']=-114.001397+math.degrees(r['east_offset_m']/(6378137.0/ell*math.cos(phi)))
  if float(r['raw_measured_depth_m'])!=md:changed.append((r['well'],r['stage'],r['position']))
 corrected.append(r)
write('stage_locations_reconciled.csv',corrected)
print('CHANGED_PRIOR_ROWS',changed)
print('SUMMARY_WIDTHS',{w:sorted({round(b-t,3) for t,b in x.values()}) for w,x in summaries.items()})
# Explicitly recover two page-spanning rows and A19 second perforating run.
for stage,pages in [(15,(28,29)),(11,(30,31))]:
 doc=fitz.open(a.pdf_dir/DAILY['A']);s0=doc[pages[0]-1].get_text(sort=True);s1=doc[pages[1]-1].get_text(sort=True)
 start=re.search(rf'Plug and Perforate Stage {stage}- Set YJ Composite Plug at ([\d.]+)\s*mKB, Perforate - ([\d.,\s]+)',s0)
 end=re.search(r'((?:\d{4}\.\d+,\s*)+\d{4}\.\d+)mKB',s1)
 assert start and end
 shots=[float(x) for x in re.findall(r'\d{4}\.\d+',start[2]+end[1])];assert len(shots)==8
 st,sb=summaries['A'][stage]
 narrative.append(dict(well='A',licence=LIC['A'],stage=stage,daily_file=DAILY['A'],daily_page=';'.join(map(str,pages)),plug_m=float(start[1]),shots_m=';'.join(map(str,shots)),shot_count=len(shots),top_m=min(shots),bottom_m=max(shots),summary_top=st,summary_bottom=sb,top_diff_m=min(shots)-st,bottom_diff_m=max(shots)-sb))
doc=fitz.open(a.pdf_dir/DAILY['A']);s=doc[26].get_text(sort=True);mt=re.search(r'Perforate Stage 19- Perforate - ([\d.,\s]+)mKB',s);assert mt
shots=[float(x.strip()) for x in mt[1].split(',')];st,sb=summaries['A'][19]
narrative.append(dict(well='A',licence=LIC['A'],stage=19,daily_file=DAILY['A'],daily_page=27,plug_m=None,shots_m=';'.join(map(str,shots)),shot_count=len(shots),top_m=min(shots),bottom_m=max(shots),summary_top=st,summary_bottom=sb,top_diff_m=min(shots)-st,bottom_diff_m=max(shots)-sb))
write('daily_perforation_segments_reviewed.csv',narrative)
envelopes=[]
for w in LIC:
 for stage in sorted({r['stage'] for r in narrative if r['well']==w}):
  rows=[r for r in narrative if r['well']==w and r['stage']==stage];shots={float(v) for r in rows for v in r['shots_m'].split(';')};note=''
  if w=='B' and stage==53:
   assert shots=={0.,2877.4,2885.4,2893.4,2901.4,2909.4,2917.4,2925.4};shots.remove(0.);note='Source prints 0mKB as eighth entry; retained in raw segments, excluded from supported interval. Service summary and detail support seven nonzero depths / 48m span.'
  if w=='A' and stage==19:note='Two runs; four initial depths plus three rerun depths define envelope; 5035.4 not explicitly listed, and guns-fired narrative is inconsistent. Do not invent all eight shots.'
  if w=='C' and stage==45:note='Repeated daily narrative includes copy-forward date conflict; not independent corroboration or timing proof.'
  st,sb=summaries[w][stage]
  envelopes.append(dict(well=w,licence=LIC[w],stage=stage,top=min(shots),bottom=max(shots),explicit_distinct_shot_depths=len(shots),source_pages=';'.join(sorted({str(r['daily_page']) for r in rows})),summary_top=st,summary_bottom=sb,top_diff=min(shots)-st,bottom_diff=max(shots)-sb,note=note))
write('reviewed_daily_envelopes.csv',envelopes)
print('REVIEWED_DAILY_ENVELOPES',len(envelopes),{w:sum(r['well']==w for r in envelopes) for w in LIC})
print('REVIEWED_DAILY_MISMATCHES',[(r['well'],r['stage'],r['top_diff'],r['bottom_diff']) for r in envelopes if r['top_diff'] or r['bottom_diff']])
print('MISSING_REVIEWED_DAILY_STAGES',{w:sorted(set(summaries[w])-set(r['stage'] for r in envelopes if r['well']==w)) for w in LIC})
# Annotate the revised copy with actual endpoint source, preserving raw references.
for r in corrected:
 r['raw_perforation_file']=r['perforation_file'];r['raw_perforation_page']=r['perforation_page']
 if r['well']=='B' and r['stage']=='9':r['perforation_page']=30
 ew=[e for e in envelopes if e['well']==r['well'] and str(e['stage'])==r['stage']]
 r['daily_endpoint_evidence_pages']=ew[0]['source_pages'] if ew else ''
 r['evidence_limit']='Recorded perforation endpoints also found in daily narrative; not independently certified' if ew else 'Summary/planned interval only in this endpoint audit; not evidence of perforation'
write('stage_locations_reconciled.csv',corrected)
for f in DAILY.values():
 fpath=a.pdf_dir/f;hashes.append(dict(file=f,sha256=hashlib.sha256(fpath.read_bytes()).hexdigest(),physical_pages=len(fitz.open(fpath))))
(a.out/'input_hashes.json').write_text(json.dumps(hashes,indent=2))
# Dataset-level assertions supplement, not replace, source visual review.
assert len(summaries['A'])+len(summaries['B'])+len(summaries['C'])==156
assert len(prior)==len(corrected)==468
assert sum(len(v) for v in surveys.values())==978
assert len(bad)==4 and {(r['well'],r['stage']) for r in bad}=={('A',8),('B',9),('C',8),('C',19)}
assert len(envelopes)==139
assert {(r['well'],r['stage']) for r in envelopes if r['top_diff'] or r['bottom_diff']}=={('B',9)}
assert set(changed)=={('B','9','top_perforation'),('B','9','midpoint')}
selected=list(csv.DictReader((a.prior_dir/'deliverables/Cygnet_selected_stage_coordinates.csv').open()))
for src in selected:
 candidate=next(r for r in corrected if all(r[k]==src[k] for k in ['well','stage','position']))
 for k in ['measured_depth_m','north_offset_m','east_offset_m','tvd_m','approximate_latitude','approximate_longitude']:
  assert float(candidate[k])==float(src[k]),(src['well'],src['stage'],k)
assert next(r for r in corrected if r['well']=='C' and r['stage']=='1' and r['position']=='bottom_perforation')['tvd_m']==''
print('VALIDATION PASSED: 11 source hashes; 156 summaries; 137 service details; 139 reviewed narrative envelopes; 978 survey rows; 468 output rows; exactly 2 coordinate changes; 7 selected rows unchanged; C1 missing bottom remains blank.')
