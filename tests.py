import unittest
from build_wordlist import extract_words, compound_words
from futzing import num_alts, replaceable_sections, replacements
from expand_known import find_alternate_paths
from utils import crack

class UtilsTest(unittest.TestCase):

    def test_find_alternate_paths(self):
        alts = find_alternate_paths('[assembly:/_pro/environment/geometry/props/lamps/table_lamp_b.wl2?/table_lamp_b.prim].pc_prim')
        self.assertEqual(sorted(list(alts.keys())), ['002FD1C467166E5E', '0030A0D22171B48E', '00358562D91EA649', '003ECCF5A8D38451', '0057B95F2B255C6D', '005FEB95C8C99832', '006303F1C897C52D', '008A3519919395F0', '00AC89D978CBF4DC', '00E3C72FE24E4993'])

    def test_compound_words(self):
        words = compound_words('sunrise')
        assert words is not None
        self.assertEqual(sorted(list(words)), ['rise', 'sun', 'sunrise'])

        words = compound_words('tequilasunrisesuit')
        assert words is not None
        self.assertEqual(sorted(list(words)), ['rise', 'suit', 'sun', 'sunrise', 'tequila'])

    # TODO: Fix this test, the wordlist script needs to be overhauled
    # def test_extract_words(self):
    #     words = extract_words('[assembly:/runtimeresources/vertexpaint/_pro/environment/templates/levels/fox/abandoned_building_fox_a/abandoned_building_kit_fox_inner_wall_9m_a_29_1a25694801db41bb9cb01474bbff9a3c.vertexdata].pc_vertexdata')
    #     self.assertEqual(sorted(words), ['29', '9m', 'a', 'abandoned', 'assembly', 'building', 'data', 'environment', 'fox', 'inner', 'kit', 'levels', 'paint', 'pc', 'pro', 'runtimeresources', 'templates', 'vertex', 'vertexdata', 'vertexpaint', 'wall'])

    #     words = extract_words('[assembly:/localization/hitman6/conversations/ui/pro/online/repository/outfits_npcs_paris.sweetmenutext?/outfits_paris_worker_fashionmodel_f_hpa912_description_dbad44de-8ff1-4ef8-8b74-596adf32b40e.sweetline].pc_sweetline')
    #     self.assertEqual(sorted(words), ['assembly', 'conversations', 'description', 'f', 'fashion', 'fashionmodel', 'fits', 'hitman6', 'hpa912', 'is', 'line', 'localization', 'model', 'npcs', 'on', 'online', 'out', 'outfits', 'par', 'paris', 'pc', 'pro', 'repository', 'sweet', 'sweetline', 'sweetmenutext', 'ui', 'worker'])

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

    def test_crack(self):
        # successful crack
        path = crack(
            '0053C4978B85C299',
            '[assembly:/localization/hitman6/conversations/ui/pro/online/',
            '.sweetmenutext].pc_localized-textlist',
            ['challenges', 'repository', 'unlocks', 's2', 'sc', 's3'],
            [],
            1,
            4
        )
        self.assertEqual(path, '[assembly:/localization/hitman6/conversations/ui/pro/online/repository/unlocks_sc.sweetmenutext].pc_localized-textlist')

        # unnsuccessful crack because hippo is not in it
        path = crack(
            '0053C4978B85C299',
            '[assembly:/localization/hitman6/conversations/ui/pro/online/',
            '.sweetmenutext].pc_localized-textlist',
            ['challenges', 'repository', 'unlocks', 's2', 'sc', 's3'],
            ['hippo'],
            1,
            4
        )
        self.assertEqual(path, None)

if __name__ == '__main__':
    unittest.main()