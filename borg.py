from utils import ioi_string_to_hex, load_data, hashcat
import re, string, pickle
from typing import List, Dict

'''
Some helper commands to answer basic questions:

Q. Do all BORGs have a PRIM reverse dependency?
A. No, 128 of them don't, they have TEMP
[hash for hash in data if data[hash]['type'] == 'BORG' and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'PRIM']))]
[hash for hash in data if data[hash]['type'] == 'BORG' and (hash not in reverse or (not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'PRIM']) and not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'TEMP'])))]

Q. Do all BORGs with known names come from a known PRIM?
A. No. See 003B63108C6380A7 as an instance.
[hash for hash in data if data[hash]['type'] == 'BORG' and data[hash]['correct_name'] and not any([x for x in reverse[hash] if data[x]['type'] == 'PRIM' and data[x]['correct_name']])]

Q. Do all BORGs with a known PRIM reverse have a name?
A. Yes.
[hash for hash in data if data[hash]['type'] == 'BORG' and not data[hash]['correct_name'] and any([x for x in reverse[hash] if data[x]['type'] == 'PRIM' and data[x]['correct_name']])]

Q. Do all BORGs with no PRIM reverse have a name?
A. No. Sample is 00B14B5A0291EDD6
[(hash, len(reverse[hash])) for hash in data if data[hash]['type'] == 'BORG' and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'PRIM']))]
[(hash, data[hash]['name']) for hash in data if data[hash]['type'] == 'BORG' and data[hash]['correct_name'] and (hash not in reverse or not any([x for x in reverse[hash] if x in data and data[x]['type'] == 'PRIM']))]
'''

# The weird way
def guess_from_prims():
    data = load_data()
    print('loaded')

    paths: set[str] = set()

    for hash in data:
        if data[hash]['type'] == 'PRIM' and data[hash]['correct_name']:
            pieces = re.search(r'^(\[.*?\.wl2\?)/.*', data[hash]['name'], re.IGNORECASE)
            if pieces is None:
                continue
            paths.add(pieces.group(1) + '/bonesandcollision.weightedprim](bodypart).pc_bonerig')
            paths.add(pieces.group(1) + '/bones.weightedprim](bodypart).pc_bonerig')
            paths.add(pieces.group(1) + '/collision.weightedprim](bodypart).pc_bonerig')
    for path in paths:
        hash = ioi_string_to_hex(path)
        if hash in data and not data[hash]['correct_name']:
            print(hash + '.' + data[hash]['type'] + ', ' + path)

def try_and_guess_from_temp():
    with open('reverse.pickle', 'rb') as handle:
        reverse: Dict[str, List[str]] = pickle.load(handle)

    data = load_data()
    print('loaded')

    for hash in data:
        if data[hash]['type'] == 'BORG':
            found_temp = False
            guesses: set[str] = set()
            for reversed in reverse[hash]:
                if data[reversed]['type'] == 'TEMP' and data[reversed]['correct_name']:
                    found_temp = True
                    pieces = re.search(r'^(\[.*?)/([^\/]*)\.template\?/.*', data[reversed]['name'], re.IGNORECASE)
                    if pieces is None:
                        continue
                        # print('fuck ' + hash + ': ' + reversed + ' what is this: ' + data[reversed]['name'])
                        # exit()
                    remove_suffix = '_'.join(pieces.group(2).split('_')[:-1])
                    guesses.add(pieces.group(1).replace('templates', 'geometry') + '/frames/' + pieces.group(2) + '/' + pieces.group(2) + '_rig.wl2?/' + pieces.group(2) + '.linkedprim](bodypart).pc_bonerig')
                    guesses.add(pieces.group(1).replace('templates', 'geometry') + '/frames/' + pieces.group(2) + '/' + pieces.group(2) + '.wl2?/' + pieces.group(2) + '.linkedprim](bodypart).pc_bonerig')
                    guesses.add(pieces.group(1).replace('templates', 'geometry') + '/frames/' + remove_suffix + '/' + pieces.group(2) + '_rig.wl2?/' + pieces.group(2) + '.linkedprim](bodypart).pc_bonerig')
                    guesses.add(pieces.group(1).replace('templates', 'geometry') + '/frames/' + remove_suffix + '/' + pieces.group(2) + '.wl2?/' + pieces.group(2) + '.linkedprim](bodypart).pc_bonerig')
                    guesses.add(pieces.group(1).replace('templates', 'geometry') + '/frames/' + remove_suffix + '/' + remove_suffix + '_rig.wl2?/' + pieces.group(2) + '.linkedprim](bodypart).pc_bonerig')
                    guesses.add(pieces.group(1).replace('templates', 'geometry') + '/frames/' + remove_suffix + '/' + remove_suffix + '.wl2?/' + pieces.group(2) + '.linkedprim](bodypart).pc_bonerig')
            found_it = False
            for guess in guesses:
                possible_hash = ioi_string_to_hex(guess)
                if possible_hash in data:
                    found_it = True
                    if data[possible_hash]['correct_name']:
                        print('Known - ' + possible_hash + ', ' + guess)
                    else:
                        print('New - ' + possible_hash + ', ' + guess)
                    
            if not found_it and found_temp and data[hash]['correct_name']:
                print('what gives ' + hash)
                    # [assembly:/_pro/items/templates/firearms/pistol_classic_a.template?/firearm_model_pistol_classic_a.entitytemplate].pc_entitytype ->
                    #  [assembly:/_pro/items/geometry/firearms/frames/pistol_classic_a/pistol_classic_a_rig.wl2?/pistol_classic_a.linkedprim](bodypart).pc_bonerig

guess_from_prims()
# try_and_guess_from_temp()
