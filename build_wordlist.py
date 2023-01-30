import pickle, re, os, json, string
from typing import List, Optional, Any, Dict
from utils import load_data, HashData, extract_strings_from_json

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
md5_pattern = re.compile(r"^[a-f0-9\-]{30,}")
remove_pattern = re.compile(r"d[ar]\d{3,}")
def extract_words(word: str) -> List[str]:
    # First, split on slashes. We'll never(?) have a word that spans a slash
    chunks = ''
    # split on symbols
    words = re.split(split_pattern, word)
    words = set([w for w in words if w != ''])

    result: List[str] = []
    for word in words:
        # remove md5-esque strings
        if re.match(md5_pattern, word):
            continue
        result.append(word)
        # Check if it's a compound word (currently only doing two letter words)
        compound = compound_words(word)
        if compound is not None:
            for w in compound:
                # Some simple filtering
                if re.match(remove_pattern, w):
                    continue
                result.append(w)
            
    return list(set(result))

# convert into assembly, _pro, pro, environment, templates, props, paintings, pictures, tamagozake, a, template, vodka, bottle, d, 00, entitytemplate, pc, entitytype, pc_entitytype
# words = extract_words('[assembly:/_pro/environment/templates/props/paintings/pictures_tamagozake_a.template?/vodka_bottle_d_00.entitytemplate].pc_entitytype')

# Takes all known names, and gets all of the folders
# Then we just spit them out
def build_folder_wordlist(data: Dict[str, HashData]):
    folder_pieces: set[str] = set()

    for hash in data:
        if data[hash]['correct_name']:
            parts = data[hash]['name'].split('.', 1)[0].split('/')
            for i in range(1, len(parts) - 1):
                folder_pieces.add(parts[i])

    ordered_words = sorted(list(folder_pieces))
    with open('hitman_folder_wordlist.txt', 'w') as fp:
        for word in ordered_words:
            # write each item on a new line
            fp.write(word.encode("ascii", errors="ignore").decode() + '\n')

if __name__ == '__main__':
    # Extract folders from known files
    data = load_data()

    words: set[str] = set()

    for hash in data:
        name = data[hash]['name']
        for x in extract_words(name):
            words.add(x)
        # this should be for only some hash lists
        # also we need to extract punctuation
        # also we need to remove super long strings
        # 
        # for now we can proxy this by just filtering
        # out some types. We really should extract from these though. Especially
        # DLGE and JSON
        # if data[hash]['type'] == 'JSON': # handle ORES, REPO
        #     for hex_string in data[hash]['hex_strings']:
        #         try:
        #             # There are comments inline, which will cause the parser to choke unless they're removed
        #             json_data = json.loads(re.sub(r'/\*.*?\*/', '', hex_string, flags=re.S))
        #             json_strings = [x.lower() for x in extract_strings_from_json(json_data)]
        #             json_strings = [x for x in json_strings if 'assembly:' in x]
        #             found = found.union(json_strings)
        #         except:
        #             found.add(f)
        potential_words: set[str] = set()
        if data[hash]['type'] in ['DLGE', 'RTLV']:
            for hex_string in data[hash]['hex_strings']:
                # Remove the spacing between the portions of dialogue
                hex_string = re.sub(r'\/\/\(.*?\)\\\\', ' ', hex_string)
                # Remove all punctuation
                hex_string = re.sub(r'[^\w\s]', '', hex_string)
                # Split on spaces
                for f in hex_string.split(' '):
                    if len(f) > 0:
                        potential_words.add(f.lower())
        elif data[hash]['type'] == 'WWES':
            for hex_string in data[hash]['hex_strings']:
                if hex_string.count('_') > 1:
                    for f in hex_string.split('_')[1:-1]:
                        potential_words.add(f.lower())
        elif data[hash]['type'] == 'LOCR':
            for hex_string in data[hash]['hex_strings']:
                # Remove the spacing between the portions of dialogue
                hex_string = re.sub(r'<\/?li>', ' ', hex_string)
                # Split on spaces
                for f in hex_string.split(' '):
                    if len(f) > 0:
                        potential_words.add(f.lower())
        # GFXF has real stuff but needs better extraction
        elif data[hash]['type'] not in ['JSON', 'BORG', 'CRMD', 'DLGE', 'REPO', 'MATE', 'GFXF', 'ORES']:
            for hex_string in data[hash]['hex_strings']:
                # We need to handle / and _ better for things that are clearly pathlike
                # and therefore have both of them
                if '/' in hex_string:
                    for x in hex_string.lower().split('/'):
                        if len(x) > 0:
                            potential_words.add(x)
                elif '\\' in hex_string:
                    for x in hex_string.lower().split('\\'):
                        if len(x) > 0:
                            potential_words.add(x)
                elif ' ' in hex_string:
                    for x in hex_string.lower().split(' '):
                        if len(x) > 0:
                            potential_words.add(x)
                elif '_' in hex_string:
                    for x in hex_string.lower().split('_'):
                        if len(x) > 0:
                            potential_words.add(x)
                elif '<' in hex_string:
                    continue # just fail out for now
                else:
                    # best effort, should use extract_word
                    potential_words.add(hex_string.lower())
        for w in potential_words:
            # run the _ splitting again
            if '_' in w:
                array_of_words = w.split('_')
            else:
                array_of_words = [w]
            for word in array_of_words:
                if not re.match(md5_pattern, word):
                    words.add(re.sub(r'[^\w\d_]', '', word))
    # For now, remove trailing digits. This will leave a lot of stuff on the table
    # but who cares.
    ordered_words = sorted(set([x.rstrip(string.digits) for x in words if len(x) > 0 and not x.isspace()]))
    with open('hitman_wordlist.txt', 'w') as fp:
        for word in ordered_words:
            # write each item on a new line
            fp.write(word.encode("ascii", errors="ignore").decode() + '\n')


