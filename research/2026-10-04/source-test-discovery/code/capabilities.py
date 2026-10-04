"""Enumerate field semantics without pretending source-local identifiers interoperate."""
import json,re,collections
from normalize import OUT
from build import csvwrite,dump,jl
IDENTIFIERS={
 'LEI':r'\blei\b','IMO_ship':r'(?:vessel|ship) imo|imo (?:ship|number)|\bimo where',
 'IMO_company':r'imo company','MMSI':r'\bmmsi\b','ICAO24':r'icao 24',
 'CVE':r'\bcve\b','DOI':r'\bdoi\b','ORCID':r'\borcid\b','ASN':r'\basn\b',
 'UEI':r'\buei\b','CAGE':r'\bcage\b','CIK':r'\bcik\b','CNPJ':r'\bcnpj\b',
 'CPF':r'\bcpf\b','ACN':r'\bacn\b','ABN':r'\babn\b','NZBN':r'\bnzbn\b',
 'SIREN':r'\bsiren\b','SIRET':r'\bsiret\b','CIN':r'\bcin\b','LLPIN':r'\bllpin\b',
 'UEN':r'\buen\b','KVK':r'\bkvk\b','EIN':r'\bein\b','GIIN':r'\bgiin\b',
 'NCT':r'\bnct\b','ISIN':r'\bisin\b','CUSIP':r'\bcusip\b','FIGI':r'\bfigi\b',
 'CELEX':r'\bcelex\b','ELI':r'\beli\b','Wikidata_QID':r'\bqid\b',
 'NORAD':r'\bnorad\b','COSPAR_designator':r'international designator',
 'HS_classification':r'harmonized system','CN_classification':r'combined nomenclature',
 'domain':r'\bdomain\b','IP_address':r'\bip(?: prefix)?\b','URL':r'\burl\b',
 'certificate_fingerprint':r'certificate fingerprint',
}
def main():
 rows=[];src=[]
 for s in map(json.loads,(OUT/'sources.jsonl').read_text().splitlines()):
  types=set(); namespaces=set()
  for f in s['join_fields']:
   low=f.lower(); ns=[k for k,v in IDENTIFIERS.items() if re.search(v,low)]
   if ns:
    kind='named_namespace';status='potential_exact_key_only_if_same_issuer_entity_type_value_and_date';namespaces.update(ns)
   elif re.search(r'coordinates|geometry|pixel|grid cell|bounding|quadkey|mascon|basin|river reach',low):
    kind='spatial';status='spatial_relation_not_identity; CRS_resolution_boundary_vintage_required';types.add('geographic_feature')
   elif re.search(r'country|jurisdiction|geograph|province|region|territory|economy',low):
    kind='jurisdiction_or_geography';status='aggregate_or_disambiguation_only; code_and_boundary_concordance_required';types.add('geography_or_aggregate')
   elif re.search(r'date|time|period|year|month|epoch',low):
    kind='time';status='temporal_constraint; event_vs_publication_vs_effective_date_must_be_resolved'
   elif re.search(r'id\b|number|code|reference|citation|identifier|symbol|accession|docket|registration|licence|permit|cable|document|title|order|claim',low):
    kind='source_or_jurisdiction_scoped_identifier';status='not_cross_source_compatible_without_documented_issuing_namespace_and_crosswalk'
   else:
    kind='attribute_or_role';status='not_a_stable_identity_key'
   if re.search(r'officer|director|person|donor|contributor|physician|investigator|author|inventor|lobbyist|member|insider|accused|defendant',low):types.add('person_or_role; may_also_name_entities')
   if re.search(r'company|entity|organisation|organization|parent|owner|operator|supplier|vendor|buyer|winner|recipient|sponsor|proponent|firm|issuer|registrant|client|holder|institution',low):types.add('organization_or_role; may_also_name_people')
   if re.search(r'vessel|ship|imo|mmsi',low):types.add('vessel_or_shipping_company; distinguish_namespaces')
   if re.search(r'aircraft|tail|icao',low):types.add('aircraft')
   if re.search(r'facility|site|plant|asset|project|building|mine',low):types.add('asset_site_or_project')
   if re.search(r'event|incident|occurrence|disaster|storm|conflict',low):types.add('event_or_incident')
   if re.search(r'document|filing|publication|accession|cable|request|doi|docket|case',low):types.add('document_request_or_case')
   if re.search(r'product|chemical|pollutant|mineral|commodity|ingredient|taxon|species|crop',low):types.add('substance_product_or_taxon')
   if kind=='named_namespace' and set(ns)&{'HS_classification','CN_classification'}:status='classification_key_only; versioned_concordance_and_aggregation_required; not_entity_identity'
   rows.append(dict(sys_id=s['sys_id'],source=s['name'],original_field=f,field_kind=kind,named_namespaces=ns,compatibility_constraint=status,availability='catalog_field_claim_unverified',evidence_ap_ids=[a['ap_id'] for a in s['labeled_access_points'] if f in [x.strip() for x in a['fields']['Useful join fields'].split(';')]]))
  src.append(dict(sys_id=s['sys_id'],entity_types=sorted(types) or ['collection-specific; inspect schema'],named_namespaces=sorted(namespaces),crosswalk_requirement='Source-local numbers, names, addresses and roles never silently become shared IDs.',time_rule='Retain time granularity and interval; no exact day inferred from annual observation.'))
 csvwrite(OUT/'join-field-dictionary.csv',rows);jl('source-capabilities.jsonl',src)
 dump('identifier-compatibility.json',{'named_namespace_catalog':IDENTIFIERS,'fields_classified':len(rows),'sources':344,'rules':['Same token text is not sufficient: namespace, issuing authority, entity type, actual value and effective interval must agree.','IMO ship numbers and IMO company numbers are separate.','Registration number requires registry and jurisdiction, not merely country name.','Person names require independent biographical identity; employer, address and family names are not ownership.','Local facility IDs require an official crosswalk; spatial nearest neighbor is provisional.','Country/year and product classes support aggregate comparisons, never named actor attribution.','Date fields constrain joins, they do not by themselves identify a record.','No compatibility dictionary entry verifies field presence, completeness or legal reuse.']})
if __name__=='__main__':main()
