import census,json,concurrent.futures,hashlib,fitz,re
P=census.OUT
rs=[json.loads(l) for l in (P/'inventory.jsonl').read_text().splitlines()]
# PDF candidates are only substantive document links, excluding ubiquitous header annual report.
jobs=[]
for i,r in enumerate(rs):
 if r['org']=='Basel Institute on Governance':
  us=[u for u in r.get('download_urls',[]) if '.pdf' in u and '1c14abd6-9e97' not in u]
 else: us=[u for u in r.get('download_urls',[]) if '.pdf' in u and any(x in u for x in ['asso-sherpa.org','plan-vigilance.org'])][:1]
 if us: jobs.append((i,us[0]))
def run(job):
 i,u=job
 try:
  b=census.get(u);doc=fitz.open(stream=b,filetype='pdf');t='\n'.join(f'\n[PAGE {j+1}]\n'+p.get_text() for j,p in enumerate(doc));census.CACHE.joinpath(hashlib.sha256(u.encode()).hexdigest()+'.txt').write_text(t)
  return i,dict(report_url=u,report_bytes=len(b),report_sha256=hashlib.sha256(b).hexdigest(),pages=len(doc),acquisition_status='pdf_fulltext_acquired',text_chars=len(t))
 except Exception as e:return i,dict(report_url=u,report_error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for i,v in ex.map(run,jobs):rs[i].update(v)
# Deduplicate identical report hashes (versions/languages with different hashes remain explicitly visible).
seen={};keep=[];dup=[]
for r in rs:
 h=r.get('report_sha256')
 if h and h in seen:dup.append(dict(url=r['url'],canonical=seen[h],reason='identical report SHA256'));continue
 if h:seen[h]=r['url']
 keep.append(r)
P.joinpath('deduplication.json').write_text(json.dumps(dup,indent=2));P.joinpath('inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in keep));print('reports attempted',len(jobs),'success',sum('report_sha256' in r for r in rs),'dedup',len(dup),flush=True)
