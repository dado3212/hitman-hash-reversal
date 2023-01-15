import re, os
from typing import List, Dict, Iterable
from utils import ioi_string_to_hex, load_data

'''
This is VERY work in progress.

To use this file, you will need to copy the hashcat 6.2.4 build from GitHub
(https://github.com/hashcat/hashcat/releases/tag/v6.2.4) and also download
grappigegovert's patch from https://github.com/grappigegovert/hashcat
(https://cdn.discordapp.com/attachments/815577522958893096/909394928403107961/hashcat_ioihash_fixed.zip).

Move the 6.2.4 folder into this one, and from the patch copy in the files to the
modules and OpenCL folders.

It will generate the files and print out the command you want to use.
After it's finished running
'''
hashcat_path = 'hashcat-6.2.4'

data = load_data()
print('loaded')

# Format that they should be in, with the words being inserted between the entries
format = ['[assembly:/', '.wl2?/', '.prim].pc_prim']
target_type = 'PRIM'
assert len(format) == 3

# Definition to create the two wordlists
prefixes: Iterable[str] = set()
tblu_suffixes: List[List[str]] = []
suffixes: set[str] = set()
for hash in data:
    if data[hash]['type'] == 'MATI' and data[hash]['correct_name']:
        pieces = re.search(r"^\[assembly:/(.*\/)([^\/]*)\.mi.*$", data[hash]['name'], re.IGNORECASE)
        if pieces is None:
            continue
        prefix = pieces.group(1).replace('materials', 'geometry', 1)
        prefixes.add(f'{prefix}{pieces.group(2)}')
        suffixes.add(pieces.group(2))
    if data[hash]['type'] == 'TBLU':
        tblu_suffixes.append([x.lower() for x in data[hash]['hex_strings']])

suffixes = suffixes.union(*tblu_suffixes)

# Save the wordlists and print out the format
### 
### HERE BE DRAGONS, DON'T EDIT
###

possible_hashes = [hash for hash in data if data[hash]['type'] == target_type and not data[hash]['correct_name']]
print(f'Saving wordlists: {len(prefixes)} left, {len(suffixes)} right, targeting {len(possible_hashes)} unknown hashes.')
with open(f'{hashcat_path}/left.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(prefixes))

with open(f'{hashcat_path}/right.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(suffixes))

try:
    os.remove(f'{hashcat_path}/hashes.txt')
except OSError:
    pass

with open(f'{hashcat_path}/hashes.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(possible_hashes))

# Must be before first, after first but before second, and after second
assert len(format) == 3

print(f'cd {hashcat_path}')
output_string = './hashcat.exe -m 92100 -a 1'
left = format[0]
middle = format[1]
right = format[2]
if len(left) > 0 or len(middle) > 0:
    output_string += ' -j \''
    for l in left[::-1]:
        output_string += '^' + l
    for m in middle:
        output_string += '$' + m
    output_string += '\''
if len(right) > 0:
    output_string += ' -k \''
    for r in right:
        output_string += '$' + r
    output_string += '\''

output_string += f' hashes.txt left.txt right.txt --outfile-autohex-disable --status --status-timer=3'
print(output_string)

# ./hashcat.exe -m 92100 --show hashes.txt