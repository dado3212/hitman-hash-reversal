from typing import List, TypedDict, Dict, Optional
import hashlib, pickle, itertools

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