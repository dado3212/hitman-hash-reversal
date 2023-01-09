from utils import ioi_string_to_hex, load_data
import pickle, re, json
from typing import Dict, Optional

data = load_data()

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

# This fetches the LOCRs that have LINEs that aren't complete.
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

# Given a LOCR hash this tries to figure out what the prefix is based on the 
# known LINEs for the LOCR
def guess_prefix(hash: str) -> Optional[str]:
    potential_prefixes: Dict[str, int] = {}
    for reverse_hash in reverse[hash]:
        if reverse_hash in data and data[reverse_hash]['type'] == 'LINE' and data[reverse_hash]['correct_name']:
            # Guess the prefix
            reverse_name = data[reverse_hash]['name']
            for i in range(0, len(reverse_name)):
                if reverse_name[i] == '_':
                    prefix = reverse_name[:i]
                    if prefix not in potential_prefixes:
                        potential_prefixes[prefix] = 0
                    potential_prefixes[prefix] += 1
    prefixes = [(key, potential_prefixes[key]) for key in potential_prefixes if potential_prefixes[key] > 1]
    # If you have prefixes, then return the most popular, tiebreaking by length
    if len(prefixes) > 0:
        most_common = max([pref[1] for pref in prefixes])
        best = sorted([x[0] for x in prefixes if x[1] == most_common], key=lambda x: len(x))
        return best[-1]
    # Now we're in pure guess mode, these are hardcoded lol
    return None

# It goes through each LOCR, and figures out if it has LINEs that depend on it.
# If it does, it guesses the prefix. It then basically just tries to replace
# spaces with nothing or _ and see if that works. It has an okay hit rate.
def extract_from_locrs():
    for hash in data:
        if data[hash]['type'] == 'LOCR' and data[hash]['correct_name']:
            # check if it has LINE that depends on it
            if any([(x in data and data[x]['type'] == 'LINE' and not data[x]['correct_name']) for x in reverse[hash]]):
                # Do we know the prefix? If so, let's use it
                prefix = guess_prefix(hash)
                if prefix is None:
                    print('We should guess. ' + hash + ', ' + data[hash]['name'])
                    continue
                for hex_string in data[hash]['hex_strings']:
                    guesses: set[str] = set()
                    for x in [hex_string.lower().replace(' ', '_'), hex_string.lower().replace(' ', '')]:
                        guesses.add(f'{prefix}_{x}.sweetline].pc_sweetline')
                    for guess in guesses:
                        guessed_hash = ioi_string_to_hex(guess)
                        if guessed_hash in data and data[guessed_hash]['correct_name']:
                            continue
                        elif guessed_hash in data:
                            print(guessed_hash + ', ' + guess)
                            continue
                        else:
                            # dang, maybe we can improve this
                            #print(hash + ': ' + hex_string)
                            continue

# A lot of names/descriptions are stored in the REPO file. If we get new LOCR
# bases then we can guess a lot of files using this technique. See the note
# around importing the file correctly though.
def guess_from_repo():
    # You will need to extract the REPO file from chunk0patch2 in RPKG and rename
    # it to repo.json in this directory
    with open('repo.json', 'r', encoding='utf-8') as f:
        repo = json.load(f)

    prefixes: set[str] = set()

    for hash in data:
        if data[hash]['correct_name'] and data[hash]['type'] == 'LOCR':
            # extract it
            if 'sweetmenutext' in data[hash]['name']:
                f = re.search(r"^(.*sweetmenutext).*$", data[hash]['name'], re.IGNORECASE)
                assert f is not None
                prefixes.add(f.group(1))

    for item in repo:
        guesses: set[str] = set()
        keys = ['Name', 'Description', 'Name_LOC', 'Description_LOC']
        for key in keys:
            if key in item:
                item_key_string = item[key]
                for prefix in prefixes:
                    guesses.add(f'{prefix}?/{item_key_string}.sweetline].pc_sweetline')
        
        for guess in guesses:
            hash = ioi_string_to_hex(guess)
            if hash in data and not data[hash]['correct_name']:
                print(hash + ', ' + guess)

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

# A lot of the locations or items have _name or _title or _desc suffixes.
# Just try swapping them all to see if we get anything new!
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

# This goes through the REPO.json file and finds names that look like they should
# be LINE values, but aren't currently used. These are like the things that are
# missing from the LOCR values because they don't have a known LOCR. We can use
# them to guess.
def find_unowned_hashes():
    with open('repo.json', 'r', encoding='utf-8') as f:
        repo = json.load(f)

    correct_lines: Dict[str, str] = {}
    for hash in data:
        if data[hash]['type'] == 'LINE' and data[hash]['correct_name']:
            correct_lines[data[hash]['name']] = hash

    repo_strings: set[str] = set()
    for item in repo:
        keys = ['Name', 'Description', 'Name_LOC', 'Description_LOC']
        for key in keys:
            if key in item:
                item_key_string = item[key]
                # Then look it up...in all of hashes LMAO
                found = False
                for name in correct_lines:
                    if item_key_string in name:
                        found = True
                        break
                if not found and item_key_string.count('_') > 1:
                    repo_strings.add(item_key_string)

    sorted_strings = sorted(list(repo_strings))
    for string in sorted_strings:
        print(string)

# Used only for when you've just found a new LOCR and you want to locally check
# it for LINE expansions. If the LOCR is already in the hash_list then you can 
# just use `guess_from_repo` instead which will automtically find it
def search_repo_for_new_locr(prefix: str):
    # You will need to extract the REPO file from chunk0patch2 in RPKG and rename
    # it to repo.json in this directory
    with open('repo.json', 'r', encoding='utf-8') as f:
        repo = json.load(f)

    for item in repo:
        guesses: set[str] = set()
        keys = ['Name', 'Description', 'Name_LOC', 'Description_LOC']
        for key in keys:
            if key in item:
                item_key_string = item[key]
                guesses.add(f'{prefix}?/{item_key_string}.sweetline].pc_sweetline')
        
        for guess in guesses:
            hash = ioi_string_to_hex(guess)
            if hash in data and not data[hash]['correct_name']:
                print(hash + ', ' + guess)

# Every LINE that has a named LOCR and we know the suffix from REPO should be
# known. Did we get them all?
def are_we_dumb():
    for hash in data:
        if data[hash]['type'] == 'LINE' and not data[hash]['correct_name']:
            # It's not correct, but we have a REPO, and a LOCR with the correct name
            if any([dep for dep in data[hash]['depends'] if dep in data and data[dep]['type'] == 'LOCR' and data[dep]['correct_name']]) and any([v for v in reverse[hash] if v in data and data[v]['type'] == 'REPO']):
                print(hash)

search_repo_for_new_locr('[assembly:/localization/hitman6/conversations/ui/pro/online/repository/firearms_sc.sweetmenutext')