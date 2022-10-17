from utils import ioi_string_to_hex
import pickle
from typing import List

replacements = [
    (('.pc_tex', 'TEXT'), ('.pc_mpblock1', 'TEXD')),

]

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

            for replacement in replacements:
                if file.endswith(replacement[0][0]):
                    new_file = file.removesuffix(replacement[0][0]) + replacement[1][0]
                    new_hash = ioi_string_to_hex(new_file)
                    new_name = new_hash + '.' + replacement[1][1]
                    if new_name in data and len(data[new_name]['name']) == 0:
                        expanded_lines.append(new_hash + ', ' + new_file)
                if file.endswith(replacement[1][0]):
                    new_file = file.removesuffix(replacement[1][0]) + replacement[0][0]
                    new_hash = ioi_string_to_hex(new_file)
                    new_name = new_hash + '.' + replacement[0][1]
                    if new_name in data and len(data[new_name]['name']) == 0:
                        expanded_lines.append(new_hash + ', ' + new_file)

            # '.prim].pc_prim > .prim].pc_entitytype (TEMP)
            # .pc_entitytype > .pc_entityblueprint
            # .pc_entitytemplate > .pc_entityblueprint
            # .prim].pc_prim > .linkedprim].pc_bonerig (BORG)
            # .prim].pc_prim > .linkedprim].pc_coll (ALOC)
            # > .linkedprim].pc_entitytype (TEMP)
            # > .linkedprim].pc_linkedprim (PRIM)
            # pc_coll 
            # pc_bonerig (BORG)
            # .pc_entitytype -> pc_entityblueprint

    expanded_lines = list(set(expanded_lines))

    with open('tmp2.txt', 'w') as f:
        for line in expanded_lines:
            f.write(line + '\n')