"""Regression checks on actual export defects and source-preserving locators."""
import unittest,json
from ingest import P,read,date
class IngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw,cls.cols,cls.rows,cls.repairs,cls.flags=read('ForeignPrincipals')
    def test_every_record_retained(self):self.assertEqual(len(self.rows),17765);self.assertEqual(len(self.repairs),15)
    def test_quote_repair_does_not_shift_ids(self):
        row=self.rows[677];self.assertEqual(row['Registration Number'],'7383');self.assertEqual(row['Foreign Principal Registration Date'],'03/25/2024');self.assertEqual(row['Country/Location Represented'],'UKRAINE')
    def test_c1_chars_do_not_shift_physical_lines(self):
        lines=self.raw.decode('iso-8859-1').split('\n')
        for repair in self.repairs:
            start,end=repair['physical_lines'];actual='\n'.join(lines[start-1:end]).rstrip('\r\n');self.assertEqual(actual,repair['raw'])
    def test_original_embedded_newlines_retained(self):self.assertTrue(any('\n' in r['Registrant Name'] for r in self.rows))
    def test_snapshot_status_not_deduplicated(self):
        self.assertEqual(sum(not r['Foreign Principal Termination Date'] for r in self.rows),822)
    def test_implausible_year_not_silently_corrected(self):self.assertEqual(date('11/16/0200'),'0200-11-16')
if __name__=='__main__':unittest.main()
