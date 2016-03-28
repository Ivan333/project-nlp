# -*- coding: utf-8 -*-

import re
import pickle

class MkTextChecker:

    #constructor with dictionaryName
    def __init__(self, dictionaryName):
        self.dictionaryMk = {}
        for line in open(dictionaryName, 'r'):
            split = line.split('\t')
            if len(split) >= 2:
                self.dictionaryMk[split[0]] = split[1]



    # check text returns T if contains 50% or more macedonian words F otherwise
    def checkMkText(self,text):
        countT = 0
        countF = 0
        words = text.lower().split()
        wordsLen = len(words)

        for word in words:
            if(self.checkMkWord(word)):
                countT+=1
            else:
                countF+=1
            if(countT >= wordsLen/2.0):
                return True
            elif(countF >= wordsLen/2.0):
                return False
        return False
    #if word is macedonian returns T, F otherwise
    def checkMkWord(self,word):
        if(self.dictionaryMk.get(word)):
            return True
        return False
