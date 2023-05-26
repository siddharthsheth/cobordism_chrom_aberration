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

    def test_cobordism_composition_valid(self):
        c = Cobordism(('W', 'I', 'P', 'C', 'T'))
        c.composition(Cobordism(('W', 'I', 'P', 'C', 'T')))
        self.assertEqual(c.steps, [('W', 'I', 'P', 'C', 'T'), ('W', 'I', 'P', 'C', 'T')])

    # def test_cobordism_composition_invalid(self):
    #     c = Cobordism(('W', 'I', 'P', 'C', 'T'))
    #     self.assertRaises(ValueError(), c.composition(Cobordism(('W', 'I', 'P', 'C', 'W'))))

    def test_complex_cobordism(self):
        steps = [('I', 'I', 'W', 'C'), ('P', 'P', 'P')]
        c = Cobordism(steps)
        self.assertEqual(c.steps, steps)

    def test_complex_cobordism_in_out_len(self):
        steps = [('I', 'I', 'W', 'C'), ('P', 'P', 'P')]
        c = Cobordism(steps)
        self.assertEqual(c.in_len, 5)
        self.assertEqual(c.out_len, 3)

    def test_generate_configs_simple(self):
        c = Cobordism(('W', 'I', 'P', 'C', 'T'))
        configs = c._generate_configs()
        # print([i.labels for i in configs[1]])
        self.assertEqual([i.labels for i in configs[0]], 
                         [('0','1'), ('2','3'), ('4','5'), ('6','7'), ('8','9'), ('10','11'), ('12','13')])
        self.assertEqual([i.labels for i in configs[1]], 
                         [('2','3'), ('0','1'), ('4','5'), ('6','7','8','9'), ('10','14'), ('15','11'), ('13','12')])
        
    def test_generate_configs_complex(self):
        steps = [('I', 'I', 'W', 'C'), ('P', 'P', 'P')]
        c = Cobordism(steps)
        configs = c._generate_configs()
        self.assertEqual([i.labels for i in configs[0]], 
                         [('0','1'), ('2','3'), ('4','5'), ('6','7'), ('8','9')])
        self.assertEqual([i.labels for i in configs[1]], 
                         [('0','1'), ('2','3'), ('6','7'), ('4','5'), ('8','10'), ('11','9')])
        self.assertEqual([i.labels for i in configs[2]], 
                         [('0','1','2','3'), ('6','7','4','5'), ('8','10','11','9')])
        
    def test_generate_in_out_map(self):
        steps = [('I', 'T', 'C', 'C', 'C'), ('P', 'P', 'P', 'P')]
        c = Cobordism(steps)
        c.generate_terminal_config_map()
        self.assertEqual([i.labels for i in c.in_config],
                         [('0','1'), ('2','3'), ('4','10','11','5'), ('6','12','13','7'), ('8','14','15','9')])