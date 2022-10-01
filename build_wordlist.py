import pickle, re
from typing import List

def extract_words(word: str) -> List[str]:
    # First, split on slashes. We'll never(?) have a word that spans a slash
    chunks = ''
    # split on symbols
    words = re.split(r"[\[\]\:\/\_\?\. \(\)]", word)
    return list(set([w for w in words if w != '']))

# convert into assembly, _pro, pro, environment, templates, props, paintings, pictures, tamagozake, a, template, vodka, bottle, d, 00, entitytemplate, pc, entitytype, pc_entitytype
# words = extract_words('[assembly:/_pro/environment/templates/props/paintings/pictures_tamagozake_a.template?/vodka_bottle_d_00.entitytemplate].pc_entitytype')

if __name__ == '__main__':
    with open('hashes.pickle', 'rb') as handle:
        data = pickle.load(handle)

    words: List[str] = []

    for hash in data:
        name = data[hash]['name']
        for x in extract_words(name):
            words.append(x)
        
    words = sorted(list(set(words)))
    with open('hitman_wordlist.txt', 'w') as fp:
        for word in words:
            # write each item on a new line
            fp.write(word + '\n')


