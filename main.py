# -*- coding: utf-8 -*-
# New game: trígrafos
# Trigraphs and their frequencies taken from Wikicorpus: http://www.cs.upc.edu/~nlp/wikicorpus/
# Sam Ettinger, May 2015
# sam_ettinger@hmc.edu
import pickle
import random

uni = open('unigram.dict', 'r')
unigram = pickle.load(uni)
uni.close()

lev = open('levels.list', 'r')
levels = pickle.load(lev)
lev.close()
N = len(levels)

# Start the game!
onStreak = True
level = 0
while 1:
    trig = random.choice(levels[level].keys())
    guess = raw_input('Level ' + str(level+1) + ': name a word that contains \'' + trig + '\':\n')
    if trig in guess and guess in unigram.keys():
        print(u'¡Muy bien!')
        if onStreak and level<N-1:
            level += 1
        else:
            onStreak = True
    else:
        print('Mais non! We would have accepted: ' + levels[level][trig][1][0] + ', ' + levels[level][trig][1][1] + ', ' + levels[level][trig][1][2] + ', ' + levels[level][trig][1][3] + ', ' + levels[level][trig][1][4] + ', etc.')
        if not onStreak and level>0:
            level += -1
        else:
            onStreak = False

#áéíóúñü
