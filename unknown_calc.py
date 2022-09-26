from utils import ioi_string_to_hex
import pickle
from typing import Dict

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

types: Dict[str, Dict[str, int]] = dict()
for hash in data:
    type = data[hash]['type']
    if type not in types:
        types[type] = {
            'correct': 0,
            'total': 0,
        }
    if ioi_string_to_hex(data[hash]['name']) + '.' + type == hash:
        types[type]['correct'] += 1
        types[type]['total'] += 1
    else:
        types[type]['total'] += 1

keys = sorted(types.keys())
print('| File Type | Correct | Total | Percentage |')
print('| --- | --- | --- | --- |')
for type in keys:
    perc = round(types[type]['correct'] * 100.0 / types[type]['total'], 1)
    print(f"| {type} | {types[type]['correct']} | {types[type]['total']} | {perc}% |")

