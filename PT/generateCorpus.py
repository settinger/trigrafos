# -*- coding: utf-8 -*-
import re
import csv
import pickle
from collections import defaultdict
from math import log10, ceil

# Portuguese frequency data taken from http://www.clul.ul.pt/

filenames = ['../../rawPT/unigram.csv']

# Initialize dicts
unigram = defaultdict(lambda: 0)
trigraph = defaultdict(lambda: [0,[]])

# Start reading from csv (each row is of form [word, count])
for filename in filenames:
    foo = open(filename, 'rb')
    reader = csv.reader(foo)
    for row in reader:
        word = row[0]
        count = int(row[1])
        unigram[word] = count
        if len(word)>4:
            for num in range(len(word)-2):
                trig = word[num:num+3]
                if '-' not in trig:
                    trigraph[trig][0] += count
                    trigraph[trig][1] += [word]

# Finish the unigram model by converting to a regular dict
unigram = dict(unigram)

# Edit the trigraph model by converting AND ALSO keeping only five tokens that contain the trigraph
trigraph = dict(trigraph)
n = 0.0
N = float(len(trigraph.keys()))
for key in trigraph.keys():
    while len(trigraph[key][1])>5:
        # Remove least frequent word from first six; repeat
        sixwords = trigraph[key][1][0:6]
        sixcounts = [unigram[word] for word in sixwords]
        for index,word in enumerate(sixwords):
            if sixcounts[index] == min(sixcounts):
                trigraph[key][1].remove(word)
                break
    n += 1.0
    print(str(n/N)[0:6] + ' done with trigraph LM')

# Break trigraph dict into N dicts, one for each difficulty level
N = 20   # Let there be 20 difficulty levels
cut = 5  # Ignore any trigrams that appear fewer than 5 times
topCount = max([trigraph[key][0] for key in trigraph.keys()])  # Count of most frequent trigraph
# trigraph goes into one of N sub-dicts, depending on its count


def whichDict(N, cut, topCount, count):
    ''' Dictates which level of difficulty is appropriate for a certain trigraph'''
    spread = (log10(topCount) - log10(cut))/float(N)  # Log range of one difficulty level
    diff = int(ceil((log10(count) - log10(cut))/spread))
    return diff-1


# If whichdict(trigraph count) is between 1 and N, assign it to the appropriate subdict
# Initialize N dicts
levels = [dict() for num in range(N)]
for key in trigraph.keys():
    if trigraph[key][0] > cut:
        index = whichDict(N, cut, topCount, trigraph[key][0])
        levels[index][key] = trigraph[key]
levels.reverse()

print('Writing .dict files...')
out1 = open('unigram.dict', 'w')
pickle.dump(unigram, out1)
out1.close()
out2 = open('levels.list','w')
pickle.dump(levels, out2)
out2.close()

#áâãàéêíóôõúçü
