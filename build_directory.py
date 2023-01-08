import pickle
from typing import Dict, Any

COUNT_KEY = '~'

# print the actual directory
def print_directory(current_dict: Dict[str, Any], padding: str = ""):
    for key in current_dict:
        if key[0] == '~':
            print(padding + f'\x1b[48;2;{130};{40};{40}m {key[1:]} {current_dict[key]} \x1b[0m')
        else:
            print(padding + key)
            print_directory(current_dict[key], padding + "  ")

def build_directory(filter: str = '') -> Dict[str, Any]:
    with open('hashes.pickle', 'rb') as handle:
        data: Dict[str, Any] = pickle.load(handle)

    directory: Dict[str, Any] = {}
    for hash in data:
        if data[hash]['correct_name'] and filter in data[hash]['type']:
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
    return directory

# Build a list of all paths
def build_paths(current_dict: Dict[str, Any], prefix: str):
    paths = set([])
    for key in current_dict:
        if key[0] != '~':
            path = f'{prefix}/{key}'
            paths.add(path)
            paths = paths.union(build_paths(current_dict[key], path))
    return paths

if __name__ == '__main__':
    directory = build_directory('MRTN')
    paths = build_paths(directory, '[assembly:')
    print(len(paths))
    print_directory(directory)
