from utils import ioi_string_to_hex, hashcat, targeted_hashcat, load_data
from typing import List, Dict

data = load_data()
vidb_hex_strings: set[str] = set()
rtlv_names: set[str] = set()

for hash in data:
    if data[hash]['type'] == 'VIDB':
        if len(data[hash]['hex_strings']) == 1:
            print(hash + '.VIDB, ' + data[hash]['hex_strings'][0])
        else:
            print(hash + '.VIDB')
            print(data[hash]['hex_strings'])
        vidb_hex_strings = vidb_hex_strings.union(data[hash]['hex_strings'])
    elif data[hash]['type'] == 'RTLV':
        rtlv_names.add(data[hash]['name'])

# for string in vidb_hex_strings:
#     print(string)

# for f in vidb_hex_strings.difference(rtlv_names):
#     print('Missing from RTLV: ' + f)

# for f in rtlv_names.difference(vidb_hex_strings):
#     print('Missing from VIDB: ' + f)

# Missing from RTLV: briefing_ginfizz - s6
# Missing from RTLV: briefing_seabreeze - s6
# Missing from RTLV: briefing_thelastword - sapienza ET?
# Missing from RTLV: debriefing_flamingo_e3_2018
# Missing from RTLV: debriefing_flamingo_gamescom_2018
# Missing from RTLV: briefing_gimlet - s6
# Missing from RTLV: briefing_blackrussian - s6
# Missing from RTLV: briefing_blueblazer - s6
# Missing from RTLV: briefing_mimosa - s6
# Missing from RTLV: briefing_bronx - patient zero, the rogue (maybe? check once RTLV has been fixed)
# Missing from RTLV: previously_on_season1
# Missing from RTLV: hitman_trailer
# Missing from RTLV: briefing_tamagozake
# Missing from RTLV: briefing_snakebite