import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

have_assembly_strings: Dict[str, int] = {}

# {'ORES': 12, 'ECPB': 7805, 'JSON': 23, 'MATI': 17, 'TBLU': 32, 'ALOC': 55, 'TEMP': 88}

for hash in data:
    hex_strings = data[hash]['hex_strings']
    for hex_string in hex_strings:
        if 'assembly' in hex_string:
            if data[hash]['type'] != 'ECPB':
                # print(data[hash]['type'] + ',' + hex_string)
                if data[hash]['type'] in have_assembly_strings:
                    have_assembly_strings[data[hash]['type']] += 1
                else:
                    have_assembly_strings[data[hash]['type']] = 1
            if '[assembly' in hex_string:
                hex_string = re.match(r'.*(\[assembly.*)', hex_string).group(1)
                new_hash = ioi_string_to_hex(hex_string)
                if new_hash in data and not data[new_hash]['correct_name']:
                    print(new_hash + ',' + hex_string)
            elif '.mi' in hex_string:
                potential_paths = [
                    f'[{hex_string}].pc_mi',
                    f'[{hex_string}].pc_entityblueprint',
                    f'[{hex_string}].pc_entitytype'
                ]
                for potential_path in potential_paths:
                    new_hash = ioi_string_to_hex(potential_path)
                    if new_hash in data and not data[new_hash]['correct_name']:
                        print(new_hash + ',' + potential_path)

print(have_assembly_strings)
