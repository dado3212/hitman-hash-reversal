import pickle
from typing import Dict, List
from utils import ioi_string_to_hex

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('hitman_wordlist.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]

last_perc = 0.0
num_words = len(words)
#print('0%')

for i in range(len(words)):
    new_perc = round(i * 100.0 / len(words), 1)
    if new_perc > last_perc:
        last_perc = new_perc
        print(new_perc, '%')
    word = words[i]
    for word2 in words:
        file = f'[assembly:/localization/hitman6/conversations/ui/pro/online/repository/outfits_{word}_{word2}.sweetmenutext].pc_localized-textlist'
        hash = ioi_string_to_hex(file)
        if hash in data and not data[hash]['correct_name']:
            print(hash + ', ' + file)

exit()

relevant: Dict[str, List[bool]] = {}
for hash in data:
    if data[hash]['type'] == 'LOCR':
        relevant[hash] = [data[hash]['correct_name'], False]

for i in range(num_words):
    new_perc = round(i * 100.0 / num_words, 1)
    if new_perc > last_perc:
        last_perc = new_perc
        print(str(new_perc) + '%' + ' - ' + str(i))
    current_word = words[i]
    total_paths: set[str] = set()
    for word in [current_word, f'{current_word}_vr', f'{current_word}_s2', f'{current_word}_s3', f's2_{current_word}', f's3_{current_word}']:
        for extension in ['pc_localized-textlist', 'pc_multilanguage-textlist']:
            paths = set([
                f'[assembly:/localization/hitman6/conversations/ui/{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/repository/{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/menutext_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/repository/outfits_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/repository/outfits_npcs_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/challenges/challenges_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/challenges/challenges_et_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/challenges/challenges_orbis_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/gamechangers/gamechangers_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/textlists/ui/{word}/{word}.localized-textlist].{extension}',
                f'[assembly:/localization/textlists/ui/common/{word}.localized-textlist].{extension}',
                f'[assembly:/localization/textlists/ui/items/{word}.localized-textlist].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/hud_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/repository/actor_{word}.sweetmenutext].{extension}',
                f'[assembly:/localization/hitman6/conversations/ui/pro/online/repository/items_{word}.sweetmenutext].{extension}'
            ])
            total_paths = total_paths.union(paths)
    for path in total_paths:
        hash = ioi_string_to_hex(path)
        if hash in data:
            relevant[hash][1] = True
            if not data[hash]['correct_name']:
                print(hash + ', ' + path)

print('Relevant')
for hash in relevant:
    if relevant[hash][1] == False and relevant[hash][0] == True:
        print(hash + ' - ' + data[hash]['name'])
