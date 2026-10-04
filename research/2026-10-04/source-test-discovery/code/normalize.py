"""Normalize explicit labeled descriptions; preserve byte/line/AP provenance. No network."""
import re,json,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).resolve().parents[1]
FILES=['Rabbit2(1).txt','Rabbit3.txt','Rabbit4.txt','Rabbit5.txt','Rabbit6.txt']
def sha(b): return hashlib.sha256(b).hexdigest()
def fields(text): return {m[1]:m[2] for m in re.finditer(r'^- \*\*(.+?):\*\* (.*)$',text,re.M)}
def run():
 sources=[]; manifest=[]; all_ids=[]; all_aps=[]
 for filename in FILES:
  p=ROOT/'references/rabbit/originals'/filename; raw=p.read_bytes(); t=raw.decode(); ms=list(re.finditer(r'^## (SYS-\d+) — (.+)$',t,re.M)); selected=0; labeled=0
  for i,m in enumerate(ms):
   end=ms[i+1].start() if i+1<len(ms) else len(t); block=t[m.start():end]; all_ids.append(m[1]); am=list(re.finditer(r'^#### (AP-\d+) — (.+)$',block,re.M)); aps=[]
   for j,a in enumerate(am):
    ae=am[j+1].start() if j+1<len(am) else len(block); ab=block[a.start():ae].split('### Coverage mappings')[0]; af=fields(ab); all_aps.append(a[1])
    if 'Useful join fields' in af:
     labeled+=1
     aps.append({'ap_id':a[1],'name':a[2],'line_start':t[:m.start()+a.start()].count('\n')+1,'fields':af,'raw_ap_text':ab})
   if not aps: continue
   selected+=1; sf=fields(block.split('### Editorial ranking')[0]); source={'sys_id':m[1],'name':m[2],'file':str(p.relative_to(ROOT)),'file_sha256':sha(raw),'block_sha256':sha(block.encode()),'line_start':t[:m.start()].count('\n')+1,'line_end':t[:end].count('\n'),'byte_start':len(t[:m.start()].encode()),'byte_end':len(t[:end].encode()),'metadata':sf,'labeled_access_points':aps,'all_ap_ids':[a[1] for a in am],'join_fields':list(dict.fromkeys(f.strip() for ap in aps for f in ap['fields']['Useful join fields'].split(';'))),'availability':'catalog_only_unverified'}
   sources.append(source)
  manifest.append({'file':str(p.relative_to(ROOT)),'sha256':sha(raw),'bytes':len(raw),'systems':len(ms),'explicit_labeled_systems':selected,'explicit_labeled_ap_occurrences':labeled})
 assert len(sources)==344 and len(set(all_ids))==1555 and len(set(all_aps))==2516
 assert [m['explicit_labeled_systems'] for m in manifest]==[267,77,0,0,0]
 (OUT/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
 (OUT/'source-manifest.json').write_text(json.dumps({'files':manifest,'unique_systems':len(set(all_ids)),'unique_access_points':len(set(all_aps)),'selected_systems':len(sources),'older_Rabbit2_excluded':'Superseded duplicate volume, not a sixth volume.'},indent=2)+'\n')
 return sources
if __name__=='__main__': run()
