from utils import ioi_string_to_hex
import pickle
from typing import List, Any

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('reverse.pickle', 'rb') as handle:
    reverse = pickle.load(handle)

for file in data:
    if data[file]['type'] == 'TEXT' and len(data[file]['name']) > 0:
        materials: List[Any] = []
        if file in reverse:
            for d in reverse[file]:
                if d in data:
                    if data[d]['type'] == 'MATI' and 'assembly' in data[d]['name']:
                        materials.append(data[d])
        if len(materials) == 1:
            print(materials[0]['name'] + "\t" + data[file]['name'])
            # print(data[file]['name'], materials)
        elif len(materials) > 1:
            # Ignore these for now
            continue

