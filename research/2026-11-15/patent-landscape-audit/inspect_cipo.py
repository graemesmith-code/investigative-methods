import zipfile,pathlib,collections,xml.etree.ElementTree as E,json,hashlib,re
base=pathlib.Path(__file__).parent;p=next(base.glob('*.zip'));z=zipfile.ZipFile(p)
counts=collections.Counter();dates=collections.defaultdict(list);kinds=collections.Counter();rows=[];hits=[]
def tag(e):return e.tag.split('}')[-1]
patterns={k:re.compile(v,re.I) for k,v in {'autonomy':r'autonom|unmanned|uncrewed','weapon':r'weapon|munition|missile|firearm|lethal','guardrail':r'safeguard|guardrail|ethical|rules of engagement|human.in.the.loop|human.on.the.loop|abort|inhibit|geofenc','AI':r'artificial intelligence|machine learning|neural network','safety':r'\bsafe|collision|avoidance'}.items()}
for n in z.namelist():
 assert not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts
 b=z.read(n)
 if not n.endswith('.xml'):
  (base/n).write_bytes(b);continue
 assert b'<!DOCTYPE' not in b and b'<!ENTITY' not in b
 r=E.fromstring(b);seen=set(tag(e) for e in r.iter());counts.update(seen)
 ident=next(e for e in r.iter() if tag(e)=='PatentPublicationIdentification');fields={tag(e):e.text for e in ident};kinds[fields.get('PatentDocumentKindCode')]+=1
 for e in r.iter():
  if tag(e) in ['PublicationDate','FilingDate','EventDate'] and e.text:dates[tag(e)].append(e.text)
 titles=[e.text for e in r.iter() if tag(e)=='InventionTitle']
 # Screen invention text only, excluding names/addresses/status event false hits. Bibliographic-only files cannot support claims screening.
 content='\n'.join(' '.join(e.itertext()) for e in r.iter() if tag(e) in ['InventionTitle','Abstract','Description','Claims'])
 matches={k:[content[max(0,m.start()-60):m.end()+100] for m in pat.finditer(content)] for k,pat in patterns.items() if pat.search(content)}
 row={'file':n,**fields,'titles':titles,'top_level':[tag(e) for e in r],'has_abstract':'Abstract' in seen,'has_description':'Description' in seen,'has_claims':'Claims' in seen}
 rows.append(row)
 if matches:hits.append({'publication':fields,'titles':titles,'matches':matches})
summary={'archive':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'members':len(z.infolist()),'expanded_bytes':sum(i.file_size for i in z.infolist()),'xml_records':len(rows),'unique_publications':len(set((r.get('PublicationNumber'),r.get('PatentDocumentKindCode')) for r in rows)),'kind_counts':kinds,'date_ranges':{k:[min(v),max(v)] for k,v in dates.items()},'patent_publication_date_range':[min(r['PublicationDate'] for r in rows),max(r['PublicationDate'] for r in rows)],'top_level_patterns':dict(collections.Counter('|'.join(r['top_level']) for r in rows)),'fields_of_interest':{k:v for k,v in counts.items() if any(s in k.lower() for s in ['abstract','description','claim','paragraph','drawing'])},'screening_hit_records':len(hits),'screening_scope':'InventionTitle, Abstract, Description, Claims elements; lexical triage only, not relevance finding','crc_bad_member':z.testzip()}
for name,obj in [('inventory',rows),('field_counts',counts),('keyword_hits',hits),('summary',summary)]: (base/(name+'.json')).write_text(json.dumps(obj,indent=2,ensure_ascii=False))
print(json.dumps(summary,indent=2));print(json.dumps(hits,indent=2)[:9000])
