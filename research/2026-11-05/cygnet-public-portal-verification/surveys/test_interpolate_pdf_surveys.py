import unittest
from interpolate_pdf_surveys import interpolate

class InterpolationTests(unittest.TestCase):
    def setUp(self):
        self.rows={100:{'values':(90,90,50,10,20,0),'pages':[1]},200:{'values':(90,90,70,30,60,0),'pages':[2]}}
    def test_midpoint(self):
        v=interpolate(self.rows,150)
        self.assertEqual((v['tvd_m'],v['north_offset_m'],v['east_offset_m']),(60,20,40))
    def test_exact_point(self):
        self.assertEqual(interpolate(self.rows,100)['survey_lower_md_m'],100)
        self.assertEqual(interpolate(self.rows,200)['east_offset_m'],60)
    def test_no_extrapolation(self):
        for md in [99,201]:
            with self.assertRaises(ValueError):interpolate(self.rows,md)
if __name__=='__main__':unittest.main()
