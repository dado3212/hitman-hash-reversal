from typing import List, TypedDict, Dict, Optional, Any
import hashlib, pickle, itertools, os, subprocess, string, functools

class HashData(TypedDict):
    name: str
    type: str
    depends: List[str]
    chunks: List[str]
    correct_name: bool
    hex_strings: List[str]
    country: str

def hash_to_hex(hash: int) -> str:
    return format(hash, 'x').upper().rjust(16, '0')

def hex_to_hash(hex: str) -> int:
    return int(hex.lstrip('0'), 16)

def ioi_string_to_hex(path: str) -> str:
    raw = hashlib.md5(path.encode()).hexdigest().upper()
    return '00' + raw[2:16]

def load_data() -> Dict[str, HashData]:
    with open('hashes.pickle', 'rb') as handle:
        return pickle.load(handle)
    
def location_list() -> set[str]:
    return [
        'sniperchallenge',
        'versus',
        'base',
        'boot',
        'boot_base',
        'qloc',
        'reference',
        'cinematic',
        'tutorial',
        'polarbear',
        'thefacility',
        'the facility',
        'greenland',
        'paris',
        'peacock',
        'france',
        'italy',
        'sapiensa',
        'sapienza',
        'serpienza',
        'coastaltown',
        'coastal_town',
        'octopus',
        'marrakesh',
        'consulate',
        'spider',
        'bangkok',
        'tiger',
        'colorado',
        'colorado_2',
        'bull',
        'hokkaido',
        'snowcrane',
        'newzealand',
        'newzea',
        'sheep',
        'miami',
        'flamingo',
        'colombia',
        'hippo',
        'mumbai',
        'mongoose',
        'india',
        'northamerica',
        'vermont',
        'suburbia',
        'skunk',
        'northsea',
        'theark',
        'sgail',
        'theisland',
        'island',
        'magpie',
        'greedy',
        'raccoon',
        'thebank',
        'newyork',
        'bank',
        'opulent',
        'stingray',
        'maldives',
        'hawk',
        'austria',
        'salty',
        'seagull',
        'harbour',
        'caged',
        'falcon',
        'prison',
        'golden',
        'gecko',
        'dubai',
        'edgy',
        'fox',
        'berlin',
        'germany',
        'wet',
        'rat',
        'chongqing',
        'china',
        'ancestral',
        'bulldog',
        'dartmoor',
        'uk',
        'england',
        'elegant',
        'llama',
        'mendoza',
        'argentina',
        'trapped',
        'wolverine',
        'carpathian',
        'romania',
        'snug',
        'vanilla',
        'rocky',
        'dugong',
    ]


# Takes in a json_data and returns a list of strings
def extract_strings_from_json(json_data: Any) -> set[str]:
    # Check if it's a string
    result: set[str] = set()
    if isinstance(json_data, str):
        return set([json_data])
    elif isinstance(json_data, list):
        for key in json_data: #pyright: ignore [reportUnknownVariableType]
            options = extract_strings_from_json(key)
            result = result.union(options)
    elif isinstance(json_data, dict):
        for key in json_data: #pyright: ignore [reportUnknownVariableType]
            options = extract_strings_from_json(json_data[key]) #pyright: ignore [reportUnknownArgumentType]
            result = result.union(options)
    return result

def _combine_wordlists(wordlists: List[set[str]], joins: List[str]) -> set[str]:
    if len(wordlists) == 1:
        return wordlists[0]
    # TODO: Inline more of them, for now just handle 1 and 2 manually
    elif len(wordlists) == 2:
        glue = joins[0]
        return set([f'{a}{glue}{b}' for a in wordlists[0] for b in wordlists[1]])
    # Have some pseudocode but it's not actually supported right now
    else:
        print('Yikes')
        return set()
        # starts: set[str] = set()
        # for combo in itertools.product(*first_bits):
        #     word = combo[0]
        #     for i in range(1, len(wordlists) - 1):
        #         word += format[i] + combo[i]
        #     starts.add(word)

