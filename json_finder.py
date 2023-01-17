
import pickle, re, json, string
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data, hashcat, recursive_search_json

def guess_from_internal_json():
    data = load_data()
    print('loaded')

    json_files: List[set[str]] = []

    for hash in data:
        if data[hash]['type'] == 'JSON':
            for hex in data[hash]['hex_strings']:
                # There are comments inline, which will cause the parser to choke unless they're removed
                json_data = json.loads(re.sub(r'/\*.*?\*/', '', hex, flags=re.S))
                json_files.append(recursive_search_json('.json', json_data))
    
    unique_json_files: set[str] = set()
    unique_json_files = unique_json_files.union(*json_files)
    prefixes = [
        '[assembly:/_pro/online/default/cloudstorage/resources/',
        '[assembly:/_pro/online/default/cloudstorage/resources/pages/',
    ]
    for file in unique_json_files:
        file = file.lower()
        paths = [f'{prefix}{file}].pc_json' for prefix in prefixes]
        found = False
        for path in paths:
            hash = ioi_string_to_hex(path)
            if hash in data:
                found = True
                if not data[hash]['correct_name']:
                    print(hash + ', ' + path)
        if not found:
            # we're missing:
            #  - menusystem/actions/availability/data/packageids/packageid_seasonpass.json
            #  - menusystem/elements/contract/actions/gotoplanning/planningpage.json
            #  - menusystem/actions/availability/data/packageids/packageid_main.json
            print(file)

guess_from_internal_json()

def guess_from_ores():
    data = load_data()

    print('Loaded')
    # Get all of the ORES files
    potential_images: List[str] = []
    for hash in data:
        if data[hash]['type'] == 'ORES':
            for file in data[hash]['hex_strings']:
                if file.endswith('json'):
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
    # You will need to extract the REPO file from chunk0patch2 in RPKG and rename
    # it to repo.json in this directory
    with open('repo.json', 'r', encoding='utf-8') as f:
        repo = json.load(f)

    data = load_data()

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
        