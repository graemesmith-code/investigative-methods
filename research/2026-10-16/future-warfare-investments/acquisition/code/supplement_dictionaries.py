#!/usr/bin/env python3
import csv,json
from bs4 import BeautifulSoup
from acquire import ROOT,DATA
s=BeautifulSoup((DATA/'raw/sbir_docs/data_dictionary.html').read_text(),'html.parser');official={}
for tr in s.find('table').find_all('tr')[1:]:
 vals=[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'])]
 if len(vals)>=7:official[vals[2].casefold()]={'definition':vals[3],'form_type':vals[5],'format':vals[6],'source':'https://www.sbir.gov/data-resources/data-dictionary'}
cols=next(csv.reader((DATA/'raw/sbir_current/award_data.csv').open(encoding='utf-8-sig')));rows=[]
for field in cols:
 v=official.get(field.casefold(),{})
 if field=='Proposal Receipt Date':v={'definition':'Proposal receipt date as labeled in bulk export; not award/performance date. Online dictionary uses Proposal Submitted Date; do not silently equate terminology for timeliness analysis.','form_type':'date','format':'MM/DD/YYYY or blank','source':'bulk CSV label; compare online dictionary'}
 if not v:
  role='principal investigator' if field.startswith('PI ') else ('research institution contact' if field.startswith('RI POC ') else ('research institution' if field=='RI Name' else 'award company contact'))
  v={'definition':'Public '+role+' '+field.split(' ',1)[-1].lower()+' field supplied in bulk export. Not an entity/award join or monetary measure.','form_type':'text','format':'source string; may be blank','source':'bulk CSV header; role inferred from header'}
 rows.append({'field':field,**v})
with (ROOT/'validation/sbir_fields.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
j=json.loads((ROOT/'validation/grants_profile.json').read_text());definitions={
 'OpportunityID':'Grants.gov numeric opportunity identifier; record-link key, not award ID.',
 'OpportunityNumber':'Agency opportunity/solicitation number; not a guaranteed later award key.',
 'OpportunityTitle':'Published opportunity title.',
 'PostDate':'Posting date; MMDDYYYY; selection uses FY derived from this date.',
 'CloseDate':'Application closing date; not award date.',
 'LastUpdatedDate':'Metadata update date; not a new award or new funding.',
 'ArchiveDate':'Opportunity archive date; not end of contract performance.',
 'Version':'Current synopsis/forecast version in this snapshot; not a historical-version census.',
 'CFDANumbers':'Assistance Listing / legacy CFDA program number(s); does not identify an award.',
 'AgencyCode':'Publisher agency/component code; security selection uses explicit prefixes.',
 'AgencyName':'Publisher agency/component name.',
 'Description':'Published narrative, possibly escaped HTML; canonical text strips HTML for analysis.',
 'AwardCeiling':'Expected maximum individual award amount, USD; funding intent only; zero may be unspecified.',
 'AwardFloor':'Expected minimum individual award amount, USD; funding intent only.',
 'EstimatedTotalProgramFunding':'Estimated total program funding, USD; not an award or obligation.',
 'ExpectedNumberOfAwards':'Estimated award count; not monetary funding or actual award count.',
 'CostSharingOrMatchingRequirement':'Whether matching is requested; not the amount of federal/nonfederal spending.',
 'FundingInstrumentType':'Anticipated instrument classification; not an executed instrument.'}
rows=[{'field':k,'presence_count_raw':n,'definition':definitions.get(k,'Published XML field; retain source label and source schema context. See raw XML; no award or monetary meaning inferred.'),'source_schema':'http://apply.grants.gov/system/OpportunityDetail-V1.0','repeated_values':'Selected-source JSONL retains original repeated-element arrays; flattened source Parquet joins repeated values with semicolons.'} for k,n in sorted(j.get('field_presence_counts_raw',{}).items())]
with (ROOT/'validation/grants_fields.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Supplement field dictionaries',len(cols),len(rows))
