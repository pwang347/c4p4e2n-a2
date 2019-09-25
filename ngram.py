# ngram.py
# Referenced http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/

from math import log10
from collections import defaultdict, namedtuple

NGRAM_FILE = "english_quintgrams.txt"

ngrams = {}
for line in open(NGRAM_FILE):
    key, count = line.split(" ")
    ngrams[key] = int(count)

N = len(key)
ngram_sum = sum(ngrams.values())

for key in ngrams.keys():
    ngrams[key] = log10(float(ngrams[key]/N))

floor = log10(0.01/N) # this was actually a bug, but for sake of reproducibility of scores
                      # I'll keep it here
                      # should be ngram_sum not N

# we can bias the score to prioritize certain combinations
Bias = namedtuple("Bias", ["id", "factor"])

def ngram_score(decrypted_text, biases=None):
    if biases is None:
        biases = []
    score = 0
    bias_map = defaultdict(int)
    for i in range(len(decrypted_text) - N + 1):
        if decrypted_text[i:i+N] in ngrams:
            score += ngrams[decrypted_text[i:i+N]]
        else:
            score += floor
        for bias in biases:
            if decrypted_text[i:i+len(bias.id)] == bias.id:
                bias_map[bias.id] += 1
    for bias in biases:
        score *= bias.factor ** bias_map[bias.id]
    return score
