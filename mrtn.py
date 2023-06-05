from utils import ioi_string_to_hex, load_data, hashcat, find_folder_patterns
import pickle, re, string
from typing import List, Optional, Tuple, Dict

'''
Q. Do any of them have altenterexit?
A. Just that one!
[hash for hash in data if data[hash]['type'] == 'MRTN' and any([x for x in data[hash]['hex_strings'] if 'altenterexit' in x.lower()])]
# 002DB94AA986D1EF

[(data[hash]['name'], data[hash]['hex_strings'], hash) for hash in data if data[hash]['correct_name'] and data[hash]['type'] == 'MRTN' and any([x for x in data[hash]['hex_strings'] if 'hm_disguise' in x.lower()])]

[hash for hash in data if data[hash]['type'] == 'MRTN' and any([x for x in data[hash]['hex_strings'] if 'hm_weapon_arm_and_grip_poses_1h' in x.lower()])]

[hash for hash in data if data[hash]['type'] == 'MRTN' and not data[hash]['correct_name'] and any([x for x in data[hash]['hex_strings'] if 'hm_disguise' in x.lower()])]
'''

data = load_data()
with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, List[str]] = pickle.load(handle)

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

def guess_mrtn_name_from_tblu(hash: str) -> set[str]:
    # Check reverse hash from TEMP -> TBLU
    possible: set[str] = set()
    if hash in reverse:
        # For now, only one
        for r in reverse[hash]:
            if r in data and data[r]['type'] == 'TEMP':
                for d in data[r]['depends']:
                    if d in data and data[d]['type'] == 'TBLU':
                        for h in data[d]['hex_strings']:
                            h = h.lower()
                            if h.startswith('act_'):
                                possible.add(h.removeprefix('act_'))
    return possible

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
5 - there were multiple that had the same prefix, like a worse 3
6 - there were no likely names...but there were potential names
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
            hex_string.startswith('fr_') or
            hex_string.startswith('s03_hm_')):
            likely_names.add(hex_string)

        if hex_string not in ['ioivariation1', '__network__', 'controlparameters']:
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
        if len(filtered_likely) == 0 and len(filtered_unlikely) == 0:
            return [(h, 2) for h in likely_names]
        if len(filtered_likely) == 0:
            if len(filtered_unlikely) == 1:
                # Even LESS likely
                # Ex. 00F3D1A4356768BC
                return [(filtered_unlikely.pop(), 3)]
            else:
                return [(h, 5) for h in filtered_unlikely]
        if len(filtered_likely) == 1:
            return [(filtered_likely.pop(), 1)]
        else:
            return [(h, 2) for h in filtered_likely]
    else:
        if len(potential_names) == 1:
            # Example is 00E0560CEEE1C676
            return [('mr_' + potential_names.pop(), 4)]
        return [(h, 6) for h in potential_names]

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
        # '0074CEBF259295F9', # mr_stand_rail_lean_100cm -> mr_stand_rail_lean
        if guess.endswith('cm'):
            looser_guesses.add('_'.join(guess.split('_')[:-1]))
        # '00F078E11C62DE9E', # huntact_checkhighcover_pistol_right_aggressive -> huntact_checkhighcover_pistol_right
        if guess.endswith('_aggressive'):
            looser_guesses.add(guess.removesuffix('_aggressive'))
        # 004917F96BE6BA2E, # mr_bodyguard_start_alarm -> bodyguard_start_alarm
        if guess.startswith('mr_'):
            looser_guesses.add(guess.removeprefix('mr_'))
        # 005B61579DDCE049, # fr_staff_stand_japanesebow -> fr_stand_japanesebow
        if '_staff_' in guess:
            looser_guesses.add(guess.replace('_staff_', '_'))
        # 0048DC89E83F6F1B, # mr_carryplate_pickup_putdown_75cm -> mr_carryplate_putdown_75cm
        if '_pickup_putdown_' in guess:
            looser_guesses.add(guess.replace('_pickup_putdown_', '_pickup_'))
            looser_guesses.add(guess.replace('_pickup_putdown_', '_putdown_'))
        # '002DB94AA986D1EF', # hm_disguise_hips_coffin_altenterexit -> disguisesafezonecoffin_altenterexit
        # '008A8778030C24C5', # hm_disguise_hips_coffin -> disguisesafezonecoffin
        # '001C64C3F221DC93', # hm_disguise_hips_railing -> disguisesafezonerailing
        if 'hm_disguise_hips_' in guess:
            looser_guesses.add(guess.replace('hm_disguise_hips_', 'disguisesafezone'))
            # '007B79FCA15E280A', # hm_disguise_hips_bodyguard_stand -> disguisesafezonebodyguardstand
            looser_guesses.add(guess.replace('hm_disguise_hips_', 'disguisesafezone').replace('_', ''))
        # '00AF21190B40D4FB', # hm_disguise_blendin_microscope -> disguisesafezonemicroscope
        # '0001297A2543AAAA', # hm_disguise_blendin_scarecrow -> disguisesafezonescarecrow
        if 'hm_disguise_blendin_' in guess:
            looser_guesses.add(guess.replace('hm_disguise_blendin_', 'disguisesafezone'))
        # '00E98DB69697ACBF', # fh_stand_clipboard -> fr_stand_clipboard
        # '002472F589824BBB', # fh_stand_impatient -> fr_stand_impatient
        if guess.startswith('fh_stand_'):
            looser_guesses.add('fr_stand_' + guess.removeprefix('fh_stand_'))
        # 00342898A1FEADF5, # mr_cross_stand_impatient -> mr_cross_stand_angry
        if guess.endswith('_impatient'):
            looser_guesses.add(guess.removesuffix('_impatient') + '_angry')
        # '0082187AFCEE2CE0', # mr_s02_hm_interact_torch_ignite_0cm -> s03_hm_interact_torch_ignite_0cm
        if guess.startswith('mr_s02_'):
            looser_guesses.add('s03_' + guess.removeprefix('mr_s02_'))
        # 0096B19F9FC0B735, # mr_stand_table_lean_forward_drink_120cm_01 -> mr_stand_table_lean_forward_drink_120cm
        if re.match(r'.*_\d+$', guess):
            looser_guesses.add('_'.join(guess.split('_')[:-1]))
        # 006F50D89CD7F69E, # mr_stand_planning_table_act02_100cm -> mr_stand_planning_table_02_100cm
        if '_act' in guess:
            looser_guesses.add(re.sub(r'_act(\d+)', r'_\1', guess))
        # 009EE8284A331A10, # mr_military_stand_riffle_var1 -> mr_military_stand_riffle_var01
        # 00FBD313412B952C, # mr_military_stand_riffle_var2 -> mr_military_stand_riffle_var02
        if guess[-1].isnumeric():
            looser_guesses.add(guess[:-1] + '0' + guess[-1])            
            
    return looser_guesses


