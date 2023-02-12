from utils import load_data, hashcat, targeted_hashcat, hashcat_multiple, find_folder_patterns
import pickle, re, string
from typing import List, Dict

data = load_data()

def get_mati_names() -> set[str]:
    mati_names: set[str] = set()
    for hash in data: 
        if data[hash]['type'] == 'MATI':
            if not data[hash]['correct_name']:
                for x in data[hash]['hex_strings']:
                    if '.mi' in x.lower():
                        mati_names.add(x.lower())
    return mati_names    
        
def use_known_folders():
    mati_names = get_mati_names()

    with open('material_folders.pickle', 'rb') as handle:
        material_folders: List[str] = pickle.load(handle)

    hashes = hashcat('MATI', set(material_folders), mati_names, ['', '/', '].pc_mi'], data)
    for hash in hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + hashes[hash])

def guess_folders():
    mati_names = get_mati_names()

    # Only use ascii and _ in the guessing for these paths
    # Not suitable for everything
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    formats: List[List[str]] = [
        # Failed for quixel lookup
        # ['[assembly:/_pro/_licensed/quixel/materials/', '/', '].pc_mi'],
        # ['[assembly:/_pro/_licensed/quixel/materials/generic/', '/', '].pc_mi'],
        # ['[assembly:/_pro/_licensed/quixel/materials/props/', '/', '].pc_mi'],
        # ['[assembly:/_pro/_licensed/quixel/materials/decals/', '/', '].pc_mi'],
        # ['[assembly:/_pro/characters/assets/crowd/male/','/materials/','].pc_mi'],
        # TODO: Can do more gender futzing
        # ['[assembly:/_pro/characters/assets/crowd/female/','/materials/','].pc_mi'],
        ['[assembly:/_pro/environment/materials/generic/','/','].pc_mi'],
    ]

    found_hashes: Dict[str, str] = {}
    for format in formats:
        hashes = hashcat('MATI', wordlist, mati_names, format, data)
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
        
    for hash in found_hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + found_hashes[hash])

# Currently this only supports patterns with one '*'
# TODO: Expand this
def guess_from_folder_patterns(patterns: set[str]):
    mati_names = get_mati_names()
    print('found mati names')

    # Only use ascii and _ in the guessing for these paths
    # Not suitable for everything
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    # bolster from mati names
    for mati_name in mati_names:
        if '_' in mati_name:
            wordlist.add('_'.join(mati_name.split('_')[:-1]))

    formats: List[List[str]] = []
    for pattern in patterns:
        pattern_pieces = pattern.split('*')
        formats.append([pattern_pieces[0], pattern_pieces[1], '].pc_mi'])

    index = 0
    found_hashes: Dict[str, str] = {}
    for format in formats:
        index += 1
        hashes = hashcat('MATI', wordlist, mati_names, format, data)
        print(f'For hash {index} of {len(formats)}, found {len(hashes)} hashes.')
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
        
    for hash in found_hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + found_hashes[hash])

def temporary_multiple():
    mati_names = get_mati_names()
    print('found mati names')

    # Only use ascii and _ in the guessing for these paths
    # Not suitable for everything
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    with open('hitman_folder_wordlist.txt', 'r') as f:
        hitman_folder_wordlist = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12).union(hitman_folder_wordlist)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    # bolster from mati names
    for mati_name in mati_names:
        if '_' in mati_name:
            wordlist.add('_'.join(mati_name.split('_')[:-1]))

    #
    found_hashes = hashcat(
        'MATI',
        wordlist,
        mati_names,
        ['[assembly:/_pro/characters/assets/individuals/hokkaido/','/materials/', '].pc_mi'],
        data
    )
    for hash in found_hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + found_hashes[hash])

def smart_wordlist_mapping():
    with open('material_folders.pickle', 'rb') as handle:
        material_folders: List[str] = list(pickle.load(handle))

    print('loaded')
    patterns = find_folder_patterns(material_folders)
    guess_from_folder_patterns(patterns)

# To run on new update
smart_wordlist_mapping()

# EXPLORATORY

# hashcat_multiple
# paths_50 = find_folder_patterns(5, 2)
# print(paths_50)

# temporary_multiple()

# guess_folders()

# have run up to 50
# last_paths = find_folder_patterns(30)
# new_paths = find_folder_patterns(50)
# new_patterns = new_paths.difference(last_paths)
# print(len(new_patterns))
# guess_from_folder_patterns(new_patterns)

# guess_from_folder_patterns(find_folder_patterns())
# Try and guess quixel hash
# print(targeted_hashcat('00B813C4D7BED527', [['[assembly:/_pro/_licensed/quixel/materials/', '/', '/quixel_debris_b.mi].pc_mi']]))

# --------------------------------------------------------

# mati_names = get_mati_names()
# print('found mati names')

