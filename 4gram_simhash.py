# -*- coding: utf-8 -*-

import re
from mkText import MkTextChecker
from simhash import Simhash, SimhashIndex
import time

#initialise global variables
text = {}
fourgram = {}

checkerMk = MkTextChecker("wfl-mk.tbl")

i = 0
start_time = time.time()
#read texts from file
domains = ["http://brkajrabota.mk", "http://fokus.mk", "http://loza.mk", "http://akademik.mk", "http://vistinomer.mk", "http://fakulteti.mk"]
for line in open("rez_final.txt"):
    if i == 1000: break
    split = line.split('\t')
    domain = "/".join(split[0].split("/")[:3])
    if domain not in domains: continue
    i += 1
    if(checkerMk.checkMkText(split[1])):
        text[split[0]] = split[1].decode("utf-8")
        print split[0]



#create fourgrams
for url in text:
    fourgram[url] = []
    words = text[url].split()
    for n in range(len(words) - 3):
        for j in range(n, n+4):
            fourgram[url].append(words[j])



#duplicate detection
keys = fourgram.keys()
f1 = open('rezFinalNoDuplicates.txt', 'w')
objs = []
for k in fourgram:
    try:
        objs.append((k, Simhash(fourgram[k])))
    except Exception as e:
        print e
#objs = [(k, Simhash(fourgram[k])) for k in fourgram]
index = SimhashIndex(objs, k=3)

print "bucket_size", index.bucket_size()

for key in keys:
    s1 = Simhash(fourgram[key])
    duplicates = ", ".join(index.get_near_dups(s1))
    f1.write(key + "\t" + duplicates+"\n")
    print key, duplicates

'''
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
'''

f1.close()

print time.time() - start_time, "s"
