# UICT depends on UICB and CPPT (reverse hash directly to ASET)
# 
from utils import load_data, ioi_string_to_hex

data = load_data()
for hash in data:
    if data[hash]['type'] == 'TBLU':
        for hex in data[hash]['hex_strings']:
            if 'hud' in hex.lower():
                guess = '.'.join(hex.lower().split('_'))
                possible_path = f'[assembly:/ui/controls/hud.swf?/{guess}.uic].pc_entityblueprint'
                possible_hash = ioi_string_to_hex(possible_path)
                if possible_hash in data and not data[possible_hash]['correct_name']:
                    print(possible_hash + '.' + data[possible_hash]['type'] + ', ' + possible_path)
