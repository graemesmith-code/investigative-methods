import json
from evaluate import P,write
for id in ['C01','E01','E02']:
 d=json.loads((P/'dossiers/stage2'/f'{id}.json').read_text())
 d['evidence'].append({'citation':'history-original-access.json; sources/original-*.html and *.txt','fact':'All137 unique originals in four paginated corporate-history queries now acquired and text extracted: Stark13,ELTA6,IsraelAerospace56,IAINorthAmerica62. No State of Israel text in Stark,ELTA or IsraelAerospace query originals; Pillsbury LD1 lists State of Israel. This is query-bounded evidence, not proof no alias/misindex exists.'})
 if id=='C01':
  d['evidence'].append({'citation':'https://efile.fara.gov/docs/7518-Exhibit-AB-20251212-5.pdf#page=12','fact':'Further original contract review: physicalp12 expressly identifies Stark as subsidiary ofIAI NorthAmerica, which is subsidiary ofIsraelAerospaceIndustries. Six-month termNov1 2025-Apr30 2026; $45000/month,$270000 fixedfee,plus up to$100000 reimbursable expenses. Signaturesphysicalp17 datedNov7 2025 (not executionNov1). Physicalpp11,18 scope supportsIAI andStark withgovernment/media outreach; contract does not prove actual amounts paid. Do not combine fullterm fee with2025LDAincome as annual spending. Ownership snapshot is still later thanEmanuelOct20 filing. FARA7518Sept11amendmentoriginalp1 addsCoteDIvoireparty, notStark; reject as same-registrant different-principal.'})
 write(P/'dossiers/stage3'/f'{id}.json',d)
