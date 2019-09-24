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
tokens = [re.sub("[\>\<\#\”\“\'\`\(\)\:\;\!\?\"\,\s\.\[\]]+", "", w) for w in tokens] #Masalah: "menunggu/stesen" menjadi satu kata "menunggustesen" > "/" dibuang 
tokens = [t for t in tokens if t != ""] #supaya "" tidak akan dihitung nanti

#open MALINDO Morph and make a list of all surface forms
m = codecs.open('/home/david/MALINDO_Morph/malindo_dic_20190923.tsv', encoding='utf-8', mode='r')
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


#print each token in the MALINDO Morph format
#analyse using MALINDO Morph morphological analyser
import morph_analyzer as ma
from pickle import load
from spellchecker import SpellChecker

def analisis(token, rootlist, Indo = False):
    cand = ma.morph(token, rootlist)
    rt,s,pfx,sfx,cfx,rdp = ([],token,[],[],[],[])
    for c in cand:
        if c[0] not in rt:
            rt.append(c[0])
        if c[2] not in pfx:
            pfx.append(c[2])
        if c[3] not in sfx:
            sfx.append(c[3])
        if c[4] not in cfx:
            cfx.append(c[4])
        if c[5] not in rdp:
            rdp.append(c[5])
    rt = "@".join(rt)
    pfx = "@".join(pfx)
    sfx = "@".join(sfx)
    cfx = "@".join(cfx)
    rdp = "@".join(rdp)
    return rt,s,pfx,sfx,cfx,rdp

with open("rootlist.pkl", "rb") as f:
    rootlist = load(f)
out = open("add2malindo.tsv", "w", encoding="utf-8")
c = 9135 # counter utk nombor siri
spell = SpellChecker()
for t in diff:
    r,s,pfx,sfx,cfx,rdp = analisis(t, rootlist)
    print("ec-4{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\tLain\t{2}\t{2}".format(
            str(c),r,t,pfx,sfx,cfx,rdp), file=out) # Tukar "Lain" kpd nama sumber yg sesuai
# Untuk abaikan bahasa Inggeris
#for t in diff:
#    if spell.unknown([t]): #abaikan kalau bahasa Inggeris
#        r,s,pfx,sfx,cfx,rdp = analisis(t, rootlist)
#        print("ec-48{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\tMelayu-Sabah\t{2}\t{2}".format(
#                str(c),r,t,pfx,sfx,cfx,rdp), file=out)
    c += 1
out.close()
