import json, re, pickle, zipfile, os, requests
from typing import List, Dict, Any

print('Starting!')
if not os.path.exists('hashes.json'):
    print("hashes.json doesn't exit. Please extract it from my hitman-hashes-json repo.")
    exit()

print('Downloading hash list...')
try:
    os.remove('./hash_list.txt')
except OSError:
    pass

r = requests.get('https://hitmandb.notex.app/latest-hashes.zip', stream=True)
with open('hash_list.zip', 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

with zipfile.ZipFile('hash_list.zip') as zf:
    zf.extractall('./')

os.remove('hash_list.zip')
print('Extracted hash_list.txt.')

print('Building hashes pickle...')
with open('hashes.json', 'r') as f:
    data = json.load(f)
    print('Loaded hashes.json.')

with open('./hashes.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Done.')

print('Building reverse pickle...')
reverse: Dict[str, List[str]] = dict()
for hash in data:
    for depends in data[hash]['depends']:
        depends = str(depends)
        if depends not in reverse:
            reverse[depends] = []
        reverse[depends].append(hash)

with open('./reverse.pickle', 'wb') as handle:
    pickle.dump(reverse, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Done.')

print('Building pattern pickes...')
# Build patterns
texture_folders = set([])
texture_suffixes = set([])
material_folders = set([])
template_folders = set([])
wwev_folders = set([])
mrtn_folders = set([])
with open('hash_list.txt', 'r') as f:
    # completion
    f.readline()
    # hashes count
    f.readline()
    # version number
    f.readline()

    for line in f.readlines():
        split = line.split(',', 1)
        ioi_string = split[1].rstrip()
        extension = split[0][-4:]
        if extension == 'TEXT':
            if 'texture' in ioi_string:
                info = re.search(r"^(.*)/([^\\]*)\.texture(.*)$", ioi_string, re.IGNORECASE)
                if info is None:
                    print(ioi_string)
                    break
                else:
                    texture_folders.add(info.group(1))
                    texture_suffixes.add(info.group(3))
        elif extension == 'MATI':
            if 'assembly' in ioi_string:
                info = re.search(r"^(.*)/[^\\]*\.mi\]\.pc_mi$", ioi_string, re.IGNORECASE)
                if info is None:
                    print(ioi_string)
                    break
                else:
                    material_folders.add(info.group(1))

        elif extension == 'TBLU' or extension == 'TEMP':
            if 'assembly' in ioi_string:
                # [assembly:/_pro/environment/templates/backdrop/ground/backdrop_ground_skunk_a.template?/backdrop_ground_skunk_a.entitytemplate].pc_entityblueprint
                info = re.search(r"^(.*\.template\?).*$", ioi_string, re.IGNORECASE)
                if info is None:
                    continue
                else:
                    template_folders.add(info.group(1))

        elif extension == 'WWEV':
            if 'assembly' in ioi_string:
                # [assembly:/sound/wwise/exportedwwisedata/events/ambience_events/amb_marrakesh/amb_marrakesh_elements/amb_e_market/play_amb_e_lamp_jangle_array.wwiseevent].pc_wwisebank
                info = re.search(r"^(.*\/)[^\/]*.wwiseevent.*$", ioi_string, re.IGNORECASE)
                if info is None:
                    continue
                else:
                    wwev_folders.add(info.group(1))

        elif extension == 'MRTN':
            if 'assembly' in ioi_string:
                # [assembly:/animationnetworks/hitman01/disguiseacts/safezones/s03_hm_lip_sit_mindcontrolexperiment.aln].pc_rtn
                info = re.search(r"^(.*\/)[^\/]*.aln.*$", ioi_string, re.IGNORECASE)
                if info is None:
                    continue
                else:
                    mrtn_folders.add(info.group(1))


with open('./texture_folders.pickle', 'wb') as handle:
    pickle.dump(texture_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./texture_suffixes.pickle', 'wb') as handle:
    pickle.dump(texture_suffixes, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./material_folders.pickle', 'wb') as handle:
    pickle.dump(material_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./template_folders.pickle', 'wb') as handle:
    pickle.dump(template_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./wwev_folders.pickle', 'wb') as handle:
    pickle.dump(wwev_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./mrtn_folders.pickle', 'wb') as handle:
    pickle.dump(mrtn_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Building wordlist pickles...')

_end = '_end_'

def build_trie(words: List[str]):
    trie: Dict[str, Any] = dict()
    for word in words:
        current_dict = trie
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return trie

# convert this to a trie for quick lookups
with open('wordlist_3.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]
    trie = build_trie(words)
    with open('./w3_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('wordlist_1.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]
    trie = build_trie(words)
    with open('./w1_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('wordlist_12.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]
    trie = build_trie(words)
    with open('./w12_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Done. Closing!')
