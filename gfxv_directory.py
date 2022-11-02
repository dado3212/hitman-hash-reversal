import pickle
from typing import List
from utils import ioi_string_to_hex
from build_directory import build_directory, build_paths

directory = build_directory()
paths = build_paths(directory, '[assembly:')
print(len(paths))

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

# Search the directory
for hash in data:
    if data[hash]['type'] == 'GFXV':
        hex_strings = data[hash]['hex_strings']
        if not data[hash]['correct_name']:
            for string in hex_strings:
                if 'usm' in string or 'avi' in string or 'wav' in string:
                    name = string.lower()[:-4].strip(':')
                    # if data[hash]['name'] == '':
                    #     print(hash + ',' + string.lower())
                    names: List[str] = [name]
                    if name.endswith('.fl'):
                        names.append(name[:-3])
                    for name in names:
                        potential_paths: List[str] = []
                        for path in paths:
                            potential_paths.append(f'{path}/videos/{name}.avi].pc_gfxv')
                            potential_paths.append(f'{path}/videos/{name}.usm].pc_gfxv')
                            potential_paths.append(f'{path}/videos/{name}.wav].pc_gfxv')
                            potential_paths.append(f'{path}/video/{name}.avi].pc_gfxv')
                            potential_paths.append(f'{path}/video/{name}.usm].pc_gfxv')
                            potential_paths.append(f'{path}/video/{name}.wav].pc_gfxv')
                        for potential_path in potential_paths:
                            hex = ioi_string_to_hex(potential_path)
                            if hex in data and not data[hex]['correct_name']:
                                print(hex + ',' + potential_path)
