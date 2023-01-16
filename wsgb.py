from utils import hashcat, load_data
from typing import Dict, Optional
import string

data = load_data()

names: set[str] = set()
to_crack: Dict[str, Optional[str]] = {}

for hash in data:
    if data[hash]['type'] == 'WSGB':
        to_crack[hash] = None
        for string in data[hash]['hex_strings']:
            names.add(string.lower())

with open('hitman_wordlist.txt', 'r') as f:
    hitman_wordlist = set([x.strip() for x in f.readlines()])
    hitman_wordlist = hitman_wordlist.union(names)

formats = [
    # [assembly:/sound/wwise/exportedwwisedata/states/mix_states/mix_isseason3.wwisestategroup].pc_entityblueprint
    ['[assembly:/sound/wwise/exportedwwisedata/states/','_states/','.wwisestategroup].pc_entityblueprint'],
    ['[assembly:/sound/wwise/exportedwwisedata/states/levelspecific_states/','/','.wwisestategroup].pc_entityblueprint'],
    ['[assembly:/sound/wwise/exportedwwisedata/states/levelspecific_states/states_','/','.wwisestategroup].pc_entityblueprint'],
    # [assembly:/sound/wwise/exportedwwisedata/states/ingamemusic_states/musiccore_s2_ambientbiome.wwisestategroup].pc_entityblueprint
]

for format in formats:
    hashes = hashcat('WSGB', hitman_wordlist, names, format, override_hashes=set([hash for hash in data if data[hash]['type'] == 'WSGB']))
    for hash in hashes:
        to_crack[hash] = hashes[hash]

for hash in to_crack:
    path = to_crack[hash]
    if path is None:
        if data[hash]['correct_name']:
            print('Not finding known hash ' + hash + ': ' + data[hash]['name'])
        else:
            print('Failed to find string for hash ' + hash + ': ' + ', '.join(data[hash]['hex_strings']))
    else:
        if data[hash]['correct_name']:
            print('known - ' + hash + ', ' + path)
        else:
            print('new - ' + hash + ', ' + path)