import json,csv,io,zipfile,pathlib,collections
P=pathlib.Path(__file__).resolve().parents[1];R=P/'results'
def readzip(name):
 z=zipfile.ZipFile(P/'sources'/name);n=z.namelist()[0]
 if n.endswith('.zip'):z=zipfile.ZipFile(io.BytesIO(z.read(n)));n=z.namelist()[0]
 return csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig'))
period=json.loads((R/'jobs-period.json').read_text());licenses={j['Well_Licence_Number'] for j in period};real=json.loads((R/'sensitivity-MLy-only.json').read_text());candidate_licenses={c['job']['Well_Licence_Number'] for c in real}
out=[];n=0
rd=readzip('petrinex-well-license.zip')
for row in rd:
 n+=1
 if row['LicenceNumber'] in licenses:out.append(row)
(R/'petrinex-licences-period.json').write_text(json.dumps(out,indent=2)+'\n')
(R/'petrinex-licence-schema.json').write_text(json.dumps({'fields':rd.fieldnames,'rows':n,'retained':len(out)},indent=2)+'\n')
print('Licence records',n,len(out))
for row in out:
 if row['LicenceNumber'] in candidate_licenses:print(json.dumps(row))
# Exact incident number and licence matches; absence here is not absence from earthquake dashboard.
for filename in ['incident-release.csv','incident-complaints.xls']:
 path=P/'sources'/filename
 with path.open(encoding='utf-8-sig',errors='replace') as f:
  lines=[next(f) for _ in range(9)]
 print(filename,''.join(lines)[:2000])
