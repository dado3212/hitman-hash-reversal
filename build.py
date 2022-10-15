import json, re, pickle, zipfile, os, requests
from typing import List, Dict

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

with open('./texture_folders.pickle', 'wb') as handle:
    pickle.dump(texture_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./texture_suffixes.pickle', 'wb') as handle:
    pickle.dump(texture_suffixes, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./material_folders.pickle', 'wb') as handle:
    pickle.dump(material_folders, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Done. Closing!')
