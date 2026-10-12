"""Guard against invalid comparison inputs, rather than trusting saved decisions."""
import copy
import unittest
from decimal import InvalidOperation
from replay_language_controls import replay


class FollowupGuards(unittest.TestCase):
    def setUp(self):
        self.row = {'control_id': 'example', 'entity': 'one mine', 'year': 2023,
                    'metal': 'Au', 'english': {'value': '3418', 'unit': 'oz'},
                    'spanish': {'value': '3.4', 'unit': 'koz'},
                    'difference_spanish_minus_english': '-18',
                    'display_precision_allowance': '101',
                    'within_precision': True, 'governments_pair': False}

    def test_cross_metal_mass_units_rejected(self):
        row = copy.deepcopy(self.row)
        row['spanish']['unit'] = 't'
        with self.assertRaises(ValueError):
            replay([row])

    def test_duplicate_checks_cannot_inflate_denominator(self):
        with self.assertRaises(ValueError):
            replay([self.row, copy.deepcopy(self.row)])

    def test_dash_cannot_become_zero(self):
        row = copy.deepcopy(self.row)
        row['spanish']['value'] = '-'
        with self.assertRaises(InvalidOperation):
            replay([row])

    def test_claimed_agreement_rejected_outside_display_allowance(self):
        row = copy.deepcopy(self.row)
        row['spanish']['value'] = '3.0'
        row['difference_spanish_minus_english'] = '-418'
        with self.assertRaises(ValueError):
            replay([row])


if __name__ == '__main__':
    unittest.main()
