"""Machine indexing only; this script makes no reading or investigative claims.
Run after census.py/acquire.py. Full texts stay in /tmp/legal-enforcement.
Offsets are Python Unicode character offsets in extracted page-marked text.
No excerpts or copyrighted bulk text are written to the research repository.
"""
import pathlib,json,hashlib,re,collections,datetime
P=pathlib.Path(__file__).parent
CACHE=pathlib.Path('/tmp/legal-enforcement')
TERMS={
 'manual_labour':r'\b(?:manual(?:ly)?|labou?r(?:ious|intensive)?|time.consuming|manuell?e?s?|fastidieu\w*|chronophage\w*)\b',
 'cost':r'\b(?:costs?|expensive|affordab\w*|coûts?|couteu\w*|coûteu\w*)\b',
 'data':r'\b(?:data|dataset\w*|données?|donnees?)\b',
 'access':r'\b(?:access\w*|inaccess\w*|accès|acces|available|unavailable|disponib\w*|indisponib\w*)\b',
 'pdf_format':r'\b(?:pdf|scanned|ocr|unstructured|machine.readable|format\w*|numéris\w*)\b',
 'ownership_registry':r'\b(?:ownership|beneficial|registr(?:y|ies)|registers?|bénéficiaires?|beneficiaires?|registre\w*|propriét\w*|propriet\w*)\b',
 'payments':r'\b(?:payments?|paiements?|versements?|receipts?|recettes?)\b',
 'invoice_trade':r'\b(?:invoic\w*|misinvoic\w*|factur\w*|trade|commerce|customs|douan\w*)\b',
 'procurement':r'\b(?:procurement|tenders?|contracts?|marchés?|marches?|appels? d.offres?)\b',
 'bottleneck_missing':r'\b(?:bottleneck\w*|barriers?|limitations?|incomplete|missing|fragment\w*|obstacles?|lacunes?|incompl\w*|manquant\w*)\b',
 'identity_join':r'\b(?:identit\w*|identif\w*|names?|noms?|matching|reconcil\w*|rapprochement\w*)\b',
 'financial_evidence':r'\b(?:bank|banks|banking|banqu\w*|confidential\w*|intelligence|private|privé\w*|seized|saisi\w*)\b'
}
rows=[];missing=[];totals=collections.Counter();orgs=collections.defaultdict(collections.Counter)
for r in map(json.loads,(P/'inventory.jsonl').read_text().splitlines()):
 if not r.get('report_sha256') or not r.get('report_url'):continue
 f=CACHE/(hashlib.sha256(r['report_url'].encode()).hexdigest()+'.txt')
 if not f.exists():missing.append({'url':r['url'],'report_url':r['report_url'],'status':'text_cache_missing'});continue
 b=f.read_bytes();t=b.decode('utf-8');
 if not t.strip():missing.append({'url':r['url'],'report_url':r['report_url'],'status':'empty_text'});continue
 # Page markers are derived by acquire.py from the PDF's zero-based pages +1.
 pages=[(m.start(),int(m.group(1))) for m in re.finditer(r'\[PAGE (\d+)\]',t)]
 def page_at(offset):
  result=None
  for pos,num in pages:
   if pos>offset:break
   result=num
  return result
 hits={}
 for name,pat in TERMS.items():
  matches=list(re.finditer(pat,t,re.I));totals[name]+=len(matches)
  hits[name]={'count':len(matches),'first_positions':[{'char_offset':m.start(),'pdf_page':page_at(m.start())} for m in matches[:3]]}
 rows.append({'org':r['org'],'canonical_url':r['url'],'report_url':r['report_url'],'report_sha256':r['report_sha256'],'cache_text_sha256':hashlib.sha256(b).hexdigest(),'char_count':len(t),'byte_count':len(b),'page_marker_count':len(pages),'cache_path':str(f),'screening_type':'fulltext_machine_keyword_index_only','term_hits':hits})
 orgs[r['org']]['nonempty_fulltext_machine_screened']+=1
P.joinpath('machine-screen.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
summary={'record_count':len(rows),'scope':'canonical acquired PDF reports only; merged language/version manifestations excluded from this count','missing_or_empty_count':len(missing),'by_org':dict(orgs),'term_totals':dict(totals),'terms':TERMS,'character_offset_unit':'Python Unicode characters in cache text','no_contextual_reading_claim':True,'missing_or_empty':missing}
P.joinpath('machine-screen-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in summary.items() if k in ['record_count','missing_or_empty_count','by_org','term_totals']},indent=2))
