import unittest
from cobordism_chrom_aberration.segment import ChromSegment, Label, Chromatin
from cobordism_chrom_aberration.configuration import ChromConfiguration

class TestChromConfiguration(unittest.TestCase):
    def test_valid_configuration(self):
        ab = Chromatin(Label('a', True), Label('b', False), 'red', True)
        cd = Chromatin(Label('c', False), Label('d', True), 'red', False)

        ef = Chromatin(Label('e', True), Label('f', False), 'blue', True)
        gh = Chromatin(Label('g', False), Label('h', True), 'blue', False)

        abcd = ChromSegment([ab,cd])
        efgh = ChromSegment([ef,gh])
        configuration = ChromConfiguration([abcd, efgh])

        self.assertEqual(configuration.is_valid_terminal_configuration(), True)

    def test_invalid_configuration_extra_telomeres(self):
        ab = Chromatin(Label('a', True), Label('b', False), 'red', True)
        cd = Chromatin(Label('c', True), Label('d', False), 'red', False)
        ef = Chromatin(Label('e', True), Label('f', False), 'red', False)

        gh = Chromatin(Label('g', False), Label('h', True), 'blue', True)
        ij = Chromatin(Label('i', False), Label('j', True), 'blue', False)
        kl = Chromatin(Label('k', False), Label('l', True), 'blue', False)

        abgh = ChromSegment([ab,gh])
        cdij = ChromSegment([cd, ij])
        efkl = ChromSegment([ef,kl])

        configuration = ChromConfiguration([abgh, cdij, efkl])
        self.assertEqual(configuration.is_valid_terminal_configuration(), False)

    def test_invalid_configuration_missing_telomeres(self):
        ab = Chromatin(Label('a', False), Label('b', False), 'red', True)
        cd = Chromatin(Label('c', False), Label('d', False), 'red', False)
 
        ef = Chromatin(Label('e', True), Label('f', False), 'blue', False)
        gh = Chromatin(Label('g', False), Label('h', True), 'blue', True)

        ij = Chromatin(Label('i', True), Label('j', False), 'green', True)
        kl = Chromatin(Label('k', False), Label('l', True), 'green', False)

        ijcdgh = ChromSegment([ij,cd,gh])
        efabkl = ChromSegment([ef,ab,kl])

        configuration = ChromConfiguration([ijcdgh, efabkl])
        self.assertEqual(configuration.is_valid_terminal_configuration(), False)

    def test_invalid_configuration_extra_centromeres(self):
        ab = Chromatin(Label('a', True), Label('b', False), 'red', True)
        # cd = Chromatin(Label('c', False), Label('d', False), 'red', False)
        ef = Chromatin(Label('e', True), Label('f', False), 'red', True)

        gh = Chromatin(Label('g', False), Label('h', True), 'blue', True)
        # ij = Chromatin(Label('i', False), Label('j', False), 'blue', False)
        kl = Chromatin(Label('k', False), Label('l', True), 'blue', False)

        abgh = ChromSegment([ab,gh])
        # cdij = ChromSegment([cd, ij])
        efkl = ChromSegment([ef,kl])

        configuration = ChromConfiguration([abgh, efkl])
        self.assertEqual(configuration.is_valid_terminal_configuration(), False)

    def test_invalid_configuration_missing_centromeres(self):
        ab = Chromatin(Label('a', True), Label('b', False), 'red', False)
        ef = Chromatin(Label('e', True), Label('f', False), 'red', False)

        gh = Chromatin(Label('g', False), Label('h', True), 'blue', True)
        kl = Chromatin(Label('k', False), Label('l', True), 'blue', False)

        abgh = ChromSegment([ab,gh])
        efkl = ChromSegment([ef,kl])

        configuration = ChromConfiguration([abgh, efkl])
        self.assertEqual(configuration.is_valid_terminal_configuration(), False)

    def test_configuration_from_file(self):
        pass