# This will crash your computer if you run it with multiple large wordlists
def hashcat_multiple(
    target_type: str,
    wordlists: List[set[str]],
    format: List[str],
    data: Optional[Dict[str, HashData]] = None,
    override_hashes: Optional[set[str]] = None,
) -> Dict[str, str]:
    print('This will crash your computer')
    exit()
    if len(wordlists) < 2:
        print('If you only have one wordlist just run it with ioi_string_to_hash.')
        exit()
    # Just forward this
    if len(wordlists) == 2:
        return hashcat(target_type, wordlists[0], wordlists[1], format, data, override_hashes)
    # Confirm that format is wellformed
    if len(format) != len(wordlists) + 1:
        print(f'The format must contain {len(wordlists)+1} values to fully wrap the {len(wordlists)} wordlists.')
        exit()

    # Determine where to split the wordlists
    min_total_words = None
    min_pos = 0
    wordlist_sizes = [len(x) for x in wordlists]
    for i in range(1, len(wordlists)):
        first_chunk = functools.reduce(lambda a, b: a * b, wordlist_sizes[:i])
        second_chunk = functools.reduce(lambda a, b: a * b, wordlist_sizes[i:])
        if min_total_words is None or (first_chunk + second_chunk) < min_total_words:
            min_total_words = first_chunk + second_chunk
            min_pos = i

    first_chunk = wordlists[:min_pos]
    second_chunk = wordlists[min_pos:]

    print(f'Splitting on {min_pos}')

    first_wordlist = _combine_wordlists(first_chunk, format[1:min_pos])
    second_wordlist = _combine_wordlists(second_chunk, format[min_pos+1:-1])

    print('Created wordlists')

    return hashcat(target_type, first_wordlist, second_wordlist, [format[0], format[min_pos], format[-1]], data, override_hashes)

def hashcat(
    target_type: str,
    left: set[str],
    right: set[str],
    format: List[str],
    data: Optional[Dict[str, HashData]] = None,
    override_hashes: Optional[set[str]] = None,
    silence: bool = False,
) -> Dict[str, str]:
    # Confirm that format is wellformed
    if len(format) != 3:
        print('The format must contain three values, one for before the first set, then in-between the sets, then after the second set.')
        exit()

    # TODO: Flag this in README
    hashcat_path = 'hashcat-6.2.4'
    # Confirm that the path exists
    if not os.path.exists(hashcat_path):
        print('Hashcat is not properly setup. See utils.py for instructions.')
        exit()
    # Clear the output file
    open(f'{hashcat_path}/{target_type}-cracked.txt', 'w').close()

    # Filter the hash list down to what we're targeting. Without this the target
    # hash list will be redundant, and also too big.
    if override_hashes is not None:
        possible_hashes = override_hashes
    else:
        # If you happen to be generating lists from raw wordlists without loading
        # data, then we will need to load it to get our target hashes
        if (data is None):
            data = load_data()
        possible_hashes = [hash for hash in data if data[hash]['type'] == target_type and not data[hash]['correct_name']]
    if not silence:
        print(f'Saving temporary wordlists: {len(left)} left, {len(right)} right, targeting {len(possible_hashes)} unknown hashes.')
    with open(f'{hashcat_path}/left.txt', 'w', encoding='utf-8', buffering=1) as f:
        f.write("\n".join(left))

    with open(f'{hashcat_path}/right.txt', 'w', encoding='utf-8', buffering=1) as f:
        f.write("\n".join(right))

    with open(f'{hashcat_path}/hashes.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(possible_hashes))

    commands = [
        'hashcat.exe',
        '-m', '92100', # Glacier hashing algorithm, IOI modified version of MD5
        '-a', '1', # combination attack using the two dictionaries
    ]
    left_chunk = format[0]
    middle_chunk = format[1]
    right_chunk = format[2]
    # Modifications to the left dictionary
    if len(left_chunk) > 0 or len(middle_chunk) > 0:
        commands.append('-j')
        hashcat_command = ''
        for l in left_chunk[::-1]:
            hashcat_command += '^' + l
        for m in middle_chunk:
            hashcat_command += '$' + m
        commands.append(f'"{hashcat_command}"')
    # Modifications to the right dictionary
    if len(right_chunk) > 0:
        commands.append('-k')
        hashcat_command = ''
        for r in right_chunk:
            hashcat_command += '$' + r
        commands.append(f'"{hashcat_command}"')

    commands.extend([
        'hashes.txt', # the hashlist that we're trying to crack
        'left.txt', # the left dictionary
        'right.txt', # the right dictionary
        '--outfile-autohex-disable', # print them out in real english, not hashes
        '--status', # automatically display progress
        '--status-timer', '3', # update the progress every 3 seconds
        '--force', # get in the robot shinji
        '--potfile-disable', # we don't want to save the hashes (for now)
        '-o', f'{target_type}-cracked.txt', # cracked hashes
    ])
    if not silence:
        print(' '.join(commands))
    process = subprocess.Popen(' '.join(commands), stdout=subprocess.PIPE, cwd=hashcat_path, shell=True)

    while process.stdout is not None and process.stdout.readable():
        line = process.stdout.readline()
        if not line:
            break

        if not silence:
            line = line.strip().decode('utf-8')
            if line.startswith('Time.Estimated') or line.startswith('Progress') or line.startswith('Candidates.#1'):
                print(line)
            elif line.startswith('Hardware.Mon.#1'):
                print(line + '\n')

    # Read the new hashes
    new_hashes: Dict[str, str] = {}
    with open(f'{hashcat_path}/{target_type}-cracked.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(':', 1)
            solution = line[1].rstrip()
            # TODO: Current bug in hashcat, but while these are *cracked*
            # the output isn't correct. For now, silently drop them. WE SHOULD 
            # FIX THIS.
            if len(solution) == 256:
                continue
            new_hashes[line[0].upper()] = solution

    return new_hashes

def targeted_hashcat(
    hash: str,
    formats: List[List[str]],
) -> Optional[str]:
    # Only use ascii and _ in the guessing for these paths
    # Not suitable for everything
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])
    
    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])
        
    target_hashes = set([hash])
    for format in formats:
        hashes = hashcat('targeted', wordlist, wordlist, format, override_hashes=target_hashes)
        if hash in hashes:
            return hashes[hash]
    return None

