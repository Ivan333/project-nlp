# -*- coding: utf-8 -*-

import re
from mkText import MkTextChecker

#initialise global variables
text = {}
fourgram = {}

checkerMk = MkTextChecker("wfl-mk.tbl")

i = 0

#read texts from file
for line in open("rez.txt"):
    i+=1
    split = line.split('\t')
    if(checkerMk.checkMkText(split[1])):
        text[split[0]] = split[1]
        print split[0]
    if i == 200:
        break;

#create fourgrams
for i in text.keys():
    fourgram[i] = set()
    words = text[i].split()
    for n in range(len(words) - 3):
        fourgram[i].add( ' '.join( words[n : n + 4] ) )



#duplicate detection
keys = fourgram.keys()
f1 = open('rezNoDuplicates.txt', 'w')

while len(keys) > 0:
    key = keys.pop()
    keysJ = list(keys)
    f1.write(key + '\t' + text[key])

    while len(keysJ) > 0:
        j = keysJ.pop()
        intersect = fourgram[key] & fourgram[j]
        #print "checking", text[j]
        #print "forgram ", fourgram[key], "fourgram", fourgram[j]
        #print "calculation", len(intersect) , len(fourgram[key]) / 2.0
        if len(intersect) >= len(fourgram[key])/2.0 and len(intersect) >= len(fourgram[j])/2.0:
            text.pop(j)
            keys.remove(j)
            fourgram.pop(j)


f1.close()
