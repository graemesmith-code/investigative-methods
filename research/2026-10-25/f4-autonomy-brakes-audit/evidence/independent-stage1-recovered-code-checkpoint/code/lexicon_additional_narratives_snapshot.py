"""Versioned high-recall lexicon. Token boundaries protect short acronyms.
Preliminary hits are leads, never verified program classifications.
"""
import re, unicodedata,html
LEXICON={
'A': ['ETHIC*','MORAL*','LAW OF WAR','LAWS OF WAR','LAW OF ARMED CONFLICT','LOAC','INTERNATIONAL HUMANITARIAN LAW','IHL','RULES OF ENGAGEMENT','ROE','PROPORTIONALITY','NON-COMBATANT','NONCOMBATANT','BYSTANDER','CIVILIAN HARM','CIVILIAN PROTECTION','COLLATERAL DAMAGE','UNINTENDED ENGAGEMENT','NONMALEFICENCE','DISTINCTION','DE-ESCALATION','COMBATANT DISCRIMINATION','TARGET DISCRIMINATION','ETHICAL LEGAL SOCIAL','ELSI'],
'B': ['HUMAN CONTROL','MEANINGFUL HUMAN','HUMAN JUDGMENT','HUMAN JUDGEMENT','HUMAN-IN-THE-LOOP','HUMAN-ON-THE-LOOP','HUMAN OUT OF THE LOOP','HUMAN AUTHORIZATION','HUMAN AUTHORISATION','POSITIVE CONTROL','POSITIVE AUTHORIZATION','TARGET AUTHORIZATION','TARGET AUTHORISATION','ENGAGEMENT AUTHORIZATION','HUMAN VETO','VETO','ABORT','FAIL-SAFE','FAILSAFE','SELF-DESTRUCT','BOUNDED AUTONOMY','BOUNDED ENGAGEMENT','ENGAGEMENT ENVELOPE','BOUNDED REACHABILITY','GEOfENC*','KEY LOADER','HUMAN-MACHINE TRUST','TRUST CALIBRATION','HUMAN OVERRIDE','OPERATOR OVERRIDE','WEAPON RELEASE','WEAPONS RELEASE','FIRE AUTHORIZATION'],
'C': ['RUN-TIME ASSURANCE','RUNTIME ASSURANCE','RUN TIME ASSURANCE','RTA','ASSURED AUTONOMY','TRUSTED AUTONOMY','TRUST-AWARE','SAFE AUTONOMY','SAFETY CRITICAL','FORMAL VERIFICATION','FORMAL METHODS','GUARDRAIL*','TEVV','TEST AND EVALUATION','TEST & EVALUATION','V&V','IV&V','VERIFICATION AND VALIDATION','VALIDATION AND VERIFICATION','CERTIFICATION','EXPLAINABLE AI','XAI','CALIBRAT*','UNCERTAINTY QUANTIFICATION','RED TEAM*','TRUSTED AI','TRUSTWORTHY AI','SAFE REINFORCEMENT LEARNING','SIMPLEX','ASSURANCE','ASSURED','SAFETY','SAFE','ROBUST*','RELIAB*','ADVERSARIAL','DATA POISONING','DATA DRIFT','DISTRIBUTION SHIFT','OUT-OF-DISTRIBUTION','SENSOR CONFIDENCE','CONFIDENCE CALIBRATION','SAFETY CASE','SAFETY ENVELOPE','RISK-AWARE','RISK SENSITIVE','HALLUCINAT*','SPOOF*','DECEPTION','NEUROSYMBOLIC','NEURO-SYMBOLIC','NEURO SYMBOLIC','REACHABILITY','BARRIER FUNCTION','RUNTIME MONITOR*','RUN-TIME MONITOR*','ANOMALY DETECT*','MODEL MONITOR*','MLOPS','AI ASSURANCE','AI ALIGNMENT'],
'D': ['RESPONSIBLE AI','RESPONSIBLE ARTIFICIAL INTELLIGENCE','RAI','3000.09','CHMR','CHMR-AP','CPCOE','CIVILIAN PROTECTION CENTER OF EXCELLENCE','SENIOR OFFICIAL REVIEW','NSPM-11','AI ETHICS PRINCIPLES','AI GOVERNANCE','ETHICS FRAMEWORK','ETHICAL FRAMEWORK'],
'domain': ['AI','ARTIFICIAL INTELLIGENCE','AUTONOM*','AUTOMAT*','ROBOT*','TARGET*','WEAPON*','MUNITION*','MISSILE*','LETHAL*','KILL CHAIN','FIRE CONTROL','WARFIGHT*','BATTLE*','COMBAT*','MILITARY','DEFENSE','DEFENCE','MACHINE LEARNING','DEEP LEARNING','NEURAL NETWORK*','REINFORCEMENT LEARNING','UAS','UAV','UGV','USV','UUV','UNMANNED','UNCREWED','DRONE*','SWARM*','HUMAN-MACHINE','HUMAN-AI','C2'],
'institution': ['CDAO','CHIEF DIGITAL AND AI','CHIEF DIGITAL AND ARTIFICIAL INTELLIGENCE','CHIEF DIGITAL & AI','CHIEF DIGITAL & ARTIFICIAL INTELLIGENCE','DOT&E','DOT & E','DIRECTOR OPERATIONAL TEST','DIRECTOR OF OPERATIONAL TEST','DIRECTOR, OPERATIONAL TEST','OPERATIONAL TEST AND EVALUATION','TEST RESOURCE MANAGEMENT CENTER','TRMC','DARPA I2O','DARPA STO','DARPA DSO','INFORMATION INNOVATION OFFICE','INFORMATION INNOVATION INNOVATION OFFICE','STRATEGIC TECHNOLOGY OFFICE','DEFENSE SCIENCES OFFICE','AFRL SAFE AUTONOMY'],
'program': ['ASIMOV','CALVIN','RESPECT','REBAR','GEARS','MAGNET','ANSR','ASSURED NEURO SYMBOLIC LEARNING AND REASONING','ASSURED NEURO-SYMBOLIC LEARNING AND REASONING','TIAMAT','ASSURED AUTONOMY','GUARANTEEING AI ROBUSTNESS AGAINST DECEPTION','GARD','COMPETENCE-AWARE MACHINE LEARNING','COMPETENCE AWARE MACHINE LEARNING','CAML','SAFE AUTONOMY','DCIST','STRONG','PROJECT LINCHPIN','LINCHPIN','TETRAS','JATIC','SHIELDS','TALON','QUASISTATICS','IN THE MOMENT','ITM','PERCEPTUALLY-ENABLED TASK GUIDANCE','PTG','PERCEPTUALLY ENABLED TASK GUIDANCE','LEARNING INTROSPECTIVE CONTROL','LINC','TRUSTED INTEGRATED OPERATIONS','TRUST','SOTERIA','SENTINEL'],
}
AMBIGUOUS_PROGRAMS={'RESPECT','GEARS','MAGNET','STRONG','TRUST','TALON','SHIELDS','GARD','CAML','ITM','LINC','SENTINEL','REBAR','CALVIN'}
A_PROGRAMS={'ASIMOV','CALVIN','RESPECT','REBAR','GEARS','MAGNET'}
B_PROGRAMS={'QUASISTATICS'}
D_PROGRAMS={'SHIELDS'}
GENERIC_A={'DISTINCTION','MORAL*','ETHIC*','BYSTANDER','ELSI'}
REQUIRED=['ETHIC*','MORAL*','LAW OF WAR','LAWS OF WAR','LOAC','RULES OF ENGAGEMENT','ROE','PROPORTIONALITY','NON-COMBATANT','NONCOMBATANT','BYSTANDER','CIVILIAN HARM','COLLATERAL DAMAGE','UNINTENDED ENGAGEMENT','RESPONSIBLE AI','RAI','TRUSTWORTHY AI','ELSI','3000.09','NONMALEFICENCE','CALVIN','ASIMOV','RESPECT','REBAR','GEARS','MAGNET','RUN-TIME ASSURANCE','RUNTIME ASSURANCE','RTA','ASSURED AUTONOMY','TRUSTED AUTONOMY','TRUST-AWARE','SAFE AUTONOMY','SAFETY CRITICAL','FORMAL VERIFICATION','FORMAL METHODS','GUARDRAIL*','BOUNDED AUTONOMY','FAIL-SAFE','FAILSAFE','ABORT','HUMAN CONTROL','HUMAN JUDGMENT','HUMAN-IN-THE-LOOP','TEVV','TEST AND EVALUATION','V&V','IV&V','CERTIFICATION','EXPLAINABLE AI','XAI','CALIBRAT*','UNCERTAINTY QUANTIFICATION','RED TEAM*']
def normalize(text):
 text=html.unescape(unicodedata.normalize('NFKC',text)).upper()
 text=re.sub('[\u2010-\u2015\u2212]', '-',text)
 return re.sub(r'\s+',' ',text)
