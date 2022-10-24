import pickle, re
from typing import List, Dict, Any, Optional
from utils import ioi_string_to_hex

############################
## KNOWN
############################

# unique: set[str] = set()
# with open('hash_list.txt', 'r') as f:
#     # completion
#     f.readline()
#     # hashes count
#     f.readline()
#     # version number
#     f.readline()

#     for line in f.readlines():
#         split = line.split(',', 1)
#         ioi_string = split[1].rstrip()
#         extension = split[0][-4:]
        
#         if extension == 'WWEV':
#             if 'assembly' in ioi_string:
#                 # [assembly:/_pro/environment/templates/backdrop/buildings/backdrop_buildings_hokkaido_a.template?/backdrop_hokkaido_building_clusters_a.entitytemplate].pc_entityblueprint
#                 info = re.search(r"^(.*\/)[^\/]*.wwiseevent.*$", ioi_string, re.IGNORECASE)
#                 if info is None:
#                     continue
#                     # print(ioi_string)
#                     # break
#                 else:
#                     unique.add(info.group(1))

# sort = sorted(list(unique))
# for s in sort:
#     print(s)
# exit()

with open('hashes.pickle', 'rb') as handle:
    data: Dict[str, Any] = pickle.load(handle)

# with open('wwev_folders.pickle', 'rb') as handle:
#     wwev_folders: List[str] = pickle.load(handle)

with open('hitman_wordlist.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]
    # sfx, [assembly:/sound/wwise/exportedwwisedata/events/sfx_cutscenes/sfx_cutscenes_{x}/
    # sfx, [assembly:/sound/wwise/exportedwwisedata/events/props_events/props_{x}/
    # ui_, [assembly:/sound/wwise/exportedwwisedata/events/gui_events/ingame_gui/{x}/
    # item_, [assembly:/sound/wwise/exportedwwisedata/events/item_events/item_{x}/
    # cin_, [assembly:/sound/wwise/exportedwwisedata/events/sfx_cutscenes/sfx_cutscenes_{x}/sfx_cutscenes_{x}_music/
    # cin_, [assembly:/sound/wwise/exportedwwisedata/events/sfx_cutscenes/sfx_cutscenes_{x}/sfx_cutscenes_{x}_soundfx/
    # distraction, [assembly:/sound/wwise/exportedwwisedata/events/props_events/setpieces/distractions/distraction_{x}/ <- there's more here, pull guesses from file names
    # container, [assembly:/sound/wwise/exportedwwisedata/events/props_events/setpieces/containers/{x}/
    # container, [assembly:/sound/wwise/exportedwwisedata/events/props_events/setpieces/containers/container_{x}/
    # sfx, [assembly:/sound/wwise/exportedwwisedata/events/props_events/setpieces/activators/activator_{x}/ <- more here
    # sfx, [assembly:/sound/wwise/exportedwwisedata/events/effects/{x}/
    # fol_, [assembly:/sound/wwise/exportedwwisedata/events/animation/foley/environment_interactions/{x}/
    # fol_, [assembly:/sound/wwise/exportedwwisedata/events/animation/acts/fol_{x}/
    # fol_, [assembly:/sound/wwise/exportedwwisedata/events/animation/fol_{x}/
    # CURRENTLY ^ ARE DONE
    # sfx, [assembly:/sound/wwise/exportedwwisedata/events/animation/acts/{x}/
    # sfx, 
    # sfx, [assembly:/sound/wwise/exportedwwisedata/events/ambience_events/elements/amb_e_{x}/
    # sfx, [assembly:/sound/wwise/exportedwwisedata/events/ambience_events/elements/{x}/

    prefixes = [f'[assembly:/sound/wwise/exportedwwisedata/events/animation/fol_{x}/' for x in words]

# def guess(guessed_name: str) -> Optional[str]:
    # for wwev_folder in wwev_folders:
    #     path = wwev_folder + guessed_name + '.wwiseevent].pc_wwisebank'
    #     if ioi_string_to_hex(path) == hash:
    #         return path

print('Processing')
unknown: Dict[str, str] = {}
for hash in data:
    if data[hash]['type'] == 'WWEV':
        if not data[hash]['correct_name']:
            guessed_name = ''
            if 'unknown' in data[hash]['name']:
                guessed_name = re.search(r"^.*\/([^\/]*).wwiseevent.*$", data[hash]['name'], re.IGNORECASE).group(1)
            elif len(data[hash]['hex_strings']) > 0:
                guessed_name = data[hash]['hex_strings'][0].lower()
            #if 'fol_' in guessed_name:
            unknown[hash] = guessed_name

last_perc = 0.0
num_prefixes = len(prefixes)
for i in range(num_prefixes):
    new_perc = round(i * 100.0 / num_prefixes, 1)
    if new_perc > last_perc:
        last_perc = new_perc
        #print(str(new_perc) + '%' + ' - ' + str(i))
    prefix = prefixes[i]
    for hash in unknown:
        new_name = prefix + unknown[hash] + '.wwiseevent].pc_wwisebank'
        if ioi_string_to_hex(new_name) == hash:
            print(hash + ', ' + new_name)

# for hash in data:
#     if not data[hash]['correct_name'] and data[hash]['type'] == 'WWEV':
#         if len(data[hash]['hex_strings']) == 0:
#             continue
#         guessed_name: str = data[hash]['hex_strings'][0].lower()
#         guessed_path = guess(guessed_name)
#         if guessed_path is not None:
#             print(hash + ',' + guessed_path)
#         else:
#             # Don't do this until the lz4 decode is fixed. Broken example:
#             # chunk28.rpkg, 006ABC35562F09D2 
#             temp_path = f'[unknown:/sound/wwise/exportedwwisedata/events/unknown/{guessed_name}.wwiseevent].pc_wwisebank'
#             if temp_path != data[hash]['name'] and data[hash]['name'] == '':
#                 #print(hash + ',' + temp_path + ',' + data[hash]['name'])
#                 continue