# # Only use ascii and _ in the guessing for these paths
# # Not suitable for everything
# allowed = set(string.ascii_lowercase + '_')
# with open('hitman_wordlist.txt', 'r') as f:
#     hitman_wordlist = set([x.strip() for x in f.readlines()])
# with open('wordlist_12.txt', 'r') as f:
#     wordlist_12 = set([x.strip() for x in f.readlines()])
# with open('hitman_folder_wordlist.txt', 'r') as f:
#     hitman_folder_wordlist = set([x.strip() for x in f.readlines()])

# wordlist = hitman_wordlist.union(wordlist_12)
# wordlist = set([word for word in wordlist if set(word) <= allowed])
# wordlist = set(wordlist.union(hitman_folder_wordlist))

# # bolster from mati names
# for mati_name in mati_names:
#     if '_' in mati_name:
#         wordlist.add('_'.join(mati_name.split('_')[:-1]))
#     pieces = re.search(r"^male_reg_(.*)_([^_]*?)_(\d+).mi", mati_name, re.IGNORECASE)
#     if pieces is None:
#         continue
#     wordlist.add(pieces.group(1))
#     wordlist.add(f'male_reg_{pieces.group(1)}')

# formats: List[List[str]] = [
#     # ['[assembly:/_pro/characters/assets/individuals/hokkaido/','/materials/', '].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/individuals/marrakesh/','/materials/', '].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/individuals/italy/','/materials/', '].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/workers/','_/materials/', '].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/individuals/','/materials/', '].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/guards/','/materials/', '].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/_apparel/accessories/','s/materials/','].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/crowd/male/','/materials/','].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/hero/agent47/','/materials/','].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/hero/agent47/outfits/','/materials/','].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/hero/','/agent47/materials/','].pc_mi'],
#     # ['[assembly:/_pro/environment/materials/props/','_','/colombia_road_detail_a.mi].pc_mi'], # wordlist, wordlist
#     # ['[assembly:/_pro/characters/materials/mongoose/','/','].pc_mi'],
#     # ['[assembly:/_pro/characters/materials/','/mongoose/','].pc_mi'],
#     # ['[assembly:/_pro/characters/assets/','/male/casual/materials/','].pc_mi'],
#     ['[assembly:/_pro/characters/assets/','/male/','/materials/male_reg_protester_04_bandana_01.mi].pc_mi].pc_mi']
# ]

# all_found: dict[str, str] = {}
# for format in formats:
#     found_hashes = hashcat(
#         'MATI',
#         wordlist,
#         wordlist,
#         format,
#         data
#     )

#     for hash in found_hashes:
#         all_found[hash] = found_hashes[hash]

# for hash in all_found:
#     print(hash + '.' + data[hash]['type'] + ', ' + all_found[hash])

# -----------------------------------

# allowed = set(string.ascii_lowercase + '_')
# with open('hitman_wordlist.txt', 'r') as f:
#     hitman_wordlist = set([x.strip() for x in f.readlines()])
# with open('wordlist_12.txt', 'r') as f:
#     wordlist_12 = set([x.strip() for x in f.readlines()])
# with open('hitman_folder_wordlist.txt', 'r') as f:
#     hitman_folder_wordlist = set([x.strip() for x in f.readlines()])

# wordlist = hitman_wordlist.union(wordlist_12)
# wordlist = set([word for word in wordlist if set(word) <= allowed])
# wordlist = set(wordlist.union(hitman_folder_wordlist))

# mati_names = get_mati_names()

# # bolster from mati names
# for mati_name in mati_names:
#     if '_' in mati_name:
#         wordlist.add('_'.join(mati_name.split('_')[:-1]))
#     pieces = re.search(r"^male_reg_(.*)_([^_]*?)_(\d+).mi", mati_name, re.IGNORECASE)
#     if pieces is None:
#         continue
#     wordlist.add(pieces.group(1))
#     wordlist.add(f'male_reg_{pieces.group(1)}')

# with open('material_folders.pickle', 'rb') as handle:
#     material_folders: List[str] = list(pickle.load(handle))

# all_folders = set(material_folders)
# for folder in material_folders:
#     all_folders.add(folder.replace('materials', 'material'))
#     all_folders.add(folder.replace('male', 'female'))
#     all_folders.add(folder.replace('male', 'fem'))

# found_hashes = hashcat(
#     'MATI',
#     all_folders,
#     mati_names,
#     ['', '/', '].pc_mi'],
#     data
# )
# for hash in found_hashes:
#     print(hash + '.' + data[hash]['type'] + ', ' + found_hashes[hash])

# -----------------------

# ordered_words = sorted(list(get_mati_names()))
# with open('unknown_mati.txt', 'w') as fp:
#     for word in ordered_words:
#         # write each item on a new line
#         fp.write(word.encode("ascii", errors="ignore").decode() + '\n')