def term_re(term):
 term=term.upper();wild=term.endswith('*');term=term.rstrip('*')
 p=re.escape(term).replace(r'\ ',r'[\s\-]+').replace(r'\-',r'[\s\-]?')
 return r'(?<![A-Z0-9])'+p+(r'[A-Z0-9]*' if wild else '')+r'(?![A-Z0-9])'
PATTERNS={k:[(s,re.compile(term_re(s),re.I)) for s in v] for k,v in LEXICON.items()}
PREFILTER={k:re.compile('|'.join(term_re(s) for s in v),re.I) for k,v in LEXICON.items()}
def hits(text):
 n=normalize(text)
 return {k:[term for term,p in items if p.search(n)] for k,items in PATTERNS.items() if PREFILTER[k].search(n)}
def classify(h):
 tags=set(); reasons=[]
 paired=bool(h.get('domain') and any(h.get(k) for k in 'ABCD'))
 if paired:
  reasons.append('safeguard_and_domain_cooccurrence')
  tags.update(k for k in 'ABCD' if h.get(k))
 if h.get('institution'):
  tags.add('D');reasons.append('institutional_anchor_requires_scope_review')
 if h.get('program'):
  reasons.append('program_name_direct_catch_requires_identity_review')
  ps=set(h['program']);tags.update('A' for p in ps&A_PROGRAMS);tags.update('B' for p in ps&B_PROGRAMS);tags.update('D' for p in ps&D_PROGRAMS)
  if ps-A_PROGRAMS-B_PROGRAMS-D_PROGRAMS:tags.add('C')
 return sorted(tags),reasons
