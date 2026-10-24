import sqlite3,json,re,csv,collections,time
from pathlib import Path
from decimal import Decimal
B=Path(__import__('os').environ.get('F2_ROOT', str(Path(__file__).resolve().parents[1]))); O=B/'lane1'; C=sqlite3.connect(B/'data/financial_actions.sqlite'); C.row_factory=sqlite3.Row
patterns={
'ai':r'\bartificial intelligence\b|\bmachine learning\b|\bdeep learning\b|\bneural\b|\breinforcement learning\b|\bcomputer vision\b|\bAI\b|\bML\b|\bATR\b|\blearn(?:ed|ing)\b|\bperception\b',
'autonomy':r'autonom|robot|unmanned|uncrewed|\bdrone|swarm|collaborative combat|\bCCA\b|\bUAV\b|\bUAS\b|\bUGV\b|\bUSV\b|\bUUV\b|\bRCV\b',
'weapons':r'weapon|munitions?|fire[ -]?control|target[ -]?(?:recognition|acquisition|classification)|terminal guid|seeker|lethality|loiter|counter[ -]?(?:uas|drone)|missile|kinetic|combat|breach|electronic warfare|electronic attack|\bEW\b|cognitive radar',
'contested':r'GPS[ -]denied|GNSS[ -]denied|comms?[ -]denied|contested|off[ -]road|attritable|remote weapon|sensor[ -]to[ -]shooter|tactical',
'transition':r'phase\s*(?:III|3)\b|APFIT|\bRDER\b|\bDIU\b|AFWERX|SOFWERX|NavalX|transition|operational|production|fielding|\b6\.[345]\b|advanced technology development|advanced component development|system development',
'vendor_name_semantics':r'autonom|robot|neural|cognit|tactic|unmanned|deep|machine|percept|vision|intellig|guidance|maritime|swarm|adaptive|aeronautic|artificial|spectrum|\bAI\b',
'psc':r'^(?:10|11|12|13|14|15|19|20|58|AC|AD|AJ|AZ)|\b(?:AC[0-9]|AD[0-9]|AJ[0-9])',
'naics':r'\b(?:336411|336412|336413|336414|336415|336419|336611|334511|334220|541713|541714|541715|541330)\b'
}
vendor_patterns={
'Overland AI':r'OVERLAND\s*(?:AI|ARTIFICIAL)', 'AimLock':r'AIM\s*LOCK','Shield AI':r'SHIELD\s*AI','Anduril':r'ANDURIL','Skydio':r'SKYDIO','Saronic':r'SARONIC','Epirus':r'EPIRUS','Ghost Robotics':r'GHOST ROBOT','EpiSci':r'EPISCI|EPISYS SCIENCE','Scientific Systems':r'SCIENTIFIC SYSTEMS','Charles River Analytics':r'CHARLES RIVER ANALYT','Kitware':r'KITWARE','Heron Systems':r'HERON SYSTEM','PhysicsAI':r'PHYSICS\s*AI','DZYNE':r'DZYNE','AeroVironment':r'AEROVIRONMENT','Leidos/Dynetics':r'LEIDOS|DYNETICS','Textron':r'TEXTRON','General Atomics':r'GENERAL ATOMIC',
'Applied Intuition':r'APPLIED INTUITION','Forterra/Robotic Research':r'FORTERRA|ROBOTIC RESEARCH','Kodiak':r'KODIAK ROBOT','Kodiak':r'KODIAK ROBOT','Auterion':r'AUTERION','Autonodyne':r'AUTONODYNE','Neros':r'NEROS','Darkhive':r'DARKHIVE','Red Cat/Teal':r'RED CAT|TEAL DRONE','ModalAI':r'MODAL\s*AI','Primordial Labs':r'PRIMORDIAL','Firestorm':r'FIRESTORM','Mach Industries':r'MACH INDUSTR','Allen Control':r'ALLEN CONTROL','Picogrid':r'PICOGRID','HavocAI':r'HAVOC\s*AI','Seasats':r'SEASATS','Saildrone':r'SAILDRONE','Sea Machines':r'SEA MACHINES','Sea Hunter/Leidos':r'SEA HUNTER','Nauticus':r'NAUTICUS|HOUSTON MECHATRONIC','Ocean Aero':r'OCEAN AERO','ACUA Ocean':r'ACUA OCEAN','Vatn':r'VATN','HII/Hydroid':r'HYDROID|HUNTINGTON INGALLS','BlueHalo':r'BLUEHALO','MORSE':r'MORSE CORP','STR':r'SYSTEMS [&A-Z ]*TECHNOLOGY RESEARCH','Neya':r'NEYA SYSTEM','Near Earth':r'NEAR EARTH AUTONOM','TurbineOne':r'TURBINE\s*ONE','Syntiant':r'SYNTIANT','SRI':r'SRI INTERNATIONAL','QinetiQ':r'QINETIQ','Ghost Autonomy':r'GHOST AUTONOM','Notch':r'NOTCH','PteroDynamics':r'PTERODYNAMICS','Vantage Robotics':r'VANTAGE ROBOT','RapidFlight':r'RAPIDFLIGHT','Edge Autonomy':r'EDGE AUTONOM|UAV FACTORY','Swarm Aero':r'SWARM AERO','Ursa Major':r'URSA MAJOR','Intellisense':r'INTELLISENSE','PDW':r'PERFORMANCE DRONE|\bPDW\b','Sightline':r'SIGHTLINE','Battle Road':r'BATTLE ROAD','Swarmer':r'SWARMER','Anello':r'ANELLO','Sandtable':r'SANDTABLE','Robust AI':r'ROBUST\s*AI','Boresight':r'BORESIGHT','Natilus':r'NATILUS','Aevex':r'AEVEX','Draper':r'DRAPER','Kratos':r'KRATOS','Lockheed Martin':r'LOCKHEED MARTIN','RTX/Raytheon':r'RAYTHEON','Boeing':r'BOEING','Northrop Grumman':r'NORTHROP GRUMMAN','BAE':r'BAE SYSTEM','CACI':r'\bCACI\b','Palantir':r'PALANTIR','Nexcepta':r'NEXCEPTA','Tiami':r'TIAMI','Wolfrider':r'WOLFRIDER','Altamar':r'ALTAMAR','Schemata':r'SCHEMATA','Analatom':r'ANALATOM','Red Six':r'RED SIX','Soar Technology':r'SOAR TECH','Galois':r'GALOIS','Decisive Point':r'DECISIVE POINT','Exyn':r'EXYN','Exail':r'EXAIL','Sarcos/Palladyne':r'SARCOS|PALLADYNE','Pratt Miller':r'PRATT.{0,5}MILLER','Ottopia':r'OTTOPIA','Curiosity Lab':r'CURIOSITY LAB','BILT':r'BEHAVIORAL INTELLIGENCE','Vectr':r'VECTR','Nemesis':r'NEMESIS','ResilienX':r'RESILIENX','Reliable Robotics':r'RELIABLE ROBOT','Merlin':r'MERLIN LAB','Daedalean':r'DAEDAL','Guardian AI':r'GUARDIAN\s*AI'
}
rx={k:re.compile(v,re.I) for k,v in patterns.items()}; vrx={k:re.compile(v,re.I) for k,v in vendor_patterns.items()}
# Known-vendor lookup covers all unique recipient names; semantic route remains independent.
name_routes={}
for (name,) in C.execute('SELECT DISTINCT entity_name FROM transactions'):
 name_routes[name]={'vendor_matches':[k for k,r in vrx.items() if r.search(name or '')], 'recipient_semantic_matches': sorted(set(m.group(0).lower() for m in rx['vendor_name_semantics'].finditer(name or '')))}
