from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import shape
P=Path(__file__).resolve().parents[1];R=P/'results'
f=json.loads((R/'rule-geometries.geojson').read_text())['features'];ps={x['properties']['Order_Numb']:shape(x['geometry']) for x in f};packets=json.loads((R/'evidence-packets.json').read_text())
fig,axs=plt.subplots(1,3,figsize=(15,6))
for ax,(name,ids) in zip(axs,[('Fox Creek',['2']),('Brazeau',['6.2','6.1']),('Red Deer',['7.2','7.1'])]):
 for i,key in enumerate(ids):
  poly=ps[key]
  for geom in ([poly] if poly.geom_type=='Polygon' else poly.geoms):
   xx,yy=geom.exterior.xy;ax.fill(xx,yy,alpha=.25,label=key);ax.plot(xx,yy,linewidth=.8)
 if name=='Red Deer':
  seen=set()
  for p in packets:
   e=p['event'];k=e['id']
   if k not in seen:ax.scatter(e['lon'],e['lat'],marker='*',s=80,c='red');seen.add(k)
  for p in {p['well']['licence']:p for p in packets}.values():
   b=p['well']['bottomhole'];s=p['well']['surface'];ax.plot([b['lon'],s['SH_Actual_Longitude']],[b['lat'],s['SH_Actual_Latitude']],color='black',linewidth=.5);ax.scatter(b['lon'],b['lat'],s=8,c='black')
 ax.set_title(name);ax.set_xlabel('Longitude, NAD83');ax.set_ylabel('Latitude');ax.set_aspect(1.65);ax.legend(title='Official GIS label');ax.grid(alpha=.2)
fig.suptitle('AER order outlines: geographic screening only; formation and actual pumping still required',fontsize=12)
fig.text(.02,.01,'Source: AER Order System spatial download, 2026-10-06. Red stars: catalogue events; black: well reference points. Lines connect endpoints, not surveyed trajectories.',fontsize=8)
fig.tight_layout(rect=[0,.04,1,.94]);fig.savefig(R/'rule-boundary-review.png',dpi=150)
