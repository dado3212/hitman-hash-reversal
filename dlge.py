import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

def guess_expansions(path: str) -> set[str]:
    paths: set[str] = set()
    paths.add(path)
    match = re.search(r"^(\[assembly:/localization/hitman6/conversations/.*?\/(\d{4,})_.*?)\/(.*.sweetdialog].pc_dialogevent)$", path, re.IGNORECASE)
    if match is None:
        return paths
    # [assembly:/localization/hitman6/conversations/mumbai/25000_mongoose
    start = match.group(1)
    # 2500
    int_prefix = match.group(2)
    # 25000_story/dr25363_laundry_47foremantakeabreakrandom.sweetdialog].pc_dialogeven
    suffix = match.group(3)
    if suffix.startswith(int_prefix):
        new_ending = '/'.join(suffix.split('/')[1:])
        paths.add(f'{start}/{int_prefix}_story/{new_ending}')
        paths.add(f'{start}/{int_prefix}_ambient/{new_ending}')
        paths.add(f'{start}/{int_prefix}_ambience/{new_ending}')
        paths.add(f'{start}/{int_prefix}_handler/{new_ending}')
        paths.add(f'{start}/{int_prefix}_elusive/{new_ending}')
        paths.add(f'{start}/{new_ending}')
    else:
        paths.add(f'{start}/{int_prefix}_story/{suffix}')
        paths.add(f'{start}/{int_prefix}_ambient/{suffix}')
        paths.add(f'{start}/{int_prefix}_ambience/{suffix}')
        paths.add(f'{start}/{int_prefix}_handler/{suffix}')
        paths.add(f'{start}/{int_prefix}_elusive/{suffix}')
    return paths

def guess(hash: str) -> Optional[str]:
    for dependency in data[hash]['depends']:
        if dependency in data and data[dependency]['type'] == 'WWES' and data[dependency]['correct_name']:
            raw_guessed_name = re.search(r"^\[assembly:/sound/wwise/originals/voices/english\(us\)\/(.*)\.wav.*$", data[dependency]['name'], re.IGNORECASE)
            if raw_guessed_name is None:
                continue
            guessed_name = raw_guessed_name.group(1)
            pieces = guessed_name.split('/')
            last = pieces[-1].split('_')
            for i in range(1, len(last)+1):
                core_bit = '/'.join(pieces[:-1]) + '/' + '_'.join(last[0:i])
                possible_paths = guess_expansions(f'[assembly:/localization/hitman6/conversations/{core_bit}.sweetdialog].pc_dialogevent')
                for path in possible_paths:
                    possible_hash = ioi_string_to_hex(path)
                    if possible_hash == hash:
                        return path
    return None

print('Loaded')
####### Trivial expansion
# for hash in data:
#     if data[hash]['type'] == 'DLGE':
#         if not data[hash]['correct_name']:
#             path = guess(hash)
#             if path is not None:
#                 print(hash + ', ' + path)

###### Try and just guess any remaining female foley sounds
# with open('wordlist_1.txt', 'r') as f:
#     words = [x.strip() for x in f.readlines()]

# for word in words:
#     path = f'[assembly:/localization/hitman6/conversations/ai/fol_fem/exp_{word}_fol_fem.sweetdialog].pc_dialogevent'
#     hash = ioi_string_to_hex(path)
#     if hash in data and not data[hash]['correct_name']:
#         print(hash + ', ' + path)


######## Guess based on SDEF
# actor_names: set[str] = set()
# action_names: set[str] = set()
# sdef_actor_names: set[str] = set()
# for hash in data:
#     if data[hash]['type'] == 'SDEF':
#         sdef_actor_name = re.search(r"^\[assembly:/sound/sounddefinitions/(.*).sdefs].pc_sdefs$", data[hash]['name'], re.IGNORECASE)
#         if sdef_actor_name is None:
#             print('WHOA!', hash)
#             exit()
#         sdef_actor_names.add(sdef_actor_name.group(1))
#         depends = [x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'DLGE' and data[x]['correct_name']]
#         names = [data[x]['name'] for x in depends]
#         for name in names:
#             extract = re.search(r"^\[assembly:/localization/hitman6/conversations/ai/(.*?)/(.*)_\1.sweetdialog].pc_dialogevent$", name, re.IGNORECASE)
#             if extract is not None:
#                 actor_name = extract.group(1)
#                 action_name = extract.group(2)
#                 actor_names.add(actor_name)
#                 action_names.add(action_name)

# # We're missing these
# print(sdef_actor_names.difference(actor_names))

# # Just brute force the rest
# actor_names = actor_names.union(sdef_actor_names)
# for actor_name in actor_names:
#     for action_name in action_names:
#         path = f'[assembly:/localization/hitman6/conversations/ai/{actor_name}/{action_name}_{actor_name}.sweetdialog].pc_dialogevent'
#         hash = ioi_string_to_hex(path)
#         if hash in data and not data[hash]['correct_name']:
#             data[hash]['name'] = path
#             data[hash]['correct_name'] = True
#             print(hash + ', ' + path)