counts=collections.Counter(); awards={}; txhits=[]; route_rows=collections.defaultdict(set); fieldrows=collections.Counter(); date_min=None;date_max=None
for r0 in C.execute('SELECT * FROM transactions'):
 r=dict(r0); counts['deduplicated_transactions_screened']+=1
 for field in ['description_text','psc_text','naics_text','agency_text','capability_tags']:
  if r[field] not in ('','[]',None): fieldrows[field]+=1
 date=r['action_date']; date_min=min(date_min,date) if date_min else date; date_max=max(date_max,date) if date_max else date
 semantic=' | '.join(str(r[k] or '') for k in ['description_text','psc_text','naics_text','agency_text','capability_tags'])
 keymatches={k:sorted(set(m.group(0).lower() for m in x.finditer(semantic))) for k,x in rx.items() if k not in ['vendor_name_semantics','psc','naics']}
 keymatches={k:v for k,v in keymatches.items() if v}
 codes={k:sorted(set(m.group(0).lower() for m in rx[k].finditer(r[k+'_text'] or ''))) for k in ['psc','naics']}; codes={k:v for k,v in codes.items() if v}
 nr=name_routes.get(r['entity_name'],{}); vendors=nr.get('vendor_matches',[]); ns=nr.get('recipient_semantic_matches',[])
 routes=[]
 if keymatches: routes.append('keyword_metadata')
 if codes: routes.append('psc_naics')
 if vendors: routes.append('named_vendor')
 if ns: routes.append('recipient_semantic')
 if not routes: continue
 for rt in routes: counts['transactions_'+rt]+=1; route_rows[rt].add(r['award_key'])
 counts['union_hit_transactions']+=1
 if r['award_key'] not in awards:
  awards[r['award_key']]={'award_key':r['award_key'],'award_id':r['award_id'],'award_type':r['award_type'],'entity_names':set(),'entity_keys':set(),'sources':set(),'source_urls':set(),'first_action':date,'last_action':date,'transactions':0,'net_obligation_cents':0,'gross_positive_cents':0,'deobligation_cents':0,'calendar_year_cents':collections.Counter(),'fiscal_year_cents':collections.Counter(),'routes':set(),'vendor_matches':set(),'recipient_semantic_matches':set(),'keyword_matches':collections.defaultdict(set),'code_matches':collections.defaultdict(set),'first_row_number':r['row_number'],'evidence_descriptions':[]}
  a=awards[r['award_key']]
 a=awards[r['award_key']];
 if keymatches and r['description_text'] not in a['evidence_descriptions'] and len(a['evidence_descriptions'])<6:a['evidence_descriptions'].append(r['description_text'])
 a['entity_names'].add(r['entity_name']); a['entity_keys'].add(r['entity_key']);a['sources'].add(r['source']);a['source_urls'].add(r['source_url']);a['first_action']=min(a['first_action'],date);a['last_action']=max(a['last_action'],date);a['transactions']+=1
 cents=r['obligation_cents'] or 0;a['net_obligation_cents']+=cents;a['gross_positive_cents']+=max(0,cents);a['deobligation_cents']+=min(0,cents);a['calendar_year_cents'][date[:4]]+=cents;a['fiscal_year_cents'][str(r['fiscal_year'])]+=cents;a['routes'].update(routes);a['vendor_matches'].update(vendors);a['recipient_semantic_matches'].update(ns)
 for k,v in keymatches.items(): a['keyword_matches'][k].update(v)
 for k,v in codes.items(): a['code_matches'][k].update(v)
 txhits.append((r['row_number'],r['transaction_key'],r['award_key'],','.join(routes)))
