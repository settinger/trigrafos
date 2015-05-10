# -*- coding: utf-8 -*-
import re
import pickle
from collections import defaultdict
from math import log10, ceil

# Italian frequency data taken from Google Books n-Grams

filenames = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'other']

# Initialize dicts
unigram = defaultdict(lambda: 0)
trigraph = defaultdict(lambda: [0,[]])

# Start reading from ngram (ngram TAB year TAB match_count TAB volume_count NEWLINE)
for letter in filenames:
    filename = '../../rawIT/googlebooks-ita-all-1gram-20120701-' + letter
    foo = open(filename, 'rb')
    # Keep track of lines, for progress updates
    with open(filename) as f:
        size = sum(1 for _ in f)
        print('Reading a file with ' + str(size) + ' lines...')
    counter = 0.0
    for line in iter(foo):
        # Locate tabs
        tab1 = line.find('\t')
        tab2 = line.find('\t', tab1+1)
        tab3 = line.find('\t', tab2+1)
        word = line[0:tab1]
        # Verify we care about this word (lowercase, no special characters, 5+ letters long)
        if word.isalpha() and word.islower() and len(word)>4:
            count = int(line[tab2+1:tab3])  # Count instances
            unigram[word] += count
        counter += 1
        '''if counter % (size/10000) == 0.0:
            print(str(round(counter/size, 4)) + ' of letter ' + letter)'''

# Remove all words with a total count less than, say, 190, before doing trigraph
cutoff = 190
newUnigram = dict()
for key in unigram.keys():
    if unigram[key] > cutoff:
        newUnigram[key] = unigram[key]
        for num in range(len(key)-2):
            trig = key[num:num+3]
            trigraph[trig][0] += unigram[key]
            trigraph[trig][1] += [key]
        
# Finish the unigram model by converting to a regular dict
unigram = dict(newUnigram)

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
