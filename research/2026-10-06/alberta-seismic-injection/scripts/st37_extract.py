"""Retain public infrastructure rows for all study-period fracture licences, not outcome-selected companies."""
import json,pathlib,openpyxl,datetime,zipfile,tempfile
R=pathlib.Path(__file__).resolve().parents[1];jobs=json.loads((R/'results/jobs-period.json').read_text());lic={j['Well_Licence_Number'].strip().zfill(7) for j in jobs}
meta={}
tmp=pathlib.Path(tempfile.mkdtemp(prefix='alberta-st37-'))
with zipfile.ZipFile(R/'sources/ST37-excel.zip') as archive:archive.extractall(tmp)
for fn in ['ST37_SH.xlsx','ST37_BH.xlsx','ST37_ Production_Strings.xlsx']:
 w=openpyxl.load_workbook(tmp/'ST_37_Excel'/fn,read_only=True,data_only=True)
 for s in w:
  it=iter(s.values);header=next(it);idx=header.index('Well_Licence_Number');out=[];n=0
  for row in it:
   n+=1
   if str(row[idx]).strip().zfill(7) in lic:out.append(dict(zip(header,row)))
  (R/'results'/('st37-'+s.title.replace(' ','_')+'.json')).write_text(json.dumps(out,indent=2,default=str)+'\n')
  meta[s.title]={'source':fn,'headers':header,'rows_scanned':n,'retained':len(out),'selection':'all licence identifiers in period jobs; independent of collisions'}
  print(s.title,n,len(out),flush=True)
 w.close()
(R/'results/st37-extraction.json').write_text(json.dumps(meta,indent=2)+'\n')
