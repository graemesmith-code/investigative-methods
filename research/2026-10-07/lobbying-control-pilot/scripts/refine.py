"""Audited second-pass changes; originals drive edits, not Jev confidence."""
from build_dossiers import P,save,lda
import json
p=P/'dossiers/stage2'
x=json.loads((p/'E01.json').read_text());x['evidence'][0]['fact']=x['evidence'][0]['fact'].replace('Q4 amount null (not zero); needs original checkbox interpretation.','Q4 original section12 checks Less than $5000; annual income range $87500 to below$92500.').replace('no registry identifier bridge yet.','no registry identifier bridge yet; company original product sheet dated2021-09-11 p2 gives8955 HenkelsLane AnnapolisJunctionMD20701, matching original LDA address apart from spelling transposition (https://eltanorthamerica.com/wp-content/uploads/2021/09/ENA-OTHELLO-RGB.pdf).');x['baseline']='high';save(p/'E01.json',x)
for id,name in [('C12','Haiti'),('C15','Congo')]:
 x=json.loads((P/'dossiers/stage1'/f'{id}.json').read_text());rows=json.loads((P/'sources'/f'lda-{name}-001.json').read_text())['results'];x['evidence'].append({'citation':[lda(r['filing_uuid']) for r in rows],'fact':'Original LDA client fields now acquired/read: '+', '.join(sorted({r['client']['name'] for r in rows}))+'. These do not identify the FARA government principal. No same-client pair; reject country-name join, no contradiction established.'});save(p/f'{id}.json',x)
x=json.loads((P/'dossiers/stage1/C02.json').read_text());x['evidence'].append({'citation':'https://efile.fara.gov/docs/6399-Amendment-20260302-69.pdf#page=1','fact':'Original2026-03-02 amendment names same Harena principal and updated contract/ExhibitB. It does not establish corporate control or contradict a nonexistent acquired LDA pair.'});save(p/'C02.json',x)
# Simple transparent evidence-rule baseline. Coded gates use human-verified original facts.
flags={'C01':(True,True,True,False),'E01':(True,True,True,False),'E02':(True,True,False,True),'N01':(True,True,False,False)}
out=[]
for stage in ['stage1','stage2']:
 for f in sorted((P/'dossiers'/stage).glob('*.json')):
  x=json.loads(f.read_text());id=x['id']
  if id in flags:
   identity,dated,explicit_no,partial=flags[id]
   if stage=='stage1':dated=False
   rank='high' if identity and dated and explicit_no else 'medium' if explicit_no or partial else 'low'
  else:rank='abstain' if x.get('source',{}).get('principal','present') is None else 'low'
  out.append({'stage':stage,'id':id,'priority':rank,'flags':flags.get(id)})
save(P/'dossiers/code-baseline.json',out)
