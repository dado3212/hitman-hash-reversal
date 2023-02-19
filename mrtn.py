from utils import ioi_string_to_hex, load_data, hashcat
import pickle
import re
from typing import List, Optional, Tuple

'''
Q. Do any of them have altenterexit?
A. Just that one!
[hash for hash in data if data[hash]['type'] == 'MRTN' and any([x for x in data[hash]['hex_strings'] if 'altenterexit' in x.lower()])]
# 002DB94AA986D1EF

[(data[hash]['name'], data[hash]['hex_strings'], hash) for hash in data if data[hash]['correct_name'] and data[hash]['type'] == 'MRTN' and any([x for x in data[hash]['hex_strings'] if 'hm_disguise' in x.lower()])]


'''

data = load_data()

def attempt_one():
    # Open the prefixes
    with open('mrtn_folders.pickle', 'rb') as handle:
        mrtn_folders: set[str] = set(pickle.load(handle))

    for folder in list(mrtn_folders):
        mrtn_folders.add(folder.replace('hitman01', 'hitman02'))
        mrtn_folders.add(folder.replace('hitman01', 'hitman03'))

    all_folders: set[str] = set()
    for folder in mrtn_folders:
        all_folders.add(folder)
        all_folders.add(folder + 'mr_')

    mrtn_strings: set[str] = set()

    for hash in data:
        if data[hash]['type'] == 'MRTN':
            for hex_string in data[hash]['hex_strings']:
                mrtn_strings.add(hex_string.lower())

    found = hashcat('MRTN', all_folders, mrtn_strings,
                    ['', '', '.aln].pc_rtn'])
    for hash in found:
        print(hash + '.' + data[hash]['type'] + ', ' + found[hash])


'''
Things that this fails on:
- 00CEC267BD1B5133 (too many strings)
- 00D48551E6479601 (HM_Interact_Place_Sneak_60cm and HM_Interact_DumbWaiter_Mid_Put_Take) -> hm_interact_placement
  - 00EC06ECA85A09B8
- 00942EC0A63F14DF (too many strings, but maybe a shared one?)
- 007584610AE12FE5 (Sick_Sit_To_Stand_Sick_Bench) -> mr_sit_bench_poison_sick
Returns a tuple of the guessed base name, and its confidence level.
0 - strong confidence
1 - there were multiple, but they have the same prefix, so should be right
2 - split strong confidence (this should be combined with 3, TODO)
3 - this one was the prefix for multiple...but who knows
4 - only one potential. this is really at the level of 1b
'''
def guess_mrtn_name(hash: str) -> List[Tuple[str, int]]:
    # Load its hex strings
    assert hash in data

    likely_names: set[str] = set()
    potential_names: set[str] = set()
    for hex_string in data[hash]['hex_strings']:
        hex_string = hex_string.lower()
        if (hex_string.startswith('mr_') or
            hex_string.startswith('hm_') or
            hex_string.startswith('fh_') or
            hex_string.startswith('fr_')):
            likely_names.add(hex_string)

        if hex_string not in ['ioivariation1', '__network__']:
            potential_names.add(hex_string)

    if len(likely_names) == 1:
        return [(likely_names.pop(), 0)]
    elif len(likely_names) > 1:
        # check if they one of them is just the other with a suffix
        # if so, we can just return that one (though with lower confidence)
        filtered_likely: set[str] = set()
        filtered_unlikely: set[str] = set()
        for likely in likely_names:
            all_found = True
            multiFound = 0
            for likely_2 in likely_names:
                if not likely_2.startswith(likely):
                    all_found = False
                else:
                    multiFound += 1
            if all_found:
                filtered_likely.add(likely)
            elif multiFound >= 2:
                filtered_unlikely.add(likely)
        if len(filtered_likely) == 1:
            return [(filtered_likely.pop(), 1)]
        elif len(filtered_likely) == 0 and len(filtered_unlikely) == 1:
            # Even LESS likely
            # Ex. 00F3D1A4356768BC
            return [(filtered_unlikely.pop(), 3)]
        return [(h, 2) for h in filtered_likely]
    else:
        if len(potential_names) == 1:
            # Example is 00E0560CEEE1C676
            return [('mr_' + potential_names.pop(), 4)]
    return []

