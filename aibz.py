from utils import hashcat
from typing import List
import string

# Only use ascii and _ in the guessing for these paths
# Not suitable for everything
allowed = set(string.ascii_lowercase + '_')
with open('hitman_wordlist.txt', 'r') as f:
    hitman_wordlist = set([x.strip() for x in f.readlines()])
with open('wordlist_12.txt', 'r') as f:
    wordlist_12 = set([x.strip() for x in f.readlines()])

wordlist = hitman_wordlist.union(wordlist_12)
wordlist = set([word for word in wordlist if set(word) <= allowed])

formats: List[List[str]] = [
    ['[assembly:/ai/behaviortrees/', '_', '.aibt].pc_aibz']
]

target_hashes = set(['005F87B4C57FD0FF'])
for format in formats:
    hashes = hashcat('targeted', wordlist, wordlist, format, override_hashes=target_hashes)
    for hash in hashes:
        print(hash + '.AIBZ, ' + hashes[hash])
