#!/usr/bin/env python3
"""Compare detection counts across extraction variants of identical source bytes.

Page/signal agreement is not exact semantic deduplication or OCR certification.
No source text or additional quotation is emitted.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

def records(path):return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
def compare(first,second):
    sa={x['document_id']:x for x in records(first/'sources.jsonl')}
    sb={x['document_id']:x for x in records(second/'sources.jsonl')}
    if set(sa)!=set(sb):raise ValueError('Extraction variants must have identical document IDs')
    for doc in sa:
        if not sa[doc].get('source_sha256') or sa[doc]['source_sha256']!=sb[doc].get('source_sha256'):
            raise ValueError('Variants have different or unknown source-byte identities')
    a=records(first/'occurrences.jsonl');b=records(second/'occurrences.jsonl')
    def counts(rows):return Counter((x['document_id'],x.get('page'),sig)
                                    for x in rows for sig in x.get('signal_ids',[]))
    ac,bc=counts(a),counts(b)
    differences=[{'document_id':k[0],'page':k[1],'signal_id':k[2],
      'first_detections':ac[k],'second_detections':bc[k],
      'disposition':'retain both variants; manually inspect before suppressing any occurrence'}
      for k in sorted(set(ac)|set(bc),key=lambda k:tuple(str(v) for v in k)) if ac[k]!=bc[k]]
    return {'primary_document_count':len(sa),'extraction_variants':2,
      'first_machine_physical_spans':sum(bool(x.get('signal_ids')) for x in a),
      'second_machine_physical_spans':sum(bool(x.get('signal_ids')) for x in b),
      'new_page_signal_pairs_in_second':len(set(bc)-set(ac)),
      'differences':differences,'limitation':'Counts compare page/signal detections, not legal claims or semantic recall.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('first',type=Path);p.add_argument('second',type=Path)
    p.add_argument('output',type=Path);a=p.parse_args();result=compare(a.first,a.second)
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
