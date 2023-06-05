# Hitman Hash Reversal

This repo is a collection of scripts that I've written for trying to crack IOI
hashes. I make no promises of efficacy.

## General Steps

You'll need to copy hashes.json to this folder from the latest release on my other repo: https://github.com/dado3212/hitman-hashes-json/releases.
Then you'll need to run `python3 build.py`. After that, the other scripts will work, though they're all WIP and
are likely to change between versions.

Recommended scripts after a new version bump:
* `python3 futzing.py` - does some letter futzing for known files (this takes around 30 minutes to run currently)
* `python3 main.py > tmp.txt` and follow up with `python3 expand_known.py` which will do some trivial checks and save it into `tmp2.txt`.

## Current Progress

Current state of the world (calculate using `python3 unknown_calc.py`, and then run `\| +\n` -> `|\n` in regex replace):
### Finished
All of these are reversed.
| File Type | Total | Correct | Correct Percentage |
| --- | --- | --- | --- |
| AIBB | 1 | 1 | 100% |
| AIBX | 1 | 1 | 100% |
| AIRG | 44 | 44 | 100% |
| BOXC | 40 | 40 | 100% |
| CBLU | 1643 | 1643 | 100% |
| CPPT | 1643 | 1643 | 100% |
| FXAC | 2 | 2 | 100% |
| GFXF | 37 | 37 | 100% |
| GIDX | 1 | 1 | 100% |
| PREL | 139 | 139 | 100% |
| REPO | 1 | 1 | 100% |
| SDEF | 499 | 499 | 100% |
| WBNK | 92 | 92 | 100% |
| WWES | 185648 | 185648 | 100% |

### Searchable
All of these have a searchable string.
| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |
| --- | --- | --- | --- | --- | --- |
| ASVA | 259 | 250 | 96.5% | 259 | 100% |
| CRMD | 42 | 41 | 97.6% | 42 | 100% |
| ENUM | 1 | 0 | 0.0% | 1 | 100% |
| ERES | 249 | 246 | 98.7% | 249 | 100% |
| GFXV | 247 | 113 | 45.7% | 247 | 100% |
| TBLU | 52764 | 33287 | 63.0% | 52764 | 100% |
| WSWB | 8 | 7 | 87.5% | 8 | 100% |
| YSHP | 3 | 2 | 66.6% | 3 | 100% |

