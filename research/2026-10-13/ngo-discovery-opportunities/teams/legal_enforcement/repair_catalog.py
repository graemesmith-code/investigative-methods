import pathlib,json,unicodedata,re,datetime
P=pathlib.Path(__file__).parent
rs=[json.loads(l) for l in (P/'inventory.jsonl').read_text().splitlines()]
rs=[r for r in rs if not r['title'].startswith('Reports Archive')]
meta=json.load(open(P/'spotlight-catalog-dates.json'))
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s.lower()))
for r in rs:
 if r['org']=='Spotlight on Corruption':
  for m in meta:
   if norm(m['title']).startswith(norm(r['title'])):r['date']=datetime.datetime.strptime(m['date'],'%d %B, %Y').date().isoformat();r['date_provenance']='official report archive';break
P.joinpath('inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs));P.joinpath('spotlight-catalog-dates.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
cs=json.load(open(P/'counts.json'));cs['Spotlight on Corruption']['enumerated']=sum(r['org']=='Spotlight on Corruption' for r in rs);cs['Spotlight on Corruption']['acquired']=cs['Spotlight on Corruption']['enumerated'];P.joinpath('counts.json').write_text(json.dumps(cs,indent=2));print('missing dates',[r['title'] for r in rs if r['date'] is None]);print(cs)
