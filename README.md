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

| File Type | Total | Correct | Correct Percentage | Searchable | Searchable Percentage |
| --- | --- | --- | --- | --- | --- |
| AIBB | 1 | 1 | 100.0% | 1 | 100.0% |
| AIBX | 1 | 1 | 100.0% | 1 | 100.0% |
| AIBZ | 4 | 3 | 75.0% | 3 | 75.0% |
| AIRG | 40 | 40 | 100.0% | 40 | 100.0% |
| ALOC | 24769 | 14390 | 58.1% | 14390 | 58.1% |
| ASEB | 5369 | 1410 | 26.3% | 1410 | 26.3% |
| ASET | 12236 | 4996 | 40.8% | 4996 | 40.8% |
| ASVA | 259 | 245 | 94.6% | 245 | 94.6% |
| ATMD | 15192 | 5096 | 33.5% | 5096 | 33.5% |
| BMSK | 55 | 36 | 65.5% | 36 | 65.5% |
| BORG | 6357 | 2232 | 35.1% | 2232 | 35.1% |
| BOXC | 37 | 37 | 100.0% | 37 | 100.0% |
| CBLU | 1531 | 1531 | 100.0% | 1531 | 100.0% |
| CLNG | 4 | 0 | 0.0% | 0 | 0.0% |
| CPPT | 1531 | 1531 | 100.0% | 1531 | 100.0% |
| CRMD | 42 | 41 | 97.6% | 41 | 97.6% |
| DITL | 4 | 0 | 0.0% | 0 | 0.0% |
| DLGE | 47670 | 24743 | 51.9% | 46877 | 98.3% |
| DSWB | 43 | 26 | 60.5% | 43 | 100.0% |
| ECPB | 2730 | 0 | 0.0% | 0 | 0.0% |
| ECPT | 2730 | 0 | 0.0% | 0 | 0.0% |
| ERES | 246 | 243 | 98.8% | 243 | 98.8% |
| FXAC | 2 | 2 | 100.0% | 2 | 100.0% |
| FXAS | 184999 | 184996 | 100.0% | 184996 | 100.0% |
| GFXF | 37 | 37 | 100.0% | 37 | 100.0% |
| GFXI | 8575 | 6546 | 76.3% | 6547 | 76.3% |
| GFXV | 219 | 93 | 42.5% | 219 | 100.0% |
| GIDX | 1 | 1 | 100.0% | 1 | 100.0% |
| JSON | 1349 | 1199 | 88.9% | 1330 | 98.6% |
| LINE | 10570 | 4617 | 43.7% | 4617 | 43.7% |
| LOCR | 779 | 166 | 21.3% | 166 | 21.3% |
| MATB | 5151 | 4487 | 87.1% | 5150 | 100.0% |
| MATE | 824 | 456 | 55.3% | 456 | 55.3% |
| MATI | 17575 | 16206 | 92.2% | 17575 | 100.0% |
| MATT | 5151 | 4487 | 87.1% | 5150 | 100.0% |
| MJBA | 17388 | 5629 | 32.4% | 5629 | 32.4% |
| MRTN | 2091 | 942 | 45.1% | 942 | 45.1% |
| MRTR | 796 | 68 | 8.5% | 68 | 8.5% |
| NAVP | 67 | 66 | 98.5% | 66 | 98.5% |
| ORES | 6 | 4 | 66.7% | 4 | 66.7% |
| PREL | 100 | 100 | 100.0% | 100 | 100.0% |
| PRIM | 39604 | 18588 | 46.9% | 18808 | 47.5% |
| REPO | 1 | 1 | 100.0% | 1 | 100.0% |
| RTLV | 119 | 0 | 0.0% | 114 | 95.8% |
| SCDA | 774 | 715 | 92.4% | 715 | 92.4% |
| SDEF | 499 | 499 | 100.0% | 499 | 100.0% |
| TBLU | 50959 | 32090 | 63.0% | 50959 | 100.0% |
| TEMP | 78549 | 48430 | 61.7% | 78549 | 100.0% |
| TEXD | 39223 | 29527 | 75.3% | 29566 | 75.4% |
| TEXT | 40311 | 30116 | 74.7% | 30451 | 75.5% |
| UICB | 283 | 283 | 100.0% | 283 | 100.0% |
| UICT | 283 | 283 | 100.0% | 283 | 100.0% |
| VIDB | 88 | 0 | 0.0% | 0 | 0.0% |
| VTXD | 11107 | 8517 | 76.7% | 8517 | 76.7% |
| WBNK | 89 | 88 | 98.9% | 88 | 98.9% |
| WSGB | 132 | 23 | 17.4% | 130 | 98.5% |
| WSGT | 132 | 23 | 17.4% | 130 | 98.5% |
| WSWB | 6 | 1 | 16.7% | 4 | 66.7% |
| WSWT | 49 | 27 | 55.1% | 47 | 95.9% |
| WWEM | 7006 | 0 | 0.0% | 6894 | 98.4% |
| WWES | 184994 | 184994 | 100.0% | 184994 | 100.0% |
| WWEV | 8112 | 2233 | 27.5% | 8112 | 100.0% |
| YSHP | 3 | 2 | 66.7% | 2 | 66.7% |

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

### TBLU

### Script Expansions
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
