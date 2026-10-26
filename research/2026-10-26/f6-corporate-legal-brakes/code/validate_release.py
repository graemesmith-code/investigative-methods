#!/usr/bin/env python3
"""Validate bounded publication and traceability; independent review is external."""
import argparse
import hashlib
import json
from pathlib import Path

def records(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]

def validate(repo_dir, data_dir, final=False):
    errors=[]
    files=[p for p in repo_dir.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    for p in files:
        if p.stat().st_size>=100000: errors.append('Git file too large: '+str(p))
        if p.suffix.lower() in ['.pdf','.zip','.gz','.xml','.csv','.jsonl']:
            errors.append('Detailed/source payload belongs on Drive: '+str(p))
    src=records(data_dir/'sources.jsonl'); occ=records(data_dir/'occurrences.jsonl')
    coverage=records(data_dir/'coverage.jsonl'); candidates=records(data_dir/'candidates.jsonl')
    ids={s['document_id'] for s in src}; oi={o['occurrence_id'] for o in occ}
    if len(ids)!=len(src): errors.append('Duplicate source IDs')
    if len(oi)!=len(occ): errors.append('Duplicate occurrence IDs')
    for o in occ:
        if o['document_id'] not in ids: errors.append('Orphan occurrence')
    for c in candidates:
        if c['document_id'] not in ids or not set(c['occurrence_ids'])<=oi:
            errors.append('Orphan candidate')
        if c['promotion_status']=='promoted':
            for k in ['legal_entity','jurisdiction','document_date','source_url',
                      'decision_maker','trigger','exceptions_override','short_evidence']:
                if not c.get(k): errors.append('Promoted record missing '+k)
    if final:
        review=data_dir/'independent_release_review.json'
        if not review.exists() or json.loads(review.read_text()).get('decision')!='accepted':
            errors.append('Independent release acceptance pending')
        if any(c.get('status')!='fully_processed' and not c.get('final_disposition') for c in coverage):
            errors.append('Explicit coverage dispositions required for incomplete sources')
    return {'errors':errors,'git_files':len(files),'source_records':len(src),
      'occurrences':len(occ),'candidates':len(candidates),'final_mode':final,
      'scope':'Mechanical consistency only; no independent legal or source acceptance.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('repo_dir',type=Path);p.add_argument('data_dir',type=Path)
    p.add_argument('--final',action='store_true');a=p.parse_args()
    result=validate(a.repo_dir,a.data_dir,a.final); print(json.dumps(result,indent=2))
    raise SystemExit(bool(result['errors']))
