import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex, load_data

data = load_data()

# with open('reverse.pickle', 'rb') as handle:
#     reverse: Dict[str, str] = pickle.load(handle)

# Try and pull them from TEXT/TEXD files for linkedprim

print('loaded')

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
        
