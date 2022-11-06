import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

print('Loaded')
# Get all of the ORES files
potential_images: List[str] = []
for hash in data:
    if data[hash]['type'] == 'ORES':
        for file in data[hash]['hex_strings']:
            if file.endswith('jpg') or file.endswith('png'):
                potential_images.append(file)

for file in potential_images:
    paths = [
        f'[assembly:/_pro/online/default/cloudstorage/resources/{file}].pc_gfx'
    ]
    for path in paths:
        hash = ioi_string_to_hex(path)
        if hash in data and not data[hash]['correct_name']:
            print(hash + ', ' + path)
        #elif hash in data and data[hash]['correct_name']:
        #    print(hash + ', ' + path)