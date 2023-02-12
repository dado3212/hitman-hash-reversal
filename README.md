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
| BOXC | 40 | 40 | 100% |
| CBLU | 1641 | 1641 | 100% |
| CPPT | 1641 | 1641 | 100% |
| FXAC | 2 | 2 | 100% |
| GFXF | 37 | 37 | 100% |
| GIDX | 1 | 1 | 100% |
| REPO | 1 | 1 | 100% |
| SDEF | 499 | 499 | 100% |
| WWES | 185647 | 185647 | 100% |

### Searchable
All of these have a searchable string.
| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |
| --- | --- | --- | --- | --- | --- |
| ASVA | 259 | 250 | 96.5% | 259 | 100% |
| CRMD | 42 | 41 | 97.6% | 42 | 100% |
| TBLU | 52753 | 32913 | 62.3% | 52753 | 100% |
| WSWB | 8 | 7 | 87.5% | 8 | 100% |
| WWEV | 8425 | 2233 | 26.5% | 8425 | 100% |
| YSHP | 3 | 2 | 66.6% | 3 | 100% |

### Incomplete
Missing searchable strings.
| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |
| --- | --- | --- | --- | --- | --- |
| AIBZ | 4 | 3 | 75.0% | 3 | 75.0% |
| AIRG | 44 | 41 | 93.1% | 41 | 93.1% |
| ALOC | 25067 | 15147 | 60.4% | 15147 | 60.4% |
| ASEB | 5501 | 1424 | 25.8% | 1424 | 25.8% |
| ASET | 12412 | 5180 | 41.7% | 5180 | 41.7% |
| ATMD | 15356 | 5096 | 33.1% | 5096 | 33.1% |
| BMSK | 55 | 37 | 67.2% | 37 | 67.2% |
| BORG | 6416 | 2247 | 35.0% | 2247 | 35.0% |
| CLNG | 4 | 0 | 0.0% | 0 | 0.0% |
| DITL | 4 | 0 | 0.0% | 0 | 0.0% |
| DLGE | 47904 | 24743 | 51.6% | 46877 | 97.8% |
| DSWB | 46 | 27 | 58.6% | 41 | 89.1% |
| ECPB | 2833 | 0 | 0.0% | 0 | 0.0% |
| ECPT | 2833 | 0 | 0.0% | 0 | 0.0% |
| ENUM | 1 | 0 | 0.0% | 0 | 0.0% |
| ERES | 249 | 243 | 97.5% | 246 | 98.7% |
| FXAS | 185652 | 185649 | 99.9% | 185649 | 99.9% |
| GFXI | 9349 | 7250 | 77.5% | 7251 | 77.5% |
| GFXV | 247 | 93 | 37.6% | 219 | 88.6% |
| JSON | 1391 | 1233 | 88.6% | 1364 | 98.0% |
| LINE | 11412 | 4720 | 41.3% | 4720 | 41.3% |
| LOCR | 804 | 197 | 24.5% | 197 | 24.5% |
| MATB | 5256 | 4519 | 85.9% | 5157 | 98.1% |
| MATE | 835 | 456 | 54.6% | 456 | 54.6% |
| MATI | 17736 | 16363 | 92.2% | 17604 | 99.2% |
| MATT | 5256 | 4519 | 85.9% | 5157 | 98.1% |
| MJBA | 17618 | 5635 | 31.9% | 5635 | 31.9% |
| MRTN | 2134 | 942 | 44.1% | 942 | 44.1% |
| MRTR | 823 | 72 | 8.7% | 72 | 8.7% |
| NAVP | 73 | 67 | 91.7% | 68 | 93.1% |
| ORES | 6 | 4 | 66.6% | 4 | 66.6% |
| PREL | 139 | 100 | 71.9% | 100 | 71.9% |
| PRIM | 40079 | 19500 | 48.6% | 19718 | 49.1% |
| RTLV | 124 | 0 | 0.0% | 114 | 91.9% |
| SCDA | 781 | 722 | 92.4% | 722 | 92.4% |
| TEMP | 80662 | 50095 | 62.1% | 80560 | 99.8% |
| TEXD | 39886 | 29661 | 74.3% | 29700 | 74.4% |
| TEXT | 40990 | 30255 | 73.8% | 30590 | 74.6% |
| UICB | 304 | 283 | 93.0% | 283 | 93.0% |
| UICT | 304 | 283 | 93.0% | 283 | 93.0% |
| VIDB | 90 | 0 | 0.0% | 88 | 97.7% |
| VTXD | 11284 | 8682 | 76.9% | 8682 | 76.9% |
| WBNK | 92 | 91 | 98.9% | 91 | 98.9% |
| WSGB | 139 | 121 | 87.0% | 132 | 94.9% |
| WSGT | 139 | 121 | 87.0% | 132 | 94.9% |
| WSWT | 54 | 34 | 62.9% | 49 | 90.7% |
| WWEM | 7187 | 0 | 0.0% | 6894 | 95.9% |

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

TODO: PREL conversion for Freelancer