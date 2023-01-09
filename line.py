from utils import ioi_string_to_hex, load_data
import pickle, re
from typing import List, Tuple, Dict

data = load_data()

with open('reverse.pickle', 'rb') as handle:
    reverse: Dict[str, str] = pickle.load(handle)

def extract_setpieces_from_locrs():
    for hash in ['0082FCF9BF0CA18E']:
        if data[hash]['type'] == 'LOCR':
            for hex_string in data[hash]['hex_strings']:
                guesses: set[str] = set()
                for x in [hex_string.lower().replace(' ', '_'), hex_string.lower().replace(' ', '')]:
                    guesses.add(f'[assembly:/localization/hitman6/conversations/ui/pro/setpieces.sweetmenutext?/setpieces_localization_prompt_{x}.sweetline].pc_sweetline')
                for guess in guesses:
                    guessed_hash = ioi_string_to_hex(guess)
                    if guessed_hash in data and data[guessed_hash]['correct_name']:
                        continue
                    elif guessed_hash in data:
                        print(guessed_hash + ', ' + guess)
                        continue
                    else:
                        # dang
                        #print(hash + ': ' + hex_string)
                        continue

def extract_from_locrs():
    for hash in data:
        if data[hash]['type'] == 'LOCR':
            for hex_string in data[hash]['hex_strings']:
                guesses: set[str] = set()
                for x in [hex_string.lower().replace(' ', '_'), hex_string.lower().replace(' ', '')]:
                    guesses.add(f'[assembly:/localization/hitman6/conversations/ui/pro/setpieces.sweetmenutext?/setpieces_localization_prompt_{x}.sweetline].pc_sweetline')
                for guess in guesses:
                    guessed_hash = ioi_string_to_hex(guess)
                    if guessed_hash in data and data[guessed_hash]['correct_name']:
                        continue
                    elif guessed_hash in data:
                        print(guessed_hash + ', ' + guess)
                        continue
                    else:
                        # dang
                        #print(hash + ': ' + hex_string)
                        continue

extract_setpieces_from_locrs()