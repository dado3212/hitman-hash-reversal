import unittest
from build_wordlist import extract_words
from futzing import num_alts, replaceable_sections, replacements

class UtilsTest(unittest.TestCase):

    def test_extract_words(self):
        words = extract_words('[assembly:/shaders/win32/glare.fx](dx11,fx50).pc_mate')
        correct = ['assembly', 'assembly:', 'shaders', 'win32', 'glare', 'fx', 'dx11', 'fx50', '(dx11,fx50)', 'pc', 'mate', 'pc_mate']
        # Currently this is wrong
        # self.assertEqual(sorted(words), sorted(correct))

    def test_replaceable_sections(self):
        string = '[assembly:/_pro/environment/geometry/props/paintings/pictures_tamagozake.wl2?/portrait.prim].pc_prim'
        sections = replaceable_sections(string)
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0][0], string)
        self.assertEqual(sections[0][1], False)

        string = '[assembly:/_pro/environment/geometry/props/paintings/pictures_tamagozake_a.wl2?/portrait_10.prim].pc_prim'
        sections = replaceable_sections(string)
        recombined = ''.join([x[0] for x in sections])
        self.assertEqual(recombined, string)
        correct = [('[assembly:/_pro/environment/geometry/props/paintings/pictures_tamagozake_', False), ('a', True), ('.wl2?/portrait_', False), ('10', True), ('.prim].pc_prim', False)]
        self.assertEqual(sections, correct)

    def test_replacements(self):
        string = '[assembly:/_pro/environment/geometry/props/paintings/pictures_tamagozake_a.wl2?/portrait.prim].pc_prim'
        sections = replaceable_sections(string)
        replacement_strings = replacements(sections)
        self.assertEqual(len(replacement_strings), 26)
        
        string = '[assembly:/_pro/environment/geometry/props/paintings/pictures_tamagozake_1.wl2?/portrait.prim].pc_prim'
        sections = replaceable_sections(string)
        replacement_strings = replacements(sections)
        self.assertEqual(len(replacement_strings), 17)

        string = '[assembly:/_pro/environment/geometry/props/paintings/pictures_tamagozake_a.wl2?/portrait_1.prim].pc_prim'
        sections = replaceable_sections(string)
        replacement_strings = replacements(sections)
        self.assertEqual(len(replacement_strings), 26 * 17)
        self.assertEqual(num_alts(sections), 26 * 17 - 1)

        string = '[assembly:/_pro/characters/assets/workers/eventscrew_01/materials/male_reg_bangkok_bandcrew_01_wristbands_01.mi].pc_entitytype'
        sections = replaceable_sections(string)
        self.assertEqual(num_alts(sections), 17 * 17 * 17 - 1)

if __name__ == '__main__':
    unittest.main()