#!/usr/bin/env python3
"""Regenerate the 75-source reading pack from the public Drive master CSV.

No original private workspace or source bodies are needed. The rank IDs refer to
aliases preserved in the master. This is a rendering check, not new verification.
"""
import argparse,csv,json
from pathlib import Path
from assemble_reviewed_register import RANK
def readable(value):
    try:
        obj=json.loads(value)
        if isinstance(obj,list): return '; '.join(map(str,obj))
    except (ValueError,TypeError): pass
    return value
def render(master):
    rows=list(csv.DictReader(Path(master).open()));byid={}
    for r in rows:
        for alias in r['aliases'].split(';'): byid[alias]=r
    selected=[byid[sid] for sid in RANK]
    assert len(selected)==75 and len({r['source_url'] for r in selected})==75
    lines=['# F5 ranked reading pack: 75 primary sources','','Ranked for reporting value and evidence specificity. Related mirrors, statutes, patent family members and agency views are not independent proofs. Actual access and claim limits are explicit. Newly retrieving a source is not journalistic novelty. Wider source inventories remain on Drive.','']
    for i,r in enumerate(selected,1):
        lines += [f"{i}. **[{r['title']}]({r['source_url']})** — {r['source_date']}. {readable(r['claim_supported'])} Access: {r['access_state']}. Limit: {readable(r['limits'] or r['implementation'])}",'']
    return '\n'.join(lines)+'\n'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--master',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    data=render(a.master);assert len(data.encode())<=100000;Path(a.output).write_text(data)
