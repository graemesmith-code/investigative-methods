import gzip,json,sqlite3,collections,hashlib,re,time,os
from decimal import Decimal, InvalidOperation
from pathlib import Path
BASE=Path(__import__('os').environ.get('F2_ROOT', str(Path(__file__).resolve().parents[1]))); P=BASE/'data/normalized/financial_actions.jsonl.gz'; DB=BASE/'data/financial_actions.sqlite'
start=time.time(); con=sqlite3.connect(DB); con.execute('PRAGMA journal_mode=WAL'); con.execute('PRAGMA synchronous=NORMAL'); con.execute('PRAGMA temp_store=FILE')
con.executescript('''CREATE TABLE IF NOT EXISTS source_rows(row_number INTEGER PRIMARY KEY, transaction_key TEXT, award_key TEXT, award_id TEXT, award_type TEXT, award_id_parse_status TEXT, entity_key TEXT, entity_name TEXT, source TEXT, source_url TEXT, raw_locator TEXT, source_snapshot_sha256 TEXT, retrieved_at TEXT, eligibility TEXT, capability_tags TEXT, action_date TEXT, fiscal_year INTEGER, action_obligation_usd TEXT, obligation_cents INTEGER, description_text TEXT, psc_text TEXT, naics_text TEXT, agency_text TEXT, source_json TEXT);''')
cols=collections.Counter(); nonempty=collections.Counter(); sources=collections.Counter(); names=collections.Counter(); fy=collections.Counter(); tags=collections.Counter(); semantickeys=collections.Counter(); n=0; badmoney=[]; batch=[]
def valstr(v): return json.dumps(v,ensure_ascii=False,sort_keys=True) if isinstance(v,(dict,list)) else str(v)
def parse_award(s):
 if s.startswith('CONT_AWD_'):
  parts=s.split('_'); return (parts[2], 'CONT_AWD', 'parsed_from_generated_award_key') if len(parts)>=6 else ('','CONT_AWD','unparsed')
 if s.startswith('ASST_NON_'):
  parts=s.split('_'); return (parts[2], 'ASST_NON', 'parsed_from_generated_award_key') if len(parts)>=4 else ('','ASST_NON','unparsed')
 return ('','', 'unparsed')
with gzip.open(P,'rt',encoding='utf-8') as f:
 for n,line in enumerate(f,1):
  r=json.loads(line); cols.update(r.keys()); nonempty.update(k for k,v in r.items() if v not in (None,'',[],{},'[]')); sources[r.get('source','')]+=1; fy[str(r.get('fiscal_year',''))]+=1; names[r.get('entity_name','')]+=1; tags[valstr(r.get('capability_tags',''))]+=1
  money=r.get('action_obligation_usd',''); cents=None
  try: cents=int((Decimal(str(money))*100).quantize(Decimal('1')))
  except (InvalidOperation,ValueError,TypeError): badmoney.append([n,money])
  desc={k:v for k,v in r.items() if re.search(r'descri|title|abstract|purpose|project_name|programme|program_name',k,re.I)}
  psc={k:v for k,v in r.items() if re.search(r'(^psc$|product.*service.*code|^psc_)',k,re.I)}
  naics={k:v for k,v in r.items() if 'naics' in k.lower()}
  agency={k:v for k,v in r.items() if re.search(r'agency|office|department',k,re.I)}
  semantickeys.update(desc.keys()); semantickeys.update(psc.keys()); semantickeys.update(naics.keys()); semantickeys.update(agency.keys())
  aid,atype,pstatus=parse_award(r.get('award_key',''))
  batch.append((n,r.get('transaction_key',''),r.get('award_key',''),aid,atype,pstatus,r.get('entity_key',''),r.get('entity_name',''),r.get('source',''),r.get('source_url',''),r.get('raw_locator',''),r.get('source_snapshot_sha256',''),r.get('retrieved_at',''),r.get('eligibility',''),valstr(r.get('capability_tags','')),r.get('action_date',''),r.get('fiscal_year'),str(money),cents,' | '.join(valstr(v) for v in desc.values()),' | '.join(valstr(v) for v in psc.values()),' | '.join(valstr(v) for v in naics.values()),' | '.join(valstr(v) for v in agency.values()),line.strip()))
  if len(batch)>=10000:
   con.executemany('INSERT INTO source_rows VALUES('+','.join('?'*24)+')',batch); con.commit(); batch=[]
   if n%100000==0: print(n, 'rows indexed',round(time.time()-start,1),'sec',flush=True)
if batch: con.executemany('INSERT INTO source_rows VALUES('+','.join('?'*24)+')',batch); con.commit()
con.executescript('''CREATE INDEX idx_source_tx ON source_rows(transaction_key); CREATE INDEX idx_source_award ON source_rows(award_key); CREATE INDEX idx_source_award_id ON source_rows(award_id); CREATE INDEX idx_source_entity ON source_rows(entity_name COLLATE NOCASE); CREATE INDEX idx_source_entity_key ON source_rows(entity_key); CREATE INDEX idx_source_action ON source_rows(action_date); CREATE TABLE unique_transaction_rows AS SELECT transaction_key, MIN(row_number) AS row_number, COUNT(*) AS source_record_count FROM source_rows GROUP BY transaction_key; CREATE UNIQUE INDEX idx_unique_tx ON unique_transaction_rows(transaction_key); CREATE UNIQUE INDEX idx_unique_row ON unique_transaction_rows(row_number); CREATE VIEW transactions AS SELECT r.*,u.source_record_count FROM source_rows r JOIN unique_transaction_rows u USING(row_number);''')
con.commit()
counts={k:con.execute(q).fetchone()[0] for k,q in {'unique_transaction_keys':'SELECT COUNT(*) FROM unique_transaction_rows','unique_award_keys':'SELECT COUNT(DISTINCT award_key) FROM transactions','unique_entity_names':'SELECT COUNT(DISTINCT entity_name) FROM transactions','duplicate_rows':'SELECT SUM(source_record_count-1) FROM unique_transaction_rows','missing_transaction_keys':"SELECT COUNT(*) FROM source_rows WHERE transaction_key=''",'duplicate_financial_conflicts':"SELECT COUNT(*) FROM (SELECT transaction_key FROM source_rows GROUP BY transaction_key HAVING COUNT(DISTINCT award_key)>1 OR COUNT(DISTINCT action_obligation_usd)>1 OR COUNT(DISTINCT action_date)>1)",'nonzero_tags':"SELECT COUNT(*) FROM transactions WHERE capability_tags NOT IN ('[]','')"}.items()}
summary={'file':str(P),'gzip_crc_full_read':'passed','compressed_bytes':P.stat().st_size,'compressed_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'physical_rows_scanned':n,**counts,'field_presence':dict(cols),'field_nonempty':dict(nonempty),'description_psc_naics_agency_field_keys':dict(semantickeys),'sources':dict(sources),'fiscal_year_physical_rows':dict(fy),'capability_tags':dict(tags),'invalid_obligations':badmoney,'index_seconds':round(time.time()-start,2),'database':str(DB),'dedup_rule':'One financial observation per exact transaction_key, earliest source row retained; all physical rows/provenance preserved. Conflicts counted separately. Award keys remain distinct, do not merge by PIID alone. Obligations converted to integer cents; never ceilings.'}
(BASE/'lane1/coverage_audit.json').write_text(json.dumps(summary,indent=2))
con.execute('PRAGMA wal_checkpoint(TRUNCATE)'); con.close(); print(json.dumps(summary,indent=2),flush=True)
