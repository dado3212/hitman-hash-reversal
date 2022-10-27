import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

for hash in data:
    if data[hash]['type'] == 'ECPB':
        hex_strings = data[hash]['hex_strings']
        for string in hex_strings:
            potential_paths = [
                f'[{string}].pc_mi',
                f'[{string}].pc_entityblueprint',
                f'[{string}].pc_entitytype'
            ]
            for potential_path in potential_paths:
                hex = ioi_string_to_hex(potential_path)
                if hex in data and not data[hex]['correct_name']:
                    print(hex + ',' + potential_path)
        