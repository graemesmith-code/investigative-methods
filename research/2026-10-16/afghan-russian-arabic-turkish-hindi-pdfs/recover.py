import sys, json, time, concurrent.futures
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'afghan-chinese-deps'))
from download_pdfs import download_one
import fitz
ROOT=Path(__file__).resolve().parent
seen=set();pending={}

def recover(path):
    record=json.loads(path.read_text());key=record['record_key']
    out=download_one(record)
    if out.get('pdf_path'):
        try:
            doc=fitz.open(ROOT/out['pdf_path'])
            out['pdf_pages']=len(doc)
            text=[]
            for i,p in enumerate(doc):
                text.append(f'\n--- Page {i+1} ---\n'+p.get_text())
            (ROOT/'native-text'/(key+'.txt')).write_text(''.join(text))
            if len(doc):doc[0].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(ROOT/'previews'/(key+'.png'))
        except Exception as e:out['pdf_read_error']=str(e)[:200]
    out['record_key']=key
    (ROOT/'downloads'/(key+'.json')).write_text(json.dumps(out,ensure_ascii=False))
    print(out['status'],record['provenance']['config'],record['url'],flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    while True:
        for path in (ROOT/'work'/'records').glob('*.json'):
            if path.name in seen:continue
            candidate=json.loads(path.read_text())
            allowed=set(json.loads((ROOT/'work/allowed-hosts.json').read_text()))
            if not (candidate['host']=='gov.af' or candidate['host'].endswith('.gov.af') or candidate['host'] in allowed):continue
            seen.add(path.name)
            if (ROOT/'downloads'/path.name).exists():continue
            pending[pool.submit(recover,path)]=path
        for fut in list(pending):
            if not fut.done():continue
            p=pending.pop(fut)
            try:fut.result()
            except Exception as e:print('ERROR',p.name,type(e).__name__,str(e)[:100],flush=True)
        if (ROOT/'work'/'summary.json').exists() and not pending:break
        time.sleep(4)
