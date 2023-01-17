import string
from utils import hashcat
# ['00AF9CBF71D4D99A', '0022A81496B8F58B', '00AFF40E7198420C']
#   - 00AF9CBF71D4D99A.FXAS 5F (unknown, but should be [assembly:/animationfacefx/hitman/<something>.animset].pc_animset)
#   - 0022A81496B8F58B.FXAS 5F (unknown, but should be [assembly:/animationfacefx/hitman/<something>.animset].pc_animset)
#   - 000F40D2DF1C4DB1.FXAS 5F [assembly:/animationfacefx/hitman/specificreactions.animset].pc_animset
#   - 00F22453A545A820.FXAS 5F [assembly:/animationfacefx/hitman/reactions.animset].pc_animset

allowed = set(string.ascii_lowercase + '_')
with open('hitman_wordlist.txt', 'r') as f:
    hitman_wordlist = set([x.strip() for x in f.readlines()])
with open('wordlist_12.txt', 'r') as f:
    wordlist_12 = set([x.strip() for x in f.readlines()])

wordlist = hitman_wordlist.union(wordlist_12)
wordlist = set([word for word in wordlist if set(word) <= allowed])

# print(hashcat('FXAS', wordlist, wordlist, ['[assembly:/animationfacefx/hitman/', '', '.animset].pc_animset']))
print(hashcat('FXAS', wordlist, wordlist, ['[assembly:/animationfacefx/hitman/', '_', '.animset].pc_animset']))