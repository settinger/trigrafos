# -*- coding: utf-8 -*-
import re
import pickle
from collections import defaultdict
from math import log10, ceil

badwords = ['title', 'nonfiltered', 'processed', 'dbindex']
filenames = ['../rawESP/es01', '../rawESP/es02', '../rawESP/es03', '../rawESP/es04', '../rawESP/es05', '../rawESP/es06', '../rawESP/es07', '../rawESP/es08', '../rawESP/es09', '../rawESP/es10', '../rawESP/es11', '../rawESP/es12', '../rawESP/es13', '../rawESP/es14', '../rawESP/es15', '../rawESP/es16', '../rawESP/es17', '../rawESP/es18', '../rawESP/es19', '../rawESP/es20', '../rawESP/es21', '../rawESP/es22', '../rawESP/es23', '../rawESP/es24', '../rawESP/es25', '../rawESP/es26', '../rawESP/es27', '../rawESP/es28', '../rawESP/es29', '../rawESP/es30', '../rawESP/es31', '../rawESP/es32', '../rawESP/es33', '../rawESP/es34', '../rawESP/es35', '../rawESP/es36', '../rawESP/es37', '../rawESP/es38', '../rawESP/es39', '../rawESP/es40', '../rawESP/es41', '../rawESP/es42', '../rawESP/es43', '../rawESP/es44', '../rawESP/es45', '../rawESP/es46', '../rawESP/es47', '../rawESP/es48', '../rawESP/es49', '../rawESP/es50', '../rawESP/es51', '../rawESP/es52', '../rawESP/es53', '../rawESP/es54', '../rawESP/es55', '../rawESP/es56', '../rawESP/es57']
#filenames = ['../rawESP/es01']

# Initialize dicts
unigram = defaultdict(lambda: 0)
trigraph = defaultdict(lambda: [0,[]])
for filename in filenames:
    # Read in a chunk of the raw corpus
    with open(filename, 'r') as content_file:
        content = content_file.read()
    # Tokenize a chunk of the raw corpus
    pattern = ur'[ (][a-záéíóúñü]+'
    rawtokens = re.findall(pattern, content)
    tokens = [token[1:] for token in rawtokens if len(token)>5 and token[1:] not in badwords]
    # Create unigram, trigraph models
    for token in tokens:
        unigram[token] += 1
        for num in range(len(token)-2):
            trigraph[token[num:num+3]][0] += 1
            if token not in trigraph[token[num:num+3]][1]:
                trigraph[token[num:num+3]][1] += [token]
    print('Finished with ' + filename)

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

print('Writing .dict files...')

out1 = open('unigram.dict', 'w')
pickle.dump(unigram, out1)
out1.close()
out2 = open('trigraph.dict','w') # No longer necessary!
pickle.dump(trigraph, out2)
out2.close()
out3 = open('levels.list','w')
pickle.dump(levels, out3)
out3.close()

#áéíóúñüÁÉÍÓÚÑÜ'''
