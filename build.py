import json, hashlib, re, pickle
from typing import Optional, List

def hash_to_hex(hash: int) -> str:
    return format(hash, 'x').upper().rjust(16, '0')

def hex_to_hash(hex: str) -> int:
    return int(hex.lstrip('0'), 16)

def ioi_string_to_hex(path: str) -> str:
    raw = hashlib.md5(path.encode()).hexdigest().upper()
    return '00' + raw[2:16]

print('Starting')
with open('hashes.json', 'r') as f:
    data = json.load(f)
    print('Loaded')

with open('./hashes.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

reverse = dict()
for hash in data:
    for depends in data[hash]['depends']:
        depends = str(depends)
        if depends not in reverse:
            reverse[depends] = []
        reverse[depends].append(hash)

with open('./reverse.pickle', 'wb') as handle:
    pickle.dump(reverse, handle, protocol=pickle.HIGHEST_PROTOCOL)

ioi_strings = dict()
for hash in data:
    name = data[hash]['name']
    if len(name) > 0:
        ioi_strings[name] = hash

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

# Build text patterns
texture_folders = set([])
texture_suffixes = set([])
for hash in data:
    if data[hash]['type'] == 'TEXT':
        name = data[hash]['name']
        if len(name) > 0 and 'texture' in name:
            info = re.search(r"^(.*)/([^\\]*)\.texture(.*)$", name, re.IGNORECASE)
            if info is None:
                print(name)
                break
            else:
                texture_folders.add(info.group(1))
                texture_suffixes.add(info.group(3))

with open('./texture_folders.pickle', 'wb') as handle:
    pickle.dump(texture_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./texture_suffixes.pickle', 'wb') as handle:
    pickle.dump(texture_suffixes, handle, protocol=pickle.HIGHEST_PROTOCOL)

material_folders = set([])
material_suffixes = set([])
for hash in data:
    if data[hash]['type'] == 'MATI':
        name = data[hash]['name']
        if 'mi' not in name:
            print(data[hash])
        if len(name) > 0 and 'mi' in name:
            # [assembly:/_pro/effects/materials/debris/fx_par_debris_paper_4x4_01.mi].pc_mi
            info = re.search(r"^(.*)/([^\\]*)\.mi(.*)$", name, re.IGNORECASE)
            if info is None:
                print(name)
                break
            else:
                material_folders.add(info.group(1))
                material_suffixes.add(info.group(3))

print(material_folders)
print(material_suffixes)

with open('./texture_folders.pickle', 'wb') as handle:
    pickle.dump(texture_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./texture_suffixes.pickle', 'wb') as handle:
    pickle.dump(texture_suffixes, handle, protocol=pickle.HIGHEST_PROTOCOL)
