#!/usr/bin/env python3
import census as c
import json,re,hashlib,concurrent.futures,subprocess
p=c.BASE
rows=[json.loads(s) for s in (p/'inventory.jsonl').read_text().splitlines()]
terms=re.compile('money|enabl|ownership|secret|contract|procure|finance|political|lobby|badge|debt|grand corruption|loophole|export|asset|shell|climate|revolving|recovery',re.I)
selected=[r for r in rows if terms.search(r['title'])]
def acquire(r):
 b=c.get(r['url']);r['landing_bytes']=len(b);r['landing_sha256']=hashlib.sha256(b).hexdigest() if b else None
 links=list(dict.fromkeys(re.findall(r'(?:href|src)=["\'](https://[^"\']+\.pdf(?:\?[^"\']*)?)["\']',b.decode(errors='replace'))))
 links=[u for u in links if 'transparencycdn' in u]
 if links:
  # final Download link generally follows cover; first PDF link is the official report.
  u=links[0];pb=c.get(u);r['fulltext_url']=u
  if pb.startswith(b'%PDF'):
   h=hashlib.sha256(pb).hexdigest();f=c.CACHE/(h+'.pdf');f.write_bytes(pb);txt=c.CACHE/(h+'.txt')
   proc=subprocess.run(['pdftotext','-layout',str(f),str(txt)],capture_output=True)
   r.update(acquisition_status='fulltext_acquired',bytes=len(pb),sha256=h)
   if proc.returncode==0:
    t=txt.read_text(errors='replace');r['pages']=t.count('\f');r['text_characters']=len(t);r['machine_keyword_hits']=len(terms.findall(t));r['screening_rationale']='Report acquired and machine-indexed; human contextual reading pending.'
  else:r['acquisition_status']='pdf_download_failed'
 else:
  r['acquisition_status']='landing_only';r['screening_rationale']='Official abstract acquired; report download not located.'
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(acquire,selected):print(r['acquisition_status'],r['title'],flush=True)
(p/'inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
with (p/'acquisition-log.jsonl').open('a') as f:
 for l in c.LOG:f.write(json.dumps(l)+'\n')
