from utils import ioi_string_to_hex, hashcat, load_data
from typing import List, Dict, Optional
import string

# As of Jan 15th, 2023 this gets everything we know
# Outputs known and unknown as well
def broad_guessing():
    data = load_data()

    names: set[str] = set()
    to_crack: Dict[str, Optional[str]] = {}

    for hash in data:
        if (data[hash]['type'] == 'WSWB' or data[hash]['type'] == 'DSWB'):
            to_crack[hash] = None
            for string in data[hash]['hex_strings']:
                names.add(string.lower())

    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])

    formats = [
        ['[assembly:/sound/wwise/exportedwwisedata/switches/levelspecific_switches/switches_','/','.wwiseswitchgroup].pc_entityblueprint'],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/levelspecific_switches/','/','.wwiseswitchgroup].pc_entityblueprint'],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','/','.wwiseswitchgroup].pc_entityblueprint'],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_switches/','.wwiseswitchgroup].pc_entityblueprint'],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/switches_','/','.wwiseswitchgroup].pc_entityblueprint'],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/switch_','/','.wwiseswitchgroup].pc_entityblueprint'],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_switch/','.wwiseswitchgroup].pc_entityblueprint']
    ]
    target_hashes = set([hash for hash in data if data[hash]['type'] in ['WSWB', 'DSWB']])
    for format in formats:
        hashes = hashcat('WSWB', hitman_wordlist, names, format, data, target_hashes)
        for hash in hashes:
            to_crack[hash] = hashes[hash]

    for hash in to_crack:
        path = to_crack[hash]
        if path is None:
            if data[hash]['correct_name']:
                print('Not finding known hash ' + hash + ': ' + data[hash]['name'])
            else:
                print('Failed to find string for hash ' + hash + ': ' + ', '.join(data[hash]['hex_strings']))
        else:
            if data[hash]['correct_name']:
                print('known - ' + hash + ', ' + path)
            else:
                print('new - ' + hash + ', ' + path)


def targeted_guessing(hash: str, name: str):
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])
        
    ending = f'/{name}.wwiseswitchgroup].pc_entityblueprint'
    formats = [
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_switches/switches_',ending],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_switch/switches_',ending],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_switches/switch_',ending],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_switch/switch_',ending],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_',ending],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/','_','_switch'+ending],
        ['[assembly:/sound/wwise/exportedwwisedata/switches/switch_','_',ending],
    ]
    target_hashes = set([hash])
    for format in formats:
        hashes = hashcat('WSWB', wordlist, wordlist, format, override_hashes=target_hashes)
        if hash in hashes:
            print(hash + ', ' + hashes[hash])

broad_guessing()
# targeted_guessing('00CDCD5B35D361CA', 'test_buttonhold_styles') -- failed
# targeted_guessing('0022F2B894BA83F5', 'snipermap_escapecut') -- unknown
# targeted_guessing('000678694BF37C32', 'switch_band_music') -- failed
# targeted_guessing('00E506DBB280035F', 'crowd_state') -- failed