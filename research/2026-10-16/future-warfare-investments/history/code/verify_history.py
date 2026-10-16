#!/usr/bin/env python3
"""Validate retained bytes, extraction completeness, raw schema and index pointers."""
import collections,csv,gzip,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from collect_history import ROOT,FIELDS,START,END,sha,parse,dump,write_csv

def main():
 errors=[];warnings=[];counts=collections.Counter();unhandled=[];bodychecks=[];nonrecord_substantive=[];unknown_sections=[];long_paragraphs=[]
 allrecords=[];pages=[]
 for p in sorted((ROOT/'pages').glob('*.json')):
  x=json.loads(p.read_text());pages.append(x)
  if not x.get('html_file'):continue
  b=gzip.decompress((ROOT/x['html_file']).read_bytes())
  if sha(b)!=x['response_sha256']:errors.append(f'Hash mismatch {p.name}')
  if x['status']!='ok':continue
  if x.get('parser_sha256')!=sha(Path(__file__).with_name('collect_history.py').read_bytes()):errors.append(f'Parser hash mismatch {p.name}')
  d,t,records,blocks=parse(b,x['original_url'])
  if records!=x['records']:errors.append(f'Extraction mismatch {p.name}')
  s=BeautifulSoup(b,'html.parser');body=s.select_one('div.body') or s.select_one('[itemprop="articleBody"]')
  norm=lambda s:re.sub(r'\s+','',s)
  source=norm(body.get_text());extracted=norm(' '.join(block['text'] for block in blocks if block['kind']!='official_no_awards'))
  # Official no-awards marker duplicates its short note for explicit classification.
  if source!=extracted:
   warnings.append(f'Body/block non-whitespace text differs: {p.name}')
  missing_money=[]
  # Every dollar-bearing block must be either a complete record or a retained note.
  for block in blocks:
   if '$' in block['text'] and block['kind']!='record':missing_money.append(block)
  for block in blocks:
   clean=' '.join(block['text'].split())
   if block['kind']=='note' and len(clean)>100 and not clean.startswith('*'):nonrecord_substantive.append(dict(article_id=x['article_id'],date=d,text=block['text']))
  for rec in records:
   if not rec['service_or_agency_section']:unknown_sections.append(dict(article_id=x['article_id'],date=d,paragraph_index=rec['paragraph_index']))
   if len(rec['raw_paragraph_verbatim'])>10000:long_paragraphs.append(dict(article_id=x['article_id'],date=d,paragraph_index=rec['paragraph_index'],characters=len(rec['raw_paragraph_verbatim']),prefix=rec['raw_paragraph_verbatim'][:150]))
  if missing_money:unhandled.append(dict(article_id=x['article_id'],announcement_date=d,blocks=missing_money))
  bodychecks.append(dict(article_id=x['article_id'],date=d,records=len(records),blocks=len(blocks),body_text_chars=len(body.get_text()),reconstructed_text_matches=source==extracted,nonrecord_money_blocks=len(missing_money)))
  if x.get('in_requested_period'):allrecords.extend(records);counts[d[:4]]+=len(records)
 history=list(csv.DictReader((ROOT/'pentagon_contract_paragraphs_history.csv').open(newline='')))
 if len(history)!=len(allrecords):errors.append('History CSV rows differ from in-period parsed records')
 if any(not START<=r['announcement_date']<=END for r in history):errors.append('Out-of-period row')
 if any(not r['raw_paragraph_verbatim'].strip() for r in history):errors.append('Empty paragraph')
 if len({r['record_id'] for r in history})!=len(history):errors.append('Duplicate history record ID')
 if history and list(history[0])[:6]!=FIELDS:errors.append('Raw fields differ from original schema')
 original=ROOT.parent/'raw/pentagon_contract_paragraphs_10000.csv';orig=list(csv.DictReader(original.open(newline='')))
 expected_hash='bf717bac8ad92d8c4d7d4aa6371b73b64580f0df7f3f9708cf2d798af895349c'
 if sha(original.read_bytes())!=expected_hash:errors.append('Original corpus changed')
 index=list(csv.DictReader((ROOT/'combined_deduplicated_index.csv').open(newline='')));pointers=[p for r in index for p in json.loads(r['pointers'])]
 if len(pointers)!=len(orig)+len(history):errors.append('Index pointer count mismatch')
 pointerkeys={(p['file'],p['data_row']) for p in pointers}
 expected={('../raw/pentagon_contract_paragraphs_10000.csv',n) for n in range(1,len(orig)+1)}|{('pentagon_contract_paragraphs_history.csv',n) for n in range(1,len(history)+1)}
 if pointerkeys!=expected:errors.append('Index missing or repeated row references')
 for r in index:
  for p in json.loads(r['pointers']):
   data=orig if p['file'].startswith('../raw/') else history
   rec=data[p['data_row']-1]
   key=sha(json.dumps([rec['announcement_date'],' '.join(rec['service_or_agency_section'].split()),' '.join(rec['raw_paragraph_verbatim'].split())],ensure_ascii=False).encode())
   if key!=r['dedup_key']:errors.append('Bad index dedup key')
   if p.get('paragraph_sha256')!=sha(rec['raw_paragraph_verbatim'].encode()):errors.append('Bad index pointer raw hash')
 write_csv(ROOT/'audit/page_extraction_checks.csv',bodychecks,['article_id','date','records','blocks','body_text_chars','reconstructed_text_matches','nonrecord_money_blocks'])
 dump(ROOT/'audit/nonrecord_money_blocks.json',unhandled)
 dump(ROOT/'audit/nonrecord_substantive_blocks.json',nonrecord_substantive)
 dump(ROOT/'audit/unknown_section_records.json',unknown_sections)
 dump(ROOT/'audit/paragraphs_over_10000_characters.json',long_paragraphs)
 if nonrecord_substantive:warnings.append(f'{len(nonrecord_substantive)} substantive-length notes need review')
 if unknown_sections:warnings.append(f'{len(unknown_sections)} records without a section need review')
 report=dict(errors=errors,warnings=warnings,unhandled_money_block_pages=len(unhandled),history_rows=len(history),history_rows_by_year=dict(sorted(counts.items())),original_rows=len(orig),original_sha256=sha(original.read_bytes()),index_unique_rows=len(index),index_pointer_count=len(pointers),hash_checked_pages=sum(bool(p.get('html_file')) for p in pages),successful_pages=sum(p['status']=='ok' for p in pages),history_paragraph_length_range=[min(map(lambda r:len(r['raw_paragraph_verbatim']),history)),max(map(lambda r:len(r['raw_paragraph_verbatim']),history))] if history else [],note='Verifies retained response bytes and deterministic complete-block extraction. Does not establish archive/publication coverage or financial comparability.')
 dump(ROOT/'audit/verification.json',report);print(json.dumps(report,indent=2))
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
