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
| ALOC | 24769 | 14379 | 58.1% | 14379 | 58.1% |
| ASEB | 5369 | 1410 | 26.3% | 1410 | 26.3% |
| ASET | 12236 | 4996 | 40.8% | 4996 | 40.8% |
| ASVA | 259 | 245 | 94.6% | 245 | 94.6% |
| ATMD | 15192 | 5096 | 33.5% | 5096 | 33.5% |
| BMSK | 55 | 36 | 65.5% | 36 | 65.5% |
| BORG | 6357 | 2230 | 35.1% | 2230 | 35.1% |
| BOXC | 37 | 37 | 100.0% | 37 | 100.0% |
| CBLU | 1531 | 1531 | 100.0% | 1531 | 100.0% |
| CLNG | 4 | 0 | 0.0% | 0 | 0.0% |
| CPPT | 1531 | 1531 | 100.0% | 1531 | 100.0% |
| CRMD | 42 | 41 | 97.6% | 41 | 97.6% |
| DITL | 4 | 0 | 0.0% | 0 | 0.0% |
| DLGE | 47670 | 22459 | 47.1% | 45061 | 94.5% |
| DSWB | 43 | 26 | 60.5% | 43 | 100.0% |
| ECPB | 2730 | 0 | 0.0% | 0 | 0.0% |
| ECPT | 2730 | 0 | 0.0% | 0 | 0.0% |
| ERES | 246 | 243 | 98.8% | 243 | 98.8% |
| FXAC | 2 | 2 | 100.0% | 2 | 100.0% |
| FXAS | 184999 | 184996 | 100.0% | 184996 | 100.0% |
| GFXF | 37 | 37 | 100.0% | 37 | 100.0% |
| GFXI | 8575 | 6546 | 76.3% | 6547 | 76.3% |
| GFXV | 219 | 93 | 42.5% | 218 | 99.5% |
| GIDX | 1 | 1 | 100.0% | 1 | 100.0% |
| JSON | 1349 | 1199 | 88.9% | 1330 | 98.6% |
| LINE | 10570 | 4616 | 43.7% | 4616 | 43.7% |
| LOCR | 779 | 162 | 20.8% | 162 | 20.8% |
| MATB | 5151 | 4485 | 87.1% | 5148 | 99.9% |
| MATE | 824 | 456 | 55.3% | 456 | 55.3% |
| MATI | 17575 | 16178 | 92.1% | 17562 | 99.9% |
| MATT | 5151 | 4485 | 87.1% | 5148 | 99.9% |
| MJBA | 17388 | 5629 | 32.4% | 5629 | 32.4% |
| MRTN | 2091 | 942 | 45.1% | 942 | 45.1% |
| MRTR | 796 | 68 | 8.5% | 68 | 8.5% |
| NAVP | 67 | 66 | 98.5% | 66 | 98.5% |
| ORES | 6 | 4 | 66.7% | 4 | 66.7% |
| PREL | 100 | 100 | 100.0% | 100 | 100.0% |
| PRIM | 39604 | 18571 | 46.9% | 18748 | 47.3% |
| REPO | 1 | 1 | 100.0% | 1 | 100.0% |
| RTLV | 119 | 0 | 0.0% | 113 | 95.0% |
| SCDA | 774 | 715 | 92.4% | 715 | 92.4% |
| SDEF | 499 | 499 | 100.0% | 499 | 100.0% |
| TBLU | 50959 | 31905 | 62.6% | 50959 | 100.0% |
| TEMP | 78549 | 48230 | 61.4% | 78549 | 100.0% |
| TEXD | 39223 | 29447 | 75.1% | 29486 | 75.2% |
| TEXT | 40311 | 30035 | 74.5% | 30370 | 75.3% |
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
| WWEV | 8112 | 1982 | 24.4% | 7914 | 97.6% |
| YSHP | 3 | 2 | 66.7% | 2 | 66.7% |

## Raw Notes

### Future TODOs
1. Extract strings from hex files. Especially ECPB -> MAT[ITB] (done)
2. ORES blob files -> strings for GFXI file names
3. LINE -> trivial futzing


### TBLU



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