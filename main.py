import json, hashlib, re, pickle
from typing import Optional, List, Dict

def hash_to_hex(hash: int) -> str:
    return format(hash, 'x').upper().rjust(16, '0')

def hex_to_hash(hex: str) -> int:
    return int(hex.lstrip('0'), 16)

def ioi_string_to_hex(path: str) -> str:
    raw = hashlib.md5(path.encode()).hexdigest().upper()
    return '00' + raw[2:16]

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
    data: Dict[int, str] = pickle.load(handle)

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[int, str] = pickle.load(handle)

with open('texture_folders.pickle', 'rb') as handle:
    texture_folders: Dict[int, str] = pickle.load(handle)

with open('texture_suffixes.pickle', 'rb') as handle:
    texture_suffixes: Dict[int, str] = pickle.load(handle)

print("finished loading")

# ioi_strings = dict()
# for hash in data:
#     name = data[hash]['name']
#     if len(name) > 0:
#         ioi_strings[name] = hash

def recursive_print(hash, prefix = ""):
    if (len(prefix) > 2):
        return
    name = data[hash]['name']
    if (len(name) == 0):
        name = data[hash]['hex']
    print(prefix + name + ' - ' + hash)
    if hash in reverse:
        short = reverse[hash][:3]
        for reverse_hash in short:
            recursive_print(reverse_hash, prefix + ' ')

def child_names(hash) -> List[str]:
    names = []
    for depends in data[hash]['depends']:
        depends = str(depends)
        names.append(data[depends]['name'])
    return names

def parent_names(hash) -> List[str]:
    names = []
    if hash in reverse:
        for d in reverse[hash]:
            names.append(data[d]['name'])
    return names

# 'TEXT'
def search_names(search_str, search_type = None):
    names = dict()
    for name in ioi_strings:
        if search_str in name:
            if search_type is None:
                names[name] = ioi_strings[name]
            elif data[ioi_strings[name]]['type'] == search_type:
                names[name] = ioi_strings[name]
    return names

# search_names('whiskey', 'TEXT')

# guess 18148364999063540
# This is ONLY optimized for TEXT right now
def guess(hash) -> Optional[str]:
    if hash not in reverse:
        # Can this even happen?
        print(data[hash])
        return None
    # If it's more than 20, then it's probably some common thing, for now we'll just be scared
    if len(reverse[hash]) > 20:
        return None
    # Check if we have a parent material
    possible = []
    for d in reverse[hash]:
        if data[d]['type'] == 'MATI' and len(data[d]['name']) > 0:
            guessed_name = re.search(r"^.*/([^\\]*)\.mi.*$", data[d]['name'], re.IGNORECASE)
            if guessed_name is None:
                continue
            else:
                guessed_name = guessed_name.group(1)
            for folder in texture_folders:
                for suffix in texture_suffixes:
                    path_guess = folder + '/' + guessed_name + '.texture' + suffix
                    if str(hex_to_hash(ioi_string_to_hex(path_guess))) == hash:
                        return path_guess
    # Check all of the parents and figure out the folder structures that we might guess
    # Check
    # names = []
    # for d in reverse[hash]:
    #     names.append(data[d]['name'])
    # return names

    # Check how many things it's used on
    return None

# print(guess('62858028897180236'))
# num = 0
for hash in data:
    if len(data[hash]['name']) == 0 and data[hash]['type'] == 'TEXT':
        path = guess(hash)
        # if path is None:
        #     print(data[hash]['hex'] + ' - ' + hash + ' - Unknown')
        if path is not None:
            print(data[hash]['hex'] + ' - ' + hash + ' - ' + path)
