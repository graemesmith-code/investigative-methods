#!/usr/bin/env python3
"""Build authored evidence observations and a deliberately ranked 75-source guide.

Input registers contain source-specific analysis/access limits, never confidential
notes. Output CSV belongs on Drive. Ranking is editorial relevance, not a measured
quality score. Same URL aliases are retained, not counted as independent evidence.
"""
import argparse,csv,json
from pathlib import Path
RANK='''US-SAF-01 A01 A33 A31 A32 L-AR2753 L-NSPM11 P-US11946710B1 N26 N01 N19 P-US11768065B2 US-SAF-27 A25 A28 F01 A35 A34 F02 A02 A22 A23 A24 A30 A17 A18 A09 A11 A15 A06 N02 N04 N09 N11 N12 N14 N15 N16 N18 N20 N21 N22 N23 US-SAF-02 US-SAF-04 US-SAF-05 US-SAF-06 US-SAF-08 US-SAF-09 US-SAF-10 US-SAF-14 US-SAF-15 US-SAF-16 US-SAF-17 US-SAF-18 US-SAF-20 L-NL2026 P-US20220366798A1 P-US20250030576A1 P-US20260022912A1 P-US12087171B2 P-US12154441B2 P-US12175877B2 P-WO2023167712A2 L-AP136 L-USSTATUS L-ICRC2006 L-231101 L-300009 L-UK2016 L-AU2024 L-CA2024 L-MCKEE2025 F03 F04'''.split()
FIELDS=['source_id','aliases','workstream','title','source_date','source_url','evidence_quality','access_state','claim_supported','currentness','implementation','funding','novelty','limitation']
def main():
 p=argparse.ArgumentParser();
 for name in ['allied','safety','patents','financial']:p.add_argument('--'+name,required=True,type=Path)
 p.add_argument('--extra',type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--reading-pack',required=True,type=Path);a=p.parse_args()
 sources=[];byid={};byurl={}
 for group,path in [('allied',a.allied),('safety',a.safety),('patents',a.patents),('financial',a.financial)]+([('extra',a.extra)] if a.extra else []):
  for index,r in enumerate(json.loads(path.read_text()),1):
   sid=r.get('id',r.get('source_id','F%02d'%index if group=='financial' else 'V%02d'%index))
   work=r.get('workstream',1 if sid.startswith('A') else 2 if sid.startswith('N') else 4 if sid.startswith('P-') else 5 if sid.startswith('L-') else 3)
   quality=r.get('quality',r.get('evidence_quality',r.get('evidence_type','primary source')))
   row=dict(source_id=sid,aliases=sid,workstream=str(work),title=r['title'],source_date=r.get('date') or 'undated; accessed 2026-10-25',source_url=r['url'],evidence_quality=quality,access_state=r.get('access',r.get('access_status','See source-specific memo for readable/indexed/catalogue access distinction')),claim_supported=r.get('claim',r.get('supports','')),currentness=r.get('currentness','Version/date above; retrieval 2026-10-25 is not proof of current implementation'),implementation=r.get('implementation','Policy/research/trial scope; particular operational safeguard effectiveness unverified'),funding=r.get('funding','No outlay or safeguard-budget attribution'),novelty=r.get('novelty','New F5 source review; publication may predate F5'),limitation=r.get('limitation',r.get('limitations','See thematic dossier for context and access limits')))
   if row['source_url'] in byurl:
    existing=byurl[row['source_url']];existing['aliases']+=';'+sid;byid[sid]=existing
   else:sources.append(row);byurl[row['source_url']]=row;byid[sid]=row
 assert len(RANK)==75 and len(set(RANK))==75
 selected=[byid[k] for k in RANK]
 assert len({r['source_url'] for r in selected})==75,'Ranking contains duplicate-source URLs'
 a.out.parent.mkdir(parents=True,exist_ok=True)
 with a.out.open('w',newline='') as f:w=csv.DictWriter(f,FIELDS);w.writeheader();w.writerows(sources)
 lines=['# F5 ranked reading pack: 75 primary sources','', 'Ranked for a feature reporter by relevance to the strongest verified findings, authority and specificity. This is editorial ranking, not a numerical effectiveness score. Dates distinguish old standards, new guidance and current retrieval. A source can verify a policy or patent while leaving implementation unproved. Related database views and same-family patent publications are not independent observations.','', 'The complete source-observation register is on Drive through `DRIVE_DATA_MANIFEST.json`; source-specific access limits remain in the five memos. Some official pages were available only as indexed text or catalogue records. Such entries are retained with that limitation, not presented as complete-document review.','']
 for i,r in enumerate(selected,1):
  claim=r['claim_supported'].strip().replace('\n',' ');limit=str(r['limitation']).strip().replace('\n',' ')
  lines.extend([str(i)+'. **['+r['title']+']('+r['source_url']+')** — '+str(r['source_date'])+'; '+str(r['evidence_quality']).replace('_',' ')+'. '+claim+' Limit: '+limit,''])
 data='\n'.join(lines)+'\n'
 if len(data.encode())>100000:raise ValueError('Reading pack exceeds Git size limit')
 a.reading_pack.write_text(data)
 print(json.dumps({'source_observations':len(sources),'ranked_sources':len(selected),'reading_pack_bytes':len(data.encode())}))
if __name__=='__main__':main()
