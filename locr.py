from typing import Dict, List
import re
from utils import ioi_string_to_hex, load_data, hashcat

data = load_data()

def guess_outfits_from_wordlist():
    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]
    words = set(words)

    known = hashcat('LOCR', words, words, ['[assembly:/localization/hitman6/conversations/ui/pro/online/repository/outfits_', '_', '.sweetmenutext].pc_localized-textlist'], data)
    for hash in known:
        print(hash + '.' + data[hash]['type'] + ', ' + known[hash])

def guess_other_from_wordlist():
    with open('hitman_wordlist.txt', 'r') as f:
        words = [x.strip() for x in f.readlines()]
    words = set(words)

    known = hashcat('LOCR', words, words, ['[assembly:/localization/hitman6/conversations/ui/pro/online/repository/', '_', '.sweetmenutext].pc_localized-textlist'], data)
    for hash in known:
        print(hash + '.' + data[hash]['type'] + ', ' + known[hash])

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

    all_words: set[str] = set()
    for word in words:
        all_words.add(word)
        all_words.add(f'{word}_vr')
        all_words.add(f'{word}_s2')
        all_words.add(f'{word}_s3')
        all_words.add(f's2_{word}')
        all_words.add(f's3_{word}')

    extensions: set[str] = set(['pc_localized-textlist', 'pc_multilanguage-textlist'])
    formats: List[List[str]] = [
        ['[assembly:/localization/hitman6/conversations/ui/','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/repository/','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/menutext_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/repository/outfits_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/repository/outfits_npcs_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/challenges/challenges_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/challenges/challenges_et_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/challenges/challenges_orbis_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/gamechangers/gamechangers_','.sweetmenutext].',''],
        # # ['[assembly:/localization/textlists/ui/','/','.localized-textlist].',''], -> can't be supported
        ['[assembly:/localization/textlists/ui/common/','.localized-textlist].',''],
        ['[assembly:/localization/textlists/ui/items/','.localized-textlist].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/hud_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/repository/actor_','.sweetmenutext].',''],
        ['[assembly:/localization/hitman6/conversations/ui/pro/online/repository/items_','.sweetmenutext].',''],
    ]
    all_found: dict[str, str] = {}
    for format in formats:
        found = hashcat('LOCR', all_words, extensions, format, data)
        for hash in found:
            all_found[hash] = found[hash]
    for hash in all_found:
        print(hash + '.' + data[hash]['type'] + ', ' + all_found[hash])

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

# To run on new update
# guess_outfits_from_wordlist()
# guess_other_from_wordlist()
# guess_online_folder_from_wordlist() -> this isn't onboarded to hashcat yet
other_formats()

# Current noodling
# guess_online_folder_from_wordlist()

# season_expansion_from_known()
# guess_other_from_wordlist()
# [x for x in data if data[x]['type'] == 'LOCR' and any([f for f in data[x]['hex_strings'] if 'ghost' in f.lower() and 'coin' in f.lower()])]
# [x for x in data if data[x]['type'] == 'LOCR' and any([f for f in data[x]['hex_strings'] if 'blueprint' in f.lower() and 'submarine' in f.lower()])]

# [(x, data[x]['hex_strings']) for x in data if data[x]['type'] == 'LINE' and data[x]['correct_name'] and any([f for f in data[x]['hex_strings'] if '{0}' in f.lower()])]

# [x for x in data if data[x]['type'] == 'LOCR' and not data[x]['correct_name'] and any([f for f in data[x]['hex_strings'] if '<li>' in f.lower()])]
# [x for x in data if data[x]['type'] == 'LOCR' and data[x]['correct_name'] and any([f for f in data[x]['hex_strings'] if 'golden handshake' in f.lower()])]

# trivial