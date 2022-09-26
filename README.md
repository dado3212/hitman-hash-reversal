Checked all CSS color names from https://css-tricks.com/snippets/css/named-colors-and-hex-equivalents/
- found black,blue,cyan,grey,green,purple,red,white,yellow no other matches, and all are named
- '[assembly:/_pro/environment/textures/constants/color_' + color + '.texture?/diffuse_a.tex](ascolormap).pc_tex'
- b for cyan, yellow
- c for yellow

Potential patterns:
[assembly:/_pro/environment/textures/generic/metal/gold_clean_a.texture?/diffuse_a.tex](ascolormap).pc_tex

You'll need to copy hashes.json to this folder from the latest release on my repo: https://github.com/dado3212/hitman-hashes-json/releases.
Then you'll need to run `python3 build.py`. After that, the other scripts will work, though they're all WIP and
are likely to change between versions.

https://github.com/dado3212/hitman-hash-reversal/commit/3d2a7b525c99750e6291960919bbbe584a0fdbbc had the version of main.py that I used to actually create the current shared list in new.txt.

Current state of the world (calculate using `python3 unknown_calc.py`, and then run `\| +\n` -> `|\n` in regex replace):

| File Type | Correct | Total | Percentage |
| --- | --- | --- | --- |
| AIBB | 1 | 1 | 100.0% |
| AIBX | 1 | 1 | 100.0% |
| AIBZ | 3 | 4 | 75.0% |
| AIRG | 40 | 40 | 100.0% |
| ALOC | 14345 | 24764 | 57.9% |
| ASEB | 1399 | 5368 | 26.1% |
| ASET | 4984 | 12235 | 40.7% |
| ASVA | 245 | 259 | 94.6% |
| ATMD | 5096 | 15192 | 33.5% |
| BMSK | 34 | 55 | 61.8% |
| BORG | 2226 | 6350 | 35.1% |
| BOXC | 0 | 37 | 0.0% |
| CBLU | 1531 | 1531 | 100.0% |
| CLNG | 0 | 4 | 0.0% |
| CPPT | 1531 | 1531 | 100.0% |
| CRMD | 41 | 42 | 97.6% |
| DITL | 0 | 4 | 0.0% |
| DLGE | 22459 | 47662 | 47.1% |
| DSWB | 19 | 43 | 44.2% |
| ECPB | 0 | 2730 | 0.0% |
| ECPT | 0 | 2730 | 0.0% |
| ERES | 243 | 246 | 98.8% |
| FXAC | 2 | 2 | 100.0% |
| FXAS | 182190 | 182193 | 100.0% |
| GFXF | 37 | 37 | 100.0% |
| GFXI | 6138 | 8158 | 75.2% |
| GFXV | 93 | 219 | 42.5% |
| GIDX | 1 | 1 | 100.0% |
| JSON | 1195 | 1345 | 88.8% |
| LINE | 4614 | 10547 | 43.7% |
| LOCR | 162 | 766 | 21.1% |
| MATB | 4464 | 5147 | 86.7% |
| MATE | 456 | 823 | 55.4% |
| MATI | 16142 | 17560 | 91.9% |
| MATT | 4464 | 5147 | 86.7% |
| MJBA | 5629 | 17381 | 32.4% |
| MRTN | 942 | 2091 | 45.1% |
| MRTR | 68 | 790 | 8.6% |
| NAVP | 64 | 65 | 98.5% |
| ORES | 4 | 6 | 66.7% |
| PREL | 97 | 97 | 100.0% |
| PRIM | 18505 | 39592 | 46.7% |
| REPO | 1 | 1 | 100.0% |
| RTLV | 0 | 119 | 0.0% |
| SCDA | 715 | 774 | 92.4% |
| SDEF | 499 | 499 | 100.0% |
| TBLU | 31254 | 50931 | 61.4% |
| TEMP | 47512 | 78512 | 60.5% |
| TEXD | 28799 | 39197 | 73.5% |
| TEXT | 29378 | 40284 | 72.9% |
| UICB | 283 | 283 | 100.0% |
| UICT | 283 | 283 | 100.0% |
| VIDB | 0 | 88 | 0.0% |
| VTXD | 8517 | 11107 | 76.7% |
| WBNK | 88 | 89 | 98.9% |
| WSGB | 23 | 132 | 17.4% |
| WSGT | 23 | 132 | 17.4% |
| WSWB | 1 | 6 | 16.7% |
| WSWT | 20 | 49 | 40.8% |
| WWEM | 0 | 7002 | 0.0% |
| WWES | 182188 | 182188 | 100.0% |
| WWEV | 1982 | 8095 | 24.5% |
| YSHP | 2 | 3 | 66.7% |