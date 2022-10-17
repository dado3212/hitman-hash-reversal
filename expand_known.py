from utils import ioi_string_to_hex
import pickle
from typing import List

replacements = [
    ('.pc_tex', '.pc_mipblock1'),
    ('.prim].pc_prim', '.prim].pc_entitytype'),
    ('.prim].pc_prim', '.linkedprim].pc_bonerig'),
    ('.prim].pc_prim', '.linkedprim].pc_coll'),
    ('.prim].pc_prim', '.linkedprim].pc_entitytype'),
    ('.prim].pc_prim', '.linkedprim].pc_linkedprim'),
    ('.pc_entitytype', '.pc_entityblueprint'),
    ('.pc_entitytemplate', '.pc_entityblueprint'),
]

def find_alternate_paths(file: str, run_again: bool = True) -> dict[str, str]:
    alt_paths: dict[str, str] = dict()
    for replacement in replacements:
        if file.endswith(replacement[0]):
            new_file = file.removesuffix(replacement[0]) + replacement[1]
            new_hash = ioi_string_to_hex(new_file)
            alt_paths[new_hash] = new_file
        if file.endswith(replacement[1]):
            new_file = file.removesuffix(replacement[1]) + replacement[0]
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
            print(alt_paths)
            for hash in alt_paths:
                if hash in data and not data[hash]['correct_name']:
                    expanded_lines.append(hash + ', ' + alt_paths[hash])

    expanded_lines = list(set(expanded_lines))

    with open('tmp2.txt', 'w') as f:
        for line in expanded_lines:
            f.write(line + '\n')