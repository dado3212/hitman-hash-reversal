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
            'total': 0,
            'correct': 0,
            'searchable': 0,
        }
    types[type]['total'] += 1
    if len(data[hash]['name']) > 0:
        types[type]['searchable'] += 1
    if data[hash]['correct_name']:
        types[type]['correct'] += 1

keys = sorted(types.keys())
print('| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |')
print('| --- | --- | --- | --- | --- | --- |')
for type in keys:
    correct_perc = round(types[type]['correct'] * 100.0 / types[type]['total'], 1)
    searchable_perc = round(types[type]['searchable'] * 100.0 / types[type]['total'], 1)
    print(f"| {type} | {types[type]['total']} | {types[type]['correct']} | {correct_perc}% | {types[type]['searchable']} | {searchable_perc}% |")