assert not set(REQUIRED)-set(sum(LEXICON.values(),[]))
if __name__=='__main__':
 import json;print(json.dumps(LEXICON,indent=2))
# Round 2 editor challenge, preserved separately from initial regex lexicon.
ROUND2_ADDITIONS={'A':['DEONTIC*','NORMATIVE','ETHICAL CONSTRUCT*','CONDUCT ASSURANCE','OBLIGATIONS PERMISSIONS PROHIBITIONS','COMBATANT NONCOMBATANT','COMBATANT NON-COMBATANT','CIVILIAN CLASSIFICATION'], 'program':['CODORD','CATE','CETLAWS','TEELAWS','RAIDER','CAMP']}
for _k,_vs in ROUND2_ADDITIONS.items():LEXICON[_k].extend(_vs)
A_PROGRAMS.update({'CODORD','CATE','CETLAWS','TEELAWS'});AMBIGUOUS_PROGRAMS.update({'CATE','CAMP','RAIDER'})
# Token-trie matcher: punctuation/hyphen/whitespace variations canonicalized;
# acronym boundaries remain exact; wildcard stem applies only to final token.
_TOKEN=re.compile(r'[A-Z0-9]+(?:[&.][A-Z0-9]+)*|&')
_INDEX={}
for _group,_terms in LEXICON.items():
 for _term in _terms:
  _seq=tuple(_TOKEN.findall(normalize(_term.rstrip('*'))))
  if not _seq:continue
  _INDEX.setdefault(_seq[0] if len(_seq)>1 or not _term.endswith('*') else '*',[]).append((_seq,_term.endswith('*'),_group,_term))
def hits(text):
 tokens=_TOKEN.findall(normalize(text));found={}
 for i,tok in enumerate(tokens):
  for seq,wild,g,term in _INDEX.get(tok,[])+_INDEX.get('*',[]):
   if i+len(seq)>len(tokens):continue
   ok=True
   for j,s in enumerate(seq):
    actual=tokens[i+j]
    if not (actual.startswith(s) if wild and j==len(seq)-1 else actual==s):ok=False;break
   if ok:found.setdefault(g,set()).add(term)
 return {g:[term for term in LEXICON[g] if term in ts] for g,ts in found.items()}
# Round 3 known-positive calibration and scope corrections.
ROUND3_ADDITIONS={'A':['MACHINE ETHICS','POLICY COMPLIANCE','NORM COMPLIANCE','LEGAL COMPLIANCE'], 'domain':['AGENT*','ARTIFICIAL AGENCY'], 'program':['HAMLET','CASPER','ADAPTIVE ETHICAL REASONING','NORMATIVE']}
for _k,_vs in ROUND3_ADDITIONS.items():LEXICON[_k].extend(_vs)
A_PROGRAMS.discard('CATE')  # CaTE is calibrated trust measurement/evaluation, not proven LOAC.
A_PROGRAMS.update({'HAMLET','CASPER','ADAPTIVE ETHICAL REASONING','NORMATIVE'})
AMBIGUOUS_PROGRAMS.update({'HAMLET','CASPER'})
_INDEX={}
for _group,_terms in LEXICON.items():
 for _term in _terms:
  _seq=tuple(_TOKEN.findall(normalize(_term.rstrip('*'))))
  if _seq:_INDEX.setdefault(_seq[0] if len(_seq)>1 or not _term.endswith('*') else '*',[]).append((_seq,_term.endswith('*'),_group,_term))
