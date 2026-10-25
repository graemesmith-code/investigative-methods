import pathlib,csv,json,xml.etree.ElementTree as E,hashlib
from decimal import Decimal as D
R=pathlib.Path(__file__).parent;rows=list(csv.DictReader(open(R/'retained-177-actions.csv')));ks=['agency_id','piid','parent_agency_id','parent_piid','modification','transaction'];m={tuple(r[k] for k in ks):r for r in rows};ns={'a':'http://www.w3.org/2005/Atom','f':'https://www.fpds.gov/FPDS'}
fields={'agency_id':'awardID/awardContractID/agencyID','piid':'awardID/awardContractID/PIID','parent_agency_id':'awardID/referencedIDVID/agencyID','parent_piid':'awardID/referencedIDVID/PIID','modification':'awardID/awardContractID/modNumber','transaction':'awardID/awardContractID/transactionNumber','signed_date':'relevantContractDates/signedDate','effective_date':'relevantContractDates/effectiveDate','current_completion':'relevantContractDates/currentCompletionDate','ultimate_completion':'relevantContractDates/ultimateCompletionDate','obligation_usd':'dollarValues/obligatedAmount','description':'contractData/descriptionOfContractRequirement'}
seen=set();errors=[];n=0;pages=[];psc=set()
for receipt in json.load(open(R/'primary-response-recovery.json')):
 p=R/receipt['path'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==receipt['historical_expected_sha256'];root=E.fromstring(b);entries=root.findall('a:entry',ns);nexts=[x.attrib['href'] for x in root.findall("a:link[@rel='next']",ns)];pages.append({'sha256':receipt['sha256'],'entries':len(entries),'next_urls':nexts})
 for e in entries:
  z=e.find('a:content/f:award',ns);assert z is not None
  r={k:z.findtext('/'.join('f:'+v for v in path.split('/')),default='',namespaces=ns) for k,path in fields.items()};key=tuple(r[k] for k in ks);assert key not in seen;seen.add(key);target=m[key]
  for k,v in r.items():
   ok=D(v)==D(target[k]) if k.endswith('_usd') else v==target[k];n+=1
   if not ok:errors.append({'identity':key,'field':k,'xml':v,'export':target[k]})
  psc.add(z.findtext('f:productOrServiceInformation/f:productOrServiceCode',default='',namespaces=ns))
out={'primary_response_bodies':len(pages),'all_raw_SHA256s_equal_pinned_export_receipts':True,'unique_actions':len(seen),'compared_fields':n,'errors':errors,'all_177_export_identities_matched':seen==set(m),'pages':pages,'psc_codes':sorted(psc)}
(R/'recovered-xml-reparse.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='pages'});assert not errors and seen==set(m)
