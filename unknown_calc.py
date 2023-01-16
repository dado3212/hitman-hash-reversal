import pickle, math
from typing import Dict, TypedDict

class TypeData(TypedDict):
    total: int
    correct: int
    searchable: int

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

types: Dict[str, TypeData] = dict()
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

# There are three table groups.
# 1. Finished - these types have all of the correct names.
# 2. Searchable - these types are all searchable, though they may be missing
#    some correct names.
# 3. Incomplete - these types are missing some searchable names
finished: Dict[str, TypeData] = dict()
searchable: Dict[str, TypeData] = dict()
incomplete: Dict[str, TypeData] = dict()

for type in types:
    if types[type]['correct'] == types[type]['total']:
        finished[type] = types[type]
    elif types[type]['searchable'] == types[type]['total']:
        searchable[type] = types[type]
    else:
        incomplete[type] = types[type]

# Finished
finished_keys = sorted(finished.keys())
print('### Finished')
print('All of these are reversed.')
print('| File Type | Total | Correct | Correct Percentage |')
print('| --- | --- | --- | --- |')
for type in finished_keys:
    print(f"| {type} | {finished[type]['total']} | {finished[type]['correct']} | 100% |")
print()
# Searchable
searchable_keys = sorted(searchable.keys())
print('### Searchable')
print('All of these have a searchable string.')
print('| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |')
print('| --- | --- | --- | --- | --- | --- |')
for type in searchable_keys:
    correct_perc = math.floor(searchable[type]['correct'] * 100.0 / searchable[type]['total']*10)/10
    print(f"| {type} | {searchable[type]['total']} | {searchable[type]['correct']} | {correct_perc}% | {types[type]['searchable']} | 100% |")
print()
# Incomplete
incomplete_keys = sorted(incomplete.keys())
print('### Incomplete')
print('Missing searchable strings.')
print('| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |')
print('| --- | --- | --- | --- | --- | --- |')
for type in incomplete_keys:
    correct_perc = math.floor(incomplete[type]['correct'] * 100.0 / incomplete[type]['total']*10)/10
    searchable_perc = math.floor(incomplete[type]['searchable'] * 100.0 / incomplete[type]['total']*10)/10
    print(f"| {type} | {incomplete[type]['total']} | {incomplete[type]['correct']} | {correct_perc}% | {incomplete[type]['searchable']} | {searchable_perc}% |")

