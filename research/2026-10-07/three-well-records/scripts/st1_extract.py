import zipfile,re,json,pathlib,io
P=pathlib.Path(__file__).resolve().parents[1];found=[];counts={}
for yr in [2024,2025]:
 z=zipfile.ZipFile(P/f'sources/st1-{yr}.zip');count=0
 for month in z.namelist():
  m=zipfile.ZipFile(io.BytesIO(z.read(month)))
  for n in m.namelist():
   txt=m.read(n).decode(errors='replace');count+=1
   matches=list(re.finditer(r'0?51(?:5889|6327|6328)',txt))
   if matches:
    path=f'sources/st1-{yr}-{pathlib.Path(n).name}';(P/path).write_text(txt)
    for match in matches:found.append({'archive_year':yr,'month':month,'member':n,'saved':path,'excerpt':txt[max(0,match.start()-400):match.end()+600]})
 counts[yr]=count
(P/'results/st1-target-matches.json').write_text(json.dumps({'files_scanned':counts,'matches':found},indent=2)+'\n');print(json.dumps(found,indent=2))
