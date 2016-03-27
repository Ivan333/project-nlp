# -*- coding: utf-8 -*-

import re

text = {}
a = 'this is text number one and contains a sentence.'
b = 'this is text number one and contains a few words.'
c = 'this is text number one and contains a sentence.'
text[0] = a
text[1] = b
text[2] = c

fourgram = {}

for i in range(3):
    fourgram[i] = set()
    words = re.findall('\w+', text[i])
    for n in range(len(words) - 3):
        fourgram[i].add( ' '.join( words[n : n + 4] ) )
        
for j in fourgram.keys():
    if 0 == j: continue
    intersect = fourgram[0] & fourgram[j]
    if len(intersect) >= len(fourgram[0]) / 2.0: print 0, j, intersect