'''
Used for debugging the detection scripts. This tries to find all the ones that are known
'''
def check_known_mrtns():
    known_exceptions = [
        '00D48551E6479601', # hm_interact_place_sneak_60cm -> hm_interact_placement
        '007584610AE12FE5', # mr_sit_bench_sick -> mr_sit_bench_poison_sick
        # '0056E8A0D2783184', # darksnipersuit_idle
        # '0020CB240F4A51DC', # clownsuit_idle (<- you can fix this TODO)
        # '0006FD4A21D6857C', # cowboysuit_idle

        # TODO: we should do neutral stands for everyone
        '00380C7C35DA0DFA', # fh_stand_neutral/fh_model_stand_wait_1/fh_model_mr_stylist_stand_makeup - fh_model_stand_neutral

        '0030C9AB45CBB928', # hm_disguise_hips_sit_tablet -> disguisesafezone_readtablet_sit

        '00B3731113F4D6E6', # hm_push_elevator_button -> elevatorpushbutton
        '00027A8D19596880', # hm_weapon_arm_and_grip_poses_1h_remote_detonator_detonate -> hm_remote_activate_detonator
        '00D572BC26F9B5DA', # hm_interact_vial_bottle_100cm_1 -> hm_interact_vialknife_bottle_100cm
        '00D180C1A5D45737', # hm_interact_vial_bottle_100cm -> hm_interact_vial_food_100cm
        '003A7A583C6DDFFE', # hm_interact_vial_bottle_100cm -> hm_interact_vial_glass_100cm
        '00441D3D4B28F351', # hm_interact_vial_bottle_100cm -> hm_interact_vial_glass_120cm
        '006DA32411BEF322', # hm_weapon_arm_and_grip_poses_1h_remote_detonator_detonate_wolverine -> hm_remote_activate_detonator_wolverine
        '00884A91011B01F1', # hm_placement_place_stand_60cm_down -> hm_interact_placement_placeobject_60cm
        '00D22202379F2D01', # hm_placement_retrieve_stand_60cm_down -> hm_interact_placement_retrieveobject_60cm
        '006F8644D9A8F2D1', # mr_stand_phone_text_pace -> mr_stand_phone_pace_text
        # # LMAOOOO
        '00DD13648025C431', # mr_stand_wall_lean_side_shoulder_left -> mr_stand_wall_lean_side_shoulder_right
        '005A8982427113DC', # hm_interact_flip_switches_horiz_140cm -> hm_interact_flip_switches_140cm_up
        '00385A27CB01A94A', # hm_interact_flip_switches_horiz_140cm_1 -> hm_interact_flip_switches_140cm_down
        '00005A83449DFF02', # hm_push_button_100cm_prologexit -> hm_interact_push_button_100cm_prologexit
        '0021DD8CC33BB8A7', # hm_interact_dumbwaiter_mid_put_take_1 -> hm_interact_placement_swapobjects_110cm
        '001A6D9FC79DE34C', # lots of stuff -> mr_hunting_act_guard
        # # Huh.
        '0097BCCD01FD6FCB', # mr_stand_submissive_01 -> mr_stand_sumissive_01
        '007DB78C218A7E45', # mr_stand_knightkgb_projectorreaction_1 -> mr_kgb_stand_reactionprojector
        '008B0958B5469A06', # <nothing> -> disguisesafezoneclipboard
        '000A03C9A2ED26AF', # hm_disguise_blendin_mop -> disguisesafezonejanitormop
        '00B8829435F03EEA', # mr_stand_wall_lean_back_transition -> talkact_mr_leanwall_back
        '00FC0D312CE3E152', # act_stand_piano_lean_enter_openlid -> mr_stand_piano_lean_open_lid
        '007280B3FD792FDC', # hm_interact_dumbwaiter_mid_put -> hm_interact_place_object_110_cm
        '00E5721B66CCF47C', # mr_carryglass_putpick_100cm -> mr_stand_neutral_glass_putdown_100cm
        '0099CBEA613CC81C', # mr_carryglass_putpick_100cm_1 -> mr_stand_neutral_glass_pickup_100cm
        # TODO: gettable
        '006D48AE8E519E86', # fr_heidi_stand_angry_gesture/listen/stand/behaviour -> fr_heidi_stand_angry
        '007DE788C98E33C5', # fh_catwalk_end_act_01 -> fh_model_catwalk_end_act03
        '00B079A44EB37E64', # fh_catwalk_end_act_02 -> fh_model_catwalk_end_act04
        '009123995FFEFAC4', # fh_carryglass_putpick_120cm -> fh_stand_neutral_glass_putdown_120cm
        '0070CCC9BC1E1EE2', # mr_stand_phone_filming -> mr_stand_filming_phone
        '00EC77B2BAEE4D74', # mr_mime_standidle -> mr_mime_stand_perform
        '002419E880E53C4E', # lots of stuff -> hm_interact_pickup_object_110_cm
    ]

    count = 0
    for hash in data:
        if data[hash]['type'] == 'MRTN':
            count += 1
            # If the hash has the correct name, we should be able to guess it
            if not data[hash]['correct_name']:
                continue
            if len(data[hash]['hex_strings']) > 70: # really 1000 is a better limit
                # For now, just ignore these
                # Ex. 00CEC267BD1B5133 (TODO: are we extracting everything from here?)
                # Ex. 005C40E612CC9242 (only 72, should we be able to fix this?)
                continue
            names = guess_mrtn_name(hash)
            from_tblu = guess_mrtn_name_from_tblu(hash)
            for f in from_tblu:
                names.append((f, 1))
            
            # TODO: Idle should be guessable
            if 'idle' in data[hash]['name'] or hash in known_exceptions:
                continue
            if len(names) == 0:
                print(f'Found nothing ({count})')
                print(hash)
                print(data[hash]['name'])
                if count > 1400:
                    exit()
            else:
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
                        print(f'Was wrong.  ({count})')
                        print(hash)
                        print(data[hash]['name'])
                        print(names)
                        print(loose)
                        if count > 1400:
                            exit()

