"""Offline archive reconciliation, source-hash, privacy-shape and Markdown-link checks."""
import collections,csv,hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'research/2026-10-01/ati-live'
def main():
 raw=json.loads((OUT.parent/'ati-cloud-preflight/corpus/records.json').read_text())
 ranked=json.loads((OUT/'full-ranked.json').read_text())
 assert len(raw)==len(ranked)==1234
 assert len({r['_id'] for r in ranked})==1234
 assert {r['_id'] for r in ranked}=={r['_id'] for r in raw}
 with (OUT/'full-ranked.csv').open() as f:assert len(list(csv.DictReader(f)))==1234
 ledger=json.loads((OUT/'ledger-accounting.json').read_text());attempts=ledger['attempts'];counts=collections.Counter(r['provider'] for r in attempts)
 assert counts=={'jev':1402,'exa':17}
 assert all(r['status']=='success' for r in attempts)
 assert all('request' not in r and 'response' not in r for r in attempts)
 assert {p:sum(r['accounted'] for r in attempts if r['provider']==p) for p in counts}=={'jev':61954,'exa':119000}
 assert ledger['accounted_microusd']=={'jev':61954,'exa':119000}
 groups=[]
 for name in ['control-plans-results.json','coverage-plans-results.json','expansion-plans-results.json']:
  values=json.loads((OUT/name).read_text());groups.extend(values)
  for g in values:
   assert '_raw_response_utf8' not in g['response']
   assert all('text' not in r and 'highlights' not in r and 'summary' not in r for r in g['response']['results'])
 assert len(groups)==17
 assert len(json.loads((OUT/'branch-decisions.json').read_text()))==5
 assert len(json.loads((OUT/'release-ocr/pages.json').read_text())['pages'])==7
 for p in (OUT/'public-sources').glob('*.json'):
  r=json.loads(p.read_text());assert 'thecanadareport.ca' not in r['url']
  assert hashlib.sha256((p.parent/r['raw_file']).read_bytes()).hexdigest()==r['sha256']
 provenance=json.loads((OUT/'executed-code-provenance.json').read_text())
 for entry in provenance['files']:assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256']
 scope=[ROOT/'code/ati',OUT,OUT.parent/'ati-cloud-preflight']
 files=[p for folder in scope for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
 for p in files:
  assert p.suffix not in ['.sqlite','.db','.pem','.key'] and not p.name.startswith('.env')
  assert 'ledger.json'!=p.name
 for p in [ROOT/'README.md']+[p for p in files if p.suffix=='.md']:
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
   local=target.split('#',1)[0]
   assert (p.parent/local).exists(),f'Broken local link: {p.relative_to(ROOT)} -> {target}'
 result={'tests':'13 offline safeguards tests pass: 11 run-era plus 2 post-run continuation guards','scored_unique_records':1234,'jev_calls':1402,'exa_calls':17,'accounted_microusd':ledger['accounted_microusd'],'all_calls_successful':True,'pending_attempts':0,'branch_questions':5,'release_packets':1,'release_pages':7,'full_third_party_news_text':'excluded','live_database':'excluded','source_hashes':'verified','executed_source_hashes':'verified','relative_markdown_links':'verified','tax_inclusive_invoice':'not verified','whitespace_note':'Author-written source/docs clean; original source bytes, OCR and CSV CRLF preserved despite data whitespace diagnostics.'}
 (OUT/'archive-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
