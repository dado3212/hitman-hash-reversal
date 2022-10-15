from utils import ioi_string_to_hex
import pickle, re
from typing import List, Any, Optional, Dict

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('reverse.pickle', 'rb') as handle:
    reverse = pickle.load(handle)

with open('texture_suffixes.pickle', 'rb') as handle:
    texture_suffixes: List[str] = pickle.load(handle)

print("finished loading")

# search_names('whiskey', 'TEXT')
def sub_guess(prefix: str, hash: str) -> Optional[str]:
    for suffix in texture_suffixes:
        path_guess = prefix + '.texture' + suffix
        if ioi_string_to_hex(path_guess) == hash[:-5]:
            return path_guess
    return None

def guess(hash: str) -> Optional[str]:
    if hash not in reverse:
        # Can this even happen?
        return None
    # Check if we have a parent material
    possible: List[str] = []
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
                    a = sub_guess(g, hash)
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

for file in data:
    if data[file]['type'] == 'TEXT' and len(data[file]['name']) == 0:
        materials: List[Any] = []
        any_mats = False
        if file in reverse:
            for d in reverse[file]:
                if d in data:
                    if data[d]['type'] == 'MATI':
                        any_mats = True
                        if 'assembly' in data[d]['name']:
                            materials.append(data[d])
        if len(materials) == 1:
            continue
            # print(materials[0]['name'])
            # print(data[file]['name'], materials)
        elif len(materials) > 1:
            # Ignore these for now
            continue
        else:
            if not any_mats:
                print(file)

