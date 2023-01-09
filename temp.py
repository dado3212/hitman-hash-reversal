from utils import ioi_string_to_hex, load_data
import pickle, re, json
from typing import List, Tuple, Dict, Optional

data = load_data()

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

for hash in data:
    if data[hash]['type'] == 'LINE' and not data[hash]['correct_name']:
        # It's not correct, but we have a REPO, and a LOCR with the correct name
        if any([dep for dep in data[hash]['depends'] if dep in data and data[dep]['type'] == 'LOCR' and data[dep]['correct_name']]) and any([v for v in reverse[hash] if v in data and data[v]['type'] == 'REPO']):
            print(hash)