# All hits are complete award sums where recipient name varies: retrieve entire corresponding award, not only hit rows.
C.execute('CREATE TABLE IF NOT EXISTS f2_candidate_awards(award_key TEXT PRIMARY KEY)');C.executemany('INSERT OR IGNORE INTO f2_candidate_awards VALUES(?)',[(k,) for k in awards]);C.commit()
for r0 in C.execute('SELECT t.award_key,COUNT(*) AS n,SUM(obligation_cents) AS cents,SUM(CASE WHEN obligation_cents>0 THEN obligation_cents ELSE 0 END) AS gross,SUM(CASE WHEN obligation_cents<0 THEN obligation_cents ELSE 0 END) AS deob,MIN(action_date) AS first_action,MAX(action_date) AS last_action FROM transactions t JOIN f2_candidate_awards c USING(award_key) GROUP BY t.award_key'):
 r=dict(r0);a=awards[r['award_key']];a['transactions']=r['n'];a['net_obligation_cents']=r['cents'];a['gross_positive_cents']=r['gross'];a['deobligation_cents']=r['deob'];a['first_action']=r['first_action'];a['last_action']=r['last_action'];a['calendar_year_cents']=collections.Counter();a['fiscal_year_cents']=collections.Counter()
for r in C.execute('SELECT t.award_key,SUBSTR(action_date,1,4),SUM(obligation_cents) FROM transactions t JOIN f2_candidate_awards c USING(award_key) GROUP BY t.award_key,SUBSTR(action_date,1,4)'): awards[r[0]]['calendar_year_cents'][r[1]]=r[2]
for r in C.execute('SELECT t.award_key,fiscal_year,SUM(obligation_cents) FROM transactions t JOIN f2_candidate_awards c USING(award_key) GROUP BY t.award_key,fiscal_year'): awards[r[0]]['fiscal_year_cents'][str(r[1])]=r[2]
# Large traditional integrators deliberately score lower without descriptions: broad inclusion is not promotion.
traditional={'Leidos/Dynetics','Textron','General Atomics','HII/Hydroid','SRI','QinetiQ','Draper','Kratos','Lockheed Martin','RTX/Raytheon','Boeing','Northrop Grumman','BAE','CACI','Palantir','Ursa Major','Intellisense','Red Six'}
ranked=[]
for a in awards.values():
 recent=sum(v for y,v in a['calendar_year_cents'].items() if y in ['2024','2025','2026']);prior=sum(v for y,v in a['calendar_year_cents'].items() if y<'2024'); growth= (recent/prior) if prior>0 else None
 a['net_obligation_2024_2026_cents']=recent;a['pre_2024_net_obligation_cents']=prior;a['recent_to_prior_ratio']=growth;a['growth_flag']='new_award_2024_2026' if a['first_action']>='2024-01-01' else ('recent_at_least_2x_prior' if prior>0 and recent>=2*prior else ('positive_recent_after_nonpositive_prior' if recent>0 and prior<=0 else ''))
 for field in ['entity_names','entity_keys','sources','source_urls','routes','vendor_matches','recipient_semantic_matches']: a[field]=sorted(a[field])
 for field in ['keyword_matches','code_matches']:a[field]={k:sorted(v) for k,v in a[field].items()}
 for field in ['calendar_year_cents','fiscal_year_cents']:a[field]=dict(a[field])
 nontrad=bool(set(a['vendor_matches'])-traditional)
 a['screen_score']=(12 if nontrad else (2 if a['vendor_matches'] else 0))+(4 if recent>0 else 0)+(4 if a['growth_flag'] else 0)+(3 if 10000000<=recent<=50000000000 else 0)+(2 if a['last_action']>='2025-01-01' else 0)+(3*len(a['keyword_matches']))+(2 if a['recipient_semantic_matches'] else 0)
 a['substantive_tactical_combo']=bool((set(a['keyword_matches']) & {'ai','autonomy'}) and (set(a['keyword_matches']) & {'weapons','contested'}));
 a['screen_score']+=(15 if a['substantive_tactical_combo'] else 0)+(5 if 'transition' in a['keyword_matches'] and (set(a['keyword_matches']) & {'ai','autonomy'}) else 0)
 a['screen_interpretation']='Procurement-discovery candidate only; funded award identity and net transactions do not establish autonomy, modern AI, tactical hardware, or transition. No unavailable descriptive field was searched.'
 ranked.append(a)
