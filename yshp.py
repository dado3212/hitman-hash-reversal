# import string
from utils import ioi_string_to_hex
from typing import List, Dict
# import itertools

match = {
    '00805A591F1A33EE': 1,
    '00777786A3E3D47B': 2,
    '00B476579A770AB6': 3,
}

with open('hitman_wordlist.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]

# def foo(l: str, str_length: int):
#      yield from itertools.product(*([l] * str_length)) 

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
        file = f"[assembly:/_pro/characters/prototypes/ragdoll_physx/ragdoll_{word}_{word2}.repx].pc_physsys"
        hash = ioi_string_to_hex(file)
        if hash in match:
            print(hash + ',' + file)
