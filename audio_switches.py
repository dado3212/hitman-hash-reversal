from utils import ioi_string_to_hex
import pickle, re
from typing import List

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

# The general approach is to see if we can futz a known format into left hand/right hand and find anything
real_switch_groups: List[str] = []
for hash in data:
    if data[hash]['type'] == 'DSWB' or data[hash]['type'] == 'WSWB':
        if len(data[hash]['name']):
            current = data[hash]['name']
            if (ioi_string_to_hex(data[hash]['name']) != hash[:-5]):
                print(hash, data[hash]['name'])
            else:
                print("Real", data[hash]['name'])
        else:
            print("MISSING", hash, data[hash])