### Incomplete
Missing searchable strings.
| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |
| --- | --- | --- | --- | --- | --- |
| AIBZ | 4 | 3 | 75.0% | 3 | 75.0% |
| ALOC | 25067 | 15407 | 61.4% | 15407 | 61.4% |
| ASEB | 5504 | 1443 | 26.2% | 1443 | 26.2% |
| ASET | 12423 | 5257 | 42.3% | 5257 | 42.3% |
| ATMD | 15356 | 5098 | 33.1% | 5098 | 33.1% |
| BMSK | 55 | 37 | 67.2% | 37 | 67.2% |
| BORG | 6417 | 2284 | 35.5% | 2284 | 35.5% |
| CLNG | 4 | 0 | 0.0% | 0 | 0.0% |
| DITL | 4 | 0 | 0.0% | 0 | 0.0% |
| DLGE | 47904 | 24944 | 52.0% | 47078 | 98.2% |
| DSWB | 46 | 27 | 58.6% | 41 | 89.1% |
| ECPB | 2832 | 0 | 0.0% | 0 | 0.0% |
| ECPT | 2832 | 0 | 0.0% | 0 | 0.0% |
| FXAS | 185653 | 185650 | 99.9% | 185650 | 99.9% |
| GFXI | 9366 | 7264 | 77.5% | 7265 | 77.5% |
| JSON | 1392 | 1234 | 88.6% | 1377 | 98.9% |
| LINE | 11430 | 4811 | 42.0% | 4811 | 42.0% |
| LOCR | 803 | 200 | 24.9% | 200 | 24.9% |
| MATB | 5257 | 4616 | 87.8% | 5252 | 99.9% |
| MATE | 835 | 617 | 73.8% | 617 | 73.8% |
| MATI | 17733 | 16489 | 92.9% | 17725 | 99.9% |
| MATT | 5257 | 4616 | 87.8% | 5252 | 99.9% |
| MJBA | 17618 | 5642 | 32.0% | 5642 | 32.0% |
| MRTN | 2134 | 974 | 45.6% | 974 | 45.6% |
| MRTR | 823 | 72 | 8.7% | 72 | 8.7% |
| NAVP | 73 | 71 | 97.2% | 72 | 98.6% |
| ORES | 6 | 4 | 66.6% | 4 | 66.6% |
| PRIM | 40081 | 19827 | 49.4% | 20045 | 50.0% |
| RTLV | 124 | 0 | 0.0% | 119 | 95.9% |
| SCDA | 781 | 722 | 92.4% | 722 | 92.4% |
| TEMP | 80674 | 50776 | 62.9% | 80609 | 99.9% |
| TEXD | 39895 | 29803 | 74.7% | 29842 | 74.8% |
| TEXT | 40999 | 30404 | 74.1% | 30739 | 74.9% |
| UICB | 304 | 298 | 98.0% | 298 | 98.0% |
| UICT | 304 | 298 | 98.0% | 298 | 98.0% |
| VIDB | 93 | 0 | 0.0% | 89 | 95.6% |
| VTXD | 11284 | 8684 | 76.9% | 8684 | 76.9% |
| WSGB | 139 | 126 | 90.6% | 137 | 98.5% |
| WSGT | 139 | 126 | 90.6% | 137 | 98.5% |
| WSWT | 54 | 34 | 62.9% | 49 | 90.7% |
| WWEM | 7187 | 0 | 0.0% | 6894 | 95.9% |
| WWEV | 8426 | 2308 | 27.3% | 8425 | 99.9% |

https://wiki.glaciermodding.org/glacier2/fileformats

## Raw Notes

### Future TODOs
NOTE: v a lot of this needs us to remove the truncation that we do on XOR/LZ4 decompression
for large files.

1. Extract strings from hex files. Especially ECPB -> MAT[ITB] (done)
    a. ORES blob files -> strings for GFXI file names
    b. MRTN -> pull names out
    c. MRTR
2. LINE -> trivial futzing, need JSON extraction working correctly for localization files
3. WBNK -> should be able to crack the last one
4. DLGE -> all of these have different paths but basically the same. Missing something about the folder structure.
00F477D5E622EBAB
005366CD58EAF59E
00D9EE72519B89B9
0072750B687220AF
00B81A231C11FC4D
005F0A31EA67B2EC
007C84ADA21F5322

LINE
LOCR
PRIM
MJBA (ATMD)

MRTN -> MJBA -> ATMD, MRTR

* when you get MATI -> 

## Status on non-complete
* DSWB (same as WSWB)
  Names come from hex_strings, wordlist guessing for the directory.
* GFXV
  Names come from hex_strings, wordlist guessing for the directory (and maybe ORES?)
* MATI
  Names come from hex_strings, wordlist guessing for the directory (shared with TEXT/PRIM dependencies).
* TBLU
  Names come from hex_strings, directories from TBLU/TEMP dependencies.
* TEMP
  Names come from PRIM/TBLU dependencies.
* WWEV
  Names come from hex_strings, directories from wordlists.

* AIBZ
  Comes from wordlist
* ALOC
  Comes directly from TEMP dependency with a different suffix (AFAIK)
* ASEB
  Comes directly from ASET dependency with a different suffix, exhaustive.
* ASET
  Comes from TEMP children, CPPT, and maybe ECPT though we don't have any yet.
* ASVA
  Comes from TEMP dependencies, with some name mangling.
* ATMD
  Comes from MJBA, exhaustive. Has CPPT/CBLU names in it. Also has some unknown stuff like saudioanimationeventdata.
* BMSK
  Comes from wordlist.
