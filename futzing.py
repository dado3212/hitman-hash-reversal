from utils import ioi_string_to_hex
import pickle, string, re, itertools
from typing import Dict, List, Tuple

def replaceable_sections(ioi_string: str) -> List[Tuple[str, bool]]:
    pieces: List[Tuple[str, bool]] = []
    curr_index = 0
    for m in re.finditer(r"_([\d]+|[a-z])[\./_]", ioi_string):
        pieces.append((ioi_string[curr_index:m.start(0) + 1], False))
        pieces.append((ioi_string[m.start(0) + 1:m.end(1)], True))
        curr_index = m.end(1)
    pieces.append((ioi_string[curr_index:], False))
    return pieces

def num_alts(sections: List[Tuple[str, bool]]) -> int:
    total = 1
    for section in sections:
        if section[1] == True:
            if section[0].isalpha():
                total *= 26
            else:
                if len(section[0]) == 1:
                    total *= 17
                elif len(section[0]) == 2:
                    if (section[0][0] == '0'):
                        total *= 17
                    else:
                        total *= 100
                else:
                    # currently ignored
                    continue
    # The original one
    return total - 1


def replacements(sections: List[Tuple[str, bool]]) -> set[str]:
    if len(sections) == 0:
        return set()
    elif len(sections) == 1:
        return set(sections[0][0])
    else:
        options: set[str] = set()
        for section_index in range(0, len(sections)):
            section = sections[section_index]
            # Handle the first replaceable section
            if section[1] == True:
                # If it's alphabetical
                if section[0].isalpha():
                    for replacement_letter in string.ascii_lowercase:
                        new = [*sections[:section_index], (replacement_letter, False), *sections[section_index+1:]]
                        options = options.union(replacements(new))
                    return options
                # Assume it's numeric
                else:
                    if len(section[0]) == 1:
                        number_replacements = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','47']
                    elif len(section[0]) == 2:
                        if section[0][0] == '0':
                            number_replacements = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','47']
                        else:
                            number_replacements = [''.join(x) for x in itertools.product([d for d in '0123456789'], repeat=2)]
                    else:
                        continue
                    for replacement_number in number_replacements:
                        new = [*sections[:section_index], (replacement_number, False), *sections[section_index+1:]]
                        options = options.union(replacements(new))
                    return options
        return {''.join([x[0] for x in sections])}
            
if __name__ == '__main__':

    with open('hashes.pickle', 'rb') as handle:
        data = pickle.load(handle)

    print('loaded')

    # Length of the number strings
    # {2: 55288, 1: 4475, 3: 372129, 4: 70, 5: 46, 6: 2}
    options: Dict[int, List[str]] = {}

    unique_found: Dict[str, str] = {}

    hashes = list(data.keys())
    num_hashes = len(hashes)
    old_perc = -1

    # Number futzing
    for i in range(num_hashes):
        hash = hashes[i]
        new_perc = round(i * 100.0 / num_hashes, 2)
        if new_perc > old_perc:
            old_perc = new_perc
            print(str(new_perc) + '% - ' + str(i))
        name = data[hash]['name']
        if len(name) > 0:
            sections = replaceable_sections(name)
            num_alt_strings = num_alts(sections)
            # Try and avoid huge fanouts for now
            if num_alt_strings > 0 and num_alt_strings < 100000:
                possible_names = replacements(sections)
                for possible_name in possible_names:
                    new_hash = ioi_string_to_hex(possible_name)
                    if new_hash in data and not data[new_hash]['correct_name'] and new_hash not in unique_found:
                        print(new_hash + ',' + possible_name)
                        unique_found[new_hash] = possible_name
            elif num_alt_strings > 0:
                continue
                # print("Skipping " + name)

    for h in unique_found:
        print(h + ',' + unique_found[h])

# TODO - we should be able to futz name/desc/title