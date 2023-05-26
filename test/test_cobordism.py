import unittest
from cobordism_chrom_aberration.genericcobordism import Interval, elementary_forward_cobordisms, Cobordism

class TestCobordism(unittest.TestCase):
    def test_simple_cobordism(self):
        step = ('W', 'I', 'P', 'C', 'T')
        c = Cobordism(step)
        self.assertEqual(c.steps, [step])

    def test_simple_cobordism_in_out_len(self):
        c = Cobordism(('W', 'I', 'P', 'C', 'T'))
        self.assertEqual(c.in_len, 7)
        self.assertEqual(c.out_len, 7)

    def test_cobordism_composition(self):
        pass