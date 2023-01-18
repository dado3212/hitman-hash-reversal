
import re, json
from typing import Dict
from utils import load_data, extract_strings_from_json

data = load_data()
print('loaded')

# type: {
#   hash: [strings]
# }
assembly_strings: Dict[str, Dict[str, set[str]]] = {}

for hash in data:
            # # There are comments inline, which will cause the parser to choke unless they're removed
            # json_data = json.loads(re.sub(r'/\*.*?\*/', '', hex, flags=re.S))
            # json_strings = [x.lower() for x in extract_strings_from_json(json_data)]
            # json_strings = [x for x in json_strings if 'assembly' in x]
            # if len(json_strings) > 0:
            #     if data[hash]['type'] not in assembly_strings:
            #         assembly_strings[data[hash]['type']] = {}
            #     assembly_strings[data[hash]['type']][hash] = json_strings
    # Extract from everything else
    if len(data[hash]['hex_strings']) > 0:
        filtered = [x.lower() for x in data[hash]['hex_strings'] if 'assembly' in x.lower()]
        if len(filtered) > 0:
            if data[hash]['type'] not in assembly_strings:
                assembly_strings[data[hash]['type']] = {}
            found: set[str] = set()
            for f in filtered:
                # Try and handle JSON
                try:
                    json_data = json.loads(re.sub(r'/\*.*?\*/', '', f, flags=re.S))
                    json_strings = [x.lower() for x in extract_strings_from_json(json_data)]
                    json_strings = [x for x in json_strings if 'assembly' in x]
                    found = found.union(json_strings)
                except:
                    found.add(f)
            # Add it to the list
            assembly_strings[data[hash]['type']][hash] = found

unique_extensions: set[str] = set()
for type in assembly_strings:
    for hash in assembly_strings[type]:
        for assembly_path in assembly_strings[type][hash]:
            if '.' in assembly_path:
                unique_extensions.add(assembly_path.split('.')[-1])
            else:
                unique_extensions.add('-1beals-1')
print(unique_extensions)

    # if type != 'FXAS' and type != 'ECPB':
    #     print(type)
    #     print(len(assembly_strings[type]))
    #     for string in assembly_strings[type]:
    #         print(string)
    #     print(assembly_strings[type])
