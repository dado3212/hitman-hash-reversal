import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

print('Loaded')
# 0089303A81F5B2B1
# Get all of the DLGE files
potential_images: List[str] = []
for hash in data:
    if data[hash]['type'] == 'DLGE':
        if not data[hash]['correct_name']:
            for dependency in data[hash]['depends']:
                if dependency in data and data[dependency]['type'] == 'WWES' and data[dependency]['correct_name']:
                    raw_guessed_name = re.search(r"^\[assembly:/sound/wwise/originals/voices/english\(us\)\/(.*)\.wav.*$", data[dependency]['name'], re.IGNORECASE)
                    if raw_guessed_name is None:
                        continue
                    guessed_name = raw_guessed_name.group(1)
                    pieces = guessed_name.split('/')
                    last = pieces[-1].split('_')
                    for i in range(1, len(last)+1):
                        core_bit = '/'.join(pieces[:-1]) + '/' + '_'.join(last[0:i])
                        possible_paths = [
                             f'[assembly:/localization/hitman6/conversations/{core_bit}.sweetdialog].pc_dialogevent',
                             f'[assembly:/localization/hitman6/conversations/{core_bit}.sweetdialog].pc_sweetdialog'
                        ]
                        for path in possible_paths:
                            possible_hash = ioi_string_to_hex(path)
                            if possible_hash in data and not data[possible_hash]['correct_name']:
                                print(possible_hash + ', ' + path)
