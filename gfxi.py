import pickle, re, json, string
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data, hashcat

'''
Q. Are there items in the repo file that don't have Image but do have an ID_?
A. Yes.
[item for item in repo if 'Image' not in item][:100]

Q. Are there items in the repo file that don't have Image but do have Outfit?
A. No.
[item for item in repo if 'Image' not in item and 'Outfit' in item]
'''

def guess_from_ores():
    data = load_data()

    print('Loaded')
    # Get all of the ORES files
    potential_images: List[str] = []
    for hash in data:
        if data[hash]['type'] == 'ORES':
            for file in data[hash]['hex_strings']:
                if file.endswith('jpg') or file.endswith('png'):
                    potential_images.append(file)

    for file in potential_images:
        paths = [
            f'[assembly:/_pro/online/default/cloudstorage/resources/{file}].pc_gfx'
        ]
        for path in paths:
            hash = ioi_string_to_hex(path)
            if hash in data and not data[hash]['correct_name']:
                print(hash + ', ' + path)
            #elif hash in data and data[hash]['correct_name']:
            #    print(hash + ', ' + path)

def guess_from_repo():
    data = load_data()

    repo = [data[hash] for hash in data if data[hash]['type'] == 'REPO'][0]
    repo = json.loads(repo['hex_strings'][0])

    print('loaded')

    # keys: set[str] = set()
    # for item in repo:
    #     for key in item:
    #         if isinstance(item[key], str) and ('.jpg' in item[key] or '.png' in item[key] or 'image' in item[key] or 'img' in item[key]):
    #             keys.add(key)
    # print(keys)

    # From above snippet
    guesses: set[str] = set()
    strings: set[str] = set()
    keys = ['ImageTransparent', 'Tile', 'Image']
    for item in repo:
        for key in keys:
            if key in item:
                item_key_string = item[key]
                strings.add(item_key_string)
                # guesses.add(f'[assembly:/_pro/online/default/cloudstorage/resources/{item_key_string}].pc_gfx')

    print(hashcat('GFXI', set(['resources']), strings, ['[assembly:/_pro/online/default/cloudstorage/','/','].pc_gfx']))
        
        # for guess in guesses:
        #     hash = ioi_string_to_hex(guess)
        #     if hash in data and not data[hash]['correct_name']:
        #         print(hash + ', ' + guess)

def just_guess():
    data = load_data()

    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])

    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    for word in wordlist:
        path = '[assembly:/_pro/online/default/cloudstorage/resources/images/entrances/' + word + '_entrance_main_entrance.jpg].pc_gfx'
        hash = ioi_string_to_hex(path)
        if hash in data and not data[hash]['correct_name']:
            print(hash + ', ' + path) # coastaltown_copperhead

# [assembly:/_pro/online/default/cloudstorage/resources/images/contracts/dugong/dugong_tile.jpg].pc_gfx
def alt_guess():
    data = load_data()

    location_prefixes: set[str] = set()
    for hash in data:
        if data[hash]['type'] == 'GFXI' and data[hash]['correct_name']:
            pieces = re.search(r'^.*/resources/images/locations/location_(.*)\/', data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue
            location_prefixes.add(pieces.group(1))
            location_prefixes.add('_'.join(pieces.group(1).split('_')[:-1]))

    print(location_prefixes)

    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])

    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    print(hashcat('GFXI', location_prefixes, wordlist, [
        '[assembly:/_pro/online/default/cloudstorage/resources/images/entrances/','_entrance_','.jpg].pc_gfx'
    ], data))
    # [assembly:/_pro/online/default/cloudstorage/resources/images/locations/location_coastaltown_copperhead/background.jpg].pc_gfx

def paris_guess():
    data = load_data()

    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])

    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    print(hashcat('GFXI', wordlist, wordlist, [
        '[assembly:/_pro/online/default/cloudstorage/resources/images/entrances/paris_entrance_','','.jpg].pc_gfx'
    ], data))
    # [assembly:/_pro/online/default/cloudstorage/resources/images/locations/location_coastaltown_copperhead/background.jpg].pc_gfx

# For new updates
# guess_from_ores()
# guess_from_repo()

# testing
# paris_guess()

# a9debd40-0840-4d44-a035-477295f3d001 <- from sweetline to image, are all of them already listed?