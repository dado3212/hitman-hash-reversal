import re, json
from typing import List, Iterable
from utils import ioi_string_to_hex, load_data, hashcat, extract_strings_from_json

data = load_data()

print('loaded data')

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
            elif string.endswith('.scattermap].scattermap'):
                full_path = string.removesuffix('.scattermap].scattermap') + '.scatterdata].pc_scatterdata'
                if full_path not in known_names:
                    missing.add(full_path)
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

'''
00204D1AFD76AB13
editordropdata: <root type="tarray&lt;zresourceid&gt;" count="1"><i>assembly:/localization/hitman6/conversations/ui/pro/online/repository/actors.sweetmenutext?/eb179158-b383-4dd9-8c8f-1ea421ef459f_fatheradalricocandelaria_description.sweetline</i></root>

assembly_lines_a_decal_onlynormals
'''