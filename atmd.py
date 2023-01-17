import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data, hashcat

data = load_data()

print('loaded')

'''
Some helper commands to answer basic questions:

Q. Do all ATMD's have an MJBA?
A. Yes.
[hash for hash in data if data[hash]['type'] == 'ATMD' and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'MJBA']))]

Q. Do all ATMD's with a known MJBA have a name?
A. Yes.
[hash for hash in data if data[hash]['type'] == 'ATMD' and not data[hash]['correct_name'] and any([x for x in reverse[hash] if data[x]['type'] == 'MJBA' and data[x]['correct_name']])]
'''

# Confirm that there aren't weird thing in here hiding.
# There are:
#   - modules:/zhm5hikeventconsumer.class
#   - modules:/zhm5bodysoundeventconsumer.class
for hash in data:
    if data[hash]['type'] == 'ATMD':
        for string in data[hash]['hex_strings']:
            string = string.lower()
            if 'module' in string:
                path = f'[{string}].pc_entitytype'
                new_hash = ioi_string_to_hex(path)
                if new_hash not in data:
                    print('AH!!: ' + hash + ', ' + string)
                if new_hash in data and not data[new_hash]['correct_name']:
                    print('Whoa, new ' + new_hash + ', ' + path)