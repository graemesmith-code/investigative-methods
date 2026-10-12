"""Replay pilot government extraction from unpacked workbooks; see IMPLEMENTATION.md.

Blank monthly cells follow the pilot zero-contribution convention. No blank annual
observation is fabricated: only selected rows are aggregated. Review source meaning
before reusing this convention on another archive.
"""
import json,unicodedata,openpyxl
from pathlib import Path
from decimal import Decimal as D
OUT=Path('research/2026-10-12/peru-production-pilot')
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',str(s or '').upper()) if unicodedata.category(c)!='Mn')
entities={'southern':'SOUTHERN PERU COPPER','cerro_verde':'SOCIEDAD MINERA CERRO VERDE','antamina':'COMPANIA MINERA ANTAMINA','hudbay':'HUDBAY PERU','yanacocha':'MINERA YANACOCHA','gold_fields':'GOLD FIELDS LA CIMA','la_arena':'LA ARENA S.A.','shahuindo':'SHAHUINDO S.A.C.','ares':'COMPANIA MINERA ARES','nexa_peru':'NEXA RESOURCES PERU','buenaventura':'COMPANIA DE MINAS BUENAVENTURA'}
metals={'COBRE':'Cu','ORO':'Au','PLATA':'Ag','ZINC':'Zn','MOLIBDENO':'Mo'}
rows=[]
for y in range(2019,2024):
 files=[Path(f'research/pilot-raw/minem-{y}-bulk/{m}.xlsx') for m in metals] if y==2019 else [p for p in Path(f'research/pilot-raw/minem-{y}-bulk').glob('*.xlsx') if norm(p.name).startswith('PRODUCCION METALICA')]
 for p in files:
  s=openpyxl.load_workbook(p,read_only=True,data_only=True).active
  for i,r in enumerate(s.iter_rows(values_only=True),1):
   if i<(6 if y==2019 else 5):continue
   k=4 if y==2019 else 5
   if len(r)<=k:continue
   entity=next((e for e,n in entities.items() if n in norm(r[k])),None)
   if not entity or norm(r[0]).lstrip('%') not in metals:continue
   monthstart=9 if y==2019 else 10
   mm=[D(str(v or 0)) for v in r[monthstart:monthstart+12]]
   rows.append(dict(year=y,entity_id=entity,metal=metals[norm(r[0]).lstrip('%')],source=str(p),sheet=s.title,row=i,operator=r[k],plant=r[k+1],stage=r[1 if y==2019 else 2],process=r[2 if y==2019 else 3],months=[str(v) for v in mm],sum_months=str(sum(mm)),annual_cell=str(r[monthstart+12]) if len(r)>monthstart+12 else None,monthly_cells=f'{openpyxl.utils.get_column_letter(monthstart+1)}{i}:{openpyxl.utils.get_column_letter(monthstart+12)}{i}'))
(OUT/'host-detailed-rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
host=json.load(open(OUT/'host-records.json'));checks=[]
for r in host:
 rr=[x for x in rows if (x['entity_id'],x['metal'],x['year'])==(r['entity_id'],r['metal'],r['year']) and norm(x['stage'])=='CONCENTRACION']
 total=sum(D(x['sum_months']) for x in rr)
 chk=dict(record_id=r['record_id'],rows=[dict(source=x['source'],sheet=x['sheet'],row=x['row'],plant=x['plant'],stage=x['stage'],process=x['process'],sum_months=x['sum_months']) for x in rr],bulk_sum=str(total) if rr else None,yearbook_value=r['host_original_value'])
 if r['host_original_value'] is not None:chk['bulk_minus_yearbook']=str(total-D(r['host_original_value'])) if rr else None
 else:chk['bulk_minus_yearbook']=None
 checks.append(chk)
 print(r['record_id'],[x['plant'] for x in rr],chk['bulk_minus_yearbook'] if r['host_original_value'] is not None else 'NEW '+str(total))
(OUT/'host-version-audit.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
