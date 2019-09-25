# playfair.py
# Playfair cipher cracker
#
# See results of run at crack2a.txt
#

from ciphertexts import CIPHERTEXTS, Cipher, generate_key, square_key, step_key
from ngram import ngram_score, Bias
from collections import namedtuple, defaultdict
from math import exp
import argparse
import random
import string
import time

parser = argparse.ArgumentParser(description='Playfair cracker')
parser.add_argument('--parent')
parser.add_argument('--default_temp', type=int, default=20)
parser.add_argument('--default_step', type=int, default=2)
parser.add_argument('--default_count', type=int, default=1000)

args = parser.parse_args()

Digram = namedtuple("Digram", ["first", "second"])

def decipher_playfair(key, ciphertext):
    """
    Deciphers playfair, ignoring the first rule.
    Referenced https://en.wikipedia.org/wiki/Playfair_cipher#Description
    """

    if len(ciphertext) % 2 == 1:
        raise Exception("Should not have ciphertext of odd length")
    
    str_builder = []
    key_square, key_mapping = square_key(key)

    # apply Playfair rules
    for idx in range(0, len(ciphertext), 2):

        if ciphertext[idx] == "J":
            raise Exception("Should not have the letter J in ciphertext")

        digram = Digram(ciphertext[idx], ciphertext[idx+1])

        # rule 2
        if key_mapping[digram.first].y == key_mapping[digram.second].y:
            str_builder.append(key_square[key_mapping[digram.first].y][(key_mapping[digram.first].x - 1) % 5])
            str_builder.append(key_square[key_mapping[digram.second].y][(key_mapping[digram.second].x - 1) % 5])
        # rule 3
        elif key_mapping[digram.first].x == key_mapping[digram.second].x:
            str_builder.append(key_square[(key_mapping[digram.first].y - 1) % 5][key_mapping[digram.first].x])
            str_builder.append(key_square[(key_mapping[digram.second].y - 1) % 5][key_mapping[digram.second].x])
        # rule 4
        elif key_mapping[digram.first].x != key_mapping[digram.second].x \
            and key_mapping[digram.first].y != key_mapping[digram.second].y:
            str_builder.append(key_square[key_mapping[digram.first].y][key_mapping[digram.second].x])
            str_builder.append(key_square[key_mapping[digram.second].y][key_mapping[digram.first].x])

    return "".join(str_builder)

PLAYFAIR_KEY_ALPHABET = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")
# note that COMMA could be rendered both COMMA and COMXMA
biases = [Bias("THE", 1.05), Bias("AND", 1.05), Bias("DOT", 1.05), Bias("COMXMA", 3), Bias("COMMA", 3)]

def crack_playfair(temp, step, default_count, default_key=None):
    """
    Cracks Playfair.
    Referenced pseudocode for SA:
    http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-playfair/
    """
    for ciphertext in filter(lambda c: c.cipher == Cipher.PLAYFAIR, CIPHERTEXTS):
        start = time.time()
        if default_key is not None:
            parent_key = default_key
            deciphered = decipher_playfair(parent_key, ciphertext.value)
            import pdb; pdb.set_trace()
            p_fitness = ngram_score(deciphered, biases=biases)
            print("Using preset key with fitness: %s" % p_fitness)
        else:
            parent_key = generate_key(PLAYFAIR_KEY_ALPHABET)
            deciphered = decipher_playfair(parent_key, ciphertext.value)
            p_fitness = ngram_score(deciphered, biases=biases)
            print("Starting new key with fitness: %s" % p_fitness)
        iterations = 0
        seen = set()
        while temp >= 0:
            count = default_count
            while count > 0:
                iterations  += 1
                child_key = step_key(parent_key, seen=seen)
                deciphered = decipher_playfair(child_key, ciphertext.value)
                c_fitness = ngram_score(deciphered, biases=biases)
                dF = c_fitness - p_fitness
                if dF >= 0:
                    parent_key = child_key
                    p_fitness = c_fitness
                    print(p_fitness)
                elif temp > 0:
                    probability = exp(dF / temp)
                    if (random.random() <= probability):
                        parent_key = child_key
                        p_fitness = c_fitness
                        print("*%s" % p_fitness)
                count -= 1
            temp -= step

        end = time.time()
        elapsed = end - start

        print("For %d iterations in %.2f seconds, the fittest key with score=%s was:\n%s" % (iterations, elapsed, p_fitness, parent_key))
        print("The decrypted text: %s" % decipher_playfair(parent_key, ciphertext.value))
        return p_fitness, parent_key

best_key = None
best_fitness = None
while True:
    fitness, key = crack_playfair(default_key=args.parent, temp=args.default_temp, step=args.default_step, default_count=args.default_count)
    if best_fitness is None or fitness > best_fitness:
        best_fitness = fitness
        best_key = key
    print("Best key so far is %s with fitness %s" % (best_key, best_fitness))
