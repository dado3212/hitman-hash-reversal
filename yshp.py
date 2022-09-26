import string
from utils import ioi_string_to_hex
from typing import List, Dict
import itertools

match = {
    '00805A591F1A33EE': 1,
    '00777786A3E3D47B': 2,
    '00B476579A770AB6': 3,
}

def foo(l: str, str_length: int):
     yield from itertools.product(*([l] * str_length)) 

for x in foo(string.ascii_lowercase, 5):
    file = f"[assembly:/_pro/characters/prototypes/ragdoll_physx/ragdoll_{''.join(x)}.repx].pc_physsys"
    hash = ioi_string_to_hex(file)
    if hash in match:
        print(hash + ',' + file)
