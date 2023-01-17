from utils import ioi_string_to_hex, load_data
import re, string

data = load_data()

def targeted_guessing():
    '''
    Unknown
    | ERES | TEMP | TBLU |
    | 001F8CB0FC47624B | 005B5E3A0F9F28CF | 00F93C172854DF3D | fx_md_env_stone_concrete_intel
    | 006D43618F5FD0C8 | 009FF3D42323A204 | 0082310ABD81354D | fx_md_env_stone_concrete (kind of exists)
    | 0006AA0D8B4A2951 | 00A1A72A3C3BB347 | 00F0B889CB520543 | fx_md_env_stone_tiles (kind of exists) -> literally the same file as the known one
    Known
    | 00B8E792F4463362 | 004F956E5876378B | 00CA829E0D075E5E |
    | 0046D368C7FEC9B6 | 00C2B1DA5587F2A0 | 0032F68C3F4179E3 | [assembly:/_pro/effects/templates/materialdescriptors/fx_md_env_stone_tiles.template?/fx_md_env_stone_tiles.entitytemplate].pc_entityresource
    '''
    stone_tiles = '[assembly:/_pro/effects/templates/materialdescriptors/fx_md_env_stone_tiles.template?/fx_md_env_stone_tiles.entitytemplate].pc_entityresource'
    for i in range(0, len(stone_tiles) + 1):
        for num in ['0','1','2','3','4','5','6','7','8','9', 'clean', 'clear', 'blood', 'bloody']:
            path = stone_tiles[0:i] + num + stone_tiles[i:]
            if ioi_string_to_hex(path) == '00F0B889CB520543':
                print(path)
            path = stone_tiles[0:i] + '_' + num + stone_tiles[i:]
            if ioi_string_to_hex(path) == '00F0B889CB520543':
                print(path)

    # Only use ascii and _ in the guessing for these paths
    # Not suitable for everything
    allowed = set(string.ascii_lowercase + '_')
    with open('hitman_wordlist.txt', 'r') as f:
        hitman_wordlist = set([x.strip() for x in f.readlines()])
    with open('wordlist_12.txt', 'r') as f:
        wordlist_12 = set([x.strip() for x in f.readlines()])

    wordlist = hitman_wordlist.union(wordlist_12)
    wordlist = set([word for word in wordlist if set(word) <= allowed])

    for word in wordlist:
        path = f'[assembly:/_pro/effects/templates/materialdescriptors/fx_md_env_stone_tiles_{word}.template?/fx_md_env_stone_tiles_{word}.entitytemplate].pc_entityresource'
        hash = ioi_string_to_hex(path)
        if hash in data and not data[hash]['correct_name']:
            print(hash + ', ' + path)


for hash in data:
    if data[hash]['type'] == 'ERES':
        if not data[hash]['correct_name']:
            for d in data[hash]['depends']:
                if d in data and data[d]['type'] == 'TEMP':
                    # Try this
                    relevant = re.search(r"(.*)\..*",data[d]['name'], re.IGNORECASE)
                    if relevant is None:
                        filename = f"[assembly:/_pro/effects/templates/materialdescriptors/{data[d]['name']}.template?/{data[d]['name']}.entitytemplate].pc_entityresource"
                        print(data[d]['name'])
                    else:
                        filename = f"{relevant.group(1)}.pc_entityresource"
                    if ioi_string_to_hex(filename) == hash:
                        print(hash, filename)
