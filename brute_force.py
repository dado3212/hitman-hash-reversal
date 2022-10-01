from utils import ioi_string_to_hex
import pickle, re
from typing import List, Any, Optional, Dict

# fumigation_skunk_a maybe in the same boat
# flightcases_stickers_b
# moja_logo_decal_a
# miami_race_track_painted_logo_a
# miami_garage_wallpaper_logos_a
# thai_exterminator_a
# movie_set_fx_crew_trailer_logo
# sarhimnir_logo_a
# schnelli_express_fast_food_logo_a, schnelli_express_fast_food_logo_b

# Weird ones
# sanguine_b -> sanguine_logo_bw
# hokkaido_hospital_a_chrome -> hokkaido_hospital_a
# jitter_logo_entrance_a -> jitter_logo_a
# wine_barrels_a -> wine_barrel_a
# hokkaido_hospital_a_frosted -> hokkaido_hospital_a
# italy_shops_butcher_a_diffuseonly -> italy_shops_butcher_a
# eclipse_white_a_hardalpha -> eclipse _white_a
# italy_bakery_a -> cafe_carpet_italy_a
# 

# with open('reverse.pickle', 'rb') as handle:
#     reverse = pickle.load(handle)
# Just brute force one thing

# [assembly:/_pro/environment/materials/decals/logo/himmapan_hotel_a.mi].pc_mi
# [assembly:/_pro/environment/materials/decals/logo/himmapan_hotel_b.mi].pc_mi
with open('texture_suffixes.pickle', 'rb') as handle:
    texture_suffixes: List[str] = pickle.load(handle)

success = [
    '0067952FA6FA8D56',
    '0058E0876756F198',
    '009CDB2526FD9A66',
    '0030383696BACB49',
    '00734EF25A7A7E5C',
    '00382AD529561BC1',
]

start = [
    '[assembly:/_pro/environment/textures/decals/logo/',
    '[assembly:/_pro/environment/textures/decals/logos/',
    '[assembly:/_pro/environment/textures/decals/',
    '[assembly:/_pro/environment/textures/logo/',
    '[assembly:/_pro/environment/textures/logos/',

    '[assembly:/_pro/environment/textures/levels/bangkok/',
    '[assembly:/_pro/environment/textures/levels/bangkok/himmapan_hotel_a/',
    '[assembly:/_pro/environment/textures/levels/tiger/himmapan_hotel_a/',
    '[assembly:/_pro/environment/textures/levels/tiger/',
]
base = [
    'himmapan_hotel_b',
    'himmapan_hotel_a',
    'himmapan_hotel_c',
    'himmapan_hotel_d',
]
name = base[::]
for n in base:
    for i in range(len(n)):
        if n[i] == '_':
            new = n[0:i] + ' ' + n[i:]
            name.append(new)

for n in base:
    for i in range(len(n)):
        if n[i] == '_':
            new = n[0:i] + '_logo' + n[i:]
            name.append(new)

for n in base:
    name.append('logo_' + n)

for n in name[::]:
    name.append(n + 'w')

for n in name[::]:
    name.append(n.replace('himmapan_', ''))
    name.append(n.replace('hotel_', ''))

for n in name[::]:
    name.append(n + '_decal')
    name.append(n + '_a')
    name.append(n + '_decal_a')

print(name)

for s in start:
    for n in name:
        for suffix in texture_suffixes:
            file = s + n + '.texture' + suffix
            if (ioi_string_to_hex(file) in success):
                print(file)

# with open('hashes.pickle', 'rb') as handle:
#     data = pickle.load(handle)

# for hash in data:
#     if '_pro/environment/materials/decals/logo' in data[hash]['name']:
#         for depends in data[hash]['depends']:
#             print(data[hash]['name'] + '\t' + (data[depends]['name'] if depends in data else 'unknown'))