* BORG
  Comes from PRIM, reverse dependency. Also can come from modified TEMP files, as well as non-linked PRIMs.
* CLNG
  No info.
* CRMD
  Comes from wordlist and reverse TEMP.
* DITL
  No info.
* DLGE
  Futzing from SDEF and known DLGE paths. <- do more here
* ECPB
  No info. Source of a lot of MATI strings.
* ECPT
  No info.
* ERES
  From TEMP dependency (materialdescriptor).
* FXAS
  From hex_strings, except for 3 of them (two of them are in a known form)
* GFXI
  Names from ORES, REPO, and JSON files. Appears to be missing a lot of info.
* JSON
  Names from JSON, ORES, REPO. Missing some...but not too many.
* LINE
  From LOCR and hex_strings. Also REPO, maybe a little JSON TODO?
* LOCR
  From REPO (maybe a little JSON TODO)?
* MATB
  From MATT with a different ending, exhaustively.
* MATE
  I have no idea. TODO: explore this. It looks like hex_strings and wordlist
* MATT
  From MATI with a different ending.
* MJBA
  From MRTN. Potentially other places too?
* MRTN
  From hex_strings (usually with hm or mr), with maybe wordlist directories? <- we can do searchable easily
  Also from reverse TEMP, which has TBLU
* MRTR
  From MJBA with reverse dependency, exhaustively. Also hex_strings but modified, which can help the other direction.
* ORES
  From ORES hex_strings. Maybe futzing?
* PRIM
  From MATI dependency and TEMP reverse dependency. They basically all have MATI.
* RTLV
  No info, just guesses.
* SCDA
  From reverse TEMP hex_strings. There are SCDA paths in the large .brick files that appear to be unused.
* TEXD
  From reverse TEXT dependency. Basically exhaustive.
* TEXT
  From reverse MATI dependency, futzing, and wordlists.
* VIDB
  From hex_strings, missing extension (also from TEMP -> TBLU dependency). <- should do easily searchable
* VTXD
  From reverse TEMP hex_strings. There are VTXD paths in the large .brick files that appear to be unused.
* WBNK
  Wordlists, based on reverse dependencies. <- should take an updated cracking look at the last one
* WWEM
  From reverse WWEV hex_strings, and wordlists. <- should take an updated cracking look at this, and verify inverse for all others

More broadly, can we check any JSON/ORES/REPO strings with 'assembly' in them
and see if they match a known name?
Ditto for file extensions.
  scattermap from temp

### Script Expansions
* aibz.py
  * wordlist -> AIBZ
* aseb.py
  * Literally does nothing but verify that it's a subset of ASET
* aset.py
  * TEMP -> ASET
* prim.py
  * TBLU + MATI -> PRIM
* ecpb.py
  * ECPB -> MATI, MATB, MATT
* wswb_dswb.py
  * wordlist -> WSWB, DSWB

* expand_known.py
  * ASET <-> ASEB
  * WSWB <-> WSWT
  * WSGB <-> WSGT
  * PRIM <-> BORG
  * ALOC <-> TEMP
  * MATT <-> MATB
  * TEXT <-> TEXD
  * PREL <-> TBLU(/TEMP/NAVP)
  * more

# What to run
* python3 main.py
* python3 aset.py
* python3 mati.py (this takes a while)
* python3 prim.py
* python3 futzing.py

### Known Bugs
* hashcat chokes on outputting more than 256 characters, and will truncate despite successfully
  cracking the hash. This is currently happening for aset.py, and maybe others?

### Misc

Checked all CSS color names from https://css-tricks.com/snippets/css/named-colors-and-hex-equivalents/
- found black,blue,cyan,grey,green,purple,red,white,yellow no other matches, and all are named
- '[assembly:/_pro/environment/textures/constants/color_' + color + '.texture?/diffuse_a.tex](ascolormap).pc_tex'
- b for cyan, yellow
- c for yellow

