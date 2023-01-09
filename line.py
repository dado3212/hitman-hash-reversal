from utils import ioi_string_to_hex, load_data
import pickle, re
from typing import List, Tuple, Dict

data = load_data()

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

def extract_setpieces_from_locrs():
    for hash in ['0082FCF9BF0CA18E']:
        if data[hash]['type'] == 'LOCR':
            for hex_string in data[hash]['hex_strings']:
                guesses: set[str] = set()
                for x in [hex_string.lower().replace(' ', '_'), hex_string.lower().replace(' ', '')]:
                    guesses.add(f'[assembly:/localization/hitman6/conversations/ui/pro/setpieces.sweetmenutext?/setpieces_localization_prompt_{x}.sweetline].pc_sweetline')
                for guess in guesses:
                    guessed_hash = ioi_string_to_hex(guess)
                    if guessed_hash in data and data[guessed_hash]['correct_name']:
                        continue
                    elif guessed_hash in data:
                        print(guessed_hash + ', ' + guess)
                        continue
                    else:
                        # dang
                        #print(hash + ': ' + hex_string)
                        continue

def get_incomplete_locrs():
    for hash in data:
        if data[hash]['type'] == 'LOCR' and data[hash]['correct_name']:
            # print if it has incomplete LINEs that depend on it
            incomplete_lines: set[str] = set()
            for x in reverse[hash]:
                if x in data and data[x]['type'] == 'LINE' and not data[x]['correct_name']:
                    incomplete_lines.add(x)
            if len(incomplete_lines) > 0:
                print(hash + ', ' + data[hash]['name'])
                for incomplete in incomplete_lines:
                    print('  ' + incomplete + ': ' + ', '.join(data[incomplete]['hex_strings']))

def extract_from_locrs():
    for hash in data:
        if data[hash]['type'] == 'LOCR' and data[hash]['correct_name']:
            # check if it has LINE that depends on it
            if any([(x in data and data[x]['type'] == 'LINE' and not data[x]['correct_name']) for x in reverse[hash]]):
                name = data[hash]['name']
                print(hash + ', ' + name)
                for hex_string in data[hash]['hex_strings']:
                    guesses: set[str] = set()
                    for x in [hex_string.lower().replace(' ', '_'), hex_string.lower().replace(' ', '')]:
                        guesses.add(f'[assembly:/localization/hitman6/conversations/ui/pro/setpieces.sweetmenutext?/setpieces_localization_prompt_{x}.sweetline].pc_sweetline')
                    for guess in guesses:
                        guessed_hash = ioi_string_to_hex(guess)
                        if guessed_hash in data and data[guessed_hash]['correct_name']:
                            continue
                        elif guessed_hash in data:
                            print(guessed_hash + ', ' + guess)
                            continue
                        else:
                            # dang
                            #print(hash + ': ' + hex_string)
                            continue

def missing_lines():
    locr = '001F0F3B7F11E788'
    for depends in reverse[locr]:
        if data[depends]['type'] == 'LINE' and not data[depends]['correct_name']:
            print(depends + ', ' + ', '.join(data[depends]['hex_strings']))

def all_lines():
    locr = '001F0F3B7F11E788'
    for depends in reverse[locr]:
        if data[depends]['type'] == 'LINE':
            print(depends + ', ' + ', '.join(data[depends]['hex_strings']))

def weird_sgail_guess():
    # with open('hitman_wordlist.txt', 'r') as f:
    #     words = [x.strip() for x in f.readlines()]
    with open('wordlist_1.txt', 'r') as f:
        words = set([]).union([x.strip() for x in f.readlines()])

    for word in words:
        path = f'[assembly:/localization/hitman6/conversations/ui/pro/menutext_s3_elegant.sweetmenutext?/ui_location_elegant_llama_{word}.sweetline].pc_sweetline'
        hash = ioi_string_to_hex(path)
        if hash in data:
            print(hash + ', ' + path + ' : ' + ('old' if data[hash]['correct_name'] else 'new'))

# One off, used to define what goes into futz_names
# Returns 'name', 'title', 'desc', 'description' and a bunch of others
def get_suffixes():
    suffixes: Dict[str, int] = {}
    for hash in data:
        if data[hash]['correct_name'] and data[hash]['type'] == 'LINE':
            path = data[hash]['name']
            real_name = re.search(r"^.*sweetmenutext\?\/?([^\.]*)\.sweetline.*$", path, re.IGNORECASE)
            if (real_name is None):
                continue
            assert real_name is not None
            real_name = real_name.group(1)
            for i in range(0, len(real_name)):
                if real_name[i] == '_':
                    suff = real_name[i+1:]
                    if suff not in suffixes:
                        suffixes[suff] = 0
                    suffixes[suff] += 1
    
    sorted_suffixes = sorted(suffixes.items(), key=lambda x: x[1])
    for suffix in sorted_suffixes:
        if suffix[1] > 2:
            print(suffix[0] + ' - ' + str(suffix[1]))

# A lot of the locations or items have _name or _title or _desc suffixes. Just swap them all
def futz_names():
    swaps = ['name', 'title', 'desc', 'description']
    for hash in data:
        if data[hash]['correct_name'] and data[hash]['type'] == 'LINE':
            name = data[hash]['name']
            guesses: set[str] = set()
            for swap in swaps:
                if swap in name:
                    for new_swap in swaps:
                        guesses.add(new_swap.join(name.rsplit(swap, 1)))
            for guess in guesses:
                possible_hash = ioi_string_to_hex(guess)
                if possible_hash in data and not data[possible_hash]['correct_name']:
                    print(possible_hash + ', ' + guess)


# missing_lines()
# all_lines()
# get_incomplete_locrs()
weird_sgail_guess()
# futz_names()
