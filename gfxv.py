import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data

data = load_data()

with open('hitman_wordlist.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]

for hash in data:
    if data[hash]['type'] == 'GFXV':
        hex_strings = data[hash]['hex_strings']
        if not data[hash]['correct_name']:
            for string in hex_strings:
                if 'usm' in string or 'avi' in string or 'wav' in string:
                    name = string.lower()[:-4].strip(':')
                    if data[hash]['name'] == '':
                        print(hash + ',' + string.lower())
                    names: List[str] = [name]
                    if name.endswith('.fl'):
                        names.append(name[:-3])
                    for name in names:
                        for word in words:
                            prefixes = [
                                f'[assembly:/{word}/videos/{name}',
                                f'[assembly:/_pro/{word}/videos/{name}',
                                f'[assembly:/ui/{word}/{name}',
                                f'[assembly:/_pro/effects/{word}/{name}',
                            ]
                            potential_paths: List[str] = []
                            for x in prefixes:
                                potential_paths.append(f'{x}.avi].pc_gfxv')
                                potential_paths.append(f'{x}.usm].pc_gfxv')
                                potential_paths.append(f'{x}.wav].pc_gfxv')
                            for potential_path in potential_paths:
                                hex = ioi_string_to_hex(potential_path)
                                if hex in data and not data[hex]['correct_name']:
                                    print(hex + ',' + potential_path)
                                # elif hex in data  and data[hex]['correct_name']:
                                #     print('correct - ' + hex + ',' + potential_path)
                