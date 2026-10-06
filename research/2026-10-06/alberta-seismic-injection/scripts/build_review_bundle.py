"""Build compact review ZIP; full raw corpus stays in the private repository."""
import pathlib,sys,json,hashlib,zipfile,subprocess
P=pathlib.Path(__file__).resolve().parents[1];dest=pathlib.Path(sys.argv[1]);dest.parent.mkdir(parents=True,exist_ok=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
keep=set(P.glob('*.md'))|set(P.glob('requirements*.txt'))
for folder in ['scripts','results','jev']:
 keep.update(p for p in (P/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.sqlite','.pyc'])
names=['manifest.jsonl','SummaryChemical-WaterUse.csv.gz','earthquakes.json','earthquake-count.json','nrcan-events.txt','nrcan-events.xml','tableau-browser-error.json','jev-models.html','jev-api.html']
keep.update(P/'sources'/n for n in names)
keep.update(p for p in (P/'sources/waveforms').rglob('*') if p.is_file())
keep.update((P/'sources').glob('*.pdf'));keep.update((P/'sources').glob('*.txt'))
files=[{'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(keep)]
manifest={'kind':'compact review bundle; full offline reproduction requires private checkout','repository':'https://github.com/graemesmith-code/investigative-methods','commit':commit,'experiment_path':'research/2026-10-06/alberta-seismic-injection','excluded':'Bulk ST37/order archives and multipart pieces, volume/identity/incident source archives, most HTML snapshots; all retained in private repo. Local live ledger excluded; cumulative JSON export included.','files':files}
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(keep):z.write(p,str(p.relative_to(P)))
 z.writestr('BUNDLE-MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for f in files:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256']
print(json.dumps({'file':str(dest),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'files':len(files),'commit':commit}))
