from utils import ioi_string_to_hex
import pickle, string, re, itertools
from typing import Dict, List

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

print('loaded')

# Letter futzing
# for hash in data:
#     name = data[hash]['name']
#     if len(name) > 0:
#         for letter in string.ascii_lowercase:
#             if ('_' + letter + '.') in name or ('_' + letter + '/') in name or ('_' + letter + '_') in name:
#                 for replacement_letter in string.ascii_lowercase:
#                     if replacement_letter != letter:
#                         new_name = name.replace('_' + letter + '.', '_' + replacement_letter + '.')
#                         new_name = new_name.replace('_' + letter + '/', '_' + replacement_letter + '/')
#                         new_name = new_name.replace('_' + letter + '_', '_' + replacement_letter + '_')
#                         new_hash = ioi_string_to_hex(new_name) + '.' + data[hash]['type']
#                         if new_hash in data:
#                             if len(data[new_hash]['name']) == 0:
#                                 print(new_hash + ',' + new_name)

# Length of the number strings
# {2: 55288, 1: 4475, 3: 372129, 4: 70, 5: 46, 6: 2}
options: Dict[int, List[str]] = {}

for i in [1, 2]:
    options[i] = [''.join(x) for x in itertools.permutations([d for d in '0123456789'], i)]

unique_found: Dict[str, str] = {}

miss_unique = 0
miss_numbers = 0

# Number futzing
for hash in data:
    name = data[hash]['name']
    if len(name) > 0:
        matches = re.findall(r"(.*?_)([\d]+)([\./_].*?)", name, re.IGNORECASE)
        if len(matches) > 0:
            matched_numbers = [x[1] for x in matches]
            unique_numbers = list(set(matched_numbers))
            if len(unique_numbers) == 1:
                num_numbers = len(unique_numbers[0])
                if num_numbers <= 2:
                    for i in range(1, num_numbers + 1):
                            for opt in options[i]:
                                new_file = name.replace(unique_numbers[0], opt)
                                new_hash = ioi_string_to_hex(new_file) + '.' + data[hash]['type']
                                if new_hash in data and len(data[new_hash]['name']) == 0 and new_hash not in unique_found:
                                    print(new_hash + ',' + new_file)
                                    unique_found[new_hash] = new_file
                else:
                    miss_numbers += 1
            else:
                miss_unique += 1

# 3727 368710
print(miss_unique, miss_numbers)