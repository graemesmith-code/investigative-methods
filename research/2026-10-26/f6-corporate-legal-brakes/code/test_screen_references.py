"""Adversarial recall, provenance and incomplete-coverage regression tests."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from screen_references import run, load_jsonl

class ScreeningTests(unittest.TestCase):
    def screen(self, sources, reviews=None):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root=Path(tmp.name); inp=root/'sources.jsonl'
        inp.write_text(''.join(json.dumps(s)+'\n' for s in sources))
        rev=root/'reviews.jsonl'
        rev.write_text(''.join(json.dumps(r)+'\n' for r in reviews or []))
        result=run(inp,root/'out',rev)
        return result,root/'out'

    def test_no_weapon_keyword_required_and_every_repeat_retained(self):
        s={'document_id':'D1','segments':[{'page':7,'clause':'2','text':
             'Applicable law. Applicable law. Human dignity. IHL. Article 36. proportionality.'}],
           'public_quote_word_budget':4}
        result,out=self.screen([s]); hits=load_jsonl(out/'occurrences.jsonl')
        self.assertEqual(result['occurrences'],6)
        self.assertEqual(sum(h['signal_id']=='generic_no_established_ihl_link:0' for h in hits),2)
        self.assertLessEqual(sum(len(h['short_original_extract'].split()) for h in hits),4)
        self.assertTrue(all(h['page']==7 for h in hits))

    def test_false_positive_negation_and_unicode_offsets(self):
        text='é漢字 A distinction between prices. No IHL restriction is promised.'
        s={'document_id':'D2','segments':[{'page':1,'text':text}]}
        _,out=self.screen([s]);hits=load_jsonl(out/'occurrences.jsonl')
        direct=next(h for h in hits if h['screen_class']=='explicit_ihl_reference')
        self.assertEqual(text.encode()[direct['utf8_byte_start']:direct['utf8_byte_end']],b'IHL')
        review={'document_id':'D2','text_sha256':hashlib.sha256(text.encode()).hexdigest(),
           'kind':'adjudication','occurrence_id':next(h['occurrence_id'] for h in hits if h['screen_class']=='substantive_concept_unlabelled'),
           'classification':'rejected_false_positive','confidence':'high','reviewer':'test',
           'rationale':'Price comparison, not war-law distinction.','negation_exception_status':'not_applicable'}
        _,out=self.screen([s],[review])
        self.assertEqual(sum(h['reviewed_class']=='rejected_false_positive' for h in load_jsonl(out/'occurrences.jsonl')),1)

    def test_no_absence_claim_for_ocr_or_missing_sections(self):
        _,out=self.screen([{'document_id':'D3','segments':[{'page':1,'text':'Unrelated.'}],
             'expected_pages':2,'full_accessible_text_verified':True,'image_text_status':'unknown'}])
        self.assertFalse(load_jsonl(out/'coverage.jsonl')[0]['no_reference_claim_allowed'])
        self.assertEqual(len(load_jsonl(out/'access_failures.jsonl')),1)

    def test_semantic_miss_retained_without_lexicon_hit(self):
        text='An officer must approve any change in the proposed mission.'
        source={'document_id':'D4','segments':[{'page':1,'text':text}],
               'full_accessible_text_verified':True,'image_text_status':'not_applicable'}
        review={'document_id':'D4','text_sha256':hashlib.sha256(text.encode()).hexdigest(),
          'kind':'semantic_addition','char_start':0,'char_end':len(text),
          'classification':'plausible_indirect_connection','confidence':'low',
          'reviewer':'test','rationale':'Possible mission-change gate; applicability unresolved.'}
        result,out=self.screen([source],[review])
        self.assertEqual(result['occurrences'],1)
        self.assertEqual(load_jsonl(out/'occurrences.jsonl')[0]['review_status'],'reviewed')

    def test_duplicate_versions_and_stale_reviews_fail_closed(self):
        source={'document_id':'D5','segments':[{'page':1,'text':'lawful use'}]}
        with self.assertRaises(ValueError): self.screen([source,source])
        with self.assertRaises(ValueError): self.screen([source],[{'document_id':'D5','text_sha256':'stale'}])

    def test_layout_linebreaks_and_empty_extraction(self):
        s={'document_id':'D6','segments':[{'page':1,'text':'international   humanitarian\nlaw and human-in-the-loop'}]}
        result,out=self.screen([s])
        self.assertEqual(result['occurrences'],2)
        s={'document_id':'D7','segments':[{'page':1,'text':''}],
           'full_accessible_text_verified':True,'image_text_status':'not_applicable'}
        _,out=self.screen([s])
        self.assertFalse(load_jsonl(out/'coverage.jsonl')[0]['extraction_complete'])

    def test_humanitarian_variant_and_substring_false_positive(self):
        s={'document_id':'D8','segments':[{'page':1,'text':'global humanitarian law. Determination. any lawful uses.'}]}
        result,out=self.screen([s]); hits=load_jsonl(out/'occurrences.jsonl')
        self.assertEqual(result['occurrences'],2)
        self.assertTrue(any(h['screen_class']=='explicit_ihl_reference' for h in hits))

if __name__=='__main__': unittest.main()
