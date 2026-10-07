import unittest,json
from foreign_discovery import enrich,P,S
class DiscoveryRegression(unittest.TestCase):
 def test_actual_us_steel_below_threshold_filing(self):
  rows=[r for f in S.glob('lda-annual-*.json') for r in json.loads(f.read_text())['results']]
  screen=json.loads((P/'client-screen.json').read_text());rr=json.loads((P/'rr-coverage.json').read_text());out=enrich(screen,rows,rr)
  steel=next(r for r in out if r['client_id']==165440)
  self.assertFalse(steel['initial_high_amount_foreign_entities_listed']);self.assertTrue(steel['any_acquired_2025_foreign_entities_listed'])
  self.assertEqual(steel['acquired_2025_foreign_entity_filing_uuids'],['f938042d-26f9-49cb-988d-fa6c42ec8924'])
  r=next(r for r in rows if r['filing_uuid']==steel['acquired_2025_foreign_entity_filing_uuids'][0]);self.assertEqual(r['expenses'],'360000.00');self.assertEqual(r['foreign_entities'][0]['ownership_percentage'],'100.00')
  original=(S/('original-'+r['filing_uuid']+'.html')).read_text();self.assertIn('NIPPON STEEL',original.upper())
 def test_deduplicates_rows_and_keeps_scope(self):
  s=[{'client_id':1,'country':'US','foreign_additions_present':False}];r={'filing_uuid':'x','client':{'id':1},'foreign_entities':[{'name':'Owner'}]}
  o=enrich(s,[r,r],[])[0];self.assertEqual(o['acquired_2025_foreign_entity_filing_uuids'],['x']);self.assertNotIn('foreign_additions_present',o)
 def test_rr_positive_selects_us_even_without_annual_addition(self):
  o=enrich([{'client_id':1,'country':'US'}],[],[{'client_id':1,'foreign_entities':[[{'name':'Owner'}]]}])[0]
  self.assertTrue(o['history_expansion_selected']);self.assertFalse(o['any_acquired_2025_foreign_entities_listed'])
 def test_foreign_domicile_not_selected_for_us_extension(self):
  o=enrich([{'client_id':1,'country':'JP'}],[],[{'client_id':1,'foreign_entities':[[{'name':'Owner'}]]}])[0];self.assertFalse(o['history_expansion_selected'])
 def test_empty_metadata_does_not_claim_no_owner(self):
  o=enrich([{'client_id':1,'country':'US'}],[],[])[0];self.assertFalse(o['history_expansion_selected']);self.assertIn('not an original-form No',o['foreign_field_interpretation'])
 def test_removal_parser_ignores_extended_blank_row_numbers(self):
  from ownership_timelines import extract_fields
  s=b'<p>28. Name of each previously reported foreign entity that no longer owns, or controls, or is affiliated</p><td>1</td><td>24</td><td>Former Parent Ltd.</td><h2>CONVICTIONS DISCLOSURE</h2>'
  self.assertEqual(extract_fields(s)['removed_foreign_entities'],['Former Parent Ltd.'])
 def test_image_pdf_not_treated_as_no(self):
  from ownership_timelines import extract_fields
  self.assertNotIn('registration_section14_response',extract_fields(b'%PDF-1.4'))
if __name__=='__main__':unittest.main()
