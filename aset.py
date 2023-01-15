
import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data

data = load_data()

with open('aset_suffixes.pickle', 'rb') as handle:
    aset_suffixes: List[str] = pickle.load(handle)

print('loaded')

# As of Jan 14, 2023 this finds every known ASET
for hash in data:
    if data[hash]['type'] == 'ASET' and not data[hash]['correct_name']:
        guesses: set[str] = set([])
        for depends in data[hash]['depends']:
            if depends in data and data[depends]['correct_name'] and data[depends]['name'].endswith('.pc_entitytype'):
                temp_name = data[depends]['name'].removesuffix('.pc_entitytype')
                guesses = guesses.union([f'[assembly:/templates/aspectdummy.aspect]({temp_name}.entitytype{suffix}' for suffix in aset_suffixes])
        found = False
        for guess in guesses:
            possible_hash = ioi_string_to_hex(guess)
            if possible_hash in data and not data[possible_hash]['correct_name']:
                print(possible_hash + ', ' + guess)