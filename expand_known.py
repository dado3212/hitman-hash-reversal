from utils import ioi_string_to_hex
import pickle
from typing import List

replacements = [
    (('.pc_tex', 'TEXT'), ('.pc_mipblock1', 'TEXD')),
    (('.prim].pc_prim', 'PRIM'), ('.prim].pc_entitytype', 'TEMP')),
    (('.prim].pc_prim', 'PRIM'), ('.linkedprim].pc_bonerig', 'BORG')),
    (('.prim].pc_prim', 'PRIM'), ('.linkedprim].pc_coll', 'ALOC')),
    (('.prim].pc_prim', 'PRIM'), ('.linkedprim].pc_entitytype', 'TEMP')),
    (('.prim].pc_prim', 'PRIM'), ('.linkedprim].pc_linkedprim', 'PRIM')),
    (('.pc_entitytype', 'ZZZZ'), ('.pc_entityblueprint', 'ZZZZ')),
    (('.pc_entitytemplate', 'ZZZZ'), ('.pc_entityblueprint', 'ZZZZ')),
]

def find_alternate_paths(file: str) -> dict[str, str]:
    alt_paths: dict[str, str] = dict()
    for replacement in replacements:
        if file.endswith(replacement[0][0]):
            new_file = file.removesuffix(replacement[0][0]) + replacement[1][0]
            new_hash = ioi_string_to_hex(new_file)
            new_name = new_hash + '.' + replacement[1][1]
            alt_paths[new_name] = new_file
        if file.endswith(replacement[1][0]):
            new_file = file.removesuffix(replacement[1][0]) + replacement[0][0]
            new_hash = ioi_string_to_hex(new_file)
            new_name = new_hash + '.' + replacement[0][1]
            alt_paths[new_name] = new_file
    return alt_paths

if __name__ == '__main__':
    with open('hashes.pickle', 'rb') as handle:
        data = pickle.load(handle)
    
    # To add
    expanded_lines: List[str] = []
    with open('tmp.txt', 'r', encoding='utf-16') as f:
        lines = f.readlines()
        for line in lines:
            a = line.strip().split(',', 1)
            hash = a[0].strip()
            if '.' in hash:
                hash = hash[:-5]
            file = a[1].strip()
            expanded_lines.append(hash + ', ' + file)
            alt_paths = find_alternate_paths(file)
            for hash in alt_paths:
                if hash in data and len(data[hash]['name']) == 0:
                    expanded_lines.append(hash + ', ' + alt_paths[hash])

    expanded_lines = list(set(expanded_lines))

    with open('tmp2.txt', 'w') as f:
        for line in expanded_lines:
            f.write(line + '\n')