wordlist_1.txt and wordlist_3.txt are downloaded from https://www.keithv.com/software/wlist/ and are used as a very
low quality hashing dictionary. Really we should be using a Hitman-specific wordlist, but as of right now
I haven't built one.

Potential patterns:
[assembly:/_pro/environment/textures/generic/metal/gold_clean_a.texture?/diffuse_a.tex](ascolormap).pc_tex

https://github.com/dado3212/hitman-hash-reversal/commit/3d2a7b525c99750e6291960919bbbe584a0fdbbc had the version of main.py that I used to actually create the current shared list in new.txt.

# Adhoc hashcat
`./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz0123456789_/ 00F1C98E21AC5D76 "[assembly:/_pro/online/contracts/?1?1?1?1?1?1?1?1?1/Ancestral_bulldog_Death_In_755984a8-fb0b-4673-8637-95cfe7d34e0f.contracts.json].pc_json" --increment --increment-min 2 --increment-max 3`
## did 5, 6, 7
./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz0123456789_/ 006BF37145EFFA5D "[assembly:/_pro/scenes/missions/miami/scene_?1?1?1?1?1?1?1?1.navp].pc_navp"  --outfile-autohex-disable --status --status-timer 3 --force --potfile-disable -o miami-cracked.txt

## tried 1, 2, 3, 4, 5, 6, 7
./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz 005F87B4C57FD0FF "[assembly:/ai/behaviortrees/?1?1?1?1?1?1?1.aibt].pc_aibz"  --outfile-autohex-disable --status --status-timer 3 --force --potfile-disable -o aibz-cracked.txt

## tried 1, 2, 3, 4, 5, 6
./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz 005F87B4C57FD0FF "[assembly:/ai/behaviortrees/custom/?1?1?1?1?1?1?1.aibt].pc_aibz"  --outfile-autohex-disable --status --status-timer 3 --force --potfile-disable -o aibz-cracked.txt

## tried 1-6
./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz 00AF9CBF71D4D99A "[assembly:/animationfacefx/?1?1?1?1?1?1.animset].pc_animset"  --outfile-autohex-disable --status --status-timer 3 --force --potfile-disable -o fxas-cracked.txt

# tried 1-6, 8 (7 no)
./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz_0123 00D27A79757FD3C5 "[assembly:/_pro/characters/assets/crowd/female/?1?1?1?1?1?1?1/materials/female_crowd_formal_marakesh_body_02_v2.mi].pc_mi" --outfile-autohex-disable --status --status-timer 3 --force --potfile-disable -o custom-mati-cracked.txt

# tried 1-7
./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz_ 00D63DA408C1369A "[assembly:/sound/wwise/exportedwwisedata/soundbanks/globaldata/?1?1?1?1?1?1?1.wwisesoundbank].pc_wwisebank" --outfile-autohex-disable --status --status-timer 3 --force --potfile-disable -o wbnk-cracked.txt

# tried 1-6, on 7 so boost increment-min to 102
./hashcat.exe -a 3 -m 92100 -1 abcdefghijklmnopqrstuvwxyz 006CF07CF75C7EBF "[assembly:/_pro/scenes/frontend/videodatabase/videodatabase_dlc_1_harveywallbanger.entity].pc_?1?1?1?1?1?1?1?1?1?1" --outfile-autohex-disable --status --status-timer 3 --force --potfile-disable -o rtlv-cracked.txt --increment --increment-min 95 --increment-max 105

# Setting up and want to copy paste:
```
from utils import load_data, hashcat, targeted_hashcat, ioi_string_to_hex
import re, json, pickle
data = load_data()
with open('reverse.pickle', 'rb') as handle:
    reverse = pickle.load(handle)
```

Search for string 
```
[hash for hash in data if any([x for x in data[hash]['hex_strings'] if 'picture_modern_penthouse_b_01' in x.lower()])]
[hash + '.' + data[hash]['type'] for hash in data if any([x for x in data[hash]['hex_strings'] if 'hud.swf' in x.lower()])]
```

# Running tests
`python3 tests.py`

TODO: PREL conversion for Freelancer