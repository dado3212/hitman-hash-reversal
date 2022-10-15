from utils import ioi_string_to_hex
import pickle
import os, shutil
from typing import List, Dict

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

text_names = []

print('Finished loading')

lookup: Dict[str, set[str]] = dict()

def get_recursive_depends(hash: str, search_type: str) -> set[str]:
    if hash not in data:
        return set()
    matching: set[str] = set()
    for depends in data[hash]['depends']:
        if depends in lookup:
            matching = matching.union(lookup[depends])
            continue
        if depends in data:
            depends_hashes: set[str] = set()
            if data[depends]['type'] == search_type:
                depends_hashes.add(depends) # + ' - ' + depends + ' - ' + ','.join(data[depends]['chunks']))
            for f in get_recursive_depends(depends, search_type):
                depends_hashes.add(f)
            matching = matching.union(depends_hashes)
            lookup[depends] = depends_hashes
        else:
            lookup[depends] = set()
    return matching

brick = '00E9F09C3B030590.TEMP'
# scene = '00E4D6951CC4089E.TEMP'
# smaller = '009A2D29F25BCA8F.PRIM'
brick_recursion = get_recursive_depends(brick, 'TEXT')
# recursion2 = get_recursive_depends(scene, 'TEXT')

# new_additions = [x for x in recursion2 if x not in recursion]

# for dirpath,_,filenames in os.walk('D:\\Alex\\Desktop\\Hitman Modding\\Extracts\\Textures'):
#     for f in filenames:
#         for img in new_additions:
#             if '.png' in f and img in f:
#                 absolute = os.path.abspath(os.path.join(dirpath, f))
#                 shutil.copyfile(absolute, './scene/' + img + '.png')

apt = '00916FCA49E7A124.TEMP'
apt_recursion = get_recursive_depends(apt, 'TEXT')
apt_recursion = [x for x in apt_recursion if x not in brick_recursion]

for dirpath,_,filenames in os.walk('D:\\Alex\\Desktop\\Hitman Modding\\Extracts\\Textures'):
    for f in filenames:
        for img in apt_recursion:
            if '.png' in f and img in f:
                absolute = os.path.abspath(os.path.join(dirpath, f))
                shutil.copyfile(absolute, './apt/' + img + '.png')

# 002A945B6025BD1A.TEXT - deck of cards
# wall_rug

