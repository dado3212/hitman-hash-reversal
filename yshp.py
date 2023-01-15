# import string
from utils import ioi_string_to_hex, hashcat
from typing import List, Dict
# import itertools

def guess_from_wordlist():

    match = {
        '00805A591F1A33EE': 1,
        '00777786A3E3D47B': 2,
        '00B476579A770AB6': 3,
    }

    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]

    # def foo(l: str, str_length: int):
    #      yield from itertools.product(*([l] * str_length)) 

    # last_perc = 0.0
    # print(len(words))
    # print('0%')
    # # got up to 6.4% with word_word2 and wordlist_3
    # for i in range(len(words)):
    #     new_perc = round(i * 100.0 / len(words), 1)
    #     if new_perc > last_perc:
    #         last_perc = new_perc
    #         print(new_perc, '%')
    #     word = words[i]
    #     for word2 in words:
    #         file = f"[assembly:/_pro/characters/prototypes/ragdoll_physx/ragdoll_{word}_{word2}.repx].pc_physsys"
    #         hash = ioi_string_to_hex(file)
    #         if hash in match:
    #             print(hash + ',' + file)

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
            file = f"[assembly:/_pro/characters/{word}/ragdoll_physx/ragdoll_{word2}.repx].pc_physsys"
            hash = ioi_string_to_hex(file)
            if hash in match:
                print(hash + ',' + file)

with open('hitman_wordlist.txt', 'r') as f:
    hitman_wordlist = [x.strip() for x in f.readlines()]

with open('wordlist_12.txt', 'r') as f:
    words_12 = [x.strip() for x in f.readlines()]
    words_12 = set([word for word in words_12 if word.isalpha()])

with open('wordlist_3.txt', 'r') as f:
    words_3 = [x.strip() for x in f.readlines()]
    words_3 = set([word for word in words_3 if word.isalpha()])

# hashes = hashcat('YSHP', set(hitman_wordlist), set(hitman_wordlist), ['[assembly:/_pro/characters/','/ragdoll_physx/ragdoll_','.repx].pc_physsys'])
# hashes = hashcat('YSHP', set(hitman_wordlist), set(hitman_wordlist), ['[assembly:/_pro/characters/prototypes/ragdoll_physx/ragdoll_','_','.repx].pc_physsys'])
# hashes = hashcat('YSHP', words_12, words_12, ['[assembly:/_pro/characters/prototypes/ragdoll_physx/ragdoll_','_','.repx].pc_physsys'])
# hashes = hashcat('YSHP', words_12, words_12, ['[assembly:/_pro/characters/prototypes/ragdoll_physx/ragdoll_','','.repx].pc_physsys'])
# hashes = hashcat('YSHP', words_3, words_3, ['[assembly:/_pro/characters/prototypes/ragdoll_physx/ragdoll_','_','.repx].pc_physsys'])
hashes = hashcat('YSHP', words_3, words_3, ['[assembly:/','rigged_props','/ragdoll_physx/ragdoll_bodybag.repx].pc_physsys'])
for hash in hashes:
    print(hash + ', ' + hashes[hash])