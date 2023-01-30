
import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data, hashcat

'''
Some helper commands to answer basic questions:

Q. Do all ASETs have a TEMP dependency?
A. No, some of them just have CPPT and ECPT
[hash for hash in data if data[hash]['type'] == 'ASET' and not any([x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'TEMP'])]

Q. Do all ASETs with a known TEMP dependency have a name?
A. No, but there are only 45 like this right now. 00B47427D1E402CF should probably be gettable.
len([hash for hash in data if data[hash]['type'] == 'ASET' and not data[hash]['correct_name'] and any([x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'TEMP' and data[x]['correct_name']])])

Q. Do any ASETs without TEMP dependencies have known names?
A. Yes, lots. I think they take from the CPPT in these cases. Unless there's an ECPT. Sample is 007D825ACF481D17.
[hash for hash in data if data[hash]['type'] == 'ASET' and data[hash]['correct_name'] and not any([x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'TEMP'])]

Q. Are we missing names for any ASETs without TEMP/ECPTs?
A. No. All missing names have at least one.
[hash for hash in data if data[hash]['type'] == 'ASET' and not data[hash]['correct_name'] and not any([x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'TEMP']) and not any([x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'ECPT'])]

CBLU comes from hex strings. They define CPPT. CPPT defines ASET.
ECPB HAS hex strings, but they're MATI. ASET and ECPT depend on them.
Some of ECPB have the same contents, but different hashes: 0092FF76C6B57704, 00C51F046C6AC1DE
'''

data = load_data()

with open('aset_suffixes.pickle', 'rb') as handle:
    aset_suffixes: List[str] = pickle.load(handle)

print('loaded')

# As of Jan 14, 2023 this finds every known ASET
def use_hashcat():
    left: set[str] = set()
    for hash in data:
        if data[hash]['type'] == 'ASET' and not data[hash]['correct_name']:
            guesses: set[str] = set([])
            for depends in data[hash]['depends']:
                if depends in data and data[depends]['correct_name'] and data[depends]['name'].endswith('.pc_entitytype'):
                    temp_name = data[depends]['name'].removesuffix('.pc_entitytype')
                    left.add(temp_name)
                    guesses = guesses.union([f'[assembly:/templates/aspectdummy.aspect]({temp_name}.entitytype{suffix}' for suffix in aset_suffixes])

    hashes = hashcat('ASET', left, set(aset_suffixes), ['[assembly:/templates/aspectdummy.aspect](', '.entitytype', ''], data)
    for hash in hashes:
        print(hash + ', ' + hashes[hash])

use_hashcat()