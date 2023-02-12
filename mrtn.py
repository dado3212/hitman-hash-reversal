from utils import ioi_string_to_hex, load_data, hashcat
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

    all_folders: set[str] = set()
    for folder in mrtn_folders:
        all_folders.add(folder)
        all_folders.add(folder + 'mr_')
    
    mrtn_strings: set[str] = set()

    for hash in data:
        if data[hash]['type'] == 'MRTN':
            for hex_string in data[hash]['hex_strings']:
                mrtn_strings.add(hex_string.lower())

    found = hashcat('MRTN', all_folders, mrtn_strings, ['', '', '.aln].pc_rtn'])
    for hash in found:
        print(hash + '.' + data[hash]['type'] + ', ' + found[hash])

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
        
