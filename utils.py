from typing import List, TypedDict, Dict, Optional, Any
import hashlib, pickle, itertools, os, subprocess, string

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

'''
To use this file, you will need to copy the hashcat 6.2.4 build from GitHub
(https://github.com/hashcat/hashcat/releases/tag/v6.2.4) and also download
grappigegovert's patch from https://github.com/grappigegovert/hashcat
(https://cdn.discordapp.com/attachments/815577522958893096/909394928403107961/hashcat_ioihash_fixed.zip).

Move the 6.2.4 folder into this one, and from the patch copy in the files to the
modules and OpenCL folders.

Sample command:
hashcat('PRIM', ['test'], ['test'], ['[assembly:/', '.wl2?/', '.prim].pc_prim'])
'''
def hashcat(
    target_type: str,
    left: set[str],
    right: set[str],
    format: List[str],
    data: Optional[Dict[str, HashData]] = None,
    override_hashes: Optional[set[str]] = None,
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
    print(f'Saving temporary wordlists: {len(left)} left, {len(right)} right, targeting {len(possible_hashes)} unknown hashes.')
    with open(f'{hashcat_path}/left.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(left))

    with open(f'{hashcat_path}/right.txt', 'w', encoding='utf-8') as f:
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
    print(' '.join(commands))
    # return {}
    process = subprocess.Popen(' '.join(commands), stdout=subprocess.PIPE, cwd=hashcat_path, shell=True)

    while process.stdout is not None and process.stdout.readable():
        line = process.stdout.readline()
        if not line:
            break

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
            new_hashes[line[0].upper()] = line[1].rstrip()

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