def loose_expand(orig_guesses: List[Tuple[str, int]]) -> set[str]:
    looser_guesses: set[str] = set()
    for guess in orig_guesses:
        guess = guess[0]
        looser_guesses.add(guess)
        # Try some very specific stuff
        # '0072098A65C7CB9D', # mr_act_death_sit_table_02 -> knockdown_sittable_poison_02
        # '0064BE8B37D50B17', # mr_act_death_sit_table -> knockdown_sittable_poison_01
        # '00C0A8E790CA6207', # mr_act_death_sit_bench_02 -> knockdown_sitbench_poison_02
        if guess.startswith('mr_act_'):
            looser_guesses.add(guess.removeprefix('mr_act_'))
            # Try death stuff
            if 'death' in guess:
                knockdown_version = guess.removeprefix('mr_act_').replace('death', 'knockdown').replace('sit_', 'sit')
                looser_guesses.add(knockdown_version)
                looser_guesses.add(f'{knockdown_version}_poison_01')
                if knockdown_version.endswith('_02'):
                    looser_guesses.add(f'{knockdown_version[:-3]}_poison_02')
    return looser_guesses

# attempt_one()
# with open('hitman_wordlist.txt', 'r') as f:
#     words = [x.strip() for x in f.readlines()]

# words = set(words)
# possible_hex: set[str] = set()
# for hash in data:
#     if data[hash]['type'] == 'MRTN' and not data[hash]['correct_name']:
#         for hex_string in data[hash]['hex_strings']:
#             hex_string = hex_string.lower()
#             # Can also do s03
#             # if not hex_string.startswith('mr_'):
#             #     continue
#             possible_hex.add(hex_string)

# # solved = hashcat('MRTN', words, possible_hex, ['[assembly:/animationnetworks/actors/acts/generic/', '/', '.aln].pc_rtn'], data)
# solved = hashcat('MRTN', words, possible_hex, ['[assembly:/animationnetworks/actors/acts/levels/', '/', '.aln].pc_rtn'], data)
# for hash in solved:
#     print(hash + ', ' + solved[hash])

# print(guess_mrtn_name('00E0560CEEE1C676'))
# exit()

print('Loaded')

known_broken = [
    '00D48551E6479601',
    '00942EC0A63F14DF',
    '00EC06ECA85A09B8',
    '007584610AE12FE5',
    '0056E8A0D2783184', # darksnipersuit_idle
    '0020CB240F4A51DC', # clownsuit_idle (<- you can fix this TODO)
    '002DB94AA986D1EF', # hm_disguise_hips_coffin_altenterexit -> disguisesafezonecoffin_altenterexit
    '008A8778030C24C5', # hm_disguise_hips_coffin -> disguisesafezonecoffin
    '00B3731113F4D6E6', # hm_push_elevator_button -> elevatorpushbutton
    '00027A8D19596880', # hm_weapon_arm_and_grip_poses_1h_remote_detonator_detonate -> hm_remote_activate_detonator
    '00D572BC26F9B5DA', # hm_interact_vial_bottle_100cm_1 -> hm_interact_vialknife_bottle_100cm
    '00D180C1A5D45737', # hm_interact_vial_bottle_100cm -> hm_interact_vial_food_100cm
    '003A7A583C6DDFFE', # hm_interact_vial_bottle_100cm -> hm_interact_vial_glass_100cm
    '009C5F666D1F2403', # mr_stand_sick_throw_up -> mr_stand_sick
    '008EF93363C43FDD', # hm_idle_stand_bat -> baseball_bat_idle
    '00441D3D4B28F351', # hm_interact_vial_bottle_100cm -> hm_interact_vial_glass_120cm
]

for hash in data:
    if data[hash]['type'] == 'MRTN':
        # If the hash has the correct name, we should be able to guess it
        if not data[hash]['correct_name']:
            continue
        if len(data[hash]['hex_strings']) > 70: # really 1000 is a better limit
            # For now, just ignore these
            # Ex. 00CEC267BD1B5133 (TODO: are we extracting everything from here?)
            # Ex. 005C40E612CC9242 (only 72, should we be able to fix this?)
            continue
        names = guess_mrtn_name(hash)
        
        # TODO: Idle should be guessable
        if len(names) == 0 and hash not in known_broken and 'idle' not in data[hash]['name']:
            print(hash)
            exit()
        elif hash not in known_broken:
            found = False
            # for each guessed name, it should be in it?
            for f in names:
                if f[0] in data[hash]['name']:
                    found = True
            if not found:
                loose = loose_expand(names)
                looseFound = False
                for l in loose:
                    if l in data[hash]['name']:
                        looseFound = True
                if not looseFound:
                    print('Was wrong.')
                    print(hash)
                    print(data[hash]['name'])
                    print(names)
                    print(loose)
                    exit()

