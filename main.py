# -*- coding: utf-8 -*-
# New game: trígrafos
# Trigraphs and their frequencies taken from Google Books n-Grams
# Sam Ettinger, May 2015
# sam_ettinger@hmc.edu
import pickle
import random
import os, os.path

# Determine all the language packs we have.
# We just decide each directory in here is a language.
languages = [lang for lang in os.listdir('.') if os.path.isdir(lang) and '.' not in lang]

print('Select your language:')
for i, lang in enumerate(languages):
    print('{}: {}'.format(i + 1, lang))
    
while True:
    # Make the user pick a language
    try:    
        selected = int(raw_input('Language number:\n'))
        if selected > 0 and selected <= len(languages):
            # Set the language
            language = languages[selected - 1]
            break
    except:
        pass
    
    print(u'¡No!')

print('Loading {} unigrams...'.format(language))
uni = open(language + '/unigram.dict', 'r')
unigram = pickle.load(uni)
uni.close()

print('Loading {} levels...'.format(language))
lev = open(language + '/levels.list', 'r')
levels = pickle.load(lev)
lev.close()
N = len(levels)

# Start the game!
onStreak = True
level = 0
while 1:
    trig = random.choice(levels[level].keys())
    guess = raw_input('Level {}: name a word that contains \'{}\':\n'.format(str(level+1), trig))
    if trig in guess and guess in unigram.keys():
        print(u'¡Muy bien!')
        if onStreak and level<N-1:
            level += 1
        else:
            onStreak = True
    else:    
        # Say what would have been good
        ok_answers =  levels[level][trig][1][0:]
        print('Mais non! We would have accepted: {}, etc.'.format(', '.join(ok_answers)))
        
        if len(guess) < 5:
            # This should not be a secret rule.
            print('Remember, words must be 5 letters or more.')
            
        if not onStreak and level>0:
            level += -1
        else:
            onStreak = False

#áâãàéêíóôõúçü
