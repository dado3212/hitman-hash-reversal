import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data

data = load_data()

print('loaded')

# with open('reverse.pickle', 'rb') as handle:
#     reverse: Dict[str, str] = pickle.load(handle)

# Try and pull them from TEXT/TEXD files for linkedprim
def pull_from_textd():
    potential: set[str] = set()

    for hash in data:
        if data[hash]['correct_name'] and (data[hash]['type'] == 'TEXT' or data[hash]['type'] == 'TEXD'):
            # [assembly:/_pro/items/textures/firearms/frames/sniper_jaeger_envy_a/sniper_jaeger_envy_stock_a.texture?/normal_a.tex](asnormalmap).pc_mipblock1
            # [assembly:/_pro/items/geometry/firearms/frames/sniper_jaeger_envy_a/sniper_jaeger_envy_stock_a.wl2?/sniper_jaeger_envy_stock_a.linkedprim](bodypart).pc_linkedprim
            pieces = re.search(r"^\[assembly:/_pro/items/textures/(.*\/)([^\/]*)\.texture.*$", data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue
            potential.add(f'[assembly:/_pro/items/geometry/{pieces.group(1)}{pieces.group(2)}.wl2?/{pieces.group(2)}.linkedprim](bodypart).pc_linkedprim')
            potential.add(f'[assembly:/_pro/items/geometry/{pieces.group(1)}{pieces.group(2)}.wl2?/{pieces.group(2)}.linkedprim].pc_linkedprim')

    for path_name in potential:
        path_hash = ioi_string_to_hex(path_name)
        if path_hash in data and not data[path_hash]['correct_name']:
            print(path_hash + ', ' + path_name)

def extract_from_dependent_mati():
    for hash in data:
        if data[hash]['type'] == 'PRIM' and not data[hash]['correct_name']:
            for depends in data[hash]['depends']:
                if depends in data and data[depends]['type'] == 'MATI' and data[depends]['correct_name']:
                    # Get the name and see if we can build the PRIM from it
                    pieces = re.search(r"^\[assembly:/_pro/environment/materials/(.*\/)([^\/]*)\.mi.*$", data[depends]['name'], re.IGNORECASE)
                    if pieces is None:
                        continue
                    path_name = f'[assembly:/_pro/environment/geometry/{pieces.group(1)}{pieces.group(2)}.wl2?/{pieces.group(2)}.prim].pc_prim'
                    path_hash = ioi_string_to_hex(path_name)
                    if path_hash in data and not data[path_hash]['correct_name']:
                        print(path_hash + ', ' + path_name)

# Credit to Notex for guessing this pattern 1:54am PST 1/13/2023
def broadly_guess_from_tblu_mati_synthesis():
    prefixes: set[str] = set()
    suffixes: set[str] = set()
    for hash in data:
        if data[hash]['type'] == 'MATI' and data[hash]['correct_name']:
            pieces = re.search(r"^\[assembly:/_pro/environment/materials/(.*\/)([^\/]*)\.mi.*$", data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue
            prefixes.add(f'{pieces.group(1)}{pieces.group(2)}')
            suffixes.add(pieces.group(2))
        if data[hash]['type'] == 'TBLU':
            suffixes = suffixes.union([x.lower() for x in data[hash]['hex_strings']])

    print(len(prefixes))
    print(len(suffixes))

    for prefix in prefixes:
        for suffix in suffixes:
            path_name = f'[assembly:/_pro/environment/geometry/{prefix}.wl2?/{suffix}.prim].pc_prim'
            path_hash = ioi_string_to_hex(path_name)
            if path_hash in data and not data[path_hash]['correct_name']:
                print(path_hash + ', ' + path_name)

broadly_guess_from_tblu_mati_synthesis()
        
