import re, pickle
from typing import Optional, List, Dict, Any
from utils import ioi_string_to_hex

# Find solvable hashes
# What is a solvable hash?
#  it has no name
#  reverse shows

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

with open('texture_folders.pickle', 'rb') as handle:
    texture_folders: List[str] = pickle.load(handle)

with open('texture_suffixes.pickle', 'rb') as handle:
    texture_suffixes: List[str] = pickle.load(handle)

# search_names('whiskey', 'TEXT')
def sub_guess(prefix: str, type_str: str) -> Optional[str]:
    for suffix in texture_suffixes:
        path_guess = prefix + '.texture' + suffix
        if ioi_string_to_hex(path_guess) + '.' + type_str == hash:
            return path_guess
    return None

# guess 18148364999063540
# This is ONLY optimized for TEXT right now
def guess(hash: str) -> Optional[str]:
    if hash not in reverse:
        # Can this even happen?
        return None
    # Check if we have a parent material
    for d in reverse[hash]:
        if d in data:
            if data[d]['type'] == 'MATI' and len(data[d]['name']) > 0:
                raw_guessed_name = re.search(r"^(.*/)([^\\]*)\.mi.*$", data[d]['name'], re.IGNORECASE)
                if raw_guessed_name is None:
                    continue
                guessed_name = raw_guessed_name.group(1) + raw_guessed_name.group(2)
                guesses = [
                    guessed_name.replace('materials', 'textures'),
                    guessed_name.replace('materials', 'textures').replace('props/', ''),
                    raw_guessed_name.group(2)
                ]
                for g in guesses:
                    a = sub_guess(g, data[hash]['type'])
                    if a is not None:
                        return a
    # Check all of the parents and figure out the folder structures that we might guess
    # Check
    # names = []
    # for d in reverse[hash]:
    #     names.append(data[d]['name'])
    # return names

    # Check how many things it's used on
    return None

# num = 0
for hash in data:
    if len(data[hash]['name']) == 0 and data[hash]['type'] == 'TEXT':
        path = guess(hash)
        # if path is None:
        #     print(data[hash]['hex'] + ' - ' + hash + ' - Unknown')
        if path is not None:
            print(hash + ',' + path)
