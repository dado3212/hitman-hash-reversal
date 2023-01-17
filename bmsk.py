from utils import ioi_string_to_hex, load_data, hashcat
import re, string
from typing import List, Dict

data = load_data()
print('loaded')

def from_hashcat():
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])

    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    # The format is
    # maybe carry?
    # hm_[run,sneak,stand,sneakwalk,vault,walk]_[leftarm,rightarm,both_arms]_[item]
    # futz_with_hashcat()
    actions = ['run', 'sneak', 'stand', 'sneakwalk', 'vault', 'walk']
    arms = ['leftarm', 'rightarm', 'both_arms']

    formats: List[List[str]] = [
        # [assembly:/animations/bonemasks/hm_walk_rightarm_fireextinguisher.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask
        # ['[assembly:/animations/bonemasks/hm_walk_', '_', '.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask']
    ]
    for arm in arms:
        formats.append(['[assembly:/animations/bonemasks/hm_', f'_{arm}_', '.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask'])

    found_hashes: Dict[str, str] = {}
    for format in formats:
        hashes = hashcat('BMSK', set(actions), wordlist, format, data)
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
    for hash in found_hashes:
        print(hash + '.BMSK, ' + found_hashes[hash])

def alt_hashcat():
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])

    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    # The format is
    # maybe carry?
    # hm_[run,sneak,stand,sneakwalk,vault,walk]_[leftarm,rightarm,both_arms]_[item]
    # futz_with_hashcat()
    actions = ['run', 'sneak', 'stand', 'sneakwalk', 'vault', 'walk']
    arms = ['leftarm', 'rightarm', 'both_arms']

    formats: List[List[str]] = [
        # [assembly:/animations/bonemasks/hm_walk_rightarm_fireextinguisher.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask
        # ['[assembly:/animations/bonemasks/hm_walk_', '_', '.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask']
    ]
    for arm in arms:
        for action in actions:
            formats.append([f'[assembly:/animations/bonemasks/hm_{action}_{arm}_', '', '.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask'])

    found_hashes: Dict[str, str] = {}
    for format in formats:
        hashes = hashcat('BMSK', wordlist, wordlist, format, data)
        for hash in hashes:
            found_hashes[hash] = hashes[hash]
    for hash in found_hashes:
        print(hash + '.BMSK, ' + found_hashes[hash])

def futz_with_hashcat():
    known: List[str] = []
    for hash in data:
        if data[hash]['type'] == 'BMSK':
            if len(data[hash]['name']) > 0:
                relevant = re.search(r"\[assembly:/animations/bonemasks/(.*).bonemask\]\(assembly:/geometry/characters/_export_rigs/biped~~.xml\).pc_bonemask",data[hash]['name'], re.IGNORECASE)
                assert relevant is not None
                known.append(relevant.group(1))

    known = sorted(known)
    for k in known:
        print(k)
    exit()

    for possible in known:
        file_name = f"[assembly:/animations/bonemasks/{possible}.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask"
        possible_hash = ioi_string_to_hex(file_name)
        if possible_hash in data:
            if not data[possible_hash]['correct_name']:
                print(possible_hash + ',' + file_name)

def dump_stuff():
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])

    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    # Gotten from futz_with_hashcat
    prefixes: List[List[str]] = [
        ['carry_lh_', '_'],
        ['hm_cover_','_r_arm'],
        ['hm_rightarm_',''],
        ['hm_run_rightarm_',''],
        ['hm_sneak_rightarm_',''],
        ['hm_sneakwalk_leftarm_',''],
        ['hm_stand_reload_1h_',''],
        ['hm_stand_rightarm_',''],
        ['hm_walk_rightarm_',''],
    ]
    for prefix in prefixes:
        for word in wordlist:
            file_name = f"[assembly:/animations/bonemasks/{prefix[0]}{word}{prefix[1]}.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask"
            possible_hash = ioi_string_to_hex(file_name)
            if possible_hash in data and not data[possible_hash]['correct_name']:
                    print(possible_hash + ',' + file_name)

def from_futzing():
    # The general approach is to see if we can futz a known format into left hand/right hand and find anything
    bonemasks: List[str] = []
    known: List[str] = []
    for hash in data:
        if data[hash]['type'] == 'BMSK':
            bonemasks.append(hash)
            if len(data[hash]['name']) > 0:
                relevant = re.search(r"\[assembly:/animations/bonemasks/(.*).bonemask\]\(assembly:/geometry/characters/_export_rigs/biped~~.xml\).pc_bonemask",data[hash]['name'], re.IGNORECASE)
                assert relevant is not None
                known.append(relevant.group(1))

    def add_to_list(orig: List[str], left: str, right: str, both_ways: bool = True) -> List[str]:
        new: List[str] = []
        for l in orig:
            new.append(l)
            new.append(l.replace(left, right))
            if both_ways:
                new.append(l.replace(right, left))
        return list(set(new))

    known = add_to_list(known, 'left', 'right')
    known = add_to_list(known, 'left', 'l', False)
    known = add_to_list(known, 'right', 'r', False)
    known = add_to_list(known, 'arm', 'leg')
    known = add_to_list(known, 'arm', 'hand')
    known = add_to_list(known, 'hand', 'leg')
    known = add_to_list(known, 'rh', 'lh')
    known = add_to_list(known, '_r', '_l')
    known = add_to_list(known, 'r_', 'l_')
    known = add_to_list(known, '2h', '1h')
    known = add_to_list(known, 'both', 'left')
    known = add_to_list(known, 'both_', 'left')
    known = add_to_list(known, 'both', 'right')
    known = add_to_list(known, 'both_', 'right')
    known = add_to_list(known, 'arms', 'arm')
    known = add_to_list(known, 'legs', 'leg')

    iterable = known[::]
    for k in iterable:
        known.append('inverse_' + k)
        if ('inverse_' in k):
            known.append(k.replace('inverse_', ''))

    known = list(set(known))

    known = sorted(known)

    for k in known:
        print(k)

    for possible in known:
        file_name = f"[assembly:/animations/bonemasks/{possible}.bonemask](assembly:/geometry/characters/_export_rigs/biped~~.xml).pc_bonemask"
        possible_hash = ioi_string_to_hex(file_name)
        if possible_hash in data:
            if not data[possible_hash]['correct_name']:
                print(possible_hash + ',' + file_name)


alt_hashcat()