from utils import ioi_string_to_hex
import pickle, re
from typing import List, Dict

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('hitman_wordlist.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]
    # prefixes = [f'[assembly:/_pro/environment/templates/props/{x}/{x}_props_a.template?/' for x in words]
    # prefixes = [f'[assembly:/_pro/environment/templates/props/{x}_props/{x}_props_a.template?/' for x in words]
    prefixes = [f'[assembly:/_pro/environment/templates/props/{x}/{x}_a.template?/' for x in words]

print('Processing')
unknown: Dict[str, str] = {}
for hash in data:
    if data[hash]['type'] == 'TEMP':
        if (len(data[hash]['name']) > 0 and 
            not data[hash]['current_name']
            and data[hash]['name'] != 'geomentity01'):
            unknown[hash] = data[hash]['name']

last_perc = 0.0
num_prefixes = len(prefixes)
print('0%')
# got up to 6.4% with word_word2 and wordlist_3
for i in range(num_prefixes):
    new_perc = round(i * 100.0 / num_prefixes, 1)
    if new_perc > last_perc:
        last_perc = new_perc
        print(str(new_perc) + '%' + ' - ' + str(i))
    prefix = prefixes[i]
    for hash in unknown:
        new_name = prefix + unknown[hash] + '.entitytemplate].pc_entitytype'
        if ioi_string_to_hex(new_name) == hash:
            print(hash + ', ' + new_name)

