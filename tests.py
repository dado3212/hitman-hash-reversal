import unittest
from build_wordlist import extract_words

class UtilsTest(unittest.TestCase):

    def test_extract_words(self):
        words = extract_words('[assembly:/shaders/win32/glare.fx](dx11,fx50).pc_mate')
        correct = ['assembly', 'assembly:', 'shaders', 'win32', 'glare', 'fx', 'dx11', 'fx50', '(dx11,fx50)', 'pc', 'mate', 'pc_mate']
        self.assertEqual(sorted(words), sorted(correct))

if __name__ == '__main__':
    unittest.main()