import re
from typing import List, Iterable
from utils import ioi_string_to_hex, load_data, hashcat

data = load_data()

print('loaded')

'''
Some helper commands to answer basic questions:

Q. Do all PRIMs's have a MATI dependency.
A. No. 20 do not. They depend on unknown hashes though, which we can't do much about.
[hash for hash in data if data[hash]['type'] == 'PRIM' and not any([x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'MATI'])]

Q. Do all PRIMs have a reverse dependency TEMP?
A. Nope. 13 do not. Most are light gizmo's, and then there's 00A2A8F4A90A06C2.
[(hash, data[hash]['name']) for hash in data if data[hash]['type'] == 'PRIM' and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'TEMP']))]

Q. Do all PRIMs have a named reverse dependency TEMP have a name?
A. Yes (as long as you filter to the right type).
[hash for hash in data if data[hash]['type'] == 'PRIM' and not data[hash]['correct_name'] and any([x for x in reverse[hash] if x in data and data[x]['type'] == 'TEMP' and data[x]['correct_name'] and 'geometry' in data[x]['name']])]
'''

# with open('reverse.pickle', 'rb') as handle:
#     reverse: Dict[str, str] = pickle.load(handle)

# Try and pull them from TEXT/TEXD files for linkedprim
def pull_from_textd():
    potential: set[str] = set()

    for hash in data:
        if data[hash]['correct_name'] and (data[hash]['type'] == 'TEXT' or data[hash]['type'] == 'TEXD'):
            # [assembly:/_pro/items/textures/firearms/frames/sniper_jaeger_envy_a/sniper_jaeger_envy_stock_a.texture?/normal_a.tex](asnormalmap).pc_mipblock1
            # [assembly:/_pro/items/geometry/firearms/frames/sniper_jaeger_envy_a/sniper_jaeger_envy_stock_a.wl2?/sniper_jaeger_envy_stock_a.linkedprim](bodypart).pc_linkedprim
            pieces = re.search(r"^\[assembly:/(.*\/)([^\/]*)\.texture.*$", data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue
            prefix = pieces.group(1).replace('textures', 'geometry', 1)
            potential.add(f'[assembly:/{prefix}{pieces.group(2)}.wl2?/{pieces.group(2)}.linkedprim](bodypart).pc_linkedprim')
            potential.add(f'[assembly:/{prefix}{pieces.group(2)}.wl2?/{pieces.group(2)}.linkedprim].pc_linkedprim')

    for path_name in potential:
        path_hash = ioi_string_to_hex(path_name)
        if path_hash in data and not data[path_hash]['correct_name']:
            print(path_hash + ', ' + path_name)

def extract_from_dependent_mati():
    for hash in data:
        if data[hash]['type'] == 'PRIM' and not data[hash]['correct_name']:
            for depends in data[hash]['depends']:
                if depends in data and data[depends]['type'] == 'MATI' and data[depends]['correct_name']:
                    # Get the name and see if we can build the PRIM from it
                    pieces = re.search(r"^\[assembly:/(.*\/)([^\/]*)\.mi.*$", data[depends]['name'], re.IGNORECASE)
                    if pieces is None:
                        continue
                    prefix = pieces.group(1).replace('materials', 'geometry', 1)
                    path_name = f'[assembly:/{prefix}{pieces.group(2)}.wl2?/{pieces.group(2)}.prim].pc_prim'
                    path_hash = ioi_string_to_hex(path_name)
                    if path_hash in data and not data[path_hash]['correct_name']:
                        print(path_hash + ', ' + path_name)

# Credit to Notex for guessing this pattern
def broadly_guess_from_tblu_prefix_synthesis():
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
        if data[hash]['type'] == 'TEMP' and data[hash]['correct_name']:
            pieces = re.search(r"^\[assembly:/(.*\/)([^\/]*)\.template.*$", data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue
            prefix = pieces.group(1).replace('templates', 'geometry', 1)
            prefixes.add(f'{prefix}{pieces.group(2)}')
        if data[hash]['type'] == 'TBLU':
            if data[hash]['correct_name']:
                pieces = re.search(r"^\[assembly:/(.*\/)([^\/]*)\.template.*$", data[hash]['name'], re.IGNORECASE)
                if pieces is None:
                    continue
                prefix = pieces.group(1).replace('templates', 'geometry', 1)
                prefixes.add(f'{prefix}{pieces.group(2)}')

            tblu_suffixes.append([x.lower() for x in data[hash]['hex_strings']])
            tblu_suffixes.append(['_'.join(x.lower().split('_')[:-1]) for x in data[hash]['hex_strings'] if '_' in x])

    suffixes = suffixes.union(*tblu_suffixes)

    hashes = hashcat('PRIM', prefixes, suffixes, ['[assembly:/', '.wl2?/', '.prim].pc_prim'], data)
    for hash in hashes:
        print(hash + ', ' + hashes[hash])

# Inspired by:
# [assembly:/_pro/characters/assets/individuals/fox/clubsecpick/geometry/male_reg_clubsecpick.wl2?/clubsecpick_torso.weightedprim](bodypart).pc_weightedprim
def find_unique_bodyparts():
    for hash in data:
        if data[hash]['type'] == 'TEMP' and data[hash]['correct_name'] and 'unique' in data[hash]['name']:
            pieces = re.search(r"^\[assembly:/_pro/characters/templates/(.*?)/(.*?).template\?/(.*?).entitytemplate\].pc_entitytemplate$", data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue

            # Let's just guess the name
            split = re.search(r".*unique_(.*?)(_[mf][_$]|$).*", pieces.group(3))
            if split is None:
                # print(hash + ', ' + data[hash]['name'])
                # 001392EB9BD9FE6E, [assembly:/_pro/characters/templates/colorado/char_colorado_guards.template?/outfit_militiabasic_m_actor_v10.entitytemplate].pc_entitytemplate
                continue
            type = split.group(1)
            prefix = ''
            if split.group(2) == '_m_':
                prefix = 'male_reg_'
            elif split.group(2) == '_f_':
                prefix = 'female_reg_'
            start = '[assembly:/_pro/characters/assets/individuals/' + pieces.group(1) + '/' + type + '/geometry/' + prefix + type + '.wl2?/' + type + '_'

            # Calculated from:
            # sorted(set([re.search(r".*_(.*?).wl2\?\/\1_(.*).weightedprim\]\(bodypart\).*", data[hash]['name']).group(2) for hash in data if data[hash]['type'] == 'PRIM' and re.match(r".*_(.*?).wl2\?\/\1_.*.weightedprim\]\(bodypart\).*", data[hash]['name']) is not None]))
            bodyparts = ['accesories', 'accessories', 'apron', 'belt', 'coat', 'dress', 'earpiece', 'gloves', 'hair', 'hairhat', 'hands', 'hat', 'head', 'jacket', 'pants', 'sashbanner', 'scarf', 'shirt', 'shoes', 'sweater', 'tanktop', 'tie', 'tights', 'torso', 'vest']
            for bodypart in bodyparts:
                name = start + bodypart + '.weightedprim](bodypart).pc_weightedprim'
                possible_hash = ioi_string_to_hex(name)
                if possible_hash in data and not data[possible_hash]['correct_name']:
                    print(possible_hash + ', ' + name)


# Main thing
# broadly_guess_from_tblu_prefix_synthesis()

# Idle speculation
