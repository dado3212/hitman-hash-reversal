from utils import ioi_string_to_hex, load_data, hashcat, targeted_hashcat
import pickle, re, itertools, string
from typing import List, Dict
from futzing import replaceable_sections, num_alts, replacements

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

def print_unknown_tblus():
    data = load_data()

    unique: set[str] = set()

    for hash in data:
        if data[hash]['type'] == 'TBLU' and not data[hash]['correct_name'] and len(data[hash]['hex_strings']) == 1:
            unique.add(data[hash]['hex_strings'][0].lower())
    
    sorted_unique = sorted(unique)
    for f in sorted_unique:
        print(f)

############################
## FUTZING
############################

# This is wrong, include TBLU and TEMP
# with open('template_folders.pickle', 'rb') as handle:
#     template_folders = pickle.load(handle)

# with open('hashes.pickle', 'rb') as handle:
#     data = pickle.load(handle)

# print(len(template_folders))
# futzed: set[str] = set()
# for folder in template_folders:
#     sections = replaceable_sections(folder)
#     num_alt_strings = num_alts(sections)
#     # Try and avoid huge fanouts for now
#     if num_alt_strings > 0 and num_alt_strings < 100000:
#         possible_names = replacements(sections)
#         futzed = futzed.union(possible_names)

# prefixes = list(futzed.difference(template_folders))

# print('Processing')
# unknown: Dict[str, str] = {}
# for hash in data:
#     if data[hash]['type'] == 'TEMP' or data[hash]['type'] == 'TBLU':
#         if (len(data[hash]['name']) > 0 and 
#             not data[hash]['correct_name']
#             and data[hash]['name'] != 'geomentity01'):
#             unknown[hash] = data[hash]['name']

# # unknown = {'00CFE3B1AB59144F':'keyword_flu_cough_exclude'}

# last_perc = 0.0
# num_prefixes = len(prefixes)
# print('0%')
# # got up to 6.4% with word_word2 and wordlist_3
# for i in range(num_prefixes):
#     new_perc = round(i * 100.0 / num_prefixes, 1)
#     if new_perc > last_perc:
#         last_perc = new_perc
#         print(str(new_perc) + '%' + ' - ' + str(i))
#     prefix = prefixes[i]
#     for hash in unknown:
#         new_name = prefix + '/' + unknown[hash] + '.entitytemplate].pc_entitytype'
#         if ioi_string_to_hex(new_name) == hash:
#             print(hash + ', ' + new_name)

############################
## GUESSING
############################

