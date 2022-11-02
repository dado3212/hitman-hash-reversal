import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex

COUNT_KEY = '~'

# print the actual directory
def print_directory(current_dict, padding = ""):
    for key in current_dict:
        if key[0] == '~':
            print(padding + f'\x1b[48;2;{130};{40};{40}m {key[1:]} {current_dict[key]} \x1b[0m')
        else:
            print(padding + key)
            print_directory(current_dict[key], padding + "  ")

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

directory: Dict[str, Any] = {}
j = 0
for hash in data:
    if data[hash]['correct_name']:
        # 00AC02DBC8446FD5
        sections = data[hash]['name'].split('/')[1:]
        current = directory
        for section in sections:
            if '.' in section:
                key = '~' + data[hash]['type']
                if key in current:
                    current[key] += 1
                else:
                    current[key] = 1
                break
            if section not in current:
                current[section] = {}
            current = current[section]

# Build a list of all paths
def build_paths(current_dict, prefix):
    paths = set([])
    for key in current_dict:
        if key[0] != '~':
            path = f'{prefix}/{key}'
            paths.add(path)
            paths = paths.union(build_paths(current_dict[key], path))
    return paths

paths = build_paths(directory, '[assembly:')
print(len(paths))

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
