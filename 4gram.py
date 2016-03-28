# -*- coding: utf-8 -*-

import re

text = {}
a = 'this is text number one and contains a sentence.'
b = 'this is text number one and contains a few words.'
c = 'this is text number'

i = 0
for line in open("rez.txt"):
    i+=1
    split = line.split('\t')
    print line.split('\t')[0]
    text[split[0]] = split[1]







fourgram = {}

for i in text.keys():
    fourgram[i] = set()
    words = re.findall('\w+', text[i])
    for n in range(len(words) - 3):
        fourgram[i].add( ' '.join( words[n : n + 4] ) )

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




#for j in fourgram.keys():
#    if 0 == j: continue
#    intersect = fourgram[0] & fourgram[j]
#    print "intesect len ", len(intersect), "calculatioan", len(fourgram[0]) / 2.0
#    if len(intersect) >= len(fourgram[0]) / 2.0: print 0, j, intersect
