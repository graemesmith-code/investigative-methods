#!/usr/bin/env python3
"""Table-level pilot, NOT a validated crisis forecast. Python stdlib plus pdftotext.
Reads authentic public 2004/2005/2006 OCC PDF vintages. No model/API required.
"""
from pathlib import Path
import re,csv,json,hashlib,subprocess
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parent
VINTAGE={2004:'2004-11-09',2005:'2005-07-28',2006:'2006-10-18'}
RETAIL=['Affordable Housing','Consumer Leasing','Credit Card','Other Direct Consumer','Home Equity Conventional','Home Equity High LTV','Indirect Consumer','Residential Real Estate']
def norm(s):
 s=' '.join(s.split()).replace('—-','—')
 s=s.replace('Home Equity — Conventional','Home Equity Conventional').replace('Home Equity — High LTV','Home Equity High LTV')
 return s
rows=[]
for v,release in VINTAGE.items():
 pdf=ROOT/f'occ{v}.pdf'; txt=ROOT/f'occ{v}.txt'
 subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True)
 bbox=ROOT/f'occ{v}_bbox.html'
 subprocess.run(['pdftotext','-bbox-layout',str(pdf),str(bbox)],check=True)
 ns={'x':'http://www.w3.org/1999/xhtml'}
 xmlpages=ET.parse(bbox).findall('.//x:page',ns)
 for page_num,page in enumerate(txt.read_text().split('\f'),1):
  if 'Changes in Underwriting Standards in' not in page: continue
  standard=page.split('Changes in Underwriting Standards in',1)[1].split('Changes in the Level of Credit Risk',1)[0]
  name=norm(standard.split('Portfolios')[0].replace('Loan','').replace('Credit','Credit'))
  # The table title, not a model, supplies the identity.
  if name not in RETAIL: continue
  words=[(w.text or '',float(w.get('xMin')),float(w.get('yMin'))) for w in xmlpages[page_num-1].findall('.//x:word',ns)]
  # Some 2005 table cells sit 6pt above their year label. Plain text row regex
  # lost six of eight current-year retail rows. Use coordinates, not silent fills.
  for year in range(1999,v+1):
   candidates=[w for w in words if w[0]==str(year)]
   assert candidates,(v,name,year,'missing year')
   yw=min(candidates,key=lambda w:w[2])
   cells=sorted([w for w in words if w[0].isdigit() and w[1]>yw[1]+80 and abs(w[2]-yw[2])<=8],key=lambda w:w[1])
   assert len(cells)==3,(v,name,year,cells)
   ease,same,tight=[int(w[0]) for w in cells]
   assert abs(ease+same+tight-100)<=1,(v,name,year)
   rows.append(dict(vintage=v,release_announcement_date=release,observation_year=year,category=name,eased=ease,unchanged=same,tightened=tight,net_easing_pp=ease-tight,pdf_page=page_num))
 assert len({r['category'] for r in rows if r['vintage']==v})==(7 if v==2006 else 8)
 assert len([r for r in rows if r['vintage']==v])==(v-1998)*(7 if v==2006 else 8)
with (ROOT/'occ_retail_all_vintages.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Same-vintage current-year results; not reconstructed from a later release.
results={}
for v in VINTAGE:
 current=[r for r in rows if r['vintage']==v and r['observation_year']==v]
 results[v]={'universe_size':len(current),'net_easing':{r['category']:r['net_easing_pp'] for r in current},'threshold_sensitivity':{str(t):[r['category'] for r in current if r['net_easing_pp']>=t] for t in [1,10,20]}}
# Cross-vintage overlap audit (every retail row and numeric column).
lookup={(r['vintage'],r['observation_year'],r['category']):r for r in rows}
comparison=[]
for early,late in [(2004,2005),(2005,2006),(2004,2006)]:
 count=0;diff=[]
 for r in rows:
  if r['vintage']!=early:continue
  l=lookup.get((late,r['observation_year'],r['category']))
  if l:
   count+=1
   for col in ['eased','unchanged','tightened']:
    if r[col]!=l[col]: diff.append({'year':r['observation_year'],'category':r['category'],'column':col,'earlier':r[col],'later':l[col]})
 comparison.append({'earlier_vintage':early,'later_vintage':late,'rows_compared':count,'numeric_cells_compared':count*3,'differences':diff})
# All years in 2006 edition, explicitly a single-vintage descriptive history.
historical={y:[r['category'] for r in rows if r['vintage']==2006 and r['observation_year']==y and r['net_easing_pp']>=10] for y in range(1999,2007)}
# Threshold was chosen after source reading. This is an illustration, not preregistration.
out={'purpose':'Descriptive extraction / alert-reproducibility pilot; no predictive validation','rule':'net_easing_pp = percent eased - percent tightened; illustrative threshold >=10pp','rule_registration':'Selected retrospectively after inspecting source; not preregistered', 'measurement_scope':'Percentages concern relevant-product respondents, not all survey banks or loan-dollar shares. In 2006 high-LTV home equity covered 19 banks; residential real estate 62; overall survey 73. Automated checks validate category coverage, expected row counts and percentage totals; product-specific bank denominators were not independently reconstructed.', 'provenance_caveat':'The edition-specific PDFs were retrieved in 2026. 2006 PDF metadata says created and modified 2006-10-19, one day after the 2006-10-18 release announcement. Historical byte identity/first availability of this exact PDF was not independently archived. Do not claim exact-day predictive lead time.','current_vintage_results':results,'cross_vintage_audit':comparison,'single_2006_vintage_history_threshold10':historical,'hashes':{f'occ{y}.pdf':hashlib.sha256((ROOT/f'occ{y}.pdf').read_bytes()).hexdigest() for y in VINTAGE}}
(ROOT/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
