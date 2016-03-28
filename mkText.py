# -*- coding: utf-8 -*-

import re
import pickle

class MkTextChecker:

    def __init__(self, dictionaryName):
        self.t = open(dictionaryName, 'r').read()

    def checkMkText(self,text):
        count = 0
        words = text.split()
        wordsLen = len(words)
        for word in words:
            if(self.checkMkWord(word)):
                count+=1
            if(count >= wordsLen/2.0):
                return True
        return False

    def checkMkWord(self,word):
        if(self.t.find(word) != -1):
            return True
        return False
