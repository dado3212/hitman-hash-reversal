from utils import load_data, hashcat, targeted_hashcat, ioi_string_to_hex
import re, json, pickle, string
from typing import List

data = load_data()
with open('reverse.pickle', 'rb') as handle:
    reverse = pickle.load(handle)

'''
My theory is, what if RTLV is just the same as the temp path but with a different
extension?

003996A72169FC91.TEMP - [assembly:/_pro/scenes/frontend/videodatabase/videodatabase_dlc_1_harveywallbanger.entity].pc_entitytemplate
depends on 
001A3C5C433DF838.TBLU - [assembly:/_pro/scenes/frontend/videodatabase/videodatabase_dlc_1_harveywallbanger.entity].pc_entityblueprint
006CF07CF75C7EBF.RTLV - briefing_harveywallbanger
'''

 # Only use ascii and _ in the guessing for these paths
# Not suitable for everything
with open('hitman_wordlist.txt', 'r') as f:
    hitman_wordlist = set([x.strip() for x in f.readlines()])
with open('wordlist_12.txt', 'r') as f:
    wordlist_12 = set([x.strip() for x in f.readlines()])
with open('wordlist_1.txt', 'r') as f:
    wordlist_1 = set([x.strip() for x in f.readlines()])
with open('wordlist_3.txt', 'r') as f:
    wordlist_3 = set([x.strip() for x in f.readlines()])

wordlist = hitman_wordlist.union(wordlist_12).union(wordlist_1).union(wordlist_3)

'''
Courtesy of set([data[hash]['name'].split('.')[-1] for hash in data if data[hash]['correct_name']])
these are all of the current extensions.

{'pc_bonerig', 'pc_rtn', 'pc_asva', 'pc_blobs', 'pc_preload', 'pc_json', 'pc_airg', 'pc_wes', 'pc_mipblock1', 'pc_unlockables', 'pc_sweetline', 'pc_localized-textlist', 'pc_coll', 'pc_entityresource', 'pc_swf', 'pc_entitytemplate', 'pc_animset', 'pc_entityblueprint', 'pc_gfx', 'pc_contracts', 'pc_scatterdata', 'pc_resourceidx', 
'pc_facefx', 'pc_prim', 'pc_multilanguage-textlist', 'pc_physsys', 'pc_boxc', 'pc_entitytype', 'pc_rtr', 'pc_crmd', 'pc_mi', 'pc_mate', 'pc_tex', 'pc_atmd', 'pc_vertexdata', 'pc_linkedprim', 'pc_aibz', 'pc_animation', 'pc_navp', 'pc_wwisebank', 'pc_dialogevent', 'pc_sdefs', 'pc_bonemask', 'pc_repo', 'pc_weightedprim', 'pc_activities', 'pc_gfxv'}
'''

# debunked .pc_<wordlist><wordlist>
# debunked .pc_<wordlist>

hash = '006CF07CF75C7EBF'
target_hashes = set([hash])
formats: List[List[str]] = [
    ['[assembly:/_pro/scenes/frontend/videodatabase/videodatabase_dlc_1_harveywallbanger.entity]','','']
]
for format in formats:
    hashes = hashcat('targeted-rtlv', set(['.pc_']), wordlist, format, override_hashes=target_hashes)
    if hash in hashes:
        print(hash + ', ' + hashes[hash])