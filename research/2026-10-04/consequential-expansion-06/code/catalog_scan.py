import pathlib,re,json,hashlib
P=pathlib.Path(__file__).resolve().parents[1];repo=P.parents[2];base=repo/'references/rabbit/originals'
files=['Rabbit2(1).txt','Rabbit3.txt','Rabbit4.txt','Rabbit5.txt','Rabbit6.txt']
patterns=[r'carbon[ -]?credit',r'offset.{0,20}registr',r'registr.{0,20}offset',r'Verra',r'Gold Standard',r'Climate Action Data',r'renewable energy certificate',r'guarantee.{0,5}origin',r'WREGIS',r'\bI-REC\b',r'Union Registry']
blocks=[];hits=[];support=[]
for name in files:
 text=(base/name).read_text();lines=text.splitlines(keepends=True);starts=[i for i,l in enumerate(lines) if re.match(r'^## SYS-\d{4} —',l)]
 for ix,start in enumerate(starts):
  end=starts[ix+1] if ix+1<len(starts) else len(lines);raw=''.join(lines[start:end]);sid=re.search(r'SYS-\d{4}',lines[start])[0]
  record=dict(sys_id=sid,file=name,line_start=start+1,line_end=end,block_sha256=hashlib.sha256(raw.encode()).hexdigest(),title=lines[start].strip())
  blocks.append(record)
  matches=[p for p in patterns if re.search(p,raw,re.I)]
  if matches:hits.append(dict(**record,patterns=matches))
  if sid=='SYS-0854':support.append(dict(**record,all_ap_ids=list(dict.fromkeys(re.findall(r'AP-\d{4}',raw))),source_text=raw))
(P/'evidence/environmental-registry-scan.json').write_text(json.dumps(dict(files=files,excluded_duplicate='Rabbit2.txt',excluded_front_matter='Rabbit1.txt',system_count=len(blocks),patterns=patterns,matching_source_blocks=hits,interpretation='Targeted textual search only. No serial-level environmental-attribute registry was identified by these patterns; not proof that none exists anywhere in Rabbit prose or outside Rabbit.'),indent=2)+'\n')
(P/'supporting-sources.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in support))
print('Catalog blocks',len(blocks),'targeted hits',len(hits))
