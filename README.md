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
| AIRG | 40 | 40 | 100% |
| BOXC | 37 | 37 | 100% |
| CBLU | 1531 | 1531 | 100% |
| CPPT | 1531 | 1531 | 100% |
| FXAC | 2 | 2 | 100% |
| GFXF | 37 | 37 | 100% |
| GIDX | 1 | 1 | 100% |
| PREL | 100 | 100 | 100% |
| REPO | 1 | 1 | 100% |
| SDEF | 499 | 499 | 100% |
| UICB | 283 | 283 | 100% |
| UICT | 283 | 283 | 100% |
| WSWB | 6 | 6 | 100% |
| WWES | 184994 | 184994 | 100% |

### Searchable
All of these have a searchable string.
| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |
| --- | --- | --- | --- | --- | --- |
| ASVA | 259 | 250 | 96.5% | 259 | 100% |
| CRMD | 42 | 41 | 97.6% | 42 | 100% |
| DSWB | 43 | 28 | 65.1% | 43 | 100% |
| GFXV | 219 | 93 | 42.4% | 219 | 100% |
| MATI | 17575 | 16213 | 92.2% | 17575 | 100% |
| NAVP | 67 | 66 | 98.5% | 67 | 100% |
| TBLU | 50959 | 32165 | 63.1% | 50959 | 100% |
| TEMP | 78549 | 49257 | 62.7% | 78549 | 100% |
| WSGB | 132 | 121 | 91.6% | 132 | 100% |
| WSGT | 132 | 121 | 91.6% | 132 | 100% |
| WSWT | 49 | 34 | 69.3% | 49 | 100% |
| WWEV | 8112 | 2233 | 27.5% | 8112 | 100% |
| YSHP | 3 | 2 | 66.6% | 3 | 100% |

### Incomplete
Missing searchable strings.
| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |
| --- | --- | --- | --- | --- | --- |
| AIBZ | 4 | 3 | 75.0% | 3 | 75.0% |
| ALOC | 24769 | 15030 | 60.6% | 15030 | 60.6% |
| ASEB | 5369 | 1423 | 26.5% | 1423 | 26.5% |
| ASET | 12236 | 5168 | 42.2% | 5168 | 42.2% |
| ATMD | 15192 | 5096 | 33.5% | 5096 | 33.5% |
| BMSK | 55 | 37 | 67.2% | 37 | 67.2% |
| BORG | 6357 | 2246 | 35.3% | 2246 | 35.3% |
| CLNG | 4 | 0 | 0.0% | 0 | 0.0% |
| DITL | 4 | 0 | 0.0% | 0 | 0.0% |
| DLGE | 47670 | 24743 | 51.9% | 46877 | 98.3% |
| ECPB | 2730 | 0 | 0.0% | 0 | 0.0% |
| ECPT | 2730 | 0 | 0.0% | 0 | 0.0% |
| ERES | 246 | 243 | 98.7% | 243 | 98.7% |
| FXAS | 184999 | 184996 | 99.9% | 184996 | 99.9% |
| GFXI | 8575 | 6546 | 76.3% | 6547 | 76.3% |
| JSON | 1349 | 1199 | 88.8% | 1330 | 98.5% |
| LINE | 10570 | 4710 | 44.5% | 4710 | 44.5% |
| LOCR | 779 | 183 | 23.4% | 183 | 23.4% |
| MATB | 5151 | 4487 | 87.1% | 5150 | 99.9% |
| MATE | 824 | 456 | 55.3% | 456 | 55.3% |
| MATT | 5151 | 4487 | 87.1% | 5150 | 99.9% |
| MJBA | 17388 | 5635 | 32.4% | 5635 | 32.4% |
| MRTN | 2091 | 942 | 45.0% | 942 | 45.0% |
| MRTR | 796 | 72 | 9.0% | 72 | 9.0% |
| ORES | 6 | 4 | 66.6% | 4 | 66.6% |
| PRIM | 39604 | 19364 | 48.8% | 19582 | 49.4% |
| RTLV | 119 | 0 | 0.0% | 114 | 95.7% |
| SCDA | 774 | 715 | 92.3% | 715 | 92.3% |
| TEXD | 39223 | 29531 | 75.2% | 29570 | 75.3% |
| TEXT | 40311 | 30122 | 74.7% | 30457 | 75.5% |
| VIDB | 88 | 0 | 0.0% | 0 | 0.0% |
| VTXD | 11107 | 8517 | 76.6% | 8517 | 76.6% |
| WBNK | 89 | 88 | 98.8% | 88 | 98.8% |
| WWEM | 7006 | 0 | 0.0% | 6894 | 98.4% |

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
* ORES
  From ORES hex_strings. Maybe futzing?

  # WBNK

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
