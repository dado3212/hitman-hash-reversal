from utils import hashcat, load_data
from typing import Dict, Optional
import string

data = load_data()

names: set[str] = set()
to_crack: Dict[str, Optional[str]] = {}

'''
Some helper commands to answer basic questions:

Q. Do all MRTR's have a reverse dependency MJBA?
A. Yes.
[hash for hash in data if data[hash]['type'] == 'MRTR' and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'MJBA']))]

Q. Do all MRTR's with a known MJBA have a name?
A. Yes.
[hash for hash in data if data[hash]['type'] == 'MRTR' and not data[hash]['correct_name'] and any([x for x in reverse[hash] if data[x]['type'] == 'MJBA' and data[x]['correct_name']])]
'''