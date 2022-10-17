from utils import ioi_string_to_hex
import pickle, re, itertools, string
from typing import List, Dict

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
        
#         if extension == 'TBLU':
#             if 'assembly' in ioi_string:
#                 # [assembly:/_pro/environment/templates/backdrop/buildings/backdrop_buildings_hokkaido_a.template?/backdrop_hokkaido_building_clusters_a.entitytemplate].pc_entityblueprint
#                 info = re.search(r"^(.*)\.template.*$", ioi_string, re.IGNORECASE)
#                 if info is None:
#                     continue
#                     # print(ioi_string)
#                     # break
#                 else:
#                     unique.add(info.group(1))

# sort = sorted(list(unique))
# for s in sort:
#     print(s)

############################
## UNKNOWN
############################

# with open('hashes.pickle', 'rb') as handle:
#     data = pickle.load(handle)

# unknown: set[str] = set()
# for hash in data:
#     if (data[hash]['type'] == 'TBLU' or data[hash]['type'] == 'TEMP') and not data[hash]['correct_name']:
#         unknown.add(data[hash]['name'])
# sort = sorted(list(unknown))
# for s in sort:
#     print(s)

############################
## GUESSING
############################

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('hitman_wordlist.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]
    # event, [assembly:/_pro/design/gamecore/events/eventtokens_mission_
    # event, [assembly:/_pro/design/gamecore/events/eventtokens_
    # key, [assembly:/_pro/design/gamecore/keywords/keyword
    # a_ext, [assembly:/_pro/environment/templates/kits/{x}/{x}.template?/ ({x}, {x}_a)
    # access_helper, [assembly:/_pro/design/gamecore/{x}.template?/
    # access_helper, [assembly:/_pro/environment/templates/architecture/doors/{x}_a.template?/ ({x}_a, {x}, doors_{x}, doors_{x}_a)
    # accessoryitem, [assembly:/_pro/items/templates/accessories/{x}.template?/ ({x}, {x}_a)
    # accessoryitem, [assembly:/_pro/environment/templates/props/accessories/{x}.template?/ ({x}, {x}_a)
    # act_fr, [assembly:/_pro/design/actor/acts/{x}.template?/ ({x}, fr_{x}, fh_{x}, mr_{x})
    # act_fr, [assembly:/_pro/design/actor/acts/levels/{x}.template?/
    # TODO: ^ rerun above with act_mr
    # actor, [assembly:/_pro/design/actor/{x}.template?/
    # animlib, [assembly:/templates/{x}/{x}animlibraries.template?/
    # armoury, [assembly:/_pro/environment/templates/levels/the_ark/the_ark_environment _{x}_a.template?/ (without space too, {x}, {x}_a)
    # armoury, [assembly:/_pro/environment/templates/levels/the_ark/the_ark_{x}_a.template?/ ({x}, {x}_a)
    # _ext_, [assembly:/_pro/environment/templates/kits/{x}/{x}.template?/ ({x}, {x}_a)
    # _int_, [assembly:/_pro/environment/templates/kits/{x}/{x}.template?/ ({x}, {x}_a)
    # backdrop, [assembly:/_pro/environment/templates/backdrop/buildings/backdrop_buildings_{x}_a.template?/ ({x}, {x}_a)
    # everything, [assembly:/_pro/environment/templates/kits/{x}/{x}_a.template?/ (got to 92% and stopped)
    # prop_device_, [assembly:/_pro/design/items/prop_{x}_runtimes.template?/
    # prop_device_, [assembly:/_pro/design/items/prop_{x}.template?/ ({x}, {x}_a)
    # prop_device_, [assembly:/_pro/design/items/prop_explosives_{x}.template?/ ({x}, {x}_a)
    # sculpture, [assembly:/_pro/environment/templates/props/sculptures/scuptures_{x}.template?/ ({x}, {x}_a)
    # setpiece_, [assembly:/_pro/design/setpieces/unique/setpiece_{x}_unique.template?/
    # setpiece_, [assembly:/_pro/design/setpieces/setpieces/setpiece_{x}.template?/ ({x}, {x}_a)
    # shelving_, [assembly:/_pro/environment/templates/props/furniture/{x}_a.template?/ ({x}, {x}_a)
    # shirt_, [assembly:/_pro/environment/templates/props/clothing/{x}_a.template?/ ({x}, {x}_a)
    # TODO: Do ^ with everything
    # sign_, [assembly:/_pro/environment/templates/props/signs/signs_{x}_a.template?/ ({x}_a, {x})
    # TODO: Do ^ with everything for non sign_ named signs
    # door, [assembly:/_pro/environment/templates/architecture/doors/doors_{x}_a.template?/ ({x}_a, {x})
    # sky_, [assembly:/_pro/environment/templates/backdrop/sky/sky_{x}.template?/, ({x}, {x}_a)
    # sky_, [assembly:/_pro/environment/templates/backdrop/{x}/{x}_a.template?/
    # slurry_, [assembly:/_pro/environment/templates/levels/{x}/slurry_shed_a.template?/
    # sofa_, [assembly:/_pro/environment/templates/props/furniture/{x}_furniture_a.template?/
    # TODO: Do ^ for everything
    # sound_, [assembly:/templates/sound/{x}.template?/ ({x}, {x}_a)
    # sound_, [assembly:/templates/sound/sound_{x}_a.template?/ ({x}, {x}_a)
    # spray_, [assembly:/_pro/environment/templates/props/{x}_props/{x}_inside_props_b.template?/ (_b, _a, _inside, _outside, {x}_props/{x}_, {x}/{x}_)
    # TODO: This shows that some of them are _b suffixed. Can we futz all known folders?
    # TODO: Some version of [assembly:/_pro/environment/templates/props/furniture/cafe_furniture_italy_a.template?/table_cafe_italy_a_00.entitytemplate].pc_entityblueprint or street_furniture_marrakesh
    prefixes = [f'[assembly:/_pro/environment/templates/props/{x}/{x}_outside_props_a.template?/' for x in words]
    # 

# prefixes = [
#     '[assembly:/templates/sound/sound_characters.template?/',
#     '[assembly:/templates/sound/sound_crowd.template?/',
# ]

print('Processing')
unknown: Dict[str, str] = {}
for hash in data:
    if data[hash]['type'] == 'TEMP':
        if (len(data[hash]['name']) > 0 and 
            not data[hash]['correct_name']
            and data[hash]['name'] != 'geomentity01'):
            if 'spray_' in data[hash]['name']:
                unknown[hash] = data[hash]['name']

# unknown = {'00CFE3B1AB59144F':'keyword_flu_cough_exclude'}

last_perc = 0.0
num_prefixes = len(prefixes)
print('0%')
# got up to 6.4% with word_word2 and wordlist_3
for i in range(num_prefixes):
    new_perc = round(i * 100.0 / num_prefixes, 1)
    if new_perc > last_perc:
        last_perc = new_perc
        print(str(new_perc) + '%' + ' - ' + str(i))
    prefix = prefixes[i]
    for hash in unknown:
        new_name = prefix + unknown[hash] + '.entitytemplate].pc_entitytype'
        if ioi_string_to_hex(new_name) == hash:
            print(hash + ', ' + new_name)

