#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script for checking tokens in a corpus which are not yet included in MALINDO Morph.
@author: David Moeljadi <davidmoeljadi@gmail.com>
'''

__author__ = "David Moeljadi <davidmoeljadi@gmail.com>"
__credits__ = [ "David Moeljadi" ]
__license__ = "MIT"
__maintainer__ = "David Moeljadi"
__email__ = "<davidmoeljadi@gmail.com>"

########################################################################

#os and glob to open all txt files in a directory/folder
import os
import glob
#codecs for utf-8
import codecs
#re for regular expression
import re
#nltk for tokenization
import nltk
from nltk.tokenize import word_tokenize

#path to the directory/folder of the files
path = "/home/david/Melayu_Sabah"

#open all txt files in the directory/folder and tokenize
tokens = []
for filename in glob.glob(os.path.join(path, '*.txt')):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    for line in f.readlines():
        items = line.strip()
        token = word_tokenize(items)
        for x in token:
            tokens.append(x)

#remove all punctuations
tokens = [re.sub("[\>\<\/\#\”\“\'\`\(\)\:\;\!\?\"\,\s\.]+", "", w) for w in tokens]

#open MALINDO Morph and make a list of all surface forms
m = codecs.open('/home/david/MALINDO_Morph/malindo_dic_20180817.tsv', encoding='utf-8', mode='r')
katakata = []
for baris in m.readlines():
    kata = baris.strip().split('\t')
    katakata.append(kata[2])

#extract the difference of tokens and MALINDO Morph surface forms
diff = list(set(tokens)-set(katakata))
#check the number of tokens, surface forms, and the difference
#print(len(tokens))
#print(len(set(tokens)))
#print(len(katakata))
#print(len(set(tokens)-set(katakata)))

#check the frequency of the tokens
wordcount = dict((x,0) for x in diff)
for w in tokens:
     if w in wordcount:
        wordcount[w] += 1

#sort the tokens based on the frequency, descending
copy = []
for k,v in wordcount.items():
    copy.append((v, k))
copy = sorted(copy, reverse=True)

#print each token and its frequency
for k in copy:
    print ("%s\t%d" %(k[1], k[0]))