# This takes the known folders, and finds the patterns
# It also uses some relatively complex logic to extract best guesses for the 
# base MRTN names from hex_strings and reverse TEMP -> TBLU dependencies.
# Finally it tries to combine all of these
def attempt_smarter():
    # Open the prefixes
    with open('mrtn_folders.pickle', 'rb') as handle:
        mrtn_folders: set[str] = set(pickle.load(handle))

    folder_patterns = find_folder_patterns(list(mrtn_folders))
    formats: List[List[str]] = []
    for pattern in folder_patterns:
        pattern_pieces = pattern.split('*')
        formats.append([pattern_pieces[0], pattern_pieces[1], '.aln].pc_rtn'])
        if 'hitman01' in pattern:
            pattern_pieces2 = pattern.replace('hitman01', 'hitman02').split('*')
            formats.append([pattern_pieces2[0], pattern_pieces2[1], '.aln].pc_rtn'])

            pattern_pieces3 = pattern.replace('hitman01', 'hitman03').split('*')
            formats.append([pattern_pieces3[0], pattern_pieces3[1], '.aln].pc_rtn'])

    mrtn_strings: List[set[str]] = []
    for hash in data:
        if data[hash]['type'] == 'MRTN':
            names = guess_mrtn_name(hash)
            from_tblu = guess_mrtn_name_from_tblu(hash)
            for f in from_tblu:
                names.append((f, 1))
            loose = loose_expand(names)
            mrtn_strings.append(loose)
    unique_mrtn_strings: set[str] = set()
    unique_mrtn_strings = unique_mrtn_strings.union(*mrtn_strings)

    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])
        
    index = 0
    found_hashes: Dict[str, str] = {}
    for format in formats:
        index += 1
        hashes = hashcat('MRTN', wordlist, unique_mrtn_strings, format, data)
        print(f'For hash {index} of {len(formats)}, found {len(hashes)} hashes.')
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
    
    # Run with the known folders
    found = hashcat('MRTN', mrtn_folders, unique_mrtn_strings,
                    ['', '', '.aln].pc_rtn'])
    for hash in found:
        found_hashes[hash] = found[hash]
        
    for hash in found_hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + found_hashes[hash])

# attempt_one()
# with open('hitman_wordlist.txt', 'r') as f:
#     words = [x.strip() for x in f.readlines()]

# for word in words:
#     # {word}suit
#     path = '[assembly:/animationnetworks/hitman01/idles/{word}suit_idle.aln].pc_rtn'
#     hash = ioi_string_to_hex(path)
#     if hash in data and not data[hash]['correct_name']:
#         print(hash + ', ' + path)
# exit()

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

# print(guess_mrtn_name('00545ACF3EC44F60'))
# exit()

print('Loaded')
attempt_smarter()