"""Mechanical fulltext indexing, explicitly distinct from human/contextual reading.
Counts literal screening terms and records page character offsets, without retaining text.
Run after acquire_selected.py. Standard library only.
"""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).parent
TERMS=['corruption','beneficial ownership','payment','contract','disclosure','reconciliation','inconsistent','comparability','limitation','verification','traceability','sanction','money laundering']
def records():
    for r in json.load(open(ROOT/'nrgi_selected_acquisition.json')):
        seen=set()
        for f in r.get('report_files',[]):
            if 'sha256' not in f or f['sha256'] in seen:continue
            seen.add(f['sha256']);p=Path(f['text_file'])
            if not p.exists():continue
            b=p.read_bytes();text=b.decode('utf-8','replace');offsets=[];offset=0
            for n,page in enumerate(text.split('\f'),1):
                if page.strip():offsets.append(dict(pdf_page=n,char_start=offset,char_end=offset+len(page)))
                offset+=len(page)+1
            yield dict(org='NRGI',url=r['url'],acquisition_url=f['url'],report_sha256=f['sha256'],text_sha256=hashlib.sha256(b).hexdigest(),text_bytes=len(b),char_count=len(text),nonempty=bool(text.strip()),keyword_counts={term:len(re.findall(re.escape(term),text,re.I)) for term in TERMS},page_offsets=offsets,screening_level='machine_only',fulltext_read=False)
if __name__=='__main__':
    out=list(records())
    with open(ROOT/'machine-screen.jsonl','w') as f:
        for r in out:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    print('Machine-indexed PDF representations:',len(out),'unique hashes:',len(set(r['report_sha256'] for r in out)),'nonempty:',sum(r['nonempty'] for r in out))
