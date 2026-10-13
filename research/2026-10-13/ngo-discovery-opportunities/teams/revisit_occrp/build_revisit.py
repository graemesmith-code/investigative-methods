"""Reproduce metadata adjudication from documented official browser reads.
Browser query/access manifest is recorded separately; no denied-source retry.
"""
import pathlib,json
P=pathlib.Path(__file__).parent;ROOT=P.parent
original={r['url']:r for r in map(json.loads,(ROOT/'kleptocracy/inventory.jsonl').read_text().splitlines())}
records=[
 ('https://www.occrp.org/en/investigation/instead-of-helping-ukraines-poor-ferrexpos-charitable-donations-flowed-to-companies-associated-with-its-then-ceo','2026-09-16','Instead of Helping Ukraine’s Poor, Ferrexpo’s Charitable Donations Flowed to Companies Associated With Its Then-CEO','official article dateline','RO-CHARITY','Full body read including methods, bank-record provenance, related-party disagreements and responses; HTML body paragraphs corresponding to browser lines47–216.'),
 ('https://www.occrp.org/en/investigation/a-police-hq-wind-farms-and-natural-gas-mapping-the-european-holdings-of-chinas-central-bank','2026-07-24',"A Police HQ, Wind Farms, and Natural Gas: Mapping China's Investments in Europe",'official catalog date from original inventory','RO-HOLDINGS','Full methods and limitations/context read, including registry cross-reference, annual-report look-through and access restriction; body browser lines31–127.'),
 ('https://www.occrp.org/en/investigation/the-luxury-french-real-estate-of-alleged-latin-american-money-launderers-and-officials-accused-of-corruption','2023-07-05','The Luxury French Real Estate of Alleged Latin American Money Launderers and Officials Accused of Corruption','inferred from official GACC Oct15 2023 case study saying same publication day as TI Behind a Wall, which has official July5 2023 dateline; not visible in original article','RO-PROPERTY','Full body read including Data Analysis methods, deed-request requirement, registry limitations, bank/investigation-record dependencies and responses; browser lines22–144.')]
rs=[]
for u,date,title,provenance,opp,rationale in records:
 r=dict(original.get(u,{}));r.update(org='OCCRP',title=title,date=date,date_source=provenance,url=u,type='investigation',acquisition_status='official_browser_full_body_readable',fulltext_acquired=True,fulltext_screened=True,deeply_read=True,bytes=None,sha256=None,pages=None,original_bytes=None,hash_scope=None,screening_rationale=rationale,opportunity_ids=[opp],acquisition_date='2026-10-13',sampling_method='method-diversity purposive sample; no local OCCRP text index available',revisit_existing_record=u in original);rs.append(r)
P.joinpath('inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs))
P.joinpath('counts.json').write_text(json.dumps(dict(sampled_eligible_sources=3,acquired_browser_full_body=3,contextually_screened=3,deeply_read=3,retained_finalists=0,additional_existing_catalog_reads=2,new_source_records=1,supporting_case_study_reads=1,failed_article_reads=1,local_fulltexts=0,machine_screened=0,actual_spend_usd=0),indent=2))
P.joinpath('access-log.json').write_text(json.dumps([
 {'url':r['url'],'method':'official browser open; contextual follow-up open where needed','status':'readable_body','bytes':None,'sha256':None} for r in rs]+[
 {'url':'https://www.occrp.org/en/investigation/family-of-ilham-aliyevs-security-chief-owns-vast-property-holdings-in-the-united-kingdom','method':'browser open','status':'Internal Error; no retry or alternative route; not read'},
 {'url':'https://gacc.occrp.org/post/who-really-owns-french-property','method':'browser open','status':'complete24-line case study read; supporting provenance only','date':'2023-10-15'},
 {'url':'https://find-and-update.company-information.service.gov.uk/search?q=Ferrexpo','method':'browser open','status':'not accessible via tool; no retry or alternative route'}],indent=2))
assert len(rs)==3 and len({r['url'] for r in rs})==3
print('3 additional contextual and deeper OCCRP investigation reads; zero local text/machine screens')
