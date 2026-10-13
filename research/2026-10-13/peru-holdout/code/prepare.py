"""Prepare identical factual packets; reviewed layout selection is explicit setup, not automation."""
import json,hashlib,datetime,re,copy,time
from pathlib import Path
from lxml import html
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]; CACHE=Path('/workspace/peru-holdout-cache')
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
start=time.perf_counter();s=(CACHE/'nexa-peru-annual2025.txt').read_text();tree=html.fromstring((CACHE/'nexa-sec2025.html').read_bytes());table=tree.xpath('//table')[301]
en=' '.join(table.text_content().split()); alltext=' '.join(tree.text_content().split())
# Reviewed table locator 301 is zero-based lxml document order; locate scalar rows automatically.
rows={}
for tr in table.xpath('.//tr'):
 vals=[' '.join(x.text_content().split()) for x in tr.xpath('./td|./th')]
 if vals and any(vals[0].startswith(m+' (in ') for m in ['Zinc','Copper','Lead','Silver','Gold']) and '%' not in vals[0] and 'ounces per tonne' not in vals[0]:rows[vals[0].split(' (')[0]]=vals
sp=s[s.index('Tabla 4. Producción Anual de la UM Cerro Lindo'):s.index('Inventario de Reservas y Recursos',s.index('Tabla 4.'))]
# Exact source snippets: title and ownership come from SEC mine section; Spanish scope page7.
pos=alltext.index('Cerro Lindo. Our Cerro Lindo mine');ownership=alltext[pos:alltext.index('The',pos+100) if False else pos+680]
spanish_context=s[s.index('CERRO LINDO\n'):s.index('Tabla 3. Información General')]
spanish_scope=s[s.index('Este documento presenta los impactos'):s.index('A la fecha de emisión')]
spanish_status=' '.join(s.splitlines()[13:16]);access=[json.loads(x) for x in (ROOT/'provenance/acquisition.jsonl').read_text().splitlines()];sources={r['id']:r for r in access}
sec=sources['nexa-sec2025.html'];es=sources['nexa-peru-annual2025.pdf'];filings=json.loads((ROOT/'provenance/nexa-sec-submissions.json').read_text())['filings']['recent'];idx=filings['primaryDocument'].index('nexaform20f_2025.htm');secdate=filings['filingDate'][idx]
meta={'english':{'url':sec['url'],'sha256':sec['sha256'],'class':'SEC company 20-F','filing_date':secdate,'locator':'printed page57; HTML table301 (zero-based lxml //table); 2025 first annual column'},'spanish':{'url':es['url'],'sha256':es['sha256'],'class':'Company-hosted signed preliminary annual report; NOT independently retrieved from SMV','document_date':'2026-02-26 digital signature','locator':'PDF pages1,7,16-17; table4, 2025 second annual column','preliminary':True}}
write(ROOT/'provenance/source-pair.json',meta)
metals={'Zn':('Zinc','Zinc','t'),'Cu':('Copper','Cobre','t'),'Pb':('Lead','Plomo','t'),'Ag':('Silver','Contenidos de Plata','oz'),'Au':('Gold','Contenidos de Oro','oz')};packets=[];reference=[]
for metal,(ename,sname,unit) in metals.items():
 erow=rows[ename];val=next(x for x in erow[1:] if re.fullmatch(r'[\d,]+',x));vals=re.search(re.escape(sname)+r'\s+(?:tmf|Oz)\s+([\d,]+)\s+([\d,]+)',sp)
 if not vals:raise ValueError('Reviewed Spanish layout missing')
 ev=val.replace(',','');sv=vals.group(2).replace(',','')
 p={'id':f'CL-2025-{metal}','kind':'natural_holdout','target':{'entity':'Cerro Lindo','year':2025,'metal':metal},'sources':meta,'evidence':{'english':{'ownership_context':ownership,'table_title':'Cerro Lindo mine: Metal contained in concentrates production','heading':'For the Year Ended December 31, 2025 2024 2023','row':' '.join(erow),'value':ev,'unit':unit,'display_step':'1','year':2025,'product_scope':'metal contained in concentrates production'},'spanish':{'mine_context':spanish_context,'report_scope':spanish_scope,'version_context':spanish_status,'table_text':sp,'value':sv,'unit':unit,'display_step':'1','year':2025,'product_scope':'Producción de finos (tmf: tonelada métrica fina); contenidos de plata/oro (Oz)' }},'instruction':'Assess only supplied original bilingual excerpts and source provenance. Numbers are extracted by shared Python and arithmetic is downstream code; never infer absent scope from equality. Preliminary source is preliminary, not final approved or ministry return. No misconduct conclusion.'}
 packets.append(p)
 reference.append({'id':p['id'],'gates':{k:'supported' for k in json.loads((ROOT/'questions.json').read_text())},'classification':'comparable_agreement','source_grounded_reason':'Same Cerro Lindo full2025 mine output: SEC explicitly wholly-owned mine and metal contained in concentrate; Spanish full calendar-year scope, mine-specific fine metal/content table and concentrate description. One table100% unit output despite parent83.55% share. Identifiable preliminary company version, not final/SMV-certified. Both scalar rows match at integer display precision. No observed natural mismatch.','human_label':False,'independent_blind_review':False})
