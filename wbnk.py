import string
from utils import ioi_string_to_hex, hashcat, targeted_hashcat, load_data
from typing import List, Dict
# import itertools

match = {
    '00D63DA408C1369A': 1,
}
data = load_data()

allowed = set(string.ascii_lowercase + '_')
with open('hitman_wordlist.txt', 'r') as f:
    hitman_wordlist = set([x.strip() for x in f.readlines()])
with open('wordlist_12.txt', 'r') as f:
    wordlist_12 = set([x.strip() for x in f.readlines()])

wordlist = hitman_wordlist.union(wordlist_12)
wordlist = set([word for word in wordlist if set(word) <= allowed])

# '[assembly:/sound/wwise/exportedwwisedata/soundbanks/globaldata/','_','.wwisesoundbank].pc_wwisebank' -> nothing
# '[assembly:/sound/wwise/exportedwwisedata/soundbanks/globaldata/','','.wwisesoundbank].pc_wwisebank'
#     '[assembly:/sound/wwise/exportedwwisedata/soundbanks/globaldata/play','','.wwisesoundbank].pc_wwisebank'
#     '[assembly:/sound/wwise/exportedwwisedata/soundbanks/globaldata/play_','_','.wwisesoundbank].pc_wwisebank'

f = hashcat('WBNK', wordlist, wordlist, [
    '[assembly:/sound/wwise/exportedwwisedata/soundbanks/globaldata/play_','','.wwisesoundbank].pc_wwisebank'
], override_hashes=set([hash for hash in data if data[hash]['type'] == 'WBNK']))
print(f)

# [assembly:/sound/wwise/exportedwwisedata/soundbanks/{word}/{word2}.wwisesoundbank].pc_wwisebank

# print(targeted_hashcat('00D63DA408C1369A', [
# [assembly:/sound/wwise/exportedwwisedata/soundbanks/{word}/{word2}.wwisesoundbank].pc_wwisebank
# ]))
#     for word in [current_word, f'{current_word}_convolution', f'{current_word}_hq', f'{current_word}_convolution_hq', f'{current_word}_fsp']:
#         paths = set([
#             f'[assembly:/sound/wwise/exportedwwisedata/soundbanks/levelspecific/{word}.wwisesoundbank].pc_wwisebank',
#             f'[assembly:/sound/wwise/exportedwwisedata/soundbanks/globaldata/{word}.wwisesoundbank].pc_wwisebank',
#             f'[assembly:/sound/wwise/exportedwwisedata/soundbanks/{word}data/{word}.wwisesoundbank].pc_wwisebank'
#         ])
#         total_paths = total_paths.union(paths)
#     for path in total_paths:
#         hash = ioi_string_to_hex(path)
#         if hash in match:
#             print(hash + ', ' + path)