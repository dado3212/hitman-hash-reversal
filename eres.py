from utils import ioi_string_to_hex
import pickle, re
from typing import List

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

# We're guessing at the switch group name
real_switch_groups: List[str] = []
missing_switch_group: List[str] = []
for hash in data:
    if data[hash]['type'] == 'ERES':
        if len(data[hash]['name']) == 0:
            for d in data[hash]['depends']:
                if d in data and data[d]['type'] == 'TEMP':
                    # Try this
                    relevant = re.search(r"(.*)\..*",data[d]['name'], re.IGNORECASE)
                    if relevant is None:
                        filename = f"[assembly:/_pro/effects/templates/materialdescriptors/{data[d]['name']}.template?/{data[d]['name']}.entitytemplate].pc_entityresource"
                        print(data[d]['name'])
                    else:
                        filename = f"{relevant.group(1)}.pc_entityresource"
                    if ioi_string_to_hex(filename) == hash[:-5]:
                        print(hash, filename)
