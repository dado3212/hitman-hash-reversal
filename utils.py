from typing import List, TypedDict, Dict
import hashlib, pickle

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