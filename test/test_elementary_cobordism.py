import unittest
from cobordism_chrom_aberration.genericcobordism import Interval, elementary_forward_cobordisms, elementary_reverse_cobordisms

class TestElementaryCobordism(unittest.TestCase):
    def test_interval(self):
        i = Interval(['a','b'])
        self.assertEqual(i.next_interval, None)
        self.assertEqual(i.prev_interval, None)
        self.assertEqual(i.labels, ('a','b'))

    def test_identity(self):
        i = Interval(['a','b'])
        new_i, = elementary_forward_cobordisms['I'](i)
        self.assertEqual(new_i.labels, i.labels)
        self.assertEqual(new_i.prev_interval, i)
        self.assertEqual(i.next_interval, new_i)

    def test_twist(self):
        i = Interval(['a','b'])
        new_i, = elementary_forward_cobordisms['T'](i)
        self.assertEqual(new_i.labels, ('b','a'))
        self.assertEqual(new_i.prev_interval, i)
        self.assertEqual(i.next_interval, new_i)

    def test_braid(self):
        i_1 = Interval(['a','b'])
        i_2 = Interval(['c','d'])
        new_i_1, new_i_2 = elementary_forward_cobordisms['W'](i_1, i_2)
        self.assertEqual(new_i_1.labels, ('c','d'))
        self.assertEqual(new_i_1.prev_interval, i_2)
        self.assertEqual(i_2.next_interval, new_i_1)
        self.assertEqual(new_i_2.labels, ('a','b'))
        self.assertEqual(new_i_2.prev_interval, i_1)
        self.assertEqual(i_1.next_interval, new_i_2)
    
    def test_copants(self):
        i = Interval(['a','b'])
        new_left, new_right = elementary_forward_cobordisms['C'](i, 'c', 'd')
        self.assertEqual(new_left.labels, ('a','c'))
        self.assertEqual(new_left.prev_interval, i)
        self.assertEqual(i.next_interval['left'], new_left)
        self.assertEqual(new_right.labels, ('d','b'))
        self.assertEqual(new_right.prev_interval, i)
        self.assertEqual(i.next_interval['right'], new_right)
    
    def test_pants(self):
        i_1 = Interval(['a','b'])
        i_2 = Interval(['c','d'])
        new_i, = elementary_forward_cobordisms['P'](i_1, i_2)
        self.assertEqual(new_i.labels, ('a','b','c','d'))
        self.assertEqual(i_1.next_interval, new_i)
        self.assertEqual(i_2.next_interval, new_i)
        self.assertEqual(new_i.prev_interval, {'left':i_1, 'right':i_2})

    def test_identity_reverse(self):
        i = Interval(['a','b'])
        new_i, = elementary_reverse_cobordisms['I'](i)
        self.assertEqual(new_i.labels, i.labels)
        self.assertEqual(new_i.prev_interval, i)
        self.assertEqual(i.next_interval, new_i)

    def test_twist_reverse(self):
        i = Interval(['a','b'])
        new_i, = elementary_reverse_cobordisms['T'](i)
        self.assertEqual(new_i.labels, ('b','a'))
        self.assertEqual(new_i.prev_interval, i)
        self.assertEqual(i.next_interval, new_i)

    def test_braid_reverse(self):
        i_1 = Interval(['a','b'])
        i_2 = Interval(['c','d'])
        new_i_1, new_i_2 = elementary_reverse_cobordisms['W'](i_1, i_2)
        self.assertEqual(new_i_1.labels, ('c','d'))
        self.assertEqual(new_i_1.prev_interval, i_2)
        self.assertEqual(i_2.next_interval, new_i_1)
        self.assertEqual(new_i_2.labels, ('a','b'))
        self.assertEqual(new_i_2.prev_interval, i_1)
        self.assertEqual(i_1.next_interval, new_i_2)

    def test_copants_reverse(self):
        i_1 = Interval(['a','b'])
        i_2 = Interval(['c','d'])
        new_i, = elementary_reverse_cobordisms['C'](i_1, i_2)
        self.assertEqual(new_i.labels, ('a','b','c','d'))
        self.assertEqual(i_1.next_interval, new_i)
        self.assertEqual(i_2.next_interval, new_i)
        self.assertEqual(new_i.prev_interval, {'left':i_1, 'right':i_2})

    def test_pants_reverse(self):
        i = Interval(['a','b'])
        new_left, new_right = elementary_reverse_cobordisms['P'](i, 'c', 'd')
        self.assertEqual(new_left.labels, ('a','c'))
        self.assertEqual(new_left.prev_interval, i)
        self.assertEqual(i.next_interval['left'], new_left)
        self.assertEqual(new_right.labels, ('d','b'))
        self.assertEqual(new_right.prev_interval, i)
        self.assertEqual(i.next_interval['right'], new_right)

    def test_double_braid(self):
        i_1 = Interval(['a','b'])
        i_2 = Interval(['c','d'])
        new_i_1, new_i_2 = elementary_forward_cobordisms['W'](i_1, i_2)
        final_1, final_2 = elementary_forward_cobordisms['W'](new_i_1, new_i_2)
        self.assertEqual(i_1.labels, final_1.labels)
        self.assertEqual(i_2.labels, final_2.labels)

    def test_double_twist(self):
        i = Interval(['a','b'])
        new_i, = elementary_forward_cobordisms['T'](i)
        final_i, =elementary_forward_cobordisms['T'](new_i)
        self.assertEqual(i.labels, final_i.labels)