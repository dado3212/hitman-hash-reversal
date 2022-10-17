from utils import ioi_string_to_hex
import pickle, re
from typing import List

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

# The general approach is to see if we can futz a known format into left hand/right hand and find anything
bonemasks: List[str] = []
known: List[str] = []
for hash in data:
    if data[hash]['type'] == 'BMSK':
        bonemasks.append(hash)
        if len(data[hash]['name']) > 0:
            relevant = re.search(r"\[assembly:/animations/bonemasks/(.*).bonemask\]\(assembly:/geometry/characters/_export_rigs/biped~~.xml\).pc_bonemask",data[hash]['name'], re.IGNORECASE)
            assert relevant is not None
            known.append(relevant.group(1))

def add_to_list(orig: List[str], left: str, right: str, both_ways: bool = True) -> List[str]:
    new: List[str] = []
    for l in orig:
        new.append(l)
        new.append(l.replace(left, right))
        if both_ways:
            new.append(l.replace(right, left))
    return list(set(new))

known = add_to_list(known, 'left', 'right')
known = add_to_list(known, 'left', 'l', False)
known = add_to_list(known, 'right', 'r', False)
known = add_to_list(known, 'arm', 'leg')
known = add_to_list(known, 'arm', 'hand')
known = add_to_list(known, 'hand', 'leg')
known = add_to_list(known, 'rh', 'lh')
known = add_to_list(known, '_r', '_l')
known = add_to_list(known, 'r_', 'l_')
known = add_to_list(known, '2h', '1h')
known = add_to_list(known, 'both', 'left')
known = add_to_list(known, 'both_', 'left')
known = add_to_list(known, 'both', 'right')
known = add_to_list(known, 'both_', 'right')
known = add_to_list(known, 'arms', 'arm')
known = add_to_list(known, 'legs', 'leg')

iterable = known[::]
for k in iterable:
    known.append('inverse_' + k)
    if ('inverse_' in k):
        known.append(k.replace('inverse_', ''))

known = list(set(known))

known = sorted(known)

for k in known:
    print(k)

for possible in known:
    file_name = f"[assembly:/animations/bonemasks/{possible}.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask"
    possible_hash = ioi_string_to_hex(file_name)
    if possible_hash in data:
        if not data[possible_hash]['correct_name']:
            print(possible_hash + ',' + file_name)

