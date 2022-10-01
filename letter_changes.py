from utils import ioi_string_to_hex
import pickle, re, string
from typing import List, Any, Optional, Dict

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

print('loaded')

opts = ['_' + l + '.' for l in string.ascii_lowercase]

for hash in data:
    name = data[hash]['name']
    if len(name) > 0:
        for o in opts:
            if o in name:
                for b in opts:
                    if b != o:
                        new_name = name.replace(o, b)
                        new_hash = ioi_string_to_hex(new_name) + '.' + data[hash]['type']
                        if new_hash in data:
                            if len(data[new_hash]['name']) == 0:
                                print(new_hash + ',' + new_name)
