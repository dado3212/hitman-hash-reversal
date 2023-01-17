import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data, hashcat

data = load_data()

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

print('loaded')

for hash in data:
    if data[hash]['type'] == 'ASEB':
        if hash not in reverse:
            print('Whoa, ' + hash + ' is not used anywhere.')
            exit()
        found = False
        for reversed in reverse[hash]:
            if data[reversed]['type'] == 'ASET':
                found = True
                if data[reversed]['correct_name'] and not data[hash]['correct_name']:
                    print('Whoa, ' + hash + ' has an ASET but does not know what it is')
                    exit()
        if not found:
            print('Whoa, ' + hash + ' has no ASET dependency.')
            exit()
            

