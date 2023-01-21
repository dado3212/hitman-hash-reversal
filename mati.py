from utils import load_data, hashcat, targeted_hashcat
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

def find_folder_patterns() -> set[str]:
    with open('material_folders.pickle', 'rb') as handle:
        material_folders: List[str] = list(pickle.load(handle))

    print('loaded')

    unique_formats: set[str] = set()
    for i in range(len(material_folders)):
        folder1 = material_folders[i].split('/')
        
        # We're going to guess that this is a format
        num = len(folder1)
        format: List[List[str]] = [[x] for x in folder1]
        # Initialize to 1 because folder1 matches it by default
        num_matching = 1

        # We don't need to iterate through anything earlier because it will
        # already be considered as a format
        for j in range(i + 1, len(material_folders)):
            folder2 = material_folders[j].split('/')
            # for now only look at them if they're the same length
            # TODO: could potentially be expanded to levenshtein in the future
            if len(folder2) != num:
                continue
        
            differences = 0
            changes: Dict[int, str] = {}
            for pos in range(num):
                if folder2[pos] == folder1[pos]:
                    # In this case it's matching the format
                    continue
                else:
                    # Something's different. Store the difference in case the 
                    # total difference ends up being small enough
                    differences += 1
                    changes[pos] = folder2[pos]
            
            # For now only look at formats with two changes. There may be
            # real paths with more, but not sure what they are
            # TODO: run this with 3 and compare the diffset
            if differences <= 2:
                for change_index in changes:
                    format[change_index].append(changes[change_index])
                num_matching += 1

        # This means the format matches more than one thing
        if num_matching > 1:
            refined_format: List[List[str]] = []
            wildcard_count = 0
            for element in format:
                if len(element) == 1:
                    refined_format.append([element[0]])
                else:
                    # Check if this is different for everything
                    unique = set(element)
                    if len(unique) == len(element):
                        # TODO: Maybe want to check if this is only two or something
                        refined_format.append(['*'])
                        wildcard_count += 1
                    else:
                        # kind of arbitrary tbh
                        # maybe want to compare to length of elements in terms
                        # of how much it compresses
                        if len(unique) <= 5:
                            refined_format.append([x for x in unique])
                        else:
                            refined_format.append(['*'])
                            wildcard_count += 1
                            # can revisit this in the future
                            # usually this is stuff like 'paris' and 'marrakesh'
                            # print(len(element))
                            # print(len(unique))
                            # print(element)
                            # print(format)
                            # exit()

            # for now only do one wildcard
            if wildcard_count == 1:
                result: List[str] = ['']
                for elem in refined_format:
                    if len(elem) == 1:
                        result = [prefix + elem[0] + '/' for prefix in result]
                    else:
                        temp_result: List[str] = []
                        for word in elem:
                            for prefix in result:
                                temp_result.append(prefix + word + '/')
                        result = temp_result
                unique_formats = unique_formats.union(result)
    return unique_formats      
        
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
        ['[assembly:/_pro/characters/assets/crowd/male/','/materials/','].pc_mi'],
        # TODO: Can do more gender futzing
        ['[assembly:/_pro/characters/assets/crowd/female/','/materials/','].pc_mi'],
    ]

    found_hashes: Dict[str, str] = {}
    for format in formats:
        hashes = hashcat('MATI', wordlist, mati_names, format, data)
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
        
    for hash in found_hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + found_hashes[hash])

def find_folder_patterns_and_guess():
    patterns = find_folder_patterns()
    print('found patterns')

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

    found_hashes: Dict[str, str] = {}
    for format in formats:
        hashes = hashcat('MATI', wordlist, mati_names, format, data)
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
        
    for hash in found_hashes:
        print(hash + '.' + data[hash]['type'] + ', ' + found_hashes[hash])

find_folder_patterns_and_guess()
# Try and guess quixel hash
# print(targeted_hashcat('00B813C4D7BED527', [['[assembly:/_pro/_licensed/quixel/materials/', '/', '/quixel_debris_b.mi].pc_mi']]))