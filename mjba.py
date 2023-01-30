from utils import ioi_string_to_hex, load_data
import pickle, re
from typing import List, Tuple

'''
Some helper commands to answer basic questions:

Q. Do all MJBA's have a reverse dependency MRTN?
A. No. 6,020 do not.
[hash for hash in data if data[hash]['type'] == 'MJBA' and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'MRTN']))]

Q. Do all MJBA's without a reverse dependency MRTN have a reverse dependency ASVA?
A. Nop. 3,433 do not. Some of them 
[hash for hash in data if data[hash]['type'] == 'MJBA' and (hash not in reverse or (not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'MRTN']) and not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'ASVA'])))]

Q. Do any MJBA's without a reverse dependency MRTN have a name?
A. Yes. But it may be because of other MRTNs that for some reason aren't direct dependencies.
[hash for hash in data if data[hash]['type'] == 'MJBA' and data[hash]['correct_name'] and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'MRTN']))]
# Example:
[(hash, data[hash]['type']) for hash in data if any([x for x in data[hash]['hex_strings'] if 'mr_carryplate_pickup_putdown_75cm' in x.lower()])]
'''

data = load_data()

# Extract from ATMDs
def extract_from_atmds():
    for hash in data:
        if data[hash]['type'] == 'MJBA' and not data[hash]['correct_name']:
            for depends in data[hash]['depends']:
                # This literally never happens right now
                if depends in data and data[depends]['type'] == 'ATMD' and data[depends]['correct_name']:
                    pieces = re.search(r"^(.*)\.amd\?\/(.*)\.atmd\]\.pc_atmd*$", data[depends]['name'], re.IGNORECASE)
                    if pieces is None:
                        print('Something went wrong regex')
                        print(hash + ', ' + data[hash]['name'])
                        exit()
                    potential_paths = [
                        f'{pieces.group(1)}.xmd?/{pieces.group(2)}.xmdtake](cutsequence).pc_animation',
                        f'{pieces.group(1)}.xmd?/{pieces.group(2)}.xmdtake](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_animation'
                    ]
                    for potential_path in potential_paths:
                        potential_hash = ioi_string_to_hex(potential_path)
                        if potential_hash in data and not data[potential_hash]['correct_name']:
                            print(potential_hash + ', ' + potential_path)

# Extract from MRTNs
def extract_from_mrtns():
    for hash in data:
        if data[hash]['correct_name'] and data[hash]['type'] == 'MRTN':
            # Needs to have some correct, and some empty
            correct: set[Tuple[str, str]] = set()
            wrong_hashes: set[str] = set()
            for depends in data[hash]['depends']:
                if depends in data and data[depends]['type'] == 'MJBA':
                    if data[depends]['correct_name']:
                        # [assembly:/animations/npc/009_acts/levels/hokkaido/mr_sit_ground_spa_relaxed.xmd?/enter.xmdtake](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_animation
                        pieces = re.search(r"^(.*\.xmd\?\/)(.*)(\.xmdtake.*)$", data[depends]['name'], re.IGNORECASE)
                        if pieces is None:
                            print('Failed to extract: ' + depends)
                            exit()
                        correct.add((pieces.group(1), pieces.group(3)))
                    else:
                        wrong_hashes.add(depends)
            if len(wrong_hashes) > 0 and len(correct) > 0:
                for c in correct:
                    for hex_string in data[hash]['hex_strings']:
                        possible_path = c[0] + hex_string.lower() + c[1]
                        possible_hash = ioi_string_to_hex(possible_path)
                        if possible_hash in wrong_hashes:
                            print(possible_hash + ', ' + possible_path)


extract_from_atmds()
# extract_from_mrtns()