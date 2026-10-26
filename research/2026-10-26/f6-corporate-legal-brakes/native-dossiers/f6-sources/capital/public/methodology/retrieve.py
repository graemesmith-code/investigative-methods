import json, pathlib, urllib.request, urllib.error, hashlib, datetime, subprocess, concurrent.futures
from lxml import html
ROOT=pathlib.Path(__file__).parent
def fetch(d):
    try:
        req=urllib.request.Request(d['url'],headers={'User-Agent':'Mozilla/5.0 (public-source research)'})
        with urllib.request.urlopen(req,timeout=45) as r:
            b=r.read(); status=r.status; effective=r.url; ct=r.headers.get('Content-Type','')
        ext='pdf' if b.startswith(b'%PDF') else 'html'
        p=ROOT/'private'/(d['id']+'.'+ext);p.write_bytes(b)
        if ext=='pdf':
            subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
            text=p.with_suffix('.txt').read_text(); pages=len(text.split('\f'))-1
        else:
            tree=html.fromstring(b)
            for el in tree.xpath('//script|//style|//noscript'): el.drop_tree()
            text=tree.text_content(); text='\n'.join(x.strip() for x in text.splitlines() if x.strip());pages=None
            p.with_suffix('.txt').write_text(text)
        d.update(status=status,effective_url=effective,content_type=ct,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),text_sha256=hashlib.sha256(text.encode()).hexdigest(),pages=pages,text_characters=len(text),access_depth='full downloaded body; text extracted; image text not generally OCRed',retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),raw_publication='excluded: copyright status not licensed; private working copy',text_path=str(p.with_suffix('.txt')))
    except Exception as e: d.update(status='failed',error=str(e),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),access_depth='retrieval failure')
    return d
if __name__=='__main__':
    docs=json.loads((ROOT/'documents-input.json').read_text()); prior={d['id']:d for d in json.loads((ROOT/'private'/'retrievals.json').read_text())} if (ROOT/'private'/'retrievals.json').exists() else {}
    missing=[d for d in docs if d['id'] not in prior]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for d in ex.map(fetch,missing):
            prior[d['id']]=d;print(d['id'],d['status'],d.get('bytes',d.get('error')))
    (ROOT/'private'/'retrievals.json').write_text(json.dumps(list(prior.values()),indent=2))
