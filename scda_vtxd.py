import re, json
from typing import List, Iterable
from utils import ioi_string_to_hex, load_data, hashcat, extract_strings_from_json

data = load_data()

print('loaded data')

def extract_from_hex_strings():
    known_names: dict[str, str] = {}
    with open('hash_list.txt', 'r') as f:
        # completion
        f.readline()
        # hashes count
        f.readline()
        # version number
        f.readline()

        for line in f.readlines():
            split = line.split(',', 1)
            ioi_string = split[1].rstrip()
            hash = split[0][:-5]
            if ioi_string != '' and 'assembly:' in ioi_string:
                known_names[ioi_string] = hash

    print('loaded hash list known names')

    assembly_strings: dict[str, dict[str, set[str]]] = {}
    total_count = 0
    for hash in data:
        if len(data[hash]['hex_strings']) > 0:
            filtered = [x.lower() for x in data[hash]['hex_strings'] if 'assembly:' in x.lower()]
            if len(filtered) > 0:
                if data[hash]['type'] not in assembly_strings:
                    assembly_strings[data[hash]['type']] = {}
                found: set[str] = set()
                for f in filtered:
                    # Try and handle JSON
                    try:
                        # There are comments inline, which will cause the parser to choke unless they're removed
                        json_data = json.loads(re.sub(r'/\*.*?\*/', '', f, flags=re.S))
                        json_strings = [x.lower() for x in extract_strings_from_json(json_data)]
                        json_strings = [x for x in json_strings if 'assembly:' in x]
                        found = found.union(json_strings)
                    except:
                        found.add(f)
                # Add it to the list
                assembly_strings[data[hash]['type']][hash] = found
                total_count += len(found)

    print(f'Found {total_count} assembly strings')

    known_scda: set[str] = set()
    known_vtxd: set[str] = set()

    missing: set[str] = set()
    for type in assembly_strings:
        for hash in assembly_strings[type]:
            for string in assembly_strings[type][hash]:
                if '].pc_' in string:
                    if string not in known_names:
                        missing.add(string)
                elif string.endswith('.mi'):
                    full_path = f'[{string}].pc_mi'
                    if full_path not in known_names:
                        missing.add(full_path)
                elif string.endswith('.json'):
                    full_path = string.removesuffix('.json') + '.pc_json'
                    if full_path not in known_names:
                        missing.add(full_path)
                elif string.endswith('.entitytemplate'):
                    full_path = string.removesuffix('.entitytemplate') + '.pc_entitytemplate'
                    if full_path not in known_names:
                        missing.add(full_path)
                elif string.endswith('.sweetline'):
                    full_path = string.removesuffix('.sweetline') + '.pc_sweetline'
                    if full_path not in known_names:
                        missing.add(full_path)
                elif string.endswith('.brick'):
                    full_path = f'[{string}].pc_entityblueprint'
                    if full_path not in known_names:
                        missing.add(full_path)
                elif string.endswith('.entity'):
                    full_path = f'[{string}].pc_entitytemplate'
                    if full_path not in known_names:
                        missing.add(full_path)
                elif string.endswith('.vertexpaint].vertexpaint'):
                    full_path = string.removesuffix('.vertexpaint].vertexpaint') + '.vertexdata].pc_vertexdata'
                    if full_path not in known_names:
                        missing.add(full_path)
                    else:
                        known_vtxd.add(full_path)
                elif string.endswith('.scattermap].scattermap'):
                    full_path = string.removesuffix('.scattermap].scattermap') + '.scatterdata].pc_scatterdata'
                    if full_path not in known_names:
                        missing.add(full_path)
                    else:
                        known_scda.add(full_path)
                else:
                    print(hash)
                    print(string)

    for expected_path in missing:
        hash = ioi_string_to_hex(expected_path)
        if hash in data and not data[hash]['correct_name']:
            print(hash + '.' + data[hash]['type'] + ', ' + expected_path)

    with open('expected_but_missing.txt', 'w') as f:
        for expected_path in missing:
            f.write(expected_path + '\n')

    for hash in data:
        if data[hash]['type'] == 'SCDA' and data[hash]['correct_name']:
            if data[hash]['name'] not in known_scda:
                print(hash + ', ' + data[hash]['name'])
        if data[hash]['type'] == 'VTXD' and data[hash]['correct_name']:
            if data[hash]['name'] not in known_vtxd:
                print(hash + ', ' + data[hash]['name'])

# Found nothing
def guess_weird_suffixes():
    bases: set[str] = set()
    for hash in data:
        if data[hash]['type'] == 'TEMP' and data[hash]['correct_name'] and '.brick' in data[hash]['name']:
            # [assembly:/_pro/scenes/missions/paris/location.brick].pc_entitytype
            pieces = re.search(r"^\[assembly:/(.*\/[^\/]*).brick].pc_entitytype$", data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue
            bases.add(f'[assembly:/runtimeresources/scatter/{pieces.group(1)}/')

    suffixes: List[str] = []

    for letter in 'abcdefghijklmnopqrstuvwxyz':
        for number1 in range(10):
            for number2 in range(10):
                for number3 in range(10):
                    suffixes.append(f'{letter}_{number1}{number2}_{number3}')

    hashcat('SCDA', bases, set(suffixes), ['', 'scattercontainer_', '.scatterdata].pc_scatterdata'], data)

guess_weird_suffixes()