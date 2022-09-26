import json, hashlib, re, pickle
from typing import Optional, List, Dict, Any
from utils import ioi_string_to_hex

# Missing names:
'''
{
    'LOCR': 604,
    'MATE': 386,
    'TEXT': 10605,
    'ORES': 2,
    'LINE': 5933,
    'ASET': 7251,
    'ECPB': 2730,
    'ECPT': 2730,
    'ASEB': 3969,
    'JSON': 19,
    'YSHP': 1,
    'BMSK': 21,
    'MJBA': 11752,
    'PRIM': 20910,
    'ATMD': 10096,
    'ALOC': 10419,
    'BORG': 4124,
    'VIDB': 88,
    'ASVA': 14,
    'WBNK': 1,
    'DITL': 4,
    'CLNG': 4,
    'DLGE': 2601,
    'GFXI': 2019,
    'FXAS': 3,
    'BOXC': 37,
    'MRTR': 722,
    'VTXD': 2590,
    'TEXD': 10392,
    'RTLV': 6,
    'MRTN': 1149,
    'WWEV': 181,
    'WWEM': 108,
    'ERES': 3,
    'AIBZ': 1,
    'SCDA': 59,
    'CRMD': 1,
    'NAVP': 1,
    'WSWB': 2,
    'WSGB': 2,
    'WSGT': 2,
    'WSWT': 2,
    'GFXV': 1
}
'''

# Find solvable hashes
# What is a solvable hash?
#  it has no name
#  reverse shows

print("starting loading")

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

with open('texture_folders.pickle', 'rb') as handle:
    texture_folders: Dict[int, str] = pickle.load(handle)

with open('texture_suffixes.pickle', 'rb') as handle:
    texture_suffixes: Dict[int, str] = pickle.load(handle)

print("finished loading")

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
    possible = []
    for d in reverse[hash]:
        if d in data:
            if data[d]['type'] == 'MATI' and len(data[d]['name']) > 0:
                guessed_name = re.search(r"^(.*/[^\\]*)\.mi.*$", data[d]['name'], re.IGNORECASE)
                if guessed_name is None:
                    continue
                else:
                    guessed_name = guessed_name.group(1)
                guesses = [
                    guessed_name.replace('materials', 'textures'),
                    guessed_name.replace('materials', 'textures').replace('props/', '')
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
            print(hash + ' - ' + path)
