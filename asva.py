from utils import ioi_string_to_hex, load_data, hashcat
from typing import Dict, Optional, List, Callable
import pickle, re, string

data = load_data()
print('loaded')

def hashcat_guessing():
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    found: Dict[str, str] = {}
    formats: List[List[str]] = [
        # ['[assembly:/animations/animationdatabases/hm5_animations.aset?/vri_civ_', '_', '.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/actor_reactions.aset?/vri_civ_', '_', '.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/hm5_weapons.aset?/vri_civ_', '_', '.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/hm5_animations.aset?/vri_bodyguard_', '_', '.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/actor_reactions.aset?/vri_bodyguard_', '_', '.asva].pc_asva'],
        # Found nothing
        # ['[assembly:/animations/animationdatabases/actor_reactions.aset?/vri_civ_carry','','.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/hm5_animations.aset?/vri_civ_carry','','.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/actor_reactions.aset?/vri_civ_carry','_','.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/hm5_animations.aset?/vri_civ_carry','_','.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/actor_reactions.aset?/vri_civ_female_carry','_','.asva].pc_asva'],
        # ['[assembly:/animations/animationdatabases/hm5_animations.aset?/vri_civ_female_carry','_','.asva].pc_asva'],
        ['[assembly:/animations/animationdatabases/actor_reactions.aset?/vri_civ_female_carry','','.asva].pc_asva'],
        ['[assembly:/animations/animationdatabases/hm5_animations.aset?/vri_civ_female_carry','','.asva].pc_asva'],
    ]
    for format in formats:
        hashes = hashcat('ASVA', wordlist, wordlist, format, data)
        for hash in hashes:
            found[hash] = hashes[hash]

    for hash in found:
        print(hash + '.ASVA, ' + found[hash])

def smart_guessing():
    with open('reverse.pickle', 'rb') as handle:
        reverse: Dict[str, str] = pickle.load(handle)

    for hash in data:
        if data[hash]['type'] == 'ASVA':
            # [assembly:/animations/animationdatabases/hm5_weapons.aset?/
            # [assembly:/animations/animationdatabases/hm5_animations.aset?/
            # [assembly:/animations/animationdatabases/actor_reactions.aset?/
            options: set[str] = set()
            raw_chunks: set[str] = set()
            if hash in reverse:
                for used in reverse[hash]:
                    match = re.search(r"^\[assembly:/_pro/design/actor/animvariation.template\?/(.*?)\.entitytemplate\].pc_entitytype$", data[used]['name'], re.IGNORECASE)
                    if match is None:
                        # print(hash + ', ' + used + ', ' + data[used]['name'])
                        match = re.search(r"^\[assembly:/_pro/design/gamecore/itemhelpers_grippose.template\?/itemhelpers_grippose_(.*?)\.entitytemplate\].pc_entitytype$", data[used]['name'], re.IGNORECASE)
                        if match is None:
                            # print(hash + ', ' + used + ', ' + data[used]['name'])
                            continue
                    chunk = match.group(1)
                    raw_chunks.add(chunk)
                    changes: List[Callable[[str], str]] = [
                        lambda x: x,
                        lambda x: f'prop_{x}',
                        lambda x: f'prop_1h_{x}',
                        lambda x: x.replace('male_', ''),
                        lambda x: x.replace('vri_', ''),
                        lambda x: x.replace('civ_', 'civ_male_'),
                        lambda x: x.replace('civ_', 'civ_female_'),
                        lambda x: x.replace('civ_', 'civ_model_'),
                        lambda x: x.replace('_s01', ''),
                        lambda x: x.replace('_s02', ''),
                        lambda x: x.replace('_s03', ''),
                        lambda x: x.replace('s01_', ''),
                        lambda x: x.replace('s02_', ''),
                        lambda x: x.replace('s03_', ''),
                        lambda x: x.replace('guard', 'bodyguard'),
                        lambda x: f'vri_{x}',
                        lambda x: f'{name}_s01',
                        lambda x: f'{name}_s02',
                        lambda x: f'{name}_s03',
                        lambda x: f'{name}_01',
                        lambda x: f'{name}_02',
                        lambda x: f'{name}_03',
                        lambda x: f's01_{name}',
                        lambda x: f's02_{name}',
                        lambda x: f's03_{name}',
                        lambda x: f'01_{name}',
                        lambda x: f'02_{name}',
                        lambda x: f'03_{name}',
                        lambda x: f's01_l01_{name}',
                        lambda x: f's02_l02_{name}',
                        lambda x: f's03_l03_{name}',
                        lambda x: '_'.join(x.split('_')[:-1]) + '_carry' + x.split('_')[-1],
                        lambda x: '_'.join(x.split('_')[:-1]) + '1h_' + x.split('_')[-1],
                        lambda x: '_'.join(x.split('_')[:-1]) + '2h_' + x.split('_')[-1],
                        lambda x: '_'.join(x.split('_')[:-2]) + '_' + x.split('_')[-2] + '_' + x.split('_')[-1] if len(x.split('_')) > 2 else x,
                    ]
                    names = set([chunk.removeprefix('animset_')])
                    for i in range(0, 4):
                        for name in list(names)[::]:
                            for change in changes:
                                names.add(change(name))
                    for name in names:
                        options.add(f'[assembly:/animations/animationdatabases/hm5_weapons.aset?/{name}.asva].pc_asva')
                        options.add(f'[assembly:/animations/animationdatabases/hm5_animations.aset?/{name}.asva].pc_asva')
                        options.add(f'[assembly:/animations/animationdatabases/actor_reactions.aset?/{name}.asva].pc_asva')
            found = False
            for option in options:
                possible_hash = ioi_string_to_hex(option)
                if possible_hash == hash:
                    found = True
                    if data[hash]['correct_name']:
                        print('Known: ' + hash + ', ' + option)
                    else:
                        print('New: ' + hash + ', ' + option)
            if not found:
                if data[hash]['correct_name']:
                    print('Missing: ' + hash + ': ' + data[hash]['name'])
                    print(raw_chunks)
                else:
                    print('Unknown: ' + hash)
                    print(raw_chunks)

hashcat_guessing()