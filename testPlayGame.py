import pickle
import random

tri = open('trigraph.dict', 'r')
trigraph = pickle.load(tri)
tri.close()

uni = open('unigram.dict', 'r')
unigram = pickle.load(uni)
uni.close()

wei = open('weights.list', 'r')
weights = pickle.load(wei)
wei.close()

### Taken from http://stackoverflow.com/questions/13047806/weighted-random-sample-in-python
def weighted_choice(weights, random=random):
    """ Given a list of weights [w_0, w_1, ..., w_n-1],
        return an index i in range(n) with probability proportional to w_i. """
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        if w<0:
            raise ValueError("Negative weight encountered.")
        rnd -= w
        if rnd < 0:
            return i
    raise ValueError("Sum of weights is not positive")

# start the game! aaaa
while 1:
    trig = trigraph.keys()[weighted_choice(weights)]
    guess = raw_input('Name a word that contains \'' + trig + '\':\n')
    if trig in guess and guess in unigram.keys():
        print('Muy bien!')
    else:
        print('Mais non! We would have accepted: ' + str(trigraph[trig][1])[1:-1] + ', etc.')