# Engineered guard fixtures reuse an admitted natural packet; all changes prominently labelled fictional.
base=packets[0]
stresses=[('S01-quantity','comparable_numerical_difference'),('S02-year','invalid_comparison'),('S03-unit','invalid_comparison'),('S04-missing','insufficient_evidence'),('S05-ownership','invalid_comparison')]
for id,expected in stresses:
 p=copy.deepcopy(base);p['id']=id;p['kind']='engineered_stress';p['fixture_warning']='Planted fictional change to a real evidence packet. Never a discovery or natural prevalence observation.';es=p['evidence']['spanish'];g={k:'supported' for k in json.loads((ROOT/'questions.json').read_text())}
 if id=='S01-quantity':
  new=str((Decimal(es['value'])*Decimal('1.10')).quantize(Decimal('1')));es['table_text']=es['table_text'].replace('87,141',f'{int(new):,}');es['value']=new
 elif id=='S02-year':
  es['year']=2024;es['report_scope']='Fictional: esta tabla cubre solamente el año calendario 2024.';es['table_text']='Fictional: Producción de finos de Zinc, Cerro Lindo, año2024, tmf '+es['value'];g['period_ownership']='conflict'
 elif id=='S03-unit':
  es['unit']='m3';es['table_text']='Fictional: Cerro Lindo 2025, zinc, volumen en m3 '+es['value'];g['units']='conflict';g['measurement_product']='conflict'
 elif id=='S04-missing':
  es['value']=None;es['table_text']=es['table_text'].replace('87,141','—');p['fixture_note']='Spanish2025 zinc value explicitly unavailable, not zero.'
 elif id=='S05-ownership':
  es['report_scope']='Fictional footnote: cantidades corresponden solo al periodo1julio–31diciembre2025 después de adquisición; producción atribuible al83.55%, no producción100% de la mina.';g['period_ownership']='conflict'
 packets.append(p);reference.append({'id':id,'gates':g,'classification':expected,'human_label':False,'independent_blind_review':False,'reason':'Known engineered fixture; guard expectation fixed by protocol before arm calls.'})
for p in packets:write(ROOT/'packets'/f'{p["id"]}.json',p)
write(ROOT/'reference-review.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'Same assistant preparing packets; source-grounded, pre-output, not independent human labels. No separate model used as truth.','rows':reference})
audit=json.loads((ROOT/'provenance/freshness-audit.json').read_text());audit['new_document_hash_overlap']={k:v['sha256'] in audit['prior_document_hashes'] for k,v in meta.items()};audit['new_assertion_keys']=[['Cerro Lindo',m,2025] for m in metals];audit['decision_2025']='Admitted as fresh against available committed baseline: new hashes, no prior2025 Cerro production assertion found; prior2025 mentions were publication/signature/other-company dates and registry buckets. Same-document comparative2024 excluded; unseen uncommitted prior assistant history cannot be proven absent.'
# Repository-wide audit uses tracked baseline, excluding new branch artifacts.
import subprocess
hits=[]
for file in subprocess.check_output(['git','ls-tree','-r','--name-only','c319cce044c416a90bb4b7e5ac81d49ec63fb11f'],text=True).splitlines():
 if file.endswith(('.json','.md','.jsonl','.txt','.csv','.py')):
  try:txt=Path(file).read_text()
  except (UnicodeError,OSError):continue
  for n,line in enumerate(txt.splitlines(),1):
   if '2025' in line and re.search(r'Cerro Lindo|NEXA|nexa',line):hits.append({'file':file,'line':n,'excerpt':line[:350]})
audit['baseline_repo_same_line2025_mentions']=hits;write(ROOT/'provenance/freshness-audit.json',audit)
write(ROOT/'provenance/packet-freeze.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packet_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'packets').glob('*.json'))},'reference_sha256':hashlib.sha256((ROOT/'reference-review.json').read_bytes()).hexdigest(),'no_paid_calls_yet':True,'preparation_script_elapsed_seconds':time.perf_counter()-start,'manual_or_assistant_layout_prep_window':'08:50–08:55 UTC approx; wall window includes reasoning/acquisition; no human stopwatch, no invented labor charge'})
print('Prepared',len(packets),'packets; values',[(p['id'],p['evidence']['english']['value'],p['evidence']['spanish']['value']) for p in packets[:5]])
