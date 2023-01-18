from utils import ioi_string_to_hex, load_data, hashcat
import pickle, re
from typing import List

data = load_data()

def folders_with_hex_strings():
    with open('material_folders.pickle', 'rb') as handle:
        material_folders: List[str] = pickle.load(handle)

    mati_names: set[str] = set()
    for hash in data: 
        if data[hash]['type'] == 'MATI':
            if not data[hash]['correct_name']:
                for x in data[hash]['hex_strings']:
                    if '.mi' in x.lower():
                        mati_names.add(x.lower())

    hashes = hashcat('MATI', set(material_folders), mati_names, ['', '/', '].pc_mi'], data)
    for hash in hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + hashes[hash])

folders_with_hex_strings()