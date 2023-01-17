from utils import hashcat, ioi_string_to_hex
from typing import List, Dict
import string

aibz: Dict[str, str] = {
    '00560363FF10C45B': '[assembly:/ai/behaviortrees/guard.aibt].pc_aibz',
    '007EF0E7D3283E03': '[assembly:/ai/behaviortrees/sniper_challenge.aibt].pc_aibz',
    '005F87B4C57FD0FF': '',
    '00073FAE6747525B': '[assembly:/ai/behaviortrees/custom/ambientlookathitman.aibt].pc_aibz',
}

# Only use ascii and _ in the guessing for these paths
# Not suitable for everything
allowed = set(string.ascii_lowercase + '_')
with open('hitman_wordlist.txt', 'r') as f:
    hitman_wordlist = set([x.strip() for x in f.readlines()])
with open('wordlist_12.txt', 'r') as f:
    wordlist_12 = set([x.strip() for x in f.readlines()])

wordlist = hitman_wordlist.union(wordlist_12)
wordlist = set([word for word in wordlist if set(word) <= allowed])

def guess_single():
    for word in wordlist:
        possible_path = f'[assembly:/ai/behaviortrees/{word}.aibt].pc_aibz'
        possible_hash = ioi_string_to_hex(possible_path)
        if possible_hash in aibz:
            print(possible_hash + '.AIBZ, ' + possible_path)
    for word in wordlist:
        possible_path = f'[assembly:/ai/behaviortrees/custom/{word}.aibt].pc_aibz'
        possible_hash = ioi_string_to_hex(possible_path)
        if possible_hash in aibz:
            print(possible_hash + '.AIBZ, ' + possible_path)
    for word in wordlist:
        possible_path = f'[assembly:/ai/behaviortrees/custom/ambient{word}.aibt].pc_aibz'
        possible_hash = ioi_string_to_hex(possible_path)
        if possible_hash in aibz:
            print(possible_hash + '.AIBZ, ' + possible_path)

def guess_hashcat():
    formats: List[List[str]] = [
        ['[assembly:/ai/behaviortrees/', '_', '.aibt].pc_aibz'],
        ['[assembly:/ai/behaviortrees/custom/', '_', '.aibt].pc_aibz'],
        ['[assembly:/ai/behaviortrees/', '', '.aibt].pc_aibz'],
        ['[assembly:/ai/behaviortrees/custom/', '', '.aibt].pc_aibz'],
        ['[assembly:/ai/behaviortrees/custom/ambient', '', '.aibt].pc_aibz'],
        ['[assembly:/ai/behaviortrees/', '/', '.aibt].pc_aibz'],
    ]

    target_hashes = set(aibz.keys())
    found_hashes: Dict[str, str] = {}
    for format in formats:
        hashes = hashcat('targeted', wordlist, wordlist, format, override_hashes=target_hashes)
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
    for hash in found_hashes:
        print(hash + '.AIBZ, ' + found_hashes[hash])

# guess_single()
guess_hashcat()