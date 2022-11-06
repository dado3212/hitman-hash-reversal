# import string
from utils import ioi_string_to_hex
from typing import List, Dict
# import itertools

match = {
    '00D63DA408C1369A': 1,
}

with open('hitman_wordlist.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]

# last_perc = 0
# num_words = len(words)
# for i in range(num_words):
#     new_perc = round(i * 100.0 / num_words, 1)
#     if new_perc > last_perc:
#         last_perc = new_perc
#         print(str(new_perc) + '%' + ' - ' + str(i))
#     current_word = words[i]
#     total_paths: set[str] = set()
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

last_perc = 0.0
print(len(words))
print('0%')
# got up to 6.4% with word_word2 and wordlist_3
for i in range(len(words)):
    new_perc = round(i * 100.0 / len(words), 1)
    if new_perc > last_perc:
        last_perc = new_perc
        print(new_perc, '%')
    word = words[i]
    for word2 in words:
        file = f"[assembly:/sound/wwise/exportedwwisedata/soundbanks/{word}/{word2}.wwisesoundbank].pc_wwisebank"
        hash = ioi_string_to_hex(file)
        if hash in match:
            print(hash + ',' + file)