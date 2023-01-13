from typing import Dict, List
import re
from utils import ioi_string_to_hex, load_data

data = load_data()

def guess_outfits_from_wordlist():
    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]

    last_perc = 0.0
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

# ran with the two of them
def guess_other_from_wordlist():
    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]

    last_perc = 0.0
    #print('0%')

    for i in range(len(words)):
        new_perc = round(i * 100.0 / len(words), 1)
        if new_perc > last_perc:
            last_perc = new_perc
            print(new_perc, '%')
        word = words[i]
        for word2 in words:
            file = f'[assembly:/localization/hitman6/conversations/ui/pro/online/repository/{word}_{word2}.sweetmenutext].pc_localized-textlist'
            hash = ioi_string_to_hex(file)
            if hash in data and not data[hash]['correct_name']:
                print(hash + ', ' + file)

def guess_challenges_from_wordlist():
    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]

    last_perc = 0.0
    #print('0%')

    for i in range(len(words)):
        new_perc = round(i * 100.0 / len(words), 1)
        if new_perc > last_perc:
            last_perc = new_perc
            print(new_perc, '%')
        word = words[i]
        for word2 in words:
            file = f'[assembly:/localization/hitman6/conversations/ui/pro/online/challenges/challenges_{word}_{word2}.sweetmenutext].pc_localized-textlist'
            hash = ioi_string_to_hex(file)
            if hash in data and not data[hash]['correct_name']:
                print(hash + ', ' + file)

def guess_online_folder_from_wordlist():
    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]

    words = [word for word in words if word.isalpha()]

    last_perc = 0.0
    #print('0%')

    for i in range(len(words)):
        new_perc = round(i * 100.0 / len(words), 1)
        if new_perc > last_perc:
            last_perc = new_perc
            print(new_perc, '%')
        word = words[i]
        for word2 in words:
            file = f'[assembly:/localization/hitman6/conversations/ui/pro/online/{word}/{word}_{word2}.sweetmenutext].pc_localized-textlist'
            hash = ioi_string_to_hex(file)
            if hash in data and not data[hash]['correct_name']:
                print(hash + ', ' + file)

def other_formats():
    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]

    last_perc = 0.0
    num_words = len(words)

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

# Goes through the current LOCRs, find things using sc/s3/etc and swaps them
def season_expansion_from_known():
    codes = ['s1', 's2', 's3', 'sc', 'vr']

    guesses: set[str] = set()
    for hash in data:
        if data[hash]['type'] == 'LOCR' and data[hash]['correct_name']:
            # get the full name
            name = re.search(r'(.*)(.sweetmenutext\].pc_localized-textlist)', data[hash]['name'], re.IGNORECASE)
            if name is not None:
                for code in codes:
                    guesses.add(name.group(1) + '_' + code + name.group(2))

            for code in codes:
                for new_code in codes:
                    if new_code != code and f'_{code}' in data[hash]['name']:
                        guesses.add(data[hash]['name'].replace(f'_{code}', f'_{new_code}'))

    for guess in guesses:
        new_hash = ioi_string_to_hex(guess)
        if new_hash in data and not data[new_hash]['correct_name']:
            print(new_hash + ', ' + guess)

guess_online_folder_from_wordlist()

# season_expansion_from_known()
# guess_other_from_wordlist()
# [x for x in data if data[x]['type'] == 'LOCR' and any([f for f in data[x]['hex_strings'] if 'ghost' in f.lower() and 'coin' in f.lower()])]
# [x for x in data if data[x]['type'] == 'LOCR' and any([f for f in data[x]['hex_strings'] if 'blueprint' in f.lower() and 'submarine' in f.lower()])]

# [(x, data[x]['hex_strings']) for x in data if data[x]['type'] == 'LINE' and data[x]['correct_name'] and any([f for f in data[x]['hex_strings'] if '{0}' in f.lower()])]

# [x for x in data if data[x]['type'] == 'LOCR' and not data[x]['correct_name'] and any([f for f in data[x]['hex_strings'] if '<li>' in f.lower()])]
# [x for x in data if data[x]['type'] == 'LOCR' and data[x]['correct_name'] and any([f for f in data[x]['hex_strings'] if 'golden handshake' in f.lower()])]

# trivial