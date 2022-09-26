from typing import List
import hashlib

def hash_to_hex(hash: int) -> str:
    return format(hash, 'x').upper().rjust(16, '0')

def hex_to_hash(hex: str) -> int:
    return int(hex.lstrip('0'), 16)

def ioi_string_to_hex(path: str) -> str:
    raw = hashlib.md5(path.encode()).hexdigest().upper()
    return '00' + raw[2:16]

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
