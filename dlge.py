import pickle, re, string
from typing import List, Dict, Optional
from utils import ioi_string_to_hex, load_data, hashcat, crack

data = load_data()

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

######## Guess based on SDEF actor names
def approach_one():
    actor_names: set[str] = set()
    action_names: set[str] = set()
    sdef_actor_names: set[str] = set()
    for hash in data:
        if data[hash]['type'] == 'SDEF':
            sdef_actor_name = re.search(r"^\[assembly:/sound/sounddefinitions/(.*).sdefs].pc_sdefs$", data[hash]['name'], re.IGNORECASE)
            if sdef_actor_name is None:
                print('WHOA!', hash)
                exit()
            sdef_actor_names.add(sdef_actor_name.group(1))
            depends = [x for x in data[hash]['depends'] if x in data and data[x]['type'] == 'DLGE' and data[x]['correct_name']]
            names = [data[x]['name'] for x in depends]
            for name in names:
                extract = re.search(r"^\[assembly:/localization/hitman6/conversations/ai/(.*?)/(.*)_\1.sweetdialog].pc_dialogevent$", name, re.IGNORECASE)
                if extract is not None:
                    actor_name = extract.group(1)
                    action_name = extract.group(2)
                    actor_names.add(actor_name)
                    action_names.add(action_name)

    # We're missing these
    print(sdef_actor_names.difference(actor_names))

    # Just brute force the rest
    actor_names = actor_names.union(sdef_actor_names)
    for actor_name in actor_names:
        for action_name in action_names:
            path = f'[assembly:/localization/hitman6/conversations/ai/{actor_name}/{action_name}_{actor_name}.sweetdialog].pc_dialogevent'
            hash = ioi_string_to_hex(path)
            if hash in data and not data[hash]['correct_name']:
                data[hash]['name'] = path
                data[hash]['correct_name'] = True
                print(hash + ', ' + path)

    # Try and fill in some blanks with best guesses
    # for hash in data:
    #     if data[hash]['type'] == 'DLGE' and data[hash]['name'] == '':
    #         guesses: set[str] = set()
    #         for dependency in data[hash]['depends']:
    #             if dependency in data and data[dependency]['type'] == 'WWES' and data[dependency]['correct_name']:
    #                 raw_guessed_name = re.search(r"^\[assembly:/sound/wwise/originals/voices/english\(us\)\/(.*)\.wav.*$", data[dependency]['name'], re.IGNORECASE)
    #                 if raw_guessed_name is None:
    #                     continue
    #                 guessed_name = raw_guessed_name.group(1)
    #                 pieces = guessed_name.split('/')
    #                 last = pieces[-1].split('_')
    #                 core_bit = '/'.join(pieces[:-1]) + '/' + '_'.join(last[0:-1])
    #                 guesses.add(f'[unknown:/*/{core_bit}.dlge].pc_dlge')
    #         if len(guesses) == 1:
    #             print(hash + ', ' + list(guesses)[0])
    #         else:
    #             print(guesses)

# SDEF -> DLGE
# actor names but modified? Not sure how
def approach_two():
    # Extract all of the SDEF actor names
    sdef_actor_names: set[str] = set()
    for hash in data:
        if data[hash]['type'] == 'SDEF':
            sdef_actor_name = re.search(r"^\[assembly:/sound/sounddefinitions/(.*).sdefs].pc_sdefs$", data[hash]['name'], re.IGNORECASE)
            if sdef_actor_name is None:
                print('WHOA!', hash)
                exit()
            sdef_actor_names.add(sdef_actor_name.group(1))

    # Try and futz some of the SDEF actor names
    futzed_names: set[str] = set()
    for actor_name in sdef_actor_names:
        regexes = [
            r"^(.*)_[mf]hi\d+$",
            r"^(.*)_[mf]0\d+$",
            r"^(.*)[mf]0\d+$",
            r"^(.*)0\d+$",
            r"^(.*)fch\d+$",
            r"^(.*)fhi\d+$",
            r"^(.*)hi\d+$"
        ]
        for regex in regexes:
            base_actor_name = re.search(regex, actor_name, re.IGNORECASE)
            if base_actor_name is not None:
                futzed_names.add(base_actor_name.group(1).rstrip('_'))
    sdef_actor_names = sdef_actor_names.union(futzed_names)

    # Load every single correct DLGE name
    parts: List[List[str]] = []
    for hash in data:
        if data[hash]['type'] == 'DLGE' and data[hash]['correct_name']:
            for actor_name in sdef_actor_names:
                if actor_name in data[hash]['name']:
                    split = data[hash]['name'].split(actor_name)
                    parts.append(split)
    
    # For each of those parts, rebuild it with a new name
    new_hashes: Dict[str, str] = dict()
    for part in parts:
        for actor_name in sdef_actor_names:
            new_path = actor_name.join(part)
            hash = ioi_string_to_hex(new_path)
            if hash in data and not data[hash]['correct_name'] and hash not in new_hashes:
                print(hash + ', ' + new_path)
                new_hashes[hash] = new_path

def approach_basic():
    # I think this is different because sometimes the dependency structure
    # is wrong?

    # for hash in data:
    #     if data[hash]['type'] == 'DLGE':
    #         if not data[hash]['correct_name']:
    #             path = guess(hash)
    #             if path is not None:
    #                 print(hash + ', ' + path)

    found: Dict[str, str] = dict()
    for hash in data:
        if data[hash]['type'] == 'WWES' and hash == '008ABE28340A0AE5':
            # try and guess from
            # [assembly:/sound/wwise/originals/voices/english(us)/evergreen/handler/ed060_clbrtcmpnmegawinpost_diana_004.wav].pc_wes
            # 00AEC061AB63C8F3.DLGE,[assembly:/localization/hitman6/conversations/evergreen/handler/ed060_clbrtcmpnmegawinpost.sweetdialog].pc_dialogevent
            # Get all of the WWES dependencies
            wwes = re.search(r"^\[assembly:/sound/wwise/originals/voices/english\(us\)/(.*)/(.*)\.wav\].pc_wes$", data[hash]['name'], re.IGNORECASE)
            if wwes is None:
                print(data[hash]['name']  + ' does not match')
                continue
            suffix_chunks = wwes.group(2).split('_')
            for i in range(1, len(suffix_chunks)+1):
                suffix = '_'.join(suffix_chunks[:i])
                possible_path = f'[assembly:/localization/hitman6/conversations/{wwes.group(1)}/{suffix}.sweetdialog].pc_dialogevent'
                possible_hash = ioi_string_to_hex(possible_path)
                if possible_hash in data and possible_hash not in found: # and not data[possible_hash]['correct_name']:
                    print(possible_hash + ', ' + possible_path)
                    found[possible_hash] = possible_path
                    continue

# When a new update comes out
# approach_basic()
# approach_one()
# approach_two()

# Noodling
# which of them do we have, but don't match the pattern?
def missing_pattern():
    for hash in data:
        if data[hash]['type'] == 'DLGE' and data[hash]['correct_name']:
            if guess(hash) is None:
                print(hash + ', ' + data[hash]['name'])

crack('0058E57C6A9F3CE8',
    '[assembly:/localization/hitman6/conversations/marrakech/16000_ambience/',
    '.sweetdialog].pc_dialogevent',
    ['dr16010', 'cafecouchconv','cafe','couch','conv','richmale','rich','male','0','1','2','3','4'],
    [],
    1,
    8)

# [hash for hash in data if data[hash]['type'] not in ['WWES', 'FXAS'] and data[hash]['correct_name'] and 'gen_grt47' in data[hash]['name']]
