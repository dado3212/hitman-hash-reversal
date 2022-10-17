from utils import ioi_string_to_hex
import pickle, re
from typing import List

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

# We're guessing at the switch group name
real_switch_groups: List[str] = []
missing_switch_group: List[str] = []
for hash in data:
    if data[hash]['type'] == 'DSWB' or data[hash]['type'] == 'WSWB':
        if len(data[hash]['name']) > 0:
            current = data[hash]['name']
            if not data[hash]['correct_name']:
                relevant = re.search(r".*/(.*).wwiseswitchgroup.*",data[hash]['name'], re.IGNORECASE)
                assert relevant is not None
                missing_switch_group.append(relevant.group(1))
            else:
                relevant = re.search(r"\[assembly:/sound/wwise/exportedwwisedata/switches/(.*)/.*.wwiseswitchgroup\].pc_entityblueprint",data[hash]['name'], re.IGNORECASE)
                assert relevant is not None
                real_switch_groups.append(relevant.group(1))
        else:
            # print("MISSING GUESS", hash, data[hash])
            continue

for hash in data:
    if data[hash]['type'] == 'WWEV':
        if len(data[hash]['name']) > 0:
            current = data[hash]['name']
            if data[hash]['correct_name']:
                # print(data[hash]['name'])
                relevant = re.search(r"\[assembly:/sound/wwise/exportedwwisedata/events/([^\/]*)/.*",data[hash]['name'], re.IGNORECASE)
                assert relevant is not None
                real_switch_groups.append(relevant.group(1))

real_switch_groups += [
    'alarm',
    'alarms',
    'ambient',
    'backing',
    'band',
    'bands',
    'buttons',
    'musiccontrollers',
    'musiccore',
    'music',
    'car',
    'car_alarms',
    'car_alarm',
    'caralarms',
    'sounds',
    'sound',
    'crowd',
    'crowds',
    'environment',
    'evergreen_loadingscreen',
    'evergreen_loadingscreens',
    'evergreen',
    'fake',
    'fibrewire',
    'footsteps',
    'guitar',
    'guitars',
    'keyboard',
    'keyboards',
    'piano',
    'play',
    'plays',
    'pianos',
    'handheld',
    'handhelds',
    'instrument',
    'instruments',
    'intro',
    'kill',
    'level',
    'levelspecific_switches/switches_azalea',
    'levelspecific_switches/switches_bull',
    'levelspecific_switches/switches_dugong',
    'levelspecific_switches/switches_falcon',
    'levelspecific_switches/switches_flamingo',
    'levelspecific_switches/switches_gecko',
    'levelspecific_switches/switches_golden',
    'levelspecific_switches/switches_hawk',
    'levelspecific_switches/switches_hippo',
    'levelspecific_switches/switches_llama',
    'levelspecific_switches/switches_magpie',
    'levelspecific_switches/switches_mongoose',
    'levelspecific_switches/switches_octopus',
    'levelspecific_switches/switches_peacock',
    'levelspecific_switches/switches_raccoon',
    'levelspecific_switches/switches_rat',
    'levelspecific_switches/switches_seagull',
    'levelspecific_switches/switches_sheep',
    'levelspecific_switches/switches_skunk',
    'levelspecific_switches/switches_snowcrane',
    'levelspecific_switches/switches_spider',
    'levelspecific_switches/switches_stingray',
    'levelspecific_switches/switches_tiger',
    'levelspecific_switches/switches_wolverine',
    'levelspecific_switches/switches_coastaltown',
    'levelspecific_switches/switches_mamba',
    'levelspecific_switches/switches_cottonmouth',
    'levelspecific_switches/switches_gartensnake',
    'levelspecific_switches/switches_anaconda',
    'levelspecific_switches/switches_kingcobra',
    'levelspecific_switches/switches_copperhead',
    'levelspecific_switches/switches_python',
    'levelspecific_switches/switches_polarbear',
    'levelspecific_switches/switches_polar_bear',
    'levelspecific_switches/switches_thefacility',
    'levelspecific_switches/switches_base',
    'levelspecific_switches/switches_rocky_dugong',
    'events',
    'mamba',
    'loading',
    'material',
    'materials',
    'mission',
    'missions',
    'music',
    'musical',
    'play',
    'setpiece',
    'setpieces',
    'sniper',
    'snipermap',
    'song',
    'songs',
    'sound',
    'sounds',
    'track',
    'trigger',
    'vehicles',
    'voice',
    'voices',
    'weapons',
    'weapons1',
    'weapons3',
    'weapons4',
]
real_switch_groups = list(set(real_switch_groups))
# print(real_switch_groups)
# print(missing_switch_group)

for switch in real_switch_groups:
    for missing in missing_switch_group:
        filename = f"[assembly:/sound/wwise/exportedwwisedata/switches/{switch}/{missing}.wwiseswitchgroup].pc_entityblueprint"
        hash = ioi_string_to_hex(filename)
        if hash in data:
            print(hash + ', ' + filename)

with open('wordlist_1.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]

for word in words:
    for missing in missing_switch_group:
        filename = f"[assembly:/sound/wwise/exportedwwisedata/switches/{word}/{missing}.wwiseswitchgroup].pc_entityblueprint"
        hash = ioi_string_to_hex(filename)
        if hash in data:
            print(hash + ', ' + filename)