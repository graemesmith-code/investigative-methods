#!/usr/bin/env python3
"""Declare a deterministic non-hit page audit frame before human inspection.

Outputs metadata only. Does not mark pages reviewed or estimate source recall.
"""
import argparse,hashlib,json,math,random
from pathlib import Path

def read(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]

def sample(sources,occurrences,seed,rate):
    if not 0<rate<=1: raise ValueError('rate must be in (0,1]')
    rows=[]
    for source in sorted(sources,key=lambda s:s['document_id']):
        doc=source['document_id'];pages=source.get('segments',[])
        hitpages={h.get('page') for h in occurrences if h['document_id']==doc}
        frame=[p for p in pages if p.get('page') not in hitpages]
        rng=random.Random(str(seed)+':'+doc)
        selected=rng.sample(frame,min(len(frame),max(1,math.ceil(len(frame)*rate)))) if frame else []
        for page in sorted(selected,key=lambda p:p['page']):
            rows.append({'document_id':doc,'page':page['page'],'clause':page.get('clause'),
              'text_sha256':hashlib.sha256(page['text'].encode()).hexdigest(),
              'seed':str(seed),'rate':rate,'frame_pages':len(frame),
              'document_stratum':'no_machine_hits' if not hitpages else 'nonhit_pages_inside_hit_document',
              'selection_status':'selected_before_manual_review','review_status':'pending',
              'language':source.get('language','unresolved'),'image_text_status':source.get('image_text_status')})
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('sources',type=Path);p.add_argument('occurrences',type=Path)
    p.add_argument('output',type=Path);p.add_argument('--seed',default='F6-2026-10-26-01')
    p.add_argument('--rate',type=float,default=.1);a=p.parse_args()
    rows=sample(read(a.sources),read(a.occurrences),a.seed,a.rate)
    a.output.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    print(json.dumps({'sample_rows':len(rows),'status':'selected; human review pending','seed':a.seed,'rate':a.rate}))
