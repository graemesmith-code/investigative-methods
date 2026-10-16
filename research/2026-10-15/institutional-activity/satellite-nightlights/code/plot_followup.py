"""Static scientific figure from the saved follow-up extracts; no new data."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize

ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'evidence/followup_results.json').read_text())
ps=json.loads((ROOT/'evidence/followup_pixel_values.json').read_text())
from followup_brightness import good
cx,cy=r['geometry']['centre_lon_lat']; sx=111.195*np.cos(np.deg2rad(cy));sy=111.195
fig=plt.figure(figsize=(12,10),layout='constrained')
gs=fig.add_gridspec(2,2,height_ratios=[1.15,1])
axes=[fig.add_subplot(gs[0,i]) for i in [0,1]]
scenes=[[p for p in ps if p['region']=='pentagon_broad' and p['date_utc']==day] for day in ['2025-06-19','2025-06-20']]
vmax=max(p['radiance'] for scene in scenes for p in scene if good(p,'both_relaxations'))
norm=Normalize(0,vmax);cmap=plt.get_cmap('magma')
for ax,scene,label in zip(axes,scenes,['19 June, about 03:07 EDT','20 June, about 02:48 EDT']):
    for p in scene:
        x=(-80+p['col']/240-cx)*sx;y=(40-p['row']/240-cy)*sy;dx=sx/240;dy=sy/240
        ok=good(p,'both_relaxations')
        ax.add_patch(Rectangle((x-dx/2,y-dy/2),dx,dy,facecolor=cmap(norm(p['radiance'])) if ok else '#d6d9df',edgecolor='#ffffff',lw=.7,hatch=None if ok else '///'))
    ax.add_patch(Rectangle((-.25,-.25),.5,.5,fill=False,edgecolor='#00e5db',lw=2.5))
    ax.add_patch(Rectangle((-.5,-.5),1,1,fill=False,edgecolor='#b4fff8',lw=1.2,linestyle='--'))
    ax.set(xlim=(-1,1),ylim=(-1,1),aspect='equal',xlabel='East / west from fixed centre (km)',ylabel='North / south (km)',title=label)
fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cmap),ax=axes,label='Observed corrected radiance (nW cm⁻² sr⁻¹)',shrink=.78)
pair=next(p for p in r['within_event_pairs'] if p['scenario']=='both_relaxations' and p['broad_pair_pass'])
ax=fig.add_subplot(gs[1,0])
labels={'core_500m':'Central 500 m','core_1000m':'Central 1 km','pentagon_broad':'Broad 2 km','surround_disjoint':'Disjoint surroundings','rosslyn_commercial':'Rosslyn','reston_town_center':'Reston','tysons_commercial':'Tysons'}
order=list(labels); vals=[next(x['change_pct_if_75pct'] for x in pair['regions'] if x['region']==k) for k in order]
ax.barh(range(7),vals,color=['#007e80']*4+['#758296']*3)
ax.set_yticks(range(7),[labels[k] for k in order]);ax.invert_yaxis();ax.axvline(0,color='#333333',lw=.8)
for i,v in enumerate(vals):ax.text(v+(1 if v>=0 else -1),i,f'{v:+.1f}%',ha='left' if v>=0 else 'right',va='center',fontsize=10)
ax.set(xlim=(-58,24),xlabel='Change on identical valid cells (%)',title='500 m core rises no more than its surroundings')
ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.15)
ax=fig.add_subplot(gs[1,1]);tests=r['synthetic_injection']['tests'];xx=np.arange(len(tests));yy=[v['broad_mean_change_pct'] for v in tests]
ax.bar(xx,yy,color='#d88535',width=.6)
ax.set_xticks(xx,[f"+{v['injected_core_cells_pct']}%" for v in tests]);ax.set(ylim=(0,24),xlabel='Hypothetical increase in four mixed central cells',ylabel='Resulting change in broad-area mean (%)',title='Broad averaging dilutes a localized increase')
for x,y in zip(xx,yy):ax.text(x,y+.5,f'{y:.1f}%',ha='center',fontsize=11)
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
fig.suptitle('Nightlights follow-up: central brightening also appears nearby\nJune 19–20, 2025 · existing uploads only · exploratory quality mask',fontsize=17,fontweight='bold')
fig.supxlabel('Maps use each date’s valid cells; change bars use identical cells. Solid outline = 500 m; dashed = 1 km; hatched = excluded.\nOne within-event pair, no normal-night baseline. Grid cells mix light sources. Synthetic changes are in light units, not people.',fontsize=9)
(ROOT/'figures').mkdir(exist_ok=True)
fig.savefig(ROOT/'figures/followup_results.svg')
fig.savefig(ROOT/'figures/followup_results.png',dpi=150)
print('Saved followup_results.svg and local rendering.')
