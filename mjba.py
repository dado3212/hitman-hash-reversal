from utils import ioi_string_to_hex, load_data
import pickle, re
from typing import List, Tuple

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


# extract_from_atmds()
extract_from_mrtns()