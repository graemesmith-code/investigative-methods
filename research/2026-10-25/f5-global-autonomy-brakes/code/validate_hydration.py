#!/usr/bin/env python3
"""Recompute counts/sums from cached source bodies, independently of hydrator."""
import argparse,hashlib,json,pathlib,xml.etree.ElementTree as E
from decimal import Decimal
A='{http://www.w3.org/2005/Atom}';F='{https://www.fpds.gov/FPDS}'
def main():
 p=argparse.ArgumentParser();p.add_argument('--data',required=True,type=pathlib.Path);a=p.parse_args();records=json.loads((a.data/'safety-board-contracts-hydrated.json').read_text())['records'];cache=a.data/'financial-raw';issues=[];checked=set();summary=[]
 def source(receipt):
  h=receipt.get('sha256')
  if not h:return None
  b=(cache/(h+'.raw')).read_bytes();assert hashlib.sha256(b).hexdigest()==h;checked.add(h);return b
 for r in records:
  source(r.get('award_receipt',{}));tx={};feed={};ident=r['identity']
  for receipt in r['usaspending_transactions'].get('pages',[]):
   b=source(receipt)
   if b:
    for x in json.loads(b)['results']:tx[x['id']]=Decimal(str(x['federal_action_obligation']))
  for receipt in r['fpds'].get('pages',[]):
   b=source(receipt)
   if b:
    for ent in E.fromstring(b).findall(A+'entry'):
     content=ent.find(A+'content');x=list(content)[0] if content is not None and len(content) else None
     if x is None:continue
     schema=x.tag.split('}')[-1]
     if schema!=ident['schema']:continue
     def txt(path):return x.findtext('/'.join(F+y for y in path.split('/')),'')
     identpath='awardID/awardContractID' if schema=='award' else schema+'ID/'+schema+'ContractID';detail='' if schema=='award' else 'contractDetail/'
     vals=[txt(identpath+'/'+y) for y in ['PIID','agencyID','modNumber','transactionNumber']];parent=txt('awardID/referencedIDVID/PIID') if schema=='award' else '';pa=txt('awardID/referencedIDVID/agencyID') if schema=='award' else ''
     if vals[0]!=ident['piid'] or vals[1]!=ident['agency_id'] or parent!=ident['parent_piid'] or pa!=ident['parent_agency_id']:continue
     feed[tuple(vals+[parent,pa])]=Decimal(txt(detail+'dollarValues/obligatedAmount'))
  for label,actual,reported in [('USAspending',tx,r['usaspending_transactions']),('FPDS',feed,r['fpds'])]:
   if reported.get('not_applicable'):continue
   if len(actual)!=reported['action_count'] or sum(actual.values(),Decimal(0))!=Decimal(reported['action_sum_usd']):issues.append({'award_key':r['award_key'],'source':label,'count':len(actual),'sum':str(sum(actual.values(),Decimal(0)))})
  summary.append({'award_key':r['award_key'],'usa_count':len(tx),'fpds_count':len(feed),'negative_fpds':sum(v<0 for v in feed.values())})
 result={'status':'PASS' if not issues else 'FAIL','independent_cached_source_validation':True,'records':len(records),'unique_raw_source_bodies_sha256_checked':len(checked),'total_usa_actions':sum(x['usa_count'] for x in summary),'total_fpds_actions':sum(x['fpds_count'] for x in summary),'negative_fpds_actions':sum(x['negative_fpds'] for x in summary),'issues':issues,'details':summary,'scope':'Independent re-read/reparse of primary raw JSON/XML receipts; checks counts/sums/hashes; not operational effectiveness or independent agency-data provenance.'};(a.data/'hydration-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='details'}))
 if issues:raise SystemExit(1)
if __name__=='__main__':main()
