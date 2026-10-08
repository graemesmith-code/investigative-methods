"""Deterministic candidate retrieval, not entailment, novelty or misconduct classification."""
import json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
pages=[json.loads(x) for x in (R/'results/pages.jsonl').read_text().splitlines()]
patterns={'irrigation_scope':r'\b(?:additional|total|baseline|17,200|20,000|30,000)\b','benchmark_changes':r'\b(?:revised|changed|new target|replaced)\b','monitoring_gaps':r'\b(?:no information|no reliable|not available|no specific monitoring|could not|cannot be measured)\b','cost_comparison':r'cost.output|implementing agency|efficien'}
rows=[]
for p in pages:
 text=' '.join(p['text'].split())
 for test,pattern in patterns.items():
  if test=='irrigation_scope' and not any(w in text.lower() for w in ['hectare','irrigat']):continue
  for m in re.finditer(pattern,text,re.I):
   rows.append(dict(test=test,document=p['document'],pdf_page=p['pdf_page'],citation=p['citation'],matched=m.group(),context=text[max(0,m.start()-150):m.end()+250],status='unreviewed candidate'))
(R/'results/candidates.json').write_text(json.dumps(rows,indent=2))
# A fixed reading packet chosen by assistant review, explicitly separate from algorithmic ranking.
chosen={'CP12-2-5-2009E':[13,26],'CP12-2-14-2012-eng':[9,23,26,53,54],'FR5-95-2015-eng':[36,37,53]}
packet=[p for p in pages if p['pdf_page'] in chosen.get(p['document'],[])]
(R/'results/review-packet.json').write_text(json.dumps(packet,indent=2))
chars=sum(len(x['text']) for x in packet)
cost={'method':'character-based estimate only, 3–5 characters per input token; not provider tokenization','full_corpus_characters':sum(len(x['text']) for x in pages),'review_packet_pages':len(packet),'review_packet_characters':chars,'input_tokens_estimated_range':[round(chars/5),round(chars/3)],'output_budget_tokens':3000,'cost_formula_usd':'input_tokens * input_price_per_million / 1000000 + 3000 * output_price_per_million / 1000000','illustrative_prices_not_verified_or_selected':{'input_usd_per_million':0.10,'output_usd_per_million':0.40},'illustrative_packet_cost_usd_range':[round(chars/5*.1/1e6+.0012,6),round(chars/3*.1/1e6+.0012,6)],'paid_calls_authorized':False,'paid_calls_made':0,'note':'No model credentials read. Platform assistant analysis is separate; no total platform cost claim.'}
(R/'results/model-cost-design.json').write_text(json.dumps(cost,indent=2))
print('Candidates',len(rows),'packet pages',len(packet),'characters',chars)