ranked.sort(key=lambda a:(-a['screen_score'],-a['net_obligation_2024_2026_cents'],a['award_key']))
for i,a in enumerate(ranked,1):a['selection_id']=f'L1-{i:05d}'
with (O/'candidate_register.jsonl').open('w') as f:
 for a in ranked:f.write(json.dumps(a)+'\n')
with (O/'candidate_register.tsv').open('w') as f:
 fields=['selection_id','screen_score','award_id','award_key','entity_names','vendor_matches','routes','first_action','last_action','transactions','net_obligation_cents','net_obligation_2024_2026_cents','growth_flag','calendar_year_cents','source_urls','evidence_descriptions'];w=csv.DictWriter(f,fields,delimiter='\t',extrasaction='ignore');w.writeheader()
 for a in ranked:w.writerow({k:(json.dumps(v) if isinstance(v,(dict,list)) else v) for k,v in a.items()})
with (O/'transaction_hits.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['row_number','transaction_key','award_key','routes']);w.writerows(txhits)
# Vendor summary helps select unusual smaller recipients over familiar huge headline awards.
vendors=collections.defaultdict(lambda:{'awards':0,'transactions':0,'net_obligation_cents':0,'recent_cents':0,'names':set(),'latest':''})
for a in ranked:
 for name in a['vendor_matches']:
  v=vendors[name];v['awards']+=1;v['transactions']+=a['transactions'];v['net_obligation_cents']+=a['net_obligation_cents'];v['recent_cents']+=a['net_obligation_2024_2026_cents'];v['names'].update(a['entity_names']);v['latest']=max(v['latest'],a['last_action'])
for v in vendors.values():v['names']=sorted(v['names'])
(O/'vendor_summary.json').write_text(json.dumps(dict(sorted(vendors.items(),key=lambda kv:-kv[1]['recent_cents'])),indent=2))
audit={'scan_counts':dict(counts),'unique_awards_by_route':{k:len(v) for k,v in route_rows.items()},'union_candidate_awards':len(ranked),'field_nonempty_dedup_rows':dict(fieldrows),'action_date_min':date_min,'action_date_max':date_max,'patterns':patterns,'vendor_patterns':vendor_patterns,'ai_reading_depth':'Full-file deterministic field coverage and regex screening; AI reads aggregate summaries and selected original transactions, not every line semantically. Human/AI operational review count documented separately in lane1/report.md.','screen_score':'12 nontraditional or 2 traditional vendor; +4 positive 2024–2026 dollars; +4 recent growth/new award flag; +3 recent net $100,000–$500,000,000; +2 action in 2025 or later; +3 each keyword category; +2 semantic recipient name; +15 AI/autonomy plus weapons/contested description combination; +5 transition with AI/autonomy. Score prioritizes follow-up, never validates AI or weapons content.','growth_caveat':'Ratio compares cumulative 2024–2026 vs cumulative pre-2024 archive obligations, not equal annual windows. First observation in this archive is not proof of company emergence. Negative modifications retained.'}
(O/'screen_audit.json').write_text(json.dumps(audit,indent=2))
print(json.dumps(audit,indent=2));print('\nTOP 70:')
for a in ranked[:70]:print(a['selection_id'],a['screen_score'],a['award_id'],','.join(a['entity_names']),a['net_obligation_2024_2026_cents']/100,a['calendar_year_cents'])
C.close()
