# coding=utf8
from utils import ioi_string_to_hex
import pickle, re
from typing import List

replacements = [
    # Simple replacements (will be ran both ways)
    (False, '.pc_tex', '.pc_mipblock1'),
    (False, '.prim].pc_prim', '.prim].pc_entitytype'),
    (False, '.prim].pc_prim', '.linkedprim].pc_bonerig'),
    (False, '.prim].pc_prim', '.linkedprim].pc_coll'),
    (False, '.prim].pc_prim', '.linkedprim].pc_entitytype'),
    (False, '.prim].pc_prim', '.linkedprim].pc_linkedprim'),
    (False, '.pc_entitytype', '.pc_entityblueprint'),
    (False, '.pc_entitytemplate', '.pc_entityblueprint'),
    (False, '.pc_entitytype', '.pc_mi'),
    (False, '.prim].pc_prim', '.prim].pc_coll')
    # Regex replacements (are unidirectional)
    # [assembly:/_pro/environment/templates/props/street_props/street_props_mumbai_a.template?/tent_street_mumbai_f.entitytemplate].pc_entitytype
    # [assembly:/_pro/environment/geometry/props/street_props/tent_street_mumbai_a.wl2?/tent_street_mumbai_f.prim].pc_entitytype
]

def find_alternate_paths(file: str, run_again: bool = True) -> dict[str, str]:
    alt_paths: dict[str, str] = dict()
    for replacement in replacements:
        # Regex
        if replacement[0]:
            continue
        else:
            if file.endswith(replacement[1]):
                new_file = file.removesuffix(replacement[1]) + replacement[2]
                new_hash = ioi_string_to_hex(new_file)
                alt_paths[new_hash] = new_file
            if file.endswith(replacement[2]):
                new_file = file.removesuffix(replacement[2]) + replacement[1]
                new_hash = ioi_string_to_hex(new_file)
                alt_paths[new_hash] = new_file
    if run_again:
        iterated_paths = list(alt_paths.keys())[::]
        for hash in iterated_paths:
            alt_paths2 = find_alternate_paths(alt_paths[hash], False)
            for hash2 in alt_paths2:
                if hash2 not in alt_paths:
                    alt_paths[hash2] = alt_paths2[hash2]
    return alt_paths

if __name__ == '__main__':
    with open('hashes.pickle', 'rb') as handle:
        data = pickle.load(handle)
    
    # To add
    expanded_lines: List[str] = []

    # If I manually paste stuff in it's utf-8 if it's pipe it's utf-16,
    # just try both if one fails
    try:
        with open('tmp.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open('tmp.txt', 'r', encoding='utf-16') as f:
            lines = f.readlines()

    for line in lines:
        if ',' not in line:
            continue
        a = line.strip().split(',', 1)
        hash = a[0].strip()
        if '.' in hash:
            hash = hash[:-5]
        file = a[1].strip()
        expanded_lines.append(hash + ', ' + file)
        alt_paths = find_alternate_paths(file)
        for hash in alt_paths:
            if hash in data and not data[hash]['correct_name']:
                expanded_lines.append(hash + ', ' + alt_paths[hash])
                print(hash + ', ' + alt_paths[hash])

    expanded_lines = sorted(list(set(expanded_lines)), key=lambda x: x.split(', ', 1)[1])

    with open('tmp2.txt', 'w') as f:
        for line in expanded_lines:
            f.write(line + '\n')