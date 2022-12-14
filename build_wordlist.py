import pickle, re, os
from typing import List, Optional, Any, Dict

# Load raw words
_end = '_end_'

def build_trie(words: List[str]):
    trie: Dict[str, Any] = dict()
    for word in words:
        current_dict = trie
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return trie

def is_valid_word(word: str) -> bool:
    current_dict = trie
    for letter in word:
        if letter not in current_dict:
            return False
        current_dict = current_dict[letter]
    return _end in current_dict

# Need to fix this, it takes literally forever because my compound_word calculation is ass
if os.path.exists('hitman_wordlist.txt') and False:
    with open('wordlist_12.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]

    with open('hitman_wordlist.txt', 'r') as f:
        words_two = [x.strip() for x in f.readlines()]

    combined_words = list(set(words).union(set(words_two)))
    trie = build_trie(combined_words)
else:
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

split_pattern = re.compile(r"[\[\]\:\/\_\?\. \(\)]")
def extract_words(word: str) -> List[str]:
    # First, split on slashes. We'll never(?) have a word that spans a slash
    chunks = ''
    # split on symbols
    words = re.split(split_pattern, word)
    words = [w for w in words if w != '']

    result: List[str] = []
    for word in words:
        if re.match(r"^[a-f0-9\-]{30,}", word):
            continue
        result.append(word)
        # Check if it's a compound word (currently only doing two letter words)
        compound = compound_words(word)
        if compound is not None:
            for w in compound:
                result.append(w)
            
    return list(set(result))

# convert into assembly, _pro, pro, environment, templates, props, paintings, pictures, tamagozake, a, template, vodka, bottle, d, 00, entitytemplate, pc, entitytype, pc_entitytype
# words = extract_words('[assembly:/_pro/environment/templates/props/paintings/pictures_tamagozake_a.template?/vodka_bottle_d_00.entitytemplate].pc_entitytype')

if __name__ == '__main__':
    with open('hashes.pickle', 'rb') as handle:
        data = pickle.load(handle)

    words: set[str] = set()

    for hash in data:
        name = data[hash]['name']
        for x in extract_words(name):
            words.add(x)
        # this should be for only some hash lists
        # also we need to extract punctuation
        # also we need to remove super long strings
        # for string in data[hash]['hex_strings']:
        #     for x in extract_words(string.lower()):
        #         words.add(x)
            
    ordered_words = sorted(list(words))
    with open('hitman_wordlist.txt', 'w') as fp:
        for word in ordered_words:
            # write each item on a new line
            fp.write(word.encode("ascii", errors="ignore").decode() + '\n')


