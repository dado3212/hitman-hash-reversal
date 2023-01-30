from utils import ioi_string_to_hex, load_data
import pickle, re
from typing import List, Optional

data = load_data()

def attempt_one():
    # Open the prefixes
    with open('mrtn_folders.pickle', 'rb') as handle:
        mrtn_folders: set[str] = set(pickle.load(handle))

    for folder in list(mrtn_folders):
        mrtn_folders.add(folder.replace('hitman01', 'hitman02'))
        mrtn_folders.add(folder.replace('hitman01', 'hitman03'))

    for hash in data:
        if data[hash]['type'] == 'MRTN':
            for hex_string in data[hash]['hex_strings']:
                for folder in mrtn_folders:
                    possible_paths = [
                        f'{folder}{hex_string.lower()}.aln].pc_rtn',
                        f'{folder}mr_{hex_string.lower()}.aln].pc_rtn',
                    ]
                    for possible_path in possible_paths:
                        possible_hash = ioi_string_to_hex(possible_path)
                        if possible_hash in data and not data[possible_hash]['correct_name']:
                            print(possible_hash + ', ' + possible_path)

attempt_one()
# with open('hitman_wordlist.txt', 'r') as f:
#     words = [x.strip() for x in f.readlines()]

# for hash in data:
#     if data[hash]['type'] == 'MRTN' and not data[hash]['correct_name']:
#         for hex_string in data[hash]['hex_strings']:
#             hex_string = hex_string.lower()
#             # Can also do s03
#             if not hex_string.startswith('mr_'):
#                 continue
#             for word in words:
#                 possible_paths = [
#                     f'[assembly:/animationnetworks/actors/acts/generic/{word}/{hex_string}.aln].pc_rtn',
#                     f'[assembly:/animationnetworks/actors/acts/levels/{word}/{hex_string}.aln].pc_rtn',
#                 ]
#                 for possible_path in possible_paths:
#                     possible_hash = ioi_string_to_hex(possible_path)
#                     if possible_hash in data and not data[possible_hash]['correct_name']:
#                         print(possible_hash + ', ' + possible_path)
        
