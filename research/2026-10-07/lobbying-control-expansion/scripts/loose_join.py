"""Reproducible exploratory rare-token screen. Never an entity-resolution finding."""
import json,re,collections
from acquire import P
clients=json.loads((P/'client-screen.json').read_text());principals=json.loads((P/'fara-report-principals.json').read_text())
freq=collections.Counter(t for f in principals for t in set(f['normalized'].split()))
# Explicit exploratory exclusions, not preregistered or learned from misconduct labels.
stop=set('FORMERLY FINANCIAL NORTH TECHNOLOGIES SERVICES INCORPORATED POLICY CHAMBER TECHNOLOGY FEDERATION AMERICAN RESEARCH HOLDINGS CENTER PHARMACEUTICAL'.split())
out=[]
for c in clients:
 aa=set(re.findall('[A-Z0-9]+',c['client_name']))-stop
 for f in principals:
  anchor=sorted(x for x in aa&set(f['normalized'].split()) if len(x)>=5 and freq[x]<=9)
  if anchor:out.append({'client_id':c['client_id'],'client_name':c['client_name'],**{k:f[k] for k in ['principal','registration_number','pdf_page','source']},'anchor':anchor})
(P/'loose-name-reproduced.json').write_text(json.dumps(out,indent=2))
old=json.loads((P/'loose-name-candidates.json').read_text())
key=lambda x:(x['client_id'],x['principal'],x['source'],x['pdf_page'],tuple(x['anchor']))
print('Edges',len(out),'exact match to exploratory archive',set(map(key,out))==set(map(key,old)))
