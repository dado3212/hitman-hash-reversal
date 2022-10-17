from utils import ioi_string_to_hex
import pickle, re
from typing import List

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('material_folders.pickle', 'rb') as handle:
    material_folders = pickle.load(handle)

for hash in data: 
    if data[hash]['type'] == 'MATI':
        # This is just true as of right now
        assert len(data[hash]['name']) > 0
        if not data[hash]['correct_name']:
            info = re.search(r"^\[unknown:/\*/(.*)$", data[hash]['name'], re.IGNORECASE)
            if info is None:
                print(data[hash]['name'])
                continue
            for folder in material_folders:
                file_name = f"{folder}/{info.group(1)}"
                if ioi_string_to_hex(file_name) == hash:
                    print(hash + ',' + file_name)


