#!/usr/bin/env python3
"""Assemble the full authored Drive report; never copy raw source material."""
import argparse,hashlib,json
from pathlib import Path

APPENDICES=[('A: Licences and operator duties','f6-sources/licences/LICENCES_AND_OPERATOR_DUTIES_MEMO.md'),
 ('B: Capital and corporate governance','f6-sources/capital/public/CAPITAL-GOVERNANCE-MEMO.md'),
 ('C: Disputes, protests and lobbying','f6-sources/disputes/memo.md'),
 ('D: Legal risk, exports and jurisdiction','f6-sources/legal-risk/public/legal-risk-memo.md'),
 ('E: Actual independent three-round source-editor log','f6-editor/EDITORIAL_REVIEW_LOG.md')]
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('git_directory',type=Path);p.add_argument('native_directory',type=Path);p.add_argument('output',type=Path);p.add_argument('--correction',type=Path);a=p.parse_args()
 manifest=json.loads((a.native_directory/'TRANSFER_MANIFEST.json').read_text());lookup={x['path']:x for x in manifest['files']}
 text='F6 FULL INTEGRATED REPORT — REVIEW CANDIDATE\nFinal independent release acceptance pending. Cutoff 26 October 2026.\n\n'+(a.git_directory/'INTEGRATED_REPORT.md').read_text()
 if a.correction:
  body=a.correction.read_bytes()
  text+='\n\nPOST-FREEZE INDEPENDENT-EDITOR CORRECTION\nThis addendum governs the affected frozen passages below; original authored records remain unchanged.\nSHA256: '+hashlib.sha256(body).hexdigest()+'\n\n'+body.decode()
 for title,path in APPENDICES:
  body=(a.native_directory/path).read_bytes();item=lookup[path]
  assert len(body)==item['bytes'] and hashlib.sha256(body).hexdigest()==item['sha256']
  text+='\n\n'+'='*72+'\nAPPENDIX '+title+'\nFrozen authored source: '+path+'\nSHA256: '+item['sha256']+'\n'+'='*72+'\n\n'+body.decode()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'output':str(a.output),'bytes':a.output.stat().st_size,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'unabridged_authored_appendices':len(APPENDICES),'raw_third_party_source_copies':0}))
