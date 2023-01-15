from utils import ioi_string_to_hex, load_data
import pickle, re
from typing import List

data = load_data()

def folders_with_hex_strings():
    with open('material_folders.pickle', 'rb') as handle:
        material_folders = pickle.load(handle)

    for hash in data: 
        if data[hash]['type'] == 'MATI':
            if not data[hash]['correct_name']:
                names = [x.lower() for x in data[hash]['hex_strings'] if '.mi' in x]
                found = False
                for name in names:
                    for folder in material_folders:
                        file_name = f"{folder}/{name}].pc_mi"
                        if ioi_string_to_hex(file_name) == hash:
                            print(hash + ',' + file_name)
                            found = True
                if not found:
                    if len(names) == 0:
                        # this is because my string extraction is too stringent
                        # 00615023F867E70E -> bindi.mi
                        #print(hash)
                        continue
                    unknown_name = f'[unknown:/*/{names[0]}].pc_mi'
                    if unknown_name != data[hash]['name'] and data[hash]['name'] == '':
                        print(hash + ',' + unknown_name)

folders_with_hex_strings()