def guessing_first_attempt():
    data = load_data()

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
        # act_mr, [assembly:/_pro/design/actor/acts/levels/{x}.template?/ ({x}, fr_{x}, fh_{x}, mr_{x})
        # act_mr, [assembly:/_pro/design/actor/acts/{x}.template?/ ({x}, fr_{x}, fh_{x}, mr_{x})
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
        # everything, [assembly:/_pro/environment/templates/props/clothing/{x}_a.template?/ ({x}, {x}_a)
        # everything, [assembly:/_pro/environment/templates/props/signs/signs_{x}_a.template?/ ({x}_a, {x})
        # door, [assembly:/_pro/environment/templates/architecture/doors/doors_{x}_a.template?/ ({x}_a, {x})
        # sky_, [assembly:/_pro/environment/templates/backdrop/sky/sky_{x}.template?/, ({x}, {x}_a)
        # sky_, [assembly:/_pro/environment/templates/backdrop/{x}/{x}_a.template?/
        # slurry_, [assembly:/_pro/environment/templates/levels/{x}/slurry_shed_a.template?/
        # everything, [assembly:/_pro/environment/templates/props/furniture/{x}_furniture_a.template?/ ({x}_furniture, {x}_furniture_a)
        # sound_, [assembly:/templates/sound/{x}.template?/ ({x}, {x}_a)
        # sound_, [assembly:/templates/sound/sound_{x}_a.template?/ ({x}, {x}_a)
        # spray_, [assembly:/_pro/environment/templates/props/{x}_props/{x}_inside_props_b.template?/ (_b, _a, _inside, _outside, {x}_props/{x}_, {x}/{x}_)
        # TODO: This shows that some of them are _b suffixed. Can we futz all known folders?
        # TODO: Some version of [assembly:/_pro/environment/templates/props/furniture/cafe_furniture_italy_a.template?/table_cafe_italy_a_00.entitytemplate].pc_entityblueprint or street_furniture_marrakesh
        # _kit_, [assembly:/_pro/environment/templates/levels/{x}/factory_building_{x}_a.template?/
        # _kit_, [assembly:/_pro/environment/templates/levels/{x}/{x}_a.template?/
        # everything, [assembly:/_pro/environment/templates/kits/suburban_house/suburban_{x}_a.template?/
        # lamp, [assembly:/_pro/environment/templates/props/lamps/lamps_{x}_a.template?/ (lamps_{x}_a, lamps_outdoor_{x}_a, lamps_indoor_{x}_a, and without _a)
        ## prefixes = [f'[assembly:/_pro/environment/templates/props/lamps/lamps_{x}.template?/' for x in words]
        # kitchen_kit
        # gecko_penthouse

    # prefixes = [
    #     '[assembly:/_pro/design/gamecore/events/eventtokens_characters.template?/',
    #     '[assembly:/_pro/items/templates/accessories/clothes.template?/',
    #     '[assembly:/_pro/items/templates/accessories/explosives_a.template?/',
    #     '[assembly:/_pro/items/templates/accessories/pillows_a.template?/',
    #     '[assembly:/_pro/environment/templates/kits/embassy/embassy_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/sculptures/scuptures_icicle_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/sculptures/scuptures_wooden_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/signs/signs_banners_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/signs/signs_cafe_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/signs/signs_suburb_a.template?/',
    #     '[assembly:/_pro/environment/templates/architecture/doors/doors_hotel_a.template?/',
    #     '[assembly:/_pro/environment/templates/architecture/doors/doors_barn.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/penthouse_furniture_a.template?/',
    #     '[assembly:/templates/sound/sound_characters.template?/',
    #     '[assembly:/templates/sound/sound_crowd.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/barbershop_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/beachhouse_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/colombia_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/indian_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/plastic_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/raccoon_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/spa_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/winery_furniture_a.template?/',
    #     '[assembly:/_pro/design/actor/acts/experimental.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_ceiling_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_indoor_bank_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_indoor_bangkok.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_outdoor_seagull.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_colombia.template?/',
    #     '[assembly:/_pro/design/gamecore/events/eventtokens_characters.template?/',
    #     '[assembly:/_pro/items/templates/accessories/clothes.template?/',
    #     '[assembly:/_pro/items/templates/accessories/explosives_a.template?/',
    #     '[assembly:/_pro/items/templates/accessories/pillows_a.template?/',
    #     '[assembly:/_pro/environment/templates/kits/embassy/embassy_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/sculptures/scuptures_icicle_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/sculptures/scuptures_wooden_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/signs/signs_banners_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/signs/signs_cafe_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/signs/signs_suburb_a.template?/',
    #     '[assembly:/_pro/environment/templates/architecture/doors/doors_hotel_a.template?/',
    #     '[assembly:/_pro/environment/templates/architecture/doors/doors_barn.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/penthouse_furniture_a.template?/',
    #     '[assembly:/templates/sound/sound_characters.template?/',
    #     '[assembly:/templates/sound/sound_crowd.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/barbershop_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/beachhouse_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/colombia_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/indian_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/plastic_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/raccoon_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/spa_furniture_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/furniture/winery_furniture_a.template?/',
    #     '[assembly:/_pro/design/actor/acts/experimental.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_ceiling_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_indoor_bank_a.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_indoor_bangkok.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_outdoor_seagull.template?/',
    #     '[assembly:/_pro/environment/templates/props/lamps/lamps_colombia.template?/',
    # ]

    print('Processing')
    unknown: Dict[str, str] = {}
    for hash in data:
        if data[hash]['type'] == 'TEMP':
            if (len(data[hash]['name']) > 0 and 
                not data[hash]['correct_name']
                and data[hash]['name'] != 'geomentity01'):
                #if 'lamp' in data[hash]['name']:
                unknown[hash] = data[hash]['name']

    # unknown = {'00CFE3B1AB59144F':'keyword_flu_cough_exclude'}

    last_perc = 0.0
    num_prefixes = len(prefixes)
    #print('0%')
    # got up to 6.4% with word_word2 and wordlist_3
    for i in range(num_prefixes):
        new_perc = round(i * 100.0 / num_prefixes, 1)
        if new_perc > last_perc:
            last_perc = new_perc
            #print(str(new_perc) + '%' + ' - ' + str(i))
        prefix = prefixes[i]
        for hash in unknown:
            new_name = prefix + unknown[hash] + '.entitytemplate].pc_entitytype'
            if ioi_string_to_hex(new_name) == hash:
                print(hash + ', ' + new_name)

def guess_quixels_with_hashcat():
    data = load_data()
    print('loaded')

    possible_names: set[str] = set()

    for hash in data:
        if data[hash]['type'] == 'TBLU' and not data[hash]['correct_name']:
            for name in data[hash]['hex_strings']:
                if 'quixel' in name.lower():
                    possible_names.add(name.lower())

    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])
    
    hashes = hashcat('TBLU', wordlist, possible_names, ['[assembly:/_pro/_licensed/quixel/templates/quixel_', '_a.template?/', '.entitytemplate].pc_entityblueprint'], data)
    for hash in hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + hashes[hash])

def guess_tblus():
    data = load_data()
    
    with open('template_folders.pickle', 'rb') as handle:
        template_folders = pickle.load(handle)

    possible_names: set[str] = set()

    for hash in data:
        if data[hash]['type'] == 'TBLU' and not data[hash]['correct_name']:
            for name in data[hash]['hex_strings']:
                possible_names.add(name.lower())
    
    hashes = hashcat('TBLU', template_folders, possible_names, ['', '/', '.entitytemplate].pc_entityblueprint'], data)
    for hash in hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + hashes[hash])

# When new stuff omes out
# guess_tblus()

# Idle speculation
# print_unknown_tblus()
# print(targeted_hashcat('0015E4293A91BF0A', [
#     ['[assembly:/_pro/environment/templates/levels/the_ark/the_ark_',' _','_a.template?/gallery_int_ceiling_room_a.entitytemplate].pc_entityblueprint']
# ]))

# print(targeted_hashcat('001455A7C354D6C6', [
#     ['[assembly:/_pro/_licensed/quixel/templates/quixel_', '_', '_a.template?/quixel_cactus_c.entitytemplate].pc_entityblueprint'],
# ]))
# print(targeted_hashcat('00357EF86D7AA4AD', [
#     ['[assembly:/_pro/environment/templates/props/rocks/', '_', '_b.template?/quixel_mossy_rock_llama_d.entitytemplate].pc_entityblueprint'],
# ]))
# [assembly:/_pro/environment/templates/props/plants/plants_potplants_b.template?/quixel_flowerpot_sizeb_bulldog_a.entitytemplate].pc_entityblueprint