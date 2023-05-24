import unittest
from cobordism_chrom_aberration.segment import ChromSegment, Label, Chromatin

class TestChromSegment(unittest.TestCase):
    def test_valid_segment(self):
        a = Label('a', True)
        b = Label('b', True)
        c = Label('c', False)
        d = Label('d', False)
        
        segment = ChromSegment([Chromatin(a,c,'red',False), Chromatin(d,b,'blue',True)])
        self.assertEqual(segment.is_valid_terminal_segment(), True)

    def test_invalid_segment_telomere_end(self):
        a = Label('a', True)
        b = Label('b', True)
        c = Label('c', False)
        d = Label('d', True)

        segment = ChromSegment([Chromatin(a,b,'red',False), Chromatin(c,d,'blue',False)])
        self.assertEqual(segment.is_valid_terminal_segment(), False)

    def test_invalid_segment_telomere_start(self):
        a = Label('a', True)
        b = Label('b', False)
        c = Label('c', True)
        d = Label('d', True)

        segment = ChromSegment([Chromatin(a,b,'red',False), Chromatin(c,d,'blue',False)])
        self.assertEqual(segment.is_valid_terminal_segment(), False)

    # def test_invalid_segment_centromere(self):
    #     a = Label('a', True)
    #     b = Label('b', True)
    #     c = Label('c', False)
    #     d = Label('d', False)

    #     segment = ChromSegment([Chromatin(a,c,'red',True), Chromatin(d,b,'red',True)])
    #     self.assertEqual(segment.is_valid_terminal_segment(), False)

    def test_invalid_segment_no_telomere_start(self):
        a = Label('a', False)
        b = Label('b', False)
        c = Label('c', False)
        d = Label('d', True)

        segment = ChromSegment([Chromatin(a,b,'red',True), Chromatin(c,d,'blue',True)])
        self.assertEqual(segment.is_valid_terminal_segment(), False)

    def test_invalid_segment_no_telomere_end(self):
        a = Label('a', True)
        b = Label('b', False)
        c = Label('c', False)
        d = Label('d', False)

        segment = ChromSegment([Chromatin(a,b,'red',True), Chromatin(c,d,'blue',True)])
        self.assertEqual(segment.is_valid_terminal_segment(), False)