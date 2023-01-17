
import pickle, re, json, string
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data, hashcat, recursive_search_json, targeted_hashcat

def guess_from_internal_files():
    data = load_data()
    print('loaded')

    unique_json_files: set[str] = set()

    json_files: List[set[str]] = []
    for hash in data:
        # Extract from JSON files
        if data[hash]['type'] == 'JSON':
            for hex in data[hash]['hex_strings']:
                # There are comments inline, which will cause the parser to choke unless they're removed
                json_data = json.loads(re.sub(r'/\*.*?\*/', '', hex, flags=re.S))
                json_files.append(recursive_search_json('.json', json_data))
        # Extract from ORES
        if data[hash]['type'] == 'ORES':
            for file in data[hash]['hex_strings']:
                if file.endswith('json'):
                    unique_json_files.add(file)

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

'''
TODO:
# images/opportunities/paris/a_drink_to_die_for.jpg
[hash for hash in data if any([x for x in data[hash]['hex_strings'] if 'drink' in x.lower() and 'die' in x.lower()])]
['0079B380B37AEAF1', '0085A5322F17780B', '00AB1D668DC934AC', '00858D45F5F9E3CA', '0081B0BF7796D935', '008C3FB1413D3282', '0063286E12B2EB51', '0031AC754E803BCE', '002B99A09946C5DC', '009ABD734A611929', '005963BA07653C75', '00AFC440C1E9F6E9']
005963BA07653C75 -> LINE for the title (maybe op3008_cocktail_001)
0081B0BF7796D935, [unknown:/opportunities.json](sniperchallenge).pc_json -> are the summary/title/briefing used in hashes?
"728ff71e-395d-4a00-8065-305a43a92105": {
    "Summary": "op3008_cocktail_002",
    "Title": "op3008_cocktail_001",
    "Briefing": "op3008_cocktail_003",
    "Image": "images/opportunities/paris/a_drink_to_die_for.jpg",
    "IsMainOpportunity": false
},
'''
