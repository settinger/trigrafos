# -*- coding: cp1252 -*-
import re
import pickle
from collections import defaultdict

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
    pattern = ur'[ ][a-záéíóúñü]+'
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

# Finish the trigraph model by converting AND ALSO keeping only five tokens that contain the trigraph
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

print('Writing .dict files...')

out1 = open('unigram.dict', 'w')
pickle.dump(unigram, out1)
out1.close()
out2 = open('trigraph.dict','w')
pickle.dump(dict(trigraph), out2)
out2.close()

#áéíóúñüÁÉÍÓÚÑÜ'''
