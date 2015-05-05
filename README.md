# trígrafos
A word game! If you are given an arbitrary three-letter string, can you come up with a word that includes that string? Right now only in Spanish.

Trígrafos is meant as a game for foreign language vocabulary stretching, so this repo features both game code and corpus-processing code (for making new language versions).

## How to run the game
Make sure you have main.py, levels.list, and unigram.dict in the same folder, then open main.py. If you have Python 2.something, it should run!

## How to play the game
The game will give you three letters, such as *acu*, and prompts to you give a Spanish word that contains those letters in order (e.g. *facultad* or *acurrucarse*, meaning 'to snuggle'). You may want to have the special characters áéíóúñü handy! Also, your word must be five letters or more, just because. The better you do, the harder it gets (that is, the rarer the trigraphs become).

## Various notes
- The Spanish frequency data is gleaned from WikiCorpus Español, which is roughly 70 million tokens taken from the Spanish-language Wikipedia.
- As such, there are some flaws&mdash;for example, it may want you to find words that contain *kéb* (answers: *pokéball(s)*, *pokéblock(s)*).
- The letter pairs *rr*, *ll*, and *ch* are counted as two letters each. This approach won't always work; for example, the Catalan *l·l* really has to be treated as a unigraph.
- The script I used to generate the Spanish trigraph frequencies is included but it's not up-to-snuff.
- Maybe there should be a GUI? Or some easier way to input special characters.

## Let me know what you think!
I can be reached at: 
- såm ündèrscõre ëttîngêr ât hmç døt edu, without any diacritics
- sje[six squared plus four squared plus six] @ cornell.edu

I'd love suggestions/feedback on the game (or my e-mail obscuring methods)
