# This is only named for finding TEMP files

from utils import hashcat, load_data
from typing import Dict, Optional
import string


data = load_data()

for hash in data:
    if data[hash]['type'] == 'TEMP' and not data[hash]['correct_name'] and 'quixel' in data[hash]['name']:


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