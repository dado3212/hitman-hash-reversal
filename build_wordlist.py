import pickle, re
from typing import List, Optional

# Load raw words
_end = '_end_'

def is_valid_word(word: str) -> bool:
    current_dict = trie
    for letter in word:
        if letter not in current_dict:
            return False
        current_dict = current_dict[letter]
    return _end in current_dict

with open('w12_trie.pickle', 'rb') as handle:
    trie = pickle.load(handle)

def compound_words(word: str) -> Optional[set[str]]:
    if len(word) < 4:
        if is_valid_word(word):
            return {word}
        else:
            return None
    total_words: set[str] = set()
    if is_valid_word(word):
        total_words.add(word)
    for i in range(1, len(word)-1):
        first_part = word[:i]
        if is_valid_word(first_part):
            compound = compound_words(word[i:])
            if compound is not None:
                total_words.add(first_part)
                total_words = total_words.union(compound)
    if len(total_words) == 0:
        return None
    else:
        return total_words


def extract_words(word: str) -> List[str]:
    # First, split on slashes. We'll never(?) have a word that spans a slash
    chunks = ''
    # split on symbols
    words = re.split(r"[\[\]\:\/\_\?\. \(\)]", word)
    words = [w for w in words if w != '']

    result: List[str] = []
    for word in words:
        if re.match(r"^[a-f0-9\-]{30,}", word):
            continue
        result.append(word)
        # Check if it's a compound word (currently only doing two letter words)
        for i in range(1, len(word)):
            first = word[:i]
            second = word[i:]
            if len(first) > 1 and len(second) > 1 and is_valid_word(first) and is_valid_word(second):
                result.append(first)
                result.append(second)
            
    return list(set(result))

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