'''
Takes in a list of folder paths. The function treats this as a set of tokens
delimeted by `/` and goes through to finds patterns where one token
appears to change (and thus could be ran through a wordlist). You can set two 
parameters to control output.

Input:
 - unique_threshold: If a certain token has more than this many options then
                     it becomes a wildcard. <= this threshold the function will
                     spit out a format for each of the options. THIS ONLY 
                     APPLIES IF THERE ARE DUPLICATES. A list of formats with no
                     duplicates will always be treated as a wildcard.

 - max_wildcards:    Any format with more wildcards will be filtered out.

Output:
A unique set of strings with the changeable token replaced with an *. Ex:
set([
    '[assembly:/_pro/items/textures/*/'
])
'''
def find_folder_patterns(templates: List[str], unique_threshold: int = 5, max_wildcards: int = 1) -> set[str]:
    # This code requires that the templates not be suffixed with `/`
    templates = [template.removesuffix('/') for template in templates]
    unique_formats: set[str] = set()
    for i in range(len(templates)):
        folder1 = templates[i].split('/')
        
        # We're going to guess that this is a format
        num = len(folder1)
        format: List[List[str]] = [[x] for x in folder1]
        # Initialize to 1 because folder1 matches it by default
        num_matching = 1

        # We don't need to iterate through anything earlier because it will
        # already be considered as a format
        for j in range(i + 1, len(templates)):
            folder2 = templates[j].split('/')
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
                        # Currently defaulting to 5 and comparing with other
                        # lengths
                        if len(unique) <= unique_threshold:
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
            if 1 <= wildcard_count <= max_wildcards:
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

def crack(
    target: str,
    base: str,
    suffix: str,
    wordlist: List[str],
    required_words: List[str],
    min_words: int,
    max_words: int,
) -> Optional[str]:
    # Just in case I messed up
    wordlist = list(set(wordlist))
    required_words = list(set(required_words))
    num_required_words = len(required_words)
    if min_words < num_required_words:
        print(f'You are requiring {num_required_words} words but have a min words of {min_words}.')
        return None
    

    for num_words in range(min_words, max_words + 1):
        print(f'Checking {num_words} words.')
        word_choices: List[List[str]] = []
        for _ in range(num_words - num_required_words):
            word_choices.append(wordlist)
        for _ in range(num_required_words):
            word_choices.append(required_words)
        # in between any two words you can choose to put one of the following:
        # '/', '_', ''. Therefore with num_words there are num_words - 1 slots
        spacing: List[List[str]] = []
        if num_words > 1:
            for _ in range(num_words - 1):
                spacing.append(['/', '_', ''])
        for words in itertools.product(*word_choices):
            if num_words == 1:
                file = base + words[0] + suffix
                hash = ioi_string_to_hex(file)
                if hash == target:
                    return file
            for spacers in itertools.product(*spacing):
                file = base + words[0]
                for word_index in range(1, num_words):
                    file += spacers[word_index - 1] + words[word_index]
                file = file + suffix
                hash = ioi_string_to_hex(file)
                if hash == target:
                    return file
    return None