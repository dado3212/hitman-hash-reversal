import pickle, itertools
from utils import ioi_string_to_hex

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

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
        hash = split[0]
        extension = split[0][-4:]
        if extension == 'CRMD':
            if hash in data:
                print(hash + ',' + data[hash]['name'])
            elif len(ioi_string) > 0:
                print('Not in H3: ' + hash + ',' + ioi_string)

print("guess attempt")

with open('wordlist_1.txt', 'r') as f:
    words = [x.strip() for x in f.readlines()]

match = {
    '0003B0816C564D99': 'scene_flamingo_benchmark_intel_crowd_intel',
    '00111D9EBAC7FDCA': 'scene_flamingo_boardwalk',
    '00F694A4AD419A32': 'scene_flamingo_center',
    '008E37C80599C035': 'scene_flamingo_crowd pitbuilding',
    '009EB60D7DDB492C': 'scene_flamingo_crowd_startingarea',
    '00C809B60C0358B2': 'scene_flamingo_paddock',
}

for word in words:
    file = f"[assembly:/_pro/scenes/missions/miami/scene_flamingo_{word}.crmd].pc_crmd"
    hash = ioi_string_to_hex(file)
    if hash in match:
        print(hash + ',' + file)

pieces = ['benchmark', 'intel', 'crowd', 'cores', '6cores', '8cores', '10cores', '12cores', 'boardwalk', 'center','pitbuilding', 'startingarea', 'paddock']

for word_count in range(1, 8): # 8
    combinations = list(itertools.permutations(pieces, word_count))
    print(len(combinations))
    for combo in combinations:
        guesses = [
            ' '.join(combo),
            '_'.join(combo),
            '_'.join(combo[:-1]) + ' ' + combo[-1]
        ]
        for guess in guesses:
            file = f"[assembly:/_pro/scenes/missions/miami/scene_flamingo_{guess}.crmd].pc_crmd"
            hash = ioi_string_to_hex(file)
            if hash in match:
                print(hash + ',' + file)
                break


# [assembly:/_pro/scenes/missions/miami/scene_flamingo_scene_flamingo_benchmark_intel_crowd_intel.crmd].pc_crmd