#!/usr/bin/env python3
"""Small identity/pagination/accounting regressions; never makes network calls."""
import hashlib,json,unittest
import hydrate_full_award_lifecycle as h
def award(parent,amount,mod='0',agency='9700'):
 return '<award xmlns="https://www.fpds.gov/FPDS"><awardID><awardContractID><PIID>TASK</PIID><agencyID>'+agency+'</agencyID><modNumber>'+mod+'</modNumber><transactionNumber>0</transactionNumber></awardContractID><referencedIDVID><PIID>'+parent+'</PIID><agencyID>9700</agencyID></referencedIDVID></awardID><relevantContractDates><signedDate>2017-01-01</signedDate></relevantContractDates><dollarValues><obligatedAmount>'+amount+'</obligatedAmount></dollarValues></award>'
def feed(payloads,nexturl=''):
 return ('<feed xmlns="http://www.w3.org/2005/Atom">'+(''.join('<entry><content>'+p+'</content></entry>' for p in payloads))+('<link rel="next" href="'+nexturl+'"/>' if nexturl else '')+'</feed>').encode()
class Fake:
 def __init__(self,bodies):self.bodies=iter(bodies);self.calls=[]
 def fetch(self,url,body=None):
  self.calls.append((url,body));raw=next(self.bodies);return raw,{'sha256':hashlib.sha256(raw).hexdigest(),'retrieved_utc':'test'}
class Regression(unittest.TestCase):
 def test_exact_parent_and_agency_and_negatives(self):
  f=Fake([feed([award('RIGHT','100'),award('WRONG','999'),award('RIGHT','999',agency='1234')],'https://example.invalid/page2'),feed([award('RIGHT','-25','P00001')])]);r=h.fpds(f,h.identity('CONT_AWD_TASK_9700_RIGHT_9700'))
  self.assertEqual(r['action_count'],2);self.assertEqual(r['action_sum_usd'],'75');self.assertTrue(r['pagination_complete']);self.assertEqual(len(r['excluded_identities']),2);self.assertEqual(r['actions'][0]['signed_date'],'2017-01-01');self.assertEqual(len(f.calls),2)
 def test_transaction_pagination_and_no_filters(self):
  f=Fake([json.dumps({'results':[{'id':1,'federal_action_obligation':'100','action_date':'2017-01-01'}],'page_metadata':{'hasNext':True}}).encode(),json.dumps({'results':[{'id':2,'federal_action_obligation':'-25','action_date':'2026-01-01'}],'page_metadata':{'hasNext':False}}).encode()]);r=h.transactions(f,'EXACT_KEY')
  self.assertEqual(r['action_sum_usd'],'75');self.assertTrue(r['pagination_complete']);self.assertEqual(f.calls[0][1],{'award_id':'EXACT_KEY','page':1,'limit':100});self.assertEqual(f.calls[1][1]['page'],2)
 def test_missing_metadata_not_exhaustion(self):
  f=Fake([b'{"results":[]}']);r=h.transactions(f,'EXACT');self.assertFalse(r['pagination_complete'])
 def test_native_ot_identity_and_schema_separation(self):
  payload='<OtherTransactionIDV xmlns="https://www.fpds.gov/FPDS"><OtherTransactionIDVID><OtherTransactionIDVContractID><PIID>AGREEMENT</PIID><agencyID>9700</agencyID><modNumber>0</modNumber><transactionNumber>0</transactionNumber></OtherTransactionIDVContractID></OtherTransactionIDVID><contractDetail><dollarValues><obligatedAmount>25</obligatedAmount></dollarValues></contractDetail></OtherTransactionIDV>'
  r=h.fpds(Fake([feed([payload])]),h.identity('FPDS_OTHER_TRANSACTION_IDV:9700:AGREEMENT'));self.assertEqual(r['action_count'],1);self.assertEqual(r['action_sum_usd'],'25');self.assertEqual(r['actions'][0]['schema'],'OtherTransactionIDV')
  wrong=h.fpds(Fake([feed([payload])]),h.identity('CONT_IDV_AGREEMENT_9700'));self.assertEqual(wrong['action_count'],0);self.assertEqual(len(wrong['excluded_identities']),1)
  aw=payload.replace('OtherTransactionIDV','OtherTransactionAward');rr=h.fpds(Fake([feed([aw])]),h.identity('FPDS_OTHER_TRANSACTION_AWARD:9700:AGREEMENT'));self.assertEqual(rr['action_count'],1);self.assertEqual(rr['actions'][0]['schema'],'OtherTransactionAward')
if __name__=='__main__':unittest.main()
