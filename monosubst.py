# monosubst.py
# Cracks mono-substitutions
#
# See results of run at crack1.txt
#

from ciphertexts import CIPHERTEXTS, Cipher, generate_key, step_key
from ngram import ngram_score
import argparse
import time

parser = argparse.ArgumentParser(description='Monoalphabetic substitution cracker')
parser.add_argument('--key')
parser.add_argument('--num_iter', type=int, default=10000)
args = parser.parse_args()

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def decipher_substitution(key, ciphertext):
    """
    Maps a letter in the key to the original letter.
    E.g. QTU -> ABC
    """
    result_builder = []
    char_map = {k: chr(i + ord("A")) for i, k in enumerate(key)}
    for c in ciphertext:
        result_builder.append(char_map[c])
    return "".join(result_builder)

for ciphertext in filter(lambda c: c.cipher == Cipher.MONO_SUBSTITUTION, CIPHERTEXTS):
    start = time.time()
    iterations = 0
    best_key = generate_key(ALPHABET) if args.key is None else args.key
    plaintext = decipher_substitution(best_key, ciphertext.value)
    best_score = ngram_score(plaintext)

    for i in range(args.num_iter):
        iterations += 1
        key = step_key(best_key)
        plaintext = decipher_substitution(key, ciphertext.value)
        score = ngram_score(plaintext)
        if score > best_score:
            best_score = score
            best_key = key
            print(best_score)

    end = time.time()
    elapsed = end - start

    print("For %d iterations in %.2f seconds, the fittest key with score=%s was:\n%s" % (iterations, elapsed, best_score, best_key))
    print("The decrypted text: %s" % decipher_substitution(best_key, ciphertext.value))
