# Hitman Hash Reversal

This repo is a collection of scripts that I've written for trying to crack IOI
hashes. I make no promises of efficacy.

## General Steps

You'll need to copy hashes.json to this folder from the latest release on my other repo: https://github.com/dado3212/hitman-hashes-json/releases.
Then you'll need to run `python3 build.py`. After that, the other scripts will work, though they're all WIP and
are likely to change between versions.

Recommended scripts after a new version bump:
* `python3 letter_changes.py` - does some letter futzing for known files

## Current Progress

Current state of the world (calculate using `python3 unknown_calc.py`, and then run `\| +\n` -> `|\n` in regex replace):

| File Type | Correct | Total | Percentage |
| --- | --- | --- | --- |
| AIBB | 1 | 1 | 100.0% |
| AIBX | 1 | 1 | 100.0% |
| AIBZ | 3 | 4 | 75.0% |
| AIRG | 40 | 40 | 100.0% |
| ALOC | 14375 | 24769 | 58.0% |
| ASEB | 1399 | 5369 | 26.1% |
| ASET | 4985 | 12236 | 40.7% |
| ASVA | 245 | 259 | 94.6% |
| ATMD | 5096 | 15192 | 33.5% |
| BMSK | 36 | 55 | 65.5% |
| BORG | 2227 | 6357 | 35.0% |
| BOXC | 37 | 37 | 100.0% |
| CBLU | 1531 | 1531 | 100.0% |
| CLNG | 0 | 4 | 0.0% |
| CPPT | 1531 | 1531 | 100.0% |
| CRMD | 41 | 42 | 97.6% |
| DITL | 0 | 4 | 0.0% |
| DLGE | 22459 | 47670 | 47.1% |
| DSWB | 26 | 43 | 60.5% |
| ECPB | 0 | 2730 | 0.0% |
| ECPT | 0 | 2730 | 0.0% |
| ERES | 243 | 246 | 98.8% |
| FXAC | 2 | 2 | 100.0% |
| FXAS | 184996 | 184999 | 100.0% |
| GFXF | 37 | 37 | 100.0% |
| GFXI | 6546 | 8575 | 76.3% |
| GFXV | 93 | 219 | 42.5% |
| GIDX | 1 | 1 | 100.0% |
| JSON | 1199 | 1349 | 88.9% |
| LINE | 4616 | 10570 | 43.7% |
| LOCR | 162 | 779 | 20.8% |
| MATB | 4483 | 5151 | 87.0% |
| MATE | 456 | 824 | 55.3% |
| MATI | 16174 | 17575 | 92.0% |
| MATT | 4483 | 5151 | 87.0% |
| MJBA | 5629 | 17388 | 32.4% |
| MRTN | 942 | 2091 | 45.1% |
| MRTR | 68 | 796 | 8.5% |
| NAVP | 66 | 67 | 98.5% |
| ORES | 4 | 6 | 66.7% |
| PREL | 97 | 100 | 97.0% |
| PRIM | 18550 | 39604 | 46.8% |
| REPO | 1 | 1 | 100.0% |
| RTLV | 0 | 119 | 0.0% |
| SCDA | 715 | 774 | 92.4% |
| SDEF | 499 | 499 | 100.0% |
| TBLU | 31307 | 50959 | 61.4% |
| TEMP | 47628 | 78549 | 60.6% |
| TEXD | 29432 | 39223 | 75.0% |
| TEXT | 30020 | 40311 | 74.5% |
| UICB | 283 | 283 | 100.0% |
| UICT | 283 | 283 | 100.0% |
| VIDB | 0 | 88 | 0.0% |
| VTXD | 8517 | 11107 | 76.7% |
| WBNK | 88 | 89 | 98.9% |
| WSGB | 23 | 132 | 17.4% |
| WSGT | 23 | 132 | 17.4% |
| WSWB | 1 | 6 | 16.7% |
| WSWT | 27 | 49 | 55.1% |
| WWEM | 0 | 7006 | 0.0% |
| WWES | 184994 | 184994 | 100.0% |
| WWEV | 1982 | 8112 | 24.4% |
| YSHP | 2 | 3 | 66.7% |

## Raw Notes

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