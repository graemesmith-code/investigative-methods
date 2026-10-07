"""Validate complete rendered registrant responses; retain original duplicate rows.

The files are web-reader renderings, not byte-identical API downloads. Overlapping
line numbers must agree and every advertised line must exist before JSON parsing.
No paid service, URL guessing, or network access is used by this verifier.
"""
import json,re,collections,hashlib
from acquire import P,S

def reconstruct(status,total):
    files=list(S.glob(f'fara-browser-*{status}-*.txt'))
    if status=='Active':
        files+=list(S.glob('fara-browser-active-*.txt'))+[S/'fara-browser-initial.txt']
    lines={};sources=[]
    for f in sorted(set(files)):
        body=f.read_text().split('--------------------------------------------------------------------------------')[0]
        if f'/Registrants/json/{status}' not in body:continue
        sources.append({'file':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
        for number,text in re.findall(r'^L(\d+): (.*)$',body,re.M):
            number=int(number)
            if number in lines and lines[number]!=text:raise ValueError(f'Conflicting line {number}: {f}')
            lines[number]=text
    assert set(lines)==set(range(total)),f'{status}: missing lines {set(range(total))-set(lines)}'
    data=json.loads(' '.join(lines[i] for i in range(total)))
    rows=data[f'REGISTRANTS_{status.upper()}']['ROW']
    result={'provenance':'Reconstructed from complete indexed web-reader lines; not raw response bytes. Whitespace at rendered line breaks is normalized. Raw rendered chunks and their hashes are preserved.','url':f'https://efile.fara.gov/api/v1/Registrants/json/{status}','rendered_line_count':total,'sources':sources,'data':data}
    (P/f'fara-{status.lower()}-browser-inventory.json').write_text(json.dumps(result,indent=2))
    return rows

def run():
    active=reconstruct('Active',68);terminated=reconstruct('Terminated',769)
    counts=collections.Counter(r['Registration_Number'] for r in active+terminated)
    assert not ({r['Registration_Number'] for r in active}&{r['Registration_Number'] for r in terminated})
    out={'snapshot_date':'2026-10-07','active_rows':len(active),'terminated_rows':len(terminated),'unique_registration_numbers':len(counts),'duplicate_number_rows':[r for r in active+terminated if counts[r['Registration_Number']]>1],'registrant_rendered_responses_complete':True,'raw_bulk_files_acquired':0,'full_foreign_principal_inventory_acquired':False,'full_document_inventory_acquired':False,'original_document_corpus_complete':False,'legal_analysis_complete':False,'interpretation':'Complete rendered endpoint responses, not independently reconciled against bulk bytes or all historical filings. Preserve distinct termination rows; never infer active or terminated status at a past filing date from current status alone.'}
    (P/'fara-inventory-coverage.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
if __name__=='__main__':run()
