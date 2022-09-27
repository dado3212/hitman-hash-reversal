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

print(texture_folders)

with open('./texture_folders.pickle', 'wb') as handle:
    pickle.dump(texture_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./texture_suffixes.pickle', 'wb') as handle:
    pickle.dump(texture_suffixes, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Build material patterns
material_folders = set([])
for hash in data:
    if data[hash]['type'] == 'MATI':
        name = data[hash]['name']
        if 'assembly' in name:
            info = re.search(r"^(.*)/[^\\]*\.mi\]\.pc_mi$", name, re.IGNORECASE)
            if info is None:
                print(name)
                break
            else:
                material_folders.add(info.group(1))

print(material_folders)

with open('./material_folders.pickle', 'wb') as handle:
    pickle.dump(material_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)
