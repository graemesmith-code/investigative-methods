"""Deterministic major-report screen and official-report name joins, not identity findings."""
import re,json,pathlib,collections,unicodedata
from acquire import P,S

def norm(s):
 s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().upper().replace('&',' AND ')
 return ' '.join(re.findall(r'[A-Z0-9]+',s))
stop=set('THE OF AND FOR INC INCORPORATED LLC LTD LIMITED CORPORATION CORP COMPANY CO GROUP INTERNATIONAL USA US AMERICA AMERICAN NORTH UNITED STATES GOVERNMENT ASSOCIATION NATIONAL COUNCIL SERVICES'.split())
def tokens(s):return set(norm(s).split())-stop
records=[]
for f in sorted(S.glob('fara-congress-2024h*.txt')):
 reg=None;regname=None
 for pn,page in enumerate(f.read_text().split('\f'),1):
  if 'APPENDIX A - REGISTRANT INDEX' in page and pn>20:break
  lines=page.splitlines();i=0
  while i<len(lines):
   line=lines[i];m=re.match(r'^(.+?)\s+#(\d{3,5})\s*(?:\([Tt]\))?\s*$',line.strip())
   if m:regname,reg=m[1].strip(),m[2]
   if line.strip().startswith('Foreign Principal:'):
    name=line.strip().split(':',1)[1].strip();i+=1
    while i<len(lines) and lines[i].strip() and not lines[i].strip().startswith('Nature of Services:'):name+=' '+lines[i].strip();i+=1
    records.append({'source':f.name,'pdf_page':pn,'registrant':regname,'registration_number':reg,'principal':name,'normalized':norm(name),'page_text':page})
   i+=1
(P/'fara-report-principals.json').write_text(json.dumps(records,indent=2))
rows={r['filing_uuid']:r for f in sorted(S.glob('lda-major-[0-9]*.json')) for r in json.loads(f.read_text())['results']}
clients={}
for r in rows.values():
 c=clients.setdefault(r['client']['id'],{'id':r['client']['id'],'name':r['client']['name'],'country':r['client'].get('country'),'rows':[]});c['rows'].append(r)
join=[]
for id,c in clients.items():
 a=norm(c['name']);aa=tokens(c['name'])
 for f in records:
  b=f['normalized'];bb=tokens(f['principal']);shared=aa&bb
  kind='exact_normalized' if a==b else 'token_equal' if aa==bb and len(aa)>=2 else 'distinctive_containment' if min(len(aa),len(bb))>=2 and (aa<=bb or bb<=aa) else None
  if kind:join.append({'client_id':id,'client_name':c['name'],'match_type':kind,**{k:f[k] for k in ['source','pdf_page','registrant','registration_number','principal']}})
(P/'name-join-candidates.json').write_text(json.dumps(join,indent=2))
summary=[]
for id,c in clients.items():
 summary.append({'client_id':id,'client_name':c['name'],'country':c['country'],'high_amount_filings':len(c['rows']),'max_income':max(float(r['income'] or 0) for r in c['rows']),'max_expenses':max(float(r['expenses'] or 0) for r in c['rows']),'foreign_additions_present':any(r['foreign_entities'] for r in c['rows']),'fara_report_name_matches':sum(e['client_id']==id for e in join),'uuids':[r['filing_uuid'] for r in c['rows']]})
(P/'client-screen.json').write_text(json.dumps(summary,indent=2))
print('LDA records',len(rows),'clients',len(clients),'FARA report entries',len(records),'unique principals',len({r['normalized'] for r in records}),'join edges',len(join),'matched clients',len({r['client_id'] for r in join}))
for x in summary:
 if x['fara_report_name_matches'] or x['country']!='US' or x['foreign_additions_present']:print({k:v for k,v in x.items() if k!='uuids'})
